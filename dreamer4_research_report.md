# Dreamer 4 — Comprehensive Research Report

*Compiled 20 Sep 2026. Baseline: Hafner*, Yan*, Lillicrap, "Training Agents Inside of Scalable World Models", arXiv:2509.24527 (29 Sep 2025), plus the full surrounding ecosystem: official materials, talks, reimplementations, follow-up papers, press and community discussion.*

---

## 0. TL;DR

- **What it is.** Dreamer 4 is a 2B-parameter world-model agent (400M causal video tokenizer + 1.6B block-causal dynamics transformer) from Google DeepMind. It learns a Minecraft simulator from 2,541 h of offline OpenAI VPT contractor video at native 360×640 / 20 FPS, then trains a policy **entirely inside the simulator** (no environment interaction) and becomes the **first agent to obtain diamonds in Minecraft purely from offline data**.
- **Key technical ideas.** (1) *Shortcut forcing* — diffusion forcing + shortcut models, with x-prediction and a ramp loss weight — gives 4-step frame generation at >20 FPS on one H100 with a 9.6 s context; (2) an efficient space/time-factorized transformer (time attention only every 4th layer, GQA, registers); (3) *agent tokens* inserted into the same transformer for BC + reward + value heads; (4) PMPO (sign-of-advantage policy optimization) with a reverse-KL to a frozen BC prior for imagination RL.
- **Headline numbers.** Iron pickaxe 29.0 % (vs. 16.9 % WM+BC, 11.2 % Gemma‑3 VLA, 0 % VPT finetuned), diamond 0.7 % of 1,000 one-hour episodes; human players complete 14/16 interaction tasks inside the model vs. 5/16 for Oasis-large and 0/16 for Lucid‑v1; only ~100 h of action labels recovers ~85–100 % of full action-conditioning quality; Overworld-only action labels transfer to Nether/End at 76 % PSNR / 80 % SSIM.
- **Status of the work.** Still an arXiv preprint (v1 only; no conference acceptance found). **No official code or weights** — Hafner said on the TalkRL podcast (Nov 2025) that release was "probably not" possible in the current climate. Hafner left DeepMind on 3 Nov 2025 and is building a stealth humanoid-robotics startup in San Francisco (MIT Technology Review, Sep 2026).
- **Ecosystem.** ≥12 public reimplementations. The most significant: **open-dreamer** (next-state; JAX; 1.6B Minecraft world model with browser demo, released Jul 2026, ~387★), **lucidrains/dreamer4** (PyTorch library, 400+ commits), **nicklashansen/dreamer4** (PyTorch, DMControl; superseded by his MMBench2 repo), **edwhu/dreamer4-jax** (educational), **vijayabhaskar-ev/dreamer_v4** (only repo with a rigorous closed-loop evaluation of all 3 phases), **IamCreateAI/Dreamerv4-MC** (1.7B Minecraft weights on HuggingFace, inference only).
- **Follow-up science.** Hansen & Wang (UCSD, Jun 2026) train a 350M Dreamer‑4-recipe model on a 427 h / 210-task benchmark and show hallucination is *predictable and preventable* (data-coverage problem). vijayabhaskar's replication shows the imagination-RL gain is real on average but small and high-variance, and that policies can reward-hack the frozen reward head with no offline metric flagging it.

---

## 1. The paper

**Citation.** Danijar Hafner*, Wilson Yan*, Timothy Lillicrap (equal contribution; Google DeepMind, San Francisco). arXiv:2509.24527 [cs.AI], submitted 29 Sep 2025. Website: https://danijar.com/dreamer4 (redirects to danijar.com/project/dreamer4/). HTML: https://arxiv.org/html/2509.24527v1. PDF: https://arxiv.org/pdf/2509.24527.

**Venue.** No peer-reviewed venue found as of Sep 2026. An ICLR 2026 world-model workshop proposal still cites it as an arXiv preprint. Only v1 exists on arXiv.

### 1.1 Claimed contributions

