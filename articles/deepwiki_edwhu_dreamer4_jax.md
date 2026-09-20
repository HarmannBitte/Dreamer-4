<!-- source: https://deepwiki.com/edwhu/dreamer4-jax
     fetched: 2026-09-20T13:37:08Z -->

Loading...

Menu

This document provides a high-level introduction to the **dreamer4-jax** repository, an unofficial pure JAX implementation of the Dreamer 4 world model and reinforcement learning agent. This overview covers the project's purpose, goals, core architecture, and training methodology.

For detailed architectural information, see [System Architecture](https://deepwiki.com/edwhu/dreamer4-jax/1.1-system-architecture). For explanations of core terminology and concepts, see [Key Concepts](https://deepwiki.com/edwhu/dreamer4-jax/1.2-key-concepts).

**Sources:** [README.md1-138](https://github.com/edwhu/dreamer4-jax/blob/8144b940/README.md?plain=1#L1-L138)

The dreamer4-jax repository implements the complete Dreamer 4 pipeline as described in *"Training Agents Inside of Scalable World Models"*. The implementation is designed to be:

- **Educational** : Code is intentionally structured for readability and modification
- **Pure JAX** : All components use JAX, Flax, and Optax for high-performance computation
- **Modular** : Clear separation between core library (`dreamer/` ) and training scripts (`scripts/` )
- **Experimentally validated** : Currently verified on the bouncing square dataset with plans to extend to CoinRun and Minecraft

The project enables researchers and practitioners to understand, experiment with, and extend world model-based reinforcement learning approaches.

**Sources:** [README.md1-11](https://github.com/edwhu/dreamer4-jax/blob/8144b940/README.md?plain=1#L1-L11) [README.md32-47](https://github.com/edwhu/dreamer4-jax/blob/8144b940/README.md?plain=1#L32-L47)

Dreamer 4 is a world model-based agent that learns to solve control tasks by training entirely in imagination. The approach consists of two main components:

1. **World Model** : An action-conditioned video diffusion model that learns to predict environment dynamics from video data
2. **Policy** : An RL agent trained purely on imagined rollouts from the world model, never requiring real environment interaction during policy training

The key innovation is training scalable, accurate world models using a **shortcut forcing** objective that enables fast interactive inference (real-time generation on a single GPU) while maintaining high prediction accuracy for complex object interactions.

**Sources:** [README.md18-28](https://github.com/edwhu/dreamer4-jax/blob/8144b940/README.md?plain=1#L18-L28) [docs/main.txt24-36](https://github.com/edwhu/dreamer4-jax/blob/8144b940/docs/main.txt#L24-L36)

The dreamer4-jax project aims to:

1. **Reproduce Dreamer 4** : Implement the complete four-stage training pipeline in pure JAX
2. **Validate on increasing complexity** : Progress from bouncing square → CoinRun → Minecraft
3. **Enable research** : Provide a clean, modifiable codebase for world model research
4. **Demonstrate offline RL** : Show that policies can be trained purely from fixed datasets without environment interaction

Current status: The entire pipeline is implemented and verified on the bouncing square dataset, achieving ~40 PSNR on tokenizer reconstruction, ~30 PSNR on dynamics prediction, and successful policy learning for the center-hovering task.

**Sources:** [README.md7-11](https://github.com/edwhu/dreamer4-jax/blob/8144b940/README.md?plain=1#L7-L11) [README.md97-129](https://github.com/edwhu/dreamer4-jax/blob/8144b940/README.md?plain=1#L97-L129)

The core philosophy is to separate world understanding from decision making:

**Key advantages of this approach:**

| Aspect | Benefit | 
|---|---|
| **Sample Efficiency** | World model learns from all available video data, not just successful trajectories | 
| **Safety** | Policy trained in simulation; no deployment of partially-trained agents | 
| **Speed** | Imagination rollouts are faster than real environment steps | 
| **Offline Capability** | Can train policies from fixed datasets without environment access | 

**Sources:** [docs/main.txt46-66](https://github.com/edwhu/dreamer4-jax/blob/8144b940/docs/main.txt#L46-L66) [README.md18-28](https://github.com/edwhu/dreamer4-jax/blob/8144b940/README.md?plain=1#L18-L28)

**Sources:** [README.md31-46](https://github.com/edwhu/dreamer4-jax/blob/8144b940/README.md?plain=1#L31-L46)

The `dreamer/` directory contains the fundamental building blocks:

| Module | Primary Components | Purpose | 
|---|---|---|
| `models.py` | Space-time axial attention, `CausalTokenizer` ,`InteractiveDynamicsModel` , agent/reward/value heads | All neural network architectures | 
| `data.py` | Bouncing square dataset, environment interface | Data loading and environment simulation | 
| `imagination.py` | JIT-compiled rollout functions | Fast latent-space trajectory generation for RL | 
| `sampler.py` | Non-JIT sampling helpers | Debugging and visualization utilities | 
| `utils.py` | Training state management, Orbax wrappers, logging | Cross-cutting training utilities | 

**Sources:** [README.md32-37](https://github.com/edwhu/dreamer4-jax/blob/8144b940/README.md?plain=1#L32-L37)

The `scripts/` directory contains the four-stage training pipeline plus evaluation:

| Script | Input Dependencies | Output | Purpose | 
|---|---|---|---|
| `train_tokenizer.py` | Raw video data | `tokenizer_ckpt` | Train causal tokenizer (MAE on video) | 
| `train_dynamics.py` | `tokenizer_ckpt` (frozen) | `dynamics_ckpt` | Train interactive dynamics model | 
| `train_bc_rew_heads.py` | `tokenizer_ckpt` ,`pretrained_dyn_ckpt` | `bc_rew_ckpt` | Add agent tokens, BC/reward heads | 
| `train_policy.py` | `bc_rew_ckpt` (frozen) | `policy_ckpt` | Train policy via imagination RL | 
| `eval_bc_rew_heads.py` | `bc_rew_ckpt` | Evaluation metrics | Verify BC/reward performance | 

**Sources:** [README.md38-43](https://github.com/edwhu/dreamer4-jax/blob/8144b940/README.md?plain=1#L38-L43) [README.md78-93](https://github.com/edwhu/dreamer4-jax/blob/8144b940/README.md?plain=1#L78-L93)

Dreamer 4 follows a progressive training methodology where each stage builds on the previous:

**Sources:** [README.md67-93](https://github.com/edwhu/dreamer4-jax/blob/8144b940/README.md?plain=1#L67-L93)

**Phase 1: Causal Tokenizer Training**

- **Objective** : Compress video frames into continuous latent representations
- **Method** : Masked autoencoder (MAE) with reconstruction loss (MSE + LPIPS)
- **Key feature** : Causal in time for frame-by-frame decoding
- **Expected result** : ~40 PSNR reconstruction quality
- **Config location** :[scripts/train_tokenizer.py](https://github.com/edwhu/dreamer4-jax/blob/8144b940/scripts/train_tokenizer.py)`__main__` block

**Phase 2: Interactive Dynamics Training**

- **Objective** : Learn to predict future latent states given actions
- **Method** : Shortcut forcing objective (flow loss + bootstrap loss)
- **Key feature** : Fast inference (K=4 forward passes per frame)
- **Expected result** : ~30 PSNR for diffusion, ~29 PSNR for shortcut
- **Config location** :[scripts/train_dynamics.py](https://github.com/edwhu/dreamer4-jax/blob/8144b940/scripts/train_dynamics.py)`__main__` block

**Phase 3: Behavior Cloning & Reward Prediction**

- **Objective** : Add task-specific prediction capabilities
- **Method** : Agent tokens + multi-token prediction (MTP) heads
- **Key feature** : Dynamics model finetuned to prevent collapse
- **Components added** : BC head, reward head, agent tokens, task embeddings
- **Config location** :[scripts/train_bc_rew_heads.py](https://github.com/edwhu/dreamer4-jax/blob/8144b940/scripts/train_bc_rew_heads.py)`__main__` block

**Phase 4: RL Policy Training**

- **Objective** : Improve policy beyond dataset behaviors
- **Method** : PMPO-style policy gradients on imagined trajectories
- **Key feature** : No real environment interaction required
- **Components** : Policy head, value head, frozen world model
- **Config location** :[scripts/train_policy.py](https://github.com/edwhu/dreamer4-jax/blob/8144b940/scripts/train_policy.py)`__main__` block

**Sources:** [README.md68-73](https://github.com/edwhu/dreamer4-jax/blob/8144b940/README.md?plain=1#L68-L73) [README.md98-129](https://github.com/edwhu/dreamer4-jax/blob/8144b940/README.md?plain=1#L98-L129) [docs/main.txt163-330](https://github.com/edwhu/dreamer4-jax/blob/8144b940/docs/main.txt#L163-L330)

The following diagram shows how data flows from raw inputs to trained policies:

**Sources:** [README.md32-37](https://github.com/edwhu/dreamer4-jax/blob/8144b940/README.md?plain=1#L32-L37) [docs/main.txt154-330](https://github.com/edwhu/dreamer4-jax/blob/8144b940/docs/main.txt#L154-L330)

The training pipeline uses Orbax for checkpoint management with strict dependencies between stages:

| Checkpoint Name | Saved By | Loaded By | Status When Loaded | 
|---|---|---|---|
| `tokenizer_ckpt` | `train_tokenizer.py` | `train_dynamics.py` ,`train_bc_rew_heads.py` | Frozen | 
| `dynamics_ckpt` | `train_dynamics.py` | `train_bc_rew_heads.py` | Finetuned | 
| `bc_rew_ckpt` | `train_bc_rew_heads.py` | `train_policy.py` ,`eval_bc_rew_heads.py` | Frozen (policy/value heads trainable) | 
| `policy_ckpt` | `train_policy.py` | - | Final output | 

All checkpoints are saved under `logs/{run_name}/checkpoints/` by default. The checkpoint paths must be configured in each script's config section before running.

**Sources:** [README.md95-96](https://github.com/edwhu/dreamer4-jax/blob/8144b940/README.md?plain=1#L95-L96) [README.md78-93](https://github.com/edwhu/dreamer4-jax/blob/8144b940/README.md?plain=1#L78-L93)

The implementation achieves the following results on the synthetic bouncing square dataset:

| Training Phase | Metric | Value | Interpretation | 
|---|---|---|---|
| Tokenizer (MAE) | PSNR | ~40 dB | Near-perfect reconstruction | 
| Dynamics (Diffusion) | PSNR | ~30 dB | High-quality autoregressive prediction | 
| Dynamics (Shortcut) | PSNR | ~29 dB | Fast inference with minimal quality loss | 
| Policy (RL) | Task Success | Converged | Agent learns to hover near center | 

**Bouncing Square Task**: An agent controls a square in a grid using WASD commands and receives reward based on proximity to the center. This validates the complete pipeline from video compression through policy learning.

**Sources:** [README.md98-129](https://github.com/edwhu/dreamer4-jax/blob/8144b940/README.md?plain=1#L98-L129)

The implementation demonstrates key Dreamer 4 capabilities:

✓ **Causal Tokenizer**: Masked autoencoding with ~40 PSNR reconstruction

✓ **Shortcut Forcing**: Fast inference (K=4 steps) with competitive quality

✓ **Interactive Dynamics**: Action-conditioned latent prediction

✓ **Agent Tokens**: Task-specific conditioning without causal confusion

✓ **Multi-Token Prediction**: BC and reward heads with MTP (L=8)

✓ **Imagination Training**: PMPO-style policy gradients in latent space

✓ **JIT Compilation**: Fast rollout generation for efficient RL

**Sources:** [README.md100-129](https://github.com/edwhu/dreamer4-jax/blob/8144b940/README.md?plain=1#L100-L129)

The project roadmap includes:

1. **CoinRun** : Extend to procedurally generated 2D platformer
2. **Minecraft** : Scale to complex 3D environment with object interactions
3. **Architecture exploration** : Test different attention patterns, model sizes
4. **Objective ablations** : Validate shortcut forcing components

**Sources:** [README.md7-11](https://github.com/edwhu/dreamer4-jax/blob/8144b940/README.md?plain=1#L7-L11)

The project relies on the following core libraries:

| Library | Purpose | Usage | 
|---|---|---|
| JAX | Numerical computing, automatic differentiation | All computations | 
| Flax | Neural network definitions | All models in `models.py` | 
| Optax | Gradient-based optimization | All training loops | 
| Einops | Tensor shape manipulation | Reshaping operations throughout | 
| Orbax | Checkpoint save/restore | Training state management | 
| WandB | Experiment tracking (optional) | Metrics logging | 

**Sources:** [README.md49-65](https://github.com/edwhu/dreamer4-jax/blob/8144b940/README.md?plain=1#L49-L65)

To begin working with dreamer4-jax:

1. **Installation** : See[Installation and Dependencies](https://deepwiki.com/edwhu/dreamer4-jax/2.1-installation-and-dependencies) for environment setup
2. **First experiment** : See[Running Your First Experiment](https://deepwiki.com/edwhu/dreamer4-jax/2.2-running-your-first-experiment) to execute the bouncing square pipeline
3. **Understanding the pipeline** : See[Training Pipeline](https://deepwiki.com/edwhu/dreamer4-jax/3-training-pipeline) for detailed phase documentation
4. **Modifying the code** : Start from training scripts in`scripts/` and follow calls into`dreamer/` modules

The codebase is intentionally designed for modification. Each training script's `__main__` block contains configuration dictionaries that control all aspects of training.

**Sources:** [README.md47-96](https://github.com/edwhu/dreamer4-jax/blob/8144b940/README.md?plain=1#L47-L96)