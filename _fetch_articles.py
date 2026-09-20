"""Fetch web resources referenced in the Dreamer 4 research report.
Saves raw HTML + extracted Markdown for each page and writes a manifest."""
import json, os, re, time, sys
import requests, trafilatura

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "articles")
os.makedirs(OUT, exist_ok=True)
HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
           "Accept-Language": "en-US,en;q=0.9"}

PAGES = [
    # (slug, url, category)
    ("official_project_page_danijar", "https://danijar.com/project/dreamer4/", "official"),
    ("official_short_url_danijar_dreamer4", "https://danijar.com/dreamer4/", "official"),
    ("talkrl_e73_episode_page", "https://www.talkrl.com/episodes/danijar-hafner-on-dreamer-v4", "talks"),
    ("talkrl_e73_full_transcript", "https://www.talkrl.com/episodes/danijar-hafner-on-dreamer-v4/transcript", "talks"),
    ("open_dreamer_blog_how_to_train_a_frontier_world_model", "https://next-state.github.io/open-dreamer/", "reproductions"),
    ("dreamer_mc_blog_findlamp", "https://findlamp.github.io/dreamer-mc.github.io/", "reproductions"),
    ("mmbench2_project_page_hansen", "https://www.nicklashansen.com/mmbench2/", "followups"),
    ("jasmine_project_page_pdoom", "https://pdoom.org/jasmine.html", "followups"),
    ("deepwiki_edwhu_dreamer4_jax", "https://deepwiki.com/edwhu/dreamer4-jax", "reproductions"),
    ("press_techxplore_2025_10", "https://techxplore.com/news/2025-10-deepmind-ai-agent-tasks-scalable.html", "press"),
    ("press_infoq_2025_10", "https://www.infoq.com/news/2025/10/dreamer-4-minecraft-agent/", "press"),
    ("press_implicator_2026_02", "https://www.implicator.ai/dreamer-4-mines-diamonds-in-an-imagined-minecraft/", "press"),
    ("press_mit_tech_review_hafner_2026_09", "https://www.technologyreview.com/2026/09/08/1142088/danijar-hafner-developing-plan-ahead-agents/", "press"),
    ("press_analytics_insight_open_dreamer_2026_09", "https://www.analyticsinsight.net/artificial-intelligence/the-model-deepmind-described-but-never-released", "press"),
    ("press_36kr_hafner_leaves_deepmind", "https://eu.36kr.com/en/p/3539389679104131", "press"),
    ("press_cryptobriefing_hafner_startup", "https://cryptobriefing.com/danijar-hafner-ai-agents-startup/", "press"),
    ("explainer_arxiviq_substack", "https://arxiviq.substack.com/p/dreamer-4-training-agents-inside", "explainers"),
    ("explainer_pith_review", "https://pith.science/paper/2509.24527", "explainers"),
    ("explainer_emergentmind_paper", "https://www.emergentmind.com/papers/2509.24527", "explainers"),
    ("explainer_emergentmind_topic", "https://www.emergentmind.com/topics/dreamer-4", "explainers"),
    ("explainer_alphaxiv_overview", "https://www.alphaxiv.org/overview/2509.24527", "explainers"),
    ("explainer_haroldbenoit_notes", "https://haroldbenoit.com/notes/ml/llms/multi-modality/video/dreamer-4", "explainers"),
    ("explainer_medium_suzuki_intuitive_understanding", "https://medium.com/@schunsukesuzuki/first-intuitive-understanding-dreamer-v4-scaling-world-models-to-complex-environments-with-67a4c5119e15", "explainers"),
    ("explainer_awesomepapers", "https://awesomepapers.io/reinforcement-learning/papers/2509.24527", "explainers"),
    ("hf_model_IamCreateAI_Dreamerv4-MC", "https://huggingface.co/IamCreateAI/Dreamerv4-MC", "huggingface"),
    ("hf_model_nicklashansen_dreamer4", "https://huggingface.co/nicklashansen/dreamer4", "huggingface"),
    ("hf_dataset_nicklashansen_dreamer4", "https://huggingface.co/datasets/nicklashansen/dreamer4", "huggingface"),
    ("hf_model_vijayabhaskarev_dreamer-v4", "https://huggingface.co/vijayabhaskarev/dreamer-v4", "huggingface"),
    ("hf_dataset_zhwang4ai_OpenAI-Minecraft-Contractor", "https://huggingface.co/datasets/zhwang4ai/OpenAI-Minecraft-Contractor", "huggingface"),
    ("github_readme_next-state_open-dreamer", "https://github.com/next-state/open-dreamer", "repos"),
    ("github_readme_lucidrains_dreamer4", "https://github.com/lucidrains/dreamer4", "repos"),
    ("github_readme_nicklashansen_dreamer4", "https://github.com/nicklashansen/dreamer4", "repos"),
    ("github_readme_nicklashansen_mmbench2", "https://github.com/nicklashansen/mmbench2", "repos"),
    ("github_readme_vijayabhaskar-ev_dreamer_v4", "https://github.com/vijayabhaskar-ev/dreamer_v4", "repos"),
    ("github_readme_IamCreateAI_Dreamerv4-MC", "https://github.com/IamCreateAI/Dreamerv4-MC", "repos"),
    ("github_readme_edwhu_dreamer4-jax", "https://github.com/edwhu/dreamer4-jax", "repos"),
    ("github_readme_4ku_dreamer4", "https://github.com/4ku/dreamer4", "repos"),
    ("github_readme_reactor-team_open-dreamer", "https://github.com/reactor-team/open-dreamer", "repos"),
    ("zenodo_open_dreamer_doi", "https://doi.org/10.5281/zenodo.21475232", "reproductions"),
    ("community_hn_45923945", "https://news.ycombinator.com/item?id=45923945", "community"),
    ("community_reddit_accelerate_1nvbfm1", "https://old.reddit.com/r/accelerate/comments/1nvbfm1/", "community"),
    ("community_reddit_mlscaling_1nvfkgu", "https://old.reddit.com/r/mlscaling/comments/1nvfkgu/", "community"),
    ("community_reddit_singularity_1nv4zna", "https://old.reddit.com/r/singularity/comments/1nv4zna/", "community"),
    ("community_reddit_reinforcementlearning_1nu4cub", "https://old.reddit.com/r/reinforcementlearning/comments/1nu4cub/", "community"),
    ("community_x_danijar_announcement_1973072288351396320", "https://cdn.syndication.twimg.com/tweet-result?id=1973072288351396320&token=a", "community"),
    ("community_x_danijar_talkrl_1987968769462067218", "https://cdn.syndication.twimg.com/tweet-result?id=1987968769462067218&token=a", "community"),
    ("community_x_danijar_profile", "https://x.com/danijarh", "community"),
]