1. Dreamer 4, a scalable agent that solves challenging control tasks by imagination training inside a world model.
2. First agent to collect diamonds in Minecraft from **offline data only**, substantially improving over OpenAI's VPT offline agent despite ~100× less data.
3. A world model that accurately simulates Minecraft object interactions/game mechanics, running in real time on a single GPU, evaluated by human play-testing against prior Minecraft world models.
4. Shortcut forcing objective + efficient transformer architecture (ablated in detail).
5. Action conditioning learned from a small fraction of labeled data, generalizing to visual domains only seen unlabeled.

### 1.2 Method

**Three phases (one transformer throughout).**

| Phase | What is trained | Objective |
|---|---|---|
| 1. World-model pretraining | Causal tokenizer (frozen afterwards) and interactive dynamics model on video ± actions | Tokenizer: masked autoencoding (MSE + 0.2·LPIPS, patch dropout U(0, 0.9), tanh bottleneck). Dynamics: **shortcut forcing** |
| 2. Agent finetuning | Insert *agent tokens* (task embedding input), policy head, reward head; dynamics loss continues on uniform data | BC with multi-token prediction (L = 8), reward modelling |
| 3. Imagination training | Policy + value heads only; transformer frozen | PMPO with reverse-KL to frozen BC prior; TD value head; γ = 0.997 |

**Tokenizer.** Frame patches (16×16) → transformer encoder → 512×16 bottleneck (reshaped to N_z = 256 tokens × 32 dims for the dynamics model) → decoder. Causal in time so it can be used online.

**Dynamics model / shortcut forcing.** Operates on interleaved (action, latent) sequence with per-frame signal level τ and step size d. Combines *diffusion forcing* (independent noise levels per frame; context frames slightly noised at τ_ctx ≈ 0.1 during inference so the model tolerates its own imperfections) with *shortcut models* (condition on step size; bootstrap large steps from two half-steps). Crucial engineering choices: **x-prediction** (predict clean latents, not velocity — Hafner: velocity prediction forces the network to carry the exact noise pattern through all activations, so small mistakes compound autoregressively), the bootstrap target computed in v-space but the loss scaled back to x-space by (1−τ)², and a ramp loss weight w(τ) = 0.9τ + 0.1. K = 4 sampling steps per frame at inference.

**Architecture.** Pre-RMSNorm, RoPE, SwiGLU, QK-norm, logit soft-capping. Space-only attention in 3 of every 4 layers, time attention every 4th layer; grouped-query attention; register tokens; alternating batch lengths (T1 = 64 short / T2 = 256 long) for cheaper training with long context C = 192 frames (9.6 s at 20 FPS).

**Actions.** 23 binary keyboard variables + 121-way categorical for mouse (μ-law, 11×11 foveated bins, VPT convention). Unlabeled video gets a learned "no action" embedding.

**Agent heads.** Agent tokens attend to all other modalities but **nothing attends back to them** — so the world model never conditions on the policy's intentions. Task = one-hot over 20 tasks (text embeddings would work; Hafner also mentioned a task-conditioned *scalar* reward was chosen over a vector reward to allow open-vocabulary tasks). Data mix for phases 2–3: 50 % uniform / 50 % task-relevant sequences; BC loss only on relevant data, dynamics loss only on uniform data ("to avoid optimistic generations").

**PMPO.** Uses only the sign of the advantage (balanced positive/negative sets, α = 0.5), plus β = 0.3 reverse-KL to the frozen BC policy. Chosen over Dreamer 3's return normalization + entropy bonus; analogous to KL-regularized RLHF.

### 1.3 Datasets (Appendix A)

| Dataset | Size | Resolution / FPS | Actions | Dynamics config |
|---|---|---|---|---|
| Minecraft VPT contractor subsets 6–10 | 2,541 h | 360×640 (zero-padded to 384×640 → 960 patches), 20 FPS | 23 keys + 121-class mouse; game events → rewards | N_z = 256, C = 192, T1/T2 = 64/256 |
| Overworld vs Nether/End split | subset (VPT 6 & 7 excluded) | same | assigned per 5-min chunk via item events | used for action-generalization study |
| SOAR robotics | 180 h (teleop + online RL, successes & failures) | 256×256, 5 FPS | 7-D relative end-effector | N_z = 512, C = 96, T1/T2 = 32/128 |
| Epic Kitchens 100 | 100 h egocentric, 45 kitchens | 256×256, 10 FPS | none | same as SOAR |

