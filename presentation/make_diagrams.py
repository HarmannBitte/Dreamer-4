"""Explanatory diagrams for the method primer (flow matching, diffusion forcing, shortcut models, causal tokenizer, interactive dynamics).
All images are illustrations built from one archived world-model frame + synthetic noise; they do not show real model internals."""
import glob, os
import numpy as np
import matplotlib; matplotlib.use("Agg")
from matplotlib import font_manager, patches
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle, FancyBboxPatch
from PIL import Image, ImageFilter
A = "assets/"
for f in glob.glob(os.path.expanduser("~/.fonts/Carlito-*.ttf")) + glob.glob("/usr/share/fonts/truetype/crosextra/Carlito-*.ttf"):
    font_manager.fontManager.addfont(f)
FAM = "Carlito" if any(f.name == "Carlito" for f in font_manager.fontManager.ttflist) else "DejaVu Sans"
NAVY = "#14213D"; BLUE = "#2A56D6"; INK = "#1F2937"; GREY = "#6B7280"; MUTED = "#9AA3B2"; RULE = "#D3D8E2"; PANEL = "#F3F5F8"; SKY = "#9DB8F5"
plt.rcParams.update({"font.family": FAM, "font.size": 11, "text.color": INK, "axes.edgecolor": RULE})
rng = np.random.default_rng(4)

def frame(w=320, h=180):
    im = Image.open(A + "frame_pickaxe_dreamer.jpg").convert("RGB").resize((w, h), Image.LANCZOS)
    return np.asarray(im).astype(np.float32) / 127.5 - 1.0          # [-1, 1]

def noised(x, tau, eps=None):
    eps = rng.normal(size=x.shape).astype(np.float32) if eps is None else eps
    return np.clip(((1 - tau) * eps + tau * x + 1) / 2, 0, 1)

def arrow(ax, x0, y0, x1, y1, color=INK, lw=1.4, style="-|>", ms=12, cs=None, **kw):
    ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle=style, mutation_scale=ms, color=color, lw=lw, connectionstyle=cs or "arc3,rad=0", **kw))

def box(ax, x, y, w, h, text, fc=PANEL, ec=RULE, size=10.5, color=INK, bold=False):
    ax.add_patch(Rectangle((x, y), w, h, fc=fc, ec=ec, lw=1)); ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=size, color=color, fontweight=("bold" if bold else "normal"))

# ------------------------------------------------------------------ 1. flow matching: the signal-level dial
x = frame(); eps = rng.normal(size=x.shape).astype(np.float32)
taus = [0.0, 0.25, 0.5, 0.75, 1.0]
fig = plt.figure(figsize=(10, 3.3), dpi=200)
for i, t in enumerate(taus):
    ax = fig.add_axes([0.03 + i * 0.19, 0.42, 0.175, 0.5]); ax.imshow(noised(x, t, eps)); ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values(): sp.set_edgecolor(BLUE if t in (0.0, 1.0) else RULE); sp.set_linewidth(1.5 if t in (0.0, 1.0) else 0.8)
    ax.set_title(f"τ = {t:g}" + ("   pure noise ε" if t == 0 else "   clean latent x" if t == 1 else ""), fontsize=11, color=(BLUE if t in (0.0, 1.0) else INK), pad=4)
ax = fig.add_axes([0, 0, 1, 0.4]); ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
arrow(ax, 0.04, 0.72, 0.965, 0.72, color=BLUE, lw=2, ms=16)
ax.text(0.5, 0.86, "sampling: start at τ = 0 and walk to τ = 1 in K steps of size d = 1/K,   x(τ+d) = x(τ) + f(x(τ), τ)·d", ha="center", va="center", fontsize=11, color=BLUE)
ax.text(0.5, 0.42, "training: pick a random τ, corrupt the clean latent  x(τ) = (1 − τ)·ε + τ·x,  and ask the network for the way back —", ha="center", fontsize=11)
ax.text(0.5, 0.15, "either the velocity  v = x − ε  (v-prediction)  or the clean latent  x  itself (x-prediction);  they carry the same information:  v = (x − x(τ)) / (1 − τ)", ha="center", fontsize=11, color=GREY)
fig.savefig(A + "diag_flow.png", facecolor="white"); plt.close(fig)

