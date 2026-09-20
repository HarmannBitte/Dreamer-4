<!-- source: https://www.talkrl.com/episodes/danijar-hafner-on-dreamer-v4/transcript
     fetched: 2026-09-20T13:37:04Z -->

## Danijar Hafner on Dreamer v4

Talk RL. Talk

Speaker 2:
RL podcast is all reinforcement learning, all the time. Featuring brilliant guests, both researched and applied. Join the conversation on Twitter at talk r l podcast. I'm your host, Robin Chauhan. Today, I'm very pleased to be joined by Danijar Hafner.

Speaker 2:
Danijar is a research scientist at Google DeepMind. Welcome back, Danijar.

Speaker 1:
Thanks, Robin. Good to be here.

Speaker 2:
So this is your third visit on Taco RL. We first talked about Planet Dreamer, Dreamer one back in episode 11 in 2019, and then Dreamer two and three, and director in episode 42. And you know, you recently published your latest addition to the Dreamer series as Dreamer version four, training agents inside of scalable world models with yourself, Wilson Yan, Timothy Littlecrap. It's a very exciting paper and a very exciting series. Your your past Dreamer agents have shown remarkable efficiency and performance compared to other agents of their time, and this one's no exception.

Speaker 2:
So how do you like to describe the primary achievements here with Dreamer four?

Speaker 1:
Yeah. The main achievement is that we have a really scalable world model now that can take on real world diverse data and that we can train successful agents purely offline inside of that world model. So for DreamHut three, previously, the focus was really to make the algorithm robust so it works, you know, out of the box on new problems. You don't have to tune. And that was the prerequisite for scaling things up.

Speaker 1:
Because at scale, it gets really hard to, like, do a lot of tweaking because the training runs get more expensive and so on. So for dream of three, we had a very fast world model based on the variational objective and recurrent neural network. And in dream of four now, we have a very scalable world model that's more heavyweight based on a novel shortcut forcing objective, but basically resting on the principles of what's used for frontier video models. And so we can fit very diverse data. And the challenge was to make those models be conditioned on fine grained actions and get the generations to be fast enough.

Speaker 1:
And then also on the agent side, in all the previous Dreamer versions, we had a closed loop with the environment where, you know, the policy would train only inside of the world model, but then it would interact with the real world to collect new data that gets fed back to improving the world model and patch holes in the world model. And so over time, it would sort of learn all the necessary dynamics about the world. But that becomes really tricky to do when we're talking about real world RL, like robotics, for example, which is what we're moving towards and making big steps towards with 3.4. Because a real robot can't really you can't really deploy, like, a partially trained policy on, let's say, a humanoid robot. It will just fall and break itself and maybe damage the environment.

Speaker 1:
It's also besides that, it's really hard to, set up a lot of diverse like, truly diverse scenes and then reset those scenes between episodes and so on. So that's why it's a big deal to be able to purely learn just inside of the world model and get a a world model from a fixed offline dataset that is accurate enough to then learn successful behaviors without having to touch the actual environment.

Speaker 2:
Now we spoke to Jeff Clune in episode 41 about OpenAI VPT, and I understand that was trying to tackle a very similar problem in terms of the Minecraft setting, offline Minecraft video. And you noted that that Dreamer v four improves over OpenAI VPT's offline agents despite using a 100 times less data. So that's pretty dramatic. How do you explain this performance difference? Or or is it is it many many things, or can you point to a few core core things?

Speaker 1:
Yeah. There there are two key things. So like you said, we used getting diamonds in Minecraft as the main benchmark for the paper because it's a really challenging environment. We already used Minecraft in Dreamer three, but that was in the online setting without any external data. And now we're doing the opposite.

Speaker 1:
We're only using external data from humans, two thousand five hundred hours that were provided by OpenAI contractors. And so it's the same dataset used for VPT or used initially for VPT to train the inverse dynamics model. But then, of course, they used a whole web dataset that's more than 10 times larger and label that with synthetic actions to learn from from that through imitation learning. But the VPT approach, which I think it's a really interesting paper, but I it it just doesn't leverage a lot of learning signal because predicting actions is a pretty, pretty weak learning signal. Actions are pretty low dimensional.

Speaker 1:
And if you have a really high dimensional video input and you're trying to predict something, so low dimensional from it, then you're just not extracting a lot of information. And so you need a lot a lot of data to start to generalize. And yeah. So even those two thousand two hundred seventy thousand hours of web videos of just people playing Minecraft on the Internet was not enough to get a really good policy. And so what's different in Dreamer is basically two things.

Speaker 1:
For one, predicting the future, which is the world model objective, helps you learn really good representations. Because to predict the future, you have to understand the past. You have to perceive semantic details from your past video and then be able to, you know, understand things like objects and how they interact to to forward. And so this gives you really good representations, especially for control because you sort of have to extract almost like a state of the world, at least a local view on the world. And so even just doing imitation learning, by fine tuning the world model instead of just learning a behavioral clonus cloning policy from scratch gives massive improvements, and that alone already beats VPT despite using, only the two thousand five hundred hours of contractor data without any web videos.

Speaker 1:
On top of that, we then get pretty significant improvements by using the world model as a neural simulator to fine tune the policy with reinforcement learning, and that allows it allows us to specify concrete rewards for the things we care about and then to get the policy to directly optimize towards those goals. And so especially on the harder tasks, we see pretty clear benefits. But also across the board, we see that even the easier tasks are accomplished much faster by the policy that has been post trained with RL.

Speaker 2:
Okay. And then you you start with this unlabeled video, and you also you add some action labeled video. Is that right? You have some small amount of of action labeled video?

Speaker 1:
So for the main experiments, we used the whole dataset, the whole contracted dataset, which has video and mouse keyboard actions. Ah, okay. Yeah. And also game events annotated, which is part of the recording format they used. So there are events like mine cobblestone or mine or break woodblock or craft this tool or that tool or pick up this item, that item.

Speaker 1:
So a lot of semantic events, and we use those to specify the rewards. We then separately did experiments to see how many actions are actually needed for training a good world model that accurately predicts all kinds of counterfactual interactions. And so for that, we masked out different fractions of all the actions. And so on the masked out parts, the model was purely training on video. We found that, actually, you can get away with shockingly small amounts of action data or, to be more precise, of aligned video action data.

Speaker 1:
And the model can learn the majority of its knowledge just from video. And it's sort of intuitive if you think about it from a generative modeling perspective. You train a general generative model, and then it's sort of expected that you can fine tune in additional conditioning information relatively easily. But, of course, from the Aural perspective and robotics perspective, this is a really important result because it means that we can actually leverage a lot of knowledge or extract a lot of knowledge out of general web videos, potentially not even like, if you think about robotics, it probably doesn't even have to be video of robots doing things. It could be videos of people doing things, maybe even, you know, third person video and so on.

Speaker 1:
And the model will extract knowledge from that, and it should be fairly easy to then fine tune the model to, let's say, simulate the egocentric experience of a specific robot. Actually, maybe to say one more thing about the action grounding, we did this one experiment where we had where we just masked out different amounts of actions, but we wanted to see not just if the actions generalize in distribution, but also to what extent there is strong generalization into a totally different distribution. And so we did an experiment that I was quite surprised of by the result, which is to split the whole Minecraft dataset into gameplay in the overworld, like the normal world that you know from most of the Minecraft videos with trees and mountains and caves and so on. And the other dimensions in Minecraft, which is the underworld, the nether, and then the, like, end world where you can fight the dragon if you wanna play through the whole game. And so those are, like, very different environments.

Speaker 1:
Same physics, but made out of different materials. You know, the underworld, it's all, like, red blocks and a lot of lava and so on. You don't get to see that in the overworld data at all. And then the end world is sort of like a moon landscape. There's a lot of, you know, empty space and then, like, white blocks and these big towers and so on that the agent would never get to see in the overworld.

Speaker 1:
And so training only on actions for the overworld, but on video from both the the overworld and these additional, like, the underworld and the end dimension, we actually get very good generalization, and the model makes accurate action condition predictions also in those other dimensions. And so just wanted to highlight that because, moving towards training agents in the real world, I think this is really promising because it shows that, there's actually basically nothing standing in the way of just using really diverse web data, even if it's not directly aligned with your robot.

