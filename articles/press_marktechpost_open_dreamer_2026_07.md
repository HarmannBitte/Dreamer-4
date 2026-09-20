<!-- source: https://www.marktechpost.com/2026/07/25/meet-open-dreamer-a-jax-flax-reproduction-of-the-dreamer-4-world-model-pipeline-with-the-full-training-recipe-published/
     fetched: 2026-09-20T13:44:24Z -->

A small group of AI researchers ([Francesco Sacco](https://x.com/FrancescoSacco1), [Diego Martí](https://x.com/martidiegom), and [Edward Hu](https://x.com/edward_s_hu)) have released [Open Dreamer](https://next-state.github.io/open-dreamer/), an open implementation of the [Dreamer 4](https://danijar.com/project/dreamer4/) world-model pipeline written in JAX and Flax NNX. The research is sponsored by [Reactor](https://www.reactor.inc/).

## **What actually shipped**

Two repositories were released. [next-state/open-dreamer](https://github.com/next-state/open-dreamer) holds the training pipeline: a causal video tokenizer, an action-conditioned latent dynamics model, rollout generation, and FVD scoring. [reactor-team/open-dreamer](https://github.com/reactor-team/open-dreamer) holds a minimal local rollout harness that generates frames from an MP4 and a matching action file.

A third artifact is the browser demo hosted on the Reactor runtime. It streams a generated Minecraft world in real time and exposes a Game ⟷ Dream toggle that hands the stream from the real game to the world model frame by frame.

The stated objective was to reproduce the [Dreamer 4 research](https://arxiv.org/abs/2509.24527). The research team deliberately avoided methods outside that research paper to keep the search space narrow. They started on CoinRun, a procedurally generated 2D platformer trainable on a single GPU, then scaled the working pipeline to Minecraft/VPT-style gameplay video.

## **Architecture: one backbone, two models**

Both the tokenizer and the dynamics model use the same block-causal transformer backbone. That backbone alternates two attention types. Space layers propagate information among the elements of a single frame. Causal time layers propagate information between frames.

The tokenizer is a transformer-based Masked Autoencoder rather than a VAE. The team reports roughly 100× compression and notes the design needs no KL or adversarial loss. Masking, they argue, makes the latent space more diffusible.

The dynamics model performs next-frame prediction and is trained with diffusion forcing, flow matching, and shortcut models. It also predicts the next action. Rather than alternating between a separate transition module and policy, the rollout is folded into per-timestep blocks of (previous action, state, policy). Spatial attention runs inside each block; causal temporal attention connects blocks across time.

Critically, world-model tokens cannot read the agent token. Task and policy information can therefore influence future states only through the next action.

## **The training recipe, as configured**

The shipped Minecraft configs make the recipe concrete.

The dynamics model is 1.6B parameters: 30 block-causal layers, `d_model` 1920, 30 attention heads, and 3 KV heads for grouped-query attention. Every fourth layer is a time-attention layer. Each timestep carries 32 learned register tokens, and `packing_factor: 2` packs neighbouring tokenizer latents into each dynamics spatial token. Time attention uses a 192-step sliding window.

Training runs for 200,000 steps with Muon, a WSD schedule, and a peak learning rate of 3e-4. Shortcut/bootstrap samples switch on at step 100,000 at a 0.25 batch fraction. EMA decay is 0.999.

The tokenizer config emits 512 latent tokens per frame at a bottleneck width of 16. Raw 360×640 frames are padded to 368×640 so both dimensions divide into 16×16 patches. Encoder depth is 12 at `d_model` 1536; decoder depth is 8 at `d_model` 1024. MAE masking probability tops out at 0.9, and LPIPS is applied at weight 0.2 on half the timesteps.

VPT actions are parsed into 27 binary action channels plus 121 categorical mouse classes, with no continuous channels.

## **Computemaxxing and the memory wall**

The research team reports 57–58% model FLOPs utilization, against a stated 60% benchmark for healthy transformer training. The reasoning is a roofline argument. On a B200, the crossover between bandwidth-bound and compute-bound sits at 292 FLOP/byte. Feeding 256 frames per GPU pushes the workload past that ridge point.

Sharding went the other way from expectations. At 1.6B parameters the model state — parameters, gradients, optimizer state, and EMA — occupied roughly 24 GiB, which fits on a B200. Activations were the real cost. The research team tried data parallelism, FSDP, tensor parallelism, and sequence parallelism, then settled on plain data parallelism plus activation checkpointing.

Dataloading was solved by pre-tokenizing the entire dataset into `.arrayrecord` files, then using Grain with a GPU-side prefetch buffer. ffmpeg decoding was not fast enough to keep the GPUs fed.

## **The stability section is the real payload**

The research team is explicit that stability consumed the largest share of their time. Their key observation: most stability problems occur *despite* the loss going down. MSE improves smoothly while generation quality degrades.

Six fixes are documented. Muon replaced LaProp, which spiked randomly and increasingly often, across two runs of roughly 400 B200 hours each. EMA weights are treated as mandatory for diffusion inference. Mixed precision is boundary-sensitive: parameters stay float32, BF16 covers most matmul activations and attention inputs, and float32 is kept for normalization and the dynamics flow output head.

On loss weighting, they use x-prediction with a v-space loss, which reduces to a weighting term similar to Dreamer 4’s but with a squared denominator. They report a small but noticeable improvement. Minibatch barycentric optimal transport between noise and latent sequences made rollout generation more stable. μ-parametrization was tested and judged unnecessary, partly because Muon holds hyperparameters steadier across model sizes.

One further result from the CoinRun phase: an iso-FLOPs sweep put compute-optimal scaling at roughly and .

## **What is not in the box**

The repository does not include the behaviour-cloning or RL training loop; a full Dreamer 4 BC/RL agent loop is listed as an open roadmap item. The CoinRun policy work described in the post was not used for Minecraft and was not released.

The post also does not publish FVD scores, though `scripts/eval_fvd.py` ships with an I3D-based harness configured for 4 context frames and a 240-frame horizon.

## **Key Takeaways**

- Open Dreamer reproduces the Dreamer 4 pipeline in JAX/Flax NNX, with training code and a Minecraft demo.
- The dynamics model is 1.6B parameters, 30 layers, `d_model` 1920, trained 200K steps with Muon.
- Reported engineering numbers: 57–58% MFU on B200, 256 frames per GPU, ~24 GiB model state.
- Stability, not throughput, was the bottleneck; loss curves hid most generation-quality regressions.

*Check out the [blog post and demo](https://next-state.github.io/open-dreamer/), the [training repo](https://github.com/next-state/open-dreamer), the [inference repo](https://github.com/reactor-team/open-dreamer), and [Reactor on X](https://x.com/reactorworld/status/2080711388738249132). All credit for this research goes to the researchers of this project.*

Asif Razzaq is the CEO of Marktechpost AI Media Inc.. As a visionary entrepreneur and engineer, Asif is committed to harnessing the potential of Artificial Intelligence for social good. His most recent endeavor is the launch of an Artificial Intelligence Media Platform, Marktechpost, which stands out for its in-depth coverage of machine learning and deep learning news that is both technically sound and easily understandable by a wide audience. The platform boasts of over 2 million monthly views, illustrating its popularity among audiences.