---
okf_version: 0.1
type: documentation
title: "The Agent Registry & DSOM Gateway"
timestamp: "2026-08-08T12:00:00Z"
topics: ["dsom", "documentation"]
description: "Sovereign entry point instructing AI Agents to look up rules and memory under .agents/."
resource: "file:///AGENTS.md"
---
# AI Agent Registry & Sovereign Gateway

> **Entry Point:** This is the root-level gateway file for AI agents such as Google Jules, Cursor, and GitHub Copilot. The **full cognitive rulebook** and all spatial memory reside in `.agents/AGENTS.md` and `.agents/brain/`. You MUST navigate there immediately.

Welcome to the **Deep State of Mind (DSOM)** Sovereign AI Agent Workspace. If you are an AI assistant of any kind, you MUST read this document and follow its instructions to align with this repository's architecture and the DSOM protocol.

---

## Critical Instructions for AI Agents

1. **Read the Full Rulebook:** Navigate immediately to [`.agents/AGENTS.md`](.agents/AGENTS.md). This is the **Cognitive Entry Point** — the Master Rulebook containing the absolute laws, operational persona, writing styles, and all 29 detailed rules governing this project. The file you are reading now is a summary gateway only.

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
| **Open Knowledge Format (OKF)** | All `.md` documents use OKF (v0.1/v0.2) YAML frontmatter (`okf_version`, `type`, `title`, `timestamp`, `topics`), migrating opportunistically to v0.2 to protect token budgets. Must start on line 1, column 1 without BOM, with all strings containing emojis, colons, brackets, or special characters wrapped in double quotes for clean GitHub parsing. |
| **Atomic Git Commits** | Every logical action results in a discrete, semantically named Git commit. No monolithic blanket commits. |
| **Omni-Documentation Sync** | New governance documents must be registered in `SUMMARY.md` (for GitBook navigation), `mkdocs.yml` (for MkDocs/GitHub Pages navigation), `START-HERE.md`, and `llms.txt`. |
| **Sovereign Signatures** | Every markdown or readable script modified by an AI must be processed via `dsom-signature-injector`. |
| **Ansible Legacy (The Executor)** | The Third Pillar is modular: `ansible-playbook`, `uv run`, `npm run`, or `pandoc` — governed by idempotency. |
| **Command-First Architecture** | Prose instructions are converted into exact, executable, byte-capped terminal invocations. |
| **Jules & Antigravity Collaborative Sync** | Google Jules and Google Antigravity share collective architectural knowledge, including atomic replacement protocols, YAML CustomLoader safe preservation, MkDocs exclusion negation, custom link rewriting hooks, and Windows Git-symlink/CRLF test guardrails. |
| **Tri-Phasic Mind & Subsystems** | Cognitive pipeline partitioned into Active (low-latency MCP), Twilight (linters, token gates), and Deep (EOD palace-sync consolidation) states. Enforces the four functional subsystems (Cognitive Architecture, Memory Stratification, "Dreaming" & Consolidation, Metacognition & Guardrails). |
| **Native OpenWiki Emulator Mandate** | AI maintains `./openwiki/` documentation trees directly via native Python scripts (`uv run --with pyyaml python tools/openwiki_emulator.py`), eliminating external Node.js binaries, UAC elevation hangs, and API rate limits. |
| **Downstream Asymmetry & Cross-Agent Honor** | Baseline repo houses the full metacognitive engine, while downstream projects adopt the lean 6-pillar footprint and Universal Gateway Matrix (`.cursorrules`, `CLAUDE.md`, `copilot-instructions.md`, `AGENTS.md`) compelling foreign AI agents to strictly honor the DSOM brain. |
| **Diátaxis Documentation Compass** | Enforces 4-quadrant separation (Tutorials, How-To Guides, Reference, Explanation) across `START-HERE.md` and `docs/` to eliminate cognitive fatigue and maximize token efficiency. |
| **Dual-Path Custom Validators** | Integrates both the Guardrails AI Framework (for external LLM apps/Pydantic schemas) and the DSOM Native Lightweight Pathway (for FastMCP/AST command interception and offline safety) across Tri-Phasic states. |
| **The Episodic Resume Protocol (Zero Amnesia)** | AI emits a serialized `[DSOM EPISODIC RECORD]` summary block containing live commit hashes, test metrics, and cognitive delta at major milestones to guarantee zero-loss session resumes. |
| **Agent Plugins 1.0.0 Standard** | Adheres to the vendor-neutral directory standard (`agent-plugins.org/specification`) for packaging skills, MCP servers (`mcp.json`), and manifests (`plugin.json`) across AI tools. |

