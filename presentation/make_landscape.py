"""Landscape of world models 2019-2025 for the final deck: two lineages (world models the agent trains inside vs. world models a human
plays inside) on a year grid, with Dreamer 4 as the model that belongs to both. Facts: Dreamer papers (2019/2020/2023), DIAMOND (Alonso
et al. 2024), Genie 1/2/3 (DeepMind blogs Feb 2024 / Dec 2024 / Aug 2025), GameNGen (Valevski et al. Aug 2024), Oasis (Decart+Etched Oct 2024),
Lucid-v1 (Nov 2024), MineWorld (Apr 2025), Table 1 of arXiv 2509.24527 for the Minecraft numbers, SIMA 2 (Nov 2025).
Writes assets/diag_landscape.png (2666 px wide, aspect 2.7:1). Run by make_assets.py."""
import glob, os
import matplotlib; matplotlib.use("Agg")
from matplotlib import font_manager
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch
for f in glob.glob(os.path.expanduser("~/.fonts/Carlito-*.ttf")) + glob.glob("/usr/share/fonts/truetype/crosextra/Carlito-*.ttf"):
    font_manager.fontManager.addfont(f)
FAM = "Carlito" if any(f.name == "Carlito" for f in font_manager.fontManager.ttflist) else "DejaVu Sans"
NAVY = "#14213D"; BLUE = "#2A56D6"; INK = "#1F2937"; GREY = "#6B7280"; MUTED = "#9AA3B2"; RULE = "#D3D8E2"; PANEL = "#F3F5F8"; SKY = "#E3EAFB"
GREEN = "#1B7F5C"; MINT = "#E1F2EB"; AMBER = "#B7791F"; SAND = "#FBF1DC"
plt.rcParams.update({"font.family": FAM, "text.color": INK})
F = 1.15
WU, HU = 100.0, 37.0                                   # drawing units (aspect 2.7:1)

fig = plt.figure(figsize=(13.33, 13.33 * HU / WU), dpi=200)
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, WU); ax.set_ylim(0, HU); ax.axis("off")

def rect(x, y, w, h, fc="none", ec=RULE, lw=0.8, z=1):
    ax.add_patch(Rectangle((x, y), w, h, facecolor=fc, edgecolor=ec, linewidth=lw, zorder=z))

def text(x, y, s, size=8, color=INK, weight="normal", ha="left", va="top", style="normal", z=5, ls=1.25):
    ax.text(x, y, s, fontsize=size * F, color=color, fontweight=weight, ha=ha, va=va, fontstyle=style, zorder=z, linespacing=ls)

def chip(x, y, w, h, head, lines, fc="white", ec=RULE, head_color=NAVY, lw=0.9):
    rect(x, y, w, h, fc=fc, ec=ec, lw=lw, z=3)
    text(x + 0.6, y + h - 0.55, head, size=7.9, color=head_color, weight="bold")
    text(x + 0.6, y + h - 2.35, lines, size=6.9, color=GREY, ls=1.2)

# ---- grid: label column + year columns (2021-22 omitted: no entry)
LBL_W = 14.5
cols = [("2019", 10.0), ("2020", 10.0), ("2023", 10.0), ("2024", 30.0), ("2025", 25.5)]
xs = {}; x = LBL_W
for name, w in cols:
    xs[name] = (x, w); x += w
Y_HEAD = HU - 2.4
rows = {"A": (25.2, 8.0), "B": (9.6, 14.6), "C": (1.2, 7.4)}      # (y0, height)

# header
for name, (x0, w) in xs.items():
    text(x0 + w / 2, Y_HEAD + 1.9, name, size=9.5, color=GREY, weight="bold", ha="center")
    if name in ("2024", "2025"):
        rect(x0 + 0.4, 0.6, w - 0.8, HU - 3.4, fc=PANEL, ec="none", z=0)          # the 2024-25 wave, shaded
ax.plot([LBL_W, WU - 0.4], [Y_HEAD, Y_HEAD], color=RULE, lw=0.8, zorder=2)
text(xs["2020"][0] + xs["2020"][1] + 0.4, Y_HEAD + 1.5, "…", size=9.5, color=MUTED, ha="center")

# row labels
def row_label(key, head, lines, head_color=NAVY):
    y0, h = rows[key]
    text(0.6, y0 + h - 0.4, head, size=11, color=head_color, weight="bold")
    text(0.6, y0 + h - 3.0, lines, size=7.6, color=GREY, ls=1.25)
    ax.plot([0.6, WU - 0.4], [y0 + h + 0.55, y0 + h + 0.55], color=RULE, lw=0.8, zorder=2)

row_label("A", "For agents", "the agent trains inside the model\njudged by the agent's return\nsmall images, latent state,\nonline data from the real task")
row_label("B", "As media", "a human plays inside the model\njudged by how it looks and feels\nhigh-res pixels in real time;\nmechanics and memory often break")
row_label("C", "Both", "played by humans, trained in\nby the agent — and tested on\nwhether that agent succeeds\nin the real game")

# ---- row A: agents
yA, hA = rows["A"]; ch = 5.6; cy = yA + (hA - ch) / 2
for col, head, lines in [("2019", "Dreamer · 2019", "latent imagination on\nDM Control, 64×64 px"),
                         ("2020", "DreamerV2 · 2020", "discrete latents;\nAtari at human level"),
                         ("2023", "DreamerV3 · 2023", "150+ tasks, one config;\ndiamonds via online RL")]:
    x0, w = xs[col]; chip(x0 + 0.5, cy, w - 1.0, ch, head, lines)
