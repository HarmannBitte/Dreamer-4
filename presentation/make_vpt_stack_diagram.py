"""Companion to make_stack_diagram.py: the same kind of system diagram for OpenAI's VPT (Baker et al. 2022, arXiv 2206.11795 —
"Video PreTraining: Learning to Act by Watching Unlabeled Online Videos"). Facts from the paper (Sections 3–4, Appendices A–H).
Writes /home/user/vpt_stack_diagram.{png,svg}. Not part of the deck build."""
import glob, os
import matplotlib; matplotlib.use("Agg")
from matplotlib import font_manager
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle
for f in glob.glob(os.path.expanduser("~/.fonts/Carlito-*.ttf")) + glob.glob("/usr/share/fonts/truetype/crosextra/Carlito-*.ttf"):
    font_manager.fontManager.addfont(f)
FAM = "Carlito" if any(f.name == "Carlito" for f in font_manager.fontManager.ttflist) else "DejaVu Sans"
NAVY = "#14213D"; BLUE = "#2A56D6"; INK = "#1F2937"; GREY = "#6B7280"; MUTED = "#9AA3B2"; RULE = "#D3D8E2"; PANEL = "#F3F5F8"; SKY = "#E3EAFB"; DEEP = "#DCE3F0"
GREEN = "#1B7F5C"; MINT = "#E1F2EB"          # one extra tint for the "real environment" parts, which is exactly what Dreamer 4 does not have
plt.rcParams.update({"font.family": FAM, "text.color": INK, "mathtext.fontset": "custom", "mathtext.rm": FAM, "mathtext.it": FAM + ":italic", "mathtext.bf": FAM + ":bold"})
F = 1.1; YMIN = 2.5

