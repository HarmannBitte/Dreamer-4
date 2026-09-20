from __future__ import annotations

import argparse
import json
import sys
from contextlib import AbstractContextManager
from pathlib import Path
from typing import Any

import imageio.v3 as iio
import jax
import jax.numpy as jnp
import numpy as np
from flax import nnx

from pipeline.actions import Actions, parse_action_dicts, shift_actions
from pipeline.checkpointing import DynamicsCheckpointBundle
from pipeline.generation import DenoiseSchedule, latent_rollout
from pipeline.parallel import build_parallel

MODEL_HEIGHT = 368
MODEL_WIDTH = 640
MODEL_CHANNELS = 3


@nnx.jit
def encode_jit(tokenizer, frames: jax.Array) -> jax.Array:
    latents, _, _ = tokenizer.encode(frames, deterministic=True)
    return latents


@nnx.jit
def decode_jit(tokenizer, latents: jax.Array) -> jax.Array:
    frames, _ = tokenizer.decode(latents, deterministic=True)
    return frames


def decoded_uint8(frames: jax.Array) -> np.ndarray:
    return np.array(jnp.clip(frames, 0, 255).astype(jnp.uint8), copy=True)


def load_action_dicts(path: Path) -> list[dict[str, Any]]:
    text = path.read_text()
    stripped = text.lstrip()
    if not stripped:
        raise ValueError(f"Action file is empty: {path}")
    if stripped[0] == "[":
        data = json.loads(text)
        if not isinstance(data, list):
            raise ValueError(f"Expected a JSON array in {path}")
        return data

    actions = []
    for line_no, line in enumerate(text.splitlines(), start=1):
        line = line.strip()
        if not line:
            continue
        try:
            item = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSONL at {path}:{line_no}: {exc}") from exc
        if not isinstance(item, dict):
            raise ValueError(f"Expected object at {path}:{line_no}")
        actions.append(item)
    if not actions:
        raise ValueError(f"No actions found in {path}")
    return actions


def add_batch_dim(actions: Actions) -> Actions:
    return jax.tree.map(lambda x: jnp.asarray(x)[None] if x is not None else None, actions)


def mesh_context(mesh: Any) -> AbstractContextManager[Any]:
    if hasattr(jax, "set_mesh"):
        return jax.set_mesh(mesh)
    return mesh


def require_gpu() -> None:
    try:
        gpu_devices = jax.devices("gpu")
    except RuntimeError as exc:
        raise RuntimeError(
            "No JAX GPU devices are available. This checkpoint is too large for useful CPU inference; "
            "run on a machine where `nvidia-smi` works and `jax.devices('gpu')` is non-empty."
        ) from exc
    if not gpu_devices:
        raise RuntimeError(
            "No JAX GPU devices are available. This checkpoint is too large for useful CPU inference; "
            "run on a machine where `nvidia-smi` works and `jax.devices('gpu')` is non-empty."
        )
    print(f"Using JAX GPU backend with devices: {gpu_devices}", flush=True)


def read_video(path: Path, required_frames: int) -> tuple[np.ndarray, float]:
    if not path.exists():
        raise FileNotFoundError(f"Input MP4 not found: {path}")

    try:
        meta = iio.immeta(path)
        fps = float(meta.get("fps") or 20.0)
    except Exception:
        fps = 20.0

    frames = []
    for idx, frame in enumerate(iio.imiter(path)):
        if idx >= required_frames:
            break
        arr = np.asarray(frame)
        if arr.ndim != 3 or arr.shape[-1] != MODEL_CHANNELS:
            raise ValueError(
                f"Expected RGB video frames with shape HxWx3, got {arr.shape} at frame {idx}"
            )
        if arr.shape[:2] == (MODEL_HEIGHT, MODEL_WIDTH):
            prepared = arr
        elif arr.shape[:2] == (360, MODEL_WIDTH):
            prepared = np.pad(arr, ((4, 4), (0, 0), (0, 0)), mode="constant")
        else:
            raise ValueError(
                f"Unsupported frame size {arr.shape[:2]} at frame {idx}; "
                f"expected {MODEL_HEIGHT}x{MODEL_WIDTH} or 360x{MODEL_WIDTH}"
            )
        frames.append(prepared.astype(np.uint8, copy=False))

    if len(frames) < required_frames:
        raise ValueError(
            f"Input video has {len(frames)} readable RGB frames, but "
            f"num_context_frames requires {required_frames}"
        )
    return np.stack(frames, axis=0), fps


