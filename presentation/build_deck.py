"""Build the Dreamer 4 deep-dive deck (python-pptx). Run: python3 build_deck.py
All numbers come from Hafner, Yan, Lillicrap, "Training Agents Inside of Scalable World Models" (arXiv 2509.24527)
as digested in ../dreamer4_research_report.md; figures are from the paper/project page (credited on each slide)."""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.ns import qn
from lxml import etree
from PIL import Image, ImageEnhance
import os

A = "assets/"
NAVY = RGBColor(0x14, 0x21, 0x3D); BLUE = RGBColor(0x2F, 0x5B, 0xEA); TEAL = RGBColor(0x1F, 0xB5, 0xA6)
PURPLE = RGBColor(0x8B, 0x5C, 0xF6); RED = RGBColor(0xEF, 0x53, 0x50); GREY = RGBColor(0x6B, 0x72, 0x80)
LIGHT = RGBColor(0xF3, 0xF5, 0xF9); WHITE = RGBColor(0xFF, 0xFF, 0xFF); DARK = RGBColor(0x1F, 0x29, 0x37)
PALE_BLUE = RGBColor(0xE4, 0xEB, 0xFC); AMBER = RGBColor(0xF5, 0x9E, 0x0B)
FONT = "Calibri"
W, H = Inches(13.333), Inches(7.5)

prs = Presentation(); prs.slide_width = W; prs.slide_height = H
BLANK = prs.slide_layouts[6]
FOOTER = "Dreamer 4 — Hafner*, Yan*, Lillicrap (Google DeepMind), arXiv 2509.24527, Sep 2025"
state = {"n": 0}

# ---------------------------------------------------------------- helpers
def _font(run_or_p, size, bold=False, color=DARK, italic=False, name=FONT):
    f = run_or_p.font; f.size = Pt(size); f.bold = bold; f.italic = italic; f.name = name; f.color.rgb = color

import re
_MARK = re.compile(r"(?<!\w)\*\*(?=\S)(.+?)(?<=\S)\*\*(?!\w)|(?<!\w)\*(?=\S)(.+?)(?<=\S)\*(?!\w)")

def add_runs(p, text, size, color=DARK, bold=False, italic=False):
    """Add runs to paragraph p, honouring **bold** and *italic* inline markup (author asterisks like 'Hafner*' are left alone)."""
    pos = 0
    for m in _MARK.finditer(text):
        if m.start() > pos:
            r = p.add_run(); r.text = text[pos:m.start()]; _font(r, size, bold, color, italic)
        if m.group(1) is not None:
            r = p.add_run(); r.text = m.group(1); _font(r, size, True, color, italic)
        else:
            r = p.add_run(); r.text = m.group(2); _font(r, size, bold, color, True)
        pos = m.end()
    if pos < len(text) or not text:
        r = p.add_run(); r.text = text[pos:]; _font(r, size, bold, color, italic)

def add_text(slide, left, top, width, height, text, size=18, bold=False, color=DARK, align=PP_ALIGN.LEFT,
             anchor=MSO_ANCHOR.TOP, italic=False, line_spacing=1.05):
    tb = slide.shapes.add_textbox(left, top, width, height); tf = tb.text_frame; tf.word_wrap = True
    tf.vertical_anchor = anchor; tf.margin_left = tf.margin_right = Inches(0.05); tf.margin_top = tf.margin_bottom = Inches(0.02)
    lines = text if isinstance(text, list) else [text]
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align; p.line_spacing = line_spacing
        add_runs(p, line, size, color, bold, italic)
    return tb

def _bullet(p, level, char="•"):
    pPr = p._p.get_or_add_pPr()
    mar = Inches(0.28 + 0.32 * level); pPr.set("marL", str(int(mar))); pPr.set("indent", str(int(-Inches(0.24))))
    for tag in ("a:buNone", "a:buChar", "a:buAutoNum"):
        for el in pPr.findall(qn(tag)): pPr.remove(el)
    bf = etree.SubElement(pPr, qn("a:buFont")); bf.set("typeface", "Arial")
    bc = etree.SubElement(pPr, qn("a:buChar")); bc.set("char", char)

def add_bullets(slide, left, top, width, height, items, size=18, color=DARK, space=6, bold_lead=True):
    """items: list of str or (str, level). A leading '**text**' segment becomes bold."""
    tb = slide.shapes.add_textbox(left, top, width, height); tf = tb.text_frame; tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.05)
    for i, it in enumerate(items):
        txt, lvl = (it, 0) if isinstance(it, str) else it
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(space); p.line_spacing = 1.05
        sz = size if lvl == 0 else size - 2
        add_runs(p, txt, sz, color)
        _bullet(p, lvl, "•" if lvl == 0 else "–")
    return tb

def fit_picture(slide, path, left, top, max_w, max_h, align="center"):
    im = Image.open(path); ar = im.width / im.height
    w = max_w; h = int(w / ar)
    if h > max_h: h = max_h; w = int(h * ar)
    dx = (max_w - w) // 2 if align == "center" else 0
    return slide.shapes.add_picture(path, left + dx, top, width=w, height=h)

def caption(slide, left, top, width, text, size=10.5):
    return add_text(slide, left, top, width, Inches(0.5), text, size=size, color=GREY, italic=True)

def chrome(slide, title, subtitle=None, dark=False):
    state["n"] += 1
    if not dark:
        bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, W, Inches(0.12)); bar.fill.solid(); bar.fill.fore_color.rgb = NAVY; bar.line.fill.background()
        acc = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, Inches(0.12), Inches(1.6), Inches(0.05)); acc.fill.solid(); acc.fill.fore_color.rgb = BLUE; acc.line.fill.background()
        add_text(slide, Inches(0.5), Inches(0.32), Inches(12.3), Inches(0.75), title, size=26, bold=True, color=NAVY)
        if subtitle: add_text(slide, Inches(0.52), Inches(0.98), Inches(12.3), Inches(0.45), subtitle, size=15, color=GREY)
        add_text(slide, Inches(0.5), Inches(7.05), Inches(10), Inches(0.35), FOOTER, size=9.5, color=GREY)
    add_text(slide, Inches(12.2), Inches(7.05), Inches(0.8), Inches(0.35), str(state["n"]), size=10, color=(WHITE if dark else GREY), align=PP_ALIGN.RIGHT)

def notes(slide, text):
    slide.notes_slide.notes_text_frame.text = text

def new_slide(title, subtitle=None):
    s = prs.slides.add_slide(BLANK); chrome(s, title, subtitle); return s

def section(title, sub, n):
    s = prs.slides.add_slide(BLANK)
    bg = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, W, H); bg.fill.solid(); bg.fill.fore_color.rgb = NAVY; bg.line.fill.background()
    acc = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.9), Inches(3.05), Inches(1.2), Inches(0.08)); acc.fill.solid(); acc.fill.fore_color.rgb = TEAL; acc.line.fill.background()
    add_text(s, Inches(0.9), Inches(1.9), Inches(11), Inches(1.0), f"Part {n}", size=20, color=TEAL, bold=True)
    add_text(s, Inches(0.9), Inches(3.25), Inches(11.5), Inches(1.3), title, size=44, bold=True, color=WHITE)
    add_text(s, Inches(0.9), Inches(4.5), Inches(11), Inches(1.2), sub, size=20, color=RGBColor(0xC9, 0xD3, 0xE6))
    chrome(s, title, dark=True); return s

def add_table(slide, left, top, width, rows, col_widths=None, font=12, header_fill=NAVY, highlight_col=None, highlight_row=None, row_h=0.36):
    nr, nc = len(rows), len(rows[0])
    shp = slide.shapes.add_table(nr, nc, left, top, width, Inches(row_h * nr)); t = shp.table
    if col_widths:
        for i, cw in enumerate(col_widths): t.columns[i].width = Inches(cw)
    if nr > 1 and row_h > 0.45:  # keep the header row compact even when body rows are tall
        t.rows[0].height = Inches(0.42)
    for r in range(nr):
        for c in range(nc):
            cell = t.cell(r, c); cell.text = ""; cell.margin_left = cell.margin_right = Inches(0.06); cell.margin_top = cell.margin_bottom = Inches(0.03)
            p = cell.text_frame.paragraphs[0]; txt = str(rows[r][c])
            hdr = (r == 0)
            add_runs(p, txt, font, color=WHITE if hdr else DARK, bold=hdr or (highlight_col == c and r > 0) or (highlight_row == r))
            p.alignment = PP_ALIGN.LEFT if (c == 0 or len(txt) > 28) else PP_ALIGN.CENTER
            cell.fill.solid()
            if hdr: cell.fill.fore_color.rgb = header_fill
            elif highlight_row == r or (highlight_col == c): cell.fill.fore_color.rgb = PALE_BLUE
            else: cell.fill.fore_color.rgb = WHITE if r % 2 else LIGHT
    return t

def box(slide, left, top, width, height, title, body, fill=PALE_BLUE, title_color=NAVY, size=13):
    b = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height); b.fill.solid(); b.fill.fore_color.rgb = fill; b.line.fill.background()
    b.adjustments[0] = 0.08
    add_text(slide, left + Inches(0.12), top + Inches(0.08), width - Inches(0.24), Inches(0.4), title, size=size + 2, bold=True, color=title_color)
    add_text(slide, left + Inches(0.12), top + Inches(0.5), width - Inches(0.24), height - Inches(0.55), body if isinstance(body, list) else [body], size=size, color=DARK)
    return b

