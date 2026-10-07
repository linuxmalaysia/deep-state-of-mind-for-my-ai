---
name: openwiki-compiler
version: "1.0.0"
description: "Procedural SOP for executing the native Python OpenWiki Emulator to compile, update, and maintain codebase knowledge graphs within DSOM."
author: "Harisfazillah Jamel (LinuxMalaysia)"
license: "GPL-3.0-or-later"
okf_version: 0.2
type: skill
topics: ["openwiki", "skill", "compilation", "knowledge", "graph", "dsom", "python", "okf"]
status: stable
stale_after: "2027-10-01"
title: OpenWiki Knowledge Graph Compiler Skill
timestamp: "2026-08-20T23:30:00Z"
resource: "/.agents/skills/openwiki-compiler/SKILL.md"
sources: [{author: "Harisfazillah Jamel (LinuxMalaysia)", id: dsom-core-spec, resource: "/docs/governance/DSOM-TRI-PHASIC-COGNITIVE-ARCHITECTURE.md", title: "Deep State of Mind (DSOM) Governance Architecture", type: architecture_spec, url: "https://github.com/linuxmalaysia/deep-state-of-mind-for-my-ai/blob/main/docs/governance/DSOM-TRI-PHASIC-COGNITIVE-ARCHITECTURE.md"}, {author: Google Cloud Platform, id: google-okf-v02-spec, resource: "https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md", title: "Google Cloud Open Knowledge Format (OKF) v0.2 Specification", type: external_spec, url: "https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md"}]
spec_version: "0.2"
---
# OpenWiki Knowledge Graph Compiler Skill

**Purpose**: To guide AI Agents (Antigravity, Google Jules, Cursor, Claude) in maintaining and compiling OpenWiki-compliant knowledge graphs over the Sovereign Markdown Palace (`docs/`) and `.agents/brain/` using the native Python emulator (`tools/openwiki_emulator.py`).

---

## Operational Workflow for AI Agents

### 1. Execution Protocol (Zero External Binaries)

AI agents maintain `./openwiki/` using the **Native Python OpenWiki Emulator** (Rule 16 & Rule 27 Mandate):

```bash
# Execute native OpenWiki Emulator via uv
uv run --with pyyaml python tools/openwiki_emulator.py
```

---

### 2. Standard Maintenance Procedures

#### A. Initializing or Updating Knowledge Graph
Run when initializing a new DSOM project or updating an existing wiki:
```bash
uv run --with pyyaml python tools/openwiki_emulator.py
```

#### B. Incremental Deep State Update (EOD Ritual)
Execute during EOD consolidation to compile session walkthroughs into `./openwiki/`:
```bash
uv run --with pyyaml python tools/openwiki_emulator.py
```

---

### 3. AI Fallback Synthesis Protocol & OKF Compliance

When drafting or updating `./openwiki/` documentation:

1. **Skeleton Analysis:** Read `./openwiki/_skeleton.md` to inspect the planned page tree, subsystem rankings, and evidence links.
2. **Autonomous Page Drafting:** The AI agent (Gemini / Antigravity) directly drafts all planned `.md` pages under `./openwiki/` using project context and OKF YAML frontmatter.
3. **OKF Frontmatter Compliance & Signature:** Execute `uv run --with pyyaml python tools/apply_okf_frontmatter.py ./openwiki/` to validate and apply OKF v0.1 YAML frontmatter headers across all generated OpenWiki concept pages, followed by `python .agents/skills/dsom-signature-injector/scripts/inject.py ./openwiki/` to append signature footers.
4. **Regression Verification:** Run unit test assertions (`uv run --with pyyaml python -m unittest tests/test_openwiki_emulator.py tests/test_openwiki_update_workflow.py tests/test_okf_frontmatter_bom_reorder.py`).

---

## Quality Gates & Security Rules

1. **Rule 16 (`uv` Mandate & Node.js Isolation):** All Python dependencies must be run via `uv run`.
2. **Rule 24 (Credential Protection):** Never commit API keys into local files.
3. **Rule 27 (Native OpenWiki Emulator Mandate):** Maintain `./openwiki/` directly via `tools/openwiki_emulator.py`, eliminating external Node.js binaries and API rate limit dependencies.

---
*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-08-20*
*Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*