Speaker 2:
Do I understand correctly you do a type of curriculum training through the different types of crafting before you get to Diamond? How does that work?

Speaker 1:
So it's not quite a curriculum. It's actually just a multitask agent, and it trains to equal amounts on all the tasks in parallel. We take the world model, which is, yeah, a sort of diffusion transformer, and then we fine tune the agent into that, and that allows us to reuse the representations and the knowledge that the WAP model has acquired. And so we do that by adding additional agent tokens to the model. And they're part of the same transformer, but there's an important detail about how the attention works where we can talk in more detail about in a moment.

Speaker 1:
But, basically, the agent tokens get to attend to the video tokens and to the past agent tokens, but the video tokens don't get to attend to the agent tokens. So now the agent tokens get a task input, and that's just an embedding of the task. There's, I think, 20 tasks that we broke the whole sequence up to the diamond into. And so those are, like, the natural milestones for, you know, getting chopping trees and crafting crafting table and placing it and crafting a pickaxe and so on all the way to the diamond. And so from so the embedding of this task gets fed into the agent tokens.

Speaker 1:
And then from the output embeddings, we predict the reward model for that task and the policy, and it's initialized just with behavioral cloning. And then, so that way, you get a multitask agent. And there are actually some details, on the RL side for how to get this to work and how to learn this multitask policy robustly. And once you have that, you can then at inference time, you have a controllable agent now, a steerable agent. So we have a a ladder of like, a prompt ladder, which is just the sequence of those 20 tasks and how often you should accomplish each of them before you move on to the next stage.

Speaker 1:
And so that's how we guide the agent through the long horizon task during evaluation in the environment.

Speaker 2:
So is this scalar reward, or is the multitask model this vector reward?

Speaker 1:
It's task condition scalar reward. We also experimented with a vectorized reward turned out to not be necessary, and I think it's more general to have a scalar reward because then you could imagine you know, if you have a vector reward, you sort of need to know all the possible tasks in advance and maybe even have reward labels for all tasks on all your data points. Whereas, if you have a task condition scalar reward, then you could this could even work for, let's say, an open vocabulary task input where you can't really, you know, enumerate all the tasks in a feasible way.

Speaker 2:
Okay. So when we think about moving from version three to version four, you said on Twitter that Dreamer three based on a more lightweight but less scalable RNN, while the lightweight approach still makes sense for easier tasks. So is it is it a case where you would you would select your agent according to the task difficulty and and and how much data like, how much of a data sponge you need?

Speaker 1:
Yeah. Yeah. So for Dreamer three, also worked in Minecraft, but it was, like, 64 by 64 images. And we were using the MineRL competition action space, which has these abstract crafting actions. So you don't need to learn to predict mouse movement and item interactions in the inventory.

Speaker 1:
That's abstracted away. Whereas for Dreamer four, we train on high resolution videos. So you can look at it as a human. You could play the game perfectly well from those inputs. And it's pure, you know, low level mouse keyboard inputs.

Speaker 1:
All the inventory recipes for crafting and so on have to be learned by the model. And we have this, you know, much more diverse dataset of humans doing all kinds of stuff in Minecraft, and a lot of it is not even very relevant for, finding diamonds. There's, like, people building houses and people building, like, really advanced bases and so on and playing through the whole game and whatnot. So it's it's a lot more diverse of a dataset, and the old model just couldn't handle that. And so the RSSM so, basically, starting from RSSM in Dreamer three, this RNN based variational world model, we're first thinking about, you know, we should switch to diffusion transformers because they can fit much more diverse data.

Speaker 1:
But the inference speed difference between those two is about a thousand times. So it becomes very, very slow to do any sort of imagination training in a diffusion forcing transformer. And and so that's a problem even just for solving a single task, but let alone trying to develop a new algorithm where you have to train thousands of agents to figure out the right hyper parameters, the right architecture details, and so on. So a big focus of DreamL four was to operate within the diffusion forcing paradigm. That's, you know, basic the basis of a lot of the frontier video models out there.

Speaker 1:
It can fit very diverse data, but speed it up so that we can make it feasible for imagination training. And so DreamForm four lands sort of in the middle where it's, like, 30 times faster than a diffusion forcing transformer and 40 times slower than the Dreamer three model. So to answer your question about which one to use, I think, yeah, it does really depend on what you wanna do. If you wanna solve low dimensional tasks or relatively small, you know, simple images, not like a real world video input that or task where you have to really understand objects in the scene in detail and generalize to complexity of the real world, but maybe some simulation task. You can do a lot with the RSSM model, and you can do it with a lot less compute.

Speaker 1:
And so for certain research, let's say, on the a role objective, we actually used the Dreamer three agent a lot and iterated on that because we can easily train on, you know, 30 tasks in parallel, 30 different environments even, and make sure that we come up with a robust solution there. So I think for, like, a lot of interesting research questions, they can be answered with, like, a lightweight model like RSSM. And then for tackling real world tasks and more complex tasks and also research that targets, like, efficiency in the actual architecture, then it makes sense to you basically have to use the more powerful model for that.

Speaker 2:
And now some of your past dreamers, you know, your role model had some special components to deal with stochasticity in the environment. And of course, Minecraft is fairly deterministic. Does can you say more about how Dreamer four deals with stochasticity? Is that an issue at all, or is that just happens to be how Minecraft is?

Speaker 1:
Minecraft is actually very, very stochastic. Oh, okay. It might not seem that way, but there's actually from an agent's perspective, there's no difference between a partially observed environment and a stochastic environment. Right? Like, when you turn around and you don't know what's gonna be there, then that has to that like, you'll get surprised by whatever gets filled in there, whether there's, like, you know, there's mountains or there's a river and what blocks there are and what creatures there are and so on.

Speaker 1:
So as you walk around the world, it's very partially observed, and there are a lot of things the agent gets surprised by, and so it's a really stochastic environment. And that's a big reason why we actually had to move away from the variational model Mhmm. In Dreamer three, which can handle a moderate amount of stochasticity very efficiently. But the diffusion based approach in Dreamer four can handle much more complex correlations and multimodal distributions over the next frame.

Speaker 2:
Take a step back. If we go back in world models and we can we compare Dreamer on a very high level to, like, professor Rich Sutton's Dyna architecture, or maybe a purely offline Dyna, if that makes any sense?

Speaker 1:
Dyna is the sort of classical framework for, like, a hybrid model free model based RL loop, or agent blueprint. So you have an agent that interacts with some environment and gets data from that, and it trains on that data using model free RL. And it also learns the dynamics model and then uses that to further train the policy in imagination.

Speaker 2:
Which is kinda like your previous dreamers. Right? Is it more like that?

Speaker 1:
Yeah. Exactly. So yeah. We actually don't need any environment interaction for getting diamonds in Minecraft with Dreamer four. Of course of course, I think there so we did we did a lot of experiments that didn't make it into the paper, including, like, very various forms of, like, multimodal models and art like, more complex architectures and larger scale pretraining.

Speaker 1:
And one of them was also to do, like, a small number of rounds of corrective data where we, you know, run the whole Dreamer for pipeline and then deploy the agent in the environment to evaluate it, but we record that data, and we feed it back, fine tune the model on that, and then do a bit more RL on the policy in that improved web model. And so that does help. And, especially, you know, of course, depends a lot on the actual data you have and how well that covers all the different things the policy could be doing. So I I think, you know, environment interaction and learning from that is generally a good thing. It's just it's just a big operational overhead, so you wanna do as little of it as necessary.

Speaker 1:
And so, yeah, I think in general, you just wanna squeeze as much data, as much performance out of the data that you can get so that you know, because real world interaction is often the bottleneck, in, let's say, robotics applications. And so, yeah, it sort of fits in with Dyna quite well, where the idea is also to use a model to make it more efficient, but we're just, like, really leaning in on the imagination training. And I personally don't even think that model free the model free loss of Dyna will be that necessary in the future.

Speaker 2:
Would you say you're a model based maximalist, in terms of RO?

Speaker 1:
What does model based mean? So if I wanna train a robot to walk around, and I do that by training a policy with PPO inside of a MuJoCo simulator. Is that model based?

