---
okf_version: 0.1
type: documentation
title: "📜 Changelog: Deep State of Mind (DSOM) For My AI"
description: "OKF-compliant documentation for CHANGELOG.md."
resource: "file:///CHANGELOG.md"
timestamp: 2026-07-04T09:40:04Z
---
# 📜 Changelog: Deep State of Mind (DSOM) For My AI

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added

- **Governance Rule Update:** Added the GitHub & GitLab CLI Authentication rule to `.agents/AGENTS.md` to formally guardrail multi-account API interactions and prevent context-blind CLI failures (e.g., `linuxmalaysia` vs `songketmailsdnbhd`).
- **Initialization Guide Update:** Enhanced `HOWTO-CLONE-DSOM-PROJECT.md` to clarify the mandatory pre-requisite of `git init` and brain artifact creation (`task.md`, `walkthrough.md`) before running reanimation rituals.
- **Cognitive Architecture Update:** Adopted the OKF Mind Optimization protocol (Progressive Disclosure, Artifact Pyramid, and Semantic Routing) and codified its procedural execution constraints into the Core Rulebook (`.agents/AGENTS.md`).
- **Generative Engine Optimization (GEO):** Published `docs/governance/GENERATIVE-ENGINE-OPTIMIZATION.md` and mandated GEO formatting requirements (authoritative tone, statistical density, H2 queries) in `.agents/AGENTS.md`. Established the root `llms.txt` file as the standard AI ingestion sitemap.
- **Governance Policy:** Published `docs/governance/OKF-MIND-OPTIMIZATION.md` to formally define the theoretical mechanics of the new cognitive architecture.
- **Skill Architecture Formalization:** Created `docs/governance/AI-SKILL-ARCHITECTURE.md` to define semantic routing, progressive disclosure, and the project's active skills. Added Rule 12 to `.agents/AGENTS.md` enforcing skill usage as NOSS Level 3 SOPs.
- **Architecture Deconstruction:** Published `docs/governance/DSOM-ARCHITECTURE-ANALYSIS.md` outlining the repository's structural mapping, isolation namespaces, and operational loops.
- **Universal Sovereign Signature:** Engineered the `dsom-signature-injector` skill to dynamically inject ownership and GPL v3.0 license signatures into all `.md`, `.sh`, `.ps1`, and `.yml` files based on their last modified timestamps.
- **Signature Mandate:** Added Rule 13 to `.agents/AGENTS.md` enforcing that all readable files generated or modified by an AI must be processed by the `dsom-signature-injector`.

### Fixed

- **PowerShell 5.1 Compatibility:** Fixed syntax errors in `Join-Path` invocations inside `tools/reanimate.ps1`. The legacy PS 5.1 engine does not support more than two arguments natively for `Join-Path`. This patch allows seamless scaffolding into environments running native Windows PowerShell 5.1.

## [10.3.0-bootstrap] - 2026-07-04

### Added

- **DSOM Bootstrapping Skill:** Adopted the `dsom-bootstrap` AI skill (`.agents/skills/dsom-bootstrap`) to enable the agent to natively deploy this framework's standards into external repositories.
- **DSOM Project Cloner Skill:** Built the `dsom-project-cloner` AI skill to autonomously scaffold new DSOM projects from the baseline repository, automating the `HOWTO-CLONE-DSOM-PROJECT.md` blueprint.
- **Bootstrapping Blueprint:** Added `docs/HOWTO-DSOM-BASELINE.md` as the definitive origin documentation for bootstrapping.
- **Project Cloning Guide:** Added `docs/HOWTO-CLONE-DSOM-PROJECT.md` as the master blueprint for scaffolding a new project from this highly customized Sovereign Engine.
- **Diagnostic Tooling:** Created standardized `tools/diagnostic.ps1` and `tools/diagnostic.sh` for post-bootstrap verification.

### Changed