# ------------------------------------------------------------------ 2. diffusion forcing: one noise level per frame
xs = frame(160, 90); T = 8
rows = [("Standard video diffusion\none τ for the whole clip", [0.5] * T, None),
        ("Diffusion forcing (training)\nindependent τ_t per frame", [0.8, 0.3, 0.95, 0.1, 0.6, 0.45, 0.9, 0.2], None),
        ("Diffusion forcing (inference)\nslightly noised past,\nnext frame from noise", [0.95] * (T - 1) + [0.0], "gen")]
fig = plt.figure(figsize=(10, 3.5), dpi=200)
for r, (label, tl, mode) in enumerate(rows):
    y0 = 0.68 - r * 0.31
    fig.text(0.012, y0 + 0.12, label, fontsize=10.5, va="center", color=(BLUE if r else INK), fontweight=("bold" if r else "normal"))
    for t in range(T):
        ax = fig.add_axes([0.255 + t * 0.092, y0, 0.086, 0.24]); ax.imshow(noised(xs, tl[t])); ax.set_xticks([]); ax.set_yticks([])
        for sp in ax.spines.values(): sp.set_edgecolor(BLUE if (mode == "gen" and t == T - 1) else RULE); sp.set_linewidth(1.6 if (mode == "gen" and t == T - 1) else 0.8)
        ax.set_title(f"τ = {tl[t]:g}", fontsize=9.5, color=(BLUE if (mode == "gen" and t == T - 1) else GREY), pad=2)
        if r == 2: ax.set_xlabel(f"t = {t + 1}", fontsize=9.5, color=GREY, labelpad=2)
fig.text(0.94, 0.005, "K = 4 shortcut steps turn the noise into the clean latents ẑ_8, which then become context for t = 9", fontsize=10, color=BLUE, ha="right", fontweight="bold")
fig.text(0.255, 0.955, "time →", fontsize=10, color=GREY)
fig.savefig(A + "diag_forcing.png", facecolor="white"); plt.close(fig)

# ------------------------------------------------------------------ 3. shortcut models: self-consistency across step sizes
fig, (a1, a2) = plt.subplots(1, 2, figsize=(10, 3.4), dpi=200, gridspec_kw={"width_ratios": [1.15, 1]})
tt = np.linspace(0, 1, 200); path = lambda t: 0.08 + 0.5 * t + 0.15 * np.sin(np.pi * t)       # a smooth sketch of the true sampling path
a1.plot(tt, path(tt), color=RULE, lw=6, solid_capstyle="round", zorder=1); a1.text(0.99, path(0.99) - 0.1, "true path from\nnoise to data", ha="right", va="top", fontsize=9, color=MUTED)
t0, d = 0.3, 0.4; p0, p1, p2 = (t0, path(t0)), (t0 + d / 2, path(t0 + d / 2)), (t0 + d, path(t0 + d))
arrow(a1, *p0, *p1, color=GREY, lw=2.2, ms=14); arrow(a1, *p1, *p2, color=GREY, lw=2.2, ms=14)
arrow(a1, *p0, *p2, color=BLUE, lw=2.6, ms=16, cs="arc3,rad=0.28")
for p, lab, dy in ((p0, "x(τ)", -0.12), (p1, "x' after one half-step", 0.09), (p2, "target", 0.09)):
    a1.scatter(*p, s=40, color=(BLUE if p is p2 else INK), zorder=5); a1.text(p[0], p[1] + dy, lab, ha="center", fontsize=9.5, color=(BLUE if p is p2 else INK))