90/10 train/eval split by 5-minute recording chunk. Compute: 256–1,024 TPU‑v5p.

### 1.4 Results

**Offline Diamond Challenge (Table 7; 1,000 episodes × 60 min, empty inventory, random worlds).**

| Milestone | VPT (finetuned) | BC (notask) | BC | VLA (Gemma 3) | WM+BC | **Dreamer 4** |
|---|---|---|---|---|---|---|
| Log | 84.3 | 71.4 | 97.3 | 98.5 | 99.6 | 99.1 |
| Planks | 65.3 | 68.6 | 95.7 | 98.3 | 99.6 | 98.9 |
| Crafting table | 4.7 | 63.8 | 93.5 | 97.2 | 99.1 | 98.5 |
| Stick | 52.6 | 62.4 | 95.0 | 97.7 | 98.9 | 98.7 |
| Wooden pickaxe | 0.0 | 33.8 | 86.5 | 94.1 | 97.3 | 96.6 |
| Cobblestone | 6.9 | 32.0 | 83.9 | 91.6 | 97.2 | 95.9 |
| Stone pickaxe | 0.0 | 8.8 | 53.8 | 76.7 | 89.4 | 90.1 |
| Iron ore | 0.1 | 3.6 | 26.5 | 46.3 | 62.9 | 66.7 |
| Furnace | 0.0 | 4.0 | 16.2 | 42.4 | 51.1 | 58.1 |
| Iron ingot | 0.1 | 0.2 | 4.3 | 22.5 | 27.8 | 39.5 |
| Iron pickaxe | 0.0 | 0.0 | 0.6 | 11.2 | 16.9 | 29.0 |
| Diamond | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | **0.7** |

Time-to-milestone (Table 8): Dreamer 4 is fastest at every stage (crafting table 4.4 min vs 7.2 VLA; stone pickaxe 6.7 vs 14.5; iron pickaxe 13.3 vs 31.1; diamond 20.7 min average when achieved — roughly the human average of ~20 min / ~24,000 actions).

Take-aways stated by the authors: (i) world-model representations beat Gemma‑3 representations for BC ("video prediction implicitly learns an understanding of the world that is useful for decision making"); (ii) imagination RL helps most on the hardest milestones and also makes the policy faster; (iii) VPT finetuned (270K h YouTube + 2.5K h contractor) only reliably reaches sticks.

**World-model comparison (Table 1; 1 H100).**

| Model | Params | Resolution | Context | FPS | Human tasks solved |
|---|---|---|---|---|---|
| MineWorld | 1.2B | 384×224 | 0.8 s | 2 | not evaluable (needs actions in advance) |
| Lucid‑v1 | 1.1B | 640×360 | 1.0 s | 44 | 0/16 |
| Oasis (small) | 500M | 640×360 | 1.6 s | 20 | 0/16 |
| Oasis (large) | — | 360×360 | 1.6 s | ~5 | 5/16 |
| **Dreamer 4** | 2B | 640×360 | **9.6 s** | 21 | **14/16** |

The 16 tasks: eat apple, place 3 torches, chop tree, dig 3×3 pit, craft wooden pickaxe, use furnace, place/open workbench, kill zombies, mine diamonds, complete window, place & ride boat, enter portal, place door, bed & sleep, plant reed & pour water, turn 360° & enter house. Failure modes: 9.6 s memory (world changes when you look away long enough), inventory items unclear / drifting over time. Genie 3 is not comparable (no fine-grained mouse/keyboard).

**Action-label efficiency (Fig. 7; PSNR/SSIM normalized 0 % = no actions, 100 % = all 2,541 h).** 10 h of actions → 53 % PSNR / 75 % SSIM; 100 h → 85 % / 100 %; 1,000 h → 100 %. Overworld-only actions → Nether/End (seen only unlabeled): 76 % / 80 %.

**Robotics / real video.** SOAR: counterfactual actions (pick objects, flip bowl, press ball on plate, move towel, throw bowl) rendered plausibly; Epic Kitchens generations from holdout context (Fig. 9). Qualitative only.

