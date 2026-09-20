# videos/ — YouTube material cited in the report (metadata + thumbnails only)

**No video files were downloaded.** Two independent blockers: (1) full videos are tens–hundreds of MB each and would blow the workspace size cap;
(2) YouTube blocks this sandbox's download tooling (`yt-dlp 2026.08.19` → *"Sign in to confirm you're not a bot"*, no cookies available), and the
`timedtext` caption endpoint returned empty bodies for both manual and auto-generated (`kind=asr`) English tracks, so **no transcripts** could be saved either.
What *did* work: the public oEmbed endpoint (title + channel) and the `i.ytimg.com` thumbnail CDN. Everything retrieved is in `_video_metadata.json`.

| Video ID | Title (oEmbed) | Channel | URL | Thumbnail | Why it is cited |
|---|---|---|---|---|---|
| `oDlBtTcX0g0` | Dreamer 4 \| Diamonds from Offline Experience | Danijar Hafner | https://www.youtube.com/watch?v=oDlBtTcX0g0 | `oDlBtTcX0g0_thumbnail.jpg` | official Dreamer 4 overview video linked from danijar.com/project/dreamer4 and the announcement tweet |
| `n4SwlSrkhvU` | Dreamer 4 \| Diamond Challenge Uncut #1 | Danijar Hafner | https://www.youtube.com/watch?v=n4SwlSrkhvU | `n4SwlSrkhvU_thumbnail.jpg` | uncut 60-min evaluation episode ending in a diamond (evidence for the 0.7 % diamond result) |
| `5CnpLRM8iXA` | Dreamer 4 \| Diamond Challenge Uncut #2 | Danijar Hafner | https://www.youtube.com/watch?v=5CnpLRM8iXA | `5CnpLRM8iXA_thumbnail.jpg` | uncut evaluation episode #2 |
| `oZyliSpRMSw` | Dreamer 4 \| Diamond Challenge Uncut #3 | Danijar Hafner | https://www.youtube.com/watch?v=oZyliSpRMSw | `oZyliSpRMSw_thumbnail.jpg` | uncut evaluation episode #3 |
| `VSKpvb1bnbU` | Dreamer 4 \| Diamond Challenge Uncut #4 | Danijar Hafner | https://www.youtube.com/watch?v=VSKpvb1bnbU | `VSKpvb1bnbU_thumbnail.jpg` | uncut evaluation episode #4 |
| `vNCX15fkYkE` | Hack Club AMA w/ Danijar Hafner | Hack Club | https://www.youtube.com/watch?v=vNCX15fkYkE | `vNCX15fkYkE_thumbnail.jpg` | Dec 2025 AMA (post-DeepMind) — listed in the report as *not watched*, no transcript available |
| `xAXvfVTgqr0` | Learning to Walk in the Real World in 1 Hour (No Simulator) | Danijar Hafner | https://www.youtube.com/watch?v=xAXvfVTgqr0 | `xAXvfVTgqr0_thumbnail.jpg` | **not a Dreamer 4 video** — Hafner's 2022 DayDreamer robot video, linked by the Analytics Insight article as robotics context |

**Archived elsewhere:** the official project page's own 62 media assets (teaser MP4, benchmark PNG, 60 result clips) are *not* on YouTube and **are archived** in `../media/official_danijar_com/` (see `../MEDIA_INDEX.md`).
Five further third-party YouTube videos about Dreamer 4 (AI Research Roundup `1jwFoVQO8-s`, AI Paper Slop `B2ZKokWdoDk`, Dylan Curious `SXHSsIqmzDY` @12:50, The Cutting Edge School `TzGtJfbCGws` @5:07, Emergent Mind `NlzcFKJRXUM`) are listed in `../MEDIA_INDEX.md` §3.

Audio/podcast material related to the videos:

* TalkRL episode 73 "Danijar Hafner on Dreamer v4" (10 Nov 2025) — the **full transcript is archived** at `../articles/talkrl_e73_full_transcript.md` (85 KB).
  The MP3 itself (`https://media.transistor.fm/e440a692/bfc0657e.mp3`, embed `https://share.transistor.fm/e/e440a692`) was *not* downloaded (size budget); URL kept here for reference.

How to get the videos yourself: `yt-dlp --cookies-from-browser <browser> https://www.youtube.com/watch?v=<id>` from a logged-in machine, or
`yt-dlp --write-auto-subs --skip-download` for transcripts only.