def arrow(slide, left, top, width=Inches(0.45), height=Inches(0.5), color=GREY):
    a = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, left, top, width, height); a.fill.solid(); a.fill.fore_color.rgb = color; a.line.fill.background(); return a

def jpeg(path, max_w=1600, q=85):
    """Downscale/convert an asset to JPEG to keep the deck small; returns new path."""
    out = path.rsplit(".", 1)[0] + "_s.jpg"
    if os.path.exists(out): return out
    im = Image.open(path).convert("RGB")
    if im.width > max_w: im = im.resize((max_w, int(im.height * max_w / im.width)), Image.LANCZOS)
    im.save(out, quality=q, optimize=True); return out

# ================================================================ SLIDES
# 1 Title -----------------------------------------------------------------
s = prs.slides.add_slide(BLANK); state["n"] += 1
bgsrc = A + "frame_teaser_1.jpg"; im = Image.open(bgsrc).convert("RGB"); im = ImageEnhance.Brightness(im).enhance(0.35); im.save(A + "title_bg.jpg", quality=85)
s.shapes.add_picture(A + "title_bg.jpg", 0, 0, width=W, height=H)
add_text(s, Inches(0.8), Inches(1.5), Inches(11.5), Inches(0.5), "PAPER DEEP DIVE", size=16, bold=True, color=TEAL)
add_text(s, Inches(0.8), Inches(2.0), Inches(11.8), Inches(1.4), "Dreamer 4", size=66, bold=True, color=WHITE)
add_text(s, Inches(0.8), Inches(3.2), Inches(11.8), Inches(1.0), "Training Agents Inside of Scalable World Models", size=32, color=WHITE)
add_text(s, Inches(0.8), Inches(4.25), Inches(11.8), Inches(0.9), ["Danijar Hafner*, Wilson Yan*, Timothy Lillicrap — Google DeepMind", "arXiv 2509.24527 · 29 September 2025 · danijar.com/dreamer4"], size=18, color=RGBColor(0xD6, 0xDE, 0xEE))
add_text(s, Inches(0.8), Inches(6.3), Inches(11.8), Inches(0.5), "Presenter: ____________    ·    Date: ____________    ·    ~45–60 min incl. discussion", size=14, color=RGBColor(0xB8, 0xC2, 0xD6))
notes(s, "Welcome. This is a deep dive into Dreamer 4, the September 2025 DeepMind paper by Danijar Hafner, Wilson Yan and Tim Lillicrap. "
         "Headline: an agent that learns to obtain diamonds in Minecraft purely from offline video, by training inside a learned world model that runs in real time on a single GPU. "
         "Background image: a frame of the official teaser video from the project page.")

# 2 Agenda -----------------------------------------------------------------
s = new_slide("Agenda")
add_bullets(s, Inches(0.7), Inches(1.5), Inches(6), Inches(5), [
    "**Part 1 — Background:** why world models, what made scaling them hard, the offline diamond challenge",
    "**Part 2 — Method:** tokenizer, dynamics transformer, shortcut forcing, agent tokens, imagination training (PMPO)",
    "**Part 3 — Experiments:** real-time human play-testing, diamond challenge, ablations, learning from unlabeled video, robotics",
    "**Part 4 — Discussion:** limitations, critical reading, future work, takeaways",
    "**Appendix:** hyper-parameters, full tables, glossary"], size=18, space=12)
box(s, Inches(7.3), Inches(1.6), Inches(5.4), Inches(4.4), "How to read this deck", [
    "• Equations are kept to the minimum needed for intuition; the appendix has the exact settings.",
    "• Every number is from the paper's tables (Table 1, 2, 7, 8) or the authors' talks — sources are on each slide.",
    "• Figures: © the authors (arXiv 2509.24527 / danijar.com), reproduced for discussion.",
    "• Suggested pacing: Parts 1–2 ≈ 25 min, Part 3 ≈ 15 min, Part 4 ≈ 10 min + Q&A."], size=13)
notes(s, "Four parts plus an appendix. For a mixed audience I'll spend most time on the method intuition and on what the experiments do and do not show.")

# 3 TL;DR -----------------------------------------------------------------
s = new_slide("Dreamer 4 in one slide", "What the paper claims, and the evidence behind each claim")
rows = [["Claim", "Evidence in the paper"],
        ["First agent to obtain diamonds in Minecraft from offline data only", "0.7 % of 1,000 × 60-min episodes reach a diamond; 29 % reach an iron pickaxe (vs 11 % for a Gemma-3 VLA, 0.6 % for BC) — Table 7"],
        ["A world model that simulates Minecraft object interactions and menus accurately, in real time on 1 GPU", "Human play-testers solve 14/16 interaction tasks inside it at 21 FPS with a 9.6 s context (Oasis: 5/16, Lucid-v1: 0/16) — Table 1"],
        ["Shortcut forcing + an efficient transformer make this fast", "4 sampling steps instead of 16–64; FVD 306 → 57 across the design cascade while going from 0.8 to 21 FPS — Table 2, Fig. 8"],
        ["Action conditioning can be learned from few labels", "100 h of labeled actions ≈ 85 % PSNR / 100 % SSIM of using all 2,541 h; actions transfer to Nether/End seen only unlabeled — Fig. 7"],
        ["~100× less data than VPT, no environment interaction", "2,541 h contractor video vs VPT's 270 K h web video + online RL — Table 3"]]
add_table(s, Inches(0.5), Inches(1.55), Inches(12.3), rows, col_widths=[4.6, 7.7], font=12.5, row_h=0.8)
notes(s, "If you remember one slide, it's this one. Five claims, each tied to a table or figure. Note the honesty in the numbers: diamonds are rare (0.7 %), but every earlier milestone is reached far more reliably and faster than by the baselines, all without a single environment step.")

# ---- Part 1 -------------------------------------------------------------
section("Background & motivation", "World models, learning in imagination, and why Minecraft from offline data is a hard test", 1)

# 5 Why world models ---------------------------------------------------------
s = new_slide("Why world models? Learning in imagination", "The Dreamer lineage: same idea, increasingly capable simulators")
add_bullets(s, Inches(0.6), Inches(1.55), Inches(6.4), Inches(4.2), [
    "**World model:** a learned simulator that predicts what happens next given the current situation and an action",
    "**Imagination training:** the policy is optimised on rollouts generated *by the model*, not by the real environment — cheap, parallel, safe",
    "**Why it matters now:** robots and other real-world systems cannot afford millions of trial-and-error interactions; video on the internet is abundant",
    "**Dreamer 4's bet:** if the simulator is accurate enough about object interactions, RL inside it can go beyond what pure imitation learns"], size=17)
# timeline
y = Inches(6.0); xs = [0.7, 3.7, 6.7, 9.7]; items = [("Dreamer (2019)", "latent imagination on DM Control"), ("DreamerV2 (2020)", "discrete latents, Atari"), ("DreamerV3 (2023/Nature 2025)", "one config for 150+ tasks; diamonds with online RL"), ("Dreamer 4 (2025)", "transformer diffusion WM; diamonds offline; real-time on 1 GPU")]
ln = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.9), y + Inches(0.18), Inches(11.4), Inches(0.04)); ln.fill.solid(); ln.fill.fore_color.rgb = GREY; ln.line.fill.background()
for (x, (t, d)) in zip(xs, items):
    dot = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x + 0.1), y + Inches(0.05), Inches(0.3), Inches(0.3)); dot.fill.solid(); dot.fill.fore_color.rgb = BLUE if "4" in t else NAVY; dot.line.fill.background()
    add_text(s, Inches(x), y + Inches(0.4), Inches(2.9), Inches(0.8), [t, d], size=11, color=DARK)
fit_picture(s, A + "frame_imag_treechop.jpg", Inches(7.3), Inches(1.6), Inches(5.5), Inches(3.4))
caption(s, Inches(7.3), Inches(5.05), Inches(5.5), "Imagined rollout decoded for visualisation, with the agent's reward and value estimates (project page, 'Gather wood').")
notes(s, "The core idea has been constant since the first Dreamer in 2019: learn a model of the environment, then train the policy on imagined trajectories. "
         "What changed in Dreamer 4 is the simulator: a 2-billion-parameter block-causal transformer trained with a diffusion-style objective, accurate enough that a human can play inside it. "
         "The frame on the right is an imagined rollout, not the real game.")

# 6 What made it hard ------------------------------------------------------------
s = new_slide("What made scalable world models hard before", "Three requirements pulled in different directions")
box(s, Inches(0.5), Inches(1.6), Inches(4.0), Inches(2.6), "1 · Fidelity of interactions", ["Video generators look good but get game mechanics wrong: inventories, crafting menus, breaking blocks, placing a boat and riding it.", "Prior Minecraft world models (Oasis, Lucid-v1, MineWorld) fail most such tasks."], fill=LIGHT)
box(s, Inches(4.67), Inches(1.6), Inches(4.0), Inches(2.6), "2 · Speed", ["Imagination RL needs millions of generated frames — and a human tester needs ≥ 20 FPS.", "Diffusion transformers spend tens of denoising steps per frame: 0.8 FPS for the baseline in this paper."], fill=LIGHT)
box(s, Inches(8.84), Inches(1.6), Inches(4.0), Inches(2.6), "3 · Memory & drift", ["Autoregressive video drifts: small errors feed back into the context.", "Short contexts (1–2 s in prior models) forget what is behind the player."], fill=LIGHT)
add_bullets(s, Inches(0.6), Inches(4.5), Inches(12.2), Inches(2.3), [
    "**Dreamer 3's RSSM** is fast (~1,000× faster than a diffusion transformer) but operates at 64×64 pixels and needed abstract inventory state and crafting actions — not raw mouse & keyboard",
    "**Dreamer 4's answer:** a diffusion transformer that needs only 4 sampling steps (shortcut forcing), an architecture tuned for long context at low cost, and training tricks that keep long rollouts stable (x-prediction, noised context)"], size=16)
