---
okf_version: 0.1
type: agent_skill
title: "📥 DSOM Knowledge Ingester Skill"
timestamp: "2026-08-20T23:30:00Z"
description: "Executes the Ingest protocol inspired by the LLM WIKI concept to process external raw documents and synthesise them into the Sovereign Markdown Palace."
topics: ["knowledge", "ingestion", "okf", "palace", "markdown"]
name: dsom-knowledge-ingester
---
# 📥 DSOM Knowledge Ingester Skill

## When to use this skill
Use this skill when the user provides a new external source (PDF, Markdown, Web Article, Meeting Transcript) and wants to formalize it into the Palace. This embodies the "Ingest" pattern of the LLM WIKI.

## Instructions
1. **Source Discovery:** Ask the user for the path to the raw source document in `raw_sources/` (create this directory if it doesn't exist).
2. **Analysis & Synthesis:**
   - Read the raw document using `view_file`, `pdf-text-extractor`, or `read_url_content`.
   - Synthesize the key concepts, rules, and architectural data.
3. **Wiki Integration (The Palace):**
   - Create a new `.md` file in the appropriate directory (e.g., `docs/governance/`, `hall_facts/`).
   - Format the file according to DSOM Generative Engine Optimisation (GEO) standards (atomic chunks, H2 headers, expert tone).
   - Execute `uv run python tools/apply_okf_frontmatter.py <directory>` to verify and inject OKF v0.1 frontmatter headers into all newly synthesized Markdown documents.
   - Inject the Sovereign Signature using `dsom-signature-injector`.
4. **Ledger & Index Updates:**
   - Add the new file to `SUMMARY.md` and `mkdocs.yml` (Dual Documentation Sync).
   - Add the new file to `.agents/brain/palace_registry.md`.
   - Update `CHANGELOG.md` and `HISTORY.md` to note the new knowledge ingestion.
5. **Confirmation:** Provide the user with a summary of the concepts extracted and the new pages created.

---
*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-08-20*
*Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*
