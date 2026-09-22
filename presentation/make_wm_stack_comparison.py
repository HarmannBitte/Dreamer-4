"""Stack comparison of the Minecraft world models in Table 1 of the Dreamer 4 paper: MineWorld, Lucid-v1, Oasis (small/large), Dreamer 4.
One column per model, one row per layer of the stack. Numbers in the context / FPS / tasks rows are Table 1 of arXiv 2509.24527
(one H100; large-Oasis FPS translated from public information). Architecture facts: MineWorld arXiv 2504.08388; Lucid-v1 write-up
(ramimo.substack.com) + github.com/SonicCodes/lucid-v1; Oasis oasis-model.github.io + github.com/etched-ai/open-oasis; Dreamer 4 paper.
Writes /home/user/minecraft_world_models_stack.{png,svg}. Not part of the deck build."""
import glob, os
import matplotlib; matplotlib.use("Agg")
from matplotlib import font_manager
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
for f in glob.glob(os.path.expanduser("~/.fonts/Carlito-*.ttf")) + glob.glob("/usr/share/fonts/truetype/crosextra/Carlito-*.ttf"):
    font_manager.fontManager.addfont(f)
FAM = "Carlito" if any(f.name == "Carlito" for f in font_manager.fontManager.ttflist) else "DejaVu Sans"
NAVY = "#14213D"; BLUE = "#2A56D6"; INK = "#1F2937"; GREY = "#6B7280"; MUTED = "#9AA3B2"; RULE = "#D3D8E2"; PANEL = "#F3F5F8"; SKY = "#E3EAFB"; DEEP = "#DCE3F0"
AMBER = "#B7791F"; SAND = "#FBF1DC"; GREEN = "#1B7F5C"; MINT = "#E1F2EB"
plt.rcParams.update({"font.family": FAM, "text.color": INK})
F = 1.1

MODELS = [  # name, family tag, colour
    ("MineWorld", "discrete autoregressive", AMBER),
    ("Lucid-v1", "latent diffusion / flow", BLUE),
    ("Oasis (small)", "latent diffusion", BLUE),
    ("Oasis (large)", "latent diffusion", BLUE),
    ("Dreamer 4", "latent flow · shortcut forcing", NAVY)]
