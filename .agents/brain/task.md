---
okf_version: 0.2
type: task_ledger
title: "🗺️ DSOM Task List"
timestamp: "2026-10-11T06:00:00Z"
topics: ["qmd", "search", "mcp", "testing", "ci", "okf-v02"]
resource: "/.agents/brain/task.md"
sources: [{author: "Harisfazillah Jamel (LinuxMalaysia)", id: dsom-core-spec, resource: "/docs/governance/DSOM-TRI-PHASIC-COGNITIVE-ARCHITECTURE.md", title: "Deep State of Mind (DSOM) Governance Architecture", type: "architecture_spec"}]
spec_version: "0.2"
---
- `[x]` Adopt `qmd-search` skill (`.agents/skills/qmd-search/SKILL.md`) following dual Lola + OKF v0.2 frontmatter specifications.
- `[x]` Author English Diátaxis How-To Guide (`docs/how-to/install-and-use-qmd-search.md`) detailing installation, multi-project collection scoping, incremental indexing, hourly cron background sync, and MCP integration.
- `[x]` Author Bahasa Melayu Diátaxis How-To Guide (`docs/how-to/panduan-pemasangan-dan-penggunaan-qmd.md`) detailing installation, multi-project collection scoping, incremental indexing, hourly cron background sync, and MCP integration.
- `[x]` Register `qmd-search` skill and Diátaxis guides across all navigation registries and manifests: `.lola-req`, `AGENTS.md`, `.agents/AGENTS.md`, `START-HERE.md`, `SUMMARY.md`, `llms.txt`, `mkdocs.yml`, and `docs/how-to/index.md`.
- `[x]` Increment skill count from 46 to 47 agent skills in `AGENTS.md` and `.agents/AGENTS.md`.
- `[x]` Address all CodeRabbit PR review comments: parameterise MCP path examples, enforce Node.js v22+ prerequisite, ensure log directory creation in cron sync script, and fix line slice parameters.
- `[x]` Re-compile sitemaps (`sitemap.xml`, `sitemap.txt`, `robots.txt`) across root, `docs/`, and `site/` directories using `tools/generate_sitemaps.py`.
- `[x]` Validate 100% OKF v0.2 frontmatter compliance using `tools/validate-okf.sh` and `tools/apply_okf_frontmatter.py --require-okf-v02`.
- `[x]` Verify relative link integrity across all Diátaxis documentation using `tools/check_docs_links.py`.
- `[x]` Execute test suite and verify zero test regressions locally (`uv run python -m unittest discover tests`).
- `[x]` Complete spatial brain memory updates (`task.md`, `walkthrough.md`, `palace_registry.md`, `jules_pr_history.md`) and triple-ledger updates (`README.md`, `CHANGELOG.md`, `HISTORY.md`).

---
*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-10-11*
