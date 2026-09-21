"""Charts for the Dreamer 4 deck (numbers from the paper's tables; see dreamer4_research_report.md).
Style matches the deck: Carlito/Calibri, one accent colour for Dreamer 4, greys for baselines, no chart titles (the slide carries them)."""
import glob, os
import matplotlib; matplotlib.use("Agg")
from matplotlib import font_manager
import matplotlib.pyplot as plt, numpy as np
A = "assets/"
for f in glob.glob(os.path.expanduser("~/.fonts/Carlito-*.ttf")) + glob.glob("/usr/share/fonts/truetype/crosextra/Carlito-*.ttf"):
    font_manager.fontManager.addfont(f)
FAM = "Carlito" if any(f.name == "Carlito" for f in font_manager.fontManager.ttflist) else "DejaVu Sans"
NAVY = "#14213D"; BLUE = "#2A56D6"; INK = "#1F2937"; GREY = "#6B7280"; MUTED = "#9AA3B2"; RULE = "#D3D8E2"
G1, G2, G3 = "#C9CFD9", "#98A2B3", "#4B5563"          # light → dark greys for baselines
plt.rcParams.update({"font.family": FAM, "font.size": 11, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": RULE, "axes.linewidth": 0.8, "xtick.color": GREY, "ytick.color": GREY, "axes.labelcolor": GREY,
                     "xtick.major.size": 0, "ytick.major.size": 0, "text.color": INK, "legend.frameon": False})

def clean(ax, axis="y"):
    ax.grid(axis=axis, color=RULE, linewidth=0.6); ax.set_axisbelow(True)
    for sp in ("left", "bottom"): ax.spines[sp].set_color(RULE)

# 1. Hard milestones, Table 7 (success %, 1,000 episodes)
items = ["Stone\npickaxe", "Iron\nore", "Furnace", "Iron\ningot", "Iron\npickaxe", "Diamond"]
data = {"BC": [53.8, 26.5, 16.2, 4.3, 0.6, 0.0], "VLA (Gemma 3)": [76.7, 46.3, 42.4, 22.5, 11.2, 0.0],
        "WM + BC": [89.4, 62.9, 51.1, 27.8, 16.9, 0.0], "Dreamer 4": [90.1, 66.7, 58.1, 39.5, 29.0, 0.7]}
cols = [G1, G2, G3, BLUE]
fig, ax = plt.subplots(figsize=(10, 4.6), dpi=200); x = np.arange(len(items)); w = 0.2
for i, (k, v) in enumerate(data.items()):
    b = ax.bar(x + (i - 1.5) * w, v, w * 0.92, label=k, color=cols[i])
    for r, val in zip(b, v):
        ax.text(r.get_x() + r.get_width() / 2, val + 1.2, f"{val:g}", ha="center", va="bottom", fontsize=8.5,
                color=(BLUE if i == 3 else GREY), fontweight=("bold" if i == 3 else "normal"))
ax.set_xticks(x); ax.set_xticklabels(items, color=INK); ax.set_ylabel("Success rate (%)"); ax.set_ylim(0, 100)
ax.legend(ncol=4, loc="upper right", fontsize=10.5, handlelength=1.2, columnspacing=1.4); clean(ax)
fig.tight_layout(); fig.savefig(A + "chart_table7_hard.png"); plt.close(fig)

# 2. Design cascade, Table 2 (FVD lower is better; FPS where reported)
rows = [("Diffusion-forcing transformer, K = 64 steps", 306, 0.8), ("K = 4 sampling steps", 875, 9.1), ("+ shortcut objective  → shortcut forcing", 329, None),
        ("+ x-prediction", 326, None), ("+ loss in x-space (scaled by (1 − τ)²)", 151, None), ("+ ramp loss weight", 102, None),
        ("+ alternating batch lengths", 80, None), ("+ long-context (time) attention only every 4th layer", 70, 18.9), ("+ grouped-query attention", 71, 23.2),
        ("+ time-factorised long context", 91, 30.1), ("+ register tokens", 91, None), ("+ N_z 128 → 256 latent tokens (final)", 57, 21.4)]
