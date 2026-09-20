<!-- source: https://findlamp.github.io/dreamer-mc.github.io/
     fetched: 2026-09-20T13:37:06Z -->

We are thrilled to present our latest work: a real-time, infinite video generation model for Minecraft, developed as an adaptation of the DreamerV4 architecture. By leveraging this powerful foundation, we have achieved true autoregressive generation that streams indefinitely, efficiently managing temporal context to avoid the redundant re-computation of past frames. This system goes far beyond simple navigation; it captures the rich, emergent complexity of the Minecraft sandbox, seamlessly simulating intricate interactions—from the physics of archery and horse riding to the granular details of mining and consuming items.

### Key Technical Innovations

- 
                    **MAE Tokenizer for Enhanced Representation:** Instead of a standard VQ-VAE, we utilize a Masked Autoencoder (MAE) as our visual tokenizer. This enriches the latent space with stronger semantic signals, allowing the model to learn complex interactions in Minecraft more effectively than pure reconstruction methods.
- 
                    **x0 Prediction to Eliminate Drift:** As detailed below, we mitigate long-horizon drift by adopting an $ x_0 $ prediction objective. This ensures that the model predicts the clean original state at each step rather than the noise residual, effectively eliminating error accumulation and maintaining visual crispness over thousands of frames.
- 
                    **Infinite Context with Ring Buffer & Sliding KV Cache:** To support truly infinite generation without exploding memory usage, we implemented a ring buffer mechanism. Crucially, we dynamically re-apply Rotary Positional Embeddings (RoPE) during inference, allowing the model to stream continuously without being constrained by the training sequence length.
- 
                    **CUDA Graphs for Real-Time Inference:** Efficiency is paramount. We wrapped our inference pipeline using CUDA Graphs to minimize the overhead of CPU-side kernel launching. This eliminates the CPU bottleneck, allowing the GPU to execute operations continuously at interactive frame rates.

## The Challenge of Infinite Generation: Conquering Error Accumulation

                One of the most persistent hurdles in autoregressive video generation is **error accumulation**. In a standard autoregressive setup, each new frame is generated based on the previous one; consequently, minor imperfections in early frames compound over time, leading to "drift." As the generation horizon extends, this drift manifests as severe geometric distortion, blurring, and significant color shifts, eventually causing the simulation to collapse into unintelligible noise.
            

                Previous approaches have attempted to mitigate this with computationally expensive workarounds. Methods like **Context as Memory** effectively reduce drift by maintaining a bank of historical frames, but they often require re-computing or re-attending to past latents, which breaks the promise of constant-time inference. Other state-of-the-art attempts—such as **Self-Forcing** or **Rolling Forcing**—try to bridge the gap between training and inference. These methods typically involve fine-tuning a bidirectional model with "diffusion forcing" and then performing autoregressive distillation using *Distribution Matching Distillation (DMD)*. While these techniques delay the onset of degradation, they are not immune to it; once the generation length significantly exceeds the training window, the distribution inevitably shifts, resulting in the familiar artifacts of "melting" structures and washed-out colors.
            

                Our model solves this fundamentally by adopting the **$ x_0 $ prediction** objective introduced in DreamerV4. Instead of predicting the noise residual ($ \epsilon $) at every step—which allows errors to accumulate in the latent space—the model is trained to predict the clean, original image state ($ x_0 $) directly. This effectively "resets" the noise floor at each step, preventing microscopic errors from compounding. This architectural choice is the key to our model's ability to sustain crisp, coherent gameplay visuals indefinitely, without the need for expensive history re-computation.
            

## Model Architecture

Unlike traditional video transformers that operate on VAE latents, our model learns a compact, semantic latent representation of the world. This allows us to separate the visual compression from the dynamics learning, achieving high-resolution output with manageable computational costs.

### 1. Causal Gather-Token Tokenizer

To achieve a high-level semantic understanding of the Minecraft world, we designed a Causal Gather-Token Temporal Autoencoder (Figure 3). Instead of processing the entire image grid directly, we introduce a set of learnable Gather Tokens ($ G $). These tokens act as the primary information bottleneck; they query and aggregate features from the masked image patches via cross-attention, compressing the visual input into a compact latent representation $ z $.

