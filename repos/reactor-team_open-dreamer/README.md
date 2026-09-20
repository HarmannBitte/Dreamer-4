<div align="center">

<img src="assets/banner.png" alt="Open Dreamer" width="100%" />

# Inference

**Minimal local inference for the Open Dreamer world model — roll out new
frames from an MP4 and matching Minecraft VPT actions.**

[🎮 Live Demo](https://next-state.github.io/open-dreamer/) &nbsp;·&nbsp;
[🌐 Project & Training](https://github.com/next-state/open-dreamer)

<br />
<br />

<sub>REAL-TIME DEMO POWERED BY</sub>

<a href="https://reactor.inc">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="assets/reactor-logo-light.svg" />
    <img alt="Reactor" src="assets/reactor-logo-dark.svg" height="24" />
  </picture>
</a>

</div>

---

This repository is a small, self-contained rollout harness for
[Open Dreamer](https://github.com/next-state/open-dreamer). Given a short video
clip and a sequence of Minecraft/VPT-style actions, it encodes the clip into the
model's latent space and generates the frames that follow — a local, scriptable
way to drive the world model on your own footage.

Want to just play with the model instead? The **[live demo](https://next-state.github.io/open-dreamer/)**
runs the real-time version in your browser, no setup required.

## 🎮 Try it now

The easiest way to experience Open Dreamer is the in-browser demo — step into a
generated Minecraft world and play it in real time:

👉 **[Open the demo](https://next-state.github.io/open-dreamer/)**

Read on if you want to run rollouts locally.

## ⚙️ Quick Start

Run every command below from the repository root.

### 1. Install

```bash
uv sync
```

### 2. Provide a checkpoint

You need a trained Open Dreamer checkpoint (an Orbax checkpoint directory). Train
one with the [Open Dreamer training pipeline](https://github.com/next-state/open-dreamer),
or point `--checkpoint_path` at a checkpoint you already have. The examples below
use `/path/to/open-dreamer-checkpoint`.

### 3. Verify JAX sees the GPU

Rollouts require a CUDA-visible JAX GPU; the script exits before loading the
checkpoint if `jax.devices("gpu")` is empty.

```bash
uv run python - <<'PY'
import jax
import jax.numpy as jnp
print("backend", jax.default_backend())
print("gpu devices", jax.devices("gpu"))
x = jnp.ones((2048, 2048), dtype=jnp.float32)
y = (x @ x).block_until_ready()
print("result device", y.device)
PY
```

### 4. Download the sample data

`download_vpt_sample.py` fetches OpenAI's official Minecraft VPT 10.x contractor
index, verifies the sample `.mp4` is listed, and downloads the MP4 together with
its paired `.jsonl` action file:

```bash
uv run python download_vpt_sample.py --overwrite
```

Expected files:

```text
samples/vpt/cheeky-cornflower-setter-02e496ce4abb-20220421-092639.mp4
samples/vpt/cheeky-cornflower-setter-02e496ce4abb-20220421-092639.jsonl
```

### 5. Run a rollout

```bash
XLA_PYTHON_CLIENT_PREALLOCATE=false uv run python inference.py \
  --checkpoint_path /path/to/open-dreamer-checkpoint \
  --input_mp4 samples/vpt/cheeky-cornflower-setter-02e496ce4abb-20220421-092639.mp4 \
  --actions_path samples/vpt/cheeky-cornflower-setter-02e496ce4abb-20220421-092639.jsonl \
  --output_mp4 outputs/vpt_sample_rollout.mp4 \
  --num_context_frames 4 \
  --horizon 1 \
  --num_steps 4 \
  --use_ema
```

## Larger rollouts

Increase `--num_context_frames` and `--horizon` for a longer output:

```bash
XLA_PYTHON_CLIENT_PREALLOCATE=false uv run python inference.py \
  --checkpoint_path /path/to/open-dreamer-checkpoint \
  --input_mp4 samples/vpt/cheeky-cornflower-setter-02e496ce4abb-20220421-092639.mp4 \
  --actions_path samples/vpt/cheeky-cornflower-setter-02e496ce4abb-20220421-092639.jsonl \
  --output_mp4 outputs/rollout.mp4 \
  --num_context_frames 16 \
  --horizon 64 \
  --num_steps 4 \
  --use_ema
```

Only the first `--num_context_frames` video frames are read and encoded. The
action file must contain at least `num_context_frames + horizon` actions; the
full action sequence is shifted before it is split into context and future
actions.

## Input format

The action file may be a JSON array or JSONL. Each entry is a VPT-style action
dictionary with `mouse` and `keyboard` fields, for example:

```json
{"mouse":{"dx":0.0,"dy":0.0,"buttons":[],"dwheel":0.0},"keyboard":{"keys":["key.keyboard.w"]}}
```

Input video frames must be RGB `368x640`, or RGB `360x640` so they can be
zero-padded to the trained `368x640` model shape.

## 📚 References

- Open Dreamer: [project page, blog post, and training pipeline](https://github.com/next-state/open-dreamer)
- Dreamer 4: [Training Agents Inside of Scalable World Models](https://danijar.com/project/dreamer4/)

## 📄 License

**All rights reserved.** See [LICENSE](LICENSE). This is a temporary notice; a
formal license is expected in a future release.