notes(s, "Three tensions: fidelity versus speed versus stability over long horizons. Prior Minecraft world models chose speed and looked plausible, but a human trying to craft a pickaxe inside them fails. "
         "The recurrent Dreamer 3 model was fast but low-resolution and relied on privileged state. Dreamer 4 tries to get all three at once.")

# 7 The offline diamond challenge -------------------------------------------------
s = new_slide("The test bed: the offline diamond challenge", "No environment interaction at all — learn everything from 2,541 hours of human gameplay video")
add_bullets(s, Inches(0.6), Inches(1.55), Inches(6.6), Inches(5.2), [
    "**Data:** OpenAI VPT contractor recordings (subsets 6–10), 2,541 h at 360×640, 20 FPS, with mouse & keyboard labels; 90/10 train/eval split by 5-minute chunk",
    "**Actions:** 23 binary keys + 121-way mouse class (11×11 foveated bins, VPT convention) — no abstract 'craft' actions",
    "**Evaluation:** 1,000 fresh random worlds, empty inventory, 60 min each (72,000 actions at 20 FPS); a fixed prompt sequence walks the agent through the 12-item tech tree",
    "**Why it is hard:** diamonds sit ~24,000 actions deep for a human; rewards are sparse; offline data covers the late tech tree thinly; every skill (chop → craft → mine → smelt) must chain without a single trial in the real game",
    "**Baselines, all on the same data:** VPT fine-tuned, BC, BC without task input, a VLA built on Gemma 3, and 'WM + BC' (Dreamer 4 without imagination RL)"], size=15.5)
fit_picture(s, A + "frame_diamond_dreamer.jpg", Inches(7.5), Inches(1.6), Inches(5.3), Inches(3.0))
caption(s, Inches(7.5), Inches(4.62), Inches(5.3), "Diamond ore, as simulated by the world model during a human 'mine diamonds' session (project page).")
tree = "log → planks → crafting table → stick → wooden pickaxe → cobblestone → stone pickaxe → iron ore → furnace → iron ingot → iron pickaxe → diamond"
box(s, Inches(7.5), Inches(5.1), Inches(5.3), Inches(1.6), "The 12 milestones (Table 5)", [tree], fill=PALE_BLUE, size=12)
notes(s, "Offline means offline: the agent never touches Minecraft during training. The only signal is human gameplay video with logged inputs. "
         "Diamonds need a long chain of subgoals, each executed with raw mouse and keyboard at 20 Hz. That is why success rates fall off steeply along the tech tree for every method.")

# ---- Part 2 -------------------------------------------------------------
section("Method", "One transformer, three phases: world-model pretraining → agent fine-tuning → imagination training", 2)

# 9 Three phases ---------------------------------------------------------------
s = new_slide("Overview: three phases, one transformer", "Algorithm 1 in the paper")
cols = [("Phase 1 · World-model pretraining", ["Train the causal tokenizer (masked autoencoding), then freeze it", "Train the interactive dynamics model on tokenized video ± actions with shortcut forcing", "Inputs: all 2,541 h, labeled or not"], BLUE),
        ("Phase 2 · Agent fine-tuning", ["Insert agent tokens with task embedding; add policy & reward heads", "Behavioural cloning with multi-token prediction (L = 8) on task-relevant data", "Dynamics loss continues on uniform data so the model stays honest"], TEAL),
        ("Phase 3 · Imagination training", ["Freeze the transformer; train policy + value heads only", "Roll out the policy inside the world model, reward from the learned reward head", "PMPO with reverse-KL to the frozen BC policy; γ = 0.997"], PURPLE)]
x = Inches(0.5)
for i, (t, body, col) in enumerate(cols):
    b = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(1.65), Inches(3.85), Inches(3.5)); b.fill.solid(); b.fill.fore_color.rgb = LIGHT; b.line.color.rgb = col; b.line.width = Pt(2); b.adjustments[0] = 0.06
    hd = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, Inches(1.65), Inches(3.85), Inches(0.6)); hd.fill.solid(); hd.fill.fore_color.rgb = col; hd.line.fill.background(); hd.adjustments[0] = 0.3
    add_text(s, x + Inches(0.1), Inches(1.7), Inches(3.65), Inches(0.5), t, size=14, bold=True, color=WHITE, anchor=MSO_ANCHOR.MIDDLE)
    add_bullets(s, x + Inches(0.1), Inches(2.4), Inches(3.65), Inches(2.7), body, size=13, space=5)
    if i < 2: arrow(s, x + Inches(3.9), Inches(3.15), Inches(0.35), Inches(0.5))
    x += Inches(4.25)
add_bullets(s, Inches(0.6), Inches(5.4), Inches(12.2), Inches(1.6), [
    "**Key design choice:** the same block-causal transformer serves as tokenizer, dynamics model and agent backbone; policy and value are tiny heads on 'agent tokens'",
    "**Data mix in phases 2–3:** 50 % uniform sequences / 50 % task-relevant; BC loss only on relevant data, dynamics loss only on uniform data ('to avoid optimistic generations')"], size=14.5)
notes(s, "Three phases. First a world model is trained on all video. Second, agent tokens and heads are added and trained by behavioural cloning while the dynamics loss keeps running. Third, the transformer is frozen and only the policy and value heads are trained by RL on imagined rollouts. "
         "Keeping the dynamics loss on uniform data rather than task-relevant data is a small but deliberate choice to avoid a world model that is optimistic about task success.")

# 10 World model design ----------------------------------------------------------
s = new_slide("World-model design", "Figure 2: causal tokenizer + interactive dynamics model, one shared block-causal transformer")
fit_picture(s, A + "fig2_world_model_design.png", Inches(0.5), Inches(1.55), Inches(7.6), Inches(3.4))
caption(s, Inches(0.5), Inches(5.0), Inches(7.6), "Left: causal tokenizer (masked patches → latent tokens → reconstruction). Right: interactive dynamics — interleaved action tokens a, latent tokens z, and per-frame signal level τ / step size d; space layers with a causal time layer every 4th block. (Figure 2, arXiv 2509.24527)")
add_bullets(s, Inches(8.4), Inches(1.6), Inches(4.5), Inches(5.2), [
    "**Total 2 B parameters:** ≈ 400 M tokenizer + 1.6 B dynamics",
    "**Frames:** 360×640, zero-padded to 384×640 → 960 patches of 16×16",
    "**Latents:** N_z = 256 tokens × 32 dims per frame (512×16 bottleneck, tanh)",
    "**Context:** 192 frames = 9.6 s at 20 FPS",
    "**Block-causal:** full attention within a frame, causal across frames → usable online, frame by frame",
    "**Transformer recipe:** pre-RMSNorm, RoPE, SwiGLU, QK-norm, logit soft-capping, register tokens"], size=14.5)
notes(s, "Both halves use the same transformer block. Block-causal means every token in frame t can see all tokens of frames up to t, which is exactly what you need for online, frame-by-frame generation with a human or a policy in the loop.")

# 11 Tokenizer ---------------------------------------------------------------
s = new_slide("The causal tokenizer", "Compress each frame into 256 latent tokens without looking into the future")
add_bullets(s, Inches(0.6), Inches(1.55), Inches(7.4), Inches(5.3), [
    "**Masked autoencoder, not a VAE/VQ:** patches are dropped with ratio ~ U(0, 0.9) during training; encoder sees the surviving patches plus learned latent tokens, decoder reconstructs all patches",
    "**Loss:** MSE + 0.2 · LPIPS (perceptual term keeps textures crisp)",
    "**Bottleneck:** 512×16 per frame with tanh squashing, reshaped to 256 tokens × 32 dims for the dynamics model — a *continuous* latent, no codebook",
    "**Causal in time:** frame t is encoded/decoded using only frames ≤ t → the same tokenizer works during live interaction",
    "**Why MAE-style?** Inspired by MAETok (masked autoencoders make good tokenizers for diffusion models): masking regularises the latent space so the dynamics model has an easier, smoother target",
    "**Trained once, then frozen** — Hafner expects fully end-to-end training to be possible eventually"], size=15)
fit_picture(s, A + "fig_tok.png", Inches(8.3), Inches(1.7), Inches(4.5), Inches(3.9))
caption(s, Inches(8.3), Inches(5.65), Inches(4.5), "Figure 2a (arXiv HTML render).")
notes(s, "The tokenizer is a masked autoencoder over 16×16 patches with a small continuous bottleneck. Two properties matter downstream: it is causal in time, and its latent space is smooth because of the heavy masking during training. "
         "Everything after this operates on 256 latent tokens per frame instead of 960 patches.")

