# papers/ — primary literature (14 PDFs, fetched 2026-09-20 from arxiv.org)

| File | arXiv | Title / authors | Role in the report | Local size | Notes |
|---|---|---|---|---|---|
| `2509.24527_Dreamer4_Training_Agents_Inside_Scalable_World_Models.pdf` | [2509.24527](https://arxiv.org/abs/2509.24527) | **Training Agents Inside of Scalable World Models** — Hafner*, Yan*, Lillicrap (Google DeepMind, 29 Sep 2025, v1) | **The baseline paper (Dreamer 4)** | 3.5 MB | original, untouched. Also: `2509.24527_Dreamer4_arxiv_html_version.html` (arXiv HTML render, truncates around Table 1), `2509.24527_arxiv_abstract_page.html`, `2509.24527.bib` (arXiv BibTeX), `2509.24527_arxiv_api_metadata.xml` (arXiv API record), `2509.24527_openalex.json` (OpenAlex record) |
| `2301.04104_DreamerV3_Mastering_Diverse_Domains.pdf` | [2301.04104](https://arxiv.org/abs/2301.04104) | Mastering Diverse Domains through World Models (DreamerV3) — Hafner et al. | predecessor; RSSM vs. transformer comparison | 2.7 MB | untouched |
| `2009.01791_APD_Action_and_Perception_as_Divergence_Minimization.pdf` | [2009.01791](https://arxiv.org/abs/2009.01791) | Action and Perception as Divergence Minimization — Hafner et al. | background for Hafner's research programme | 0.5 MB | untouched |
| `2407.01392_Diffusion_Forcing_Chen_et_al.pdf` | [2407.01392](https://arxiv.org/abs/2407.01392) | Diffusion Forcing — Chen et al. | one of the two ingredients of *shortcut forcing* | 2.5 MB | **images downsampled** (18.9 → 2.5 MB) |
| `2410.12557_Shortcut_Models_Frans_Hafner_Levine_Abbeel.pdf` | [2410.12557](https://arxiv.org/abs/2410.12557) | One Step Diffusion via Shortcut Models — Frans, Hafner, Levine, Abbeel | second ingredient of *shortcut forcing* | 1.0 MB | **images downsampled** (11.4 → 1.0 MB) |
| `2502.03444_MAETok_Masked_Autoencoders_Tokenizers.pdf` | [2502.03444](https://arxiv.org/abs/2502.03444) | Masked Autoencoders Are Effective Tokenizers for Diffusion Models (MAETok) | inspiration for the causal MAE tokenizer | 3.1 MB | **images downsampled** (36.9 → 3.1 MB) |
| `2206.11795_VPT_Video_PreTraining_Baker_et_al.pdf` | [2206.11795](https://arxiv.org/abs/2206.11795) | Video PreTraining (VPT) — Baker et al. (OpenAI) | source of the 2,541 h contractor dataset; baseline in Table 7 | 3.5 MB | **images downsampled** (7.7 → 3.5 MB) |
| `2504.08388_MineWorld.pdf` | [2504.08388](https://arxiv.org/abs/2504.08388) | MineWorld — Guo et al. (Microsoft) | Minecraft world-model baseline (Table 1) | 1.2 MB | untouched |
| `2510.27002_Jasmine_JAX_world_modeling_codebase.pdf` | [2510.27002](https://arxiv.org/abs/2510.27002) | Jasmine — p(doom) | JAX world-model codebase + largest open Minecraft video dataset | 2.9 MB | untouched |
| `2511.19584_Hansen_Massively_Multitask_World_Models.pdf` | [2511.19584](https://arxiv.org/abs/2511.19584) | Learning Massively Multitask World Models for Continuous Control — Hansen et al. | context for nicklashansen/dreamer4 & MMBench | 1.7 MB | **images downsampled** (7.7 → 1.7 MB) |
| `2606.27326_Hansen_Wang_Hallucination_in_World_Models.pdf` | [2606.27326](https://arxiv.org/abs/2606.27326) | Hallucination in World Models is Predictable and Preventable — Hansen & Wang (2026) | main scientific follow-up built on the Dreamer 4 recipe (MMBench2) | 1.1 MB | **images downsampled** (6.3 → 1.1 MB) |
| `2602.15922_DreamZero_World_Action_Models.pdf` | [2602.15922](https://arxiv.org/abs/2602.15922) | World Action Models are Zero-shot Policies (DreamZero) | adjacent 2026 work on world-action models for robotics | 5.7 MB | **images downsampled** (9.1 → 5.7 MB) |
| `2605.30263_minWM_Causal_Forcing.pdf` | [2605.30263](https://arxiv.org/abs/2605.30263) | minWM: full-stack open framework for real-time interactive world models | adjacent 2026 work (causal forcing) | 2.9 MB | **images downsampled** (5.9 → 2.9 MB) |
| `2606.11187_Next_Forcing.pdf` | [2606.11187](https://arxiv.org/abs/2606.11187) | Next Forcing: Causal World Modeling with Multi-Chunk Prediction | adjacent 2026 work | 1.9 MB | untouched |

**About the downsampled PDFs.** To keep the whole archive under the workspace size limit, the eight PDFs marked above were rewritten in place with PyMuPDF
(`Document.rewrite_images(dpi_threshold=130, dpi_target=110, quality=60)` followed by `save(garbage=4, deflate=True)`). Only embedded raster images were
re-encoded; all text, vector graphics, equations, links and page counts are unchanged (verified: every file opens with its full page count). If you need
print-quality figures, re-download the original from the arXiv link (`https://arxiv.org/pdf/<id>`).

Citation counts: Semantic Scholar rate-limited (HTTP 429) every attempt; OpenAlex reported `cited_by_count: 0` for the DOI record, which is clearly stale for this paper —
treat citation numbers as unavailable.
