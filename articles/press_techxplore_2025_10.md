<!-- source: https://techxplore.com/news/2025-10-deepmind-ai-agent-tasks-scalable.html (via Wayback Machine snapshot 2026-09-18) -->

October 25, 2025
                                                        
  [feature](https://techxplore.com/editorials/)
                                                    

# DeepMind introduces AI agent that learns to complete various tasks in a scalable world model

##### Ingrid Fadelli

Author

##### Sadie Harley

Scientific Editor

##### Robert Egan

Associate Editor

Over the past decade, deep learning has transformed how artificial intelligence (AI) agents perceive and act in digital environments, allowing them to master board games, control simulated robots and reliably tackle various other tasks. Yet most of these systems still depend on enormous amounts of direct experience—millions of trial-and-error interactions—to achieve even modest competence.

This brute-force approach limits their usefulness in the physical world, where such experimentation would be slow, costly, or unsafe.

To overcome these limitations, researchers have turned to world models—simulated environments where agents can safely practice and learn.

These world models aim to capture not just the visuals of a world, but the underlying dynamics: how objects move, collide, and respond to actions. However, while simple games like Atari and Go have served as effective testbeds, world models still fall short when it comes to representing the rich, open-ended physics of complex worlds like Minecraft or robotics environments.

Researchers at Google DeepMind recently developed Dreamer 4, a new artificial agent capable of learning complex behaviors entirely within a scalable world model, given a limited set of pre-recorded videos.

The new model, presented in a [paper](https://arxiv.org/abs/2509.24527) published on the *arXiv* preprint server, was the first [artificial intelligence](https://techxplore.com/tags/artificial+intelligence/) (AI) agent to obtain diamonds in Minecraft without practicing in the actual game at all. This remarkable achievement highlights the possibility of using Dreamer 4 to train successful AI agents purely in imagination—with important implications for the future of robotics.

"We as humans choose actions based on a deep understanding of the world and anticipate potential outcomes in advance," Danijar Hafner, first author of the paper, told Tech Xplore.

"This ability requires an internal model of the world and allows us to solve new problems very quickly. In contrast, previous AI agents usually learn through brute-force with vast amounts of trial-and-error. But that's infeasible for applications such as physical robots that can easily break."

Some of the AI agents developed at DeepMind over the past few years have already [achieved](https://deepmind.google/discover/blog/muzero-mastering-go-chess-shogi-and-atari-without-rules/) [tremendous](https://danijar.com/project/dreamerv3/) [success](https://www.technologyreview.com/2022/07/18/1056059/robot-dog-ai-reinforcement/) at games such as Go and Atari by training in small world models. However, the world models that these models relied on failed to capture the rich physical interactions in more complex worlds, such as the Minecraft videogame.

On the other hand, "Video models such as [Veo](https://deepmind.google/models/veo/) and [Sora](https://openai.com/index/sora-2/) are rapidly improving towards generating realistic videos of very diverse situations," said Hafner.

"However, they are not interactive, and their generations are too slow, so they cannot be used as 'neural simulators' to train agents inside of yet. The goal of Dreamer 4 was to train successful agents purely inside of world models that can realistically simulate complex worlds."

Hafner and his colleagues decided to use Minecraft as a test bed for their AI agent, as it is a complex video game that contains infinite generated worlds and long-horizon tasks that require over 20,000 consecutive mouse/keyboard actions to be completed.

One of these tasks is the mining of diamonds, which requires the agent to perform a long sequence of prerequisites such as chopping trees, crafting tools, and mining and smelting ores.

Notably, the researchers wanted to train their agent purely in "imagined" scenarios, instead of allowing it to practice in the actual game, analogous to how smart robots will have to learn in simulation, because they could easily break when practicing directly in the physical world . This requires the model to learn object interactions in an accurate enough internal model of the Minecraft world.

The artificial agent developed by Hafner and his colleagues is based on a large transformer model that was trained to predict future observations, actions and the rewards associated with specific situations. Dreamer 4 was trained on a fixed offline dataset containing recorded Minecraft gameplay videos collected by human players.

"After completing this training, Dreamer 4 learns to select increasingly better actions in a wide range of imagined scenarios via reinforcement learning," said Hafner.

"Training agents inside of scalable world models required pushing the frontier of generative AI. We designed an efficient transformer architecture, and a novel training objective named shortcut forcing. These advances enabled accurate predictions while also speeding up generations by over 25x compared to typical video models."

Dreamer 4 is the first AI agent to obtain diamonds in Minecraft when trained solely on offline data, without ever practicing its skills in the actual game. This finding highlights the agent's ability to autonomously learn how to correctly solve complex and long-horizon tasks.

"Learning purely offline is highly relevant for training robots that can easily break when practicing in the physical world," said Hafner. "Our work introduces a promising new approach to building smart robots that do household chores and factory tasks."

In the initial tests performed by the researchers, the Dreamer 4 agent was found to accurately predict various object interactions and game mechanics, thus developing a reliable internal world model. The world model established by the agent outperformed the models that earlier agents relied on by a significant margin.

"The model supports real-time interactions on a single GPU, making it easy for human players to explore its dream world and test its capabilities," said Hafner. "We find that the model accurately predicts the dynamics of mining and placing blocks, crafting simple items, and even using doors, chests, and boats."

A further advantage of Dreamer 4 is that it achieved remarkable results despite being trained on a very small amount of action data. This is essentially video footage showing the effects of pressing different keys and mouse buttons within the Minecraft videogame.

"Instead of requiring thousands of hours of gameplay recordings with actions, the world model can actually learn the majority of its knowledge from video alone," said Hafner.

"With only a few hundred hours of action data, the world model then understands the effects of mouse movement and key presses in a general way that transfers to new situations. This is exciting because robot data is slow to record, but the internet contains a lot of videos of humans interacting with the world, from which Dreamer 4 could learn in the future."

This recent work by Hafner and his colleagues at DeepMind could contribute to the advancement of robotics systems, simplifying the training of the algorithms that allow them to reliably complete manual tasks in the real world.

Meanwhile, the researchers plan to further improve Dreamer 4's world model, by integrating a long-term memory component. This would ensure that the simulated worlds in which the agent is trained remain consistent over long periods of time.

"Incorporating language understanding would also bring us closer towards [agents](https://techxplore.com/tags/agents/) that collaborate with humans and perform tasks for them," added Hafner.

"Finally, training the world model on general internet videos would equip the agent with common sense knowledge of the physical world and allow us to train robots in diverse imagined scenarios."

        Written for you by our author [Ingrid Fadelli](https://sciencex.com/help/editorial-team/ingrid-fadelli/), edited by [Sadie Harley](https://sciencex.com/help/editorial-team/sadie-harley/), and fact-checked and reviewed by [Robert Egan](https://sciencex.com/help/editorial-team/robert-egan/)—this article is the result of careful human work. We rely on readers like you to keep independent science journalism alive. 
        If this reporting matters to you, please consider a [donation](https://sciencex.com/donate/?utm_source=story&utm_medium=story&utm_campaign=story) (especially monthly). You'll get an **ad-free** account as a thank-you.
    

###### Publication details

Danijar Hafner et al, Training Agents Inside of Scalable World Models, *arXiv* (2025). [DOI: 10.48550/arxiv.2509.24527](https://dx.doi.org/10.48550/arxiv.2509.24527)
																								
																								

                                                        **Journal information:**
                                                                                                                    [arXiv](https://techxplore.com/journals/arxiv/)
                                                            
                                                                
                                                             
                                                                                                            

© 2025 Science X Network

**Citation**: DeepMind introduces AI agent that learns to complete various tasks in a scalable world model (2025, October 25) retrieved 18 September 2026 from https://techxplore.com/news/2025-10-deepmind-ai-agent-tasks-scalable.html