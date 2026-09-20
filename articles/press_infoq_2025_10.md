<!-- source: https://www.infoq.com/news/2025/10/dreamer-4-minecraft-agent/
     fetched: 2026-09-20T13:37:10Z -->

Researchers from Google DeepMind have recently described a [new approach for teaching intelligent agents to solve complex, long-term tasks](https://danijar.com/project/dreamer4/) by training them exclusively on video footage rather than through direct interaction with the environment. Their new agent, called Dreamer 4, demonstrated the ability to mine diamonds playing Minecraft after being trained on videos, without ever actually playing the game.

The researchers dubbed their approach *imagination training* to emphasize that the agent learns solely from offline data, without any interaction with the physical world. In other words, the training takes place entirely within the agent’s “imagination” before being applied to real-world scenarios. This [feature is particularly important for fields like robotics](https://x.com/danijarh/status/1973072290301563079), notes Danijar Hafner, one of the study's authors, on Twitter, where direct online interaction is often practical.

In a companion [paper](https://arxiv.org/pdf/2509.24527), the researchers describe their approach in detail. Their model architecture comprises two main components: a tokenizer that compresses each video frame into a continuous representation, and a dynamics model that predicts the next world representation given the current one and the chosen action.

To make the dynamics model more efficient, the researchers employed shortcut forcing, training the model to take larger steps when predicting future frames without losing accuracy. As a result, Dreamer 4 can generate new world representations in real time. Additionally, they incorporate casual attention across space and time, along with specialized memory techniques, enabling the model to maintain a minimum of 20 frames per second on a single GPU.

As mentioned, Dreamer 4 is the first agent trained solely from offline data that has proven capable of mining diamonds in Minecraft. This may seem like a simple task, but it actually requires selecting sequences of over 20,000 mouse and keyboard actions based solely on raw pixel data.

Dreamer 4 significantly outperforms OpenAI’s VPT offline agent, while using 100 times less data. It also outperforms modern behavioral cloning approaches based on finetuning general vision-language models.


The researchers also highlight that Dreamer 4 outperformed Gemma 3, demonstrating that their approach is effective not only for building behavioral cloning agents but also potentially for general decision making.

When asked about it on X, Hafner described Minecraft as an [excellent testbed](https://x.com/danijarh/status/1973125918152597837) for embodied agent research, noting that while mining a diamond is a complex task, it is far from the only challenge Minecraft offers for testing agents:

There's so much more general AI progress we can make on Minecraft! The agent is still far from human-level play, and there are hundreds of harder tasks past getting diamonds.


As a final note, Dreamer 4 has also been tested on a real-world robotic dataset, demonstrating its ability to perform counterfactual interactions. It showed promising results compared with state-of-the-art video models, which have often struggled with the physics of object interactions.