ROWS = [  # (row label, height, cells...)
    ("who · when · access", 5.0,
     "Microsoft Research · Apr 2025\nopen code + weights\n(300 M / 700 M / 1.2 B)",
     "Rami Seid, independent (FAL-\nsponsored compute) · Nov 2024\nopen weights + inference code",
     "Decart + Etched · Oct 2024\nopen weights, 500 M\n(open-oasis)",
     "Decart + Etched · Oct 2024\nproprietary; playable web demo\nonly; size undisclosed",
     "Google DeepMind · Sep 2025\npaper only — no code, no\nweights; 2 B in total"),
    ("training data", 4.6,
     "VPT contractor recordings\n(open dataset), frames + actions,\n224×384",
     "Minecraft gameplay with actions\n(dataset not detailed in the\nwrite-up)",
     "Minecraft videos with actions\n(OpenAI VPT contractor data)",
     "as the small model, plus\nundisclosed data / compute",
     "VPT contractor data, 2,541 h at\n20 FPS, 360×640; action labels\noptional (learned 'no action')"),
    ("frame → tokens", 6.0,
     "image VQ-VAE (VQGAN init, fine-\ntuned), 16× spatial compression\n→ 14 × 24 = 336 discrete codes\nper frame",
     "own VAE with an extreme\nbottleneck: ≈ 15 latent tokens\nper frame (≈ 600 tokens for\n2 s of play)",
     "ViT-based VAE ('vit-l-20'):\ncontinuous latent grid per frame,\nencoded frame by frame",
     "same ViT VAE design",
     "causal tokenizer: 400 M block-\ncausal transformer, masked-AE\nloss → 256 continuous tokens\n× 32 dims per frame, causal in time"),
    ("backbone · objective", 7.6,
     "LLaMA-style decoder (RMSNorm,\nRoPE), 300 M–1.2 B; next-token\nprediction over the interleaved\nframe-code / action-token\nsequence — the same model is\nworld model and policy",
     "DiT ≈ 1.1 B; diffusion forcing\n('rolling diffusion') in a\nrectified-flow formulation —\nthe v-prediction variant was\nunstable to train",
     "DiT 500 M with temporal-\nattention layers interleaved\nwith spatial ones; diffusion\nforcing: independent noise\nlevel per token",
     "same design, scaled up\n(size undisclosed)",
     "block-causal transformer 1.6 B:\nspace attention + causal time\nattention every 4th layer, GQA,\nregisters; shortcut forcing with\nx-prediction and ramp loss\nweight; later hosts the agent heads"),
    ("actions in", 4.6,
     "11 tokens per step: 7 exclusive\nkey/mouse classes + 2 camera-bin\ntokens + [aBOS]/[aEOS]",
     "keyboard + mouse conditioning\nof the DiT (details unpublished)",
     "keyboard + mouse per frame,\nconditioning the DiT",
     "keyboard + mouse per frame",
     "action tokens per frame (23 keys,\n121-way mouse), interleaved\nwith the latent tokens"),
    ("generating a frame", 6.4,
     "autoregressive over 336 codes;\nparallel 'diagonal' decoding of\nspatially adjacent codes (> 3×\nfaster) — needs the actions in\nadvance → no true real-time play",
     "few flow steps per frame with\na KV cache; 20–30 FPS on one\nRTX 4090 in the released demo",
     "DDIM, 10 steps by default;\ndynamic noising: noise the\ncontext in early passes, remove\nit later, to curb error build-up",
     "same sampler on Decart's\nproprietary inference stack,\nserved from several H100s",
     "K = 4 shortcut steps per frame\n(one forward pass each, step\nsizes learned by self-distillation);\ncontext kept slightly noised"),
    ("context", 3.6, 0.8, 1.0, 1.6, 1.6, 9.6),
    ("speed on one H100 · resolution", 4.0, (2, "384×224", "2"), (44, "640×360", "44"), (20, "640×360", "20"), (5, "360×360", "~5"), (21, "640×360", "21")),
    ("human play-test, 16 tasks", 4.4, (None, "not evaluable: needs\nactions ahead of time"), (0, "generations diverge, interactions fail"), (0, "visual degradation, hallucinated structures"), (5, ""), (14, "")),
    ("beyond the simulator", 4.4,
     "same network can act as a\npolicy (predict action tokens);\nno RL",
     "simulator only",
     "simulator only\n(tech demo)",
     "simulator only\n(demo / product)",
     "agent tokens + policy / reward /\nvalue heads; RL in imagination →\ndiamonds from offline data only")]

