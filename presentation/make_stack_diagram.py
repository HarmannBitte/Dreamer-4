"""System diagram: how the parts of the Dreamer 4 stack interact (data → tokenizer → shared transformer → heads; the three training
phases; the imagination loop; acting in the real game). Facts from arXiv 2509.24527 §3–4 and Algorithm 1. Run from the presentation dir.
Writes assets/diag_stack.png (+ two half crops for the deck) and the standalone /home/user/dreamer4_stack_diagram.{png,svg}."""
import glob, os
import matplotlib; matplotlib.use("Agg")
from matplotlib import font_manager
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle
from PIL import Image
A = "assets/"; os.makedirs(A, exist_ok=True)
for f in glob.glob(os.path.expanduser("~/.fonts/Carlito-*.ttf")) + glob.glob("/usr/share/fonts/truetype/crosextra/Carlito-*.ttf"):
    font_manager.fontManager.addfont(f)
FAM = "Carlito" if any(f.name == "Carlito" for f in font_manager.fontManager.ttflist) else "DejaVu Sans"
NAVY = "#14213D"; BLUE = "#2A56D6"; INK = "#1F2937"; GREY = "#6B7280"; MUTED = "#9AA3B2"; RULE = "#D3D8E2"; PANEL = "#F3F5F8"; SKY = "#E3EAFB"; DEEP = "#DCE3F0"
plt.rcParams.update({"font.family": FAM, "text.color": INK, "mathtext.fontset": "custom", "mathtext.rm": FAM, "mathtext.it": FAM + ":italic", "mathtext.bf": FAM + ":bold"})
ZH = r"$\hat{z}$"; RH = r"$\hat{r}$"; VH = r"$\hat{v}$"          # hats via mathtext (Carlito has no combining accents)
F = 1.1                                                            # global font scale
YMIN = 2.5                                                         # bottom of the drawing (row B boxes end at 4)