Speaker 2:
That's a

Speaker 1:
very important model based. Right? Because it's using a model of the of the real world to train a policy. For certain things, like, you know, Newtonian physics are like, we can simulate them very well, especially if it's, like, not a crazy number of objects and if, you know, their shapes are not too complicated and so on. And so it makes sense to then just use a manually specified model for that.

Speaker 1:
And then if we want, let's say, robots that, you know, really deeply understand the physical world and perceive different objects and so on, that becomes a lot harder to simulate, especially not just looking at those objects, but interacting with them in all possible ways. And then there's articulated objects, like the keyboard in front of me. You know, it's very hard to generate those types of those types of objects or drawers and in the kitchen, let's say. It's very hard to generate those at scale in a diverse way for a classical simulator. And so, of course, there are people pushing that direction, and they're making progress.

Speaker 1:
But seeing this tremendous progress in video modeling, I just I think it's pretty clear that we'll get to this really diverse simulator more quickly by just training on pixels and training on diverse web data. And all the data is already there to learn almost anything about the world. And so then so so, yeah, I think model based will be quite important, coming back to your question. I also I would say, though, that you can model free RL can still help you if you have a really good starting point. So if you have strong representations and then you do behavioral cloning on that, you get a policy that works most of the time, but maybe it's just a little slow, and sometimes it's get it gets stuck in ways where maybe it's not causing damage, but it can't progress towards the task, then fine tuning that with a little bit of model free on real data, seems like a good idea.

Speaker 1:
But I just don't yeah. It it'll definitely help, but I think, using a video model will just be an an even more powerful approach. Because then you cannot just fine tune in a couple of you know, in a handful of scenarios, but you can actually use the video model to dream up a really diverse distribution of of scenarios that that the model can envision based on its pretraining knowledge and train your robot in all of those scenarios. And I think that's how we'll get, like, truly general robots.

Speaker 2:
So I remember Yan Lakun talking about this, you know, how you do video predict prediction. If you balance a pencil, you can't you know, an expectation model is gonna is gonna pick one way for it to fall, and you don't really know. So if I understood do I understand correctly, the the type of diffusion model that you would use would predict a distribution of outcomes for that or a different one each time it's sampled? Is that how you deal with the stoke SSC?

Speaker 1:
Yeah. That's right. You can sample from the model, and you'll potentially get a different outcome every time. And so that way, you can train your agent to learn what to do in all these potential scenarios.

Speaker 2:
And this form of model is gonna give you results that are that really cover that distribution and that have the right coverage. I I guess models a few years ago weren't very good at that. They would kinda collapse.

Speaker 1:
Yeah. Diffusion models cover modes pretty well. There's a little bit of mode collapse that you can get from discretizing the sampling process too harshly because you are sort of skipping over a bit of diversity if if you do fewer forward passes, but that's that's pretty minimal compared to, you know, how well it can fit a diverse dataset. And, yeah, I I agree with a lot of things Jan says and advocates for. And, I mean, he's using diffusion models for the dynamics part of some of the work they've been doing, and and I think that's a good idea.

Speaker 1:
I think also the, you know, the focus on learning good representations is really important, and there's a lot lot of headroom there for improving agent performance by learning better representations.

Speaker 2:
So I understand you're using shortcut forcing for your, as part of your dynamics model, from a recent paper, you wrote in 2024. Can you tell us a little bit about, shortcut forcing and and how that helps?

Speaker 1:
The previous paper you mentioned introduced shortcut models, and that was work done with Kevin Frantz. And, yeah, he's a brilliant guy, and it was really fun working on this. And the goal for that was really to speed up diffusion model inference and to do it in a really simple way. There's various ways to distill diffusion models after after you've after you're done training them, but it's not super practical because then you have to decide when to cut off your training run. And then there are consistency models that also try to speed up diffusion models, but they're pretty finicky to get working and often need schedules.

Speaker 1:
And, you know, then there's continuous time versions of that that need more expensive computation. And sort of yeah. There wasn't really a satisfying solution of an objective that I can just train with, and I will get a model out of it where I can later choose how many sampling steps I wanna do. Right? And maybe as a little bit of background, I should briefly summarize how diffusion models work in general.

Speaker 1:
So we've been talking about diffusion models a lot. So, basically, a diffusion model is a neural network that learns to denoise. So you give it an input, and it's, let's say, an image of your dataset with a lot of noise added, and the diffusion model tries to predict what the clean data point was. You train on images with a lot of noise on them and images that only have a little little bit of noise on them, and so you can then generate from this model once it's done training by starting with pure noise and asking it, you know, what could the clean image be? And it will not be able to make a very good guess because no information about what the image should be based on just pure noise input, but it will make a guess, and you can go a little bit in that direction.

Speaker 1:
So you interpolate, and you move a small step from the noise in the direction of what the model thinks could the could be the clean data point. And so now you have a slightly better guess about what the corresponding real image would be. And so you itch you repeat this process. You then give this slightly less but still mostly noise input to the model again and ask it for the clean data point. And so you end up following a trajectory of small steps that starts from pure noise and goes all the way to a clean data point that looks like it could have been in your dataset.

Speaker 1:
And, of course, the diffusion model generalizes, so it will general generate things that aren't exactly in the in your dataset. So this approach is very effective at modeling complex distributions. Right? But the issue is doing all these little refinement steps during generation just makes it very slow to sample from the image. And so with shortcut models, we condition the model not just on the noisy image and on the amount of noise, like the current noise level, but we also tell the model how big of a step it's supposed to make.

Speaker 1:
So it doesn't just learn the instantaneous direction, but it can learn to make a jump forward in in that sampling trajectory. And so you can learn that very efficiently by bootstrapping from the model itself. So, you know, for the smallest possible step size, you just train it like a diffusion model, and it will make this tiny little step. But then for for twice the step size, you can get a training target by asking your model to make two small steps with the smallest step size from the same starting point, from the same noisy training image. And so you get an idea of where the two small steps lead to, and you can train the model when you condition it on making a larger step to end up at the same point.

Speaker 1:
Right? And then you can do that for any you know, for two times the step size, four times, eight times that step size, all the way to going in a single step from pure noise to a clean image. And so that's how shortcut models work. And, yeah, it's very stable training objective, and you don't need to schedule anything. And, you know, for video, we extended it to the shortcut forcing approach, which takes the best of both worlds from shortcut models and another approach called diffusion forcing.

Speaker 1:
And so I'll explain that too. Diffusion forcing is a way to extend diffusion models to time series. So instead of just deciding how much noise to add, let's say 50% noise to your input image, and then you have, you know, the the Gaussian noise and the input image, and you take 50% of each and add it together and give it to your neural net. Instead of that, you can have a video with a lot of frames, and you choose a different noise level for each frame during training. You still train it to just predict the clean input.

Speaker 1:
So what that lets you do is the model gets used to having certain frames be more clearly recognizable and others being harder to recognize during training. And so then you get a lot of flexibility when you want to general, generate with that model. Right? So you could generate with that model in a way where you're just creating a whole block of video in one go, where you happen to choose the same noise level for all the frames that you're trying to generate. But you can also generate one frame at a time by giving it almost clean inputs for all the past frames and then pure noise only for the next immediate frame that you want to generate.

Speaker 1:
Do a couple of forward passes on that to to predict the clean frame, and then move on and generate the frame after that and so on. Diffusion forcing basically says, assign different noise levels to different frames in your input sequence. And so then it allows you to generate causally later on. For example, that allows you to generate blocks as well or some some somewhere in between where you have, you know, a block causal generation and so on. And so with shortcut forcing, we get a very efficient version of that, and that alone ends up speeding up speeding up generations by, like, 13 times.

Speaker 1:
And then the remaining improvements we got or we needed to speed up the model more were architectural improvements.

Speaker 2:
So before you could do this agent, you actually had to improve the underlying general models that really had nothing to do with the RO. Is that am I understanding this right?

Speaker 1:
Yeah. That's exactly right. We knew we needed this. We wanted to use diffusion models, but they weren't fast enough. So we worked on a whole project to speed up diffusion models.

