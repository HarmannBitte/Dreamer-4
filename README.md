# Dreamer 4 resource archive — manifest

Local archive of (almost) every source cited in `dreamer4_research_report.md` (copy included here; original at `/home/user/dreamer4_research_report.md`).
Everything was fetched on **2026-09-20** from the sandbox in Frankfurt. Total size ≈ 112 MB / ~1,370 files.

**Presentation.** `presentation/` holds the final ~30-minute talk (world-models framing, `Dreamer4_Final.pptx`) and a 50-slide deep dive on the paper for a mixed technical audience (45–60 min): [`Dreamer4_Deep_Dive.pptx`](presentation/Dreamer4_Deep_Dive.pptx) (with speaker notes), [`Dreamer4_Deep_Dive.pdf`](presentation/Dreamer4_Deep_Dive.pdf), the [speaker notes](presentation/Dreamer4_Deep_Dive_speaker_notes.md) as Markdown, the python-pptx scripts that regenerate it, and a one-page system diagram of the whole stack (`presentation/stack_diagram.png`). `diagrams/` holds three companion graphics in the same style: the OpenAI VPT stack, a stack-by-stack comparison of the five Minecraft world models of Table 1, and Google DeepMind's Genie 3 (stated vs. inferred vs. undisclosed); the latter two also appear in the deck (slides 28–29 and 41–42). `paper_figures/` holds every figure and table of the paper cropped from the PDF (plus the 449 raw embedded images) with a caption index.

**Media?** See **`MEDIA_INDEX.md`** — a complete list of every video, audio file, image and large artefact (archived or listed-only, with sizes and URLs).

**Scope decision.** Text, code, PDFs, metadata and thumbnails were archived. Multi-GB artefacts (model checkpoints, datasets, full videos, podcast audio,
a 2.8 GB Waymo cache) were **not** downloaded; their exact URLs and sizes are recorded so you can pull them yourself. Eight background-paper PDFs had their
embedded images downsampled to fit the workspace size cap (text/vectors untouched, details in `papers/README.md`).

```
dreamer4_resources/
├── README.md                      ← this manifest
├── MEDIA_INDEX.md                 ← complete media list (videos/audio/images/weights; archived + listed-only)
├── dreamer4_research_report.md    ← the research report (copy)
├── _fetch_articles.py             ← provenance: script that produced articles/ (URL list + extraction settings)
├── papers/        14 arXiv PDFs + Dreamer 4 HTML/abstract/BibTeX/API metadata     (35 MB)  → papers/README.md
├── media/         official Dreamer 4 clips/figure from danijar.com (62 files) + tweet video (28 MB)  → MEDIA_INDEX.md §1–2
├── repos/         14 GitHub repositories, shallow snapshots, .git removed         (40 MB)  → table below + repos/PRUNED_FILES.txt
├── articles/      48 web pages: raw HTML/JSON + Markdown extraction               (8.8 MB) → articles/README.md, articles/_manifest.json
├── community/     Hacker News thread + 4 Reddit threads (JSON + Markdown)         (0.3 MB) → table below
├── videos/        oEmbed metadata + thumbnails for 7 YouTube videos               (0.1 MB) → videos/README.md
├── huggingface/   model/dataset cards + API file listings for 4 models, 4 datasets (0.7 MB) → huggingface/README.md
├── paper_figures/ all 11 figures + 8 tables of the paper as images, raw embedded images, caption index (6.3 MB) → paper_figures/README.md
├── presentation/  final 30-min talk + 50-slide deep-dive deck (.pptx with speaker notes, .pdf, notes .md, build scripts, stack diagram) (7.9 MB) → presentation/README.md (versions/ keeps every earlier PDF render, v1–v5)
└── diagrams/      companion stack graphics: VPT, Minecraft world-model comparison, Genie 3 (PNG + SVG) → diagrams/README.md
```

---

## 1. papers/ (primary literature)