def decode_generated_latents(
    tokenizer: Any,
    latents: jax.Array,
    *,
    context_frames: int,
    horizon: int,
    chunk_size: int,
) -> np.ndarray:
    if chunk_size < 1:
        raise ValueError("--decode_chunk_size must be >= 1")

    decoder_context = tokenizer.decoder.context_length
    overlap = max(0, decoder_context - 1) if decoder_context is not None else 0
    generated_chunks = []
    for offset in range(0, horizon, chunk_size):
        total_start = context_frames + offset
        total_end = context_frames + min(offset + chunk_size, horizon)
        window_start = max(0, total_start - overlap)
        window_latents = latents[:, window_start:total_end]

        decoded_window = decode_jit(tokenizer, window_latents)
        take_start = total_start - window_start
        take_count = total_end - total_start
        generated = decoded_window[:, take_start : take_start + take_count]
        generated_chunks.append(decoded_uint8(generated[0]))

    return np.concatenate(generated_chunks, axis=0)


def write_video(path: Path, frames: np.ndarray, fps: float) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    iio.imwrite(path, frames.astype(np.uint8), fps=fps, codec="libx264", macro_block_size=16)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Roll out Open-Dreamer frames from an MP4 and VPT JSON actions.")
    parser.add_argument("--checkpoint_path", type=Path, required=True)
    parser.add_argument("--input_mp4", type=Path, required=True)
    parser.add_argument("--actions_path", type=Path, required=True)
    parser.add_argument("--output_mp4", type=Path, required=True)
    parser.add_argument("--context_frames", "--num_context_frames", dest="context_frames", type=int, default=16)
    parser.add_argument("--horizon", type=int, default=64)
    parser.add_argument("--num_steps", type=int, default=4)
    parser.add_argument("--decode_chunk_size", type=int, default=16)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--parallel_strategy", choices=("data", "fsdp", "tp", "sp"), default="data")
    parser.add_argument("--use_ema", action="store_true", help="Use dynamics_ema instead of dynamics.")
    parser.add_argument("--no_kv_cache", action="store_true", help="Disable dynamics KV caching for debugging.")
    parser.add_argument("--allow_cpu", action="store_true", help="Allow CPU inference. Not recommended for Jelly.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not args.checkpoint_path.exists():
        raise FileNotFoundError(f"Checkpoint directory not found: {args.checkpoint_path}")
    if args.context_frames < 1:
        raise ValueError("--context_frames must be >= 1")
    if args.horizon < 1:
        raise ValueError("--horizon must be >= 1")
    if not args.allow_cpu:
        require_gpu()

    total_actions = args.context_frames + args.horizon
    raw_actions = load_action_dicts(args.actions_path)
    if len(raw_actions) < total_actions:
        raise ValueError(
            f"Need at least {total_actions} actions for context+horizon, got {len(raw_actions)} from {args.actions_path}"
        )

    frames_np, fps = read_video(args.input_mp4, required_frames=args.context_frames)
    frames = jnp.asarray(frames_np[None])

    actions = parse_action_dicts(raw_actions[:total_actions])
    actions = add_batch_dim(actions)

    mesh, _, mesh_rules = build_parallel(args.parallel_strategy)
    with mesh_context(mesh):
        bundle = DynamicsCheckpointBundle.from_pretrained(
            str(args.checkpoint_path),
            mesh_rules=mesh_rules,
            model_names={"tokenizer", "dynamics_ema" if args.use_ema else "dynamics"},
        )
        tokenizer = bundle.tokenizer
        dynamics = bundle.dynamics_ema if args.use_ema else bundle.dynamics
        if dynamics is None:
            name = "dynamics_ema" if args.use_ema else "dynamics"
            raise RuntimeError(f"Checkpoint did not restore {name}")

        # Shift before splitting so context and future actions preserve training/eval alignment.
        actions = shift_actions(actions, dynamics.cfg.categorical_action_dim)
        latents = encode_jit(tokenizer, frames)
        latents_ctx = latents
        actions_ctx = actions[:, : args.context_frames]
        actions_future = actions[:, args.context_frames : total_actions]

        schedule = DenoiseSchedule.init(args.num_steps, dynamics.cfg.k_max)
        rollout_result = latent_rollout(
            dynamics=dynamics,
            policy=actions_future,
            schedule=schedule,
            latents_ctx=latents_ctx,
            actions_ctx=actions_ctx,
            num_steps=args.horizon,
            rng=jax.random.PRNGKey(args.seed),
            deterministic=True,
            use_kv_cache=not args.no_kv_cache,
        )

        generated_frames = decode_generated_latents(
            tokenizer,
            rollout_result["latents"],
            context_frames=args.context_frames,
            horizon=args.horizon,
            chunk_size=args.decode_chunk_size,
        )
        output_frames = np.concatenate([frames_np, generated_frames], axis=0)

    write_video(args.output_mp4, output_frames, fps=fps)
    print(f"Wrote {output_frames.shape[0]} frames to {args.output_mp4}")


if __name__ == "__main__":
    try:
        main()
    except (FileNotFoundError, ValueError, RuntimeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1) from None