Speaker 2:
Amazing. Quite a flex. And that worked amazingly well. Mean, none of this would have worked if you had those those models so slow. Like, is is this why you can look so far in the future because your models have are so high fidelity?

Speaker 2:
How do you how do you get that ability to go far into the future without the accumulating errors that we normally see?

Speaker 1:
Yeah. Okay. So there are a couple more details after we got shortcut forcing to work in the first place. We refined it further to help reduce artifacts that can come up in auto aggressive generations. So traditional video models actually usually generate whole blocks of video.

Speaker 1:
Maybe they generate a whole, like, twenty second clip jointly with a bidirectional transformer. Or maybe they do have some context, but they extend the video by a block that's a couple seconds long. And so if you do that, it's a little bit easier for the model because there's fewer extension steps in time, and so there's less of a chance for small prediction errors to accumulate over time and then trip up the model. For purely frame autoregressive generation, and that is something you do need if you wanna train your agent at a high control frequency. You have to generate some new input for the agent to then choose a new action based on that and feed it back into the model.

Speaker 1:
So you need this very tight loop between the policy and the video model. And so one challenge with that is that there is a high potential for small prediction errors to accumulate over time. And, yeah. So a good amount of work also went into, figuring out how to reduce those, those accumulating errors, which, you know, is basically a problem with auto aggressive video generation and and has always been. And we ended up at a point at a point where you can generate from the model for basically as long as you want to.

Speaker 1:
I've played Minecraft in this model for, like, twenty minutes, and it always makes reasonable generations. And sometimes, if there's a lot of moving objects at once, it gets a little more blurry, but it recovers a few seconds later. So it never falls off the manifold and, like, gets tripped up or anything like that. And so the main the main thing that helped with that was to predict the next frame, which is how I already explained everything so far, but it's actually not the most common way diffusion models work. Because instead of predicting the clean data point, you could also predict the noise, or you could predict the direction from noise to the clean data point, And you can convert all of these into each other if you know the, like, noisy input to the neural net, but there are different trade offs in terms of, basically, how much capacity the model assigns to the more noisy images and denoising those and denoising the cleaner images and so on.

Speaker 1:
And people often train, a yeah. I guess, like, a flow matching approach where you usually predict the velocity, so the directs you from the noise to the data. And the issue with that in the video generation it works great for images, but the issue with that for video generation is that your neural net needs to preserve a lot of information about the exact noise pattern. It is activations all the way throughout the transformer because it needs to predict this velocity, contains, you know, which, like, really depends on what the input noise was. And so if it, like, messes things up slightly in the prediction, then, you know, there's a lot of, like, really small details the model needs to get right to be able to generate a clean next frame.

Speaker 1:
Whereas if you're just predicting the next image, there's actually a lot more structure in that. And so, the model can really focus on predicting only the stuff that it actually needs to predict, and it's a bit lower frequency and harder to make these really small mistakes that or there are few of these really small mistakes to make in the first place that would then add up over time.

Speaker 2:
So you said you would play up to twenty minutes. Is everything you're doing within the distribution of the training data? How do you think about Oud out of distribution in this setting?

Speaker 1:
That's always a good question. So it's not limited to twenty minutes. You can play for as long as you want to, really. The context length of the model is limited to a couple seconds. Even though we improved that quite a bit compared to previous models, it's still quite limited.

Speaker 1:
And so if you walk

Speaker 2:
That's like frame stacking that's used to predict the next one. Is that what you is that what that means? Or

Speaker 1:
Sort of. I mean, there's no actual frame stack stacking happening, but the transformer operates on a sequence of frames, and it can attend to its past activations, but only up to that many time steps. And so then past that, the old time steps will get evicted from the k v cache of the transformer, and so the model won't have access to that anymore. And so what that means in practice is if you, you know, let's say, walk into a house and you, you know, you do something in the house for thirty seconds and you walk back out of the door, then the outside world will look different suddenly because the model can't access that that anymore. And so it'll have to fill it in with something plausible again.

Speaker 1:
And so that's, like, one of the big areas for improvement, just giving really long term memory to web models, but also and video models, but also to agents in general.

Speaker 2:
And we we hear about in offline RL things like overestimation and and algorithms like CQL being needed. And then now you're in a fully offline setting. Is any of this relevant, or is this just not a concern here? Because we're we're somehow in distribution, or maybe the KL control just handles this somehow.

Speaker 1:
It is somewhat relevant. I don't know if I've heard anybody say that CQL works that well in practice. I think But it

Speaker 2:
was the reason why it was a it was more like an illustrative algorithm, the overestimation problem.

Speaker 1:
Yeah. I mean, of course. I think, yeah, doing offline RL is if we can crack offline RL, that that'll, like, really, yeah, be very relevant for robotics. And there have been various attempts made in the space of model free offline algorithms, and CQL is one of them. There are fewer details to get right.

Speaker 1:
Right? Because it's, like, simpler in its implementation and hyperparameters than a model based approach. With a model based approach, though, you just get a lot better performance in practice right now. And so I actually think just RL in imagination is the right way to do offline RL. And you still need to be a little careful about going too far out of distribution.

Speaker 1:
So for your previous question, when I, as a human player, interact with the world model, everything I do is out of distribution to the model. Right? It's never seen that action in that situation before. It's probably not even ever seen that same situation. But there are sort of semantically more different things.

Speaker 1:
You could go more out of distribution at a at a higher level, let's say. Like, yeah, you there it is possible to exploit the world model, And you have to sort of if the world model is trained on a certain data distribution and that doesn't cover everything well enough, then you have to make sure that your policy doesn't go too far away from sort of the average human policy. And we do that with a simple KL constraint the same way it's done for language models when people train them with RLHF, and that works great. We also noticed that when we trained on corrective data, which is not something we ended up putting in the paper, but then you can get away with a much weaker KL, which also makes sense because even just after a pretty small number of rounds of correction, the world model starts to get really robust to exploitation.

Speaker 2:
On a on a high level, what I'm hearing, if I understand this right, is that there's you have pretty good coverage of your actions space, so you don't have to worry too much about a completely unknown actions or

Speaker 1:
is that is that the case? Yeah. I'll give you an example. So there's pretty there's very good coverage when it comes to moving the camera and walking around in the world. And and then when it comes to, let's say, inventory interactions, it's a bit different because there are certain scenarios that are not covered in the data, and it's, like, not really obvious what the model should predict.

Speaker 1:
So for people who've played Minecraft before, they will know that there are, you know, wooden pickaxes and stone pickaxes and iron pickaxes and diamond pickaxes. And so you craft them all in a pretty similar way. Right? There's this crafting grid, and you'd put two sticks above each other, and then you put, horizontally, you put three blocks of the material, like three stones, for example, and you get a stone pickaxe out on the other side. Now we've seen the agent attempt in imagination to craft other types of pickaxes where use, like, some rock material that you couldn't normally make a pickaxe within Minecraft, but none of the human players ever tried that.

Speaker 1:
And and so there's no information for the world model to think that that would fail and actually generalizes in a pretty cool way by letting the agent craft this this pickaxe out of other materials, and and a pickaxe comes out. But that doesn't actually work in the real game. And so then that's an example of something where you either need corrective data or you need to keep the policy a little bit closer to the behavioral cloning policy that was trained on the human data.

Speaker 2:
That's kind of almost like a charming out of distribution thing or a mistake. Right? It's like almost like a cute nice thing as opposed to when we're talking about safe RL and it's doing something that's just, just you wouldn't wanna do. I guess, there's not a lot of that in in Minecraft. Right?

Speaker 2:
Unsafe actions?

Speaker 1:
Yeah. I mean, deploying a policy in Minecraft is pretty safe. I can't think of an example where something, like, would have gone, like, catastrophically wrong. I guess

Speaker 2:
how how you treat the dragon probably really matters. And

Speaker 1:
Right. Yeah. I mean, it never made it to the dragon. So that's also another thing people you know, after Dreamer three already, people said, oh, Minecraft is done now as a benchmark, and then we released v four. And if you'll say, oh, you're still doing Minecraft.