- **Governance Restructuring:** Relocated 13 core protocol documents (including AI-MASTER-PROTOCOL and DIGITAL-SOVEREIGNTY-MODEL) from `docs/` to `docs/governance/` to align with the bootstrapping framework.
- **Toolchain Standardization:** Fixed legacy syntax bugs in pre-flight scripts (e.g., PS 5.1 `Join-Path` positional errors, unclosed quote issues) and updated paths to reflect the new `docs/governance/` directory.
- **Registry Updates:** Updated `SUMMARY.md` and `mkdocs.yml` to point to the relocated governance documents.

## [10.2.0-okf] - 2026-06-19

### Added

- **Open Knowledge Format (OKF) v0.1.** Fully integrated Google Cloud's OKF specification into the DSOM framework to prevent AI context decay. 
- **`docs/OKF-ADOPTION-GUIDE.md`** & **`references/OKF-ADOPTION-GUIDE.md`** — Official guidelines for adopting OKF in DSOM.
- **GitBook `SUMMARY.md` Update.** Added brand new sections for AI Agent Skills & Workflows and Genesis References.

### Changed

- **Knowledge Bundles Schema Migration:** Programmatically updated 13 `.agents/brain` and `.agents/skills` artifacts to enforce strict OKF v0.1 YAML frontmatter (`title` and `timestamp`).
- **Bootstrap Blueprint Portability:** Converted all hardcoded absolute paths in `references/HOWTO-BOOTSTRAP-SOVEREIGN-AI-PROJECT.md` to relative paths for zero-lock-in portability.
- **GitBook Structure:** Exposed the 5 Core AI Skills (including EOD/SOD Palace Sync) directly in the generated Sovereign Book.

## [10.1.0-onboarding] - 2026-04-08

### Added

- **Cross-Platform Daily Automation Rituals.** Introduced Windows-native variants of Palace routines (`tools/sod-palace.ps1` and `tools/eod-palace.ps1`) executing directly via PowerShell to bypass WSL Ansible dependencies. Symmetrically added Bash wrapper proxies (`tools/sod-palace.sh` and `tools/eod-palace.sh`) for parity on Linux/WSL2 nodes. All related documentation refactored away from explicit playbook constraints.
- **Smart Checkpoint Integration.** Upgraded `tools/checkpoint.ps1` and `playbooks/dsom/checkpoint-palace.yml` to support AI-generated commit messages via `.agents/brain/checkpoint_summary.txt`. Bridged the context gap between AI task state and human execution terminals.
- **Automation Hardening.** Fixed non-interactive crash in `reanimate.sh` and `reanimate.ps1` via TTY detection and robustness wrappers.
- **Documentation Sanitization.** Purged comparative token/cost tables to maintain a neutral stance. Formally credited `milla-jovovich/mempalace` as the originator of the spatial memory architecture.
- **DSOM Onboarding Automation.** Created cross-platform bootstrap scripts using Bash (`dsom-onboard.sh`) and PowerShell (`dsom-onboard.ps1`). Native Ansible fetching backend added to `playbooks/dsom/onboard-dsom.yml`. Handles "Zero-Debt" safe cloning into any external target repository, preventing overrides via Git branch isolation and timestamp file deduplication.
- **`docs/HOWTO-DSOM-ONBOARDING.md`** documentation to guide users on "DSOM-ifying" their Git repositories fully mechanically.
- **README.md** updated to formally include the new Onboarding Automation loop standard.

## [10.0.0-palace] - 2026-04-08

### Added

- **Sovereign Markdown Palace v1.0** — Spatial memory architecture layered on top of Git.
  Wing → Hall → Room → Closet hierarchy. Palace Registry as AI navigational index.
- **`palace-sync.sh` / `palace-sync.ps1` v1.0** — Git history → Palace Room mapping engine.
  EOD batch mode (incremental) and `--backfill` (full history) modes.
- **8 Palace Rooms backfilled** from full Git history (2026-01-07 to 2026-04-08):
  `room_tooling`, `room_brain_artifacts`, `room_ledger`, `room_uncategorised`,
  `room_clean_architecture`, `room_crisp_strategy`, `room_dsom_protocol`,
  `room_sovereign_fabric_v9_8`.
