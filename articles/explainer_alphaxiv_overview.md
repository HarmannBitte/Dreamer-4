<!-- source: https://www.alphaxiv.org/overview/2509.24527
     fetched: 2026-09-20T13:37:18Z -->

Submitted 29 Sept 2025

# Training Agents Inside of Scalable World Models

## Abstract

World models learn general knowledge from videos and simulate experience for training behaviors in imagination, offering a path towards intelligent agents. However, previous world models have been unable to accurately predict object interactions in complex environments. We introduce Dreamer 4, a scalable agent that learns to solve control tasks by reinforcement learning inside of a fast and accurate world model. In the complex video game Minecraft, the world model accurately predicts object interactions and game mechanics, outperforming previous world models by a large margin. The world model achieves real-time interactive inference on a single GPU through a shortcut forcing objective and an efficient transformer architecture. Moreover, the world model learns general action conditioning from only a small amount of data, allowing it to extract the majority of its knowledge from diverse unlabeled videos. We propose the challenge of obtaining diamonds in Minecraft from only offline data, aligning with practical applications such as robotics where learning from environment interaction can be unsafe and slow. This task requires choosing sequences of over 20,000 mouse and keyboard actions from raw pixels. By learning behaviors in imagination, Dreamer 4 is the first agent to obtain diamonds in Minecraft purely from offline data, without environment interaction. Our work provides a scalable recipe for imagination training, marking a step towards intelligent agents.

## AI Overview

## Introduction

*Figure 1: Dreamer 4 agent performing various Minecraft tasks including gathering wood, mining cobblestone, crafting stone pickaxes, and mining diamonds. The agent demonstrates complex behaviors like navigating environments, using tools, and interacting with crafting interfaces.*

World model-based reinforcement learning has emerged as a promising approach for training intelligent agents that can learn complex behaviors by "imagining" experiences in a learned simulation of their environment. Dreamer 4 represents a significant advancement in this field, introducing the first agent capable of obtaining diamonds in Minecraft purely from offline data - a challenging milestone that requires executing long sequences of coordinated actions over extended time horizons.

The paper presents a comprehensive system that combines modern generative AI techniques with reinforcement learning to create highly accurate and computationally efficient world models. By training agents entirely within these learned simulations, Dreamer 4 addresses critical challenges in AI including sample efficiency, safety constraints in real-world deployment, and the ability to leverage vast amounts of unlabeled video data for learning general world knowledge.

## Methodology and Architecture

Dreamer 4 employs a sophisticated three-phase training approach built around two core architectural components: a causal tokenizer and an interactive dynamics model, both utilizing an efficient transformer architecture.

### Training Pipeline

The system follows a structured learning progression:

1. **World Model Pretraining** : The tokenizer and dynamics model are trained on large video datasets using masked autoencoding and shortcut forcing objectives
2. **Agent Finetuning** : Task-specific policy and reward prediction heads are added and trained via behavior cloning
3. **Imagination Training** : The policy is optimized through reinforcement learning on trajectories generated entirely within the world model

### Causal Tokenizer Architecture

The tokenizer compresses raw video frames (360×640 pixels for Minecraft) into continuous representations that the dynamics model can process efficiently. Its causal design enables sequential encoding and decoding, crucial for real-time interactive inference. The training objective combines Mean Squared Error and LPIPS perceptual loss with masked autoencoding, where random patches are corrupted to force learning of robust, generalizable representations.

### Interactive Dynamics Model

The dynamics model serves as the core world simulator, predicting future tokenized representations conditioned on agent actions. It processes interleaved sequences of actions, noise levels, step sizes, and corrupted representations using the efficient transformer architecture.

The key innovation lies in the **shortcut forcing** training objective, which builds on diffusion forcing and shortcut models:

- **x-prediction parameterization** : Unlike typical diffusion models that predict noise, the dynamics model predicts clean representations directly, preventing accumulation of high-frequency errors during long rollouts
- **x-space loss computation** : Both flow matching and bootstrap loss terms are computed in the space of clean representations
- **Ramp loss weighting** : A linear weight  emphasizes higher signal levels, focusing model capacity on more meaningful learning signals

During inference, the model generates future states autoregressively using only K=4 sampling steps (versus 64+ for typical diffusion models), achieving a 16× speedup while maintaining quality.

### Efficient Transformer Design

Both the tokenizer and dynamics model utilize a shared transformer architecture optimized for computational efficiency:

- **Factorized attention** : Separate space-only and time-only attention layers reduce computational complexity
- **Grouped Query Attention (GQA)** : Reduces key-value cache size for faster attention computation
- **Temporal attention scheduling** : Time-based attention applied only every 4 layers
- **Stability enhancements** : QKNorm, attention logit soft capping, RMSNorm, and RoPE embeddings

### Reinforcement Learning with PMPO

For imagination training, Dreamer 4 introduces task-specific "agent tokens" that receive task embeddings and predict actions and rewards over a multi-token prediction horizon. The system employs **Preference Model Policy Optimization (PMPO)**, which focuses on advantage signs rather than magnitudes:

This approach provides balanced learning from positive and negative feedback without requiring return normalization, while a reverse KL divergence term to a behavioral prior keeps the policy within reasonable action spaces.

## Key Results and Achievements

### Offline Diamond Challenge Performance

Dreamer 4 achieves several unprecedented results in the challenging Minecraft environment:

- **First diamond acquisition from offline data** : 0.7% success rate in 60-minute episodes, representing the first agent to achieve this milestone purely from offline learning
- **Superior milestone progression** : Substantially outperforms previous methods across the crafting progression, achieving 99% success for basic items like logs and stone tools, 40% for iron pickaxes, and meaningful progress on diamond acquisition
- **Imagination training effectiveness** : Reinforcement learning in the world model consistently improves both success rates and task completion speed compared to behavior cloning baselines

*Figure 2: Dreamer 4 performance compared to previous methods across Minecraft crafting milestones. The agent significantly outperforms VPT (finetuned), BC baselines, and VLA (Gemma 3) across all tasks, with particularly strong performance on complex items requiring long-horizon planning.*

### World Model Accuracy and Interaction Quality

The world model demonstrates remarkable fidelity in simulating complex Minecraft mechanics:

- **Interactive inference speed** : Achieves 21 FPS on a single H100 GPU, exceeding Minecraft's native 20 FPS tick rate
- **Extended context** : 9.6-second context length versus 0.8-1.6 seconds in previous Minecraft world models
- **Task completion** : Successfully completes 14 out of 16 human-designed interaction tasks within simulation
- **Superior to existing models** : Outperforms Oasis and Lucid-v1 in both prediction fidelity and precise mechanic simulation

*Figure 3: Comparison of world model generation quality. Dreamer 4 maintains coherent physics and object interactions throughout extended sequences, while competing models (Oasis, Lucid) suffer from hallucinations and inconsistent mechanics.*

### Action Generalization and Data Efficiency

A particularly significant finding involves the model's ability to learn from minimal labeled action data:

- **Efficient action conditioning** : Achieves 85% PSNR with only 100 hours of action-labeled data out of 2541 total hours
- **Cross-domain generalization** : Action conditioning learned from Overworld data generalizes to visually distinct Nether and End dimensions with 76% PSNR
- **Unlabeled video utilization** : Demonstrates the ability to extract world knowledge primarily from unlabeled video content

*Figure 4: Action generalization results showing performance with varying amounts of action-labeled data (left) and generalization to unseen Nether environments (right). The model learns effective action conditioning from minimal labeled data and generalizes across visually distinct domains.*

### Real-World Applications

Beyond Minecraft, Dreamer 4 demonstrates promising capabilities on robotics datasets, accurately simulating physics and counterfactual interactions, suggesting potential for real-world robotic applications where offline learning is crucial for safety and efficiency.

## Architectural Innovations and Technical Contributions

### Shortcut Forcing Methodology

The shortcut forcing approach represents a key technical contribution that enables both high-quality generation and computational efficiency. By parameterizing the model to predict clean representations (x-prediction) rather than noise, and computing losses in x-space, the system avoids the accumulation of subtle errors that plague long-sequence generation in traditional diffusion models.

### Efficient Architecture Design

The combination of factorized attention, grouped query attention, and strategic temporal attention scheduling reduces computational costs while maintaining generation quality. Ablation studies demonstrate that these architectural improvements collectively reduce Fréchet Video Distance from 306 to 57 while enabling real-time inference.

### Integration of Modern Generative AI

Dreamer 4 successfully bridges the gap between high-fidelity generative models (like diffusion transformers) and practical agent training requirements. This integration maintains the visual richness and diversity of modern generative AI while meeting the speed and accuracy demands of reinforcement learning.

## Significance and Broader Impact

Dreamer 4 represents a substantial advancement toward more capable and practical AI agents with several important implications:

**Offline Learning Paradigm**: By demonstrating complex behavior acquisition purely from offline data, the work validates imagination-based training for scenarios where online interaction is costly, dangerous, or impractical - particularly relevant for robotics and autonomous systems.

**Data-Efficient Learning**: The ability to learn effective policies from minimal action-labeled data while leveraging vast amounts of unlabeled video content opens new possibilities for training on web-scale video datasets, potentially democratizing access to high-quality training data.

**Scalable World Models**: The achievement of real-time, high-fidelity world model inference on consumer hardware makes imagination-based training more accessible and practical for broader research and application domains.

**Foundation for General Intelligence**: The work provides a concrete pathway toward agents that can learn rich world understanding from observation and apply that knowledge to novel tasks and environments, representing progress toward more general artificial intelligence systems.

The successful completion of the Minecraft diamond challenge serves not just as a technical milestone, but as validation of the broader approach of learning complex behaviors through imagination in learned world models. This methodology may prove essential for developing AI systems that can operate safely and effectively in the real world while requiring minimal direct interaction during training.

[One step diffusion via shortcut models](https://www.alphaxiv.org/abs/2410.12557)