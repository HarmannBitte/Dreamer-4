<!-- source: https://www.emergentmind.com/papers/2509.24527
     fetched: 2026-09-20T13:37:16Z -->

# Training Agents Inside of Scalable World Models

**Abstract:** World models learn general knowledge from videos and simulate experience for training behaviors in imagination, offering a path towards intelligent agents. However, previous world models have been unable to accurately predict object interactions in complex environments. We introduce Dreamer 4, a scalable agent that learns to solve control tasks by reinforcement learning inside of a fast and accurate world model. In the complex video game Minecraft, the world model accurately predicts object interactions and game mechanics, outperforming previous world models by a large margin. The world model achieves real-time interactive inference on a single GPU through a shortcut forcing objective and an efficient transformer architecture. Moreover, the world model learns general action conditioning from only a small amount of data, allowing it to extract the majority of its knowledge from diverse unlabeled videos. We propose the challenge of obtaining diamonds in Minecraft from only offline data, aligning with practical applications such as robotics where learning from environment interaction can be unsafe and slow. This task requires choosing sequences of over 20,000 mouse and keyboard actions from raw pixels. By learning behaviors in imagination, Dreamer 4 is the first agent to obtain diamonds in Minecraft purely from offline data, without environment interaction. Our work provides a scalable recipe for imagination training, marking a step towards intelligent agents.

### Paper Prompts

Sign up for free to create and run prompts on this paper.

#### Top Community Prompts

### Explain it Like I'm 14

## Overview

This paper introduces Dreamer 4, an AI “agent” that learns to act by practicing inside its own mental simulation of the world, called a world model. Instead of constantly trying things in the real environment (which can be slow, expensive, or unsafe), Dreamer 4 watches lots of videos, learns how the world tends to work, and then trains its behavior by imagining the future accurately and quickly. The team shows this works in a very hard game, Minecraft: Dreamer 4 is the first agent to obtain diamonds using only offline data (recorded videos and actions), without playing the game during training.

## Goals of the paper

The researchers set out to answer simple but important questions:

- Can an AI learn to solve complex, long-term tasks purely by practicing in its own imagination, without new environment interaction?
- Can a world model predict detailed object interactions and game rules well enough to be truly useful for training agents?
- How can we make such a world model both accurate and fast enough to run in real time on a single GPU?
- How much action data (mouse/keyboard logs) do we need? Can the model learn most of its knowledge from unlabeled videos?
- Which parts of the design matter most for performance?

## How Dreamer 4 works

Think of Dreamer 4 as a student with a powerful “imagination” who watches videos to learn how the world behaves, then practices inside that imagination to get good at tasks.

### World model in plain words

- The world model is like a very smart video player that can predict what will happen next if you press certain buttons (actions).
- It doesn’t just replay past videos; it simulates what would happen under new actions. For Minecraft, that means predicting how blocks break, how tools work, what crafting does, and more.
- To do this, the model turns each video frame into a compact code (like a summary). Then it learns how these codes change when different actions are taken.

Key pieces explained simply:

- Tokenizer: Compresses each frame into a shorter, meaningful representation, so the model can think faster.
- Dynamics model: Predicts the next representations given the current ones and the chosen actions—this is the engine of imagination.

### Three training phases

The training happens in three steps:

1. Pretrain the world model:
  - Watch lots of videos (with or without actions).
  - Learn to predict how the world looks and changes over time.
2. Add task-specific heads:
  - Insert small “heads” that output a policy (what actions to take) and a reward/value estimate (how good things are).
  - Use behavior cloning: learn from recorded human actions for each task.
3. Imagination training:
  - Now the agent practices inside its world model only.
  - It imagines many futures, scores them using the reward head, and improves the policy to choose better actions next time—all without touching the real game.

### Making it fast and accurate

Two big ideas keep the world model both sharp and speedy:

- Shortcut forcing: Usually, models generate future frames step by tiny step. Shortcut forcing trains the model to take bigger, smarter steps without losing accuracy—like skipping ahead in a video but still landing at the right place. This means it can generate high-quality predictions in just a few steps per frame, enabling real-time use.
- Efficient transformer design: Transformers are great at understanding sequences (like videos), but standard ones can be slow. The authors carefully arrange attention across space and time and use memory-saving tricks so the model runs at or above 20 frames per second on a single GPU in Minecraft. It also “remembers” about 9.6 seconds of context—much more than earlier models.

