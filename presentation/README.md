# Dreamer 4 — deep-dive presentation

* `Dreamer4_Deep_Dive.pptx` — 39 slides (16:9), speaker notes on every slide. Mixed technical audience, 45–60 min.
  Visual system (v2): flat editorial layout — one ink colour + one accent, hairlines instead of boxes, margin notes, numbered columns,
  booktabs-style tables, charts restyled in the deck's font/palette, split title slide with model-generated frames. Every slide was
  rendered (LibreOffice → PDF → PNG) and checked for overflow/overlap.
* `Dreamer4_Deep_Dive.pdf` — the same 39 slides as a PDF (rendered with LibreOffice 26.2 using Carlito, the metric-compatible Calibri substitute; speaker notes are not included in the PDF).
* `Dreamer4_Deep_Dive_speaker_notes.md` — the notes as plain text.
* `build_deck.py` — regenerates the deck (python-pptx). `make_assets.py` recreates the `assets/` folder it needs
  (figures rendered from the paper PDF / arXiv HTML, frames from the archived official clips, matplotlib charts); `make_charts.py` is called by it.
  The assets folder was removed after building to save workspace space — run `python3 make_assets.py && python3 build_deck.py` to rebuild.

Sources: arXiv 2509.24527, the project page danijar.com/project/dreamer4, and the research report / resource archive in the repository root
(mirrored at https://github.com/HarmannBitte/Dreamer-4, where this folder lives under `presentation/`). Figures © the authors, reproduced for discussion.
