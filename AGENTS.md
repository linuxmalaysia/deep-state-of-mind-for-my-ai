---
okf_version: 0.1
type: documentation
title: "The Agent Registry & DSOM Gateway"
description: "Sovereign entry point instructing AI Agents to look up rules and memory under .agents/."
resource: "file:///AGENTS.md"
timestamp: 2026-07-26T22:08:00Z
---
# AI Agent Registry & Sovereign Gateway

> **Entry Point:** This is the root-level gateway file for AI agents such as Google Jules, Cursor, and GitHub Copilot. The **full cognitive rulebook** and all spatial memory reside in `.agents/AGENTS.md` and `.agents/brain/`. You MUST navigate there immediately.

Welcome to the **Deep State of Mind (DSOM)** Sovereign AI Agent Workspace. If you are an AI assistant of any kind, you MUST read this document and follow its instructions to align with this repository's architecture and the DSOM protocol.

---

## Critical Instructions for AI Agents

1. **Read the Full Rulebook:** Navigate immediately to [`.agents/AGENTS.md`](.agents/AGENTS.md). This is the **Cognitive Entry Point** — the Master Rulebook containing the absolute laws, operational persona, writing styles, and all 22+ detailed rules governing this project. The file you are reading now is a summary gateway only.

2. **Access Spatial Memory:** Extend your search to all brain files located in `.agents/brain/`. Read the following files to restore full operational context:
   - `task.md` — Active and completed task list (present state).
   - `walkthrough.md` — Session history and Mental Anchors (past state).
   - `palace_registry.md` — The Sovereign Markdown Palace spatial index.
   - `active_context_manifest.md` — Live list of files currently in scope.

3. **Execute the Mechanical Boot Sequence:** Upon initialization, the AI must orient itself in this strict order:
   1. **Genesis Read:** `.agents/AGENTS.md` (Establish identity and laws).
   2. **Memory Restoration:** `.agents/brain/` (Restore active task and session state).
   3. **Master Onboarding Map:** `START-HERE.md` (Understand global topology and entry points).

4. **Execute the 5-Step Knowledge-First Discovery Flow:** Before issuing any terminal command or probing external APIs, the AI must:
   1. Search OKF frontmatter (`topics:` / `description:`) in `.agents/brain/` and `docs/`.
   2. Target specific line ranges via `view_file`.
   3. Verify the OKF `timestamp` — if stale, compare with external sources and consult the human.
   4. Obtain human consensus if the local knowledge needs updating.
   5. Only then may the AI execute physical terminal commands.

5. **Synchronise & Maintain:** Keep both `AGENTS.md` files in sync — this root gateway and `.agents/AGENTS.md`. This ensures agents like Jules and teammates always have a consistent, up-to-date view of the project's operational state.

---

## Deep State of Mind (DSOM) Core Principles

The DSOM framework operates on digital sovereignty, structured metacognition, and Git-native operational management. Key principles embedded in `.agents/AGENTS.md` include:

| Principle | Description |
|:---|:---|
| **Zero-Global / Spatial Memory** | No global state. Operational memory lives in `.agents/brain/`. |
| **Open Knowledge Format (OKF)** | All `.md` documents use OKF v0.1 YAML frontmatter (`okf_version`, `type`, `title`, `timestamp`, `topics`). |
| **Atomic Git Commits** | Every logical action results in a discrete, semantically named Git commit. No monolithic blanket commits. |
| **Omni-Documentation Sync** | New governance documents must be registered in `SUMMARY.md`, `mkdocs.yml`, `START-HERE.md`, and `llms.txt`. |
| **Sovereign Signatures** | Every markdown or readable script modified by an AI must be processed via `dsom-signature-injector`. |
| **Ansible Legacy (The Executor)** | The Third Pillar is modular: `ansible-playbook`, `uv run`, `npm run`, or `pandoc` — governed by idempotency. |
| **Command-First Architecture** | Prose instructions are converted into exact, executable, byte-capped terminal invocations. |

---

## Key Files & Directories for AI Agents

| Path | Purpose |
|:---|:---|
| `.agents/AGENTS.md` | **Full Rulebook** — Core laws, persona, and all operational rules. |
| `.agents/brain/task.md` | Active task list for the current session. |
| `.agents/brain/walkthrough.md` | Session history and Mental Anchors (resume context). |
| `.agents/brain/palace_registry.md` | Spatial index of the Sovereign Markdown Palace. |
| `.agents/skills/` | OKF-compliant executable skill SOPs (e.g., `dsom-bootstrap`, `dsom-release-manager`). |
| `docs/governance/` | Theoretical blueprints, governance policies, and architectural guides. |
| `docs/governance/AI-INITIALIZATION-SEQUENCE.md` | The 5-step Mechanical Boot Sequence. |
| `docs/governance/SOP-KNOWLEDGE-FIRST-DISCOVERY.md` | The 5-step Knowledge-First Discovery Protocol. |
| `START-HERE.md` | Master onboarding map with 12 defined entry points. |
| `llms.txt` | AI Sitemap for external crawlers (NotebookLM, ChatGPT, etc.). |

---

> **Tip:** Keep both `AGENTS.md` files up to date — the root gateway and `.agents/AGENTS.md`. This helps Google Jules, Cursor, GitHub Copilot, other AI agents, and your human teammates work with this repository more effectively and in full alignment with the DSOM protocol.

---
*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-07-26*
*Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*