def draw(out, title=None):
    top = 60 if title else 56.25
    HH = 4.2; total = HH + 0.5 + sum(r[1] + 0.35 for r in ROWS) + 4.2          # header + rows + footnote
    bottom = 55.0 - total
    fig = plt.figure(figsize=(13.333, 13.333 * (top - bottom) / 100), dpi=200)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 100); ax.set_ylim(bottom, top); ax.axis("off")
    if title:
        ax.text(1.2, 58.5, title, fontsize=15 * F, fontweight="bold", color=NAVY, va="center")
        ax.text(98.8, 58.5, "context · speed · play-test rows = Table 1 of the Dreamer 4 paper; stack details from each project's own sources", fontsize=8.0 * F, color=GREY, va="center", ha="right")
    def text(x, y, s, size=7.4, color=INK, ha="left", va="top", bold=False, ls=1.28, **kw):
        ax.text(x, y, s, fontsize=size * F, color=color, ha=ha, va=va, fontweight=("bold" if bold else "normal"), linespacing=ls, **kw)
    X0 = 14.5; CW = 16.4; GAP = 0.45                         # row-label column 1…13.5, five model columns
    def cx(i): return X0 + i * (CW + GAP)
    y = 55.0
    # column headers
    for i, (name, fam, col) in enumerate(MODELS):
        hero = name == "Dreamer 4"
        ax.add_patch(Rectangle((cx(i), y - HH), CW, HH, fc=(NAVY if hero else PANEL), ec=(NAVY if hero else PANEL), lw=1, zorder=1))
        text(cx(i) + 0.8, y - 0.7, name, size=11, color=("white" if hero else NAVY), bold=True)
        text(cx(i) + 0.8, y - 2.55, fam, size=7.2, color=(SKY if hero else col))
    ax.add_patch(Rectangle((1, y - HH), 12.5, HH, fc="white", ec="white"))
    text(1.2, y - 1.0, "layer of the stack", size=7.2, color=GREY)
    text(1.2, y - 2.4, "Minecraft world\nmodels, 2024–25", size=8.6, color=NAVY, bold=True, ls=1.2)
    y -= HH + 0.5
    for label, h, *cells in ROWS:
        ax.add_patch(Rectangle((1, y - h), 12.5, h, fc=PANEL, ec=PANEL, zorder=1))
        text(1.2, y - 0.6, label, size=7.8, color=NAVY, bold=True)
        for i, c in enumerate(cells):
            hero = i == 4
            ax.add_patch(Rectangle((cx(i), y - h), CW, h, fc=(SKY if hero else "white"), ec=(NAVY if hero else RULE), lw=(1.2 if hero else 0.8), zorder=1))
            if label == "context":
                sec = c; bx, by, bw = cx(i) + 0.8, y - h + 0.9, CW - 1.6
                ax.add_patch(Rectangle((bx, by), bw, 0.9, fc=DEEP if not hero else "#C5D0EE", ec="none", zorder=2))
                ax.add_patch(Rectangle((bx, by), bw * sec / 9.6, 0.9, fc=(NAVY if hero else BLUE), ec="none", zorder=3))
                text(cx(i) + 0.8, y - 0.6, f"{sec:.1f} s" + ("  = 192 frames at 20 FPS" if hero else ""), size=8.2, bold=True, color=(NAVY if hero else INK))
            elif label.startswith("speed"):
                fps, res, lab = c; bx, by, bw = cx(i) + 0.8, y - h + 0.9, CW - 1.6
                ax.add_patch(Rectangle((bx, by), bw, 0.9, fc=DEEP if not hero else "#C5D0EE", ec="none", zorder=2))
                ax.add_patch(Rectangle((bx, by), bw * min(fps, 44) / 44, 0.9, fc=(GREEN if fps >= 20 else AMBER), ec="none", zorder=3))
                ax.plot([bx + bw * 20 / 44] * 2, [by - 0.25, by + 1.15], color=INK, lw=0.8, ls=(0, (2, 1.5)), zorder=4)
                text(cx(i) + 0.8, y - 0.6, f"{lab} FPS  ·  {res}", size=8.2, bold=True, color=(NAVY if hero else INK))
                if i == 0: text(bx + bw * 20 / 44, by - 0.3, "20 FPS = game rate", size=6.2, color=GREY, va="top", ha="center")
            elif label.startswith("human"):
                n, note = c
                if n is None:
                    text(cx(i) + 0.8, y - 0.6, "—", size=9, bold=True); text(cx(i) + 0.8, y - 1.9, note, size=6.9, color=GREY)
                else:
                    text(cx(i) + 0.8, y - 0.6, f"{n} / 16 tasks", size=8.2, bold=True, color=(NAVY if hero else INK))
                    for k in range(16):
                        ax.add_patch(Circle((cx(i) + 1.25 + k * 0.92, y - h + 0.85), 0.32, fc=((NAVY if hero else GREEN) if k < n else "white"), ec=(NAVY if hero else (GREEN if k < n else MUTED)), lw=0.7, zorder=3))
                    if note: text(cx(i) + 0.8, y - 1.8, note, size=6.4, color=GREY, ls=1.15)
            else:
                text(cx(i) + 0.8, y - 0.6, c, size=7.3, color=(NAVY if hero else INK))
        y -= h + 0.35
    text(1.2, y - 0.3, "Sources — MineWorld: Guo et al., arXiv 2504.08388 (their own measurement is 3–6 FPS with parallel decoding; the Dreamer 4 paper measures 2 FPS on one H100). Lucid-v1: ramimo.substack.com and\n"
                       "github.com/SonicCodes/lucid-v1 (1.1 B and 44 FPS per Table 1). Oasis: oasis-model.github.io, the decart.ai blog and github.com/etched-ai/open-oasis. Dreamer 4: Hafner, Yan, Lillicrap, arXiv 2509.24527.\n"
                       "Play-test = a human trying the Dreamer 4 paper's 16 interaction tasks inside each model (Table 1 / Figures 12–14).", size=6.6, color=GREY, ls=1.3)
    fig.savefig(out, facecolor="white"); plt.close(fig); print("wrote", out)

draw("/home/user/minecraft_world_models_stack.png", title="Minecraft world models, stack by stack")
draw("/home/user/minecraft_world_models_stack.svg", title="Minecraft world models, stack by stack")
