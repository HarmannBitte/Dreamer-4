"""Recreate assets/ used by build_deck.py (figures from the paper, frames from the archived official clips, charts).
Requires: pip install pymupdf imageio-ffmpeg matplotlib pillow requests ; run from this directory."""
import os, re, subprocess, requests, pymupdf, imageio_ffmpeg, shutil
os.makedirs("assets", exist_ok=True); A = "assets/"; R = "/home/user/dreamer4_resources/"
# 1. arXiv HTML figures (Fig 2a/2b, Fig 3)
for f in ["tok", "dyn", "rl"]:
    r = requests.get(f"https://arxiv.org/html/2509.24527v1/{f}.png", headers={"User-Agent": "Mozilla/5.0"}, timeout=60); open(A + f"fig_{f}.png", "wb").write(r.content)
# 2. regions rendered from the paper PDF (page, clip rect in points)
doc = pymupdf.open(R + "papers/2509.24527_Dreamer4_Training_Agents_Inside_Scalable_World_Models.pdf")
for name, pno, clip in [("fig1_teaser_pdf", 1, (72, 391, 540, 664)), ("fig2_world_model_design", 4, (72, 60, 540, 254)), ("fig5_human_interaction_pdf", 11, (80, 89, 540, 240)),
                        ("fig6_robotics", 13, (72, 65, 540, 238)), ("fig7_action_generalization", 14, (72, 56, 540, 205)), ("fig8_shortcut_vs_df", 16, (353, 71, 540, 226)),
                        ("fig11_dreamer3_vs_4", 29, (72, 494, 540, 709))]:
    doc[pno - 1].get_pixmap(matrix=pymupdf.Matrix(2.6, 2.6), clip=pymupdf.Rect(*clip), alpha=False).save(A + name + ".png")
# 3. frames from the official clips (archived from danijar.com)
ff = imageio_ffmpeg.get_ffmpeg_exe(); M = R + "media/official_danijar_com/"
def dur(p):
    m = re.search(r"Duration: (\d+):(\d+):([\d.]+)", subprocess.run([ff, "-i", p], capture_output=True, text=True).stderr); return int(m[1]) * 3600 + int(m[2]) * 60 + float(m[3])
def frame(src, frac, out): subprocess.run([ff, "-y", "-loglevel", "error", "-ss", f"{dur(src) * frac:.2f}", "-i", src, "-frames:v", "1", "-q:v", "2", out])
for i, f in enumerate((0.12, 0.45, 0.78)): frame(M + "teaser.mp4", f, A + f"frame_teaser_{i}.jpg")
for m in ("dreamer", "lucid", "oasis"):
    frame(M + f"human__{m}__task11.mp4", 0.65, A + f"frame_boat_{m}.jpg"); frame(M + f"human__{m}__task12.mp4", 0.75, A + f"frame_portal_{m}.jpg"); frame(M + f"human__{m}__task05.mp4", 0.7, A + f"frame_pickaxe_{m}.jpg")
frame(M + "human__dreamer__task09.mp4", 0.8, A + "frame_diamond_dreamer.jpg"); frame(M + "imag__treechop1.mp4", 0.5, A + "frame_imag_treechop.jpg")
frame(M + "imag__cobble1.mp4", 0.6, A + "frame_imag_cobble.jpg"); frame(M + "realworld__soar1.mp4", 0.5, A + "frame_realworld_soar1.jpg")
shutil.copy(M + "benchmark.png", A + "benchmark.png")
# 4. charts
subprocess.run(["python3", "make_charts.py"], check=True); subprocess.run(["python3", "make_diagrams.py"], check=True); subprocess.run(["python3", "make_stack_diagram.py"], check=True)
subprocess.run(["python3", "make_tech_tree.py"], check=True); subprocess.run(["python3", "make_wm_stack_comparison.py", "--deck"], check=True)
# 5. Genie 3 system diagram (standalone at /home/user/genie3_stack_diagram.png), split into its two rows for two slides
subprocess.run(["python3", "make_genie3_stack_diagram.py"], check=True)
from PIL import Image
g = Image.open("/home/user/genie3_stack_diagram.png"); ppu = g.height / 56.0          # figure spans y = 60 … 4 units
g.crop((0, int((60 - 56.6) * ppu), g.width, int((60 - 30.0) * ppu))).save(A + "genie3_top.png"); g.crop((0, int((60 - 25.6) * ppu), g.width, g.height)).save(A + "genie3_bottom.png")   # rows 01-04 without the figure title; rows 05-07
print("assets ready:", len(os.listdir(A)))

subprocess.run(["python3", "make_landscape.py"], check=True)      # final deck: world-model landscape

# ---- slide 4: official video material (thumbnail, QR codes, teaser poster frame)
import subprocess, requests, segno, imageio_ffmpeg
V = A + "video/"; os.makedirs(V, exist_ok=True)
r = requests.get("https://i.ytimg.com/vi/oDlBtTcX0g0/sddefault.jpg", timeout=30); r.raise_for_status()
open(V + "sddefault.jpg", "wb").write(r.content)
Image.open(V + "sddefault.jpg").crop((0, 60, 640, 420)).save(V + "yt_thumb_16x9.jpg", quality=92)      # 640x480 letterboxed -> 16:9 centre
segno.make("https://www.youtube.com/watch?v=oDlBtTcX0g0", error="m").save(V + "qr_video.png", scale=12, border=2, dark="#14213D", light="#FFFFFF")
segno.make("https://danijar.com/project/dreamer4", error="m").save(V + "qr_project.png", scale=12, border=2, dark="#14213D", light="#FFFFFF")
subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-loglevel", "error", "-ss", "1.0", "-i", "/home/user/dreamer4_resources/media/official_danijar_com/teaser.mp4",
                "-frames:v", "1", "-q:v", "2", V + "teaser_poster.jpg"], check=True)
print("video assets ready:", sorted(os.listdir(V)))
