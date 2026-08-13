---
okf_version: "0.1"
type: "documentation"
title: "Multi-Channel Documentation Delivery & SEO Engine"
timestamp: "2026-08-13T14:19:24Z"
topics: ["openwiki", "publishing", "delivery", "seo", "mkdocs"]
description: "MkDocs nav, GitHub Pages, RTD, Render, GitBook, SEO sitemaps."
---
# Multi-Channel Documentation Delivery & SEO Engine

DSOM compiles and delivers documentation to multiple channels simultaneously, catering to web browsers, cloud readers, and AI search engines.

## 📚 Multi-Channel Pipeline

- **GitHub Pages (Primary Web):** Accessible at the repository's main `site_url`. Uses the MkDocs Material theme with headers and glassmorphism styling defined in `docs/stylesheets/extra.css`.
- **GitBook (Sovereign Mirror):** Kept in perfect lockstep via `.gitbook.yaml` and parsed from `SUMMARY.md`.
- **Read the Docs:** Integrated via `.readthedocs.yaml` to build a production documentation surface on Python-friendly hosts.
- **Render.com Blueprint:** Deploys a static site via `render.yaml` with the automated build command:
  ```bash
  pip install -r docs/requirements.txt && mkdocs build
  ```

## 🛠️ MkDocs Custom Hooks & Exclusions

Because MkDocs treats `docs/` as the build root, paths must be handled dynamically:
- **Exclusion Negation:** Dot-prefixed folders are ignored by default. MkDocs is instructed to negation-negate `.agents` via `exclude_docs: | \\n !.agents`.
- **Custom Link Hook (`tools/mkdocs_hooks.py`):** Rewrites raw markdown links during compilation (removing `docs/` prefixes and mapping repository-root links) to ensure seamless rendering on both GitHub.com and the static site.

## 🌐 Automated Sitemaps & Robots.txt

Sitemaps are compiled dynamically via `tools/generate_sitemaps.py` using `SitemapConfig`, outputting compliant `sitemap.xml`, `sitemap.txt`, and `robots.txt` files directly to the root and static web directories.
