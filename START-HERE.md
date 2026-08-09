---
okf_version: 0.1
type: documentation
title: "START HERE: DSOM Project Benefits & Entry Points"
timestamp: "2026-08-09T11:22:00Z"
topics: ["onboarding", "entry-points", "dsom", "sovereign", "baseline", "benefits", "openwiki"]
description: "The primary onboarding document for human operators and AI agents adopting the DSOM framework into new or existing projects."
resource: "file:///START-HERE.md"
---
# START HERE: DSOM Project Benefits & Entry Points

Welcome to the **Deep State of Mind (DSOM) For My AI** framework. If you are adopting this repository to bootstrap a new infrastructure/software project, or onboarding a new human team member or AI agent, you must understand how to enter the system.

DSOM is a modular Sovereign AI Engine. To use it effectively, do not read every file at random. Start with the defined Entry Points depending on your role.

---

## 🌟 Why Adopt DSOM in Your Project? (Core Architectural Benefits)

Adopting the DSOM protocol into any new or existing project delivers four transformative capabilities:

| Core Capability / Benefit | How DSOM Achieves It | Empirical Impact / Value |
| :--- | :--- | :--- |
| **1. 98%+ Token & Cost Reduction** | **OKF YAML Frontmatter** + **Native OpenWiki (`./openwiki/`)** pre-distill codebase structures into lightweight metadata and 10 concept nodes. | AI agents search metadata in ~50 tokens instead of loading 500,000+ raw code tokens into context windows. |
| **2. Zero Memory Loss Across Sessions** | **Spatial Memory (`.agents/brain/`)** records session walkthrough anchors (`task.md`, `walkthrough.md`, `palace_registry.md`). | AI digital twins (Gemini, Jules, Claude) reanimate instantly with exact past mental state across chat reboots. |
| **3. Zero-Binary & Zero-Cost Portability** | Native Python scripts (**`uv run python tools/openwiki_emulator.py`**) replace heavy Node.js binaries and third-party APIs. | Bypasses `NODE_MODULE_VERSION` native compilation crashes, UAC elevation hangs, 135 MB bloat, and LLM API rate limits. |
| **4. Multi-Agent Cognitive Alignment** | **27 Constitutional AI Laws (`AGENTS.md`)** + **FastMCP Knowledge Server (`tools/mcp/server.py`)**. | Google Jules, Antigravity, Cursor, and Claude Desktop share identical rules, security guardrails, and test contracts. |

---

## 1. The Engineering Entry Point (Project Scaffolding)
*If you are setting up a brand new DSOM project repository for the first time.*

**Read This First:** [`docs/HOWTO-CLONE-DSOM-PROJECT.md`](docs/HOWTO-CLONE-DSOM-PROJECT.md)

**Why it matters:** This is the master blueprint. It explicitly instructs the human or the AI on how to execute the `dsom-project-cloner` and `dsom-bootstrap` skills. It establishes the initial Git Worktree isolation and ensures the spatial memory (`.agents/brain/`) is properly initialized before any real work begins.

---

## 2. The Cognitive Entry Point (AI Persona & Rules)
*If you are an AI agent, or a human programming an AI agent, and need to know the operational rules of this environment.*

**Read This First (Root Gateway):** [`AGENTS.md`](AGENTS.md)

**Then Read the Full Rulebook:** [`.agents/AGENTS.md`](.agents/AGENTS.md)

**Why it matters:** The root `AGENTS.md` is the **Gateway File** for AI agents such as Google Jules, Cursor, and Copilot that scan the repository root. It summarises the DSOM protocol and immediately redirects agents to [`.agents/AGENTS.md`](.agents/AGENTS.md) — the **Sovereign Constitution** containing all 27 operational laws, the LinuxMalaysia persona, the Defensive GitOps rules, the OKF mandate, and the UK English writing standard. Keep both files synchronised at all times.

---