def draw(out, title=None):
    top = 60 if title else 56.25
    fig = plt.figure(figsize=(13.333, 13.333 * (top - YMIN) / 100), dpi=200)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 100); ax.set_ylim(YMIN, top); ax.axis("off")
    if title:
        ax.text(1.2, 58.5, title, fontsize=15 * F, fontweight="bold", color=NAVY, va="center")
        ax.text(98.8, 58.5, "after Baker et al. (OpenAI, 2022), arXiv 2206.11795 · schematic drawn for the Dreamer 4 deck, not from the paper", fontsize=8.5 * F, color=GREY, va="center", ha="right")

    def box(x, y, w, h, fc="white", ec=RULE, lw=1.0, ls="-", z=1):
        ax.add_patch(Rectangle((x, y), w, h, fc=fc, ec=ec, lw=lw, ls=ls, zorder=z))
    def label(x, y, s, size=10.5, color=NAVY, bold=True, ha="left", va="top", **kw):
        ax.text(x, y, s, fontsize=size * F, color=color, fontweight=("bold" if bold else "normal"), ha=ha, va=va, **kw)
    def body(x, y, s, size=8.4, color=INK, ha="left", va="top", ls=1.32, **kw):
        ax.text(x, y, s, fontsize=size * F, color=color, ha=ha, va=va, linespacing=ls, **kw)
    def chip(x, y, w, h, s, fc=PANEL, ec=RULE, color=INK, size=8.0, bold=False, lw=0.9, ls=1.2):
        box(x, y, w, h, fc=fc, ec=ec, lw=lw, z=2); ax.text(x + w / 2, y + h / 2, s, fontsize=size * F, color=color, ha="center", va="center", fontweight=("bold" if bold else "normal"), zorder=3, linespacing=ls)
    def arrow(p, q, color=INK, lw=1.2, rad=0.0, ls="-", ms=10, z=4):
        ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=ms, color=color, lw=lw, linestyle=ls, connectionstyle=f"arc3,rad={rad}", zorder=z))
    def route(pts, color=INK, lw=1.1, ls="-", ms=10):
        xs, ys = zip(*pts); ax.plot(xs, ys, color=color, lw=lw, ls=ls, zorder=3, solid_capstyle="round")
        (x0, y0), (x1, y1) = pts[-2], pts[-1]; arrow((x0, y0), (x1, y1), color=color, lw=lw, ms=ms)
    def numeral(x, y, n):
        ax.text(x, y, f"{n:02d}", fontsize=13 * F, color=BLUE, fontweight="bold", ha="left", va="top")
    def small(x, y, s, color=GREY, ha="center", va="top", size=7.4):
        ax.text(x, y, s, fontsize=size * F, color=color, ha=ha, va=va)

    yA0, yA1 = 30, 55
    # ------------------------------------------------------------------ 01 web video
    box(1, 42, 19, yA1 - 42); numeral(2, 54.3, 1); label(2, 51.6, "Web video — no actions")
    body(2, 49.7, "keyword search ('minecraft survival for\nbeginners', …) → ~270k h of video\n\nclean-segment filter: CLIP RN50x64 + SVM\ntrained on 8,800 frames contractors marked\nclean / unclean (face cams, logos, mods …)\n→ web_clean ≈ 70k h", size=7.6, ls=1.28)
    # ------------------------------------------------------------------ 02 contractor data
    box(1, yA0, 19, 10.5); numeral(2, 39.9, 2); label(2, 37.3, "Contractor data — with actions")
    body(2, 35.4, "~2k h (1,962 h) of paid play, keys +\nmouse logged at 20 Hz; 640×360 video,\nmodels see 128×128 · ≈ $40k\nlater: contractor_house, 420 h of\n'build a basic house in 10 minutes'", size=7.5, ls=1.26)
    # ------------------------------------------------------------------ 03 IDM
    box(23.5, yA0, 23, 12.5); numeral(24.5, 41.8, 3); label(24.5, 39.2, "Inverse dynamics model (IDM) · 0.5 B")
    chip(25, 34.6, 20, 3.4, "non-causal: 3-D conv (temporal kernel 5) → ResNet\n→ unmasked transformer layers", fc=DEEP, size=7.6)
    chip(25, 30.9, 20, 3.2, "sees 128 frames, past and future →\nkeys + mouse at every frame", fc=PANEL, size=7.6)
    # ------------------------------------------------------------------ 04 foundation model
    box(23.5, 44.5, 23, 10.5); numeral(24.5, 54.3, 4); label(24.5, 51.6, "Pseudo-labelling")
    body(24.5, 49.8, "the IDM trained on 2k h of contractor data labels\nall 70k h of web_clean: 90.6 % keypress accuracy,\nR² 0.97 on mouse (held-out contractor data);\n100 h of labels already gets most of the way", size=7.6, ls=1.28)
    box(50, yA0, 30.5, yA1 - yA0, ec=NAVY, lw=1.3); numeral(51, 54.3, 5)
    label(51, 51.5, "VPT foundation model · 0.5 B — causal BC policy")
    body(51.3, 49.4, "inputs", size=7.6, color=GREY)
    chip(51.3, 45.9, 9.6, 2.6, "frame t, 128×128", fc=DEEP, size=7.7)
    chip(51.3, 42.9, 9.6, 2.6, "memory of past\nframes (Transformer-XL)", fc=PANEL, size=7.2)
    body(62.2, 49.4, "ResNet image stack →\ncausally masked transformer\nlayers (no future frames)\n\nBC on the IDM-labelled web_clean:\n30 epochs, ~9 days on 720 V100\nframes with the null action\n(35 % of human play) dropped", size=7.4, ls=1.28)
    body(51.3, 41.5, "outputs, per frame", size=7.6, color=GREY)
    chip(51.3, 36.9, 14.4, 3.2, "key-combination head: 8,461-way\ncategorical (+ 'move mouse?')", fc=BLUE, ec=BLUE, color="white", size=7.6, bold=True)
    chip(66.2, 36.9, 13.3, 3.2, "camera head: 121-way\n(11 × 11 foveated mouse bins)", fc=BLUE, ec=BLUE, color="white", size=7.6, bold=True)
    body(51.3, 35.9, "zero-shot: chops logs, crafts planks and crafting tables (0.19 per hour vs 5.44\nfor contractors), swims, pillar-jumps, hunts, loots villages — but nothing past\nthe crafting table", size=7.3, color=GREY, ls=1.28)
    # ------------------------------------------------------------------ 06 recipe + contrast column
    box(83, yA0, 16, yA1 - yA0, fc=PANEL, ec=PANEL); numeral(84, 54.3, 6); label(84, 51.5, "The recipe")
    body(84, 49.4, "1  collect and filter web video\n2  train a non-causal IDM on\n    ~2k h of contractor data\n3  let the IDM label 70k h\n    of web video\n4  behaviour-clone a causal\n    policy on the pseudo-labels\n5  fine-tune: BC, then RL", size=7.6, ls=1.28)
    label(84, 39.6, "Where Dreamer 4 differs", size=8.6)
    body(84, 37.8, "· actions for video: IDM labels vs.\n  none needed ('no action' token)\n· RL: 16.8 B real game frames vs.\n  zero — RL inside the world model\n· data: 70k h web + 2k h contractor\n  vs. 2.5k h contractor only\n· both keep a KL to the BC policy", size=7.3, ls=1.28)
    # ------------------------------------------------------------------ arrows, row A
    route([(20, 49.2), (23.5, 49.2)]); small(21.75, 49.6, "70k h", va="bottom", size=7)
    route([(20, 35.2), (23.5, 35.2)]); small(21.75, 35.6, "2k h", va="bottom", size=7)
    route([(35, 42.5), (35, 44.5)], color=NAVY); small(36.2, 43.5, "IDM → labels", color=NAVY, ha="left", va="center", size=7)
    route([(46.5, 49.2), (50, 49.2)], color=NAVY); small(48.25, 49.6, "70k h\nlabelled", color=NAVY, va="bottom", size=6.8)
    route([(6, yA0), (6, 25.5)], color=MUTED, ls=(0, (3, 2))); small(7, 27.8, "contractor_house", color=GREY, size=6.8, ha="left", va="center")
    route([(55, yA0), (55, 27.6), (24, 27.6), (24, 25.5)], color=NAVY); small(39.5, 27.95, "foundation model → BC fine-tuning", color=NAVY, va="bottom", size=7)
    route([(76, yA0), (76, 27.6), (88, 27.6), (88, 25.5)], color=MUTED, ls=(0, (3, 2))); small(82, 27.95, "any of the policies", color=GREY, va="bottom", size=6.8)

    # ------------------------------------------------------------------ 07 BC fine-tuning
    yB0, yB1 = 4, 25.5
    box(1, yB0, 30, yB1 - yB0); numeral(2, 24.8, 7); label(2, 22.0, "BC fine-tuning to the early game")
    body(2, 19.8, "same objective, narrower data:\n\nearlygame_keyword — web_clean videos titled\n'new world', 'let's play episode 1', …, IDM labels\n→ refines skills the model already has\n\ncontractor_house — 420 h, real labels\n→ 213× more crafting tables, 59× more planks,\n7× more logs; wooden and stone tools appear\n\nthe better the foundation model, the better\nthe fine-tuned model (data-scaling study, Fig. 8)", size=8.0, ls=1.32)
    arrow((31, 17.4), (34.5, 17.4), color=BLUE); small(32.75, 17.9, "init", color=BLUE, va="bottom", size=6.8)
    # ------------------------------------------------------------------ 08 RL fine-tuning
    box(33.5, yB0, 39.5, yB1 - yB0, ec=GREEN, lw=1.2); numeral(34.5, 24.8, 8); label(34.5, 22.0, "RL fine-tuning in the real game — PPG (a PPO variant)", color=GREEN)
    nodes = [("early-game BC\nmodel as init\n(≈ 248 M version)", SKY, BLUE), ("play Minecraft\n10-min episodes,\n12,000 steps at 20 Hz", MINT, GREEN), ("reward per item on the\ndiamond-pickaxe path\n(tiers 1 → 8)", PANEL, RULE), ("PPG update\n+ ρ · KL(π_pretrained ‖ π_θ)\nto the frozen prior", SKY, BLUE)]
    for i, (s, fc, ec) in enumerate(nodes):
        chip(34.5 + i * 9.55, 14.6, 8.6, 5.6, s, fc=fc, ec=ec, size=7.3)
        if i < 3: arrow((43.1 + i * 9.55, 17.4), (44.05 + i * 9.55, 17.4), lw=1.1, ms=9)
    route([(67.4, 14.6), (67.4, 13.3), (48.4, 13.3), (48.4, 14.6)], color=BLUE, ls=(0, (3, 2)), ms=9)
    small(57.9, 12.95, "updated policy plays the next episodes — 1.4 M episodes in total", color=BLUE, size=7)
    body(34.5, 10.8, "16.8 B real game frames · ~6 days on 80 GPUs + 56,719 CPUs (mostly Minecraft instances)\nwithout the KL term progress stalls after ~100k episodes (skills forgotten);\nRL from a random init gets almost no reward — the behavioural prior is what makes exploration work\nresult: every item up to the diamond pickaxe at human level; a diamond pickaxe in 2.5 % of the 10-min episodes", size=7.3, ls=1.3)
    # ------------------------------------------------------------------ 09 acting
    box(76, yB0, 23, yB1 - yB0); numeral(77, 24.8, 9); label(77, 22.0, "Acting / evaluation")
    steps = ["frame\n128×128", "ResNet +\ntransformer\n(memory)", "key-combo +\ncamera heads", "keys + mouse\nat 20 Hz"]
    for i, s in enumerate(steps):
        chip(77 + i * 5.4, 15.6, 4.8, 4.6, s, fc=(MINT if i == 3 else PANEL), ec=(GREEN if i == 3 else RULE), size=6.9)
        if i < 3: arrow((81.8 + i * 5.4, 17.9), (82.4 + i * 5.4, 17.9), lw=1.0, ms=8)
    route([(97, 15.6), (97, 14.4), (79.4, 14.4), (79.4, 15.6)], color=MUTED, ls=(0, (3, 2)), ms=9)
    small(88.2, 14.0, "the game returns the next frame", size=6.8)
    body(77, 11.6, "native human interface: no macros,\nGUI crafting by mouse\n\nBC models: 60-min survival episodes\n(72,000 actions), 2,500 episodes\nRL: 10-min episodes, fresh worlds", size=7.4, ls=1.3)
    fig.savefig(out, facecolor="white"); plt.close(fig); print("wrote", out)

draw("/home/user/vpt_stack_diagram.png", title="How the parts of OpenAI VPT fit together")
draw("/home/user/vpt_stack_diagram.svg", title="How the parts of OpenAI VPT fit together")
