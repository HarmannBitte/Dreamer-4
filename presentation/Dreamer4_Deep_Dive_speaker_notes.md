# Dreamer 4 deep dive — speaker notes

## Slide 1: PAPER DEEP DIVE

Welcome. This is a deep dive into Dreamer 4, the September 2025 DeepMind paper by Danijar Hafner, Wilson Yan and Tim Lillicrap. Headline: an agent that learns to obtain diamonds in Minecraft purely from offline video, by training inside a learned world model that runs in real time on a single GPU. Background image: a frame of the official teaser video from the project page.

## Slide 2: Agenda

Four parts plus an appendix. For a mixed audience I'll spend most time on the method intuition and on what the experiments do and do not show.

## Slide 3: Dreamer 4 in one slide

If you remember one slide, it's this one. Five claims, each tied to a table or figure. Note the honesty in the numbers: diamonds are rare (0.7 %), but every earlier milestone is reached far more reliably and faster than by the baselines, all without a single environment step.

## Slide 4: Background & motivation



## Slide 5: Why world models? Learning in imagination

The core idea has been constant since the first Dreamer in 2019: learn a model of the environment, then train the policy on imagined trajectories. What changed in Dreamer 4 is the simulator: a 2-billion-parameter block-causal transformer trained with a diffusion-style objective, accurate enough that a human can play inside it. The frame on the right is an imagined rollout, not the real game.

## Slide 6: What made scalable world models hard before

Three tensions: fidelity versus speed versus stability over long horizons. Prior Minecraft world models chose speed and looked plausible, but a human trying to craft a pickaxe inside them fails. The recurrent Dreamer 3 model was fast but low-resolution and relied on privileged state. Dreamer 4 tries to get all three at once.

## Slide 7: The test bed: the offline diamond challenge

Offline means offline: the agent never touches Minecraft during training. The only signal is human gameplay video with logged inputs. Diamonds need a long chain of subgoals, each executed with raw mouse and keyboard at 20 Hz. That is why success rates fall off steeply along the tech tree for every method.

## Slide 8: Method



## Slide 9: Overview: three phases, one transformer

Three phases. First a world model is trained on all video. Second, agent tokens and heads are added and trained by behavioural cloning while the dynamics loss keeps running. Third, the transformer is frozen and only the policy and value heads are trained by RL on imagined rollouts. Keeping the dynamics loss on uniform data rather than task-relevant data is a small but deliberate choice to avoid a world model that is optimistic about task success.

## Slide 10: World-model design

Both halves use the same transformer block. Block-causal means every token in frame t can see all tokens of frames up to t, which is exactly what you need for online, frame-by-frame generation with a human or a policy in the loop.

## Slide 11: The causal tokenizer

The tokenizer is a masked autoencoder over 16×16 patches with a small continuous bottleneck. Two properties matter downstream: it is causal in time, and its latent space is smooth because of the heavy masking during training. Everything after this operates on 256 latent tokens per frame instead of 960 patches.

## Slide 12: The interactive dynamics model

The dynamics model reads the interleaved sequence of actions and latents. Only every fourth layer attends across time; the rest work within one frame. That is what makes a 9.6 s context affordable. Alternating short and long batches is a training-cost trick: it cut a training step from 9.8 s to 1.5 s in the ablation (Table 2).

## Slide 13: Two-minute primer: flow matching, signal level τ, x vs v

For the non-diffusion people: think of a noise level τ from 0 (pure noise) to 1 (clean latent). The model learns to push a noisy latent toward the clean one; sampling repeats this K times. Diffusion forcing makes the noise level per frame, which is what allows causal rollouts. Shortcut models teach the network to take big steps consistently. Dreamer 4 combines the two.

## Slide 14: Shortcut forcing: the training objective

Here is the objective in words. Combining the two prior ideas gets you from 875 back to 329 FVD at 4 steps — but the big wins come from the parameterisation details: predicting x instead of v, computing the loss in x-space, and the ramp weight together take FVD from 329 to 102. These are the kind of choices you only discover with a careful cascade of ablations, which the paper provides.

## Slide 15: Why x-prediction matters for autoregressive world models

This is the most transferable lesson of the paper for anyone building autoregressive generative models: predict the clean signal, not the velocity, when your own outputs become your inputs. Open Dreamer, the open-source reproduction, independently confirmed this — they report the same instability with v-prediction at scale.

## Slide 16: Architecture choices that buy speed without losing quality

Read the bars top to bottom. The red bars are the starting point: a diffusion-forcing transformer that is either slow or bad. The grey bars are the objective changes from the previous slides; the blue bar is the final model. The architectural changes on the lower half mostly move FPS, not FVD — exactly what you want.

## Slide 17: From world model to agent: agent tokens & heads