Speaker 1:
Is Minecraft done now? And Minecraft is very far from being done for AI. There is so much more you can do. Getting diamonds is only a small part of the game, and you need to touch maybe, like, on the order of 10 items to get to diamonds, but there are 500 plus items in Minecraft, and there are hundreds of achievements that are really hard for humans to accomplish. I just recently came across, some YouTuber who has been trying to get all the achievements in Minecraft, and I just saw, you know, there's, like, 20 streams already uploaded to his channel.

Speaker 1:
They're all, like, six hour videos, and he's, like, you know, maybe three quarters through. So Minecraft is a really, really challenging test bed, for humans and and even more so for AI, and I think we can actually it's actually quite ideal for for testing AI agents, and it will be for the next coming years.

Speaker 2:
Now a while back, I guess, and this is ICLR twenty twenty two, you had Crafter, which was kind of a similar to Minecraft open world game. Is that still relevant to you, or do you feel like we're you you move beyond that now?

Speaker 1:
Crafter was actually meant as a test bed for Minecraft because I wanted to do Minecraft research, and I knew the Minecraft simulator is quite slow. Especially rendering on CPU with higher resolutions gets very slow. It gets slower than real time. So I wanted something to iterate on quickly, but that replicates a lot of the challenges that would be posed to the algorithm Mhmm. When learning on Minecraft.

Speaker 1:
There's a stepping stone. Yeah. Exactly. It's not just that it sort of looks like a simplified two d version of Minecraft, but there are also all these different items, all these different, you know, steps towards getting diamonds, really long horizons. Every episode has a totally random randomly generated terrain, so you can't really overfit to remembering where certain resources are placed.

Speaker 1:
You have to defend yourself. There's monsters and so on. So, you know, I think for any new algorithm, you always wanna train it. You always wanna get it to work on something where you can iterate as quickly as possible on. And so I'm still using, you know, simple toy tasks.

Speaker 1:
I don't think necessarily publishing results on, let's say, Atari and these type of, like, Aural tasks and maybe even Crafter makes that much sense in itself anymore because I wouldn't be unless it's, like, a really significant improvement, of course. If you can get, you know, human performance with 10 times less data, that's still really interesting. But if you're getting, like, a 30%, 20% relative improvement over state of the art, it's, like, quite possible that that wouldn't actually transfer to a large scale scenario and in whatever's environment. So so it's useful for debugging and unit testing. Very useful for that, but not in terms of pushing the frontier.

Speaker 2:
Mhmm. I I think I remember reading that that David Silver started with with much smaller Go boards, like very small boards, and then just worked its way up. So

Speaker 1:
Yeah. Pretty similar. For Go, you yeah. There's different sizes of the board and, yeah, makes the game easier and faster to play and so on.

Speaker 2:
What are the some of the main innovations in the Efficient Transformer? And, especially, I wanna understand spatial versus temporal components being treated differently in this in this transformer.

Speaker 1:
We yeah. We start with sort of pretty standard transformer that, you know, uses RMS norm and prelayer norm yeah. Prelayer norm and and swiggle activations. So, yeah, pretty standard initial setup, and then we applied various architectural architectural changes to that to make it more efficient for video data. And so in general, for video, you have a lot of tokens because each frame already will be, you know, probably at least 64 tokens up to, like, maybe a thousand tokens or so, depending on your tokenizer and the, like, fidelity you need.

Speaker 1:
And and so then if you have a high control for or a high frame rate of 20 frames per second, you know, even just one second of video, you know, could could easily be, like, you know, like, 16,000 activations or 16,000 tokens, let's say. Whereas for a language model, 16,000 tokens is, like, pretty decent for training. Like, you can you can fit, like, decent documents into that context. But for video, that's only one second of video. And the challenge is even harder for us because we wanted frame level generation.

Speaker 1:
We didn't wanna do any like, we didn't wanna cluster multiple frames together into video chunks because that would then force us to give up, how fine grained the actions can be. And so then the policy wouldn't be able to make as fast paced decisions. So so there's a lot of tokens. And then the question is how do you build an architecture that can process them all, in a way that's relatively efficient, but at the same time, it still maintains really high model capacity. And so, yeah, those are, of course, like, pre it's a pretty direct trade off.

Speaker 1:
And so there are a couple of improvements that all work together to make this possible, and it's sort of they don't perfectly stack in terms of the speed ups they get. But, yeah, one of them is to you know? So let's say you have a batch length of, like, one twenty eight frames, right, which is, like, six seconds of video. And each time step, you have, let's say, two fifty six spatial tokens. So that's an overall context length of 32,000 tokens for each entry in the batch.

Speaker 1:
And so if you just did dense attention, you know, it'd be it'd be, like, quite expensive, especially during generation. Right? Because to generate one more frame, you have to attend to all the past you know, each token in this new frame would have to attend to all the past 32,000 tokens. And, yeah, of course, attention has, like, quadratic complexity, and and also just loading the KV cache into memory is a bottleneck during inference. So very easy thing.

Speaker 1:
I guess at a very high level, it was quite surprising that you can get away with not that many temporal connections. Right? So a big thing we do is to factorize the attention into you know, some layers only do spatial attention. So each of the two fifty six tokens within the same frame only attends to the other, you know, two fifty five tokens or, I guess, itself too. So two fifty six tokens at that same frame, but not to any other time step.

Speaker 1:
So it's only local processing within the current frame. And three out of four layers three out of every four layers in the transformer are only spatial. Right? And so that really speeds things up both during training, but also during generation, especially because you don't have to attend into this really long KV cache memory for most of your layers. And but since there's a lot of local processing to do for video generation, that actually barely hurts performance at all.

Speaker 1:
And so especially if you compensate for you know, the training gets a lot cheaper as well. And so you can then, in the same amount of wall clock time, using the same amount of compute, you can train the model longer. And so you end up with a better model from making that change already.

Speaker 2:
That is so interesting. Where did that idea come from?

Speaker 1:
There's a couple of models that, like, recently I think people have been doing this for a while, but Oh. Even publicly, I guess there are a couple models now that do that. I think I think Llama was, like, the one that actually sort of published this openly. Llama four?

Speaker 2:
Oh, in a in a text model.

Speaker 1:
Yeah. Yeah. I mean, the architecture

Speaker 2:
is space still in a text model?

Speaker 1:
Oh, sorry. So what people the the analog of that in text models would be to have alternating context lengths. So have a couple of layers with very short local context. Mhmm. And then every now and then, you have a a layer that has,

Speaker 2:
like Oh, interesting. Okay.

Speaker 1:
Context. Right? And it's very similar, I guess, in the video case. You could always think of the video to operate on a two d grid where this is spatial and a temporal dimension. But you could also just flatten that, and it gets sort of quite similar to, like, a sliding window attention where the spatial attention now means you attend to, like, the last two fifty six tokens, and the temporal attention means I guess, either you tend to all the pass tokens if it's dense, or if it's axial, like in our case, you tend only to every pass two fifty sixth token.

Speaker 1:
Right? So the, let's say, top left corner of the image only attends to top left corner of the previous frame and the frame before that.

Speaker 2:
I see. The this issue comes up once in a while of, like, the pixel problem. You know, in an Atari game maybe it's not so true in Minecraft, but in an Atari game, you know, you could have just one pixel that's a bullet that's coming through, and and it's so small when you have a reconstruction objective, it might not be picked up or not much emphasis given to that that pixel, but it has a lot of it has a lot more importance to the agent than a random pixel. Does that does that come up at all when you're using reconstruction?

Speaker 1:
Yeah. It can come up. So we initially had some challenges similar to that for inventory predictions where our tokenizer was too compressed, and so it wouldn't be able to reconstruct the inventory, like, the item count, precisely. And so maybe you have eight planks, but in the reconstruction, you have, like, seven planks suddenly. And so increasing the bottleneck in the tokenizer helped or basically giving it more spatial tokens.

Speaker 1:
Yeah. It's a latent tokenizer where you have image patches, and then you also have some learned tokens. You encode everything together, and then you use the learned tokens to read out a representation that gets projected to a smaller channel dimension. There is a 10 bottleneck, so very simple, just a 10 activation to bound the representations between minus one and one. And then the same architecture mirrored for the decoder.

