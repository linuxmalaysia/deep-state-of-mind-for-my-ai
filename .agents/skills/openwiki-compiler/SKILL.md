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

# On Windows PowerShell (Non-Interactive Node v22.14.0 LTS Wrapper)
pwsh -File tools/run-openwiki.ps1 --help
```

---

### 2. Standard Command Procedures

#### A. Initializing Repository Knowledge Graph
Run when initializing a new DSOM project repository:
```bash
# Linux/WSL2
openwiki code --init

# Windows PowerShell
pwsh -File tools/run-openwiki.ps1 code --init
```

#### B. Incremental Deep State Update (EOD Ritual)
Execute during EOD consolidation to compile session walkthroughs into `./openwiki/`:
```bash
# Linux/WSL2
openwiki --update -p "Consolidate today's walkthrough anchors into the knowledge graph"

# Windows PowerShell
pwsh -File tools/run-openwiki.ps1 --update -p "Consolidate today's walkthrough anchors"
```

#### C. Non-Interactive Intelligence Retrieval
Query the OpenWiki knowledge graph without opening an interactive TTY session:
```bash
# Linux/WSL2
openwiki -p "Summarize active governance blueprints under docs/governance/"

# Windows PowerShell
pwsh -File tools/run-openwiki.ps1 -p "Summarize active governance blueprints under docs/governance/"
```

#### D. Visualizing Knowledge Graph (Web Reader)
Launch local web reader on port 4321 for human architect review:
```bash
# Linux/WSL2
openwiki visualize openwiki --port 4321 --no-open

# Windows PowerShell
pwsh -File tools/run-openwiki.ps1 visualize openwiki --port 4321 --no-open
```

---

## Quality Gates & Security Rules

1. **Rule 16 (`uv` Mandate & Node.js Isolation):** On Python environments, use `uv` for python dependencies and standard `npm` / `npx` or `tools/run-openwiki.ps1` for Node dependencies.
2. **Rule 24 (Credential Protection):** Never commit connector API keys (OpenAI, Anthropic, LangChain) into local files. Store secrets in GitHub Secrets (`gh secret set`).
3. **Rule 27 (Windows Non-Interactive Execution Mandate):** On Windows native PowerShell, do NOT invoke `nvm use` or run with `bun`. Run strictly via `pwsh -File tools/run-openwiki.ps1` or WSL2 Node v22 environment to prevent UAC background hangs.

---
*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-08-09*
*Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*