---

## Agent Skills (`/.agents/skills/`)

Skills are OKF-compliant Standard Operating Procedures (SOPs) that govern how the AI performs complex, repeatable workflows. Each skill lives in its own subdirectory with a `SKILL.md` instruction file. AI agents must discover skills via OKF `topics:` metadata (`grep_search`) and load the full `SKILL.md` only at the moment of execution.

### Project Lifecycle Skills

| Skill | Purpose | Input | Output |
|:---|:---|:---|:---|
| `dsom-bootstrap` | Bootstraps a new or existing project with the DSOM baseline structure. | Target project path. | Initialised `.agents/`, `docs/`, and `tools/` structure. |
| `dsom-project-cloner` | Scaffolds a brand new DSOM project by copying the sovereign engine from the baseline repo. | Target path, project name. | New DSOM-compliant project directory. |
| `agent-plugin-packager` | Packages and validates DSOM skills and FastMCP tools into portable Agent Plugins 1.0.0 bundles. | Skill/MCP path. | Compliant Agent Plugin package directory. |
| `initialize-gitops` | Initialises Git, creates the initial commit structure, and sets up remote tracking. | Repository URL, branch name. | Configured Git repo with DSOM GitOps conventions. |
| `dsom-release-manager` | Cuts a formal release, updates ledgers (`CHANGELOG.md`, `HISTORY.md`), tags the repo, and pushes to GitHub/GitLab. | Version number, release notes. | Git tag, updated ledgers, pushed release. |

### Knowledge & Documentation Skills

| Skill | Purpose | Input | Output |
|:---|:---|:---|:---|
| `dsom-knowledge-ingester` | Processes external raw documents and synthesises them into the Sovereign Markdown Palace (LLM WIKI pattern). | Raw document (URL, file, or text). | OKF-compliant `.md` document in `docs/`. |
| `dsom-policy-adopter` | Ingests an external research paper or policy PDF and formally integrates it into DSOM governance. | PDF URL or local file path. | OKF-compliant governance document in `docs/governance/`. |
| `okf-frontmatter-injector` | Injects OKF v0.1 YAML frontmatter (`okf_version`, `type`, `title`, `timestamp`, `topics`) into any `.md` file missing it. | File path or directory. | Updated `.md` files with valid OKF frontmatter. |
| `dsom-signature-injector` | Appends the DSOM ownership, timestamp, and GPL v3.0 signature to `.md` files; prepends comment headers to scripts. | File path(s). | Signed files with standard DSOM footer. |
| `palace-auditor` | Audits the Sovereign Markdown Palace — verifies index links, finds undocumented scripts, and proposes structural cleanups. | No input required. | Audit report with orphaned files and broken links. |
| `sitemap-seo-generator` | Generates and compiles standard sitemaps and SEO assets across platforms (GitHub Pages, Read the Docs, GitBook) to optimize search indexing. | No input required. | Generated `sitemap.txt`, `sitemap.xml`, and `robots.txt` files. |

### Document Output Skills

| Skill | Purpose | Input | Output |
|:---|:---|:---|:---|
| `latex-proposal-compiler` | Compiles a markdown proposal into a professionally formatted PDF via Pandoc and XeLaTeX. | Markdown `.md` file. | PDF document. |
| `node-proposal-formatter` | Compiles a markdown proposal into a formatted DOCX file using Node.js and the `docx` package. | Markdown `.md` file. | DOCX document. |
| `proposal-docx-formatter` | Alternative DOCX formatter for proposal documents. | Markdown `.md` file. | DOCX document. |
| `node-slide-generator` | Generates a PowerPoint presentation from a markdown outline using Node.js and `pptxgenjs`. | Markdown outline. | PPTX file. |
| `odp-slide-generator` | Generates styled 3-column corporate presentation slides (PPTX/ODP) using `python-pptx`. | Markdown outline or structured text. | PPTX/ODP file. |
| `publish-to-blogger` | Converts a markdown artifact into clean HTML for publishing on Blogger.com. | Markdown `.md` file. | HTML snippet with DSOM Human-AI Synergy Statement. |
| `pdf-text-extractor` | Downloads an external PDF and extracts its text content using `curl` and an isolated `uv` Python environment. | PDF URL. | Extracted plain text. |

### Git & Security Skills

