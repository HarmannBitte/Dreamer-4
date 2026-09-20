---
license: mit
tags:
- reinforcement-learning
- model-based-rl
- world-models
- dreamer
- flow-matching
- pytorch
library_name: pytorch
pipeline_tag: reinforcement-learning
---

# Dreamer V4 (from-scratch) — checkpoints

Inference checkpoints for a from-scratch PyTorch reproduction of **DreamerV4** (Hafner, Yan & Lillicrap, 2025; [arXiv:2509.24527](https://arxiv.org/abs/2509.24527)): tokenizer → flow-matching world model → behavior-cloned agent → imagination RL (PMPO). Checkpoints are trained end-to-end on `ball_in_cup_catch`.

**Code:** https://github.com/vijayabhaskar-ev/dreamer_v4

## Checkpoints (optimizer state stripped — inference only)

| file | what it is | size |
|---|---|---|
| `ball_in_cup/tokenizer.pt` | masked-autoencoder tokenizer (128×128) | 300 MB |
| `ball_in_cup/agent_bc.pt` | BC agent — world model + categorical policy + reward/continue heads | 507 MB |
| `ball_in_cup/agent_imagination_rl.pt` | imagination-RL policy + value heads (loads **on top of** `agent_bc`) | 7 MB |
| `ball_in_cup/world_model.pt` | world-model base, before agent finetuning — optional, only to retrain the agent | 491 MB |

Minimum set to reproduce the eval: `tokenizer` + `agent_bc` + `agent_imagination_rl` (~814 MB).

## Real-env result (closed-loop dm_control; 6 training runs × 500 episodes)

Across **six independent imagination-RL training runs** (identical recipe, different training seeds), each evaluated on the same 500 seeded episodes against a shared BC baseline (catch 0.356, random 0.094): **imagination-RL improves catch rate by +5.9 points on average** (95% CI [+1.5, +10.4], t(5)=3.40, 6/6 runs positive) and **return by +63.6** — roughly 54% from succeeding more often, 46% from catching sooner and holding longer. Per-run outcomes range from null (+1.0, p=0.77) to +10.4 (p=0.001): training-seed variance (~3.2 pts) is comparable to the effect, so single-run comparisons mislead.

> **Supersedes** the earlier single-run n=50 result reported here ("imagination-RL ≈ BC, p = 0.63") — that training run was a below-average draw. The checkpoint released here (`agent_imagination_rl.pt`) **is that original run** (run 1 of 6, catch 0.374 at n=500); the quickstart below therefore reproduces its numbers exactly. Full multi-run analysis and the reproduction scripts (`run_seed_study.sh`, `analysis/paper_stats.py`) are in the code repo.

## Reproduce

```bash
pip install -r requirements.txt && pip install dm_control mujoco
export MUJOCO_GL=egl
python -m dynamics.evaluate_env \
  --phase2-ckpt    ball_in_cup/agent_bc.pt \
  --phase3-ckpt    ball_in_cup/agent_imagination_rl.pt \
  --tokenizer-ckpt ball_in_cup/tokenizer.pt \
  --task ball_in_cup_catch --action-dim 2 \
  --num-episodes 50 --policies phase3,bc,random \
  --device cuda --readout sample --wandb-disabled --output-dir eval-stoch
```

## Provenance

Weights are derived from expert demonstrations in [nicklashansen/dreamer4](https://github.com/nicklashansen/dreamer4); the dataset itself is not redistributed (regenerate via `convert_hansen_to_npz.py` in the code repo). A faithful reproduction on a single simple task, evaluated closed-loop with multi-run statistics — not a SOTA model. Headline finding: imagination-RL improves on its BC initialization on average (+5.9 pts catch rate over six runs), with training-seed variance large enough that single-run comparisons mislead.