def draw(out, title=None):
    top = 60 if title else 56.25
    fig = plt.figure(figsize=(13.333, 13.333 * (top - YMIN) / 100), dpi=200)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 100); ax.set_ylim(YMIN, top); ax.axis("off")
    if title:
        ax.text(1.2, 58.5, title, fontsize=15 * F, fontweight="bold", color=NAVY, va="center")
        ax.text(98.8, 58.5, "after Hafner, Yan, Lillicrap (2025), arXiv 2509.24527 · schematic drawn for this deck, not from the paper", fontsize=8.5 * F, color=GREY, va="center", ha="right")

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
    def route(pts, color=INK, lw=1.1, ls="-", ms=10):          # orthogonal polyline ending in an arrow head
        xs, ys = zip(*pts); ax.plot(xs, ys, color=color, lw=lw, ls=ls, zorder=3, solid_capstyle="round")
        (x0, y0), (x1, y1) = pts[-2], pts[-1]; arrow((x0, y0), (x1, y1), color=color, lw=lw, ms=ms)
    def numeral(x, y, n):
        ax.text(x, y, f"{n:02d}", fontsize=13 * F, color=BLUE, fontweight="bold", ha="left", va="top")
    def tag(x, y, s):
        ax.text(x, y, s, fontsize=6.8 * F, color=GREY, ha="right", va="top", style="italic")
    def small(x, y, s, color=GREY, ha="center", va="top", size=7.4):
        ax.text(x, y, s, fontsize=size * F, color=color, ha=ha, va=va)

    yA0, yA1 = 30, 55                       # row A: the model.  row B (loops): 4 … 25.5.  corridor 27.5–30 carries the action/reward line.
    # ------------------------------------------------------------------ 01 data
    box(1, yA0, 15.5, yA1 - yA0); numeral(2, 54.3, 1); label(2, 51.4, "Offline data")
    body(2, 49.1, "2,541 h of human Minecraft\nplay (OpenAI VPT\ncontractor recordings)\n\n360×640 frames, 20 FPS\nkeyboard + mouse actions\n(clips without actions\nwork too: a learned\n'no action' embedding)\nitem events → rewards\n\nno environment\ninteraction at any point", size=8.2)
    # ------------------------------------------------------------------ 02 tokenizer
    box(19.5, yA0, 18, yA1 - yA0); numeral(20.5, 54.3, 2); label(20.5, 51.4, "Causal tokenizer  ·  400 M")
    chip(21, 44.9, 15, 4.6, "encoder\nframe t  →  z_t = 256 tokens × 32\n(bottleneck with tanh)", fc=DEEP, size=8.0)
    chip(21, 37.4, 15, 4.8, "decoder\nlatents → pixels — only for the\nhuman-interaction demo, videos\nand figures; never in the agent's loop", fc=PANEL, size=7.6)
    body(21, 36.3, "masked-autoencoder loss (MSE + LPIPS,\npatch dropout) · trained first, then frozen\n· causal in time → decodes frame by frame", size=7.4, color=GREY, ls=1.28)
    # ------------------------------------------------------------------ 03 transformer
    box(41, yA0, 39.5, yA1 - yA0, ec=NAVY, lw=1.3); numeral(42, 54.3, 3)
    label(42, 51.4, "Block-causal transformer  ·  1.6 B  —  dynamics model and agent in one network", size=9.8)
    body(42.3, 49.4, "inputs, per frame", size=7.6, color=GREY)
    for i, (s, fc, ec) in enumerate([("actions a_t  (or 'no action')", PANEL, RULE), ("signal level τ_t, step size d", PANEL, RULE), ("noised latents  z_t(τ_t)", DEEP, RULE), ("register tokens", PANEL, RULE), ("agent tokens  ←  task id", SKY, BLUE)]):
        chip(42.3, 45.8 - i * 2.85, 12.4, 2.45, s, fc=fc, ec=ec, size=7.8)
    body(56.2, 49.4, "space attention inside\na frame (3 of 4 layers)\n\ncausal time attention\nover 192 frames = 9.6 s\n(every 4th layer)\n\nagent tokens attend to\nall tokens; nothing\nattends back to them —\nthe agent cannot bias\nthe simulation\n('no causal confusion')", size=7.6)
    body(67.6, 49.4, "outputs", size=7.6, color=GREY)
    chip(67.6, 45.2, 11.9, 3.2, ZH + "$_t$  clean latents of frame t\nx-prediction · shortcut forcing", fc=NAVY, ec=NAVY, color="white", size=7.8, bold=True)
    chip(67.6, 41.6, 11.9, 2.3, "policy  π(a_t … a_t+8 | task)", fc=BLUE, ec=BLUE, color="white", size=7.8, bold=True)
    chip(67.6, 38.0, 11.9, 2.3, "reward  " + RH + "$_t$", fc=BLUE, ec=BLUE, color="white", size=7.8, bold=True)
    chip(67.6, 34.4, 11.9, 2.3, "value  " + VH + "$_t$", fc=BLUE, ec=BLUE, color="white", size=7.8, bold=True)
    tag(79.5, 45.0, "trained in phase 1, kept training in 2"); tag(79.5, 41.4, "phase 2 BC  →  phase 3 RL"); tag(79.5, 37.8, "phase 2"); tag(79.5, 34.2, "phase 3")
    body(67.6, 32.5, "policy, reward, value: MLP heads\nread off the agent tokens", size=7.2, color=GREY, ls=1.25)
    body(42.3, 32.5, "same weights for predicting and acting: K = 4 passes\nper imagined frame, 1 pass per real frame", size=7.2, color=GREY, ls=1.25)
    # ------------------------------------------------------------------ 04 phases
    box(83, yA0, 16, yA1 - yA0, fc=PANEL, ec=PANEL); numeral(84, 54.3, 4); label(84, 51.4, "Three training phases")
    body(84, 49.2, "1  World-model pretraining\n    tokenizer (masked AE),\n    then dynamics: shortcut-\n    forcing loss on all\n    2,541 h (actions optional)\n\n2  Agent fine-tuning\n    add agent tokens + heads;\n    BC + reward loss on task\n    clips, dynamics loss on\n    uniform clips (50 / 50)\n\n3  Imagination training\n    transformer frozen; only\n    policy + value heads learn\n    from rollouts in the model\n    (PMPO + KL to BC policy)", size=7.6, ls=1.28)
    # ------------------------------------------------------------------ arrows, row A
    arrow((16.5, 47.2), (21, 47.2)); small(18.7, 47.6, "frames", va="bottom")
    arrow((36, 47.2), (42.3, 41.3), color=NAVY, rad=-0.28); small(39.2, 44.3, "z_t(τ_t)", color=NAVY, va="center", size=7.6)
    route([(8.5, yA0), (8.5, 28.5), (48.5, 28.5), (48.5, yA0)])
    small(28.5, 28.8, "actions, task id, item-event rewards", va="bottom")

    # ------------------------------------------------------------------ 05 acting in the real game
    yB0, yB1 = 4, 25.5
    box(1, yB0, 36.5, yB1 - yB0); numeral(2, 24.8, 5); label(2, 21.9, "Acting in the real game (evaluation)")
    steps = ["Minecraft\nframe, 20 FPS", "encoder\n→ z_t", "transformer\n9.6 s context", "policy head\n→ keys + mouse"]
    for i, s in enumerate(steps):
        chip(2 + i * 8.7, 15.6, 7.6, 4.2, s, fc=(SKY if i == 3 else PANEL), ec=(BLUE if i == 3 else RULE), size=7.8)
        if i < 3: arrow((9.6 + i * 8.7, 17.7), (10.7 + i * 8.7, 17.7), lw=1.1, ms=9)
    route([(31.9, 15.6), (31.9, 14.3), (5.8, 14.3), (5.8, 15.6)], color=MUTED, ls=(0, (3, 2)), ms=9)
    small(18.8, 13.9, "the action changes the game; the next frame comes back")
    body(2, 11.5, "The world model generates nothing at test time — it supplies the\nrepresentation the policy head reads. Only encoder + transformer +\npolicy head run, one pass per frame.\n\n1,000 episodes × 60 min, fresh random worlds, empty inventory, a fixed\nprompt sequence of tasks (log → planks → … → iron pickaxe → diamond).\nSuccess = the item shows up in the inventory.", size=8.0)
    # ------------------------------------------------------------------ 06 imagination loop
    box(39.5, yB0, 59.5, yB1 - yB0, ec=BLUE, lw=1.2); numeral(40.5, 24.8, 6); label(40.5, 21.9, "Phase 3 · the imagination loop  —  inside the frozen model, entirely in latent space")
    nodes = ["real context\nlatents of a clip from\nthe training data", "policy head\nsamples a_t\n(task-conditioned)", "dynamics predicts\n" + ZH + "$_{t+1}$ in K = 4\nshortcut steps", "reward head " + RH + "$_t$\nvalue head " + VH + "$_t$\nλ-returns, γ = 0.997", "PMPO update\nadvantage sign only;\nKL β = 0.3 to BC policy"]
    for i, s in enumerate(nodes):
        fc = SKY if i in (1, 4) else (DEEP if i == 2 else PANEL); ec = BLUE if i in (1, 4) else RULE
        chip(40.5 + i * 11.7, 14.2, 10.4, 5.9, s, fc=fc, ec=ec, size=7.7)
        if i < 4: arrow((50.9 + i * 11.7, 17.15), (52.2 + i * 11.7, 17.15), lw=1.1, ms=9)
    route([(69.1, 14.2), (69.1, 13.0), (58.6, 13.0), (58.6, 14.2)], color=NAVY, ls=(0, (3, 2)), ms=9)
    small(63.85, 12.65, ZH + "$_{t+1}$ becomes the context for the next step", color=NAVY)
    route([(92.5, 14.2), (92.5, 11.1), (55.8, 11.1), (55.8, 14.2)], color=BLUE, ls=(0, (3, 2)), ms=9)
    small(74.2, 10.75, "gradients flow into the policy and value heads only; the frozen BC policy copy is the prior", color=BLUE)
    body(40.5, 8.6, "Each rollout starts from real frames, then follows the current policy through the model's imagination, one rollout per context.\n"
                    "Rewards come from the learned reward head (never from the game); the reverse KL keeps the policy in the space of behaviours seen\n"
                    "in the data. Result on the offline diamond challenge: BC on the same representations reaches the iron pickaxe in 16.9 % of\n"
                    "episodes and never a diamond; after imagination training it is 29 % and 0.7 %.", size=8.0)
    fig.savefig(out, facecolor="white"); plt.close(fig); print("wrote", out)

draw(A + "diag_stack.png")                                          # deck version (the slide carries the title)
im = Image.open(A + "diag_stack.png"); Wd, Hd = im.size             # two half-height crops for the deck (rows A and B)
def px(y): return int(round((56.25 - y) / (56.25 - YMIN) * Hd))
im.crop((int(0.004 * Wd), px(55.8), int(0.996 * Wd), px(27.5))).save(A + "diag_stack_model.png")
im.crop((int(0.004 * Wd), px(26.2), int(0.996 * Wd), px(3.4))).save(A + "diag_stack_loops.png")
print("wrote", A + "diag_stack_model.png", A + "diag_stack_loops.png")
draw("/home/user/dreamer4_stack_diagram.png", title="How the parts of Dreamer 4 fit together")
draw("/home/user/dreamer4_stack_diagram.svg", title="How the parts of Dreamer 4 fit together")