Crucially, to ensure stability in video generation, this process is not processed in isolation per frame. We incorporate Temporal Attention layers that allow the gather tokens to attend to the gather tokens of previous frames. This causal temporal link ensures that the latent representation remains consistent over time, significantly reducing flickering and ensuring that the semantic understanding of the world evolves smoothly.

### 2. Dynamic Model: Decomposed Spatial-Temporal Attention

- 
                    **Input Sequence:** At each frame, the input sequence is formed by directly concatenating the image patch tokens with specific control tokens: a Timestep Token, a Stride Token, and an Action Token.
- 
                    **Spatial Attention (Simplified & Fast):** Departing from standard Diffusion Transformer (DiT) architectures that rely on AdaIN (Adaptive Instance Normalization) to inject conditioning signals, we feed the Timestep and Stride tokens directly into the self-attention layers alongside the image tokens. By eliminating the complex and computationally expensive AdaIN modulation modules, we significantly simplify the architecture and accelerate inference speed. This streamlined design ensures the model remains lightweight enough for real-time deployment while still effectively conditioning the generation on the current state and control inputs.
- 
                    **Temporal Attention (Inter-Frame):** In the subsequent temporal layers, we restrict attention exclusively to the image patch tokens across frames. The control tokens are excluded from this step. This design efficiently propagates the "physics" of the world through time while keeping control signals localized to their specific steps, preventing signal leakage and further reducing computational overhead.

## Complex Interactions: Beyond Simple Navigation

Previous iterations of world models, including earlier Dreamer variants, were primarily benchmarked on simple locomotion tasks—essentially learning to "run" or "walk" through a static environment. While impressive, these models often struggled with the fine-grained manipulation and causal physics required for a true sandbox simulation.

                Dreamer-MC significantly raises the bar by mastering a diverse array of **complex, multi-step interactions**. The model does not just predict camera movement; it accurately simulates the cause-and-effect of tool usage, navigation, and environmental modification.
            

### 01. Boating & Water Physics

### 02. Consuming Items

### 03. Archery & Projectiles

### 04. Fluid Dynamics (Bucket)

### 05. Mining & Breaking Blocks

### 06. Sleeping / Time Skip

### 07. Nether Portals & Teleportation

## Inference Optimization

Achieving true real-time generation at high quality required moving beyond standard PyTorch implementations, with a heavily optimized inference pipeline designed for long-context workloads on a single H200 GPU.

### 1. Infinite Context via Ring Buffer & RoPE Re-indexing

                Standard sliding-window implementations often rely on shifting memory (e.g., `torch.roll` or `memmove`) to discard old frames and make room for new ones. This data movement incurs a significant $ O(N) $ overhead at every step.
            

We solve this using a Ring Buffer KV Cache. Instead of shifting data, we maintain a fixed-size buffer and simply advance a write pointer, overwriting the oldest frame with the newest one ($ O(1) $ complexity). However, this introduces a new challenge: the physical position of a frame in the buffer no longer matches its logical temporal position, breaking standard Rotary Positional Embeddings (RoPE).

To address this, we implement **RoPE Re-indexing**:

- 
                    **Pre-cached RoPE:** We pre-compute and cache the RoPE rotation matrices for the maximum context window size during initialization.
- 
                    **Dynamic Re-indexing:** During inference, we dynamically map the logical sequence order (Current Frame $ t $, Past Frame $ t-1 $, etc.) to the physical indices in the ring buffer. We then gather the corresponding position embeddings from our static RoPE cache. This effectively "slides" the positional information over the circular buffer, ensuring the model always sees a consistent temporal window without ever physically moving the heavy KV data.

### 2. Removing CPU Overhead with CUDA Graphs

In autoregressive generation, the model executes thousands of small GPU kernels (e.g., LayerNorm, Attention, MLP) per frame. In a standard Python loop, the CPU overhead of dispatching these kernels often exceeds the actual GPU execution time, creating a severe bottleneck.

To eliminate this, we utilize CUDA Graphs. We capture the entire inference step—including the Ring Buffer update and RoPE application—into a static execution graph. This allows the GPU to launch the entire sequence of kernels autonomously, bypassing the Python/CPU bottleneck entirely. This optimization reduced our frame generation latency by over 40%, enabling high-resolution generation at steady interactive framerates.