## 3. The External System Entry Point (AI Crawlers)
*If you are using an external tool (e.g., Google NotebookLM, ChatGPT) to ingest this repository.*

**Read This First:** [`llms.txt`](llms.txt)

**Why it matters:** Placed at the root of the repository, this file acts as the official AI Sitemap. It explicitly links to all the critical governance documents (including the `NOSS-INTEGRATION-GUIDE.md`) so that external systems immediately understand the architectural constraints and compliance payloads of the project without getting lost in code files.

---

## 4. The Daily Operations Entry Point (Day 2 Management)
*If the project is already running, and you are starting your work day or recovering from a server reboot.*

**Read This First:** [`docs/HOWTO-PALACE-ONBOARDING.md`](docs/HOWTO-PALACE-ONBOARDING.md)

**Why it matters:** This teaches the human and the AI how to read the `palace_registry.md` ledger during the Start of Day (SOD) ritual. It ensures the AI never suffers from memory loss between sessions by strictly governing thread states through spatial memory.

---

## 5. The Legacy Upgrade Entry Point (Existing DSOM Projects)
*If you are operating a legacy DSOM project and need to modernize it to the current master architectural baseline.*

**Read This First:** [`docs/HOWTO-UPGRADE-LEGACY-DSOM.md`](docs/HOWTO-UPGRADE-LEGACY-DSOM.md)

**Why it matters:** It explains how to systematically inject modern protocols (OKF frontmatter, LLM WIKI, dsom-signature-injector, uv Python environments) into your older repositories to achieve compliance with the current master baseline.

---

## 6. The Subagent Swarm Entry Point (Multi-Agent Orchestration)

### Entry Point 3: The Native MCP Server Integration
DSOM acts as its own Model Context Protocol (MCP) server (`tools/mcp/server.py`), allowing AI editors (Claude Desktop, Cursor, VSCode) to read the Sovereign Markdown Palace and OpenWiki knowledge graph locally without pasting context.

To configure your AI client, point it to our `uv`-managed server script:
```json
{
  "mcpServers": {
    "dsom-palace": {
      "command": "uv",
      "args": ["run", "tools/mcp/server.py"]
    }
  }
}
```

### Entry Point 4: Subagent Orchestration Workflow
*If you are scaling complex engineering tasks using autonomous AI subagents.*

**Read This First:** [`docs/governance/MULTI-AGENT-PROTOCOLS.md`](docs/governance/MULTI-AGENT-PROTOCOLS.md)

**Why it matters:** Instructs the project on how to deploy concurrent subagents safely. It enforces **Git Worktree Isolation** to prevent Silent Subagent Merge Conflicts when multiple agents edit the same repository simultaneously.

---

## 7. The Procedural Skill Entry Point (AI Automation)
*If you need to teach your AI how to perform repetitive operational workflows.*

**Read This First:** [`docs/governance/AI-SKILL-ARCHITECTURE.md`](docs/governance/AI-SKILL-ARCHITECTURE.md) and [`docs/governance/AI-SLASH-COMMANDS-GUIDE.md`](docs/governance/AI-SLASH-COMMANDS-GUIDE.md)

**Why it matters:** Explains how to structure the `.agents/skills/` directory. It ensures that all operational manuals (SOPs) are OKF-compliant and executable by the AI via semantic routing, eliminating the need to write custom Python bots.

---

## 8. The Sovereign Knowledge Entry Point (LLM WIKI Adoption)
*If you are migrating legacy documentation into an AI-native memory palace.*

**Read This First:** [`docs/governance/LLM-WIKI-ADOPTION.md`](docs/governance/LLM-WIKI-ADOPTION.md)

**Why it matters:** Dictates how to transform a standard `docs/` folder into an LLM WIKI. Explains the necessity of the OKF YAML Frontmatter and the **Artifact Pyramid (Progressive Disclosure)** to prevent context window bloat during long conversational sessions.

---

## 9. The Security & Defense Entry Point (Defensive GitOps)
*If you are adopting DSOM for secure infrastructure or production environments.*

