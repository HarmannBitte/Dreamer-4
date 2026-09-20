---
license: mit
tags:
- world-models
- reinforcement-learning
- robotics
- video-prediction
- dreamer
---

<div align="center">

# MMBench2 World Model Checkpoints

<h3 align="center"><a href="https://www.nicklashansen.com/mmbench2">Hallucination in World Models is Predictable and Preventable</a></h3>

[Nicklas Hansen](https://www.nicklashansen.com) &nbsp;·&nbsp; [Xiaolong Wang](https://xiaolonw.github.io) &nbsp;·&nbsp; UC San Diego

[![Interactive Paper](https://img.shields.io/badge/Interactive%20Paper-2a6fdb?style=for-the-badge)](https://www.nicklashansen.com/mmbench2)
[![Live Demo](https://img.shields.io/badge/Live%20Demo-e8590c?style=for-the-badge)](https://www.nicklashansen.com/mmbench2/#live-demo)
[![Dataset](https://img.shields.io/badge/Dataset-fcc419?style=for-the-badge&logo=huggingface&logoColor=black)](https://huggingface.co/datasets/nicklashansen/mmbench2)
[![License](https://img.shields.io/badge/License-MIT-2e7d32?style=for-the-badge)](https://opensource.org/licenses/MIT)

</div>

---

The world model follows the architecture and two-stage training recipe of [Dreamer 4](https://arxiv.org/abs/2509.24527), adapted for large-scale multi-task continuous control, and is trained on **MMBench2** — a 427-hour, 210-task dataset for visual world modeling (see the [dataset repository](https://huggingface.co/datasets/nicklashansen/mmbench2)). Each variant is a `(tokenizer.pt, dynamics.pt)` pair at 224×224 resolution:

- **tokenizer** — a causal video tokenizer (50M-parameter encoder + 50M-parameter decoder, projecting to a 64-dim continuous latent).
- **dynamics** — a 250M-parameter block-causal Transformer trained on the frozen tokenizer with a shortcut flow-matching objective.

## Variants

| Variant | Description |
|---------|-------------|
| `base` | Pretrained world model (200 tasks) |
| `coverage_aware` | Coverage-aware finetuned world model (200 tasks) |
| `combined` | `coverage_aware` finetuned with all targeted data collection sources (210 tasks) |

## Repository layout

```
base/            tokenizer.pt  dynamics.pt
coverage_aware/  tokenizer.pt  dynamics.pt
combined/        tokenizer.pt  dynamics.pt
```

## Usage

Using the accompanying code release:

```
cd dreamer4
python download_checkpoints.py --variant combined     # or: base | coverage_aware | all
./run_interactive.sh combined                          # launch the interactive interface
```

`download_checkpoints.py` fetches the `(tokenizer.pt, dynamics.pt)` pair into `./checkpoints/<variant>/`. Alternatively, download directly with the Hugging Face CLI:

```
hf download nicklashansen/mmbench2-models --include "combined/*" --local-dir ./checkpoints
```

See the [paper](https://www.nicklashansen.com/mmbench2) and the code release for architecture details, training recipes, and the hallucination detection and mitigation methods.

## License

Released under the MIT License.

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