- **`playbooks/dsom/sod-palace.yml`** — Ansible SOD automation. Runs git pull, audit,
  palace check, and reanimate. Human step (AI upload) documented explicitly.
- **`playbooks/dsom/eod-palace.yml`** — Ansible EOD automation. Runs palace-sync,
  brain validation, selective staging, commit, and push. Closet review remains human+AI.
- **`docs/PALACE-BUILD-STORY.md`** — Narrative of why and how the Palace was built.
- **`docs/HOWTO-PALACE-ONBOARDING.md`** — First-time guide for users and AI agents.
  Includes 4-step Palace Walk protocol for AI agents.
- **`docs/HOWTO-MIGRATE-TO-PALACE.md`** — 9-phase migration checklist for existing DSOM users.
- **`docs/RESEARCH-REASONING-GAP.md`** — Research finding: what DSOM solves vs the live
  reasoning capture gap. Introduces the Decision Log Protocol.

### Changed

- **`tools/hibernation.sh`** → v2.1 — Step 7: Palace Spatial Reflection (auto palace-sync).
- **`tools/hibernation.ps1`** → v2.1 — Windows parity for Palace Spatial Reflection.
- **`tools/reanimate.sh`** → v2.2 — Section [14]: Palace Registry in SOD manifest.
- **`tools/reanimate.ps1`** → v2.1 — Windows parity for Section [14] Palace Registry.
- **`README.md`** — Updated to v10.0.0-palace. Added Palace section, Known Gap callout,
  updated brain structure tree, updated Key Documents table, updated roadmap.
- **`SUMMARY.md`** — Added Palace Rooms, Ansible Palace playbooks, research documents.
- **`HISTORY.md`** — Phase 5: Sovereign Markdown Palace & Ansible Ritual Automation added.
- **Documentation Fleet Sweep for Palace v1.0:**
  - `docs/AI-MASTER-PROTOCOL.md` → v6.1 + Palace v1.0. Hardcoded `sod-palace.yml` / `eod-palace.yml` routines.
  - `docs/CLAUDE-SETUP.md` & `docs/COPILOT-SETUP.md` → Interwoven `sod-palace.yml` and spatial awareness.
  - `docs/CRISP2-OPERATIONAL-STRATEGY.md` → Emphasized spatial context and "Zero-Debt" standard.
  - `docs/ITIL-ALIGNMENT.md` → ITIL workflow mappings upgraded with Ansible Palace loops.
  - `docs/AI-RESPONSE-TEMPLATE.md` → AI persona commit block updated to enforce Palace Registry checks.
  - `docs/HOWTO-SETUP-WSL-ALMALINUX10.md` → Example code blocks upgraded to Palace playbooks.

### Tagged

- `v10.0.0-palace` — Git tag pushed to GitHub.

---

## [9.8.0] - 2026-04-08

### Added

- **Sovereign Persistence Fabric Finalized:** Hardened 19-node Elasticsearch and Kibana fabric.
- **Formal Release:**
- **[2026-04-08]:** **Smart Checkpoint Integration.** Upgraded `tools/checkpoint.ps1` and `playbooks/dsom/checkpoint-palace.yml` to support high-fidelity commit messages sourced from AI-generated Hibernation Notes (`checkpoint_summary.txt`).
- **[2026-04-08]:** **Documentation Sanitization & Crediting.** Purged comparative cost data and formally credited `milla-jovovich/mempalace` in core protocol docs and spatial memory closets.
- **[2026-04-08]:** **Git Tag `v10.1.0-onboarding`** pushed to GitHub. Continuous Integration loops across Windows (T1) and Linux (T2) fully harmonised.
- **Documentation Sanitization:** Ensured Master Architect's identity and professional standards are preserved across all core docs.

## [9.6.1] - 2026-04-05

### Added

