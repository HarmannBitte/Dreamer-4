"""Two assets for the Part 1 slides added in deck v5: assets/diag_tech_tree.png (the 12-milestone Minecraft tech tree with the
tool gates, Dreamer 4's time-to-item and the success-rate fall-off of three agents) and assets/chart_agent_cost.png (hours of
data/interaction behind each diamond agent, Table 3). Numbers: Tables 3, 7 and 8 of arXiv 2509.24527. Run from presentation/."""
import glob, os
import matplotlib; matplotlib.use("Agg")
from matplotlib import font_manager
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch
for f in glob.glob(os.path.expanduser("~/.fonts/Carlito-*.ttf")) + glob.glob("/usr/share/fonts/truetype/crosextra/Carlito-*.ttf"):
    font_manager.fontManager.addfont(f)
FAM = "Carlito" if any(f.name == "Carlito" for f in font_manager.fontManager.ttflist) else "DejaVu Sans"
NAVY = "#14213D"; BLUE = "#2A56D6"; INK = "#1F2937"; GREY = "#6B7280"; MUTED = "#9AA3B2"; RULE = "#D3D8E2"; PANEL = "#F3F5F8"; SKY = "#E3EAFB"; DEEP = "#DCE3F0"
AMBER = "#B7791F"; SAND = "#FBF1DC"; GREEN = "#1B7F5C"
plt.rcParams.update({"font.family": FAM, "text.color": INK})
os.makedirs("assets", exist_ok=True); F = 1.1

# item, how to get it, Dreamer 4 %, VLA (Gemma 3) %, VPT fine-tuned % (Table 7), Dreamer 4 mean minutes over successful episodes (Table 8)
ITEMS = [("log", "punch a tree", 99.1, 98.5, 84.3, 0.9),
         ("planks", "from logs, in the\n2×2 inventory grid", 98.9, 98.3, 65.3, 2.0),
         ("crafting table", "4 planks; place it,\nopen it (3×3 grid)", 98.5, 97.2, 4.7, 4.4),
         ("stick", "2 planks → 4 sticks", 98.7, 97.7, 52.6, 2.9),
         ("wooden pickaxe", "3 planks + 2 sticks,\nat the table", 96.6, 94.1, 0.0, 5.0),
         ("cobblestone", "mine stone; by hand\nnothing drops", 95.9, 91.6, 6.9, 5.6),
         ("stone pickaxe", "3 cobblestone +\n2 sticks", 90.1, 76.7, 0.0, 6.7),
         ("iron ore", "dig down to a vein;\nneeds stone pickaxe", 66.7, 46.3, 0.1, 9.9),
         ("furnace", "8 cobblestone;\nplace it", 58.1, 42.4, 0.0, 11.0),
         ("iron ingot", "smelt ore in the\nfurnace, with fuel", 39.5, 22.5, 0.1, 12.4),
         ("iron pickaxe", "3 ingots + 2 sticks", 29.0, 11.2, 0.0, 13.3),
         ("diamond", "deep underground;\nneeds iron pickaxe", 0.7, 0.0, 0.0, 20.7)]
AGES = [("Wood age", 0, 5), ("Stone age", 5, 7), ("Iron age", 7, 11), ("Diamond", 11, 12)]
BW, GAP, AGAP = 6.6, 1.2, 2.6
xs = []; x = 1.7
for i in range(12):
    xs.append(x); x += BW + GAP
    if i in (4, 6, 10): x += AGAP - GAP
cx = [x + BW / 2 for x in xs]

