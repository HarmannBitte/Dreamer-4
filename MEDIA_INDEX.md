# MEDIA INDEX — every video, audio, image and other large artefact connected to the Dreamer 4 material

Compiled 2026-09-20. **Archived** = a copy is in this folder tree. **Listed only** = not downloaded (size/blocking), URL and size recorded so you can fetch it.
Machine-readable companions: `media/_media_manifest.json` (archived files, md5, source URL) and `media/_external_media_urls.json` (all 220 external media URLs probed, with byte sizes).

## 0. Overview

| # | Group | Files | Size | Status |
|---|---|---|---|---|
| 1 | Official Dreamer 4 media on danijar.com (teaser, benchmark figure, 60 result clips) | 62 | 25.6 MB | **archived** → `media/official_danijar_com/` |
| 2 | Announcement-tweet video (X) | 1 | 1.8 MB | **archived** → `media/x_twitter/` |
| 3 | YouTube: 7 cited videos + 5 third-party coverage videos | 12 | — | listed only (metadata + 7 thumbnails in `videos/`) |
| 4 | Audio: TalkRL E73 episode, alphaXiv AI podcast | 2 | 77.3 + 5.9 MB | listed only (TalkRL **transcript** archived in `articles/`) |
| 5 | Dreamer-MC project page videos/images (IamCreateAI) | 26 | 40.0 MB | listed only |
| 6 | Open Dreamer blog media (+ Zenodo mirror) | 15 (+4) | 12.9 MB | listed only; 8 of the small SVG/GIF/JPG files are inside `repos/next-state_open-dreamer/site/public/website/` |
| 7 | MMBench2 project page videos/images (Hansen & Wang 2026) | 106 | 14.3 MB | listed only |
| 8 | Press media (TechXplore video + hero image) | 3 | 4.6 MB | listed only |
| 9 | Other X video on @danijarh (Jan 2026) | 1 | 6.7 MB | listed only |
| 10 | Media kept inside the 14 repo snapshots | 109 images + 23 small MP4s | ≈17 MB | **archived** (part of `repos/`) |
| 11 | Media/data pruned from the repo snapshots | 27 files (+2 dirs) | ≈240 MB + 2.9 GB | listed only → `repos/PRUNED_FILES.txt` |
| 12 | YouTube thumbnails | 7 | 0.1 MB | **archived** → `videos/` |
| 13 | Non-media large artefacts: checkpoints & datasets on Hugging Face | 8 repos | 12 GB + 3.7 TB | listed only → `huggingface/README.md` |

## 1. Official Dreamer 4 media — danijar.com/project/dreamer4 (ARCHIVED, `media/official_danijar_com/`)

These are the `<video>`/`<img>` assets embedded in the official project page (`https://danijar.com/asset/dreamer4/…`). Local file names flatten the path (`human/dreamer/task00.mp4` → `human__dreamer__task00.mp4`). All 62 fetched with HTTP 200; md5 per file in `_media_manifest.json`.

### 1a. Teaser & benchmark figure

| local file | what it shows | size | source |
|---|---|---|---|
| `teaser.mp4` | Project-page teaser video (top of page) | 1.71 MB | https://danijar.com/asset/dreamer4/teaser.mp4 |
| `benchmark.png` | 'Diamonds from Offline Experience' bar chart: success rate (%) on the 12 diamond-challenge milestones (log → planks → crafting table → stick → wooden pickaxe → cobblestone → stone pickaxe → iron ore → furnace → iron ingot → iron pickaxe → diamond) for VPT (finetuned), BC, VLA (Gemma 3) and Dreamer 4 — e.g. iron pickaxe 0 / 0.6 / 11 / 29 %, diamond 0 / 0 / 0 / 0.7 % | 0.30 MB | https://danijar.com/asset/dreamer4/benchmark.png |

### 1b. Imagination Training — agent acting inside the world model (6 clips)

| local file | task | size | source |
|---|---|---|---|
| `imag__treechop1.mp4` | Gather wood — rollout 1 | 0.52 MB | https://danijar.com/asset/dreamer4/imag/treechop1.mp4 |
| `imag__treechop2.mp4` | Gather wood — rollout 2 | 0.37 MB | https://danijar.com/asset/dreamer4/imag/treechop2.mp4 |
| `imag__treechop3.mp4` | Gather wood — rollout 3 | 0.58 MB | https://danijar.com/asset/dreamer4/imag/treechop3.mp4 |
| `imag__cobble1.mp4` | Mine stone — rollout 1 | 0.49 MB | https://danijar.com/asset/dreamer4/imag/cobble1.mp4 |
| `imag__cobble2.mp4` | Mine stone — rollout 2 | 0.24 MB | https://danijar.com/asset/dreamer4/imag/cobble2.mp4 |
| `imag__cobble3.mp4` | Mine stone — rollout 3 | 0.45 MB | https://danijar.com/asset/dreamer4/imag/cobble3.mp4 |

