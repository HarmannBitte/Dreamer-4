<!-- source: https://danijar.com/project/dreamer4/
     fetched: 2026-09-20T13:37:02Z -->

## Introducing Dreamer 4

World models equip agents with a deep understanding of the world and the ability to predict the future. However, previous world models have been unable to accurately predict object interactions in complex environents. We present Dreamer 4, a scalable agent that learns to solve control tasks by imagination training inside of a fast and accurate world model. Through a new objective and architecture, the world model simulates complex object interactions while achieving real-time interactive inference. By training inside of its world model, Dreamer 4 is the first agent to obtain diamonds in Minecraft purely from offline data, aligning it with applications such as robotics where online interaction is often impractical.

## Diamonds from Offline Experience

By learning behaviors in imagination, Dreamer 4 is the first agent to obtain diamonds in Minecraft purely from offline data, without environment interaction. The task requires choosing sequences of over 20,000 mouse and keyboard actions from raw pixels. This video shows the agent being evaluated in the actual Minecraft environment.

Uncut evaluation videos are available here:
[Video 1](https://www.youtube.com/watch?v=n4SwlSrkhvU),
[Video 2](https://www.youtube.com/watch?v=5CnpLRM8iXA),
[Video 3](https://www.youtube.com/watch?v=oZyliSpRMSw),
[Video 4](https://www.youtube.com/watch?v=VSKpvb1bnbU).

Dreamer 4 significantly outperforms OpenAI’s VPT offline agent, while using 100 times less data. It also outperforms modern behavioral cloning approaches based on finetuning general vision-language models.

In the research paper, we also show that the world model provides better representations for behavioral cloning agents than Gemma 3. This shows that the world model learns a deep understanding of the environment in a form that is also useful for decision making.

## Imagination Training

Dreamer 4 trains behaviors by reinforcement learning inside of the world model. We call this process imagination training. Below, we show sequences of the agent practicing two tasks inside of the world model, decoded back into pixel space.

The world model has learned a diverse distribution of Minecraft scenarios, allowing the agent to train complex and long-horizon tasks in imagination. Moreover, the reward model has accurately learned to identify task success even for imagined scenarios.

## Human Interaction

The Dreamer 4 world model achieves real-time interactive inference on a single GPU through a new objective and architecture. Here we show a human player performing a wide range of tasks in the world model to demonstrate its counterfactual generations, comparing to previous Minecraft world models.

## Real World Video

To see whether Dreamer 4 can also simulate object interactions on the physical world, we train the world model on a robotics dataset. While frontier video models have struggled with the physics of object interactions, Dreamer 4 allows for counterfactual interactions on this dataset, indicating its promise for applications such as robotics.

Dreamer 4 marks a significant step towards intelligent agents, introducing a fast and accurate world model and an effective recipe for training agents via imagination training. Details can be found in the research paper.