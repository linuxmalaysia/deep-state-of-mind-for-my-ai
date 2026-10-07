---
name: sitemap-seo-generator
version: "1.0.0"
description: "Configures and manages sitemap and robots.txt generation to optimize SEO indexation for GitHub Pages, Read the Docs, and GitBook."
topics: ["sitemap", "seo", "automation", "gitbook", "readthedocs"]
author: "Harisfazillah Jamel (LinuxMalaysia)"
license: "GPL-3.0-or-later"
okf_version: 0.2
type: agent_skill
status: stable
stale_after: "2027-10-01"
title: "🗺️ Sitemap & SEO Asset Generator Skill"
timestamp: "2026-08-12T12:00:00Z"
resource: "/.agents/skills/sitemap-seo-generator/SKILL.md"
sources: [{author: "Harisfazillah Jamel (LinuxMalaysia)", id: dsom-core-spec, resource: "/docs/governance/DSOM-TRI-PHASIC-COGNITIVE-ARCHITECTURE.md", title: "Deep State of Mind (DSOM) Governance Architecture", type: architecture_spec, url: "https://github.com/linuxmalaysia/deep-state-of-mind-for-my-ai/blob/main/docs/governance/DSOM-TRI-PHASIC-COGNITIVE-ARCHITECTURE.md"}, {author: Google Cloud Platform, id: google-okf-v02-spec, resource: "https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md", title: "Google Cloud Open Knowledge Format (OKF) v0.2 Specification", type: external_spec, url: "https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md"}]
spec_version: "0.2"
---
# 🗺️ Sitemap & SEO Asset Generator Skill

**Purpose**: To guide AI Agents (Antigravity, Google Jules, Cursor, Claude) in executing the automated sitemap and SEO asset generation workflow using the Python utility (`tools/generate_sitemaps.py`).

---

## When to use this skill

- When creating or modifying markdown files and needing to ensure sitemaps and search indexes are updated.
- When validating the integrity of `SUMMARY.md` navigation links for GitBook compatibility.
- When diagnosing robots.txt, sitemap.xml, or sitemap.txt indexing pathways.

---

## How to use it

### 1. Execute Sitemap & SEO Generation

AI agents execute sitemap generation natively via `uv run` (Rule 16 Mandate):

```bash
uv run python tools/generate_sitemaps.py
```

### 2. Validation and Output Locations

The script performs the following actions:
- Builds the MkDocs site (`site/` folder) to compile the base sitemap.
- Parses `site/sitemap.xml` for all GitHub Pages URLs.
- Derives all corresponding Read the Docs URLs.
- Processes `SUMMARY.md` to map and validate all GitBook URLs.
- Ensures all referenced markdown files exist in the repository to prevent broken links.
- Writes three files (`sitemap.txt`, `sitemap.xml`, and `robots.txt`) to the root, `docs/`, and `site/` directories.

---

## Quality Gates & Compliance

1. **Rule 16 (`uv` Mandate):** Never execute with raw python or pip; always use `uv run`.
2. **Rule 25 (BOM-less & Quoting):** Ensure all sitemaps are generated with valid absolute URIs.

---
*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-08-12*
*Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*