### Learning from unlabeled videos plus a few actions

- Most internet videos don’t include the exact actions the player took. Dreamer 4 can still learn a lot from those unlabeled videos: the look of the world, how things move, and general physics.
- Then it only needs a relatively small amount of action-labeled data to “ground” its understanding—so it knows which actions lead to which outcomes.
- The paper shows that with only about 100 hours of paired actions (out of 2,500+ hours of total video), the model already learns strong action conditioning.

## What they found

Here are the main results and why they matter:

- First offline diamonds in Minecraft:
  - Dreamer 4 is the first agent to obtain diamonds using only offline data—no new game interaction during training.
  - It beats a well-known baseline (OpenAI’s VPT) while using about 100 times less labeled data.
  - It also outperforms a strong vision-language baseline (VLA with Gemma 3) on key milestones like crafting an iron pickaxe.
- Accurate, real-time simulation of complex interactions:
  - Humans can “play inside” Dreamer 4’s world model in real time, using mouse and keyboard.
  - It correctly simulates tricky Minecraft mechanics: placing and breaking blocks, using tools, riding boats, entering portals, and interacting with crafting tables.
  - It has a much longer memory window (about 9.6 seconds) than earlier models, which helps keep its predictions consistent over time.
- Learns from mostly unlabeled videos:
  - With only a small slice of action-labeled data, Dreamer 4 learns strong action grounding.
  - The action understanding generalizes beyond where it was trained (for example, to different dimensions in Minecraft seen only in unlabeled videos).
- Scalable and fast:
  - The world model reaches real-time speeds on a single GPU and still keeps high accuracy.
  - This is crucial for imagination training and for interactive use.

## Why it matters

- Safer and cheaper training: For robots or other real-world systems, letting an unfinished agent practice in the real world can be risky and slow. A strong world model lets agents get better entirely offline until they’re ready.
- Learn from the internet: Most videos online don’t include actions. Dreamer 4 shows a path to learn general world knowledge from those videos and then add action grounding from a small, labeled subset.
- Better long-horizon skills: Tasks like getting diamonds in Minecraft require thousands of correct decisions in a row. Dreamer 4’s accurate long-horizon imagination helps it plan and learn strategies that go far beyond simple one-step predictions.
- Towards general intelligent agents: This is a practical recipe for training agents inside their own simulations. As world models get broader and better, agents may learn powerful, transferable skills across games, robots, and real-world tasks—using mostly videos and a little action data.

In short, Dreamer 4 shows that teaching an agent to think ahead inside a fast, accurate world model can unlock complex, long tasks using far less direct interaction and supervision than before.

### Knowledge Gaps

## Unresolved gaps, limitations, and open questions

Below is a single, concrete list of what remains missing, uncertain, or unexplored in the paper, structured so future work can act on it.