a1.text(0.02, 0.98, "grey: two half-steps of size d/2, computed by the model itself (stop-gradient) → target", fontsize=10, color=GREY, va="top")
a1.text(0.02, 0.89, "blue: one step of size d must land at the same point", fontsize=10.5, color=BLUE, va="top", fontweight="bold")
a1.text(0.99, 0.08, "loss = ‖ f(x(τ), τ, d) − v_target ‖²   (plain flow-matching loss at the smallest step)", ha="right", fontsize=9.5, color=BLUE)
a1.set_xlim(0, 1); a1.set_ylim(0, 1.05); a1.set_yticks([]); a1.set_xticks([0, t0, t0 + d / 2, t0 + d, 1]); a1.set_xticklabels(["τ = 0", "τ", "τ + d/2", "τ + d", "1"], fontsize=9.5)
for sp in ("top", "right", "left"): a1.spines[sp].set_visible(False)
a1.set_title("Training: step-size conditioning + self-consistency", fontsize=11.5, color=NAVY, loc="left", fontweight="bold")
# right: sampling with 4 steps vs 64
a2.set_xlim(-0.02, 1.02); a2.set_ylim(0, 1); a2.axis("off")
a2.text(0, 0.93, "Sampling one frame", fontsize=11.5, color=NAVY, fontweight="bold")
a2.hlines(0.68, 0, 1, color=RULE, lw=1); 
for k in range(4): arrow(a2, k / 4 + 0.005, 0.68, (k + 1) / 4 - 0.005, 0.68, color=BLUE, lw=2.4, ms=14, cs="arc3,rad=-0.5")
a2.text(0.5, 0.86, "shortcut model: K = 4 steps of d = 1/4  →  21 FPS", ha="center", fontsize=10.5, color=BLUE, fontweight="bold")
a2.hlines(0.3, 0, 1, color=RULE, lw=1); a2.vlines(np.linspace(0, 1, 65), 0.27, 0.33, color=GREY, lw=0.8)
a2.text(0.5, 0.42, "ordinary diffusion / diffusion forcing: K = 64 small steps  →  0.8 FPS", ha="center", fontsize=10.5, color=GREY)
a2.text(0, 0.18, "τ = 0 (noise)", fontsize=9.5, color=GREY); a2.text(1, 0.18, "τ = 1 (clean)", fontsize=9.5, color=GREY, ha="right")
a2.text(0.5, 0.04, "same network, same training run — no separate distillation stage", ha="center", fontsize=9.5, color=GREY, style="italic")
fig.tight_layout(); fig.savefig(A + "diag_shortcut.png", facecolor="white"); plt.close(fig)

# ------------------------------------------------------------------ 4. causal tokenizer: masked autoencoding + causal time
im = Image.open(A + "frame_pickaxe_dreamer.jpg").convert("RGB").resize((320, 192), Image.LANCZOS); arr = np.asarray(im)
P = 16; gh, gw = 192 // P, 320 // P
mask = rng.random((gh, gw)) < 0.6; masked = arr.copy()
for i in range(gh):
    for j in range(gw):
        if mask[i, j]: masked[i * P:(i + 1) * P, j * P:(j + 1) * P] = (220, 224, 232)
recon = np.asarray(im.filter(ImageFilter.GaussianBlur(0.7)))
fig = plt.figure(figsize=(8, 4), dpi=240)
def pic(rect, data, title, grid=False):
    ax = fig.add_axes(rect); ax.imshow(data); ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values(): sp.set_edgecolor(RULE)
    if grid:
        for i in range(1, gh): ax.axhline(i * P - 0.5, color="white", lw=0.5, alpha=0.7)
        for j in range(1, gw): ax.axvline(j * P - 0.5, color="white", lw=0.5, alpha=0.7)
    ax.set_title(title, fontsize=10, pad=4); return ax