Speaker 1:
So you take the representations, project them up to the model dimension, and then you concatenate, like, 900 or so learned embeddings from which then you run the transformer on the whole on the representation tokens and on the learned tokens, and from the learned tokens, you then predict the image patches back. So, yeah, there's no variational autoencoder or anything like that either. Just a ten h bottleneck. And and so, yeah, if you make the bottleneck big enough, then the model can be almost lossless, at least in terms of, like, visual perception. Like, when I look at the reconstructions, it's very hard to tell that they're not real.

Speaker 1:
There's maybe, like, a little bit of maybe they're, like, a tiny bit more blurry, but as long as they get all the details in terms of, you know, like, little numbers and so on, you're good. And then the limitation just becomes how big the diffusion transformer on top of that is.

Speaker 2:
Okay. But let me ask you. If you wanted to work with the environment like Minecraft except it this version had like bullet pixels in it Mhmm. Reconstruction would be challenging. Right?

Speaker 2:
Is there something you would adjust in the in your objective or something that would allow it to give more importance to modeling those?

Speaker 1:
It's a really good question. It's a really good question. I think reconstruction is not the right objective for representation learning in general, and I think that's, like, relatively clear in in the field in general. There are various different objectives for learning representations out there. They have all the different trade offs, and we have played around with different ones, and we've seen different, like, benefits and downsides.

Speaker 1:
I think, you know, if if you care about this from a practical perspective, you wanna solve a real problem where there's certain things about the input that matter, then I would just get some contractors to annotate that signal that matters and predict that from the representations with a readout head. And so that way, you can be certain that the representations will pay attention to that. Mhmm. If it's more like an academic pursuit and you're thinking about, you know, is there some representation like, I think in general, it's not possible for any objective to sort of know a priori what you will care about. Mhmm.

Speaker 1:
So your best bet then might be to use the closest you have to, like, a task specific loss. Like, you know, maybe you're not annotating the specific aspect of the input and predicting that, but let's say you can backpropagate action, gradients for predicting actions or predicting rewards into the tokenizer. And we have also played around with that and gotten that to work, but at least for Minecraft, the benefits were not large enough to justify the complexity. I don't really know if we're thinking, like, long term for real world, let's say, you know, a robotic system that interacts with the the world, like, people's households or, like, factories and so on. I'm not sure.

Speaker 1:
Like, I think it's really, like, an open question whether something really task specific will be needed, or we can get away with just general representation learning objectives. Because usually, like, individual pixels don't really matter. I mean, our retina doesn't even have pixels in that sense. Like, we we don't get, like, a stable image grid. We get very noisy firings that are async in time, and our brain reconstructs an image from that, which is already a much more stable representation.

Speaker 2:
Like, I sort of agree in the sense that there's no in real life, there's rarely a a pixel that's, know, that's gonna make all the difference. But on the other hand, it's that the general principle that the size of the thing or the amount of data you have on it is not necessarily proportional to the importance of it. And how to deal with that is sometimes Yeah. A very imbalanced thing. Right?

Speaker 1:
Yes. I totally agree with that. So but I think it yeah. So it's it doesn't have to be a tokenizer question. You can have a tokenizer that's very compressed and learns very semantic representations for what you specifically care about, and that can let you get away with a smaller diffusion transformer or smaller dynamics model on top or smaller policy transformer on top of that tokenizer.

Speaker 1:
But the problem will be that there's, like, a chance that those representations discard information you actually need, so then you might have to back prop those downstream losses into your tokenizer. I think, actually, at some point, we'll just train all the model components end to end. There won't be, like, a phase to train your tokenizer and then freeze it. It's it's not practical because, ultimately, you want to squeeze out efficiency. Or it's practical short term, but once you wanna squeeze out more efficiency, you will just wanna train everything end to end.

Speaker 1:
On the other hand, you could have a tokenizer that is pretty shallow and has pretty high dimensional representations that where you can be almost certain, like, doesn't really discard anything important. And so then you might just need a bigger model on top of that to make sense of those representations. And, yeah, and so then, you know, the, like, one pixel in the corner is clearly in the representation, but maybe your video model will actually not learn to pay attention to that pixel because there are much more important things to pay attention to to predict, like, larger objects in the next frame correctly. And so then you're at the mercy of the video model learning things in the order in which it helps it reduce pixel loss or or, I guess, diffusion loss in representation space. And so, yeah.

Speaker 1:
Like, the the things that tends to learn last are things like, yeah, very small objects, but also really long range temporal correlations. So the really semantic long range correlations will be learned last, and I think that's also an open challenge. If we can prioritize those bits somehow, that would let us learn semantically correct models much faster.

Speaker 2:
And maybe very stochastic things or fast moving things. Is that in that set too or no?

Speaker 1:
If something is static, it's easier to predict, so we learn faster or earlier. But even things that move quickly yeah. I guess the harder it is to predict, probably, the later it takes the the longer it takes for the model to actually learn that. Almost by definition. Right?

Speaker 1:
That's what it means for it to be harder to predict maybe.

Speaker 2:
So can you tell us a bit about the experience of of doing the Streamer four work? You worked with some other people. This must have been a very long project. You talked about experiments that we didn't see in the paper. This might it must have been quite an epic journey.

Speaker 2:
Can can you tell us a little bit about how that how that all unfolded and and what it felt like?

Speaker 1:
I think, in a sense, in a way, we were quite lucky to be able to work on this slightly more long term research project at a frontier lab and get support with, you know, very good computational resources. I think we I think we probably were the team with the most chips per person at the whole company. And so, yeah, I'm really grateful that, you know, GDM supported us in that way and let us do really interesting work. So, yeah, I mean, as everything moves more towards productization, I think training embodied agents is still, like, one of the biggest open frontiers towards AGI. And so, yeah, it'll become sort of mainstream part of mainstream frontier models at some point, and that's also pretty exciting.

Speaker 1:
But, yeah, for me, I guess that'll be the point when I'll start working on those models too. But, yeah, it's just incredible. And it was a good collaboration also. Wilson and I started working together at Berkeley a while back and, had very complementary skills. He had a lot of, you know, deep expertise in multimodal models and video generation.

Speaker 1:
And, yeah, then my experience in model based RL and shortcut models and so on came together very well. And, yeah, it was just good for, like, a long stretch of time to just push really hard, have all the resources to do it, and get some cool stuff to work. And and then also, like, yeah, actually get the results that we've been hoping for, like, towards the end. Just like, okay. We actually finally got our diamonds.

Speaker 1:
You know? There's, like, probably two months where we were, like, pretty close. I wasn't quite there yet. The model could get all the way to, like yeah. I guess, like, once the whole pipeline started working, we knew there wasn't any, like, obvious bucker.

Speaker 1:
So we had these success rate plots for all the different stages towards the diamond that we have in the paper too. And every week, they just moved up a little bit. And so we didn't really know necessarily what was the next thing we should be trying at times, but we knew that at a meta level, every week, we saw the whole success rates shift further to the right. So we could almost, like, project out, you know, this is roughly when we'll get to diamonds, we can release the paper. Yeah.

Speaker 1:
And then also being able to release the paper was great. Okay.

Speaker 2:
So you weren't sure if that would be the case, maybe?

Speaker 1:
Yeah. I mean, there's, like, a process for that. But, yeah, it took some asking around, but, ultimately, everybody was happy with us releasing it.

Speaker 2:
And now with the with the old Dreamers, we have some code released. And are you expecting that with Dreamer version four?

Speaker 1:
Probably not. I would love to release code and checkpoints, but I think getting the paper out was already exceptional enough in the current climate. Also, with just what models being so relevant to, you know, part of, like, frontier models that have native video integration and then also people starting to get really excited about the possibility to build general robots, it would probably be too hard to release those things.

Speaker 2:
So if we just step back and look at the broader, picture in terms of robotics, can you talk about, the major challenges in robotics and and how they relate to to some of these themes?

