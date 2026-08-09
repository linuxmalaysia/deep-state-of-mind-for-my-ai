---
okf_version: 0.1
type: governance_protocol
title: "🌐 OpenWiki Integration & Deployment Blueprint (Linux, Windows & Google Jules)"
timestamp: "2026-08-09T01:54:00Z"
topics: ["openwiki", "dsom", "governance", "installation", "jules", "windows"]
description: "Production guide and feasibility evaluation for adopting LangChain's OpenWiki within DSOM Linux, Windows PowerShell, and Google Jules environments."
resource: "file:///docs/governance/OPENWIKI-INTEGRATION-GUIDE.md"
---
# 🌐 OpenWiki Integration & Deployment Blueprint

## 🏛️ 1. Architectural Overview & Feasibility

Evaluating the adoption of **LangChain's OpenWiki** ([`github.com/langchain-ai/openwiki`](https://github.com/langchain-ai/openwiki)) within the Deep State of Mind (DSOM) ecosystem demonstrates an ideal architectural fit. OpenWiki provides an open-source, structured wiki knowledge graph engine that converts raw markdown archives into navigable, machine-readable concepts.

By adopting OpenWiki into the DSOM framework, the Cognitive Twin enhances its **Semantic Memory (Sovereign Markdown Palace)** and reinforces **Rule 15** (*Knowledge Compounding / LLM WIKI Mandate*). OpenWiki acts as an offline reflection compiler during the **Deep State (Dream Mind)** cycle, compiling chat walkthrough logs into permanent, hyperlinked markdown knowledge nodes.

---

## 💻 2. Multi-Platform Deployment Matrix

| Target Platform | Runtime Environment | Recommended Package Manager | Native Compiler Constraints |
| :--- | :--- | :--- | :--- |
| **Linux Control Node** | AlmaLinux 10 / Ubuntu 24.04 | `npm` / `pnpm` / `uv` / `npx` | Standard gcc/g++ build essentials |
| **Google Jules AI Agent** | Ubuntu 24.04 LTS Container | `npm install -g openwiki` | Pre-built Node.js 20+ runtime |
| **Windows 11 (Antigravity)** | Native PowerShell 7 | `npm install -g openwiki` | Avoid `bun` fallback (`better-sqlite3`) |

---

## 🐧 3. Deployment Guide: Linux & Google Jules (Ubuntu 24.04)

Google Jules operates in an isolated **Ubuntu 24.04 LTS** containerized execution bridge. OpenWiki deploys seamlessly into this environment using standard Node.js toolchains.

### Installation Steps (Linux / Google Jules):

```bash
# Verify Node.js version (v18.0.0+ required)
node --version
npm --version

# Global installation via npm
npm install -g openwiki

# Alternatively run on-demand via npx
npx openwiki --help
```

### Integration with Ansible & Control Nodes:
Within the DSOM Ansible Control Node (`setup-dsom-control-node.sh`), OpenWiki is invoked during EOD consolidation playbooks (`playbooks/dsom/eod-palace.yml`):

```bash
# Run OpenWiki compilation over docs/ and .agents/brain/
openwiki build --input ./docs --output .agents/brain/wings/wing_dsom_core/
```

---

## 🪟 4. Deployment Guide: Windows 11 & Antigravity (PowerShell Native)

Running OpenWiki within Windows PowerShell environments (e.g. Google Antigravity IDE on Windows 11) requires strict package manager discipline to prevent native C++ compilation errors.

### ⚠️ Critical Windows Installation Warning:
> [!WARNING]
> On Windows native checkouts, install OpenWiki exclusively using **`npm`** (`npm install -g openwiki`) or **`pnpm`** (`pnpm add -g openwiki`). 
> 
> **DO NOT install using `bun` on native Windows.** Installing with `bun` attempts to recompile the `better-sqlite3` native C++ dependency from source code. If Visual Studio Build Tools with the *"Desktop development with C++"* workload is not installed, the `bun` installation will fail with missing C++ header compilation errors (`MSB3073` / `node-gyp`). `npm` and `pnpm` automatically download pre-compiled native `.node` binaries for Windows x64.

### Execution Commands (Windows PowerShell):

```powershell
# Verify Node.js installation
node -v
npm -v

# Recommended: Global installation via npm (Pre-compiled binary support)
npm install -g openwiki

# Alternative: Installation via pnpm
pnpm add -g openwiki

# Verify CLI execution in PowerShell
openwiki --version
```

---

## 🔄 5. Integration with DSOM Tri-Phasic Mind & MCP

OpenWiki integrates directly into the DSOM Tri-Phasic Mind architecture:

1. **Active State (T1):** The FastMCP server ([`tools/mcp/server.py`](file:///d:/Users/LinuxMalaysia/Projects/deep-state-of-mind-for-my-ai/tools/mcp/server.py)) queries OpenWiki's generated index to serve semantic answers to IDE assistants.
2. **Twilight State (T2):** Pre-flight audits ([`tools/audit-pre-flight.ps1`](file:///d:/Users/LinuxMalaysia/Projects/deep-state-of-mind-for-my-ai/tools/audit-pre-flight.ps1)) check OpenWiki frontmatter formatting and broken internal wiki links.
3. **Deep State (T3):** EOD hibernation scripts ([`tools/hibernation.ps1`](file:///d:/Users/LinuxMalaysia/Projects/deep-state-of-mind-for-my-ai/tools/hibernation.ps1)) trigger `openwiki` to refresh the Sovereign Markdown Palace before syncing to Context7 (`context7-indexer`) and multi-remote Git repositories.

---

## 🛠️ 6. Troubleshooting: Visualization Shows 0 Pages

> [!IMPORTANT]
> If `openwiki visualize` launches at `http://localhost:4321` showing **0 pages**, the repository wiki has not been initialized yet.
> * **Action Required:** Execute `pwsh -File tools/run-openwiki.ps1 code --init` (or `openwiki code --init` on Linux/WSL).
> * **Result:** OpenWiki will scan the codebase, build the `./openwiki/` directory, and populate the visual graph nodes.

---

## 🔗 7. References

* **LangChain OpenWiki Repository:** [`github.com/langchain-ai/openwiki`](https://github.com/langchain-ai/openwiki)
* **DSOM Tri-Phasic Architecture:** [`docs/governance/DSOM-TRI-PHASIC-COGNITIVE-ARCHITECTURE.md`](file:///d:/Users/LinuxMalaysia/Projects/deep-state-of-mind-for-my-ai/docs/governance/DSOM-TRI-PHASIC-COGNITIVE-ARCHITECTURE.md)
* **Context7 Indexer Skill:** [`SKILL.md`](file:///d:/Users/LinuxMalaysia/Projects/deep-state-of-mind-for-my-ai/.agents/skills/context7-indexer/SKILL.md)

---
*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-08-09*
*Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*