| Skill | Purpose | Input | Output |
|:---|:---|:---|:---|
| `git-commit-resolver` | Resolves invalid or orphaned Git commit IDs in brain files by searching Git history for matching commit messages. | Orphaned commit hash or message. | Verified commit hash. |
| `git-history-scrubber` | Purges sensitive data (IPs, credentials, secrets) from Git history using `git-filter-repo`. | Pattern list (regex/strings). | Scrubbed Git history; requires force-push. |
| `github-actions-snyk-scanner` | Sets up a proven Snyk dependency vulnerability scan workflow for DSOM GitHub repositories, replacing the deprecated Red Hat CRDA action. | No input required (reads `requirements.txt`). | Deployed `.github/workflows/crda.yml` and SARIF results. |
| `forensic-log-audit` | Audits system and application logs for anomalies, failed authentications, or suspicious patterns. | Log file path or directory. | Forensic audit report. |
| `ssh-passwordless-setup` | Configures passwordless SSH key-based authentication between a control node and target hosts. | Source and target host details. | Configured `~/.ssh/authorized_keys` on target. |

### System & Environment Skills

| Skill | Purpose | Input | Output |
|:---|:---|:---|:---|
| `cross-platform-translator` | Analyses a `.ps1` or `.sh` script and generates its functional equivalent in the other shell language. | Shell script (`.ps1` or `.sh`). | Translated script in the target language. |
| `persona-injector` | Injects the DSOM Cognitive Twin persona profile into a new AI configuration. | Target AI platform config. | Updated persona profile. |
| `dsom-token-calculator` | Runs `tiktoken` against `.agents/skills/` to audit token counts and flag any `SKILL.md` exceeding the 4,000-token gate. | No input required. | Token audit report; flags `[BLOCKED]` files. |

### Session Ritual Skills

| Skill | Purpose | Input | Output |
|:---|:---|:---|:---|
| `sod-palace-sync` | Start-of-Day ritual: reads `palace_registry.md`, syncs the active context manifest, and generates the SOD manifest. | No input required. | Updated `sod_manifest.txt` and context manifest. |
| `eod-palace-sync` | End-of-Day ritual: maps Git commits to Palace Rooms, generates a `palace_update_proposal_*.md`, and prepares for hibernation. | No input required. | Palace update proposal for the AI to review. |

### Collaborative & Multi-Agent Skills

| Skill | Purpose | Input | Output |
|:---|:---|:---|:---|
| `jules-antigravity-sync` | Peer agent collaborative skill for sharing operational ledgers, Rule 25 state synchronization, and cognitive continuity between Jules and Antigravity. | None (automatic). | Shared operational ledgers and aligned rules. |

---

## Workflows (`/.agents/workflows/`)

Workflows are markdown-based governance guides providing step-by-step procedural instructions for multi-agent or complex human+AI tasks.

| Workflow | Purpose |
|:---|:---|
| `SUBAGENT-ORCHESTRATION-WORKFLOW.md` | Governs delegating tasks to autonomous subagents using Git Worktree Isolation to prevent Silent Subagent Merge Conflicts. |

---

## Automation Tools (`/tools/`)

The `tools/` directory contains cross-platform PowerShell (`.ps1`) and Bash (`.sh`) scripts for the daily DSOM operational rituals. All tools are idempotent and safe to re-run.