See `papers/README.md` for the full table (file → arXiv id → role in the report → whether images were downsampled).
Core: **2509.24527 Dreamer 4** (Hafner, Yan, Lillicrap, 29 Sep 2025 — PDF v1 untouched, plus arXiv HTML render, abstract page, BibTeX, arXiv-API XML, OpenAlex JSON).
Ingredients/background: DreamerV3, APD, Diffusion Forcing, Shortcut Models, MAETok, VPT, MineWorld. Follow-ups/adjacent: Jasmine, Hansen multitask WMs,
Hansen & Wang hallucination (MMBench2), DreamZero, minWM, Next Forcing.

## 2. repos/ (GitHub source snapshots)

`git clone --depth 1` on 2026-09-20 13:35 UTC; `.git/` deleted afterwards; each folder has a `GIT_INFO.txt` (remote, branch, commit hash, commit date, subject).
27 media/data files > 1 MB were deleted after cloning and are listed with sizes + GitHub URLs in `repos/PRUNED_FILES.txt`.

| Folder | Upstream | Branch @ commit (date) | Size | What it is (see report §"Ecosystem") | Pruned |
|---|---|---|---|---|---|
| `next-state_open-dreamer` | https://github.com/next-state/open-dreamer | main @ `797e41f` (2026-07-26) | 2.0 MB | Open Dreamer — JAX/Flax-NNX reproduction of the world-model half (1.6 B Minecraft WM, training recipe, browser demo); Reactor-sponsored | `dreamer/fvd/i3d_pretrained_400.npz` (48.6 MB), site SVG/media |
| `reactor-team_open-dreamer` | https://github.com/reactor-team/open-dreamer | main @ `829263d` (2026-07-25) | 0.3 MB | minimal local rollout harness for Open Dreamer (all-rights-reserved licence) | — |
| `lucidrains_dreamer4` | https://github.com/lucidrains/dreamer4 | main @ `f1fbbb5` (2026-09-03) | 1.3 MB | PyTorch library re-implementation (400+ commits, toy envs, many non-paper additions) | — |
| `nicklashansen_dreamer4` | https://github.com/nicklashansen/dreamer4 | main @ `b8abafb` (2026-07-09) | 9.0 MB | PyTorch Dreamer 4 for DMControl (tokenizer + dynamics + BC/RL); superseded by mmbench2 | task GIFs > 1 MB |
| `nicklashansen_mmbench2` | https://github.com/nicklashansen/mmbench2 | main @ `3dda6ea` (2026-07-09) | 8.3 MB | code for Hansen & Wang 2026 (hallucination predictors, coverage-aware sampling, 50-trajectory adaptation) | GIFs > 1 MB |
| `edwhu_dreamer4-jax` | https://github.com/edwhu/dreamer4-jax | main @ `753d650` (2026-07-24) | 1.2 MB | educational JAX implementation | — |
| `vijayabhaskar-ev_dreamer_v4` | https://github.com/vijayabhaskar-ev/dreamer_v4 | main @ `c680182` (2026-09-10) | 2.7 MB | full 3-phase pipeline with closed-loop evaluation (RL +5.9 pts over BC; Phase-2 seed variance; reward-hacking findings) | — |
| `IamCreateAI_Dreamerv4-MC` | https://github.com/IamCreateAI/Dreamerv4-MC | main @ `166d7ca` (2026-01-31) | 4.6 MB | Dreamer-MC: 1.7 B Minecraft world model, inference only; weights on HF | demo media > 1 MB |
| `4ku_dreamer4` | https://github.com/4ku/dreamer4 | master @ `3489e13` (2026-09-19) | 0.5 MB | independent PyTorch re-implementation (Minecraft/VPT data) | — |
| `HKimiwada_Dreamer4` | https://github.com/HKimiwada/Dreamer4 | main @ `27e5837` (2026-02-11) | 2.0 MB | student re-implementation with inference results | six result `.mp4` (≈83 MB) |
| `vFf0621_Dreamer4-torch` | https://github.com/vFf0621/Dreamer4-torch | main @ `2f0d7c7` (2026-07-27) | 0.1 MB | small PyTorch port | — |
| `skr3178_DreamerV4` | https://github.com/skr3178/DreamerV4 | **pretrained_tokenizer** @ `3ee81d8` (2026-01-29) | 2.8 MB | abandoned attempt using a pretrained (Cosmos) tokenizer — default branch is this one | — |
| `p-doom_jasmine` | https://github.com/p-doom/jasmine | main @ `420859b` (2025-10-31) | 0.5 MB | Jasmine JAX world-modeling codebase (arXiv 2510.27002) | — |
| `chrisgao99_dreamer4` | https://github.com/chrisgao99/dreamer4 | main @ `06ae069` (2026-09-14) | 5.6 MB | fork of nicklashansen/dreamer4 adapted to **Waymo / PufferDrive driving scenes** (not Minecraft) | `waymo/cache/` (2.8 GB) and `waymo/eval_results/` (107 MB) — see `chrisgao99_dreamer4/waymo/PRUNED_DIRS.txt`; 12 README assets byte-identical to nicklashansen_dreamer4 removed (`DEDUPED_FILES.txt`) |