pic([0.02, 0.56, 0.2, 0.36], arr, "frame t → 16×16 patches", grid=True)
pic([0.245, 0.56, 0.2, 0.36], masked, "training: drop p ~ U(0, 0.9) of them", grid=True)
ov = fig.add_axes([0, 0, 1, 1]); ov.set_xlim(0, 1); ov.set_ylim(0, 1); ov.axis("off"); ov.set_zorder(-1)
box(ov, 0.47, 0.60, 0.085, 0.28, "encoder\n(block-\ncausal\ntrans-\nformer)", size=9.5)
lat = np.tanh(rng.normal(scale=1.2, size=(16, 16)))
axl = fig.add_axes([0.585, 0.585, 0.135, 0.31]); axl.imshow(lat, cmap="Blues", vmin=-1, vmax=1); axl.set_xticks([]); axl.set_yticks([])
for sp in axl.spines.values(): sp.set_edgecolor(BLUE); sp.set_linewidth(1.5)
axl.set_title("latent: 256 tokens × 32 dims\n(tanh bottleneck, continuous)", fontsize=10, color=BLUE, pad=4)
box(ov, 0.745, 0.60, 0.085, 0.28, "decoder", size=9.5)
pic([0.845, 0.56, 0.15, 0.36], recon, "reconstruct all patches\nMSE + 0.2·LPIPS")
for x0, x1 in ((0.225, 0.243), (0.447, 0.468), (0.557, 0.583), (0.722, 0.743), (0.832, 0.843)): arrow(ov, x0, 0.74, x1, 0.74, color=GREY, lw=1.2, ms=10)
ov.text(0.652, 0.53, "→ this is what the dynamics model predicts", ha="center", fontsize=9.5, color=BLUE, style="italic")
# bottom: causal time
ov.text(0.02, 0.4, "Causal in time", fontsize=11.5, color=NAVY, fontweight="bold")
ov.text(0.02, 0.34, "frame t is encoded and decoded from\nframes ≤ t only, so the tokenizer runs\nframe by frame during live play", fontsize=10, color=GREY, va="top", linespacing=1.4)
small = np.asarray(im.resize((160, 96)))
xs_ = [0.34, 0.49, 0.64]
for k, x0 in enumerate(xs_):
    ax = fig.add_axes([x0, 0.06, 0.11, 0.19]); ax.imshow(small); ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values(): sp.set_edgecolor(RULE)
    ax.set_xlabel(["t − 2", "t − 1", "t"][k], fontsize=10, color=INK, labelpad=2)
arrow(ov, 0.395, 0.265, 0.535, 0.265, color=BLUE, lw=1.6, ms=12, cs="arc3,rad=-0.4")
arrow(ov, 0.395, 0.265, 0.685, 0.265, color=BLUE, lw=1.6, ms=12, cs="arc3,rad=-0.4")
arrow(ov, 0.545, 0.265, 0.695, 0.265, color=BLUE, lw=1.6, ms=12, cs="arc3,rad=-0.4")
ov.text(0.545, 0.43, "attention only flows forward in time", ha="center", fontsize=9.5, color=BLUE)
ov.add_patch(Rectangle((0.74, 0.08), 0.255, 0.3, fc=PANEL, ec="none"))
ov.text(0.8675, 0.32, "not a VAE, not a VQ codebook", ha="center", fontsize=10, color=NAVY, fontweight="bold")
ov.text(0.8675, 0.22, "masked autoencoder + tanh bottleneck;\nmasking regularises the latent space →\na smooth target for the dynamics model", ha="center", va="center", fontsize=8.2, color=INK)
ov.text(0.8675, 0.11, "≈ 400 M parameters, trained once, frozen", ha="center", fontsize=8.5, color=GREY, style="italic")
fig.savefig(A + "diag_tokenizer.png", facecolor="white"); plt.close(fig)