## Limitations & Future Work

While our model demonstrates the feasibility of real-time, infinite video generation, it remains a stepping stone toward a truly general-purpose world model. Several limitations currently exist that we plan to address in future iterations:

- 
                    **Tokenizer Reconstruction Fidelity:** Although our MAE-based tokenizer excels at capturing semantic logic and game mechanics, this comes at the cost of fine-grained visual reconstruction. High-frequency details—such as specific block textures or text on signs—can sometimes appear blurry or lack sharpness. Improving the tokenizer's compression rate without sacrificing pixel-level fidelity is a primary target for our next update.
- 
                    **Temporal Stability & Consistency:** While x0 prediction significantly mitigates long-term drift, inter-frame flickering can still occur during rapid camera movements or complex scene transitions. Achieving perfectly smooth, temporal coherence that matches the stability of a game engine remains an open challenge.
- 
                    **Imperfect Context Utilization:** Our model currently utilizes a 256-frame context window. However, having the context available in the buffer does not guarantee perfect recall. We have observed instances where the model struggles to maintain consistency for objects or events that occurred early in the context window (e.g., "forgetting" a block placed 200 frames ago). Improving the attention mechanism's ability to effectively utilize the full depth of the sliding window is crucial for complex, long-duration tasks.
- 
                    **Domain Specificity & Scale:** Currently, the model is trained exclusively on Minecraft data. It is a "specialist" model with a relatively modest parameter count. Our ultimate vision is to scale up both the model size and the training data. Future work will involve expanding training to include other video games and, eventually, real-world video data, moving closer to a General World Model capable of simulating diverse physical laws and environments.

## Citations

```
@article{hafner2025dreamerv4,
    title   = {Dreamer-MC: A Real-Time Autoregressive World Model for Infinite Video Generation},
    author  = {Ming Gao, Yan Yan, ShengQu Xi, Yu Duan, ShengQian Li, Feng Wang},
    year    = {2026},
    url     = {https://findlamp.github.io/dreamer-mc.github.io/}
}
```
                        ## References

```
@article{hafner2025dreamerv4,
    title   = {Training Agents Inside of Scalable World Models},
    author  = {Hafner, Danijar and Yan, Wilson and Lillicrap, Timothy},
    journal = {arXiv preprint arXiv:2509.24527},
    year    = {2025},
    url     = {https://arxiv.org/abs/2509.24527}
}
```
                        ```
@article{chen2025maetok,
    title   = {Masked Autoencoders Are Effective Tokenizers for Diffusion Models},
    author  = {Chen, Hao and Zhang, Michael and Li, Yuxin and others},
    journal = {International Conference on Machine Learning (ICML)},
    year    = {2025},
    url     = {https://arxiv.org/abs/2502.03444}
}
```
                        ```
@article{huang2025selfforcing,
    title   = {Self Forcing: Bridging the Train-Test Gap in Autoregressive Video Diffusion},
    author  = {Huang, Xun and Li, Zhengqi and He, Guande and Zhou, Mingyuan and Shechtman, Eli},
    journal = {arXiv preprint arXiv:2506.08009},
    year    = {2025},
    url     = {https://arxiv.org/abs/2506.08009}
}
```
                        ```
@article{liu2025rolling,
    title   = {Rolling Forcing: Autoregressive Long Video Diffusion in Real Time},
    author  = {Liu, Kunhao and Hu, Wenbo and Xu, Jiale and Shan, Ying and Lu, Shijian},
    journal = {arXiv preprint arXiv:2509.25161},
    year    = {2025},
    url     = {https://arxiv.org/abs/2509.25161}
}
```
                        ```
@article{yu2025context,
    title   = {Context as Memory: Scene-Consistent Interactive Long Video Generation},
    author  = {Yu, Jiwen and Bai, Jianhong and Qin, Yiran and Liu, Quande and others},
    journal = {arXiv preprint arXiv:2506.03141},
    year    = {2025},
    url     = {https://arxiv.org/abs/2506.03141}
}
```
                        Create AI Team

Contact: dujinshidai30@gmail.com