fig, ax = plt.subplots(figsize=(10.5, 6.2), dpi=200)
y = np.arange(len(rows))[::-1]; vals = [r[1] for r in rows]
colors = [G3, G3] + [G2] * 4 + [G1] * 5 + [BLUE]
ax.barh(y, vals, color=colors, height=0.62)
for yi, (name, fvd, fps) in zip(y, rows):
    ax.text(fvd + 10, yi, f"{fvd}" + (f"   ·   {fps} FPS" if fps else ""), va="center", fontsize=10, color=(BLUE if fvd == 57 else INK), fontweight=("bold" if fvd == 57 else "normal"))
ax.set_yticks(y); ax.set_yticklabels([r[0] for r in rows], fontsize=11.5, color=INK); ax.set_xlabel("FVD on 384-frame generations (lower is better)"); ax.set_xlim(0, 1000)
ax.text(1000, len(rows) - 0.2, "dark: starting point   ·   mid: objective   ·   light: architecture   ·   blue: final", ha="right", va="bottom", fontsize=9, color=GREY)
clean(ax, "x"); fig.tight_layout(); fig.savefig(A + "chart_ablation_cascade.png"); plt.close(fig)

# 3. Time to milestone, Table 8 (minutes, successful episodes)
ms = ["Crafting table", "Stone pickaxe", "Iron pickaxe", "Diamond"]; d4 = [4.4, 6.7, 13.3, 20.7]; vla = [7.2, 14.5, 31.1, None]
fig, ax = plt.subplots(figsize=(6.4, 4.2), dpi=200); x = np.arange(4); w = 0.36
ax.bar(x - w / 2, d4, w * 0.92, color=BLUE, label="Dreamer 4"); ax.bar(x + w / 2, [v or 0 for v in vla], w * 0.92, color=G2, label="VLA (Gemma 3)")
for i, v in enumerate(d4): ax.text(i - w / 2, v + 0.5, f"{v}", ha="center", fontsize=10, color=BLUE, fontweight="bold")
for i, v in enumerate(vla):
    if v: ax.text(i + w / 2, v + 0.5, f"{v}", ha="center", fontsize=10, color=GREY)
    else: ax.text(i + w / 2, 1, "never", ha="center", fontsize=9, color=GREY, rotation=90, va="bottom")
ax.set_xticks(x); ax.set_xticklabels(ms, color=INK); ax.set_ylabel("Minutes until item obtained"); ax.set_ylim(0, 36)
ax.legend(fontsize=10.5, handlelength=1.2); clean(ax)
fig.tight_layout(); fig.savefig(A + "chart_time_to_milestone.png"); plt.close(fig)

# 4. Generation speed, one dimension, log scale (paper + TalkRL): ~1,000 FPS RSSM, 21 FPS Dreamer 4, 0.8 FPS diffusion forcing K=64
plt.rcParams.update({"font.size": 13})
fig, ax = plt.subplots(figsize=(6.2, 3.2), dpi=200)
pts = [("Diffusion-forcing\ntransformer, K = 64", 0.8, G3), ("Dreamer 4\n(shortcut forcing, K = 4)", 21, BLUE), ("Dreamer 3 RSSM\n(64×64 pixels)", 1000, G2)]
ax.axvspan(20, 3000, color=BLUE, alpha=0.05, lw=0); ax.text(24, 1.66, "real time (≥ 20 FPS)", fontsize=11, color=BLUE, va="center")
ax.hlines(1, 0.3, 3000, color=RULE, lw=1)
for n, fps, c in pts:
    ax.scatter(fps, 1, s=160, color=c, zorder=3)
    ax.annotate(n, (fps, 1), textcoords="offset points", xytext=(0, -16), ha="center", va="top", fontsize=11.5, color=(BLUE if c == BLUE else INK), fontweight=("bold" if c == BLUE else "normal"))
    ax.annotate(f"{fps:g} FPS", (fps, 1), textcoords="offset points", xytext=(0, 14), ha="center", va="bottom", fontsize=11.5, color=c, fontweight="bold")
ax.set_xscale("log"); ax.set_xlim(0.3, 3000); ax.set_ylim(0.2, 1.9); ax.set_yticks([])
ax.spines["left"].set_visible(False); ax.set_xlabel("Generation speed (frames per second, log scale)")
ax.set_xticks([1, 10, 100, 1000]); ax.set_xticklabels(["1", "10", "100", "1,000"])
fig.tight_layout(); fig.savefig(A + "chart_speed.png"); plt.close(fig)
print("charts done (font:", FAM + ")")