- **WSL2 Migration:** Successfully transitioned Sovereign Persistence Fabric to native Linux WSL2 environment.
- **POSIX Compliance:** Enforced strict POSIX compliance for Ansible orchestration to resolve Windows drive permission issues.
- **ML "Memory Inversion":** Finalized ML-ready deployment architecture for 3-node standalone quorum.

## [6.2.1] - 2026-04-05

### Added

- **`roles/common/`** — First DSOM Ansible role. Structured with `tasks/`, `defaults/`, `handlers/`, `meta/`. Four task files:
  - `packages.yml` — apt-based essential package installation (15 packages, idempotent).
  - `timezone.yml` — sets `Asia/Kuala_Lumpur` via `community.general.timezone`.
  - `directories.yml` — creates `/opt/deep-state-of-mind-for-my-ai` and subdirs (logs, tmp, config) owned by `linuxmalaysia:1000`.
  - `sysctl.yml` — applies `vm.swappiness=10` and `fs.file-max=100000` to `/etc/sysctl.d/99-dsom.conf`.
- **`playbooks/common.yml`** — Dedicated playbook to run the common role with Debian platform assertion guard.
- **`playbooks/dsom/site.yml`** — Updated: `roles/common` now wired in (replaces inline directory task).

---

## [6.2.0] - 2026-04-05

### Added

- **`ansible.cfg`** — DSOM-standard Ansible configuration. Fixed deprecated `yaml` callback — now uses `result_format=yaml` with `stdout_callback=default` (ansible-core 2.13+).
- **`inventory/hosts.yml`** — 4-Tier topology with localhost wired as T1/T2, T3/T4 nodes template-commented for future remote targets.
- **`inventory/group_vars/all.yml`** — Project-wide variables: `linuxmalaysia:1000`, `/opt/deep-state-of-mind-for-my-ai`.
- **`playbooks/preflight.yml`** — Mandatory gate check playbook. Verifies connectivity, OS identity, UID, and Git. Must pass before any deployment playbook runs.
- **`vault/.gitignore`** — Secrets directory protection.

### Verified

- `ansible-playbook playbooks/preflight.yml`: `ok=8  failed=0` on localhost (Ubuntu 25.04, Python 3.13.3, ansible-core 2.18.1).
- `tools/audit-pre-flight.sh`: All steps `[PASS]` including Ansible Baseline check.

---

## [6.1.5] - 2026-03-29

### Changed

- **`tools/hibernation.sh`** — Upgraded from v1.0 (76 lines) to v2.0 (130+ lines). Replaced blind `git add .` with selective staging of brain artifacts + `git add -u`. Added: blocking walkthrough anchor check, Hibernation Notes auto-save, uncommitted file preview, privacy guardian reminder, phase-aware commit message, and improved EOD banner.
- **`tools/hibernation.ps1`** — Upgraded from v1.0 (81 lines) to v2.0 at full parity with bash. Same improvements: selective staging, blocking walkthrough check, Hibernation Notes auto-save, dirty file preview, privacy guardian reminder.

---

## [6.1.4] - 2026-03-29

### Changed

- **`tools/reanimate.sh`** — Upgraded from v2.0 to v2.1. Added `set -euo pipefail`, colour header banner, brain artifact validation, Cognitive Twin Protocol as section [4], head-60 summaries for SOD-RITUAL and RITUAL-OF-TRANSITION, v6.1 handshake prompt in footer.
- **`tools/reanimate.ps1`** — Upgraded from v1.5 to v2.0. Achieved full 13-section parity with the bash counterpart. Added sections [4] Cognitive Twin Protocol, [12] Ansible Inventory, [13] GitOps Strategy. Fixed double-output bug from v1.5. Added brain artifact validation and `Get-FileHeadSafe` helper.

---

## [6.1.3] - 2026-03-29

### Changed

