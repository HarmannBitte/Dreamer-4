"""Companion to make_stack_diagram.py: the same kind of system diagram for Google DeepMind's Genie 3 (Aug 2025). There is no paper —
facts come from the Genie 3 blog post (deepmind.google/blog/genie-3-a-new-frontier-for-world-models, 5 Aug 2025), the Genie 3 model page,
the Genie 2 blog (Dec 2024), the Genie 1 paper (arXiv 2402.15391), the SIMA 2 announcement (Nov 2025) and the Project Genie launch
coverage (Jan 2026). Everything not stated by DeepMind is marked as inferred or undisclosed. Writes /home/user/genie3_stack_diagram.{png,svg}."""
import glob, os
import matplotlib; matplotlib.use("Agg")
from matplotlib import font_manager
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle
for f in glob.glob(os.path.expanduser("~/.fonts/Carlito-*.ttf")) + glob.glob("/usr/share/fonts/truetype/crosextra/Carlito-*.ttf"):
    font_manager.fontManager.addfont(f)
FAM = "Carlito" if any(f.name == "Carlito" for f in font_manager.fontManager.ttflist) else "DejaVu Sans"
NAVY = "#14213D"; BLUE = "#2A56D6"; INK = "#1F2937"; GREY = "#6B7280"; MUTED = "#9AA3B2"; RULE = "#D3D8E2"; PANEL = "#F3F5F8"; SKY = "#E3EAFB"; DEEP = "#DCE3F0"
AMBER = "#B7791F"; SAND = "#FBF1DC"; GREEN = "#1B7F5C"; MINT = "#E1F2EB"
plt.rcParams.update({"font.family": FAM, "text.color": INK})
F = 1.1; YMIN = 4.0