Speaker 1:
People talk a lot about AGI, and they mean different things by that. But for me, that clearly includes being able to perform tasks in the physical world. And, I mean, long term, I think there are still, like, various capabilities of the human brain that we haven't we're not even that close to replicating an AI, even though, of course, the current models we have are already way better than humans at various things too, especially in the digital domain, especially when it comes to sort of knowledge based and question answering tasks. But for robotics, I mean, there have been there has been a lot of activity recently, hardware is becoming really affordable, like general hardware, humanoids. There's so many companies building them, pushing down the price.

Speaker 1:
It's, like, already significantly below, like, 10 k for for decent robot, maybe a little more with hands. So the real bottleneck at this point is just clearly building general AI to control the robot. And we can't really you know, I think people say a lot that it's data bound, and I think that's partially true. I think it's partially also just algorithm bound. Like, even if we had really diverse data or even if we just you know, somebody spent a lot of money to collect a lot of data, That alone wouldn't be enough.

Speaker 1:
You actually need an algorithm that can soak up all that data. And even more so, you need really diverse data, and it's not even really clear how to collect that in the real world at scale, like generating or creating diverse scenarios even if you have humans. Like, if you if you have thousands of human operators, teleoperating robots in various scenarios, it's actually quite hard to even create the diverse scenes and then reset them and so on in a way where you think of all the ways that in which the scene could differ at, you know, deployment time. And so so, yeah, I think, you know, for one, interacting with the real world with a partially trained policy is just really hard because the robot will probably break pretty easily. This is, like, specifically, I guess, for humanoids.

Speaker 1:
If you have arms mounted on a table, maybe you can get away with a bit more. But for the general case, you know, you definitely can't learn from, like, a bad policy and then refine that with Aurel directly in the real world. It would just cause too much damage. And and so yeah. Like, world models seem like the most promising path to get there because they they solve multiple problems.

Speaker 1:
Like, for one, we've actually seen really good generalization of pretrained video models that have been fine tuned with action data of robots to then be able to simulate the robot in really diverse scenarios that you never collected robot data from. So they can transfer a lot of their pretraining knowledge and then simulate a robot in those scenarios. So that seems like the only way we have right now to really train robots in a diverse in a in a broad range of diverse environments or scenarios. And then the second part is, of course, you hopefully can do it purely offline or maybe only with a small round with a few rounds of corrective data collection, where, you know, most of the RL training can happen in imagination. And, of course, you know, a lot of the demos we see in robotics right now are based on representation learning and behavioral cloning, and I think that's a great starting point.

Speaker 1:
And we there's even various things we can still do to further improve that, but it doesn't really yet seem like we'll get the strong generalization out of that and, you know, efficient enough policies to really produce, like, a, a general robot just that way. So I think, yeah, basically, learn good representations, learn a good behavioral cloning cloning policy, then fine tune it with RL in a Walt model in really diverse scenarios is, like, yeah, the most promising approach to get a general robot.

Speaker 2:
Can you say a bit more about what kind of settings Dreamer four is most suited for? Like, what are the properties of the settings?

Speaker 1:
So you definitely need good coverage. So there's a good chance that you will make you'll have to make a conscious effort to collect data, right, whether it's robotics or some medical decision making problem. Maybe you you know, I guess I don't know when it comes to, let's say, prescribing treatments. I don't know how diverse the coverage is of those datasets. I imagine, of course, there are a lot of treatments that have never been prescribed for a certain condition because, you know, doctors just know that that would be a bad idea, and so they've never done it.

Speaker 1:
And so that's not in the dataset. And and so the more coverage you have in your offline data, the more you can rely on reinforcement learning in Imagination and the less you need to rely on behavioral cloning. So your KL regularizer to the behavioral cloning policy can be turned down the better your model is and and the more coverage in your offline dataset you have. So, yeah, if you have not very good coverage, you can you know, we've seen in various examples, you can still squeeze out, like, maybe 10% improvement, but maybe not a 100% improvement.

Speaker 2:
If you have a perfect wealth model, you can

Speaker 1:
get, you know, infinite improvement. You can find the optimal policy without any human priors.

Speaker 2:
So I understand this version of Dreamer, Dreamer four, like the early ones, is based on your theoretical framework action and perception as divergence minimization that we saw at NeurIPS DeepRel workshop in 2020. And we talked about this AAPD framework a bit last time, but it it's just so it seems so timeless and and kind of deep, so I'm hoping we could touch on it again. For our listeners who didn't catch it, definitely check out the previous episode, episode 42 with more details. But on a high level, how do you explain what the APD really is?

Speaker 1:
That was maybe midway into my PhD, And I have been working on this for a while on the side up until that point already because I wanted to answer the question of what objective functions are there for an agent to optimize. You know, it seems like a lot of progress in the field comes from finding the right objectives. There are, you know, a lot of objectives to choose from, especially when it comes from when it comes to just learning from observation, so from fixed datasets, like next token prediction and, you know, energy based objectives, diffusion models, yeah, all kinds of ways to predict something. You could have supervised learning with annotated outputs and so on. But that never really felt satisfying because I wanted to know what is the space of all the possible objectives so we don't have to just search around blindly and hope that we find a new objective that works a bit better.

Speaker 1:
We can actually, you know, tell how far we are along the way. And and then, also, the whole picture gets a little more complicated when you have an agent that can interact with the world, and that opens the door for all kinds of new objectives that aren't as well understood. And so those would be things like, you know, intrinsic motivation, for example. The project or, you know, there's mathematical derivations that people can find in the paper and on in the video on my website. But at a high level, it turns out there are sort of two types of objective functions you can optimize as a learning system.

Speaker 1:
And one is sort of the static type of objective, something that's inherently, you know, just preferences that are domain specific. And so that could be something like a reward in reinforcement learning. I care about this sort of outcome more than this other outcome, but there's nothing mathematically profound about that. It's just all the stuff that we can't really express very well mathematically because they're just, like, sort of pretty subjective. And so that's rewards, but also things like inductive biases in your architecture, or, like, a regularizer term in your model.

Speaker 1:
Let's say you have a variational autoencoder, and there's a KL bottleneck. And so you have this KL regularizer that encourages the model to learn representations that are, shaped in a certain way, like, follow roughly a Gaussian distribution. So those are all inductive biases, subjective preferences, rewards. That's the one category. It's very hard to, like, I guess, make sense of them in a formal way because they're so inherently tied to, like, the the environment you're actually operating in.

Speaker 1:
On the other hand, there are more adaptive types of objectives. And so those are the objectives that enable learning in the first place, but they also enable additional drives when it comes to agents. And so those are objectives like predicting all your data, you know, predicting part of your data or even predicting all your data. And so these terms all they all maximize some sort of bound on information, so they help the learning system extract more knowledge in one way or another. And so, you know, you could predict, let's say, actions from video, and you'd extract a little bit of information.

Speaker 1:
But you extract a lot more information if you do the general thing, which is predict everything. You have a dataset of trajectories. Just model the whole trajectories with a diffusion model or a next token prediction or anything like that. Right? That way, you will extract the most knowledge out of the data you have.

Speaker 1:
And so that is basically what a world model does. Right? You're predicting dynamics. In a way, you're learning way more than maybe necessary for a certain task, but learning so much sets you up really well because it gives you understanding of the world and the ability to very quickly adapt to a new task that you weren't really prepared for. You're way more prepared now because you already understand the interactions of objects and so on.

Speaker 1:
You've extracted as much knowledge as you could out of the data you have.

Speaker 2:
This this relates to Yan Lakun's cake. Right? He's been talking about the cake for a long time.

Speaker 1:
Yes. That's just unsupervised learning. So, yeah, the adaptive objectives are unsupervised, and then there are the, like, supervised static ones. But it goes a little beyond that because, I guess, in Yan's cake, the unsupervised objectives are used for learning from fixed data and at least the way it was, you know, originally framed. I'd be curious if he has more thoughts on that today.

Speaker 1:
But, and then the AREL part, I guess, you would assume you have given you have been given some reward function. So that is also, sort of, like, a supervised signal, but you can't just predict the targets directly. You don't have targets. You only have rewards to maximize. So you need to use RL for that.

