# r/accelerate — DeepMind: Introducing Dreamer 4, an agent that learns to solve complex control tasks entirely inside of its scalable world model! | "Dreamer 4 is the first agent to mine diamonds in Minecraft entirely from offline data!"
https://www.reddit.com/r/accelerate/comments/1nvbfm1/
author: u/44th--Hokage | posted: 2025-10-01 15:32 UTC | score: 155 | comments (reddit count): 43 | archived comments: 51
link: https://v.redd.it/8vz8z2serisf1

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

- **u/Substantial-Sky-8556** (69 pts, 2025-10-01 16:16): These past few days have been nothing but breakthrough after breakthrough
    - **u/Dark-grey** (9 pts, 2025-10-01 18:28): it's holiday season, mfer.
    - **u/coverednmud** (3 pts, 2025-10-01 19:29): Once the cycle ends, likely with Google and Grok we should circle back around in six months or so I think?
        - **u/OrdinaryLavishness11** (6 pts, 2025-10-01 22:05): Three months*
            - **u/coverednmud** (3 pts, 2025-10-01 22:36): Hell yes. You must be correct.
                - **u/fynn34** (4 pts, 2025-10-02 02:08): We’ve moved to a quarterly cycle, pretty consistently now
                    - **u/Finanzamt_Endgegner** (1 pts, 2025-10-04 00:31): its only gonna speed up from now i think,  a lot of new chinese players on the market rn and tons of technological developments of which a lot aint even in models yet and if they are its more like proof of concepts.