**Design ablation cascade (Table 2; 48 h training, FVD on 1,024 × 384-frame generations, lower is better).**

| Change | FPS | FVD |
|---|---|---|
| Diffusion-forcing transformer, K = 64 | 0.8 | 306 |
| K = 4 steps | 9.1 | 875 |
| + shortcut (→ shortcut forcing) | | 329 |
| + x-prediction | | 326 |
| + x-space loss | | 151 |
| + ramp weight | | 102 |
| + alternating batch lengths | | 80 (step 9.8 s → 1.5 s) |
| + long context only every 4th layer | 18.9 | 70 |
| + GQA | 23.2 | 71 |
| + time-factorized long context | 30.1 | 91 |
| + register tokens | | 91 |
| N_z 128 → 256 | 21.4 | 57 |
| (full arch but v-space prediction/loss) | | 124 |

Fig. 8: at 4 sampling steps, shortcut forcing FVD ≈ 60 vs ≈ 530 for plain diffusion forcing; diffusion forcing needs 16–32 steps to match → ~16× fewer network evaluations. Hafner (TalkRL): overall ~30× faster than a diffusion-forcing transformer, ~40× slower than Dreamer 3's RSSM.

### 1.5 Relationship to earlier Dreamers (Appendix F, Table 3)

| | Dreamer 3 (Nature 2025) | Dreamer 4 |
|---|---|---|
| World model | RSSM (RNN + variational) | Block-causal diffusion/flow transformer, shortcut forcing |
| Minecraft input | 64×64 + inventory state, MineRL abstract crafting actions | 360×640 pixels only, raw mouse/keyboard |
| Data | 1.4K h *online* interaction, no human data | 2.5K h *offline* human data, no interaction |
| RL | return normalization + entropy | PMPO + KL to BC prior |
| Speed | ~1,000× faster than a DF transformer | in between (see above) |

VPT RL used 2.5K h contractor + 270K h web + 194K h *online* RL; VPT BC 2.5K + 270K h offline.

### 1.6 Limitations & future work (paper + authors' talks)