Deliberately **excluded**: `softengg-manoj/dreamer4` — a spam/"installer" mirror of lucidrains' repo, not an implementation.

## 3. articles/ (48 web pages)

Full index with per-URL status in `articles/README.md` (generated from `articles/_manifest.json`). Highlights:

* Official: danijar.com/project/dreamer4 (+ short URL). Talks: **TalkRL E73 full transcript** (`talkrl_e73_full_transcript.md`, 85 KB).
* Reproductions/follow-ups: Open Dreamer blog ("How to train a frontier world model"), Dreamer-MC blog, MMBench2 project page, Jasmine page, deepwiki on edwhu, Zenodo DOI page of Open Dreamer.
* Press: TechXplore (Oct 2025), InfoQ (Oct 2025), implicator.ai (Feb 2026), **MarkTechPost on Open Dreamer (Jul 2026)**, MIT Technology Review on Hafner's departure (Sep 2026), Analytics Insight (Sep 2026), 36kr, Crypto Briefing.
* Explainers: arxiviq (paywalled preview), Pith machine review (**AI-generated, incl. synthetic "author responses"**), EmergentMind (paper + topic), alphaXiv overview, Harold Benoit's notes, Medium (S. Suzuki, published 25 Dec 2025).
* Rendered GitHub landing pages for 9 repos and HF web pages for 5 model/dataset repos; X profile + the two single tweets that could be retrieved (announcement 1973072288351396320, TalkRL 1987968769462067218) as syndication-API JSON.

## 4. community/

| File | Source | Content |
|---|---|---|
| `hn_story_45923326_full_thread.{json,md}` | https://news.ycombinator.com/item?id=45923326 (Algolia API) | 75-comment HN thread on Hafner leaving DeepMind; the report's cited comment **45923945** is inside it (there is no large dedicated Dreamer 4 HN thread) |
| `hn_search_dreamer4_stories.json` | Algolia HN search "dreamer 4" | list of all HN stories mentioning Dreamer 4 |
| `reddit_reinforcementlearning_1nu4cub.{json,md}` | r/reinforcementlearning (score 30, 5 comments) | announcement mirror thread |
| `reddit_mlscaling_1nvfkgu.{json,md}` | r/mlscaling (29, 1) | announcement mirror thread |
| `reddit_singularity_1nv4zna.{json,md}` | r/singularity (241, 20) | announcement mirror thread |
| `reddit_accelerate_1nvbfm1.{json,md}` | r/accelerate (155, 51) | announcement mirror thread |

Reddit was archived through the **Pullpush** archive API because reddit.com returns HTTP 403 to every route tried from this sandbox; scores/comment counts are as of the Pullpush snapshot, not live.

## 5. media/ — official first-party media (new)