- **u/porcelainfog** (35 pts, 2025-10-01 15:51): One step closer to having an AI buddy in games like valhiem. Super cool.
    - **u/spaceynyc** (7 pts, 2025-10-02 01:46): Still hoping for a AI Split Fiction partner
    - **u/ihexx** (3 pts, 2025-10-02 08:38): you're thinking too small: there's nothing restricting this to just games; games are just an easy experiment environment.
      
      What's stopping the 'game' from being: using a computer terminal? Or piloting a robot?
      
      What happens when the world model scales to something like veo 3 or sora 2?
      
      What happens when the policy model scales to something like gemini or gpt5?
      
      This is a big unlock for agentic training generally
        - **u/porcelainfog** (7 pts, 2025-10-02 10:07): For sure. But I greedily want a gaming buddy. My friends are all in their 30s now and we lose steam quickly on games like the forest and mine craft and stuff. This way I could play and build at my own pace but still have that multiplayer feel to it.
            - **u/ihexx** (3 pts, 2025-10-02 10:14): honestly valid
        - **u/44th--Hokage** (2 pts, 2025-10-02 15:48): Your mind is thinking exactly in the right direction! 
          
          
          To give a little background, “from offline data” simply means the world model is trained solely on a previously collected, fixed dataset of state-action-next-state-reward tuples, with no new environment rollouts, online exploration, or further real-time interaction during learning.
          
          Essentially this means you can build a capable agent without ever touching the real world again the implications of which are staggering because now we can imagine a world of fully autonomously trained, but still highly real-world capable, agents. 
          
          
          #####AKA: this is the prelude to viable agent swarms.
            - **u/ihexx** (1 pts, 2025-10-02 16:01): yeah it's like:  
              the big thing holding RLVR back in models like deepseek is basically how algorithms like GRPO are still essentially on-policy; the model has to generate its traces. you can't have an RL stage at the same scale as you have a pretrain stage.
              
              THis changes that. Suddenly RVLR can be as big as pretraining.
                - **u/44th--Hokage** (1 pts, 2025-10-02 16:21): And in fact independent research is convening on that eventuality:
                  
                  [Nvidia's Newest Paper—RLP: Reinforcement as a Pretraining Objective ](https://research.nvidia.com/labs/adlr/RLP/)
        - **u/patham9** (1 pts, 2025-11-12 17:12): Not with current AI.
- **u/AdAnnual5736** (35 pts, 2025-10-01 17:31): I was told AI progress had plateaued…
    - **u/44th--Hokage** (43 pts, 2025-10-01 18:15): *You were *gaslit* that AI progress had plateued 
      
      FTFY
        - **u/Galilleon** (11 pts, 2025-10-01 21:02): And still are, actively, every step of the way
            - **u/44th--Hokage** (9 pts, 2025-10-02 00:52): Its all Chinese FUD bots trying to slow down western AI progress by sowing discontent and discord on top of Elon Musk funded bot-armies trying day and night to malign the name of not just OpenAI but fairly obviously specifically Sam Altman
                - **u/Mother-Daikon-1360** (1 pts, 2026-04-02 19:41): We all hate Sam Altman.
        - **u/Pyros-SD-Models** (8 pts, 2025-10-02 01:57): “This is the maximum of how smart LLMs can get” Yann LolCun about gpt-3.5
    - **u/coverednmud** (14 pts, 2025-10-01 19:30): I was told this by artist who said that AI would never figure out hands.
      
      Now it is simulating humans playing volleyball. 
      
      I'm sure the voice actors are safe though... wait a min...
    - **u/Different-Froyo9497** (12 pts, 2025-10-01 19:37): I have no doubt they’ll say it again in a week or two lol. Their brains are poor prediction machines, they’ll see a great deal of progress then think things should happen quickly, then when things slow down for a short bit they’ll think things will never happen. It’s like their brain continually oscillates between two extremes.
      
      Kurzweil has the right idea - rather than base things on fickle emotion, just follow the trend lines. Sure, sometimes progress in some domain can flatline, but you’ll never know when that happens until it happens. You’re best bet is to just trust the data
        - **u/czk_21** (1 pts, 2025-10-02 11:49): exactly just follow the trends, small hiccups along the road are completely inconsequentional
    - **u/Accomplished_Elk4969** (1 pts, 2025-10-04 06:42): It literally ran into lava as it died
    - **u/netrunui** (1 pts, 2025-10-14 07:09): this doesn't use LLMs
- **u/jthedwalker** (14 pts, 2025-10-01 20:11): Rookie move digging straight down 🫣
- **u/Helpful_Program_5473** (8 pts, 2025-10-01 16:35): Is there anyway we can manifest AI playing dwarf fortress?
    - **u/Mystery_Shaman** (1 pts, 2025-10-04 19:24): See, THIS guy gets it
- **u/vuon6** (6 pts, 2025-10-01 16:48): ai minecraft youtubers when
- **u/aiworld** (5 pts, 2025-10-01 20:18): It may seem silly but the speed and accuracy of these clicks (like in the inventory) is unprecedented. There's no huge web pretraining corpus that teaches clicks and models so far have been super slow and inaccurate. If they can transfer this ability to general computer use, things are about to get crazy.
- **u/Radfactor** (5 pts, 2025-10-01 21:05): Sweet!
- **u/JamR_711111** (5 pts, 2025-10-01 23:04): the first group to sell the product of having dynamic, competent AI singleplayer game companions will make bank
- **u/Neither-Phone-7264** (3 pts, 2025-10-01 21:36): nooo it died poor robot
- **u/Dr_Ambiorix** (3 pts, 2025-10-01 23:59): What does the "from offline data" mean?
    - **u/44th--Hokage** (5 pts, 2025-10-02 00:49): “From offline data” simply means the world model is trained solely on a previously collected, fixed dataset of state-action-next-state-reward tuples, with no new environment rollouts, online exploration, or further real-time interaction during learning.
      
      Essentially this means you can build a capable agent without ever touching the real world again the implications of which are staggering because now we can imagine a world of fully autonomously trained, but still highly real-world capable, agents. AKA this is the prelude to viable agent swarms.
        - **u/Dr_Ambiorix** (1 pts, 2025-10-02 08:21): So in this context, does it mean it learned to mine diamonds entirely from training on playing the game and learning what specific actions do from that etc?
          
          So no explicit instructions about how to actually mine diamonds where given? Or am I looking at it completely wrong now. It had to learn to upgrade its tools because during training it eventually saw that the wooden pickaxe didn't yield resources for example?
            - **u/44th--Hokage** (2 pts, 2025-10-02 16:13): Exactly.
              
              No one told it “to mine diamonds you need an iron pickaxe, which you craft from three iron ingots and two sticks…”
              
              
              It simply watched a big pile of recorded human gameplay (specifically, the “OpenAI VPT dataset,” which is 96k hours of human mouse-and-keyboard Minecraft gameplay captured from contractors) and, by predicting the next frame and reward over and over, discovered for itself that, for instance, wooden pickaxes break stone without dropping anything, or that iron ones do drop ore, or that deeper layers contain diamond blocks, etc.
              
              
              All the “rules” emerged as patterns from the data.
- **u/moxyte** (2 pts, 2025-10-01 17:08): Pretty sure Neuro did something like that at least a year ago
    - **u/Substantial-Sky-8556** (10 pts, 2025-10-01 17:16): It wasn't AI, it was an algorithm that was controlling the game, neuro is an llm and a few other narrow AI's masquerading as a general AI.
        - **u/moxyte** (2 pts, 2025-10-01 18:16): All the current cutting edge AI models including LLM's are the same technology (backpropagating massive multilayer neural networks). Neuro gameplay got increasingly better over time to the point that it wasn't entertaining anymore. It isn't some Vedal's if-else tree.
    - **u/Creative-robot** (8 pts, 2025-10-01 18:06): This is a lot smoother than Neuro’s Minecraft AI, though that one was still cool since it captured her personality quirks well.
    - **u/[deleted]** (1 pts, 2025-10-01 18:35): [deleted]
- **u/IndieDevLove** (2 pts, 2025-10-01 17:55): looks a bit like it got lucky there. It started trying to drill into bedrock but found diamonds before that. Not sure how long it would have hammered into bedrock without the diamonds there.
    - **u/44th--Hokage** (6 pts, 2025-10-01 18:10): I'm certain that wasn't their only test.
    - **u/Mindrust** (6 pts, 2025-10-01 21:40): Success rate for finding diamonds was 0.7%, so that does seem plausible
- **u/Jolly-Ground-3722** (2 pts, 2025-10-02 11:05): ![gif](giphy|MO9ARnIhzxnxu)
- **u/Revolutionalredstone** (1 pts, 2025-10-01 21:53): lol my lua script agents from 15 years ago were happily mining diamond.
  
  I get what you mean tho, unprogrammed agent ;)
- **u/Outside-Ad9410** (1 pts, 2025-10-02 00:07): "AI is just a bubble that will pop any day now trust me!" - Some luddite probably
- **u/RegularBasicStranger** (1 pts, 2025-10-05 17:37): Minecraft has only fixed number of actions and there is no ability to create new actions so it is just something like chess so AI only needs vision to do such.