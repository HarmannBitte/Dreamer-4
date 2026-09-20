# huggingface/ — model & dataset cards + file listings (fetched 2026-09-20 via `https://huggingface.co/api/{models,datasets}/<id>?blobs=true`)

**No weights or datasets were downloaded** (0.8 GB – 1.9 TB each, see sizes below). For every repo this folder holds
`README_<kind>_<owner>__<name>.md` (the raw model/dataset card) and `api_<kind>_<owner>__<name>.json` (full API record incl. per-file sizes;
for the three datasets with > 1,000 files the `siblings` list was truncated locally to the first 300 entries — noted inside each JSON).
`_hf_summary.json` is a compact summary of all eight repos.

## Models (checkpoints)

| HF repo | Belongs to | Total size | Files | License | Last modified | Largest files | Report relevance |
|---|---|---|---|---|---|---|---|
| [IamCreateAI/Dreamerv4-MC](https://huggingface.co/IamCreateAI/Dreamerv4-MC) | `repos/IamCreateAI_Dreamerv4-MC` (Dreamer-MC) | 4.2 GB | 7 | apache-2.0 | 2026-01-30 | `dynamic/diffusion_pytorch_model.safetensors` 3.3 GB, `tokenizer/diffusion_pytorch_model.safetensors` 0.9 GB | only public **Minecraft** Dreamer 4-style world-model weights (1.7 B, inference only) |
| [nicklashansen/dreamer4](https://huggingface.co/nicklashansen/dreamer4) | `repos/nicklashansen_dreamer4` | 0.77 GB | 5 | mit | 2026-01-20 | `dynamics.pt` 512 MB, `tokenizer.pt` 257 MB | pretrained DMControl tokenizer + dynamics (superseded by MMBench2) |
| [nicklashansen/mmbench2-models](https://huggingface.co/nicklashansen/mmbench2-models) | `repos/nicklashansen_mmbench2` | 4.27 GB | 9 | mit | 2026-07-09 | `base/`, `combined/`, `coverage_aware/` × (`dynamics.pt` 1.02 GB + `tokenizer.pt` 407 MB) | the 350 M models of Hansen & Wang 2026 (base / coverage-aware / combined) |
| [vijayabhaskarev/dreamer-v4](https://huggingface.co/vijayabhaskarev/dreamer-v4) | `repos/vijayabhaskar-ev_dreamer_v4` | 2.93 GB | 14 | mit | 2026-08-08 | `ball_in_cup/agent_bc.pt` 507 MB, `ball_in_cup/seeds/bc_seed1{1,2,3}.pt`, `ball_in_cup/world_model.pt` 491 MB | checkpoints of the full 3-phase (tokenizer → WM+BC → RL) reproduction incl. multi-seed BC agents |

## Datasets

| HF repo | Total size | Files | License | Last modified | Used by | Notes |
|---|---|---|---|---|---|---|
| [nicklashansen/dreamer4](https://huggingface.co/datasets/nicklashansen/dreamer4) | 30.9 GB | 1,078 | mit | 2026-01-18 | nicklashansen/dreamer4, vijayabhaskar-ev, chrisgao99 forks | DMControl `expert/`, `mixed-small/`, `mixed-large/` trajectory sets |
| [nicklashansen/mmbench2](https://huggingface.co/datasets/nicklashansen/mmbench2) | 113.9 GB | 7,658 | cc-by-4.0 | 2026-07-09 | nicklashansen/mmbench2 | MMBench2 (DMControl + Atari + …) train/test splits |
| [zhwang4ai/OpenAI-Minecraft-Contractor](https://huggingface.co/datasets/zhwang4ai/OpenAI-Minecraft-Contractor) | 1,687.9 GB | 68,012 | mit | 2025-04-16 | Dreamer-MC, HKimiwada, 4ku | HF mirror of the OpenAI **VPT contractor** data (the ≈2.5 k h source that Dreamer 4 itself was trained on) |
| [p-doom/open_ai_minecraft_arrayrecords_chunked](https://huggingface.co/datasets/p-doom/open_ai_minecraft_arrayrecords_chunked) | 1,870.5 GB | 181 | cc0-1.0 | 2025-08-05 | open-dreamer (next-state), Jasmine | same VPT data re-packed as ArrayRecord shards (~16 GB each) for JAX pipelines |

Download hint: `huggingface-cli download <repo> --local-dir <dir>` (add `--repo-type dataset` for datasets).