The project page embeds 62 assets under `https://danijar.com/asset/dreamer4/`: the teaser video, the diamond-challenge benchmark figure, 6 imagination-training rollouts (gather wood / mine stone),
51 human-interaction clips (17 tasks × Dreamer 4 / Lucid-v1 / Oasis — the qualitative side of Table 1) and 3 real-world robot-arm counterfactual clips. All are archived in `media/official_danijar_com/`
(25.6 MB, md5 + source URL per file in `media/_media_manifest.json`), plus the 1280×720 video of the announcement tweet in `media/x_twitter/`. Task-name mapping and everything *not* archived
(Dreamer-MC, Open Dreamer and MMBench2 page videos, podcasts, YouTube, TechXplore video, weights) is in `MEDIA_INDEX.md`.

## 6. videos/ and 7. huggingface/

See `videos/README.md` (7 YouTube videos: title, channel, URL, thumbnail; no downloads/transcripts possible — yt-dlp bot-blocked, caption endpoint empty)
and `huggingface/README.md` (4 checkpoint repos totalling 12 GB and 4 datasets totalling 3.7 TB — cards + file listings only).

---

## Not archived (and where to get it)

| Item | Why skipped | URL |
|---|---|---|
| Model checkpoints (Dreamer-MC 4.2 GB, nicklashansen/dreamer4 0.8 GB, mmbench2-models 4.3 GB, vijayabhaskarev 2.9 GB) | size | see `huggingface/README.md` |
| Datasets (nicklashansen/dreamer4 31 GB, mmbench2 114 GB, VPT contractor mirrors 1.7–1.9 TB) | size | see `huggingface/README.md` |
| 7 YouTube videos + captions (+5 third-party coverage videos) | size + YouTube bot-wall | `videos/README.md`, `MEDIA_INDEX.md` §3 |
| Dreamer-MC (40 MB), Open Dreamer (13 MB) and MMBench2 (14 MB) project-page videos/figures; TechXplore video; alphaXiv AI podcast | size budget — official Dreamer 4 media was prioritised | `MEDIA_INDEX.md` §5–8 |
| TalkRL E73 audio | size (transcript is archived) | https://media.transistor.fm/e440a692/bfc0657e.mp3 |
| 27 repo media/data files > 1 MB, `chrisgao99` Waymo cache/eval results | size | `repos/PRUNED_FILES.txt`, `repos/chrisgao99_dreamer4/waymo/PRUNED_DIRS.txt` |
| awesomepapers.org page | HTTP 429 every attempt, no Wayback copy; low value | https://awesomepapers.org/ (search 2509.24527) |
| Full X/Twitter announcement thread | not retrievable without login; two single tweets saved | https://x.com/danijarh/status/1973072288351396320 |
| Official Dreamer 4 code / weights | **do not exist** — DeepMind never released them (Hafner: "probably not") | — |

## Fetch problems & workarounds (for reproducibility)

* techxplore.com → 403; used Wayback Machine snapshot `20260918064016` (`web.archive.org/web/<ts>id_/<url>`; body arrives gzip-encoded on disk).
* pith.science and medium.com → 403 for `requests`/`curl` regardless of User-Agent, no Wayback snapshots; text obtained through the assistant's page-reader tool and saved as Markdown (no raw HTML for these two).
* reddit.com → 403 on web, `.json`, api.reddit.com, r.jina.ai proxy, redlib (429) and safereddit (JS challenge); Pullpush worked.
* YouTube → oEmbed + thumbnail CDN only; watch pages did not expose `ytInitialPlayerResponse` (no descriptions/durations), yt-dlp blocked, `api/timedtext` empty.
* Semantic Scholar API → 429 (citation counts unavailable); OpenAlex returns 0 citations for the DOI record (stale).
* PDF compression: ghostscript/qpdf/mutool not installable in the sandbox; PyMuPDF `rewrite_images` used instead (117 MB → 35 MB for `papers/`).

## Content warnings

* `articles/explainer_pith_review.md` is machine-generated review text; the "author responses" in it are fabricated by the site, not statements by Hafner/Yan/Lillicrap.
* `articles/explainer_medium_suzuki_intuitive_understanding.md` contains at least one factual error (DreamerV3 parameter count).
* Star counts / download numbers quoted in the report were read on 2026-09-20 and will drift; the HF `downloads` field is a rolling 30-day figure.