def tech_tree(out):
    fig = plt.figure(figsize=(13.333, 5.6), dpi=200)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 100); ax.set_ylim(0, 42); ax.axis("off")
    def text(x, y, s, size=7.4, color=INK, ha="left", va="top", bold=False, ls=1.25, **kw):
        ax.text(x, y, s, fontsize=size * F, color=color, ha=ha, va=va, fontweight=("bold" if bold else "normal"), linespacing=ls, **kw)
    # age headers
    for name, a, b in AGES:
        x0, x1 = xs[a], xs[b - 1] + BW
        ax.plot([x0, x1], [40.2, 40.2], color=NAVY, lw=1.3)
        text(x0, 41.9, name.upper() + (f"  ·  {b - a} milestones" if b - a > 1 else ""), size=7.6, color=NAVY, bold=True)
    # item boxes
    yb0, yb1 = 33.6, 39.4
    for i, (name, how, d4, vla, vpt, mins) in enumerate(ITEMS):
        ax.add_patch(Rectangle((xs[i], yb0), BW, yb1 - yb0, fc="white", ec=RULE, lw=0.9, zorder=2))
        text(xs[i] + 0.45, yb1 - 0.5, name, size=7.8, color=NAVY, bold=True)
        text(xs[i] + 0.45, yb1 - 2.2, how, size=6.1, color=GREY, ls=1.22)
        text(cx[i], 33.0, f"{mins:.1f} min", size=6.6, color=GREY, ha="center")
        if i < 11:
            ax.add_patch(FancyArrowPatch((xs[i] + BW + 0.1, 36.5), (xs[i + 1] - 0.1, 36.5), arrowstyle="-|>", mutation_scale=7, color=INK, lw=0.9, zorder=3))
    # tool gates under the age boundaries
    for i, s in [(4, "stone drops only\nwith a wooden pickaxe"), (6, "iron ore drops only\nwith a stone pickaxe"), (10, "diamond drops only\nwith an iron pickaxe")]:
        bx = (xs[i] + BW + xs[i + 1]) / 2
        ax.plot([bx, bx], [33.6, 31.6], color=AMBER, lw=1.0, ls=(0, (2, 1.5)))
        text(bx, 31.3, s, size=6.6, color=AMBER, ha="center", style="italic", ls=1.2)
    text(1.7, 31.9, "time to reach it — Dreamer 4, mean over successful episodes (Table 8)", size=6.4, color=MUTED)
    # success-rate chart
    y0, y1 = 7.5, 25.5
    def Y(p): return y0 + (y1 - y0) * p / 100
    text(1.7, 27.9, "Success rate per milestone — 1,000 episodes × 60 min, all agents trained on the same 2,541 h (Table 7)", size=7.6, color=NAVY, bold=True)
    for p in (0, 25, 50, 75, 100):
        ax.plot([1.7, 98.3], [Y(p)] * 2, color=RULE, lw=0.7, zorder=1)
        text(98.2, Y(p) + 0.15, f"{p} %", size=6.2, color=MUTED, ha="right", va="bottom")
    series = [(4, "VPT fine-tuned (Baker et al. 2022), offline", MUTED, 1.1, (0, (3, 2)), "s"),
              (3, "VLA (Gemma 3), behavioural cloning", BLUE, 1.3, "-", "o"),
              (2, "Dreamer 4, imagination training", NAVY, 2.0, "-", "o")]
    for col, lab, colr, lw, ls, mk in series:
        ys = [Y(it[col]) for it in ITEMS]
        ax.plot(cx, ys, color=colr, lw=lw, ls=ls, marker=mk, ms=3.2, zorder=4)
    for i, it in enumerate(ITEMS):
        text(cx[i], Y(it[2]) + 0.6, f"{it[2]:.1f}", size=6.6, color=NAVY, ha="center", va="bottom", bold=True)
        if i >= 6: text(cx[i] + 0.4, Y(it[3]) - 0.6, f"{it[3]:.1f}", size=6.4, color=BLUE, ha="left", va="top")
        if i in (0, 1, 3): text(cx[i] + 1.0, Y(it[4]) + 0.2, f"{it[4]:.1f}", size=6.4, color=GREY, ha="left", va="center")
    # legend
    lx, ly = 66.0, 24.3
    for k, (col, lab, colr, lw, ls, mk) in enumerate(series):
        yy = ly - k * 1.6
        ax.plot([lx, lx + 3.2], [yy, yy], color=colr, lw=lw, ls=ls, marker=mk, ms=3.2)
        text(lx + 4.0, yy, lab, size=6.8, color=INK, va="center")
    text(1.7, 4.3, "Human players with Minecraft experience need about 20 minutes ≈ 24,000 mouse-and-keyboard actions to reach a diamond; an evaluation episode gives the agent 60 minutes = 72,000 actions. "
                   "The chain cannot be shortcut: each item\nneeds the previous tool, and mining a block with a weaker tool destroys it without a drop. Diamonds sit at the end of twelve dependent skills — crafting menus, mouse precision, digging, smelting — all learned from offline video.",
         size=6.7, color=GREY, ls=1.3)
    fig.savefig(out, facecolor="white"); plt.close(fig); print("wrote", out)