- Long-horizon consistency: Despite a 9.6s temporal context, the model’s rollouts still drift over longer horizons; mechanisms to maintain causal and visual consistency beyond minutes-long tasks (e.g., inventory management across minutes) are not provided or evaluated.
- UI/state fidelity limits: The paper notes inventory UI elements can be unclear or change over time; there is no quantitative analysis or targeted method to stabilize persistent UI/object states over long sequences.
- Low end-to-end task success: Diamond acquisition reaches 0.7% success in 60-minute episodes; the paper does not identify the main bottlenecks (planning, exploration, credit assignment, or model errors) nor provide failure-mode breakdowns guiding targeted improvements.
- Model exploitation and reward hacking: The policy is optimized entirely in-model with a learned reward head; there is no systematic study of model exploitation, reward hacking, or safeguards (e.g., uncertainty penalties, consistency checks with off-model data).
- Uncertainty estimation: The world model provides point predictions; there is no treatment of epistemic uncertainty or risk-aware policy optimization to avoid confidently wrong model rollouts.
- Freezing vs. finetuning the world model: Imagination training freezes the transformer; the trade-offs of joint policy–model finetuning (overfitting vs. improved on-policy fidelity) are not explored at scale or with safeguards.
- OOD action generalization: The paper begins but does not complete a rigorous, quantitative evaluation of action conditioning generalization to held-out dimensions (Nether/End); metrics, protocols, and results remain incomplete in the provided content.
- Semantic evaluation metrics: Action-conditioned video accuracy is reported via PSNR/SSIM, which do not capture semantic task correctness; there is no standardized, action-aware metric suite (e.g., success at scripted subgoals, object-state deltas, causal consistency checks).
- Robustness to action sparsity: While 100 hours of actions yield strong conditioning, the limits under more extreme sparsity, imbalance (rare actions), or noisy/misaligned action labels are not characterized.
- Inference-time noise scheduling: The approach fixes K=4 steps and a small context noise; sensitivity to K, adaptive step sizing, or noise schedules under varying domains and horizons is not explored.
- Shortcut forcing theory: The shortcut forcing objective with x-prediction and ramp weighting is empirically motivated; formal analysis of stability, error accumulation bounds, and equivalence to multi-step integration schemes is absent.
- Architectural trade-offs: The claim that few temporal-attention layers suffice is not stress-tested for very long contexts or more stochastic domains; the quality–speed trade-off vs. denser temporal attention remains underexplored.
- Memory beyond context window: No external memory, retrieval, or hierarchical temporal abstractions are used; methods to persist and recall states (e.g., inventory over tens of minutes) are not investigated.
- Representation bottleneck design: The continuous latent bottleneck (tanh projection) is used without comparison to discrete/tokenized latents (e.g., VQ) in terms of counterfactual accuracy, compression rate, or long-horizon stability.
- Data scaling laws: There is no scaling study of performance vs. model size, dataset size/diversity, context length, or spatial resolution—making it hard to predict returns on additional compute/data.
- Compute accessibility: Training requires 256–1024 TPU-v5p; the minimal compute/data regime to retain key capabilities (e.g., action-conditioned fidelity, diamond success) is not established.
- Cross-domain generality: Results beyond Minecraft are qualitative (robotics video generations); there is no quantitative cross-domain validation (robotics control success, manipulation benchmarks, sim2real transfer).
- Language grounding: Tasks are encoded as one-hot embeddings; instruction following with natural language, compositional task generalization, and the effects of language pretraining are not studied.
- Action space design: Mouse control is discretized via foveated bins; there is no ablation on alternative parameterizations (continuous, mixture models) and their impact on precision tasks and long-horizon success.
- Policy optimization objective: PMPO is adopted without comparison to advantage-weighted or KL-regularized variants under the same in-model setting; the sensitivity to α/β and the prior direction (reverse vs. forward KL) lacks systematic study.
- Offline-to-online bridge: While offline-only training is emphasized, strategies for safe, low-regret online finetuning (e.g., DAgger-like corrections, risk-aware exploration under model uncertainty) are not explored.
- Counterfactual validity at scale: Human-in-the-loop tests show strong qualitative interactions, but there is no large-scale, action-perturbation benchmark quantifying counterfactual correctness across varied tasks and horizons.
- Reward modeling limits: The reward head is trained from event annotations; generalization to tasks without event labels, preference-based rewards, or latent goal inference is not addressed.
- Start-frame generation: Training uses 30% images for start frames; there is no ablation on how this choice affects open-loop rollouts, policy robustness from arbitrary initial states, or data efficiency.
- Safety and deployment: For robotics applications, the paper does not examine safety guarantees, failure detection, or bounded-error assurances during real-world deployment informed by the learned world model.
- Higher resolution and multi-view: Applicability to higher resolutions, multi-camera setups, or 3D-aware representations (e.g., NeRF-like factors) is not evaluated; how these affect interaction fidelity is unclear.
- Multi-agent and social dynamics: The framework’s ability to model/plan in environments with other agents (cooperative/adversarial) remains unexplored.
- Data curation and bias: The impact of dataset biases (player styles, world seeds, UI mods) on learned dynamics, policy behavior, and generalization is not analyzed.
- Benchmark standardization: A shared, open benchmark for action-conditioned world models (with protocols for human interaction, counterfactual tests, and long-horizon tasks) is not proposed, limiting comparability across methods.