- Diamond success is only 0.7 %; the pipeline is "reliable and performant starting point", not a solved task.
- Context/memory 9.6 s; long-term memory is the number-one future item (Hafner: walk into a house for 30 s and the outside is regenerated).
- No epistemic-uncertainty treatment; world model frozen during RL; policy can exploit gaps (Hafner's example: agent crafting a pickaxe from invalid materials, which the model happily renders) — handled via the KL constraint or, in unpublished experiments, a few rounds of *corrective* online data which then allowed a much weaker KL.
- Things learned last by video models: small objects and long-range semantic correlations; tokenizer trained separately (Hafner expects fully end-to-end training eventually).
- Future directions listed: internet-video pretraining, long-term memory, language conditioning, small corrective online data, automatic goal discovery (empowerment/exploration à la APD, Plan2Explore, Director).
- Independent critiques (Pith AI review, EmergentMind): long-horizon prediction accuracy lacks *direct quantitative* evidence; results rely on human play-testing and FVD on 16-frame chunks.

---

## 2. Official materials & the authors

- **Project page** https://danijar.com/project/dreamer4/ — main video (youtube.com/watch?v=oDlBtTcX0g0), uncut evaluation videos (n4SwlSrkhvU, 5CnpLRM8iXA, oZyliSpRMSw, VSKpvb1bnbU), side-by-side comparisons vs Oasis/Lucid, robotics generations. **No code link.**
- **Announcement thread** x.com/danijarh/status/1973072288351396320 (30 Sep 2025): "an agent that learns to solve complex control tasks entirely inside of its scalable world model … first agent to mine diamonds in Minecraft entirely from offline data … co-led with @wilson1yan". Mirrored/discussed on r/accelerate, r/mlscaling, r/singularity, r/reinforcementlearning.
- **TalkRL Podcast E73, "Danijar Hafner on Dreamer v4"** (10 Nov 2025; transcript at talkrl.com/episodes/danijar-hafner-on-dreamer-v4/transcript; described as "ex-GoogleDeepMind RS"). Most substantive first-person source. Key points not in the paper:
  - Why VPT needed 100× more data: "predicting actions is a pretty weak learning signal"; future prediction forces a local world state → much better representations; fine-tuning the world model for BC alone already beats VPT.
  - Minecraft is *very* stochastic from the agent's view (partial observability ≡ stochasticity); RSSM handles moderate stochasticity, diffusion handles multimodal next-frame distributions far better.
  - Inference-speed gap RSSM vs DF transformer ≈ 1,000×; Dreamer 4 sits ~30× faster than DF, ~40× slower than RSSM. Choose RSSM for simple/simulated tasks; you still need the big model for real-world complexity.
  - He has played inside the model for 20+ minutes without it "falling off the manifold"; blurs briefly with many moving objects, then recovers.
  - Unpublished experiments: multimodal variants, larger pretraining, and corrective-data rounds (help; allow weaker KL).
  - Design opinions: "RL in imagination is the right way to do offline RL"; doesn't think Dyna's model-free loss will be necessary; vector reward unnecessary vs task-conditioned scalar reward; tokenizer will eventually be trained end-to-end.
  - Story: team "probably had the most chips per person" at GDM; success-rate curves shifted right week by week; getting the paper out "took some asking around"; **code/checkpoints: "Probably not … getting the paper out was already exceptional enough in the current climate."**
  - Robotics thesis: humanoids < $10k; bottleneck is algorithms, not just data; can't do online RL on a humanoid; recipe = good representations → BC → RL in a world model across diverse imagined scenes.
- **Hack Club AMA with Danijar Hafner** (YouTube vNCX15fkYkE, Dec 2025) — informal Q&A on Dreamer 4 and world models.
- **Danijar Hafner left Google DeepMind on 3 Nov 2025** ("Today is my last day at DeepMind"). MIT Technology Review (8 Sep 2026, "Danijar Hafner is developing plan-ahead agents"), 36kr and CryptoBriefing report a stealth startup in SF (SoMa) applying model-based RL / world models to humanoid robots imported from China. Hacker News (item 45923945) speculated on the move.
- **Wilson Yan** (co-lead; video-generation/multimodal expertise; collaboration began at Berkeley). No public statement about his current affiliation found.

---

## 3. Code ecosystem (no official release)

Star counts are approximate as of Sep 2026.

| Repo | Framework | Scope | Domain / scale | Notes |
|---|---|---|---|---|
| **next-state/open-dreamer** (+ reactor-team/open-dreamer inference) | JAX / Flax NNX | Tokenizer + dynamics (no BC/RL) | Minecraft VPT, **1.6B** dynamics; browser demo | Most faithful large-scale reproduction; released 24 Jul 2026; license "all rights reserved" placeholder; ~387★; DOI 10.5281/zenodo.21475232 |
| **lucidrains/dreamer4** | PyTorch (`pip install dreamer4`) | All 3 phases + env interaction API | Toy (Moving MNIST, Snake, cartpole, HalfCheetah) | 400+ commits, active through Sep 2026, Discord; adds many non-paper ideas (RAC flow decoder, attention residuals, HL-Gauss reward…) — not a faithful replica |
| **nicklashansen/dreamer4** | PyTorch | Tokenizer + dynamics + web UI | DMControl, 30 tasks, 128×128; HF checkpoints | ~401★; 8×3090, 24 h tokenizer / 48 h dynamics; superseded Jun 2026 by **nicklashansen/mmbench2** ("strictly better implementation") |
| **edwhu/dreamer4-jax** | JAX | All 4 stages, educational | Bouncing-square toy (MAE ~40 PSNR, dynamics ~29–30 PSNR) | ~106★; thanks Danijar & Jasmine team; roadmap CoinRun → Minecraft (realised as open-dreamer) |
| **vijayabhaskar-ev/dreamer_v4** | PyTorch, MIT | All 3 phases + closed-loop eval | dm_control ball_in_cup_catch; HF `vijayabhaskarev/dreamer-v4` | ~38★; the only rigorous empirical study of phases 2–3 (see §4.3) |
| **IamCreateAI/Dreamerv4-MC ("Dreamer-MC")** | PyTorch | Inference only; weights on HF | Minecraft; 430M MAE tokenizer + **1.7B** dynamics (9 GB VRAM) | ~64★; infinite generation via ring buffer + sliding KV cache + RoPE re-application, CUDA graphs; training code "coming soon" (as of Jan 2026) |
| **4ku/dreamer4** | PyTorch | All 4 phases | Gridworld (+ LeRobot/DINOv3 extras) | Very new (Sep 2026); documents deviations (β = 0.03, pretrained critic in phase 2, bootstrap ramp-in, PMPO percentile pools) |
| **HKimiwada/Dreamer4** | PyTorch | Pipeline demo | Minecraft contractor data on 8×V100 16 GB; overfit on one video; Atari | 144 commits; MSE-only tokenizer |
| **vFf0621/Dreamer4-torch** | PyTorch | Compact model code | generic | no soft-capping; interleaved action tokens |
| **skr3178/DreamerV4** | PyTorch | — | — | **abandoned** (RTX 3060 insufficient); useful survey of compute needs |
| chrisgao99/dreamer4 | PyTorch | fork of Hansen | — | — |
| softengg-manoj/dreamer4 | — | mirror of lucidrains with "download installer" links | — | **Looks like a spam/scam mirror — avoid** |
| p-doom/**jasmine** (arXiv 2510.27002) | JAX | World-modeling infrastructure (not Dreamer 4 per se) | — | Cited by edwhu/open-dreamer as tooling/advice source |

### 3.1 open-dreamer in depth (the de-facto open reproduction)

Authors Diego Martí Monsó* (Diffusion Forcing co-author), Francesco Sacco*, Edward Hu; sponsored by Reactor (runs the real-time browser demo with a Game⟷Dream toggle). Blog "How to train a frontier-level world model" (next-state.github.io/open-dreamer/) documents the recipe:

- Started on CoinRun (1 GPU), then scaled to the 1.6B Minecraft model on B200s (57–58 % MFU with 256 frames/GPU, plain data-parallel + activation checkpointing, pre-tokenized ArrayRecord + Grain loaders).
- Tokenizer gives ~100× compression; iso-FLOP scaling fits N ∝ C^0.56, D ∝ C^0.44.
- **Muon far more stable than LaProp** (which spiked); EMA weights essential; fp32 params / bf16 matmuls / fp32 norms & flow head.
- x-prediction with a v-space-weighted loss ‖x−x̂‖²/(1−τ)² slightly better than the paper's ramp weight; minibatch optimal-transport pairing of noise/latents stabilized rollouts; μP unnecessary.
- BC/RL phases **not** released. Thanked Hafner & Yan.
- Coverage: Analytics Insight (14 Sep 2026, "The Model DeepMind Described But Never Released") — >350★ by Aug 2026, >1M views on X, featured by MarkTechPost; Martí Monsó: "There was no answer key… publishing the recipe gives another researcher something they can actually reproduce."

### 3.2 Dreamer-MC (IamCreateAI)

Independent Chinese team (Ming Gao et al., 2026; blog findlamp.github.io/dreamer-mc.github.io/). Adapts the Dreamer 4 architecture for *infinite* real-time Minecraft generation: causal "gather-token" MAE tokenizer with temporal attention, decomposed spatial/temporal attention with timestep/stride/action tokens fed as plain tokens (no AdaLN), x0-prediction credited for eliminating drift, long-context variant recalling ~12 s. Supports eating, water collection, weapons, archery, horse riding. Weights public; no agent/RL.

---

## 4. Follow-up research

### 4.1 Hansen & Wang (UCSD), "Hallucination in World Models is Predictable and Preventable" (arXiv 2606.27326, 25 Jun 2026)
Trains a 350M-parameter model that "largely follows the Dreamer 4 recipe" on **MMBench2** (427 h, 210 tasks, ground-truth actions/rewards, live simulators; 200 train / 10 held-out). Identifies three hallucination modes — *perceptual* (tokenizer), *action-marginalization* (dynamics ignores the conditioning actions), *scene divergence* (multi-step rollouts) — and three label-free predictors (tokenizer round-trip residual, flow instability, inter-seed denoising disagreement; Spearman ρ ≈ 0.8). Coverage-aware sampling reduces hallucination at no data cost; using the predictors as curiosity rewards adapts the model to unseen environments with as few as 50 trajectories. Full dataset, code, checkpoints and browser demo released (github.com/nicklashansen/mmbench2). This is effectively the "what breaks in a Dreamer 4-style model and how to detect it" paper.

### 4.2 Dreamer-MC (see §3.2)
Engineering follow-up showing the x-prediction choice is what enables drift-free infinite rollouts, and adding a ring-buffer KV cache for unbounded generation.

### 4.3 vijayabhaskar-ev replication: what phases 2–3 actually buy you
Full pipeline on dm_control *ball_in_cup_catch*, evaluated in the real simulator:
- 6 imagination-RL runs × 500 episodes: BC catch rate 0.356 → RL mean 0.415 (+5.9 pts, 95 % CI [+1.5, +10.4], 6/6 positive) — **but** per-run gains range +1.0…+10.4.
- Re-drawing Phase 2 (BC finetune) dominates: three Phase-2 seeds give BC 0.374 / 0.434 / 0.448 and RL effects of **−32.6 / +24.2 / −8.3 pts** — "the finetune stage is a lottery ticket".
- One policy **reward-hacks the frozen reward head** (imagined return 574 while never catching in reality); no offline metric flagged it. Imagined returns compress (74–78) while real catch rates diverge → closed-loop evaluation is mandatory.
- Deterministic (argmax) readout collapses to the random floor (0.10 vs 0.37 sampled).
- Offline ceiling ~0.57 vs online DreamerV3 0.96 on this task.
These are exactly the risks Hafner discussed (model exploitation, need for KL / corrective data) made quantitative at toy scale.

### 4.4 Adjacent 2026 work citing/using the recipe
- **Next Forcing** (arXiv 2606.11187) — multi-chunk prediction for causal video world models.
- **minWM / Causal Forcing** (arXiv 2605.30263) — minimal causal world-model framework.
- **DreamZero / World Action Models** (arXiv 2602.15922, Feb 2026) — autoregressive video-action model for robots with 4-step and 1-step ("Flash") inference; same design space (few-step AR diffusion for control).
- ICLR 2026 world-model workshop proposal cites Dreamer 4 as motivating prior work.
- p-doom **Jasmine** (arXiv 2510.27002) — JAX infrastructure adopted by several reproductions.

---

## 5. Press, explainers and community discussion

**Press.** TechXplore (Oct 2025; Hafner: "a few hundred hours of action data" suffice; >25× faster generation than typical video models; next: long-term memory) · InfoQ (6 Oct 2025) · implicator.ai (Feb 2026; "the binding constraint is world-model quality, not RL algorithms") · MIT Technology Review (Sep 2026; Hafner's startup) · Analytics Insight (Sep 2026; open-dreamer) · 36kr / CryptoBriefing (Hafner's departure).

**Explainers.** arxiviq Substack deep-dive (Oct 2025, paid) · Pith AI review (May 2026; flags missing direct long-horizon evidence) · EmergentMind topic page · alphaXiv overview · Harold Benoit's technical notes (Dec 2025; good derivation of the x-space/v-space bootstrap scaling) · Medium "First intuitive understanding" (Apr 2026; includes an erratum on flow matching) · Paper-to-Podcast ep. 357 (AI-generated) · Studocu student summary (Ljubljana).

**Community threads.** r/accelerate (1nvbfm1), r/mlscaling (1nvfkgu), r/singularity (1nv4zna), r/reinforcementlearning (1nu4cub), HN 45923945. Recurring themes: (a) confusion between Dreamer 3's *online* diamonds and Dreamer 4's *offline* diamonds; (b) excitement about "learn from unlabeled video, add a few hours of actions" for robotics; (c) disappointment about no code/weights; (d) debate over the 0.7 % diamond rate being called "solved"; (e) reproductions (Hansen's, open-dreamer) getting more traction on X than the paper's own announcement — open-dreamer reportedly >1M views.

---

## 6. Critical assessment — what is established vs. open

**Established (paper + independent evidence).**
- Shortcut forcing + x-prediction gives stable, drift-free, few-step autoregressive latent video; independently confirmed by open-dreamer (1.6B), Dreamer-MC (1.7B) and Hansen (350M).
- World-model representations are a strong initialization for BC (2–3× iron-pickaxe success over a Gemma‑3 VLA at equal data).
- Imagination RL improves over BC on average (paper; vijayabhaskar's toy replication).
- Action conditioning is data-cheap (~100 h) and transfers across visual domains.

**Open / caveats.**
- No official code, weights or hyper-parameter release beyond Appendix A; reproductions differ in optimizer (Muon vs LaProp), loss weighting, and never include the RL phase at Minecraft scale. **Nobody outside DeepMind has reproduced offline diamonds.**
- Diamond success 0.7 %; iron pickaxe 29 %. Progress beyond that likely needs memory, corrective data or better exploration.
- 9.6 s context → no long-term consistency; a known hard limit for building tasks.
- RL against a frozen learned reward/dynamics is exploitable; variance across Phase-2 seeds is large at small scale; imagined returns are not a reliable model-selection signal.
- Hallucination is a data-coverage issue (Hansen) — implies the recipe's promise for robotics depends on coverage-aware data collection.
- No peer review to date; some evaluation is human play-testing with n = 16 tasks.
- Original team dispersed (Hafner → startup); further "Dreamer 5" from DeepMind is not publicly indicated.

---

## 7. Link index

**Primary.** arXiv abs https://arxiv.org/abs/2509.24527 · HTML https://arxiv.org/html/2509.24527v1 · project page https://danijar.com/project/dreamer4/ · announcement https://x.com/danijarh/status/1973072288351396320 · main video https://www.youtube.com/watch?v=oDlBtTcX0g0

**Talks.** TalkRL E73 https://www.talkrl.com/episodes/danijar-hafner-on-dreamer-v4 (transcript at /transcript) · Hack Club AMA https://www.youtube.com/watch?v=vNCX15fkYkE

**Code.** https://github.com/next-state/open-dreamer · https://next-state.github.io/open-dreamer/ · https://github.com/reactor-team/open-dreamer · https://github.com/lucidrains/dreamer4 · https://github.com/nicklashansen/dreamer4 · https://github.com/nicklashansen/mmbench2 · https://github.com/edwhu/dreamer4-jax · https://github.com/vijayabhaskar-ev/dreamer_v4 · https://github.com/IamCreateAI/Dreamerv4-MC (+ https://findlamp.github.io/dreamer-mc.github.io/) · https://github.com/4ku/dreamer4 · https://github.com/HKimiwada/Dreamer4 · https://github.com/vFf0621/Dreamer4-torch · https://github.com/skr3178/DreamerV4 · https://github.com/p-doom/jasmine

**Follow-ups.** Hansen & Wang 2026 https://arxiv.org/abs/2606.27326 / https://www.nicklashansen.com/mmbench2/ · Next Forcing https://arxiv.org/abs/2606.11187 · minWM https://arxiv.org/abs/2605.30263 · DreamZero https://arxiv.org/abs/2602.15922 · Jasmine https://arxiv.org/abs/2510.27002

**Press / explainers.** https://techxplore.com/news/2025-10-deepmind-ai-agent-tasks-scalable.html · https://www.infoq.com/news/2025/10/dreamer-4-minecraft-agent/ · https://www.implicator.ai/dreamer-4-mines-diamonds-in-an-imagined-minecraft/ · https://www.technologyreview.com/2026/09/08/1142088/danijar-hafner-developing-plan-ahead-agents/ · https://www.analyticsinsight.net/artificial-intelligence/the-model-deepmind-described-but-never-released · https://arxiviq.substack.com/p/dreamer-4-training-agents-inside · https://pith.science/paper/2509.24527 · https://www.emergentmind.com/papers/2509.24527 · https://haroldbenoit.com/notes/ml/llms/multi-modality/video/dreamer-4 · https://medium.com/@schunsukesuzuki/first-intuitive-understanding-dreamer-v4-scaling-world-models-to-complex-environments-with-67a4c5119e15