# ------------------------------------------------------------------ 5. interactive dynamics: sequence layout + attention pattern
fig = plt.figure(figsize=(8, 4), dpi=240); ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
blocks = [("t − 2", 0.05, "ctx"), ("t − 1", 0.36, "ctx"), ("t", 0.67, "cur")]; bw = 0.28; y0 = 0.43; bh = 0.16
for lab, x0, kind in blocks:
    cur = kind == "cur"
    ax.add_patch(Rectangle((x0, y0), bw, bh, fc=("white" if cur else PANEL), ec=(BLUE if cur else RULE), lw=(1.6 if cur else 1)))
    box(ax, x0 + 0.01, y0 + 0.035, 0.035, 0.09, "a", fc="#E8ECF3", size=10.5)
    box(ax, x0 + 0.05, y0 + 0.035, 0.035, 0.09, "τ d", fc="#E8ECF3", size=9)
    for k in range(12):                                                  # latent tokens
        c = SKY if not cur else (BLUE if rng.random() < 0.5 else "#C7D4F5")
        ax.add_patch(Rectangle((x0 + 0.095 + k * 0.0135, y0 + 0.045), 0.011, 0.07, fc=c, ec="none"))
    box(ax, x0 + 0.262, y0 + 0.035, 0.013, 0.09, "", fc="#E8ECF3", size=8)
    ax.text(x0 + 0.176, y0 - 0.035, "z_t: 256 latent tokens" if not cur else "x(τ_t): noised latents", ha="center", fontsize=9, color=(BLUE if cur else GREY))
    ax.text(x0 + 0.0275, y0 - 0.035, "action", ha="center", fontsize=9, color=GREY); ax.text(x0 + 0.0675, y0 - 0.035, "level,\nstep", ha="center", va="top", fontsize=8.5, color=GREY)
    ax.text(x0 + 0.268, y0 - 0.035, "reg.", ha="center", fontsize=8.5, color=GREY)
    ax.text(x0 + bw / 2, y0 + bh + 0.025, f"frame {lab}" + ("   (context, slightly noised)" if not cur else "   (being predicted)"), ha="center", fontsize=10.5, color=(BLUE if cur else INK), fontweight=("bold" if cur else "normal"))
# attention arcs
arrow(ax, 0.19, y0 + bh + 0.065, 0.84, y0 + bh + 0.065, color=NAVY, lw=1.6, ms=12, cs="arc3,rad=-0.2")
arrow(ax, 0.50, y0 + bh + 0.065, 0.78, y0 + bh + 0.065, color=NAVY, lw=1.6, ms=12, cs="arc3,rad=-0.2")
ax.text(0.5, 0.86, "causal time attention — every 4th layer, over the 192-frame (9.6 s) context", ha="center", fontsize=10.5, color=NAVY, fontweight="bold")
ax.annotate("", xy=(0.68, 0.30), xytext=(0.94, 0.30), arrowprops=dict(arrowstyle="<->", color=BLUE, lw=1.4))
ax.text(0.81, 0.255, "space attention — within one frame, 3 of every 4 layers", ha="center", fontsize=9.5, color=BLUE)
# output
arrow(ax, 0.985, y0 + bh / 2, 0.985, 0.2, color=BLUE, lw=1.4, ms=10, cs="arc3,rad=0")
ax.text(0.985, 0.17, "output: ẑ_t — the clean latents of frame t (x-prediction)", ha="right", fontsize=10, color=BLUE, fontweight="bold")
ax.text(0.985, 0.115, "at inference: K = 4 shortcut steps per frame; ẑ_t becomes context for t + 1", ha="right", fontsize=9, color=GREY)
ax.text(0.015, 0.17, "inputs per frame: actions (23 keys + mouse class, or a learned 'no action' token),", fontsize=9, color=INK)
ax.text(0.015, 0.115, "one (τ_t, d) token, 256 latent tokens, register tokens", fontsize=9, color=INK)
ax.text(0.015, 0.04, "block-causal: everything within a frame sees each other; across frames, only the past. The actions of frame t are visible when predicting frame t.", fontsize=9, color=GREY, style="italic")
fig.savefig(A + "diag_dynamics.png", facecolor="white"); plt.close(fig)
print("diagrams done (font:", FAM + ")")