### Practical Applications

## Immediate Applications

The following applications can be deployed with current capabilities, leveraging Dreamer 4’s real-time world model, imagination training, and data-efficient action conditioning.

- Offline robot policy development and evaluation (Robotics)
  - Use Dreamer 4’s imagination training to develop and finetune manipulation and navigation policies purely from fixed teleoperation datasets, avoiding risky online RL. Integrate with ROS to prototype, evaluate, and iterate on policies in a high-fidelity, counterfactual simulator.
  - Tools/workflows: world-model pretraining on unlabeled lab videos, small action-labeled subset for grounding, reward model training on task events, PMPO-based offline RL, single-GPU inference for operator-in-the-loop tests.
  - Assumptions/dependencies: sufficient coverage in offline datasets; robust action-space mapping from mouse/keyboard-like controls or robot affordances; reward model accuracy; sim-to-real gap remains and needs validation; 9.6s context limits long-horizon planning.
- Human-in-the-loop “what-if” teleoperation sandboxes (Robotics, HCI)
  - Let operators practice counterfactual interventions inside a real-time world model (e.g., rehearsing grasps, tool use, or sequences like flipping bowls and moving towels). Useful for training and incident reviews without touching the physical system.
  - Tools/workflows: interactive UI binding mouse/keyboard to the dynamics model; session recording; scenario prompts via task tokens; policy snapshots.
  - Assumptions/dependencies: interactive fidelity under domain shifts; task annotation pipeline; safe translation of learned strategies to real systems.
- Game QA automation and agent prototyping (Gaming/software)
  - Train agents to complete complex, multi-step objectives (e.g., crafting ladders, iron tools, diamonds) from existing player video logs. Automate regression tests for progression, mechanics, UI flows, and balance while keeping evaluations offline.
  - Tools/workflows: ingest playtest datasets; task-conditioned policies via one-hot task tokens; imagination rollouts for stress tests; success-rate dashboards.
  - Assumptions/dependencies: availability of representative gameplay datasets; alignment between offline world model and live game builds; UI/event label quality.
- Data-efficient simulators from unlabeled video with minimal actions (Autonomous vehicles, Robotics)
  - Pretrain world models on large unlabeled video corpora and ground action-conditioning with ~10–100 hours of action data to reach usable predictive fidelity for control. Immediately applicable to internal driving or robot datasets where controls are partially labeled.
  - Tools/workflows: action-grounding modules; shortcut forcing + diffusion forcing training; metric tracking (PSNR/SSIM) for action-conditioned rollouts.
  - Assumptions/dependencies: action-space consistency across video sources; scene distribution breadth; mechanical dynamics that the model can capture; legal rights to use video.
- Promptable, multi-task agents in constrained domains (Gaming, Robotics)
  - Deploy task-conditioned policies to perform structured sequences (e.g., “collect wood → craft sticks → craft tools → mine iron”) using task tokens for steerability, and PMPO to balance positive/negative feedback.
  - Tools/workflows: task schema definitions; sparse event-to-reward pipelines; multi-token prediction heads for actions/rewards; curriculum prompts.
  - Assumptions/dependencies: reliable event logging; careful prevention of causal confusion (agent tokens cannot influence future predictions directly); stable reward scales.
- Real-time UX/interaction prototyping with video world models (HCI/software)
  - Designers can rehearse interaction flows (menu navigation, crafting UIs, inventory manipulation) in a controllable simulator, diagnosing friction points and testing alternative sequences before instrumenting live builds.
  - Tools/workflows: model-bound interaction toolkit; session scripts; counterfactual branching; playback export for design review.
  - Assumptions/dependencies: sufficiently labeled interaction events; mapping from design-specific inputs to model action space; temporal context adequate for target flows.
- ML acceleration via efficient transformer components (Software/ML infrastructure)
  - Adopt Dreamer 4’s architectural practices—axial attention (space/time factorization), reduced temporal attention frequency, GQA, QKNorm, attention logit soft-capping—to speed inference and stabilize training in existing sequence/video models.
  - Tools/workflows: drop-in transformer blocks; KV-cache memory optimization; inference benchmarking; RMS loss normalization utilities.
  - Assumptions/dependencies: compatibility with target model codebases; careful tuning of layer ratios; hardware support for grouped queries and caching.
