---
okf_version: 0.1
type: documentation
title: "START HERE: DSOM Project Entry Points"
description: "The primary onboarding document for human operators and AI agents adopting the DSOM framework into new projects."
resource: "file:///START-HERE.md"
timestamp: 2026-07-12T09:10:00Z
---
# START HERE: DSOM Project Entry Points

Welcome to the **Deep State of Mind (DSOM) For My AI** framework. If you are adopting this repository to bootstrap a new infrastructure project, or onboarding a new human team member or AI agent, you must understand how to enter the system.

DSOM is a modular Sovereign Engine. To use it effectively, do not read every file at random. Start with the following nine (9) defined Entry Points depending on your role.

---

## 1. The Engineering Entry Point (Project Scaffolding)
*If you are setting up a brand new DSOM project repository for the first time.*

**Read This First:** [`docs/HOWTO-CLONE-DSOM-PROJECT.md`](docs/HOWTO-CLONE-DSOM-PROJECT.md)

**Why it matters:** This is the master blueprint. It explicitly instructs the human or the AI on how to execute the `dsom-project-cloner` and `dsom-bootstrap` skills. It establishes the initial Git Worktree isolation and ensures the spatial memory (`.agents/brain/`) is properly initialized before any real work begins.

---

## 2. The Cognitive Entry Point (AI Persona & Rules)
*If you are an AI agent, or a human programming an AI agent, and need to know the operational rules of this environment.*

**Read This First:** [`.agents/AGENTS.md`](.agents/AGENTS.md)

**Why it matters:** This is the Sovereign Constitution. It injects the Senior ICT Consultant persona (LinuxMalaysia), enforces the Defensive GitOps rules, mandates the OKF structure, and dictates the strict standard UK English / Bahasa Melayu writing style. Any new project inherits this cognitive baseline automatically.

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

**What you need to add to your existing project:**
If your project is running an older iteration of DSOM, you must systematically inject the following modern protocols to achieve compliance with the current master baseline:

1. **Adopt `llms.txt`:** Create an `llms.txt` file at the root of your project to map your critical governance documents for external AI crawlers.
2. **Inject OKF YAML Frontmatter:** All existing `.md` files in your `brain/` and `docs/` directories must be retroactively updated to include OKF v0.1 YAML frontmatter (metadata routing).
3. **Mandate the Sovereign Signature:** Pull the `dsom-signature-injector` skill from the master baseline and execute it across your legacy repository to ensure all scripts (`.sh`, `.ps1`) and playbooks (`.yml`) carry standard developer metadata headers and GPL v3.0 licenses.
4. **Transition to `uv`:** Audit your existing Python automation scripts. Adopt the `PYTHON-UV-ENVIRONMENT-GUIDE.md` and migrate away from global `pip` installations to isolated `uv` environments to prevent dependency conflicts.
5. **Establish the Audit Ledger:** Generate an `AUTOMATION-AUDIT-LIST.md` in your `docs/governance/` directory to catalog all legacy `.sh` and `.ps1` scripts for centralized human security auditing.

---

## 6. The Subagent Swarm Entry Point (Multi-Agent Orchestration)
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
*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-07-12*
*Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*