def agent_cost(out):
    FF = 1.3          # larger type: the chart is shown at ~8 in on the slide
    fig, ax = plt.subplots(figsize=(7.6, 4.7), dpi=200)
    fig.subplots_adjust(left=0.02, right=0.98, top=0.98, bottom=0.2)
    ax.set_xscale("log"); ax.set_xlim(1e3, 5e6); ax.set_ylim(-0.55, 4.05)
    for sp in ("top", "right", "left"): ax.spines[sp].set_visible(False)
    ax.spines["bottom"].set_color(RULE); ax.tick_params(axis="y", left=False, labelleft=False); ax.tick_params(axis="x", colors=GREY, labelsize=8 * FF)
    ax.set_xticks([1e3, 1e4, 1e5, 1e6]); ax.set_xticklabels(["1K h", "10K h", "100K h", "1M h"]); ax.set_xticks([], minor=True)
    ax.grid(axis="x", color=RULE, lw=0.6); ax.set_axisbelow(True)
    C = {"contractor": NAVY, "web": "#9DB8F5", "online": AMBER}
    groups = [("VPT, RL fine-tuned  ·  OpenAI 2022", "reaches diamonds — after 194K hours of playing the real game",
               [("contractor", 2.5e3, "2.5K h contractor video with mouse & keyboard"), ("web", 2.7e5, "270K h YouTube video, IDM-labelled"), ("online", 1.94e5, "194K h of online RL in the game")]),
              ("VPT, behavioural cloning only  ·  2022", "offline: sticks 52.6 %, wooden pickaxe 0.0 % (Table 7)",
               [("contractor", 2.5e3, "2.5K h contractor video"), ("web", 2.7e5, "270K h YouTube video, IDM-labelled")]),
              ("Dreamer 3  ·  Hafner et al. 2023", "reaches diamonds — 64×64 pixels + inventory state, abstract crafting actions, online",
               [("online", 1.4e3, "1.4K h of online interaction, no human data")]),
              ("Dreamer 4  ·  2025", "reaches diamonds offline (0.7 %) — 360×640 pixels, raw mouse & keyboard, no interaction",
               [("contractor", 2.5e3, "2.5K h contractor video — nothing else")])]
    for gi, (name, outcome, bars) in enumerate(groups):
        y = (3 - gi) * 1.12
        ax.text(1.03e3, y + 0.56, name, fontsize=9.2 * FF, fontweight="bold", color=NAVY, va="center")
        ax.text(1.03e3, y + 0.37, outcome, fontsize=7.4 * FF, color=GREY, va="center")
        h = 0.16
        for bi, (kind, val, lab) in enumerate(bars):
            yy = y + 0.12 - bi * (h + 0.05)
            ax.barh(yy, val, height=h, left=1, color=C[kind], zorder=3)
            ax.text(val * 1.12, yy, lab, fontsize=7.2 * FF, color=INK, va="center")
    fig.text(0.02, 0.06, "Hours on a log scale (Table 3 of the paper). Dreamer 4 uses the same 2.5K contractor hours that VPT used to train its inverse-dynamics\n"
                         "model (IDM) — and nothing else: no pseudo-labelled web video, no environment interaction.", fontsize=7.2 * FF, color=GREY, va="center", linespacing=1.35)
    fig.savefig(out, facecolor="white"); plt.close(fig); print("wrote", out)

tech_tree("assets/diag_tech_tree.png")
agent_cost("assets/chart_agent_cost.png")