- Reproducible offline RL benchmarks for long-horizon tasks (Academia)
  - Use the “offline diamond challenge” blueprint to build domain-specific, long-horizon offline evaluations (e.g., multi-step robotics assembly, complex UI tasks) without environment interaction.
  - Tools/workflows: curated datasets with action/events; evaluation harness; success metrics over hour-long episodes; baseline agents (BC, VLA, WM+BC, imagination RL).
  - Assumptions/dependencies: access to domain datasets; compute for pretraining; consistent protocols to compare across labs; standardized task ladders.
- Organizational safety protocols favoring offline imagination training (Policy/enterprise governance)
  - Institute policy that hazardous platforms (robots, industrial systems) prefer offline RL with world models and staged validation, reducing on-floor experimentation risks and interruptions.
  - Tools/workflows: internal governance templates; risk assessments; staged deployment checklists; sandbox-only training phases.
  - Assumptions/dependencies: documented model fidelity; escalation procedures for sim-to-real tests; data governance for recordings.
- Esports analytics and training bots from match replays (Sports/gaming analytics)
  - Train task-conditioned agents on replay videos and limited control data to evaluate strategies, test patches, and coach players with offline scenario simulations.
  - Tools/workflows: replay ingestion; task prompts (objectives/roles); imagination rollouts for alternative lines; success/efficiency metrics.
  - Assumptions/dependencies: mapping from replay formats to action tokens; variability across patches/versions; licensing of replay data.

## Long-Term Applications

These applications require further research and scaling in areas such as action grounding across domains, longer temporal coherence, safety, regulatory approvals, and robust sim-to-real transfer.

- General-purpose household robots trained largely from web videos (Robotics)
  - Learn physics, affordances, and object interactions from diverse unlabeled web content, grounding actions with relatively few labeled demonstrations to achieve multi-task manipulation and navigation.
  - Dependencies: cross-domain action alignment; robust sim-to-real with contact-rich dynamics; safety certifications; long-horizon planning beyond ~10s context.
- Autonomous driving world models for planning and offline RL (Autonomous vehicles)
  - Build city-scale, data-driven simulators from fleet dashcams, then ground with limited control streams to train policies offline, test interventions, and reduce reliance on expensive on-road experimentation.
  - Dependencies: comprehensive coverage of edge cases; strong temporal consistency over minutes; rigorous validation; regulatory compliance; privacy-preserving data use.
- Factory and warehouse digital twins from CCTV (Industrial automation/energy)
  - Create operational world models from surveillance video to simulate process changes, robot workflows, and layout optimizations, enabling counterfactual planning and throughput/energy optimization.
  - Dependencies: legal/data governance; mapping of heterogeneous devices/actions; accurate reward models tied to KPIs; integration with MES/WMS systems.
- Surgical robot training and rehearsal from OR video (Healthcare/medical robotics)
  - Use action-grounded world models to practice instrument maneuvers and multi-step surgical workflows offline, with policy improvements via imagination training before any patient contact.
  - Dependencies: fine-grained action labels; rigorous clinical validation; regulatory approvals; high-fidelity modeling of soft tissue dynamics; ethics and privacy safeguards.
- Interactive STEM education labs with counterfactual physics (Education)
  - Offer students manipulable, real-time video-based simulators to explore cause-effect, engineering assembly, and experimental design—moving beyond scripted simulations to learned world behavior.
  - Dependencies: domain-specific datasets; curriculum-aligned prompts; scaling to classroom hardware; guardrails against misleading artifacts.
- Generative gameplay and NPC co-design (Gaming/creative tools)
  - Co-create quests, puzzles, and emergent behaviors by steering task-conditioned agents and testing content entirely offline in learned simulators; accelerate iteration cycles.
  - Dependencies: extended temporal coherence; IP licensing; creator tooling; robust evaluation of agent behavior and failure modes.