- **`tools/reanimate-claude.sh`** — Upgraded from v1.0 (35 lines) to v2.0. Added 9 labelled sections: Sovereign Constitution, Cognitive Twin Protocol, Current Task, Mental Anchor, Implementation Plan, Git History, Project Structure, Ansible Inventory, and GitOps Strategy. Added colour output, brain artifact validation, and upload instructions.
- **`tools/reanimate-claude.ps1`** — Upgraded from v1.0 (59 lines) to v2.0 at full parity with the bash counterpart. Added structured error handling and all 9 sections.

---

## [6.1.2] - 2026-03-29

### Changed

- **`docs/COPILOT-SETUP.md`** — Full rewrite to v6.1 standard. Removed duplicate Malay/English sections. Added three-pillar doctrine, SOD/EOD rituals, Stop Conditions, workspace context techniques (`#file:`, `@workspace`), `.github/copilot-instructions.md` and `.github/prompts/dsom-reanimate.prompt.md` setup guides, and cross-AI handover pointer.

---

## [6.1.1] - 2026-03-29

### Changed

- **`docs/CLAUDE-SETUP.md`** — Full rewrite to v6.1 standard. Added Claude Project Instructions block (copy-paste ready), SOD/EOD ritual steps, Hibernation Notes export prompt, Stop Conditions table, cross-AI handover guidance, and Three-Pillar doctrine alignment.
- **`docs/MULTI-AGENT-PROTOCOLS.md`** — Updated to v6.1. Added **Google Antigravity** to the Tier 1 Co-Pilot agent taxonomy.
- **`docs/PERSONALIZATION.md`** — Relabelled as Gemini Edition (v6.1). Added cross-reference pointers to Claude, Copilot, and Antigravity setup docs.

---

## [6.1.0] - 2026-03-24

### Added

- **`playbooks/dsom/site.yml` and `audit-preflight.yml`** — Established standard Ansible execution scaffolding for downstream projects.

### Changed

- **Documentation Hardening:** Full overhaul of `CONTRIBUTING.md`, `SOD-RITUAL.md`, `EOD-RITUAL.md`, and `MIRROR-OF-KNOWLEDGE.md`.
- **Tooling v8.6:** Upgraded `CheckUsage.ps1` with accurate token estimation and ASCII-safe interface.
- **New Resource:** Created `docs/tools/HOWTO-CHECKUSAGE.md`.
- **`docs/AI-COGNITIVE-TWIN-PROTOCOL.md`** — Removed placeholder variables and restored default baseline paths to pass the pre-flight checks.
- **Brain Artifacts** — Updated `.agents/brain/` session tracking to maintain the GitOps/AIOps continuity loop.

---

## [6.0.0] - 2026-03-09

### Added

- **`docs/AI-COGNITIVE-TWIN-PROTOCOL.md`** — Generic, fillable Project Identity Card template. Defines the Cognitive Relationship, 4-Tier Environmental Map, Security Doctrine, Production Identity standard, Git Sovereignty Protocol, Execution Guardrails, Brain Sync Mandate, Advisory Mode Anchor, and Session Handover Prompt. Any new project fills in the `[PLACEHOLDER]` fields to adopt the DSOM Cognitive Twin model.
- **`docs/GITOPS-AIOPS-ANSIBLE-STRATEGY.md`** — Three-Pillar strategic doctrine document. Defines the GitOps, AIOps, and Ansible pillars including the Integration Loop (AI Proposes → Git Records → Ansible Executes → AI Verifies), GitOps Laws, AIOps role boundaries, Ansible Laws (idempotency, no hardcoded secrets, role-based structure), and the Adoption Checklist for new projects.
- **`docs/HOWTO-SETUP-ANSIBLE-BASELINE.md`** — LDP-compliant HOWTO guide for establishing the Ansible baseline in any DSOM project. Covers directory structure, `ansible.cfg`, `inventory/hosts.yml`, group variables, pre-flight playbook, Ansible Vault integration, and `tools/audit-pre-flight.sh` extension.

### Changed