x0, w = xs["2024"]; chip(x0 + 0.9, cy, 10.5, ch, "DIAMOND · 2024", "diffusion world model;\nAtari 64×64, agent inside")
text(x0 + 12.4, cy + ch - 0.3, "recurrent or small diffusion models: fast, but low\nresolution, often with privileged state (inventory,\nabstract craft actions) — nobody would play inside them", size=7.0, color=MUTED, style="italic")

# ---- row B: media (2024: five models in two rows; 2025: two models + SIMA 2 note)
yB, hB = rows["B"]; ch2 = 5.6; gap = 0.6
x0, w = xs["2024"]; cw = (w - 1.8 - 2 * gap) / 3
top = yB + hB - 0.6 - ch2; bot = top - gap - ch2
for i, (head, lines) in enumerate([("Genie 1 · Feb 2024", "latent actions learned\nfrom video; 2D worlds"),
                                   ("GameNGen · Aug 2024", "DOOM at ~20 FPS from a\ndiffusion model"),
                                   ("Oasis · Oct 2024", "Minecraft, 500 M\n20 FPS, 360p, 1.6 s ctx")]):
    chip(x0 + 0.9 + i * (cw + gap), top, cw, ch2, head, lines)
for i, (head, lines) in enumerate([("Lucid-v1 · Nov 2024", "Minecraft, 1.1 B\n44 FPS, 360p, 1.0 s ctx"),
                                   ("Genie 2 · Dec 2024", "3D worlds from an image\n10–20 s; keys + mouse")]):
    chip(x0 + 0.9 + i * (cw + gap), bot, cw, ch2, head, lines)
text(x0 + 0.9 + 2 * (cw + gap) + 0.5, bot + ch2 - 0.4, "judged by FVD, PSNR and\nhow it feels to play — none\nof the Minecraft models\nsurvives a crafting menu\n(Table 1: 0–5 of 16 tasks)", size=6.9, color=MUTED, style="italic")
x0, w = xs["2025"]; cw5 = (w - 1.8 - gap) / 2
chip(x0 + 0.9, top, cw5, ch2, "MineWorld · Apr 2025", "Minecraft, 1.2 B, autoregressive;\nneeds the actions in advance")
chip(x0 + 0.9 + cw5 + gap, top, cw5, ch2, "Genie 3 · Aug 2025", "text → world, 720p, 24 FPS,\nminutes; internals not public")
rect(x0 + 0.9, bot, w - 1.8, ch2, fc=SKY, ec="none", z=3)
text(x0 + 1.6, bot + ch2 - 0.55, "Nov 2025 · SIMA 2 acts in Genie 3 worlds", size=7.9, color=BLUE, weight="bold")
text(x0 + 1.6, bot + ch2 - 2.35, "an agent uses the world model as a training\nground, but stays outside it — the model never\nlearns anything from the agent", size=6.9, color=GREY, ls=1.2)

# ---- row C: Dreamer 4 (spans the 2024-25 wave)
yC, hC = rows["C"]; xC0 = xs["2024"][0] + 0.9; xC1 = WU - 0.4 - 0.4
rect(xC0, yC + 0.2, xC1 - xC0, hC - 0.4, fc="white", ec=NAVY, lw=1.6, z=3)
text(xC0 + 0.8, yC + hC - 0.55, "Dreamer 4 · Sep 2025", size=10, color=NAVY, weight="bold")
text(xC0 + 0.8, yC + hC - 2.9, "Google DeepMind · 2 B parameters\npaper only — no code, no weights\narXiv 2509.24527", size=7.0, color=GREY, ls=1.25)
xt = xC0 + 14.5
text(xt, yC + hC - 0.7, "humans play inside it:", size=7.3, color=NAVY, weight="bold"); text(xt + 10.5, yC + hC - 0.7, "14/16 interaction tasks · 21 FPS · 640×360 · 9.6 s context · one H100", size=7.3, color=INK)
text(xt, yC + hC - 2.6, "the agent trains inside it:", size=7.3, color=NAVY, weight="bold"); text(xt + 10.5, yC + hC - 2.6, "diamonds from 2,541 h of offline video; zero environment steps", size=7.3, color=INK)
text(xt, yC + hC - 4.5, "one transformer:", size=7.3, color=NAVY, weight="bold"); text(xt + 10.5, yC + hC - 4.5, "one block-causal model is tokenizer, simulator and agent backbone", size=7.3, color=INK)
# lineage arrows into Dreamer 4 (the agent lineage is routed through the empty gutter left of the 2024 column)
xa = xs["2024"][0] + 0.9 + 10.5 / 2; xg = xs["2024"][0] + 0.45
ax.plot([xa, xa, xg, xg], [cy, cy - 1.1, cy - 1.1, yC + hC + 0.9], color=NAVY, lw=0.9, zorder=4, solid_capstyle="round")
ax.add_patch(FancyArrowPatch((xg, yC + hC + 1.0), (xg, yC + hC - 0.2), arrowstyle="-|>", mutation_scale=9, lw=0.9, color=NAVY, zorder=4, shrinkA=0, shrinkB=1))
text(xg - 0.9, yB + hB / 2 + 1.2, "imagination training:\nDreamer 1–3 → 4", size=7.2, color=NAVY, style="italic", ha="right")
xb = x0 + 0.9 + cw5 + gap + cw5 / 2
ax.add_patch(FancyArrowPatch((xb, top), (xb, yC + hC - 0.2), arrowstyle="-|>", mutation_scale=9, lw=0.9, color=BLUE, zorder=4, shrinkA=0, shrinkB=1))
text(xb + 0.6, bot - 0.3, "real-time video\nworld models", size=7.0, color=BLUE, style="italic", va="top")

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "diag_landscape.png")
os.makedirs(os.path.dirname(out), exist_ok=True)
fig.savefig(out, dpi=200, facecolor="white"); print("wrote", out)
