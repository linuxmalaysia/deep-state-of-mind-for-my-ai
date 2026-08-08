---
okf_version: 0.1
type: operational_guide
title: "🛠️ HOWTO: Operating OpenWiki CLI & Knowledge Compiler"
timestamp: "2026-08-09T02:00:00Z"
topics: ["openwiki", "cli", "howto", "dsom", "installation", "wsl2"]
description: "Step-by-step guide for installing, running, and managing OpenWiki CLI v0.3.1 within DSOM Linux, WSL2, and Windows environments."
resource: "file:///docs/tools/HOWTO-OPENWIKI.md"
---
# 🛠️ HOWTO: Operating OpenWiki CLI & Knowledge Compiler

This operational guide provides step-by-step instructions for installing, configuring, and running **OpenWiki v0.3.1** within the Deep State of Mind (DSOM) infrastructure across Linux Control Nodes, WSL2 AlmaLinux 10, and Windows 11 environments.

---

## 📥 1. Installation Protocols

### Linux / WSL2 AlmaLinux 10 (Recommended):

```bash
# Verify Node.js version (Node >= 20.0.0 required)
node -v
npm -v

# Global installation via npm (with sudo if root node)
sudo npm install -g openwiki

# Verify installation
openwiki --help
```

### Windows 11 PowerShell (Native):

> [!WARNING]
> On Windows native PowerShell, install strictly via `npm install -g openwiki`. Do NOT install using `bun`, which requires Visual Studio C++ Build Tools (`better-sqlite3`).

```powershell
# Run openwiki via npx or global npm install
npm install -g openwiki

# Or run on-demand via npx
npx --yes openwiki --help
```

---

## ⚡ 2. Core CLI Commands & Ingestion

| Operational Intent | CLI Invocations | Expected Result / Output |
| :--- | :--- | :--- |
| **Initialize Repo Wiki** | `openwiki --init` | Generates initial wiki structure under `./openwiki/` |
| **Update Existing Wiki** | `openwiki --update` | Incremental update over changed codebase files |
| **Personal Knowledge Brain**| `openwiki personal --init` | Initializes local brain under `~/.openwiki/wiki` |
| **Non-Interactive Print** | `openwiki -p "Summarize project"` | Runs once and outputs response to stdout |
| **Serve Interactive Graph** | `openwiki visualize` | Launches local web graph server on `http://localhost:4321` |
| **Connector Ingestion** | `openwiki ingest all` | Ingests from configured connectors (Notion, Slack, Gmail) |

---

## 🏛️ 3. Integration with DSOM Rituals

### Start-of-Day (SOD) & End-of-Day (EOD) Automation:
During the EOD hibernation phase (`tools/hibernation.ps1` / `playbooks/dsom/eod-palace.yml`), OpenWiki compiles new commit diffs into the Sovereign Palace:

```bash
# Execute non-interactive update run during Deep State consolidation
openwiki --update -p "Consolidate daily walkthrough anchors into openwiki/"
```

### FastMCP & Context7 Linkage:
OpenWiki generated documentation under `./openwiki/` is automatically scanned by our FastMCP server (`tools/mcp/server.py`) and indexed into Context7 RAG endpoints (`https://context7.com/gitlab_linuxmalaysia/...`).

---

## 🔗 4. References

* **OpenWiki Integration Blueprint:** [`docs/governance/OPENWIKI-INTEGRATION-GUIDE.md`](file:///d:/Users/LinuxMalaysia/Projects/deep-state-of-mind-for-my-ai/docs/governance/OPENWIKI-INTEGRATION-GUIDE.md)
* **OpenWiki Agent Skill:** [`SKILL.md`](file:///d:/Users/LinuxMalaysia/Projects/deep-state-of-mind-for-my-ai/.agents/skills/openwiki-compiler/SKILL.md)
* **DSOM Tri-Phasic Mind Architecture:** [`docs/governance/DSOM-TRI-PHASIC-COGNITIVE-ARCHITECTURE.md`](file:///d:/Users/LinuxMalaysia/Projects/deep-state-of-mind-for-my-ai/docs/governance/DSOM-TRI-PHASIC-COGNITIVE-ARCHITECTURE.md)

---
*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-08-09*
*Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*