# 12 Dynamics model ---------------------------------------------------------------
s = new_slide("The interactive dynamics model", "Predict the next frame's latents from past latents, actions and the current noisy guess")
add_bullets(s, Inches(0.6), Inches(1.55), Inches(7.6), Inches(5.3), [
    "**Sequence layout:** per frame, action tokens (23 keys + mouse class, or a learned 'no action' embedding for unlabeled video), then 256 latent tokens, plus a token carrying signal level τ and step size d",
    "**Attention pattern:** space-only attention inside a frame in 3 of every 4 layers; a *causal time* layer every 4th layer sees the 192-frame context → most compute is spent on cheap per-frame attention",
    "**Efficiency tricks:** grouped-query attention, register tokens, alternating batch lengths (64-frame short batches interleaved with 256-frame long batches — long context is learned without paying for it every step)",
    "**Objective:** shortcut forcing — a diffusion/flow objective that (i) noises every frame independently and (ii) is conditioned on the step size so that 4 sampling steps suffice (next slides)",
    "**Inference:** 21 FPS at 640×360 on one H100 with K = 4 steps; context frames are kept slightly noisy (τ_ctx ≈ 0.1) so the model tolerates its own imperfections"], size=14.5)
fit_picture(s, A + "fig_dyn.png", Inches(8.5), Inches(1.7), Inches(4.3), Inches(3.9))
caption(s, Inches(8.5), Inches(5.65), Inches(4.3), "Figure 2b (arXiv HTML render).")
notes(s, "The dynamics model reads the interleaved sequence of actions and latents. Only every fourth layer attends across time; the rest work within one frame. That is what makes a 9.6 s context affordable. "
         "Alternating short and long batches is a training-cost trick: it cut a training step from 9.8 s to 1.5 s in the ablation (Table 2).")

# 13 Diffusion primer ---------------------------------------------------------------
s = new_slide("Two-minute primer: flow matching, signal level τ, x vs v", "Just enough background for shortcut forcing")
box(s, Inches(0.5), Inches(1.6), Inches(6.1), Inches(2.55), "Flow matching view of diffusion", [
    "Interpolate between noise ε and clean latent x:  z_τ = τ · x + (1 − τ) · ε,  τ ∈ [0, 1]  (τ = signal level).",
    "A network learns to move z_τ toward x; sampling integrates from τ = 0 (pure noise) to τ = 1 (clean) in K steps.",
    "Standard models need many small steps because the learned direction is only locally correct."], fill=LIGHT, size=12.5)
box(s, Inches(6.75), Inches(1.6), Inches(6.1), Inches(2.55), "Two parameterisations of the same target", [
    "v-prediction: output the velocity  v = x − ε  (common in image/video diffusion).",
    "x-prediction: output the clean latent x directly; the velocity follows as (x − z_τ)/(1 − τ).",
    "Mathematically equivalent — numerically very different when errors feed back autoregressively (slide 15)."], fill=LIGHT, size=12.5)
box(s, Inches(0.5), Inches(4.35), Inches(6.1), Inches(2.45), "Diffusion forcing (Chen et al., 2024)", [
    "Give every frame in the sequence its *own* noise level instead of one level for the whole clip.",
    "The model learns to predict a noisy future from a cleaner past → supports causal, frame-by-frame rollouts and keeping context frames slightly noisy at test time.",
    "Cost: still tens of denoising steps per frame."], fill=PALE_BLUE, size=12.5)
box(s, Inches(6.75), Inches(4.35), Inches(6.1), Inches(2.45), "Shortcut models (Frans et al., 2024)", [
    "Condition the network on the step size d as well as τ.",
    "Self-consistency ('bootstrap') loss: one step of size 2d must equal two consecutive steps of size d.",
    "Result: the model learns to take large, accurate steps → few-step or even one-step sampling."], fill=PALE_BLUE, size=12.5)
notes(s, "For the non-diffusion people: think of a noise level τ from 0 (pure noise) to 1 (clean latent). The model learns to push a noisy latent toward the clean one; sampling repeats this K times. "
         "Diffusion forcing makes the noise level per frame, which is what allows causal rollouts. Shortcut models teach the network to take big steps consistently. Dreamer 4 combines the two.")

# 14 Shortcut forcing ---------------------------------------------------------------
s = new_slide("Shortcut forcing: the training objective", "Diffusion forcing + shortcut models, with three engineering choices that turn out to matter a lot")
add_bullets(s, Inches(0.6), Inches(1.55), Inches(7.2), Inches(5.3), [
    "**Per-frame noise:** each frame gets an independent signal level τ_t; the model predicts frame t's clean latent from the noisy frame t, past frames, and actions",
    "**Step-size conditioning:** the network also receives d; for d > d_min the target is the *bootstrap* target — the result of two half-steps computed by the model itself (no gradient through the target)",
    "**Choice 1 — x-prediction:** the network outputs the clean latent, not the velocity",
    "**Choice 2 — loss in x-space:** the bootstrap target is formed in v-space (where two half-steps compose cleanly) but the loss is scaled back to x-space by (1 − τ)²",
    "**Choice 3 — ramp weight:** loss weight w(τ) = 0.9 τ + 0.1 emphasises high-signal (low-noise) levels, where fine detail is decided",
    "**Inference:** K = 4 steps per frame; context frames at τ_ctx ≈ 0.1; sampling remains stochastic → diverse imagined futures for RL"], size=14.5)
box(s, Inches(8.1), Inches(1.6), Inches(4.7), Inches(3.05), "Effect of each piece (Table 2, FVD ↓)", [
    "Diffusion forcing, K = 64 steps:  306  (0.8 FPS)",
    "Same model, K = 4 steps:  875",
    "+ shortcut objective:  329",
    "+ x-prediction:  326",
    "+ x-space loss:  151",
    "+ ramp weight:  102",
    "Full architecture but v-space prediction/loss:  124  vs  57"], fill=PALE_BLUE, size=12.5)
box(s, Inches(8.1), Inches(4.85), Inches(4.7), Inches(1.9), "Why this is the key contribution", ["4 steps ≈ the quality of 16–32 diffusion-forcing steps (Fig. 8) — roughly 16× fewer network evaluations per frame, which is what makes real-time interaction and large-scale imagination RL feasible."], fill=LIGHT, size=12.5)
notes(s, "Here is the objective in words. Combining the two prior ideas gets you from 875 back to 329 FVD at 4 steps — but the big wins come from the parameterisation details: predicting x instead of v, computing the loss in x-space, and the ramp weight together take FVD from 329 to 102. "
         "These are the kind of choices you only discover with a careful cascade of ablations, which the paper provides.")

# 15 Why x-prediction ---------------------------------------------------------------
s = new_slide("Why x-prediction matters for autoregressive world models", "Hafner's explanation (TalkRL, Nov 2025) and the numbers")
add_bullets(s, Inches(0.6), Inches(1.55), Inches(7.4), Inches(4.6), [
    "**v-prediction carries the noise:** to output v = x − ε the network must reproduce the *exact* noise pattern of its input through every layer; small mistakes in that noise become errors in the sample",
    "**In autoregressive use these errors compound:** each generated frame becomes context for the next; velocity errors accumulate as drift, blur or flicker over long rollouts",
    "**x-prediction is a denoising target:** the network only needs to know what the clean frame should look like — errors are 'pulled back' toward plausible images every step",
    "**Combined with noised context (τ_ctx ≈ 0.1):** the model is trained and run on slightly corrupted context, so it never sees a distribution it was not trained on",
    "**Evidence:** full architecture with v-space prediction/loss reaches FVD 124; with x-prediction and x-space loss, 57 (Table 2). Long 384-frame generations were used for FVD precisely to expose compounding error"], size=14.5)
fit_picture(s, A + "fig8_shortcut_vs_df.png", Inches(8.3), Inches(1.6), Inches(4.5), Inches(3.9))
caption(s, Inches(8.3), Inches(5.55), Inches(4.5), "Figure 8: FVD vs sampling steps. Shortcut forcing at 4 steps ≈ 60; diffusion forcing needs 16–32 steps to match.")
notes(s, "This is the most transferable lesson of the paper for anyone building autoregressive generative models: predict the clean signal, not the velocity, when your own outputs become your inputs. "
         "Open Dreamer, the open-source reproduction, independently confirmed this — they report the same instability with v-prediction at scale.")

# 16 Efficient transformer ---------------------------------------------------------------
s = new_slide("Architecture choices that buy speed without losing quality", "Table 2: each row adds one change to the previous row")
fit_picture(s, A + "chart_ablation_cascade.png", Inches(0.4), Inches(1.5), Inches(8.3), Inches(4.4))
add_bullets(s, Inches(8.9), Inches(1.55), Inches(4.1), Inches(5.4), [
    "**Alternating batch lengths** (64 / 256 frames): FVD 102 → 80 and a training step from 9.8 s → 1.5 s",
    "**Time attention only every 4th layer:** 18.9 FPS at FVD 70",
    "**Grouped-query attention:** 23.2 FPS, FVD unchanged",
    "**Time-factorised long context** trades a little quality (91) for 30 FPS; **registers** stabilise attention",
    "**More latent tokens** (128 → 256) brings FVD to 57 at 21.4 FPS — the final configuration",
    "Runs were 48 h each; FVD computed on 1,024 generations of 384 frames"], size=14)
