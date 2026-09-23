# Dreamer 4 — deep-dive presentation

* `Dreamer4_Deep_Dive.pptx` — 50 slides (16:9), speaker notes on every slide. Mixed technical audience, 50–65 min.
  v6 (Sep 2026) added slide 4, "The paper in three minutes: the official video": the YouTube video *Dreamer 4 | Diamonds from Offline Experience* (2:55, essentially Figure 1 in motion) as a
  click-through thumbnail with QR code, plus the official 10-second teaser from danijar.com embedded as an offline-playable clip (`assets/video/`, `dreamer4_resources/media/`).
  Link chips were added to the play-test frames (all 51 project-page clips), the diamond-results slide (the four uncut 60-minute evaluation episodes) and the Figure 1 slide.
  v5 (Sep 2026) added six slides (numbers as of v6): 9 (the 12-milestone tech tree with its tool gates, Dreamer 4's time-to-item and the success-rate fall-off of VPT / VLA / Dreamer 4, `make_tech_tree.py`),
  10 (hours of data and interaction behind VPT, Dreamer 3 and Dreamer 4, Table 3), 28–29 (the Table 1 world models compared stack by stack, `make_wm_stack_comparison.py --deck`)
  and 41–42 (Genie 3 in context, crops of `make_genie3_stack_diagram.py`). A fact-check of an external brainstorm against the paper is in `brainstorm_factcheck.md`.
  Slides 13–14 ("How the pieces fit together") show the whole stack on one system diagram: data → causal tokenizer → the shared block-causal
  transformer with its inputs/outputs and the phase that trains each output, the imagination loop, and the evaluation path (`make_stack_diagram.py`;
  the full one-page version is `stack_diagram.svg` next to this file and `../dreamer4_stack_diagram.png`; in the GitHub mirror both live in `presentation/`).
  Part 2 has a three-slide primer (flow matching, diffusion forcing, shortcut models) and schematic slides for the causal tokenizer and the
  interactive dynamics model, each with a purpose-built diagram (`make_diagrams.py`; illustrations built from one archived frame, not model internals).
  Visual system (v2): flat editorial layout — one ink colour + one accent, hairlines instead of boxes, margin notes, numbered columns,
  booktabs-style tables, charts restyled in the deck's font/palette, split title slide with model-generated frames. Every slide was
  rendered (LibreOffice → PDF → PNG) and checked for overflow/overlap.
* `Dreamer4_Deep_Dive.pdf` — the same 50 slides as a PDF (the embedded teaser is replaced by its poster frame; the YouTube links are live) (rendered with LibreOffice 26.2 using Carlito, the metric-compatible Calibri substitute; images capped at 150 dpi, JPEG quality 82; speaker notes are not included in the PDF).
* `make_vpt_stack_diagram.py` → `../vpt_stack_diagram.png` / `.svg` (GitHub mirror: `diagrams/`) — the same kind of system diagram for OpenAI's VPT (Baker et al. 2022), for comparison; not used in the deck.
* `make_tech_tree.py` → `assets/diag_tech_tree.png`, `assets/chart_agent_cost.png` — the two graphics of slides 9–10 (Tables 3, 7, 8).
* `make_wm_stack_comparison.py` → `../minecraft_world_models_stack.png` / `.svg` (GitHub mirror: `diagrams/`) — stack-by-stack comparison of the five Minecraft world models of Table 1 (MineWorld, Lucid-v1, Oasis small/large, Dreamer 4); with `--deck` it writes the two halves used on slides 28–29.
* `make_genie3_stack_diagram.py` → `../genie3_stack_diagram.png` / `.svg` (GitHub mirror: `diagrams/`) — the same kind of system diagram for Google DeepMind's Genie 3 (no paper exists: stated facts vs. amber-marked inferences from the Genie 2 recipe vs. undisclosed items; SIMA 2 agent loop; Project Genie); its two rows are cropped onto slides 41–42.
* `stack_diagram.svg` (+ `stack_diagram.png` in the GitHub mirror, `../dreamer4_stack_diagram.png` here) — the one-page "how the parts of Dreamer 4 fit together" system diagram (standalone version of slides 13–14).
* `Dreamer4_Deep_Dive_speaker_notes.md` — the notes as plain text (written by `build_deck.py`).
* `versions/` — every earlier PDF render of the deck (v1 39 slides, v2 39, v3 41, v4 43 with its pptx and notes, v5 49) plus a table of what changed in each version; see `versions/README.md`.
* `build_deck.py` — regenerates the deck (python-pptx). `make_assets.py` recreates the `assets/` folder it needs
  (figures rendered from the paper PDF / arXiv HTML, frames from the archived official clips, matplotlib charts); `make_charts.py`, `make_diagrams.py`, `make_stack_diagram.py`, `make_tech_tree.py`, `make_wm_stack_comparison.py --deck` and `make_genie3_stack_diagram.py` are called by it.
  The assets folder was removed after building to save workspace space — run `python3 make_assets.py && python3 build_deck.py` to rebuild (`NO_MOVIE=1 OUT=/tmp/x.pptx python3 build_deck.py` writes the poster-only variant used for the PDF render; `assets/video/` holds the thumbnail, QR codes and teaser poster).

Sources: arXiv 2509.24527, the project page danijar.com/project/dreamer4, and the research report / resource archive in `../dreamer4_resources`
(mirrored at https://github.com/HarmannBitte/Dreamer-4, where this folder lives under `presentation/`). Figures © the authors, reproduced for discussion.