### 1c. Human Interaction — 17 tasks × {Lucid-v1, Oasis, Dreamer 4} (51 clips; the qualitative counterpart of Table 1 in the paper)

Task numbering is the site's own (`taskNN`); names are the captions used on the page.

| task | name | Dreamer 4 | Lucid-v1 | Oasis |
|---|---|---|---|---|
| 00 | Build 3x3 wall from planks | `human__dreamer__task00.mp4` (0.81 MB) | `human__lucid__task00.mp4` (1.06 MB) | `human__oasis__task00.mp4` (0.59 MB) |
| 01 | Eat apple | `human__dreamer__task01.mp4` (0.13 MB) | `human__lucid__task01.mp4` (1.13 MB) | `human__oasis__task01.mp4` (0.25 MB) |
| 02 | Place three torches | `human__dreamer__task02.mp4` (0.21 MB) | `human__lucid__task02.mp4` (0.06 MB) | `human__oasis__task02.mp4` (0.15 MB) |
| 03 | Chop tree | `human__dreamer__task03.mp4` (0.47 MB) | `human__lucid__task03.mp4` (0.59 MB) | `human__oasis__task03.mp4` (0.27 MB) |
| 04 | Dig 3x3 pit with shovel | `human__dreamer__task04.mp4` (0.80 MB) | `human__lucid__task04.mp4` (0.53 MB) | `human__oasis__task04.mp4` (0.51 MB) |
| 05 | Craft wooden pickaxe | `human__dreamer__task05.mp4` (0.16 MB) | `human__lucid__task05.mp4` (0.58 MB) | `human__oasis__task05.mp4` (0.35 MB) |
| 06 | Use furnace and exit | `human__dreamer__task06.mp4` (0.10 MB) | `human__lucid__task06.mp4` (0.18 MB) | `human__oasis__task06.mp4` (0.06 MB) |
| 07 | Place and open workbench | `human__dreamer__task07.mp4` (0.37 MB) | `human__lucid__task07.mp4` (0.41 MB) | `human__oasis__task07.mp4` (0.10 MB) |
| 08 | Kill zombies | `human__dreamer__task08.mp4` (0.36 MB) | `human__lucid__task08.mp4` (0.21 MB) | `human__oasis__task08.mp4` (0.09 MB) |
| 09 | Mine diamonds | `human__dreamer__task09.mp4` (0.27 MB) | `human__lucid__task09.mp4` (0.28 MB) | `human__oasis__task09.mp4` (0.15 MB) |
| 10 | Complete window | `human__dreamer__task10.mp4` (0.52 MB) | `human__lucid__task10.mp4` (0.59 MB) | `human__oasis__task10.mp4` (0.21 MB) |
| 11 | Place and ride boat | `human__dreamer__task11.mp4` (0.60 MB) | `human__lucid__task11.mp4` (0.14 MB) | `human__oasis__task11.mp4` (0.43 MB) |
| 12 | Enter portal | `human__dreamer__task12.mp4` (0.73 MB) | `human__lucid__task12.mp4` (0.30 MB) | `human__oasis__task12.mp4` (0.40 MB) |
| 13 | Place door and walk outside | `human__dreamer__task13.mp4` (0.17 MB) | `human__lucid__task13.mp4` (0.42 MB) | `human__oasis__task13.mp4` (0.15 MB) |
| 14 | Place bed in house and sleep | `human__dreamer__task14.mp4` (0.45 MB) | `human__lucid__task14.mp4` (0.69 MB) | `human__oasis__task14.mp4` (0.52 MB) |
| 15 | Plant reed and pour water | `human__dreamer__task15.mp4` (0.32 MB) | `human__lucid__task15.mp4` (0.38 MB) | `human__oasis__task15.mp4` (0.46 MB) |
| 16 | Turn 360 and enter house | `human__dreamer__task16.mp4` (0.15 MB) | `human__lucid__task16.mp4` (0.57 MB) | `human__oasis__task16.mp4` (0.34 MB) |

Source URL pattern: `https://danijar.com/asset/dreamer4/human/{dreamer|lucid|oasis}/taskNN.mp4`.

### 1d. Real World Video — counterfactual human actions (3 clips)

| local file | caption | size | source |
|---|---|---|---|
| `realworld__soar1.mp4` | Interaction 1 (robot-arm video model, counterfactual human actions) | 0.53 MB | https://danijar.com/asset/dreamer4/realworld/soar1.mp4 |
| `realworld__soar2.mp4` | Interaction 2 (robot-arm video model, counterfactual human actions) | 0.26 MB | https://danijar.com/asset/dreamer4/realworld/soar2.mp4 |
| `realworld__soar3.mp4` | Interaction 3 (robot-arm video model, counterfactual human actions) | 0.38 MB | https://danijar.com/asset/dreamer4/realworld/soar3.mp4 |