manifest = []
for slug, url, cat in PAGES:
    rec = {"slug": slug, "url": url, "category": cat}
    try:
        r = requests.get(url, headers=HEADERS, timeout=40, allow_redirects=True)
        rec["status"] = r.status_code
        rec["final_url"] = r.url
        ctype = r.headers.get("content-type", "")
        rec["content_type"] = ctype
        raw = r.content
        ext = ".json" if "json" in ctype else (".pdf" if "pdf" in ctype else ".html")
        raw_path = os.path.join(OUT, slug + ext)
        with open(raw_path, "wb") as f:
            f.write(raw)
        rec["raw_file"] = os.path.basename(raw_path)
        rec["raw_bytes"] = len(raw)
        if ext == ".html" and r.status_code == 200:
            md = trafilatura.extract(r.text, url=url, output_format="markdown", include_links=True,
                                     include_tables=True, include_images=False, include_comments=True,
                                     favor_recall=True)
            if md and len(md) > 200:
                md_path = os.path.join(OUT, slug + ".md")
                with open(md_path, "w") as f:
                    f.write(f"<!-- source: {url}\n     fetched: {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())} -->\n\n")
                    f.write(md)
                rec["markdown_file"] = os.path.basename(md_path)
                rec["markdown_chars"] = len(md)
            else:
                rec["markdown_file"] = None
        print(f"{r.status_code:>4}  {len(raw):>9}  {slug}")
    except Exception as e:
        rec["status"] = "error"; rec["error"] = str(e)[:200]
        print(f" ERR  {slug}: {e}")
    manifest.append(rec)
    time.sleep(0.5)

with open(os.path.join(OUT, "_manifest.json"), "w") as f:
    json.dump(manifest, f, indent=2)
print("done", len(manifest))