Agent tokens are the interface between simulation and decision making. The one-directional mask is subtle but important: if latents could attend to agent tokens, the model could 'cheat' by predicting frames consistent with what the policy intends rather than with the physics of the game. Notice how much of the gain over BC comes from this phase alone — the representation matters.

## Slide 18: Imagination training with PMPO

PMPO is deliberately simple. Using only the sign of the advantage makes the update invariant to reward scale, which matters when rewards are rare item events. The KL term to the BC policy is doing two jobs: stabilising RL and preventing the policy from wandering into regions the world model gets wrong. Hafner mentioned in a talk that a few rounds of corrective online data would allow a much weaker KL — but that is not in the paper.

## Slide 19: Experiments



## Slide 20: Is the world model accurate? Let humans play inside it

This is the paper's most convincing evidence about the world model. Real people sit down with a mouse and keyboard and try to do things. Dreamer 4 is the only model in which crafting, riding a boat or entering a portal work. The caveat is on the right: this is a small, human-judged protocol; I'd like to see automated long-horizon metrics in follow-ups.

## Slide 21: What 'accurate object interactions' looks like

Three of the sixteen tasks. In the boat task Lucid shows only blue; in the portal task the baselines never enter; in the crafting task Dreamer 4 opens a functional crafting menu. The clips themselves are in the resource archive if you want to play them during the talk.

## Slide 22: Offline diamond challenge: results

The official results figure. Every method nails the first items; the interesting region is the right half. Dreamer 4 roughly doubles or triples the VLA on iron-age items and is the only one reaching diamonds — rarely, but from zero interaction. Remember this is a 60-minute budget per episode; humans need about 20 minutes on average.

## Slide 23: Where do the gains come from? Agent ablations and speed

Two separable effects. First, using the world model as the representation for imitation already gives a large jump — that's a statement about video pretraining. Second, RL inside the model adds a further, smaller but consistent gain on the hardest items and makes the agent faster, which is a hallmark of RL over imitation.

## Slide 24: Unlabeled video: how many action labels are needed?

This experiment is easy to overlook but strategically important. Only about a hundred hours of labeled actions are needed on top of thousands of unlabeled hours, and the learned action semantics transfer to visual domains that were never labeled. That is the argument for scaling to internet video later.

## Slide 25: Inside the imagination: decoded training rollouts

Figure 1 from the paper. All of these frames are generated by the model while the policy is being trained. Worth stressing to a mixed audience: the agent learns in latent space; decoding is purely for visualisation.

## Slide 26: Beyond Minecraft: robotics & egocentric video (qualitative)

The paper positions Dreamer 4 as a step toward robotics. The evidence here is qualitative: plausible counterfactual generations on real robot and kitchen video. Hafner left DeepMind shortly after the paper to work on humanoid robotics, which tells you where the authors think this goes.

## Slide 27: Dreamer 3 vs Dreamer 4

Same family, different regime. Dreamer 3 solved diamonds with online interaction and privileged state at 64×64; Dreamer 4 does it offline from raw pixels and inputs. The price is speed: the transformer is still about forty times slower than the recurrent model, according to Hafner.

## Slide 28: Data, compute and scale

Scale context. The Minecraft data is the public VPT contractor set, which makes the comparison with VPT clean: Dreamer 4 uses about a hundred times less data and no interaction. Compute is disclosed only as a TPU range. Nothing was open-sourced, which shaped the follow-up ecosystem.

## Slide 29: Discussion



## Slide 30: Limitations the paper itself states

The authors are quite candid. The two that matter most for the agenda of the paper are memory and exploitability: both limit how far imagination training can be pushed before the policy learns things that are only true inside the model.

## Slide 31: A critical reading: established vs. open

Balance sheet. The methodological contribution — how to make a fast, accurate autoregressive video world model — is robust and has been independently reproduced. The headline agent result is real but statistically thin and has not been reproduced outside DeepMind. For a reading group, this split is where the discussion usually starts.

## Slide 32: Where the authors want to take it

Six directions, three of which — memory, corrective data, and language — directly address the limitations we just discussed. Note that the authors' next steps are toward physical robots, not more Minecraft.

## Slide 33: Key takeaways

Six takeaways, ordered from result to method to caveats.

## Slide 34: Questions for discussion

Pick two or three depending on the room.

## Slide 35: References & resources

All sources, plus the GitHub archive that contains local copies of every item used to build this deck.

## Slide 36: Appendix A — Configuration & hyper-parameters

Reference slide; not meant to be presented in full.

## Slide 37: Appendix B — Full design cascade (Table 2)

Numbers transcribed from Table 2 and read off Figure 8.

## Slide 38: Appendix C — Full success-rate table (Table 7, %)

Full table for reference.

## Slide 39: Appendix D — Glossary

Glossary for the mixed audience.
