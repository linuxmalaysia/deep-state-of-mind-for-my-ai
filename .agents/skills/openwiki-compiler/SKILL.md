---
okf_version: 0.1
type: skill
title: "OpenWiki Knowledge Graph Compiler Skill"
timestamp: "2026-08-09T02:00:00Z"
description: "Procedural SOP for executing OpenWiki CLI commands to compile, visualize, and synchronize codebase knowledge graphs within DSOM."
topics: ["openwiki", "skill", "compilation", "knowledge", "graph", "dsom"]
name: openwiki-compiler
---
# OpenWiki Knowledge Graph Compiler Skill

**Purpose**: To guide AI Agents (Antigravity, Google Jules, Cursor, Claude) in executing OpenWiki CLI operations to generate, update, and visualize knowledge graphs over the Sovereign Markdown Palace (`docs/`) and `.agents/brain/`.

---

## Operational Workflow for AI Agents

### 1. Environment Verification Gate
Before running OpenWiki commands, verify Node.js version (Node >= 20.0.0 required):

```bash
# On Linux / WSL2
node -v && openwiki --help

# On Windows PowerShell
pwsh -Command "npm -v; npx --yes openwiki --help"
```

---

### 2. Standard Command Procedures

#### A. Initializing Repository Knowledge Graph
Run when initializing a new DSOM project repository:
```bash
openwiki code --init
```

#### B. Incremental Deep State Update (EOD Ritual)
Execute during EOD consolidation to compile session walkthroughs into `./openwiki/`:
```bash
openwiki --update -p "Consolidate today's walkthrough anchors into the knowledge graph"
```

#### C. Non-Interactive Intelligence Retrieval
Query the OpenWiki knowledge graph without opening an interactive TTY session:
```bash
openwiki -p "Summarize active governance blueprints under docs/governance/"
```

#### D. Visualizing Knowledge Graph (Web Reader)
Launch local web reader on port 4321 for human architect review:
```bash
openwiki visualize openwiki --port 4321 --no-open
```

---

## Quality Gates & Security Rules

1. **Rule 16 (`uv` Mandate & Node.js Isolation):** On Python environments, use `uv` for python dependencies and standard `npm` / `npx` for OpenWiki Node dependencies.
2. **Rule 24 (Credential Protection):** Never commit connector API keys (OpenAI, Anthropic, LangChain) into local files. Store secrets in GitHub Secrets (`gh secret set`).
3. **Cross-Platform Compatibility:** On Windows native PowerShell, do NOT run with `bun`. Run via `npm install -g openwiki` or WSL2 Node v22 environment.

---
*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-08-09*
*Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*