notes(s, "Read the bars top to bottom. The red bars are the starting point: a diffusion-forcing transformer that is either slow or bad. The grey bars are the objective changes from the previous slides; the blue bar is the final model. "
         "The architectural changes on the lower half mostly move FPS, not FVD — exactly what you want.")

# 17 Agent tokens ---------------------------------------------------------------
s = new_slide("From world model to agent: agent tokens & heads", "Phase 2 — policy and reward live inside the same transformer, but cannot disturb the simulation")
add_bullets(s, Inches(0.6), Inches(1.55), Inches(7.6), Inches(5.3), [
    "**Agent tokens:** extra tokens per frame that carry a task embedding (one-hot over the 20 training tasks) and read out policy and reward",
    "**One-way attention:** agent tokens attend to actions, latents and past frames — but *nothing attends back to them*, so the world model never conditions on the policy's intentions or reward estimates",
    "**Policy head — behavioural cloning with multi-token prediction:** predict the next L = 8 actions; the extra horizon regularises the representation and encodes intent",
    "**Reward head:** predicts task rewards derived from game events (item obtained); a task-conditioned *scalar* reward was chosen over a reward vector so that open-vocabulary tasks remain possible",
    "**Value head:** added in Phase 3, trained by TD learning on imagined rollouts",
    "**Result already at this stage:** 'WM + BC' beats BC on every hard milestone (iron pickaxe 16.9 % vs 0.6 %) — the video-prediction representation is a strong prior for control"], size=14.5)
fit_picture(s, A + "fig_rl.png", Inches(8.4), Inches(1.7), Inches(4.4), Inches(2.3))
caption(s, Inches(8.4), Inches(4.05), Inches(4.4), "Figure 3: success rates of agents trained on the same offline data (BC, VLA, WM+BC, Dreamer 4).")
box(s, Inches(8.4), Inches(4.7), Inches(4.4), Inches(2.0), "Why not a separate policy network?", ["Sharing the backbone gives the policy the world model's representation for free, and keeps everything one model. The one-way attention mask is what makes this safe."], fill=PALE_BLUE, size=12.5)
notes(s, "Agent tokens are the interface between simulation and decision making. The one-directional mask is subtle but important: if latents could attend to agent tokens, the model could 'cheat' by predicting frames consistent with what the policy intends rather than with the physics of the game. "
         "Notice how much of the gain over BC comes from this phase alone — the representation matters.")

# 18 Imagination training / PMPO ---------------------------------------------------------------
s = new_slide("Imagination training with PMPO", "Phase 3 — RL on imagined rollouts, with the transformer frozen")
add_bullets(s, Inches(0.6), Inches(1.55), Inches(7.4), Inches(5.3), [
    "**Rollouts:** start from real context frames, let the policy act, and let the world model generate what happens next; rewards come from the learned reward head; γ = 0.997",
    "**Frozen transformer:** only policy and value heads are trained → the simulator cannot drift toward the policy",
    "**PMPO (Preference-style MPO):** instead of scaling the policy gradient by the advantage, use only its *sign* — positive-advantage actions are pushed up, negative ones down, with balanced weight α = 0.5 on each set",
    "**Reverse-KL to the frozen BC policy** with β = 0.3 keeps the policy on the data manifold — analogous to KL-regularised RLHF; also the main guard against exploiting world-model gaps",
    "**Why not Dreamer 3's recipe?** Return normalisation + entropy bonus were replaced by the sign-based update: robust to reward scale and to the extremely sparse late-game rewards",
    "**Effect:** iron pickaxe 16.9 % → 29.0 %, iron ingot 27.8 % → 39.5 %, diamond 0 → 0.7 %; agents also become faster (Table 8)"], size=14.5)
fit_picture(s, A + "frame_imag_cobble.jpg", Inches(8.3), Inches(1.7), Inches(4.5), Inches(2.9))
caption(s, Inches(8.3), Inches(4.62), Inches(4.5), "Imagined 'mine stone' rollout with reward and value traces (project page).")
box(s, Inches(8.3), Inches(5.15), Inches(4.5), Inches(1.6), "Failure mode the KL term addresses", ["Hafner's example: the policy discovers it can 'craft' a pickaxe from invalid materials because the model renders it anyway. The KL to the BC prior limits such exploitation."], fill=LIGHT, size=12)
notes(s, "PMPO is deliberately simple. Using only the sign of the advantage makes the update invariant to reward scale, which matters when rewards are rare item events. The KL term to the BC policy is doing two jobs: stabilising RL and preventing the policy from wandering into regions the world model gets wrong. "
         "Hafner mentioned in a talk that a few rounds of corrective online data would allow a much weaker KL — but that is not in the paper.")

# ---- Part 3 -------------------------------------------------------------
section("Experiments", "Real-time play-testing, the offline diamond challenge, ablations, label efficiency, robotics", 3)

# 20 Table 1 ---------------------------------------------------------------
s = new_slide("Is the world model accurate? Let humans play inside it", "Table 1: real-time interaction on one H100; 16 tasks attempted by human testers from the same starting frame")
rows = [["Model", "Params", "Resolution", "Context", "FPS", "Tasks solved"],
        ["MineWorld", "1.2 B", "384×224", "0.8 s", "2", "not evaluable (needs actions in advance)"],
        ["Lucid-v1", "1.1 B", "640×360", "1.0 s", "44", "0 / 16"],
        ["Oasis (small)", "500 M", "640×360", "1.6 s", "20", "0 / 16"],
        ["Oasis (large)", "—", "360×360", "1.6 s", "~5", "5 / 16"],
        ["Dreamer 4", "2 B", "640×360", "9.6 s", "21", "14 / 16"]]
add_table(s, Inches(0.5), Inches(1.6), Inches(8.0), rows, col_widths=[1.6, 0.9, 1.35, 1.0, 0.75, 2.4], font=13, highlight_row=5, row_h=0.42)
add_bullets(s, Inches(0.6), Inches(4.4), Inches(7.9), Inches(2.5), [
    "**The 16 tasks:** eat apple · place 3 torches · chop tree · dig 3×3 pit · craft wooden pickaxe · use furnace · place & open workbench · kill zombies · mine diamonds · complete window · place & ride boat · enter portal · place door · bed & sleep · plant reed & pour water · turn 360° & enter house",
    "**The two failures** were memory-related: the world changes when you look away for longer than the 9.6 s context, and inventory contents become unclear over time",
    "Genie 3 is not compared: it has no fine-grained mouse/keyboard control"], size=13.5)
fit_picture(s, A + "fig5_human_interaction_pdf.png", Inches(8.7), Inches(1.6), Inches(4.2), Inches(2.3))
caption(s, Inches(8.7), Inches(3.9), Inches(4.2), "Figure 5: same task, same start frame — Dreamer 4 (top) builds the wall; Lucid-v1 and Oasis do not.")
box(s, Inches(8.7), Inches(4.6), Inches(4.2), Inches(2.1), "Why this evaluation", ["FVD and PSNR measure how video *looks*; only interaction tests whether the model got the *mechanics* right. The paper complements it with FVD on 384-frame rollouts, but no long-horizon *quantitative* interaction metric exists yet — a fair critique."], fill=PALE_BLUE, size=12)
notes(s, "This is the paper's most convincing evidence about the world model. Real people sit down with a mouse and keyboard and try to do things. Dreamer 4 is the only model in which crafting, riding a boat or entering a portal work. "
         "The caveat is on the right: this is a small, human-judged protocol; I'd like to see automated long-horizon metrics in follow-ups.")

# 21 Human interaction frames ---------------------------------------------------------------
s = new_slide("What 'accurate object interactions' looks like", "Frames from the project page's side-by-side human sessions (same start frame, same human inputs)")
labels = ["Dreamer 4", "Lucid-v1", "Oasis"]; tasks = [("boat", "Place and ride boat"), ("portal", "Enter portal"), ("pickaxe", "Craft wooden pickaxe")]
x0 = Inches(1.7); y0 = Inches(1.75); cw = Inches(3.7); ch = Inches(1.45)
for j, lab in enumerate(labels): add_text(s, x0 + j * (cw + Inches(0.1)), Inches(1.4), cw, Inches(0.35), lab, size=14, bold=True, color=BLUE if j == 0 else GREY, align=PP_ALIGN.CENTER)
for i, (key, name) in enumerate(tasks):
    add_text(s, Inches(0.3), y0 + i * (ch + Inches(0.1)) + Inches(0.5), Inches(1.35), Inches(0.8), name, size=12, bold=True, color=DARK)
    for j, m in enumerate(["dreamer", "lucid", "oasis"]):
        fit_picture(s, A + f"frame_{key}_{m}.jpg", x0 + j * (cw + Inches(0.1)), y0 + i * (ch + Inches(0.1)), cw, ch)
caption(s, Inches(0.5), Inches(6.55), Inches(12.3), "Single frames sampled from the project-page clips (danijar.com/asset/dreamer4/human/…). Dreamer 4 renders the boat ride, the Nether-portal swirl and a working crafting-table menu; the baselines lose the scene or the menu.")
notes(s, "Three of the sixteen tasks. In the boat task Lucid shows only blue; in the portal task the baselines never enter; in the crafting task Dreamer 4 opens a functional crafting menu. "
         "The clips themselves are in the resource archive if you want to play them during the talk.")