def draw(out, title=None):
    top = 60 if title else 56.25
    fig = plt.figure(figsize=(13.333, 13.333 * (top - YMIN) / 100), dpi=200)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 100); ax.set_ylim(YMIN, top); ax.axis("off")
    if title:
        ax.text(1.2, 58.5, title, fontsize=15 * F, fontweight="bold", color=NAVY, va="center")
        ax.text(98.8, 58.5, "sources: Genie 3 blog + model page, Genie 1 paper, Genie 2 blog, SIMA 2 and Project Genie coverage\nno Genie 3 paper exists; internals are undisclosed — inferences are marked in amber", fontsize=7.4 * F, color=GREY, va="center", ha="right", linespacing=1.3)

    def box(x, y, w, h, fc="white", ec=RULE, lw=1.0, ls="-", z=1):
        ax.add_patch(Rectangle((x, y), w, h, fc=fc, ec=ec, lw=lw, ls=ls, zorder=z))
    def label(x, y, s, size=10.5, color=NAVY, bold=True, ha="left", va="top", **kw):
        ax.text(x, y, s, fontsize=size * F, color=color, fontweight=("bold" if bold else "normal"), ha=ha, va=va, **kw)
    def body(x, y, s, size=8.4, color=INK, ha="left", va="top", ls=1.32, **kw):
        ax.text(x, y, s, fontsize=size * F, color=color, ha=ha, va=va, linespacing=ls, **kw)
    def chip(x, y, w, h, s, fc=PANEL, ec=RULE, color=INK, size=8.0, bold=False, lw=0.9, ls=1.2, lstyle="-"):
        box(x, y, w, h, fc=fc, ec=ec, lw=lw, ls=lstyle, z=2); ax.text(x + w / 2, y + h / 2, s, fontsize=size * F, color=color, ha="center", va="center", fontweight=("bold" if bold else "normal"), zorder=3, linespacing=ls)
    def arrow(p, q, color=INK, lw=1.2, rad=0.0, ls="-", ms=10, z=4):
        ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=ms, color=color, lw=lw, linestyle=ls, connectionstyle=f"arc3,rad={rad}", zorder=z))
    def route(pts, color=INK, lw=1.1, ls="-", ms=10):
        xs, ys = zip(*pts); ax.plot(xs, ys, color=color, lw=lw, ls=ls, zorder=3, solid_capstyle="round")
        (x0, y0), (x1, y1) = pts[-2], pts[-1]; arrow((x0, y0), (x1, y1), color=color, lw=lw, ms=ms)
    def numeral(x, y, n):
        ax.text(x, y, f"{n:02d}", fontsize=13 * F, color=BLUE, fontweight="bold", ha="left", va="top")
    def small(x, y, s, color=GREY, ha="center", va="top", size=7.4, **kw):
        ax.text(x, y, s, fontsize=size * F, color=color, ha=ha, va=va, **kw)

    yA0, yA1 = 30, 55
    # ------------------------------------------------------------------ 01 inputs
    box(1, yA0, 18.5, yA1 - yA0); numeral(2, 54.3, 1); label(2, 51.6, "Inputs")
    chip(2, 46.6, 16.5, 4.0, "world description — a text prompt\n(+ image: Project Genie sketches it with\nNano Banana Pro or takes your photo)", fc=DEEP, size=7.6)
    chip(2, 41.6, 16.5, 4.0, "navigation actions, every frame\nWASD / arrows, camera, jump;\nfirst- or third-person character", fc=PANEL, size=7.6)
    chip(2, 36.6, 16.5, 4.0, "promptable world events — text\nduring play: weather, new objects,\ncharacters (research preview only)", fc=SAND, ec=AMBER, size=7.6)
    body(2, 35.6, "since I/O May 2026: worlds can be anchored\nin Google Maps Street View imagery", size=7.3, color=GREY, ls=1.25)
    # ------------------------------------------------------------------ 02 the world model
    box(22.5, yA0, 41, yA1 - yA0, ec=NAVY, lw=1.3); numeral(23.5, 54.3, 2)
    label(23.5, 51.6, "Genie 3 world model — what DeepMind states")
    body(23.8, 49.5, "auto-regressive, frame by frame: each new frame is generated from the world\ndescription, the latest actions and the whole trajectory generated so far —\nseveral times per second → 24 FPS at 720p\n\nvisual memory 'as far back as one minute': revisiting a place means attending back\nto what was generated there; worlds stay largely consistent for a few minutes\n\nconsistency is emergent — no explicit 3D representation (unlike NeRFs or\nGaussian splatting), which is why worlds can change on the fly", size=7.7, ls=1.3)
    body(23.8, 40.2, "undisclosed: parameter count, tokenizer / latent space, training data and objective, sampling\nscheme, hardware per session. The '11 B parameters, 200k h of gaming video' figures circulating\nonline are Genie 1's (2024), not Genie 3's.", size=7.3, color=GREY, ls=1.28)
    box(23.8, 30.7, 38.4, 5.9, fc="white", ec=AMBER, lw=1.0, ls=(0, (4, 2)), z=2)
    small(24.4, 36.2, "likely pipeline — the recipe DeepMind published for Genie 2 (Dec 2024), not confirmed for Genie 3:", color=AMBER, ha="left", size=7.0, style="italic")
    for i, s in enumerate(["autoencoder\nframe → latent grid", "large transformer\ndynamics model, causal\nmask as in LLMs", "sample one latent\nframe per step (diffusion,\nclassifier-free guidance)", "decoder\nlatent → 720p frame"]):
        chip(24.6 + i * 9.4, 31.0, 8.4, 3.5, s, fc=SAND, ec=AMBER, size=6.8, lw=0.7)
        if i < 3: arrow((33.0 + i * 9.4, 32.75), (34.0 + i * 9.4, 32.75), color=AMBER, lw=1.0, ms=8)
    # ------------------------------------------------------------------ 03 output / serving
    box(66, yA0, 14, yA1 - yA0); numeral(67, 54.3, 3); label(67, 51.6, "Output · serving")
    body(67, 49.5, "720p frames at 24 FPS,\nstreamed to the browser\n\none accelerator per user\nsession — 'a chip somewhere\nthat's only yours' (Fruchter)\n\nProject Genie: 60-second\nsessions, a compute-cost\nlimit; downloadable video\nof the walkthrough\n\nresearch preview (Aug 2025):\na few minutes of continuous\ninteraction", size=7.5, ls=1.3)
    # ------------------------------------------------------------------ 04 lineage
    box(83, yA0, 16, yA1 - yA0, fc=PANEL, ec=PANEL); numeral(84, 54.3, 4); label(84, 51.6, "The Genie lineage")
    body(84, 49.5, "Genie 1 · Feb 2024 · paper\n11 B; ST-ViViT video tokenizer,\nlatent-action model (8 actions\nlearned without labels), MaskGIT\ndynamics; 2D platformers, ~1 FPS\n\nGenie 2 · Dec 2024 · blog\nautoregressive latent diffusion,\n3D worlds from one image,\nkeyboard + mouse; 10–20 s,\nup to ~1 min; distilled real-time\nvariant at lower quality\n\nGenie 3 · Aug 2025 · blog\nreal-time 24 FPS 720p, minutes,\ntext-to-world, world events\n\nProject Genie · Jan 2026 · AI Ultra\nStreet View grounding · May 2026", size=7.2, ls=1.27)
    yB0, yB1 = 5.5, 25.5
    # ------------------------------------------------------------------ arrows row A
    arrow((19.5, 48.6), (22.5, 48.6)); small(21, 49.0, "prompt", va="bottom", size=6.8)
    arrow((19.5, 43.6), (22.5, 43.6)); small(21, 44.0, "actions", va="bottom", size=6.8)
    arrow((19.5, 38.6), (22.5, 38.6), color=AMBER); small(21, 39.0, "events", color=AMBER, va="bottom", size=6.8)
    arrow((63.5, 48.6), (66, 48.6), color=NAVY); small(64.75, 49.0, "frames", color=NAVY, va="bottom", size=6.8)
    route([(73, yA0), (73, 28.4), (15, 28.4), (15, yB1)], color=MUTED, ls=(0, (3, 2))); small(29, 28.75, "the person sees the frame and acts", va="bottom", size=6.8)
    route([(43, yA0), (43, yB1)], color=NAVY); small(44, 26.7, "the agent's actions in, frames out", color=NAVY, ha="left", va="center", size=6.8)

    # ------------------------------------------------------------------ 05 people playing
    yB0, yB1 = 5.5, 25.5
    box(1, yB0, 27.5, yB1 - yB0); numeral(2, 24.8, 5); label(2, 22.0, "People exploring")
    steps = ["prompt\n→ world", "look, act\n(24 FPS)", "next frame\ngenerated", "new event\nby text"]
    for i, s in enumerate(steps):
        chip(2 + i * 6.5, 15.8, 5.7, 4.2, s, fc=(SAND if i == 3 else PANEL), ec=(AMBER if i == 3 else RULE), size=7.4)
        if i < 3: arrow((7.7 + i * 6.5, 17.9), (8.5 + i * 6.5, 17.9), lw=1.0, ms=8)
    route([(17.35, 15.8), (17.35, 14.6), (11.35, 14.6), (11.35, 15.8)], color=MUTED, ls=(0, (3, 2)), ms=8)
    small(14.35, 14.2, "loop, several times a second", size=6.8)
    body(2, 12.4, "research preview (Aug 2025): a small cohort of academics\nand creators; a few minutes per world; world events on\n\nProject Genie (Jan 2026): AI Ultra subscribers, US, 18+;\nsketch → explore → remix; 60 s per world; 20–24 FPS; no\nworld events yet; adjustable camera; downloadable videos", size=7.6, ls=1.3)
    # ------------------------------------------------------------------ 06 agents in Genie 3 worlds
    box(31.5, yB0, 42.5, yB1 - yB0, ec=BLUE, lw=1.2); numeral(32.5, 24.8, 6); label(32.5, 22.0, "Agents inside Genie 3 worlds — SIMA 2 (Nov 2025)")
    nodes = [("Gemini proposes\na task in the\ngenerated world", PANEL, RULE), ("SIMA 2 acts:\nnavigation actions\nfrom pixels", SKY, BLUE), ("Genie 3 renders the\nconsequences — it\nknows no goal", DEEP, NAVY), ("learned reward\nmodel scores\nthe attempt", PANEL, RULE), ("experience bank →\nnext generation\nof the agent", SKY, BLUE)]
    for i, (s, fc, ec) in enumerate(nodes):
        chip(32.5 + i * 8.25, 15.6, 7.6, 5.4, s, fc=fc, ec=ec, size=7.1)
        if i < 4: arrow((40.1 + i * 8.25, 18.3), (40.75 + i * 8.25, 18.3), lw=1.0, ms=8)
    route([(69.3, 15.6), (69.3, 14.4), (44.55, 14.4), (44.55, 15.6)], color=BLUE, ls=(0, (3, 2)), ms=8)
    small(56.9, 14.05, "self-improvement loop: later generations solve tasks earlier ones failed, without new human data", color=BLUE, size=6.8)
    body(32.5, 11.5, "Aug 2025: SIMA pursued goals ('walk to the glass case') via navigation actions; 'like any other\nenvironment, Genie 3 is not aware of the agent's goal'. Nov 2025: SIMA 2 (Gemini 2.5 Flash Lite\ncore) learns in Genie 3 worlds from Gemini-written tasks and a learned reward model. The world\nmodel is only the environment; agent, rewards and learning live outside it. Stated purpose:\nevaluating and training embodied agents and robots, incl. on counterfactual 'what-if' events.", size=7.2, ls=1.3)
    # ------------------------------------------------------------------ 07 limitations + Dreamer 4 contrast
    box(77, 15.6, 22, yB1 - 15.6); numeral(78, 24.8, 7); label(78, 22.0, "Stated limitations")
    body(78, 20.2, "limited action space — events are not\nperformed by the agent · multi-agent\ninteraction · geographic accuracy ·\nlegible text only if prompted · minutes,\nnot hours · (Project Genie: control latency,\nprompt / physics adherence)", size=7.0, ls=1.25)
    box(77, yB0, 22, 10.6, fc=PANEL, ec=PANEL); label(78, 14.6, "Where Dreamer 4 differs", size=8.6)
    body(78, 12.9, "· any world from text vs. one game learned\n  from 2,541 h of Minecraft video\n· navigation (+ one 'interact') vs. full\n  keyboard + mouse incl. GUI crafting\n· ~1 min visual memory vs. 9.6 s context;\n  24 FPS 720p vs. 21 FPS 360p\n· agent outside (SIMA 2 + Gemini rewards)\n  vs. policy trained by RL inside the model\n· blog + product vs. paper; neither open", size=7.0, ls=1.25)
    fig.savefig(out, facecolor="white"); plt.close(fig); print("wrote", out)

draw("/home/user/genie3_stack_diagram.png", title="How the parts of Genie 3 fit together — as far as is public")
draw("/home/user/genie3_stack_diagram.svg", title="How the parts of Genie 3 fit together — as far as is public")