## 2. X / Twitter videos

| file / URL | what | size | status |
|---|---|---|---|
| `media/x_twitter/danijarh_1973072288351396320_announcement_video_1280x720.mp4` | video attached to the announcement tweet https://x.com/danijarh/status/1973072288351396320 (30 Sep 2025); other renditions: 640x360 `…/vid/avc1/640x360/0ZjKgKoh44U5UWdj.mp4`, 480x270 `…/vid/avc1/480x270/97vcy1o1S7gYn_-a.mp4` | 1.82 MB | **archived** |
| https://video.twimg.com/amplify_video/2011883006512742400/vid/avc1/1920x1080/p-yRX6XfviBfxoxA.mp4 | a later video post on @danijarh (media id 2011883006512742400 ≈ mid-Jan 2026; tweet text not retrievable, content unverified — may be unrelated to Dreamer 4) | 6.69 MB | listed only |
| https://pbs.twimg.com/amplify_video_thumb/1973071536891502597/img/NMrDqm7YobxinBv4?format=jpg&name=medium | poster frame of the announcement video | — | listed only |

## 3. YouTube (listed only — downloads/captions blocked from the sandbox; thumbnails in `videos/`)

| id | title | channel | URL | relation |
|---|---|---|---|---|
| `oDlBtTcX0g0` | Dreamer 4 | Diamonds from Offline Experience | Danijar Hafner | https://www.youtube.com/watch?v=oDlBtTcX0g0 | official overview video (embedded on the project page and in the TechXplore article) |
| `n4SwlSrkhvU` | Dreamer 4 | Diamond Challenge Uncut #1 | Danijar Hafner | https://www.youtube.com/watch?v=n4SwlSrkhvU | uncut 60-min evaluation episode |
| `5CnpLRM8iXA` | Dreamer 4 | Diamond Challenge Uncut #2 | Danijar Hafner | https://www.youtube.com/watch?v=5CnpLRM8iXA | uncut evaluation episode |
| `oZyliSpRMSw` | Dreamer 4 | Diamond Challenge Uncut #3 | Danijar Hafner | https://www.youtube.com/watch?v=oZyliSpRMSw | uncut evaluation episode |
| `VSKpvb1bnbU` | Dreamer 4 | Diamond Challenge Uncut #4 | Danijar Hafner | https://www.youtube.com/watch?v=VSKpvb1bnbU | uncut evaluation episode |
| `vNCX15fkYkE` | Hack Club AMA w/ Danijar Hafner | Hack Club | https://www.youtube.com/watch?v=vNCX15fkYkE | Dec 2025 AMA |
| `xAXvfVTgqr0` | Learning to Walk in the Real World in 1 Hour (No Simulator) | Danijar Hafner | https://www.youtube.com/watch?v=xAXvfVTgqr0 | 2022 DayDreamer video linked by Analytics Insight — not Dreamer 4 |
| `1jwFoVQO8-s` | Dreamer 4: Scalable World Model for Minecraft | AI Research Roundup | https://www.youtube.com/watch?v=1jwFoVQO8-s | third-party coverage listed (in a commented-out 'coverage' block) in the project-page source |
| `B2ZKokWdoDk` | Training Agents Inside of Scalable World Models (Sep 2025) | AI Paper Slop | https://www.youtube.com/watch?v=B2ZKokWdoDk | third-party coverage, same hidden list |
| `SXHSsIqmzDY` | AI SLOP (I'm Addicted to Sora 2) — segment at t=770s | Dylan Curious | https://www.youtube.com/watch?v=SXHSsIqmzDY | third-party coverage, same hidden list (Dreamer 4 segment starts 12:50) |
| `TzGtJfbCGws` | (title not returned by oEmbed — video private/removed?) — segment at t=307s | The Cutting Edge School | https://www.youtube.com/watch?v=TzGtJfbCGws | third-party coverage, same hidden list |
| `NlzcFKJRXUM` | Training Agents Inside of Scalable World Models | Emergent Mind | https://www.youtube.com/watch?v=NlzcFKJRXUM | AI-generated explainer video embedded on the EmergentMind paper page |

## 4. Audio (listed only)

| URL | what | size | note |
|---|---|---|---|
| https://media.transistor.fm/e440a692/bfc0657e.mp3 | TalkRL podcast E73 'Danijar Hafner on Dreamer v4' (10 Nov 2025); embed https://share.transistor.fm/e/e440a692 | 77.28 MB | full transcript archived: `articles/talkrl_e73_full_transcript.md` |
| https://paper-podcasts.alphaxiv.org/01999b5f-4ac0-71a8-832d-da75e4bd1b18/podcast.mp3 | alphaXiv auto-generated 'paper podcast' for 2509.24527 (AI voices, not the authors) | 5.88 MB | linked from `articles/explainer_alphaxiv_overview.html` |

## 5. Dreamer-MC project page media — IamCreateAI (listed only)

Rollout videos of the 1.7 B Dreamer-MC Minecraft world model (`video/*.mp4`, grouped by interaction: arrow, boat, bucket, consume item, mining, portal, sleep, plus `first_view`) and the four explanatory figures (`image/*`). Page: https://findlamp.github.io/dreamer-mc.github.io/ . The 19 start-frame PNGs used by its UI are archived in `repos/IamCreateAI_Dreamerv4-MC/ui/static/start_frames/`.

| file | size | URL |
|---|---|---|
| `image/compute_compare.png` | 6.18 MB | https://findlamp.github.io/dreamer-mc.github.io/image/compute_compare.png |
| `image/dynamic_attn.png` | 5.90 MB | https://findlamp.github.io/dreamer-mc.github.io/image/dynamic_attn.png |
| `image/ringbuffer.jpg` | 0.12 MB | https://findlamp.github.io/dreamer-mc.github.io/image/ringbuffer.jpg |
| `image/tokenizer.jpg` | 0.14 MB | https://findlamp.github.io/dreamer-mc.github.io/image/tokenizer.jpg |
| `video/arrow_01.mp4` | 1.02 MB | https://findlamp.github.io/dreamer-mc.github.io/video/arrow_01.mp4 |
| `video/arrow_02.mp4` | 0.63 MB | https://findlamp.github.io/dreamer-mc.github.io/video/arrow_02.mp4 |
| `video/arrow_03.mp4` | 1.96 MB | https://findlamp.github.io/dreamer-mc.github.io/video/arrow_03.mp4 |
| `video/boat_01.mp4` | 1.47 MB | https://findlamp.github.io/dreamer-mc.github.io/video/boat_01.mp4 |
| `video/boat_02.mp4` | 3.55 MB | https://findlamp.github.io/dreamer-mc.github.io/video/boat_02.mp4 |
| `video/boat_03.mp4` | 2.24 MB | https://findlamp.github.io/dreamer-mc.github.io/video/boat_03.mp4 |
| `video/bucket_01.mp4` | 0.52 MB | https://findlamp.github.io/dreamer-mc.github.io/video/bucket_01.mp4 |
| `video/bucket_02.mp4` | 1.20 MB | https://findlamp.github.io/dreamer-mc.github.io/video/bucket_02.mp4 |
| `video/bucket_03.mp4` | 1.14 MB | https://findlamp.github.io/dreamer-mc.github.io/video/bucket_03.mp4 |
| `video/consume_item_01.mp4` | 0.25 MB | https://findlamp.github.io/dreamer-mc.github.io/video/consume_item_01.mp4 |
| `video/consume_item_02.mp4` | 0.36 MB | https://findlamp.github.io/dreamer-mc.github.io/video/consume_item_02.mp4 |
| `video/consume_item_03.mp4` | 0.41 MB | https://findlamp.github.io/dreamer-mc.github.io/video/consume_item_03.mp4 |
| `video/first_view.mp4` | 4.00 MB | https://findlamp.github.io/dreamer-mc.github.io/video/first_view.mp4 |
| `video/mining_01.mp4` | 0.87 MB | https://findlamp.github.io/dreamer-mc.github.io/video/mining_01.mp4 |
| `video/mining_02.mp4` | 4.10 MB | https://findlamp.github.io/dreamer-mc.github.io/video/mining_02.mp4 |
| `video/mining_03.mp4` | 0.67 MB | https://findlamp.github.io/dreamer-mc.github.io/video/mining_03.mp4 |
| `video/portal_01.mp4` | 0.73 MB | https://findlamp.github.io/dreamer-mc.github.io/video/portal_01.mp4 |
| `video/portal_02.mp4` | 1.03 MB | https://findlamp.github.io/dreamer-mc.github.io/video/portal_02.mp4 |
| `video/portal_03.mp4` | 0.51 MB | https://findlamp.github.io/dreamer-mc.github.io/video/portal_03.mp4 |
| `video/sleep_01.mp4` | 0.37 MB | https://findlamp.github.io/dreamer-mc.github.io/video/sleep_01.mp4 |
| `video/sleep_02.mp4` | 0.36 MB | https://findlamp.github.io/dreamer-mc.github.io/video/sleep_02.mp4 |
| `video/sleep_03.mp4` | 0.31 MB | https://findlamp.github.io/dreamer-mc.github.io/video/sleep_03.mp4 |

*26 files, 40.03 MB total.*

## 6. Open Dreamer blog media — next-state (listed only, small files partly in the repo snapshot)

Page: https://next-state.github.io/open-dreamer/ ('How to train a frontier world model'). `coinrun-wm.mp4`, `comparison.mp4`, `coinrun.gif` and the 5.9 MB `xpred-vpred-noise-comparison.svg` were pruned from the local repo snapshot; the remaining SVG/GIF/JPG files exist locally under `repos/next-state_open-dreamer/site/public/website/`. Zenodo mirror of the same media (record 21475232, DOI page archived as `articles/zenodo_open_dreamer_doi.*`): `https://zenodo.org/records/21475232/files/{coinrun-wm.mp4,comparison.mp4,coinrun.gif,behaviour-cloning.gif}` — Zenodo answers HTTP 403 to scripted download, open in a browser.

| file | size | URL |
|---|---|---|
| `behaviour-cloning.gif` | 0.08 MB | https://next-state.github.io/open-dreamer/website/behaviour-cloning.gif |
| `causal-sequence.svg` | 0.01 MB | https://next-state.github.io/open-dreamer/website/causal-sequence.svg |
| `causal-space-time.svg` | 0.02 MB | https://next-state.github.io/open-dreamer/website/causal-space-time.svg |
| `coinrun-tokenizer.jpg` | 0.03 MB | https://next-state.github.io/open-dreamer/website/coinrun-tokenizer.jpg |
| `coinrun-wm.mp4` | 1.05 MB | https://next-state.github.io/open-dreamer/website/coinrun-wm.mp4 |
| `coinrun.gif` | 2.49 MB | https://next-state.github.io/open-dreamer/website/coinrun.gif |
| `comparison.mp4` | 3.07 MB | https://next-state.github.io/open-dreamer/website/comparison.mp4 |
| `compute_scaling_reconstructed.svg` | 0.00 MB | https://next-state.github.io/open-dreamer/website/compute_scaling_reconstructed.svg |
| `diffusion-forcing.svg` | 1.40 MB | https://next-state.github.io/open-dreamer/website/diffusion-forcing.svg |
| `hollow-inside.jpg` | 0.02 MB | https://next-state.github.io/open-dreamer/website/hollow-inside.jpg |
| `maetok-autoencoder-platformer.svg` | 0.25 MB | https://next-state.github.io/open-dreamer/website/maetok-autoencoder-platformer.svg |
| `optimizer-comparison.svg` | 0.02 MB | https://next-state.github.io/open-dreamer/website/optimizer-comparison.svg |
| `roofline-analysis.svg` | 0.00 MB | https://next-state.github.io/open-dreamer/website/roofline-analysis.svg |
| `search-space.svg` | 0.00 MB | https://next-state.github.io/open-dreamer/website/search-space.svg |
| `xpred-vpred-noise-comparison.svg` | 4.50 MB | https://next-state.github.io/open-dreamer/website/xpred-vpred-noise-comparison.svg |

*15 files, 12.94 MB total.*

## 7. MMBench2 project page media — Hansen & Wang 2026 (listed only)

Page: https://www.nicklashansen.com/mmbench2/ . 80 MP4 clips + 25 PNG figures + 1 poster, 14.3 MB in total. URL prefix `https://www.nicklashansen.com/mmbench2/` + path.

| folder | purpose | files | size | file names |
|---|---|---|---|---|
| `images/` | poster | 1 | 0.02 MB | demo-poster.jpg |
| `images/coverage/` | coverage density + hallucination heat-maps | 12 | 0.40 MB | cup-catch_density.png, cup-catch_hallu_u_r.png, cup-catch_initial.png, lunarlander-takeoff_hallu_coverage.png, lunarlander-takeoff_hallu_u_r.png, lunarlander-takeoff_initial.png, og-point-maze_density.png, og-point-maze_hallu_u_r.png, og-point-maze_initial.png, pygame-rocket-collect_density.png, pygame-rocket-collect_hallu_u_r.png, pygame-rocket-collect_initial.png |
| `images/datacoll/` | data-collection bottleneck figures (curiosity/expert/human/noop/random) | 5 | 0.30 MB | bottleneck_curiosity.png, bottleneck_expert.png, bottleneck_human.png, bottleneck_noop.png, bottleneck_random.png |
| `images/perceptual/` | perceptual-hallucination input vs decoded frames | 8 | 0.19 MB | cupcatch_decoded.png, cupcatch_input.png, pmaze_decoded.png, pmaze_input.png, pong_decoded.png, pong_input.png, reacher_decoded.png, reacher_input.png |
| `videos/coverage/` | coverage / data-density examples (ground truth) | 4 | 0.22 MB | cup-catch_gt.mp4, lunarlander-takeoff_gt.mp4, og-point-maze_gt.mp4, pygame-rocket-collect_gt.mp4 |
| `videos/finetune/` | 50-trajectory adaptation: gt / pre-adaptation / post-adaptation | 12 | 2.35 MB | cup-catch-var1_gt.mp4, cup-catch-var1_post.mp4, cup-catch-var1_pre.mp4, og-point-var1_gt.mp4, og-point-var1_post.mp4, og-point-var1_pre.mp4, pygame-dungeon-explorer1_gt.mp4, pygame-dungeon-explorer1_post.mp4, pygame-dungeon-explorer1_pre.mp4, pygame-reacher-easy_gt.mp4, pygame-reacher-easy_post.mp4, pygame-reacher-easy_pre.mp4 |
| `videos/realvs/` | real vs. counterfactual-action rollouts (left/none/right, flip/zero/real) | 15 | 1.13 MB | mujoco-walker_flip.mp4, mujoco-walker_real.mp4, mujoco-walker_zero.mp4, mw-pick-place_left.mp4, mw-pick-place_none.mp4, mw-pick-place_right.mp4, og-point-arena_left.mp4, og-point-arena_none.mp4, og-point-arena_right.mp4, pygame-highway_left.mp4, pygame-highway_none.mp4, pygame-highway_right.mp4, walker-run_flip.mp4, walker-run_real.mp4, walker-run_zero.mp4 |
| `videos/rollouts/` | ground-truth vs world-model rollouts | 4 | 0.80 MB | cup-catch-good_gt.mp4, cup-catch-good_wm.mp4, mw-push-base_gt.mp4, mw-push-base_wm.mp4 |
| `videos/scene/` | scene-divergence hallucination examples (gt vs wm) | 6 | 0.54 MB | og-point-bottleneck_gt.mp4, og-point-bottleneck_wm.mp4, pygame-foraging_gt.mp4, pygame-foraging_wm.mp4, pygame-point-maze-var4_gt.mp4, pygame-point-maze-var4_wm.mp4 |
| `videos/teaser/` | teaser grid — one clip per benchmark task (world-model rollouts) | 39 | 8.36 MB | atari-boxing.mp4, atari-ms-pacman.mp4, atari-road-runner.mp4, bipedal-walker-hills.mp4, cartpole-swingup.mp4, cheetah-run.mp4, cup-catch.mp4, finger-turn-hard.mp4, hopper-hop.mp4, lunarlander-hover.mp4, ms-ant-run.mp4, ms-hopper-hop.mp4, mujoco-ant.mp4, mujoco-walker.mp4, mw-assembly.mp4, mw-pick-place.mp4, mw-soccer.mp4, mw-window-close.mp4, og-ant.mp4, og-point-maze.mp4, og-point-spiral.mp4, pygame-air-hockey.mp4, pygame-bird-attack.mp4, pygame-coinrun.mp4, pygame-dungeon-explorer1.mp4, pygame-foraging.mp4, pygame-highway.mp4, pygame-landing.mp4, pygame-point-maze-var1.mp4, pygame-pong.mp4, pygame-reacher-easy.mp4, pygame-rocket-collect.mp4, pygame-spaceship.mp4, pygame-whirlpool.mp4, quadruped-run.mp4, rd-open-slide.mp4, rd-push-green.mp4, reacher-hard.mp4, walker-run.mp4 |

## 8. Press media (listed only)

| URL | what | size |
|---|---|---|
| https://scx2.b-cdn.net/gfx/video/2025/deepmind-introduces-an.mp4 | TechXplore article (Oct 2025) embedded video — re-hosted Dreamer 4 footage | 2.53 MB |
| https://scx2.b-cdn.net/gfx/video/2025/deepmind-introduces-an-1.mp4 | TechXplore article (Oct 2025) embedded video — re-hosted Dreamer 4 footage | 2.11 MB |
| https://scx1.b-cdn.net/csz/news/800a/2025/deepmind-introduces-an.jpg | TechXplore article (Oct 2025) embedded hero image — re-hosted Dreamer 4 footage | 0.00 MB |
| https://www.youtube.com/embed/oDlBtTcX0g0 | TechXplore also embeds the official YouTube video | — |

## 10. Media kept inside the repo snapshots (ARCHIVED as part of `repos/`)

| repo folder | files | size | types | notable content |
|---|---|---|---|---|
| `nicklashansen_dreamer4` | 17 | 5.60 MB | png×9, gif×8 | README figures `assets/1-3.png`, `4.gif`, 7 DMControl task GIFs, tokenizer/dynamics training curves |
| `IamCreateAI_Dreamerv4-MC` | 19 | 4.29 MB | png×19 | 19 Minecraft start-frame PNGs for the demo UI (`ui/static/start_frames/`) |
| `nicklashansen_mmbench2` | 10 | 3.41 MB | gif×9, png×1 | `assets/0.gif`, `1.png`, 8 task GIFs (Atari, BipedalWalker, MetaWorld, OGBench, PyGame, RoboDesk, Walker) |
| `skr3178_DreamerV4` | 6 | 1.63 MB | gif×5, png×1 | 5 tokenizer-reconstruction GIFs + 1 reconstruction PNG |
| `vijayabhaskar-ev_dreamer_v4` | 7 | 1.25 MB | png×6, gif×1 | site hero images + `world_model_rollout.gif` |
| `HKimiwada_Dreamer4` | 24 | 1.23 MB | mp4×21, png×3 | 23 tiny Atari world-model result MP4s (dream/rollout/counterfactual) + eval plots; the six large Minecraft MP4s were pruned |
| `next-state_open-dreamer` | 12 | 0.78 MB | svg×9, jpg×2, gif×1 | blog SVG/GIF/JPG figures (`site/public/website/`) + Reactor logos |
| `edwhu_dreamer4-jax` | 6 | 0.51 MB | png×5, gif×1 | architecture / training-curve PNGs + `video.gif` demo |
| `lucidrains_dreamer4` | 3 | 0.51 MB | mp4×2, png×1 | `dreamer4-fig2.png` (paper figure 2) + two 1-frame mock test videos |
| `chrisgao99_dreamer4` | 8 | 0.33 MB | png×7, svg×1 | Waymo docs figures; README assets identical to nicklashansen_dreamer4 were removed (see `DEDUPED_FILES.txt`) |
| `reactor-team_open-dreamer` | 2 | 0.01 MB | svg×2 | Reactor logos |

## 11. Media/data pruned from the repo snapshots (listed only — full list with sizes in `repos/PRUNED_FILES.txt`)

| size | removed file | download |
|---|---|---|
| 48.6 MB | `next-state_open-dreamer/dreamer/fvd/i3d_pretrained_400.npz` | https://github.com/next-state/open-dreamer/blob/main/dreamer/fvd/i3d_pretrained_400.npz?raw=true |
| 16.5 MB | `HKimiwada_Dreamer4/inference/results/world_model/minecraft/latest_multistep.mp4` | https://github.com/HKimiwada/Dreamer4/blob/main/inference/results/world_model/minecraft/latest_multistep.mp4?raw=true |
| 16.5 MB | `HKimiwada_Dreamer4/inference/results/world_model/minecraft/multistep_inference.mp4` | https://github.com/HKimiwada/Dreamer4/blob/main/inference/results/world_model/minecraft/multistep_inference.mp4?raw=true |
| 16.5 MB | `HKimiwada_Dreamer4/inference/results/world_model/minecraft/one_step_inference.mp4` | https://github.com/HKimiwada/Dreamer4/blob/main/inference/results/world_model/minecraft/one_step_inference.mp4?raw=true |
| 16.5 MB | `HKimiwada_Dreamer4/inference/results/world_model/minecraft/latest_singlestep.mp4` | https://github.com/HKimiwada/Dreamer4/blob/main/inference/results/world_model/minecraft/latest_singlestep.mp4?raw=true |
| 8.7 MB | `HKimiwada_Dreamer4/inference/results/tokenizer/reconstructed_output.mp4` | https://github.com/HKimiwada/Dreamer4/blob/main/inference/results/tokenizer/reconstructed_output.mp4?raw=true |
| 8.1 MB | `HKimiwada_Dreamer4/inference/results/tokenizer/v2_reconstructed_output.mp4` | https://github.com/HKimiwada/Dreamer4/blob/main/inference/results/tokenizer/v2_reconstructed_output.mp4?raw=true |
| 5.9 MB | `next-state_open-dreamer/site/public/website/xpred-vpred-noise-comparison.svg` | https://github.com/next-state/open-dreamer/blob/main/site/public/website/xpred-vpred-noise-comparison.svg?raw=true |
| 3.6 MB | `skr3178_DreamerV4/DreamerV4.pdf` | https://github.com/skr3178/DreamerV4/blob/pretrained_tokenizer/DreamerV4.pdf?raw=true |
| 3.6 MB | `vijayabhaskar-ev_dreamer_v4/assets/hero_exploiting.gif` | https://github.com/vijayabhaskar-ev/dreamer_v4/blob/main/assets/hero_exploiting.gif?raw=true |
| 3.5 MB | `vijayabhaskar-ev_dreamer_v4/assets/hero_healthy.gif` | https://github.com/vijayabhaskar-ev/dreamer_v4/blob/main/assets/hero_healthy.gif?raw=true |
| 3.5 MB | `reactor-team_open-dreamer/assets/banner.png` | https://github.com/reactor-team/open-dreamer/blob/main/assets/banner.png?raw=true |
| 3.5 MB | `next-state_open-dreamer/assets/banner.png` | https://github.com/next-state/open-dreamer/blob/main/assets/banner.png?raw=true |
| 3.1 MB | `next-state_open-dreamer/site/public/website/comparison.mp4` | https://github.com/next-state/open-dreamer/blob/main/site/public/website/comparison.mp4?raw=true |
| 3.0 MB | `vijayabhaskar-ev_dreamer_v4/assets/policy_stochastic_catch.gif` | https://github.com/vijayabhaskar-ev/dreamer_v4/blob/main/assets/policy_stochastic_catch.gif?raw=true |
| 2.5 MB | `next-state_open-dreamer/site/public/website/coinrun.gif` | https://github.com/next-state/open-dreamer/blob/main/site/public/website/coinrun.gif?raw=true |
| 2.4 MB | `skr3178_DreamerV4/Notes/5.jpeg` | https://github.com/skr3178/DreamerV4/blob/pretrained_tokenizer/Notes/5.jpeg?raw=true |
| 2.3 MB | `edwhu_dreamer4-jax/docs/rl-cropped.gif` | https://github.com/edwhu/dreamer4-jax/blob/main/docs/rl-cropped.gif?raw=true |
| 2.2 MB | `skr3178_DreamerV4/Notes/3.jpeg` | https://github.com/skr3178/DreamerV4/blob/pretrained_tokenizer/Notes/3.jpeg?raw=true |
| 2.1 MB | `skr3178_DreamerV4/Notes/2.jpeg` | https://github.com/skr3178/DreamerV4/blob/pretrained_tokenizer/Notes/2.jpeg?raw=true |
| 2.1 MB | `skr3178_DreamerV4/Notes/1.jpeg` | https://github.com/skr3178/DreamerV4/blob/pretrained_tokenizer/Notes/1.jpeg?raw=true |
| 2.1 MB | `skr3178_DreamerV4/Notes/4.jpeg` | https://github.com/skr3178/DreamerV4/blob/pretrained_tokenizer/Notes/4.jpeg?raw=true |
| 1.9 MB | `next-state_open-dreamer/site/public/website/diffusion-forcing.svg` | https://github.com/next-state/open-dreamer/blob/main/site/public/website/diffusion-forcing.svg?raw=true |
| 1.4 MB | `edwhu_dreamer4-jax/docs/imagination-cropped.gif` | https://github.com/edwhu/dreamer4-jax/blob/main/docs/imagination-cropped.gif?raw=true |
| 1.1 MB | `nicklashansen_dreamer4/assets/0.gif` | https://github.com/nicklashansen/dreamer4/blob/main/assets/0.gif?raw=true |
| 1.1 MB | `chrisgao99_dreamer4/assets/0.gif` | https://github.com/chrisgao99/dreamer4/blob/main/assets/0.gif?raw=true |
| 1.0 MB | `next-state_open-dreamer/site/public/website/coinrun-wm.mp4` | https://github.com/next-state/open-dreamer/blob/main/site/public/website/coinrun-wm.mp4?raw=true |
| 2.8 GB | `chrisgao99_dreamer4/waymo/cache/` (directory) | regenerate with the repo's Waymo preprocessing scripts (see `repos/chrisgao99_dreamer4/waymo/PRUNED_DIRS.txt`) |
| 107 MB | `chrisgao99_dreamer4/waymo/eval_results/` (directory) | https://github.com/chrisgao99/dreamer4/tree/main/waymo/eval_results |

## 12. YouTube thumbnails (ARCHIVED, `videos/`)

`<id>_thumbnail.jpg` for the 7 cited videos (source `https://i.ytimg.com/vi/<id>/hqdefault.jpg`); metadata in `videos/_video_metadata.json`.

## 13. Non-media large artefacts (listed only — details in `huggingface/README.md`)

| artefact | size | URL |
|---|---|---|
| Dreamer-MC 1.7 B Minecraft world-model weights (IamCreateAI/Dreamerv4-MC) | 4.2 GB | https://huggingface.co/IamCreateAI/Dreamerv4-MC |
| nicklashansen/dreamer4 DMControl tokenizer + dynamics | 0.77 GB | https://huggingface.co/nicklashansen/dreamer4 |
| nicklashansen/mmbench2-models (base / coverage-aware / combined) | 4.27 GB | https://huggingface.co/nicklashansen/mmbench2-models |
| vijayabhaskarev/dreamer-v4 checkpoints (WM, BC seeds, agents) | 2.93 GB | https://huggingface.co/vijayabhaskarev/dreamer-v4 |
| dataset nicklashansen/dreamer4 (DMControl trajectories) | 30.9 GB | https://huggingface.co/datasets/nicklashansen/dreamer4 |
| dataset nicklashansen/mmbench2 | 113.9 GB | https://huggingface.co/datasets/nicklashansen/mmbench2 |
| dataset zhwang4ai/OpenAI-Minecraft-Contractor (VPT contractor data mirror) | 1,688 GB | https://huggingface.co/datasets/zhwang4ai/OpenAI-Minecraft-Contractor |
| dataset p-doom/open_ai_minecraft_arrayrecords_chunked (VPT data as ArrayRecord shards) | 1,871 GB | https://huggingface.co/datasets/p-doom/open_ai_minecraft_arrayrecords_chunked |
| I3D FVD network `i3d_pretrained_400.npz` (open-dreamer) | 48.6 MB | https://github.com/next-state/open-dreamer/blob/main/dreamer/fvd/i3d_pretrained_400.npz?raw=true |
| Official Dreamer 4 checkpoints / code | — | **never released by DeepMind** |