- Cross-application UI automation agents (Software/RPA)
  - Train agents to operate complex desktop/web applications from screen recordings, grounded by minimal interaction logs, enabling robust long-horizon RPA without brittle scripted flows.
  - Dependencies: action-space standardization for GUIs; privacy/compliance for screen data; temporal memory across multi-minute workflows; reliable reward definitions.
- Policy frameworks for web-video training data (Policy/ethics)
  - Establish standards for licensing, consent, provenance, audit trails, and opt-outs when training world models on publicly scraped videos, alongside model cards documenting risks and capabilities.
  - Dependencies: multi-stakeholder agreements; enforceable governance; tooling for dataset transparency and dynamic removal.
- Carbon-aware, energy-efficient simulation at scale (Energy/sustainability)
  - Leverage single-GPU real-time inference and shortcut forcing to reduce operational costs of simulation-heavy workflows; couple with carbon-aware schedulers for training phases.
  - Dependencies: hardware availability; lifecycle carbon accounting; standardized benchmarks comparing energy per simulated hour.
- Cross-domain world models with unified action spaces (AI research)
  - Move toward agents that can switch embodiments (robot arms, vehicles, UIs) via modular action heads and shared dynamics representations, transferring knowledge of physics and interaction across domains.
  - Dependencies: large-scale multi-domain datasets; principled action abstraction; stability in multi-modal training; evaluation protocols for transfer.

### Notes on assumptions and dependencies across applications

- Data availability and rights: Many applications hinge on access to diverse, large-scale video datasets and limited action labels; ensure licensing, privacy, and consent.
- Sim-to-real fidelity: High-quality counterfactual prediction does not guarantee safe deployment; staged validation and domain randomization remain critical.
- Temporal coherence: Current context length (~9.6s) is strong but still limits very long-horizon tasks; extending memory and reducing drift over minutes is an active need.
- Reward modeling: Offline RL quality depends on reward head correctness and task event annotations; invest in robust, scalable reward pipelines.
- Hardware and compute: Pretraining requires substantial compute; inference is efficient (single high-end GPU), but deployment plans must consider hardware constraints.
- Safety and governance: For embodied applications, adopt conservative rollout policies, audit trails, and human oversight when transferring policies from imagination to reality.

### Glossary

