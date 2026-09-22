# Dreamer 4 — deep-dive presentation

* `Dreamer4_Deep_Dive.pptx` — 43 slides (16:9), speaker notes on every slide. Mixed technical audience, 45–60 min.
  Slides 10–11 ("How the pieces fit together") show the whole stack on one system diagram: data → causal tokenizer → the shared block-causal
  transformer with its inputs/outputs and the phase that trains each output, the imagination loop, and the evaluation path (`make_stack_diagram.py`;
  the full one-page version is `stack_diagram.svg` next to this file and `../dreamer4_stack_diagram.png`; in the GitHub mirror both live in `presentation/`).
  Part 2 has a three-slide primer (flow matching, diffusion forcing, shortcut models) and schematic slides for the causal tokenizer and the
  interactive dynamics model, each with a purpose-built diagram (`make_diagrams.py`; illustrations built from one archived frame, not model internals).
  Visual system (v2): flat editorial layout — one ink colour + one accent, hairlines instead of boxes, margin notes, numbered columns,
  booktabs-style tables, charts restyled in the deck's font/palette, split title slide with model-generated frames. Every slide was
  rendered (LibreOffice → PDF → PNG) and checked for overflow/overlap.
* `Dreamer4_Deep_Dive.pdf` — the same 43 slides as a PDF (rendered with LibreOffice 26.2 using Carlito, the metric-compatible Calibri substitute; images capped at 200 dpi; speaker notes are not included in the PDF).
* `stack_diagram.svg` (+ `stack_diagram.png` in the GitHub mirror, `../dreamer4_stack_diagram.png` here) — the one-page "how the parts of Dreamer 4 fit together" system diagram (standalone version of slides 10–11).
* `Dreamer4_Deep_Dive_speaker_notes.md` — the notes as plain text.
* `build_deck.py` — regenerates the deck (python-pptx). `make_assets.py` recreates the `assets/` folder it needs
  (figures rendered from the paper PDF / arXiv HTML, frames from the archived official clips, matplotlib charts); `make_charts.py`, `make_diagrams.py` and `make_stack_diagram.py` are called by it.
  The assets folder was removed after building to save workspace space — run `python3 make_assets.py && python3 build_deck.py` to rebuild.

Sources: arXiv 2509.24527, the project page danijar.com/project/dreamer4, and the research report / resource archive in `../dreamer4_resources`
(mirrored at https://github.com/HarmannBitte/Dreamer-4, where this folder lives under `presentation/`). Figures © the authors, reproduced for discussion.
