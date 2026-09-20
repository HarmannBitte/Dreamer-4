---
license: cc-by-4.0
task_categories:
- reinforcement-learning
- robotics
tags:
- world-models
- continuous-control
- video-prediction
- robotics
- dreamer
pretty_name: MMBench2
size_categories:
- 10K<n<100K
viewer: false
---

<div align="center">

# MMBench2

<h3 align="center"><a href="https://www.nicklashansen.com/mmbench2">Hallucination in World Models is Predictable and Preventable</a></h3>

[Nicklas Hansen](https://www.nicklashansen.com) &nbsp;·&nbsp; [Xiaolong Wang](https://xiaolonw.github.io) &nbsp;·&nbsp; UC San Diego

[![Interactive Paper](https://img.shields.io/badge/Interactive%20Paper-2a6fdb?style=for-the-badge)](https://www.nicklashansen.com/mmbench2)
[![Live Demo](https://img.shields.io/badge/Live%20Demo-e8590c?style=for-the-badge)](https://www.nicklashansen.com/mmbench2/#live-demo)
[![Checkpoints](https://img.shields.io/badge/Checkpoints-fcc419?style=for-the-badge&logo=huggingface&logoColor=black)](https://huggingface.co/nicklashansen/mmbench2-models)
[![License](https://img.shields.io/badge/License-CC--BY--4.0-2e7d32?style=for-the-badge)](https://creativecommons.org/licenses/by/4.0/)

</div>

---

**MMBench2** is a large-scale dataset for visual world modeling, accompanying the paper [**Hallucination in World Models is Predictable and Preventable**](https://www.nicklashansen.com/mmbench2). It spans **210 continuous control tasks** across **10 domains** (DMControl, DMControl Extended, Meta-World, ManiSkill3, MuJoCo, MiniArcade, Box2D, RoboDesk, OGBench, and Atari) comprising **65,600 mixed-quality trajectories** (**427 hours** of 224×224 RGB video at 15 fps; **~23M frames**), with ground-truth action and reward labels, language instructions, and live simulators for every task. Actions span **1–16 dimensions** (zero-padded to 16 with a per-dimension validity mask). Of the 210 tasks, **200 form the pretraining corpus** and **10 are held out as entirely unseen transfer tasks**.

## Domains

| Domain | Tasks | Action dim | Episode length | Reward |
|--------|------:|------------|----------------|--------|
| DMControl | 23 | 1–12 | 500 | dense / sparse |
| DMControl Extended | 16 | 1–7 | 500 | dense / sparse |
| Meta-World | 49 | 4 | 100 | dense |
| ManiSkill3 | 37 | 1–12 | 25–500 | dense / sparse |
| MuJoCo | 6 | 1–8 | 50–1000 | dense / sparse |
| MiniArcade | 24 | 1–2 | 200–500 | dense / sparse |
| Box2D | 8 | 2–4 | 500 | dense |
| RoboDesk | 6 | 5 | 100 | dense |
| OGBench | 14 | 2–8 | 100–1000 | dense |
| Continuous Atari | 27 | 3 | 1000 | sparse |
| **Total** | **210** | 1–16 | 25–1000 | — |

## Partitions

The dataset is organized into top-level partitions by behavior source. The base pretraining corpus (200 tasks) is split across diverse behavior policies, plus held-out validation and test splits:

| Partition | Description |
|-----------|-------------|
| `expert` | Expert policy trajectories (high-quality behavior). |
| `mixed-large` | Large mixed-quality corpus of diverse behaviors. |
| `mixed-small` | Smaller mixed-quality corpus of diverse behaviors. |
| `zeros` | No-op (all-zero action) trajectories. |
| `val` | Validation split (held-out expert trajectories). |
| `test` | Test split (held-out expert trajectories). |

The `active_*` partitions are the **targeted data collection** sets (50 trajectories per task) used for the finetuning experiments, collected on 10 seen tasks as well as 10 held-out transfer tasks under different collection policies:

| Partition | Description |
|-----------|-------------|
| `active_curiosity_u_r_norm` | Curiosity policy driven by the proposed `u_r_norm` hallucination predictor. |
| `active_expert` | Expert policy collection. |
| `active_human` | Human play. |
| `active_random` | Random actions. |
| `active_zero` | No-op (all-zero) actions. |
| `active_test` | Test trajectories (held-out expert trajectories). |
| `active_test_human` | Human-collected test trajectories. |

## Usage

Download with the accompanying code release:

```
cd dreamer4
python download_dataset.py --local_dir ./data                 # full dataset
python download_dataset.py --local_dir ./data --subset val    # a single partition
```

Then preprocess into the sharded format (requires approx. **8 TB** disk space) used for training:

```
bash preprocess.sh            # preprocess every downloaded partition under ./data
```

Or download directly with the Hugging Face CLI:

```
hf download nicklashansen/mmbench2 --repo-type dataset --include "val/*" --local-dir ./data
```

## License

Released under the [Creative Commons Attribution 4.0 International (CC-BY-4.0)](https://creativecommons.org/licenses/by/4.0/) license.

## Citation

```bibtex
@misc{Hansen2026Hallucination,
	title={Hallucination in World Models is Predictable and Preventable},
	author={Nicklas Hansen and Xiaolong Wang},
	year={2026},
	eprint={2606.27326},
	archivePrefix={arXiv},
	primaryClass={cs.LG}
}
```

## Acknowledgments

MMBench2 extends [MMBench](https://arxiv.org/abs/2511.19584) and the world model accompanying this dataset builds on [Dreamer 4](https://arxiv.org/abs/2509.24527).