# 22 Diamond results ---------------------------------------------------------------
s = new_slide("Offline diamond challenge: results", "Success rate per milestone; 1,000 episodes × 60 min; same 2,541 h of data for all methods (Table 7 / Fig. 3)")
fit_picture(s, A + "benchmark.png", Inches(0.4), Inches(1.5), Inches(12.5), Inches(3.6))
add_bullets(s, Inches(0.6), Inches(5.2), Inches(12.2), Inches(1.9), [
    "**Dreamer 4:** stone pickaxe 90.1 % · iron ore 66.7 % · furnace 58.1 % · iron ingot 39.5 % · iron pickaxe 29.0 % · **diamond 0.7 %** (≈ 7 of 1,000 episodes)",
    "**VLA on Gemma 3 (same data):** iron pickaxe 11.2 %, no diamonds · **BC:** 0.6 % · **VPT fine-tuned** (pretrained on 270 K h of web video): only reliably reaches sticks",
    "Gap widens along the tech tree: imitation is enough for early items, imagination RL matters where data is thin and horizons are long"], size=14)
caption(s, Inches(0.5), Inches(4.95), Inches(12), "Official figure from danijar.com/project/dreamer4 (benchmark.png).", size=9.5)
notes(s, "The official results figure. Every method nails the first items; the interesting region is the right half. Dreamer 4 roughly doubles or triples the VLA on iron-age items and is the only one reaching diamonds — rarely, but from zero interaction. "
         "Remember this is a 60-minute budget per episode; humans need about 20 minutes on average.")

# 23 Agent ablations + time ---------------------------------------------------------------
s = new_slide("Where do the gains come from? Agent ablations and speed", "Figure 4 / Table 8: representation (WM+BC vs BC) and imagination RL (Dreamer 4 vs WM+BC) both contribute")
fit_picture(s, A + "chart_table7_hard.png", Inches(0.4), Inches(1.5), Inches(7.4), Inches(3.4))
fit_picture(s, A + "chart_time_to_milestone.png", Inches(8.0), Inches(1.5), Inches(4.9), Inches(3.4))
add_bullets(s, Inches(0.6), Inches(5.05), Inches(12.2), Inches(2.0), [
    "**Representation:** BC on the world model's features (WM+BC) vs plain BC — iron pickaxe 16.9 % vs 0.6 %; authors: 'video prediction implicitly learns an understanding of the world that is useful for decision making'",
    "**Imagination RL:** adds +12 pts on iron pickaxe and +12 pts on iron ingot over WM+BC, and unlocks diamonds",
    "**Speed:** Dreamer 4 is fastest at every milestone — iron pickaxe in 13.3 min vs 31.1 min for the VLA; diamonds in 20.7 min on average when achieved (human average ≈ 20 min)",
    "**Task input matters:** BC without the task embedding collapses to 8.8 % stone pickaxe (Table 7)"], size=13.5)
notes(s, "Two separable effects. First, using the world model as the representation for imitation already gives a large jump — that's a statement about video pretraining. Second, RL inside the model adds a further, smaller but consistent gain on the hardest items and makes the agent faster, which is a hallmark of RL over imitation.")

# 24 Label efficiency ---------------------------------------------------------------
s = new_slide("Unlabeled video: how many action labels are needed?", "Figure 7 — action conditioning from a small labeled fraction, and transfer to unseen visual domains")
fit_picture(s, A + "fig7_action_generalization.png", Inches(0.4), Inches(1.5), Inches(8.2), Inches(2.9))
add_bullets(s, Inches(0.6), Inches(4.55), Inches(12.2), Inches(2.4), [
    "**Setup:** train on all 2,541 h of video, but keep actions for only a subset; measure PSNR/SSIM of action-conditioned predictions, normalised between 'no actions' (0 %) and 'all actions' (100 %)",
    "**10 h of labels → 53 % PSNR / 75 % SSIM; 100 h → 85 % / 100 %; 1,000 h → 100 %** — action understanding saturates with roughly 4 % of the data labeled",
    "**Domain transfer:** with actions only from the Overworld, predictions in the Nether/End (seen unlabeled) recover 76 % / 80 % — the model separates 'what actions do' from 'what the world looks like'",
    "**Why it matters:** the road to internet-scale video pretraining, where labels are scarce (VPT needed an inverse-dynamics model for this)"], size=14)
box(s, Inches(8.9), Inches(1.6), Inches(4.0), Inches(2.7), "Mechanism", ["Unlabeled frames receive a learned 'no action' embedding; the dynamics loss is the same. The model therefore learns visual dynamics from everything and the action mapping from the labeled slice."], fill=PALE_BLUE, size=12.5)
notes(s, "This experiment is easy to overlook but strategically important. Only about a hundred hours of labeled actions are needed on top of thousands of unlabeled hours, and the learned action semantics transfer to visual domains that were never labeled. "
         "That is the argument for scaling to internet video later.")

# 25 Imagination rollouts (Fig 1) ---------------------------------------------------------------
s = new_slide("Inside the imagination: decoded training rollouts", "Figure 1 — imagined sequences for four agent tasks, decoded only for visualisation")
fit_picture(s, jpeg(A + "fig1_teaser_pdf.png"), Inches(0.5), Inches(1.5), Inches(8.6), Inches(5.2))
add_bullets(s, Inches(9.3), Inches(1.6), Inches(3.7), Inches(5.3), [
    "The world model simulates chopping, crafting menus, mining, cave lighting and diamond ore — all generated, not recorded",
    "RL never sees pixels: it operates on latents; decoding is for us",
    "Each rollout starts from real context frames and follows the *current* policy → training data stays on-policy without touching the game",
    "Stochastic sampling gives diverse futures — useful for exploring rare outcomes such as finding ore"], size=14)
notes(s, "Figure 1 from the paper. All of these frames are generated by the model while the policy is being trained. Worth stressing to a mixed audience: the agent learns in latent space; decoding is purely for visualisation.")

# 26 Beyond Minecraft ---------------------------------------------------------------
s = new_slide("Beyond Minecraft: robotics & egocentric video (qualitative)", "Figure 6 and Figure 9 — same recipe, different data; no quantitative benchmark yet")
fit_picture(s, jpeg(A + "fig6_robotics.png"), Inches(0.4), Inches(1.5), Inches(8.4), Inches(3.2))
caption(s, Inches(0.4), Inches(4.7), Inches(8.4), "Figure 6: SOAR robot-arm data — counterfactual actions (pick objects, flip bowl, press ball, move towel, throw bowl) rendered by the world model.")
fit_picture(s, A + "frame_realworld_soar1.jpg", Inches(9.0), Inches(1.5), Inches(3.9), Inches(2.3))
caption(s, Inches(9.0), Inches(3.82), Inches(3.9), "Project page: human counterfactual interaction with the robot world model.")
add_bullets(s, Inches(0.6), Inches(5.2), Inches(12.2), Inches(1.9), [
    "**SOAR:** 180 h of teleoperation + online-RL data, 256×256 at 5 FPS, 7-D relative end-effector actions; N_z = 512, context 96 frames",
    "**Epic Kitchens 100:** 100 h of egocentric kitchen video, no actions — generations from held-out context (Fig. 9) show the recipe works on real, unstructured video",
    "**Caveat:** no policy was trained and no metrics are reported for these domains — they demonstrate generality of the world model, not of the agent"], size=14)
notes(s, "The paper positions Dreamer 4 as a step toward robotics. The evidence here is qualitative: plausible counterfactual generations on real robot and kitchen video. Hafner left DeepMind shortly after the paper to work on humanoid robotics, which tells you where the authors think this goes.")

# 27 Dreamer 3 vs 4 ---------------------------------------------------------------
s = new_slide("Dreamer 3 vs Dreamer 4", "Appendix F: what changed, and what the higher-fidelity model costs")
rows = [["", "Dreamer 3 (Nature 2025)", "Dreamer 4"],
        ["World model", "RSSM (recurrent + variational latent)", "Block-causal diffusion/flow transformer, shortcut forcing"],
        ["Minecraft input", "64×64 pixels + inventory state; abstract crafting actions", "360×640 pixels only; raw mouse & keyboard"],
        ["Data", "1.4 K h of *online* interaction, no human data", "2.5 K h of *offline* human data, no interaction"],
        ["RL", "Return normalisation + entropy bonus", "PMPO (advantage sign) + KL to BC prior"],
        ["Speed", "~1,000× faster than a diffusion transformer", "~30× faster than diffusion forcing; ~40× slower than the RSSM"]]
add_table(s, Inches(0.5), Inches(1.55), Inches(7.6), rows, col_widths=[1.5, 3.0, 3.1], font=12, highlight_col=2, row_h=0.6)
fit_picture(s, jpeg(A + "fig11_dreamer3_vs_4.png"), Inches(8.4), Inches(1.55), Inches(4.5), Inches(1.9))
caption(s, Inches(8.4), Inches(3.5), Inches(4.5), "Figure 11: multi-step generations, Dreamer 4 (top) vs Dreamer 3 (bottom).")
fit_picture(s, A + "chart_speed_fidelity.png", Inches(8.3), Inches(3.9), Inches(4.7), Inches(3.1))
notes(s, "Same family, different regime. Dreamer 3 solved diamonds with online interaction and privileged state at 64×64; Dreamer 4 does it offline from raw pixels and inputs. The price is speed: the transformer is still about forty times slower than the recurrent model, according to Hafner.")