Speaker 1:
But there's actually a whole class of additional unsupervised objective functions that agents can optimize with respect to their actions, not just with respect to their parameters. So not just something they can learn from the past, but also there are unsupervised objectives to be achieved through control. And so APT really gives you an exhaustive perspective on what the space of these objective functions is. And if you try to roughly, like, cluster them, you for for agent objectives besides learning from past data, in the future, you have learning from rewards, which is just standard reinforcement learning. And then in terms of future unsupervised objectives, you have things like exploration and learning to control the environment, learning to achieve certain states, which could be, like, a goal reaching policy or some, I guess, latent skill learning algorithm, something like that.

Speaker 1:
And so if you think about it, learning from the past through unsupervised learning, you're extracting information. You're maximizing the information between the past data and your model parameters. And when you're trying to explore, then you're maximizing the expected information between your parameters and the future data. You know, I'm trying to get data that will tell me as much about the optimal parameters as possible. So you're also maximizing information or more precisely expected information because the future data has not been achieved yet, and you can optimize that with respect to actions.

Speaker 1:
You know, go to parts of the world where you'll find something interesting that'll tell you a lot about the parameters that best describe the world you're in. And then for the control, empowerment, goal reaching category, it's about injecting information into the world. So maximize the mutual information between your actions and your future data. And so, you know, that means you should try to reach a lot of different states, visit a lot of different states in the world, but the states you visit, they should all be determined pretty well based on the actions you chose. So, you know, I the agent tries to be purposeful in reaching different parts of the world and learning how to bring the world into different states.

Speaker 1:
And so that's maximizing the mutual information between its actions and its future inputs conditioned on the past, and it's, you know, known as empowerment, although there's slightly, like, multiple definitions for that, but one of them would be that, goal reaching and so on. And yeah. So those are additional drives for unsupervised agents that I think in the really long term on the road map towards AGI, we can get a lot of useful learning signal out of that. You know, of course, you you know, I think we're not quite there yet in terms of the ordering of when it makes sense to, like, really build those things at scale. But, yeah, of course, you know, the trajectory has always been start with handcrafted things.

Speaker 1:
And then supervised learning doesn't need a lot of model capacity because it doesn't learn that much, but can get the job done. Just doesn't generalize as well. And so then unsupervised learning comes after that. You need more compute. You need a bigger model, but you get a much better result and a much more general system.

Speaker 1:
And I think people talk a lot about that for the evolution of, just like prediction tasks. Maybe in computer vision, people used to hard code the, conf features, and then they started learning them through supervised learning. And then, eventually, they started just learning them through unsupervised objectives, get way better models. But my point is that the same logic applies to agent objectives as well, where, you know, the first phase is to just train models on the data you have and then just use their predictions and have a human turn that into an action in the world somehow, you know, just how you would talk to ChatGPT, and then use the the answers you get to make decisions in your life. But then the next step would be through narrow signals like rewards to train the system with reinforcement learning.

Speaker 1:
And that has already begun with RLHF and, you know, browser agents and so on. And then past that, we'll get to a point where we will actually get way better edge agents if we train them to autonomously explore and autonomously learn how to change things about the world and follow their own goals. And so then we can afterwards fine tune them with a specific reward just how you would fine tune, like, a pretrained dino representation with a classifier loss.

Speaker 2:
Okay. So you're saying if I understand what you're saying, this framework can be pushed a lot further past the current tech and and bear fruit down the road. Is is the is the framework is it done? Is it, like, a complete thing, or is it a work in progress?

Speaker 1:
Yeah. The framework is done from a mathematical perspective, and it shows us that those are exactly the categories of objectives that I've mentioned. It's not done in terms of the practical realization of these systems. Mhmm. It's a it's a mathematical framework.

Speaker 1:
It doesn't tell you all the practical details to actually implement these systems. You know, when I talk about expected information between parameters and future inputs, like, yes, that's the right objective for seeking out informative data at an abstract level, but then, you know, that's an intractable equation in general. So you have to then find an algorithm to actually implement that and and approximate that, and there are better approximations and worse approximations and details to be figured out and hyperparameters to be tuned and so on. We actually tried out small versions of this. For exploration, there's a paper called plan to explore.

Speaker 1:
And then for the empowerment aspect, there's a paper called latent skill planning and also the director paper that combines exploration and goal reaching and also temporal abstraction together. So there are small instances of that in simulated environments where this stuff is all working. But, yeah, just in terms of the timeline of, you know, affecting the affecting the world in terms of real frontier models, it's a bit too early for some of those things. And I actually think people have abandoned a lot of old ideas in the field, and I think I think they most of them will actually play a role unless there's a good reason for why something is a bad idea, even though people maybe thought it was a good idea. I think a lot of them will become relevant, but they were just way too early in the in terms of the efficient timeline or the efficient ordering for implementing those things.

Speaker 1:
So I think that's true for, like, exploration. And, yeah, I guess, there's, like, you know, things that came before the transformer, like neural cheering machines and associative memories and so on. I think a lot of the stuff will probably have, an important role to play at some point.

Speaker 2:
I understand there's a close connection here to active inference, and you have as one of your coauthors, Carl Furstin, who is a major name in that area, and also free energy. Can you talk about the what is what is different here from active inference, or what's what's this what's the gap?

Speaker 1:
Yeah. So I started working on this during my master's. That was co advised by Carl, and he's a very smart guy. I learned a lot in terms of sort of nonobvious intuitions from him. And, yeah, I think he's, like has a bit of this reputation of, you know, a lot of the stuff is hard to understand, and it's true.

Speaker 1:
And it took me a really long time to understand too and to simplify things in a way that really made sense to me. Yeah. It is sort of a different perspective on his free energy principle, and maybe it developed a little bit further to connect with things like empowerment that weren't included in the original free energy principle. The ideas are you know, the inspiration is, like, clearly Carl's work, but I try to derive it in sort of the simplest possible way without talking about, you know, stochastic differential equations and and so on just from a probability perspective. And the so the APD durations start from and start from, like, pretty simple assumptions of your agent has some distribution over random variables that describe, you know, the inputs to the agent.

Speaker 1:
So your past and future sensory inputs, that's like a sequence x one to capital t, which is, like, the lifetime trajectory of sensory inputs. And then there's the trajectory of actions and the, you know, parameters of the agent and maybe trajectory of random variables inside the agent if there are any. And then the assumption that the system is efficient and trying to reach some sort of target distribution over those same variables. Right? And then you can choose a divergence measure to bring those two distributions closer.

Speaker 1:
And if you choose KL, you get all these Shannon information terms, plus all the inductive bias terms. And, yeah. So it's like yeah. I think free energy principle is, like, a big rabbit hole, and for people interested in it, can be quite rewarding and maybe a little frustrating along the way if things are hard to understand. But there are a lot of cool intuitions to draw from there that are relevant for AI.

Speaker 2:
I I do think you're you're unique in the sense that, you know, you're doing this incredibly deep engineering work to make these things actually work in the real world at scale. And then also you're doing this theoretical stuff on the other side. And and I don't know, maybe if that's that's the reason, but you seem to be getting some incredible results consistently. I was joking, you know, with the robotics group here at UBC that's you know, sometimes I I feel like maybe Dan and Jar's already solved the core problems of of robotics overall, and you're just slowly letting us know over the years.

Speaker 1:
Thank you. Thank you. Appreciate it. I yeah. I guess I feel like a lot of the yeah.

Speaker 1:
I mean, doing all this theoretical work has helped sort of frame the right direction and know what or have more certainty in what I think is important to work on. And I think besides that, maybe I would encourage people to work more on things they believe in in the long term because the timelines are actually, like, getting faster and faster. And, you know, if you work for a couple years on something, you can make really significant progress. And, of course, that means you'll have to say no to a lot of, like, shorter term projects. But I think that's, like, the most rewarding thing you can do for yourself and probably the most the way in which you can contribute the most to the world too.

Speaker 2:
It's always so fascinating talking with you. I always learned so much. Today was no exception. Thank you, Danijar Hafner.

Speaker 1:
Great chatting. Thanks for having me on.

### Creators and Guests

[Host](https://www.talkrl.com/people/robin-ranjit-singh-chauhan)
  

[Robin Ranjit Singh Chauhan](https://www.talkrl.com/people/robin-ranjit-singh-chauhan)

## Listen Anywhere

[More Options »](https://www.talkrl.com/subscribe)