- **Action conditioning** : Training a world model to use actions as inputs so it can predict action-dependent future outcomes. "Moreover, the world model learns general action conditioning from only a small amount of data"
- **Attention logit soft capping** : A stability technique that limits the magnitude of attention logits during training. "We employ QKNorm and attention logit soft capping to increase training stability."
- **Autoregressive sampling** : Generating sequences by producing each element conditioned on previously generated elements. "We sample autoregressively in time"
- **Behavioral cloning** : Supervised learning that trains a policy to imitate actions from recorded demonstrations. "Behavioral cloning from scratch using multi-token prediction (MTP), without task conditioning."
- **Behavioral prior** : A frozen reference policy used to regularize and constrain updates during reinforcement learning. "We initialize a value head and a frozen copy of the policy head that serves as a behavioral prior."
- **Block-causal transformer** : A transformer that enforces causality across time while allowing full attention within each time block. "which both use the same block-causal transformer architecture."
- **Bootstrap loss** : A distillation loss in shortcut models that trains larger steps by combining the results of two smaller steps. "shortcut models are trained using a bootstrap loss that distills two smaller steps"
- **Causal attention** : Attention masking that permits attending only to past time steps to maintain temporal causality. "It uses causal attention to achieve temporal compression while allowing frames to be decoded one by one."
- **Diffusion forcing** : A sequence modeling method that assigns different noise levels per time step to train denoising across a temporal context. "For sequential data, diffusion forcing assigns a different signal level to each time step of the data sequence, producing a corrupted sequence."
- **Diffusion models** : Generative models that progressively transform noise into data via learned denoising steps. "Our world model is based on the paradigm of diffusion models"
- **Diffusion transformers** : Transformer architectures adapted to diffusion-based generation. "such as diffusion transformers\citep{peebles2023dit,diffusionforcing}."
- **Discount factor** : The scalar γ that down-weights future rewards in reinforcement learning returns. "where  is a discount factor"
- **Flow head** : A prediction head that outputs representations under a flow/diffusion objective during imagination rollout. "sampling representations  from the flow head"
- **Flow matching** : A training objective that predicts the velocity from noise to data to guide denoising steps. "We build on the flow matching formulation"
- **Foveated discretization** : A discretization scheme for mouse inputs that uses finer resolution near the focal area. "using foveated discretization \citep{vpt}"
- **FSDP sharding** : A parallel training method that shards model parameters, gradients, and optimizer states across devices. "and FSDP sharding \citep{fsdp,deepspeed}"
- **GQA (Grouped-Query Attention)** : An attention variant where multiple query heads share key-value heads to reduce memory. "Third, we apply GQA \citep{gqa} to all attention layers in the dynamics"
- **Imagination training** : Reinforcement learning entirely inside a learned world model by generating and optimizing over imagined trajectories. "Dreamer 4 learns to solve complex control tasks by imagination training inside of its world model."
- **KL divergence** : A measure of difference between two distributions used to regularize the policy toward a prior. "we use a reverse direction for the prior KL to better constrain the policy to the space of reasonable behaviors."
- **KV cache** : Cached keys and values used by attention mechanisms for efficient inference with long contexts. "the memory bandwidth needed to access the KV cache of a long context to attend into."
- **Lambda-returns** : Returns that blend bootstrapped value estimates with multi-step targets using λ to balance bias and variance. "to predict -returns computed from the predicted rewards and values along the sequence"
- **Latent tokens** : Learned tokens that carry compressed, high-level information about each frame for transformer processing. "learned latent tokens."
- **LPIPS** : A perceptual similarity metric used as a reconstruction loss to improve visual quality. "consisting of mean squared error and LPIPS loss."
- **Multi-token prediction (MTP)** : A technique that predicts multiple future tokens/actions ahead to improve temporal learning. "using multi-token prediction (MTP) of length "
- **PMPO** : A policy optimization objective that uses only the sign of advantages and balances positive/negative feedback. "the policy head learns using PMPO"
- **PSNR** : Peak Signal-to-Noise Ratio, a metric for generation fidelity relative to ground truth. "With only 10 hours of actions, Dreamer 4 achieves 53\% PSNR"
- **QKNorm** : A normalization method for query and key vectors to stabilize attention training. "We employ QKNorm and attention logit soft capping to increase training stability."
- **Register tokens** : Learned tokens (inspired by ViT register) that provide persistent state across layers. "and concatenated with  learned register tokens \citep{vitregister} and a single token for the shortcut signal level and step size."
- **RMSNorm** : Root Mean Square normalization applied pre-layer for stable transformer training. "We start from a standard transformer with pre-layer RMSNorm \citep{rmsnorm}"
- **RoPE** : Rotary Positional Embeddings that encode relative positions for attention. "RoPE \citep{rope}"
- **Shortcut forcing** : An objective combining diffusion forcing with shortcut models to predict clean representations efficiently in few steps. "We leverage a novel shortcut forcing objective"
- **Shortcut models** : Models that condition on step size to enable larger denoising jumps and fewer sampling steps. "Shortcut models condition the neural network not only on the signal level  but also on the requested step size ."
- **Signal level** : The scalar that mixes data with noise in diffusion training/inference. "The signal level is typically sampled from a uniform distribution or a logit-normal distribution"
- **SSIM** : Structural Similarity Index Measure, a perceptual metric for image/video generation quality. "85\% PSNR and 100\% SSIM."
- **SwiGLU** : A gated activation function variant used in transformers to improve performance. "SwiGLU \citep{swiglu}"
- **Symexp twohot** : An output parameterization that uses symmetric exponential scaling with a two-hot discretization for robust reward/value learning. "the reward head is parameterized as a symexp twohot output"
- **TD-learning** : Temporal Difference learning, a method that bootstraps value estimates from future predictions. "We train the value head using temporal difference learning (TD-learning)"
- **V-prediction** : Predicting the velocity from noisy input to clean data in diffusion models. "Shortcut models parameterize the network to predict velocities , called v-prediction"
- **X-prediction** : Predicting the clean data representation directly rather than velocity in diffusion models. "Instead, we found that parameterizing the network to predict clean representations, called x-prediction"