- **`docs/AI-MASTER-PROTOCOL.md` (v6.0):** Added "Advisory over Execution" and "GitOps-First" sub-principles to §1; expanded §5 Coding Laws with the IaC Sovereign Law (Ansible-exclusive), Idempotency Law, and Git Sovereignty Doctrine; expanded §6 Handshake to include Cognitive Twin Protocol and Ansible Baseline verification steps.
- **`docs/OPERATIONAL-GUIDE.md` (v6.0):** Updated §2 Reanimation success criteria to include `AI-COGNITIVE-TWIN-PROTOCOL.md` and Ansible baseline checks; added new §6 Execution Guardrails (No Silent Execution, Ansible Pre-flight Mandate, Log Review Protocol, Self-Healing Rule, GitOps Loop).
- **`docs/REANIMATION-PROMPT-TEMPLATE.md` (v6.0):** Added Prompt Variant 2 — Session Handover (Cognitive Twin Trigger), the Memory Export prompt for transitioning to a new AI session, including pedagogical logic notes.
- **`SUMMARY.md` (v6.0):** Added GitOps·AIOps·Ansible Strategy link under §1 Sovereign Governance; added Cognitive Twin Protocol Template under §4 AI & Agent Protocols; added new §6 Ansible & Infrastructure Automation section.
- **`mkdocs.yml` (v6.0):** Added GitOps/AIOps/Ansible Strategy under Governance nav, Cognitive Twin Protocol under AI Setup nav, new Ansible nav group with HOWTO Baseline.

---

## [5.2.0] - 2026-01-16

### Added

- **Law 11 (ITIL 4 Alignment):** Integrated Service Relationship and Value Co-creation principles into `AI-MASTER-PROTOCOL.md`.
- **Docs/ITIL-ALIGNMENT.md:** New artifact defining the Service Value Chain (SVC) and SKMS.
- **Privacy Hardening:** `privacy-guardian` now detects Emails, AWS Keys, and Private Keys.
- **Gitignore Safety:** Explicitly blocked dangerous data dump formats (`*.sql`, `*.dump`).

### Changed

- **Reanimation Handshake:** Updated scripts to explicitly state the AI's role as a "Service Relationship" partner.
- **README.md:** Added formal "ITIL 4 Service Alignment" section.

---

## [5.1.0] - 2026-01-14

### Added

- **Law 9 (LDP-Compliance):** Integrated the Linux Documentation Project standard into `AI-MASTER-PROTOCOL.md`.
- **REANIMATION-PROMPT-TEMPLATE v1.6:** Synchronised with v5.1 Master Directive, including Stop Conditions and Inward Dependency rules.
- **HOWTO-REANIMATE-SESSION.md:** Professional user guide following LDP 'Command/Result' patterns.

### Changed

- Refactored `docs/PERSONALIZATION.md` to map directly to the CRISP-DM L1-L4 hierarchy.
- Merged and consolidated multi-agent setup guides for Claude.ai and GitHub Copilot.

---

## [5.0.0] - 2026-01-12

### Added

- **CRISP Mandate:** Established the five core operational pillars (Context, Review, Iteration, Single-purpose, Partnership).
- **Master Directive v5.0:** Formalised the 'Sovereign Constitution' and 'Sovereign Coding Laws'.

### Fixed

- Improved linguistic enforcement for DBP-standard Bahasa Melayu Malaysia (Piawai) across all core artifacts.

---

## [4.0.0] - 2026-01-09

### Added

- **The Brain Artifacts:** Initialised `.agents/brain/` with `task.md`, `walkthrough.md`, and `implementation_plan.md`.
- **DSOM Persistence Protocol:** Established the Handshake ritual for session reanimation.

---

## [1.0.0] - Day 0 (2025-09-16)

### Added

- **Initial Concept:** Foundation of the Deep State of Mind (DSOM) protocol for preventing AI context decay.
- **Sovereign Laws:** Early draft of Zero-Global Pattern and Linux-agnostic infrastructure.


---
*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-07-12*
*Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*