# 28 Compute & data ---------------------------------------------------------------
s = new_slide("Data, compute and scale", "Appendix A and Table 3")
rows = [["Dataset", "Size", "Resolution / FPS", "Actions", "Dynamics config"],
        ["Minecraft (VPT contractor 6–10)", "2,541 h", "360×640 → 384×640 padded, 20 FPS", "23 keys + 121-way mouse; item events → rewards", "N_z 256 · C 192 · T 64/256"],
        ["Overworld vs Nether/End split", "subset", "same", "labels only for Overworld", "action-generalisation study"],
        ["SOAR robotics", "180 h", "256×256, 5 FPS", "7-D relative end-effector", "N_z 512 · C 96 · T 32/128"],
        ["Epic Kitchens 100", "100 h", "256×256, 10 FPS", "none", "same as SOAR"]]
add_table(s, Inches(0.5), Inches(1.55), Inches(12.3), rows, col_widths=[2.6, 1.0, 2.9, 3.2, 2.6], font=12, row_h=0.5)
rows2 = [["Agent (Table 3)", "Human data", "Web video", "Online interaction"],
         ["VPT (RL fine-tuned)", "2.5 K h", "270 K h", "194 K h"],
         ["VPT (BC)", "2.5 K h", "270 K h", "—"],
         ["Dreamer 3", "—", "—", "1.4 K h"],
         ["Dreamer 4", "2.5 K h", "—", "—"]]
add_table(s, Inches(0.5), Inches(4.35), Inches(6.6), rows2, col_widths=[2.2, 1.4, 1.4, 1.6], font=12, highlight_row=4, row_h=0.4)
add_bullets(s, Inches(7.4), Inches(4.4), Inches(5.5), Inches(2.6), [
    "**Compute:** 256–1,024 TPU v5p chips per run (exact chip-hours not disclosed)",
    "**Ablations:** 48 h runs per configuration",
    "**Model:** ≈ 2 B parameters total; inference 21 FPS on one H100",
    "**Not released:** code, weights or data recipe (Hafner: 'probably not') — reproductions exist (Open Dreamer, Dreamer-MC, Hansen's PyTorch port)"], size=13.5)
notes(s, "Scale context. The Minecraft data is the public VPT contractor set, which makes the comparison with VPT clean: Dreamer 4 uses about a hundred times less data and no interaction. Compute is disclosed only as a TPU range. Nothing was open-sourced, which shaped the follow-up ecosystem.")

# ---- Part 4 -------------------------------------------------------------
section("Discussion", "Limitations, critical reading, future work, takeaways", 4)

# 30 Limitations ---------------------------------------------------------------
s = new_slide("Limitations the paper itself states", "From the discussion section and the authors' talks")
add_bullets(s, Inches(0.6), Inches(1.55), Inches(12.2), Inches(5.4), [
    "**Diamonds are rare:** 0.7 % success; the authors call the pipeline a 'reliable and performant starting point', not a solved task",
    "**Memory:** 9.6 s of context; walk into a house for 30 s and the outside is regenerated — long-term memory is the number-one item on the roadmap",
    "**Inventory drift:** small UI elements and item counts blur over long horizons; small objects and long-range semantic correlations are what video models learn last",
    "**Frozen, exploitable simulator:** no epistemic-uncertainty estimate; the policy can exploit model errors (invalid crafting) — currently mitigated only by the KL constraint",
    "**Two-stage training:** tokenizer is trained separately and frozen; the authors expect end-to-end training eventually",
    "**Single domain for the agent:** RL results exist only for Minecraft; robotics and kitchen video are qualitative world-model demos",
    "**Compute:** hundreds of TPU v5p chips per run; not a recipe individuals can reproduce at full scale"], size=15.5)
notes(s, "The authors are quite candid. The two that matter most for the agenda of the paper are memory and exploitability: both limit how far imagination training can be pushed before the policy learns things that are only true inside the model.")

# 31 Critical reading ---------------------------------------------------------------
s = new_slide("A critical reading: established vs. open", "What a reviewer would push on (and what independent groups later found)")
box(s, Inches(0.5), Inches(1.6), Inches(6.1), Inches(5.2), "Well supported", [
    "• Shortcut forcing + x-prediction gives a large speed/quality win — a clean 12-step ablation cascade, and reproduced by Open Dreamer at 1.6 B scale (JAX, 2026).",
    "• The world model handles object interactions far better than Oasis / Lucid-v1 — consistent human play-tests plus long-rollout FVD.",
    "• World-model features are a strong prior for imitation (WM+BC ≫ BC on the same data).",
    "• Action conditioning from ~4 % labeled data works and transfers across visual domains."], fill=RGBColor(0xE6, 0xF7, 0xF3), size=13)
box(s, Inches(6.75), Inches(1.6), Inches(6.1), Inches(5.2), "Open or thinly supported", [
    "• Diamond result: 0.7 % without confidence intervals or per-seed variance; success criterion is a game event, protocol details are in the appendix only.",
    "• No direct quantitative long-horizon accuracy metric — interaction accuracy is human-judged on 16 tasks (Pith/EmergentMind critique).",
    "• RL gains over WM+BC are modest on most items; small-scale reproductions report high seed variance in the RL phase and reward-hacking of the frozen reward head.",
    "• No peer review as of Sept 2026 (arXiv v1 only); no code or weights; nobody outside DeepMind has reproduced offline diamonds.",
    "• Generality of the *agent* beyond Minecraft is untested."], fill=RGBColor(0xFD, 0xF1, 0xE7), size=13)
notes(s, "Balance sheet. The methodological contribution — how to make a fast, accurate autoregressive video world model — is robust and has been independently reproduced. The headline agent result is real but statistically thin and has not been reproduced outside DeepMind. "
         "For a reading group, this split is where the discussion usually starts.")

# 32 Future directions ---------------------------------------------------------------
s = new_slide("Where the authors want to take it", "Future work listed in the paper and expanded in the TalkRL interview (Nov 2025)")
items = [("Internet-video pretraining", "Learn dynamics from unlabeled web video; label only a small slice with actions (Fig. 7 is the proof of concept)."),
         ("Long-term memory", "Beyond 9.6 s: retrieval or compressed memory so the world stays consistent when you look away."),
         ("Language conditioning", "Replace one-hot task IDs with text embeddings; scalar task-conditioned reward already anticipates open-vocabulary tasks."),
         ("A little online data", "Small rounds of *corrective* interaction to fix the errors the policy exploits — then the KL constraint can be relaxed."),
         ("Automatic goal discovery", "Empowerment / exploration objectives (APD, Plan2Explore, Director) so agents propose their own tasks inside the model."),
         ("End-to-end training", "Fold the tokenizer into the dynamics model; scale parameters and context together.")]
