<!-- source: https://next-state.github.io/open-dreamer/
     fetched: 2026-09-20T13:37:05Z -->

One of the most time-consuming parts of doing science is climbing up to the shoulders of giants. While this can be a very instructive experience, sometimes it’s nice to be teleported right on top of them and get to work right away, pushing the boundary of human knowledge.

In the last few months, with support from Reactor, we’ve been working on a frontier-level world model. We are releasing and open-sourcing the model and training code, and sharing all the lessons we learned along the way in this blog post. We want to make frontier research accessible to everyone and hope this will accelerate progress in the field.

You can also play with our model thanks to the Reactor runtime!

          We do these things not because they are easy, but because we thought they were going to be easy.
      

When starting a new project, you have to define:

- The goal.
- The starting point.
- The search space.

        Our main objective was to reproduce the Dreamer4 paper 

We purposefully refrained from using different methods that were not in the original paper as that would have made the search space wider.

This is CoinRun: it’s a 2D platform game where each level is procedurally generated. As the name suggests, the goal is to run to get the coin.

With this simple game, it is possible to do every step of the Dreamer4 paper, with some nice added benefits:


- Just one GPU (much simpler to debug).
- A fast iteration loop (much shorter training time).
- Once done, the codebase will have all the core logic ready and working.

The architecture has two main parts: the tokenizer and the dynamics model. Both use the same model-architecture backbone: the block-causal transformer.

What sets it apart is that there are two different attention-based layers:

- **Space Layer:** information propagates among all the elements that represent a single frame.
- **Causal Time Layer:** information propagates between different frames.

If you have ever trained a VAE in the past, you know how terrible of an experience that is. Most of the time the wisest thing to do is to give up and take an off-the-shelf one.

      In this project we’ve trained a transformer-based Masked Autoencoder 

This architecture is really cool because:

- Masking makes the latent space more diffusible.
- There is no need for KL or adversarial loss.
- It’s very fast to train.
- It’s scalable.
- All of the above make it easier to train than a typical VAE.

      World models fundamentally work by doing “next frame prediction”. Each frame is generated as an image conditioned on the previous ones. The dynamics model is trained with diffusion forcing 

Other than predicting just the next frame, we worked on predicting the next action as well. Typically, the rollout alternates between the world and the agent. Given the previous action $a_{t-1}$, the dynamics predicts the next state $s_t$; the policy $\pi_t$ observes that state and samples the next action:

Evaluating the transition and policy as separate modules would require repeatedly moving between them. It would also prevent them from sharing the same representation and transformer parameters. Instead, we would like to process all timesteps in parallel during training and reuse the same computation for both the world and the agent.

This architecture folds the sequence into blocks:

$$ B_t = (a_{t-1}, s_t, \pi_t) $$
Within each block, spatial attention implements $(a_{t-1} \to s_t \to \pi_t)$.

What does $s_t$ contain? The state is the part generated through diffusion—or, more precisely, the model diffuses its latent spatial tokens. The state computation therefore includes:

- a noise-level and shortcut step-size token describing how far the model should advance in one denoising step, following Shortcut Models ;
- spatial latent tokens representing the visual state;
- register tokens, which provide shared workspace for internal computation. 

Together, these tokens let each space layer turn the previous action and a noisy latent into the next clean latent state.

    As mentioned before, our first experiments were in CoinRun.

    We first trained the tokenizer and also ran some scaling experiments. Interestingly, the compute-optimal number of parameters and number of data points scale as the square root of compute!
  

      As Karpathy puts it 

      “this really didn't have to be the case, it could have been something else and complicated and a function of the model size [...] but nature decided that compute optimal Transformers fall exactly on a straight line (what???)”
  

We first tried to train a world model with random actions, but when we tried playing with the model, we found the experience quite terrible.

          To solve this, we trained a very simple RL agent to collect trajectories. We then trained a dynamics model, followed by a simple policy with a behaviour-cloning objective.

While far from optimal, the policy learns to run and jump to the right to get the coin. This showed that our pipeline was working end-to-end, and we were able to scale things up for Minecraft.

From this point on, debugging became much harder, and scaling from a working CoinRun model to Minecraft consumed most of our time. By documenting the failure modes and fixes, we hope to make this phase substantially faster for you.

The two main challenges when scaling up are squeezing as much compute as possible out of the available GPUs and making sure everything is stable.

We used JAX because the XLA compiler is great for efficient and scalable SPMD programs.

We were able to achieve around 57–58% model FLOPs utilization (MFU). In this section, we’ll explain how.

What determines if a computation is compute bound or memory bound is the arithmetic intensity.

The arithmetic intensity represents how many FLOPs you do for every byte you move from memory. On a B200, the roofline crosses over at 292 FLOP/byte. Below that point, you are bandwidth-bound. Above it, you are compute-bound.

For transformer training, arithmetic intensity improves as you increase the number of tokens per GPU because weights are reused across every token in the batch.

In general, when doing world modelling, it should be possible to make sure that your training script is compute-bound. This is because even a short video is made of lots of tokens.

In our case we discovered that feeding 256 frames per GPU would be more than enough to be in the compute-bound region. In practice it’s impossible to reach 100% MFU and 60% is considered a very healthy value of transformer training.

      For more details on how to do this kind of analysis, check the scaling book 