| Tool | Purpose | When to Run |
|:---|:---|:---|
| `reanimate.ps1` / `.sh` | Reanimates the AI session — generates the active context manifest from brain files and latest Git state. | **Start of every session.** |
| `hibernation.ps1` / `.sh` | EOD safety check: validates session anchor and task progress, runs palace-sync, commits, and pushes to remote. | **End of every session.** |
| `sod-palace.ps1` / `.sh` | Start-of-Day palace sync: reads palace registry and prepares daily context. | After `reanimate`. |
| `eod-palace.ps1` / `.sh` | End-of-Day palace sync: maps commits to Palace Rooms and generates update proposals. | Before `hibernation`. |
| `palace-sync.ps1` / `.sh` | Spatial reflection tool: scans Git commits and maps them to Sovereign Markdown Palace rooms. | SOD and EOD rituals. |
| `git-ritual.ps1` / `.sh` | Combines SOD `git pull --rebase` and EOD commit/push in a single safe invocation. | Daily Git hygiene. |
| `audit-pre-flight.ps1` / `.sh` | Validates the repository state before any major operation (checks OKF compliance, uncommitted changes). | Before bulk changes. |
| `diagnostic.ps1` / `.sh` | Full system diagnostic: checks brain files, tool availability, Git status, and OKF frontmatter coverage. | Debugging sessions. |
| `init-brain.ps1` / `.sh` | One-time initialisation of the `.agents/brain/` directory with blank OKF-compliant template files. | New project setup. |
| `checkpoint.ps1` / `.sh` | Creates a checkpoint snapshot of the current brain state without triggering full hibernation. | Mid-session saves. |
| `privacy-guardian.ps1` / `.sh` | Scans the active context manifest and session files for sensitive data (IPs, credentials) before sharing. | Before any external sync. |
| `template-reset.ps1` / `.sh` | Resets brain files to blank OKF-compliant templates for a clean session start. | Session reset. |
| `dsom-onboard.ps1` / `.sh` | One-shot onboarding script for new DSOM project contributors. | First-time setup. |
| `setup-wsl-almalinux10.ps1` | Installs and configures WSL2 with AlmaLinux 10 as the local DSOM Control Node / Execution Bridge on Windows 11. | Windows-only environment setup. |
| `setup-dsom-control-node.sh` | Configures a Linux node (physical, VM, or WSL2) as the DSOM Ansible Control Node with required tooling. | Linux control node setup. |
| `palace-sync.ps1` / `.sh` | Generates `palace_update_proposal_*.md` by correlating Git commits with Palace room definitions. | EOD ritual. |
| `build_sovereign_book.sh` | Builds the full GitBook/MkDocs documentation site from the Sovereign Markdown Palace. | Documentation deployment. |
| `check-usage.sh` / `CheckUsage.ps1` | Audits token and context window usage across brain files and skills. | Periodic maintenance. |
| `bench_brain.py` | Benchmarks brain file read latency (FUSE/disk) to calibrate token and context performance multipliers. | Performance tuning. |
| `generate-walkthrough.ps1` / `.sh` | Generates a formatted session walkthrough summary from brain state. | Session documentation. |
| `guardrails-ai-dsom` | Standalone Python package providing 10 DSOM custom validators for Guardrails AI & FastMCP. | Active/Twilight/Deep safety & pre-commit validation. |
| `install_git_guardrails.py` | Installs the unbypassable Git pre-commit guardrail hook running `guardrails-ai-dsom`. | Repo setup & initialization. |

---

## Key Files & Directories for AI Agents

| Path | Purpose |
|:---|:---|
| `AGENTS.md` | **Root Gateway** — this file. First read for all platform AI agents. |
| `.agents/AGENTS.md` | **Full Rulebook** — Core laws (29 rules), persona, boot sequence, and discovery protocols. |
| `.agents/brain/task.md` | Active task list for the current session. |
| `.agents/brain/walkthrough.md` | Session history and Mental Anchors (resume context). |
| `.agents/brain/palace_registry.md` | Spatial index of the Sovereign Markdown Palace. |
| `.agents/brain/active_context_manifest.md` | Live list of files currently in scope. |
| `.agents/skills/` | OKF-compliant executable skill SOPs (32 skills). |
| `.agents/workflows/` | Multi-agent orchestration governance workflows. |
| `docs/governance/` | Theoretical blueprints, governance policies, and architectural guides. |
| `docs/governance/AI-INITIALIZATION-SEQUENCE.md` | The 5-step Mechanical Boot Sequence. |
| `docs/governance/SOP-KNOWLEDGE-FIRST-DISCOVERY.md` | The 5-step Knowledge-First Discovery Protocol. |
| `START-HERE.md` | Master onboarding map with 19 defined entry points. |
| `llms.txt` | AI Sitemap for external crawlers (NotebookLM, ChatGPT, etc.). |
| `tools/` | Cross-platform automation scripts for all daily DSOM rituals. |

---

> **Tip:** Keep both `AGENTS.md` files up to date — the root gateway and `.agents/AGENTS.md`. This helps Google Jules, Cursor, GitHub Copilot, other AI agents, and your human teammates work with this repository more effectively and in full alignment with the DSOM protocol.

---
*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-08-22*
*Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*

<!-- OPENWIKI:START -->

## OpenWiki

This repository has a generated `openwiki/` evidence index. It is optional just-in-time context, not required startup reading.

- Treat source code and tests as authoritative. A brief's unknowns and review items are verification gaps, not automatic requirements.
- Prefer the narrowest quiet validation that proves the changed behaviour. Preserve complete failure output.

The scheduled OpenWiki GitHub Actions workflow refreshes the repository wiki. Do not hand-edit generated OpenWiki pages unless explicitly asked; prefer updating source code/docs and letting OpenWiki regenerate.

<!-- OPENWIKI:END -->