x, y = Inches(0.5), Inches(1.6)
for i, (t, d) in enumerate(items):
    box(s, x + (i % 3) * Inches(4.17), y + (i // 3) * Inches(2.6), Inches(4.0), Inches(2.4), t, [d], fill=LIGHT if i % 2 else PALE_BLUE, size=13)
notes(s, "Six directions, three of which — memory, corrective data, and language — directly address the limitations we just discussed. Note that the authors' next steps are toward physical robots, not more Minecraft.")

# 33 Takeaways ---------------------------------------------------------------
s = new_slide("Key takeaways")
add_bullets(s, Inches(0.7), Inches(1.6), Inches(12), Inches(5.3), [
    "**1. Imagination training now works from raw pixels and raw inputs, offline.** Dreamer 4 reaches diamonds in Minecraft with zero environment interaction and ~100× less data than VPT.",
    "**2. The enabling contribution is speed at quality:** shortcut forcing (4 sampling steps), x-prediction with x-space loss, and an architecture that attends across time only every 4th layer — 21 FPS on one GPU with a 9.6 s context.",
    "**3. Accuracy of interactions, not visual polish, is the bar** — validated by humans playing inside the model (14/16 tasks vs 5/16 for the best prior model).",
    "**4. Video pretraining is a strong prior for control:** most of the gain over BC comes from the world-model representation; RL adds the rest on the hardest, longest-horizon items.",
    "**5. Labels are cheap:** ~100 h of actions on top of thousands of unlabeled hours suffice, and action semantics transfer to unseen visual domains.",
    "**6. Open problems remain:** short memory, exploitable frozen simulators, thin statistics on the headline result, no official release."], size=16, space=10)
notes(s, "Six takeaways, ordered from result to method to caveats.")

# 34 Discussion questions ---------------------------------------------------------------
s = new_slide("Questions for discussion")
add_bullets(s, Inches(0.7), Inches(1.6), Inches(12), Inches(5.3), [
    "How much of the diamond result is the world model versus PMPO? Would a stronger offline-RL baseline on world-model features (no imagination) close the gap?",
    "Is human play-testing on 16 tasks a sufficient measure of 'accurate simulation'? What automated long-horizon metric would you propose?",
    "The transformer is frozen during RL and the reward head is learned: where would you expect exploitation to appear first, and how would you detect it offline?",
    "9.6 s of context: which memory mechanism (retrieval, state-space layers, compressed summaries) fits a block-causal diffusion transformer best?",
    "The recipe needs ~100 h of action labels per domain. What does the path to internet-scale video look like — inverse dynamics models, or Dreamer 4's 'no-action' embedding at scale?",
    "What would convince you that this transfers to real robots — and what evaluation would you run first?"], size=16, space=12)
notes(s, "Pick two or three depending on the room.")

# 35 References ---------------------------------------------------------------
s = new_slide("References & resources")
add_bullets(s, Inches(0.6), Inches(1.5), Inches(12.3), Inches(5.6), [
    "**Paper:** Hafner*, Yan*, Lillicrap. Training Agents Inside of Scalable World Models. arXiv:2509.24527 (29 Sep 2025). https://arxiv.org/abs/2509.24527",
    "**Project page & videos:** https://danijar.com/project/dreamer4/ — overview video (youtube.com/watch?v=oDlBtTcX0g0), four uncut 60-min 'Diamond Challenge' evaluation episodes, 51 human-interaction clips",
    "**Authors in conversation:** TalkRL E73 'Danijar Hafner on Dreamer v4' (10 Nov 2025), transcript available; Hack Club AMA (Dec 2025)",
    "**Ingredients:** Chen et al., Diffusion Forcing (2407.01392) · Frans, Hafner, Levine, Abbeel, Shortcut Models (2410.12557) · Chen et al., MAETok (2502.03444) · Baker et al., VPT (2206.11795) · Hafner et al., DreamerV3 (2301.04104)",
    "**Independent reproductions / follow-ups:** next-state/open-dreamer (JAX, 1.6 B Minecraft world model, Jul 2026) · IamCreateAI/Dreamerv4-MC (weights on HF) · nicklashansen/dreamer4 & MMBench2 (Hansen & Wang, 2606.27326) · lucidrains/dreamer4 (PyTorch)",
    "**Everything above, archived:** https://github.com/HarmannBitte/Dreamer-4 — PDFs, repo snapshots, articles, transcripts, the official clips used in this deck, and a MEDIA_INDEX.md"], size=14, space=9)
notes(s, "All sources, plus the GitHub archive that contains local copies of every item used to build this deck.")

# ---- Appendix -------------------------------------------------------------
s = new_slide("Appendix A — Configuration & hyper-parameters")
rows = [["Component", "Setting"],
        ["Tokenizer", "Masked autoencoder; 16×16 patches; patch dropout ~ U(0, 0.9); loss MSE + 0.2·LPIPS; bottleneck 512×16 with tanh → N_z = 256 tokens × 32 dims; causal in time; ≈ 400 M params; frozen after pretraining"],
        ["Dynamics model", "≈ 1.6 B params; pre-RMSNorm, RoPE, SwiGLU, QK-norm, logit soft-capping, register tokens; space attention in 3/4 layers, causal time attention every 4th layer; GQA; context C = 192 frames (9.6 s); alternating batch lengths T1/T2 = 64/256"],
        ["Shortcut forcing", "per-frame signal level τ, step size d; x-prediction; bootstrap target formed in v-space, loss scaled to x-space by (1−τ)²; ramp weight w(τ) = 0.9τ + 0.1; K = 4 sampling steps; context noise τ_ctx ≈ 0.1"],
        ["Actions", "23 binary keys + 121-way mouse (μ-law, 11×11 foveated bins, VPT convention); learned 'no action' embedding for unlabeled video"],
        ["Agent (phase 2)", "agent tokens with one-hot task (20 tasks), one-way attention; BC with multi-token prediction L = 8; task-conditioned scalar reward head; data mix 50 % uniform / 50 % task-relevant"],
        ["Imagination RL (phase 3)", "transformer frozen; policy + TD value heads; PMPO with advantage sign, α = 0.5, reverse-KL β = 0.3 to frozen BC policy; γ = 0.997"],
        ["Evaluation", "1,000 episodes × 60 min, empty inventory, random worlds, fixed prompt sequence; human interaction: 16 tasks on one H100 at 21 FPS"],
        ["Compute / data", "256–1,024 TPU v5p; 2,541 h VPT contractor video (subsets 6–10), 90/10 split by 5-min chunk; ablations: 48 h runs, FVD on 1,024 × 384-frame generations"]]
add_table(s, Inches(0.5), Inches(1.45), Inches(12.3), rows, col_widths=[2.1, 10.2], font=11, row_h=0.6)
notes(s, "Reference slide; not meant to be presented in full.")

s = new_slide("Appendix B — Full design cascade (Table 2)")
rows = [["Change (cumulative)", "FPS", "FVD ↓"], ["Diffusion-forcing transformer, K = 64", "0.8", "306"], ["K = 4 sampling steps", "9.1", "875"], ["+ shortcut objective (→ shortcut forcing)", "", "329"], ["+ x-prediction", "", "326"], ["+ x-space loss", "", "151"], ["+ ramp weight", "", "102"], ["+ alternating batch lengths (step 9.8 s → 1.5 s)", "", "80"], ["+ long context only every 4th layer", "18.9", "70"], ["+ grouped-query attention", "23.2", "71"], ["+ time-factorised long context", "30.1", "91"], ["+ register tokens", "", "91"], ["N_z 128 → 256 (final)", "21.4", "57"], ["(reference) full architecture, v-space prediction & loss", "", "124"]]
add_table(s, Inches(0.5), Inches(1.45), Inches(7.5), rows, col_widths=[5.3, 1.0, 1.2], font=11.5, highlight_row=12, row_h=0.36)
add_bullets(s, Inches(8.3), Inches(1.6), Inches(4.6), Inches(4.5), ["48-hour training runs per row", "FVD on 1,024 generations of 384 frames (long rollouts to expose compounding error)", "FPS measured for generation on one H100 where reported", "Fig. 8 adds the steps sweep: shortcut forcing FVD ≈ 160/85/60/50 at 1/2/4/8 steps vs ≈ 1,020/830/530/220 for diffusion forcing"], size=13.5)
notes(s, "Numbers transcribed from Table 2 and read off Figure 8.")

s = new_slide("Appendix C — Full success-rate table (Table 7, %)")
rows = [["Milestone", "VPT (ft)", "BC (no task)", "BC", "VLA (Gemma 3)", "WM + BC", "Dreamer 4"],
        ["Log", "84.3", "71.4", "97.3", "98.5", "99.6", "99.1"], ["Planks", "65.3", "68.6", "95.7", "98.3", "99.6", "98.9"], ["Crafting table", "4.7", "63.8", "93.5", "97.2", "99.1", "98.5"], ["Stick", "52.6", "62.4", "95.0", "97.7", "98.9", "98.7"],
        ["Wooden pickaxe", "0.0", "33.8", "86.5", "94.1", "97.3", "96.6"], ["Cobblestone", "6.9", "32.0", "83.9", "91.6", "97.2", "95.9"], ["Stone pickaxe", "0.0", "8.8", "53.8", "76.7", "89.4", "90.1"], ["Iron ore", "0.1", "3.6", "26.5", "46.3", "62.9", "66.7"],
        ["Furnace", "0.0", "4.0", "16.2", "42.4", "51.1", "58.1"], ["Iron ingot", "0.1", "0.2", "4.3", "22.5", "27.8", "39.5"], ["Iron pickaxe", "0.0", "0.0", "0.6", "11.2", "16.9", "29.0"], ["Diamond", "0.0", "0.0", "0.0", "0.0", "0.0", "0.7"]]
add_table(s, Inches(0.5), Inches(1.45), Inches(12.3), rows, col_widths=[2.3, 1.5, 1.7, 1.4, 2.0, 1.6, 1.8], font=12, highlight_col=6, row_h=0.38)
caption(s, Inches(0.5), Inches(6.5), Inches(12), "1,000 evaluation episodes of 60 minutes each; all agents trained on the same 2,541 h of contractor data (VPT additionally pretrained on 270 K h of web video).")
notes(s, "Full table for reference.")

s = new_slide("Appendix D — Glossary")
rows = [["Term", "Meaning in this paper"],
        ["World model", "Learned model that predicts future observations (here: latent frames) given past observations and actions"],
        ["Imagination training", "Training the policy on rollouts generated by the world model instead of the real environment"],
        ["Tokenizer / latents", "Encoder–decoder mapping each frame to 256 continuous tokens the dynamics model operates on"],
        ["Block-causal attention", "Full attention within a frame, causal across frames — enables frame-by-frame online generation"],
        ["Diffusion forcing", "Diffusion training with an independent noise level per frame in a sequence"],
        ["Shortcut model", "Diffusion/flow model conditioned on step size, trained to be self-consistent across step sizes → few-step sampling"],
        ["x- vs v-prediction", "Network predicts the clean latent (x) vs the velocity x − ε (v); Dreamer 4 uses x-prediction"],
        ["FVD / PSNR / SSIM", "Fréchet Video Distance (distribution-level video quality, lower is better) / per-frame reconstruction fidelity metrics"],
        ["GQA, RoPE, registers", "Grouped-query attention (fewer KV heads), rotary position embeddings, extra learnable tokens that absorb attention mass"],
        ["BC, VLA, PMPO", "Behavioural cloning; vision-language-action model (here built on Gemma 3); the sign-based, KL-regularised policy-gradient update used for RL"]]
add_table(s, Inches(0.5), Inches(1.45), Inches(12.3), rows, col_widths=[2.4, 9.9], font=11.5, row_h=0.45)
notes(s, "Glossary for the mixed audience.")

out = "Dreamer4_Deep_Dive.pptx"; prs.save(out)
print("saved", out, os.path.getsize(out) // 1024, "KB,", len(prs.slides), "slides")