At 1.6B parameters, the model state — parameters, gradients, optimizer state, and EMA — took around 24 GiB. That is large but still manageable on a B200. The real memory cost came from activations. Long video sequences create huge intermediate tensors, which must be kept around for the backward pass. Even with a batch size of one video sequence per GPU, we still needed activation checkpointing to fit training in memory.

So instead of aggressively sharding the model, we focused on making the per-GPU batch fit.

We tried data parallelism, FSDP, tensor parallelism, and sequence parallelism. In practice, DP and FSDP worked best. Since the model state already fit comfortably, FSDP did not buy us much, while it added extra communication and a little more complexity. We therefore used plain data parallelism.

Also, because each GPU performed substantial local computation before gradient synchronization, communication overhead remained small relative to compute.

Even with “just” 256 frames per device, storing the activations will cause an OOM error. Instead of storing every intermediate activation during the forward pass, we stored only some of them and recomputed the missing ones during the backward pass. This costs relatively few FLOPs, but it saves a lot of memory.

GPUs have to run in lockstep. The only way we’ve been able to guarantee that they stay in sync is to ensure that the model sees input tensors that always have the same shape. This means that, if you are using batches with variable frame lengths, you need to reshape and mask them accordingly to make them consistent.

The last bottleneck comes from keeping the GPUs well fed. Videos are heavy and decoding them with ffmpeg is not fast enough to keep the GPUs warm. So we pre-tokenized the entire dataset and saved it in .arrayrecord format.

Then, for dataloading, we used Grain and added a GPU-side prefetch buffer to preallocate the data directly on the GPUs, ready to go.

We believe this section will be the most valuable for practitioners, as it focuses on the problems that repeatedly blocked our progress and the lessons we learned while overcoming them.

Stability issues haunted this project from beginning to end. More than any other challenge, they consumed the largest share of our time.

      Unlike syntax errors, which immediately halt execution, or synchronization bugs, where the failure mode is usually visible, stability issues are far more elusive. They often emerge only at large scales—high data volumes, long training runs, and significant amounts of compute. As a result, they can take days or even weeks to surface. And when they finally do, the root cause is rarely apparent. As a matter of fact, most stability problems happen **despite** the loss going down! MSE goes down smoothly, but the generation quality degrades significantly.
  

Let’s start from the simplest to hardest ones.

      We compared Muon 

      By contrast, Muon proved to be much more stable and yielded much lower losses.
  

This is the simplest stability problem because it’s the only one that is visible in the loss curve.

In diffusion modelling, doing inference with online weights yields subpar results. Using the exponential moving average of the parameters is a must. $$ \theta_\textrm{EMA} \leftarrow \beta \theta_\textrm{EMA} + (1-\beta)\theta $$

Modern AI accelerators are optimized for BF16, but some operations still require higher precision. Keep the parameters in float32; use BF16 for most matrix-multiplication activations and attention inputs; and use float32 for normalization, selected sinusoidal and normalization helpers, optional attention weights, and the dynamics flow output head.

These precision boundaries are important: getting them wrong can destabilize both training and generation.

      Flow-matching models are usually trained to directly predict the velocity field that denoises the input (v-prediction). Recently, researchers have found that directly predicting the clean data from noisy inputs (x-prediction) with v-space loss results in higher-quality generation 

World models also have an extra inductive bias in favour of x-prediction: since all context frames are in x-space, it would only be natural to ask the neural network to predict the next frame in x-space as well.


In practice, doing x-prediction with v-space loss reduces to a loss-weighting term similar to the one in the Dreamer4 paper–but with a squared term in the denominator. $$ L_v = \frac{||x -\hat x ||^2}{(1-\tau)^2} $$

With this modification we got a small, but noticeable improvement over the dreamer4 loss-weighting, so we stuck with it.

      Optimal transport and flow matching is a match made in heaven 

      More specifically, we use minibatch barycentric OT between entire noise and latent sequences 

We also tried $\mu$-parametrization; however, we found that it was not needed for multiple reasons:

- The smallest Minecraft model we trained was just one order of magnitude smaller than the final model.
- The Muon optimizer keeps hyperparameters more stable across different model sizes .

With this work, we hope to give researchers the tools, code, and hard-won lessons needed to explore the frontier of world models.

        We want to thank
        
          
        , who generously sponsored this project. Without them, this project would not have existed.
    

        We also want to thank
        [Mihir Mahajan](https://x.com/maharajamihir),
        [Rami Seid](https://ramis.ai/),
        [Davide Locatelli](https://derewah.dev/),
        [Franz srambical](https://srambical.fr/),
        [Yong-hyun Park](https://enkeejunior1.github.io/),
        [Danijar Hafner](https://danijar.com) and
        [Wilson Yan](https://wilsonyan.com/)
        for the help and support throughout this project.
    

Edward started the project solo and got a first version running on a toy environment. Francesco and Diego took over from there, rebuilding it into the full system. Francesco wrote this post.

You can do so by sending an email to this address francesco215@live.it or by messaging on discord at sacco215

For attribution in academic contexts, please cite this work as

```
    Marti Monso, D., Sacco, F., & Hu, E. (2026). How to Train a Frontier-level World Model.
    
```
    BibTeX citation

```
    @misc{marti2026opendreamer,
        title={How to Train a Frontier-level World Model},
        author={Marti Monso, Diego and Sacco, Francesco and Hu, Edward},
        month={jul},
        year={2026},
        publisher={Zenodo},
        doi={10.5281/zenodo.21475232},
        url={https://next-state.github.io/open-dreamer/},
    }
    
```