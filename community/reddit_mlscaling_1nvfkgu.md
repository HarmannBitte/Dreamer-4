# r/mlscaling — DeepMind: Introducing Dreamer 4, an agent that learns to solve complex control tasks entirely inside of its scalable world model! | "Dreamer 4 is the first agent to mine diamonds in Minecraft entirely from offline data!"
https://www.reddit.com/r/mlscaling/comments/1nvfkgu/
author: u/44th--Hokage | posted: 2025-10-01 18:02 UTC | score: 29 | comments (reddit count): 1 | archived comments: 1
link: https://www.reddit.com/r/mlscaling/comments/1nvfkgu/deepmind_introducing_dreamer_4_an_agent_that/

#### 🎥 Demonstration Video:

https://imgur.com/gallery/vN7ypCU

---

🧠 Dreamer 4 learns a scalable world model from offline data and trains a multi-task agent inside it, without ever having to touch the environment. During evaluation, it can be guided through a sequence of tasks.


This setting is crucial for fields like robotics, where online interaction is not practical. The task requires 20k+ mouse/keyboard actions from raw pixels

The Dreamer 4 world model predicts complex object interactions while achieving real-time interactive inference on a single GPU

It outperforms previous world models by a large margin when put to the test by human interaction 🧑‍💻

For accurate and fast generations, we use an efficient transformer architecture and a novel shortcut forcing objective ⚡

We first pretrain the WM, finetune agent tokens into the same transformer to predict policy & reward, and then improve the policy by imagination training

https://i.imgur.com/OhVPIjZ.jpeg

▶️ Shortcut forcing builds on diffusion forcing and shortcut models, training a sequence model with both the noise level and requested step size as inputs

This enables much faster frame-by-frame generations than diffusion forcing, without needing a distillation phase ⏱️

https://i.imgur.com/6zfD950.jpeg


📈 On the offline diamond challenge, Dreamer 4 outperforms OpenAI's VPT offline agent despite using 100x less data

It also outperforms modern behavioral cloning recipes, even when they are based on powerful pretrained models such as Gemma 3

https://i.imgur.com/CvxmCeO.jpeg

✅ We find that imagination training not only makes policies more robust but also more efficient, so they achieve milestones towards the diamond faster

✅ Moreover, using the WM representations for behavioral cloning outperforms using the general representations of Gemma 3

https://i.imgur.com/yzB3slU.jpeg

---

####Website: danijar.com/dreamer4/

####Paper: arxiv.org/abs/2509.24527

## Comments

- **u/currentscurrents** (4 pts, 2025-10-01 19:47): Neat! I'd been wondering when there would be a follow-up work to Dreamerv3.