**Read This First:** [`docs/governance/GITOPS-AIOPS-ANSIBLE-STRATEGY.md`](docs/governance/GITOPS-AIOPS-ANSIBLE-STRATEGY.md)

**Why it matters:** Enforces the "Zero-Global Memory" rule and dictates how to use `git-filter-repo` (Privacy Guardian) to sanitize histories of IPs, secrets, and proprietary node names before syncing to public or shared remotes.

---

## 10. The Token Performance Entry Point (Context Efficiency)
*If you are onboarding a new AI agent or bootstrapping a new project and want to ensure token-efficient LLM operation from day one.*

**Read This First:** [`docs/governance/DSOM-TOKEN-PERFORMANCE-PLAYBOOK.md`](docs/governance/DSOM-TOKEN-PERFORMANCE-PLAYBOOK.md)

**Why it matters:** This is the master playbook for context window efficiency. It proves a **96.23% reduction in token consumption** versus monolithic document loading, and provides the exact procedures — benchmark commands, OKF frontmatter standards, active context manifest setup, and skill quality gates — that every new DSOM project must inherit to remain sustainable at scale.

---

## 11. The Discovery Entry Point (Knowledge-First Protocol)
*If you are an AI agent or human operator attempting to execute an exploratory terminal command or probe external nodes.*

**Read This First:** [`docs/governance/SOP-KNOWLEDGE-FIRST-DISCOVERY.md`](docs/governance/SOP-KNOWLEDGE-FIRST-DISCOVERY.md)

**Why it matters:** This protocol powers the "real engine" of DSOM's cognitive awareness. It mandates that every AI agent must execute a strict **5-step Local Knowledge-First Discovery Flow** (Search OKF -> Target Read -> Verify Timestamp -> Consult Human -> Execute).

---

## 12. The Initialization Entry Point (Mechanical Boot Sequence)
*If you need to understand how the AI's cognitive engine boots up, reanimates, and establishes its laws before the first prompt is processed.*

**Read This First:** [`docs/governance/AI-INITIALIZATION-SEQUENCE.md`](docs/governance/AI-INITIALIZATION-SEQUENCE.md)

**Why it matters:** It defines the exact **5-step Mechanical Boot Sequence** that forces the AI to natively ingest its persona, core rules (including the discovery loops), spatial memory, and onboarding map in a strict order.

---

## 13. The Automated State Sync Entry Point (Semantic Compaction)
*If you need to understand how DSOM manages token bloat automatically across Pull Requests.*

**Read This First:** [`docs/governance/DSOM-AUTOMATED-STATE-SYNC.md`](docs/governance/DSOM-AUTOMATED-STATE-SYNC.md)

---

## 14. The Cognitive Architecture Entry Point (The Tri-Phasic Mind)
*If you need to understand how the AI's cognitive pipeline is split into Active, Twilight, and Deep states.*

**Read This First:** [`docs/governance/DSOM-TRI-PHASIC-COGNITIVE-ARCHITECTURE.md`](docs/governance/DSOM-TRI-PHASIC-COGNITIVE-ARCHITECTURE.md)

---

## 15. The Native OpenWiki Knowledge Graph Entry Point (Zero-Binary Architecture)
*If you want to maintain a high-density, zero-binary knowledge graph across your repository.*

**Read This First:** [`docs/tools/HOWTO-OPENWIKI.md`](docs/tools/HOWTO-OPENWIKI.md) and [`docs/governance/OPENWIKI-INTEGRATION-GUIDE.md`](docs/governance/OPENWIKI-INTEGRATION-GUIDE.md)

**Why it matters:** Details how to maintain `./openwiki/` using the native Python script (`uv run python tools/openwiki_emulator.py`) with `--init`, `--update`, `--search`, and `--export-graph` CLI modes. Includes complete code samples and reusable AI prompt templates so any project can adopt OpenWiki emulation natively.

---
*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-08-09*
*Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*
