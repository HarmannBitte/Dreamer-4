<!-- source: https://arxiviq.substack.com/p/dreamer-4-training-agents-inside
     fetched: 2026-09-20T13:37:15Z -->

**Authors:** *Danijar Hafner, Wilson Yan, Timothy Lillicrap***Paper:** [https://arxiv.org/abs/2509.24527](https://arxiv.org/abs/2509.24527) **Website:** [danijar.com/dreamer4](https://danijar.com/dreamer4)

## TL;DR

**WHAT was done?** The paper introduces Dreamer 4, a 2B-parameter agent that is the first to solve the long-horizon “obtain diamonds” challenge in Minecraft purely from a fixed offline dataset. This is achieved by training a policy via reinforcement learning (RL) entirely inside a learned world model. The core innovation is this world model: an efficient transformer architecture trained with a novel “shortcut forcing” objective. This objective, which builds on flow matching but crucially predicts the final clean state (x-prediction) instead of the update vector (v-prediction), allows the model to accurately simulate complex game mechanics in real-time (21 FPS) on a single GPU.

**WHY it matters?** This work marks a significant milestone by demonstrating that complex control tasks, previously requiring costly or unsafe online interaction, can be mastered efficiently through imagination. It validates the offline world model paradigm for high-stakes applications like robotics, providing a recipe for training agents safely from fixed datasets. Furthermore, the model’s ability to learn from vast unlabeled videos with minimal action-labeled data—and to generalize its learned action conditioning to entirely new environments—presents a scalable path toward building general-purpose simulators and advancing embodied AI by leveraging the wealth of video data available on the internet.

## Details

### Introduction

Training intelligent agents to solve complex, long-horizon tasks in open-world environments is a grand challenge in AI. The video game Minecraft, with its procedurally generated worlds and deep crafting trees, serves as an ideal benchmark. The “obtain diamond” task, for instance, requires a sequence of over 20,000 discrete actions, demanding sophisticated planning and a deep understanding of the environment’s mechanics. Previous approaches have either relied on massive datasets for behavioral cloning or extensive, and often unsafe, online interaction for reinforcement learning.

This paper introduces Dreamer 4, a scalable agent that charts a new course. It is the first to conquer the Minecraft diamond challenge purely from a standard offline dataset, without any environment interaction. The key lies in its ability to learn an accurate, high-fidelity world model that acts as an internal simulator, allowing the agent to train and master complex behaviors entirely in “imagination.”