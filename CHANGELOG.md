# 📜 Changelog: Deep State of Mind (DSOM) For My AI
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [6.1.4] - 2026-03-29
### Changed
- **`tools/reanimate.sh`** — Upgraded from v2.0 to v2.1. Added `set -euo pipefail`, colour header banner, brain artifact validation, Cognitive Twin Protocol as section \[4\], head-60 summaries for SOD-RITUAL and RITUAL-OF-TRANSITION, v6.1 handshake prompt in footer.
- **`tools/reanimate.ps1`** — Upgraded from v1.5 to v2.0. Achieved full 13-section parity with the bash counterpart. Added sections \[4\] Cognitive Twin Protocol, \[12\] Ansible Inventory, \[13\] GitOps Strategy. Fixed double-output bug from v1.5. Added brain artifact validation and `Get-FileHeadSafe` helper.

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
- **`docs/AI-COGNITIVE-TWIN-PROTOCOL.md`** — Removed placeholder variables and restored default baseline paths to pass the pre-flight checks.
- **Brain Artifacts** — Updated `.agent/brain/` session tracking to maintain the GitOps/AIOps continuity loop.

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
- **The Brain Artifacts:** Initialised `.agent/brain/` with `task.md`, `walkthrough.md`, and `implementation_plan.md`.
- **DSOM Persistence Protocol:** Established the Handshake ritual for session reanimation.

---

## [1.0.0] - Day 0 (2025-09-16)
### Added
- **Initial Concept:** Foundation of the Deep State of Mind (DSOM) protocol for preventing AI context decay.
- **Sovereign Laws:** Early draft of Zero-Global Pattern and Linux-agnostic infrastructure.

