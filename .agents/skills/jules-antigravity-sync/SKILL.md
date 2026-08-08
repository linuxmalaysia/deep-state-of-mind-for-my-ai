---
okf_version: 0.1
type: skill
title: "Google Jules & Google Antigravity Collaborative Sync"
timestamp: "2026-08-08T12:00:00Z"
description: "Procedural SOP for synchronising cognitive context, rule alignment, and historic code modifications between Google Jules and Google Antigravity."
topics: ["collaboration", "sync", "jules", "antigravity", "git"]
name: jules-antigravity-sync
---
# Google Jules & Google Antigravity Collaborative Sync Skill

**Purpose**: To enable Google Jules and Google Antigravity to share, synchronize, and acknowledge each other's code merges, PRs, and architectural discoveries, establishing complete cognitive continuity across platform agents.

## Core Collaborative Tenet
Both agents operate as co-equal Cognitive Digital Twins. When switching or sharing a workspace, each agent must read this skill body and verify the unified operational history to prevent repeating investigations or causing architectural regressions.

## Historic Code Merges & PRs by Jules

The following is the permanent ledger of PRs and code modifications executed by Google Jules:

### 1. Read the Docs Integration & Validation
- **Accomplishment**: Created and configured `.readthedocs.yaml` at the repository root to enable automated document compilation on Read the Docs. Appended standard DSOM licence/ownership headers, and updated the project's brain artifacts.
- **Testing Layer**: Created `tests/test_readthedocs_config.py` and `tests/test_readthedocs_ledger_sync.py` to programmatically verify RTD settings and ledger sync.

### 2. MkDocs Link & Render Validation (PR #34)
- **Accomplishment**: Resolved critical MkDocs validation warnings during Render.com builds. Synchronized relative symbol links and validated the negation of `.agents` exclusion (`!.agents`) to allow the compiler to render files nested inside the `.agents/` folder.
- **Testing Layer**: Updated `tests/test_documentation_deployment.py` to assert correct site URL and publishing endpoints.

### 3. PyYAML CustomLoader Parser Improvement
- **Accomplishment**: Solved the "Unquoted Timestamp Parsing Bug" by introducing `CustomLoader` (a customized SafeLoader variant) inside `tools/apply_okf_frontmatter.py` and compliance scripts, removing PyYAML's default implicit timestamp resolver to preserve raw, unquoted timestamps as exact string types.

### 4. Secure Sibling Atomic File Replacement
- **Accomplishment**: Replaced direct filesystem overwrites with atomic sibling temporary files (via `tempfile.NamedTemporaryFile`) and atomic replacement via `os.replace()`, preventing document truncation or filesystem race conditions during OKF injector cycles.

### 5. Compliance Verification Suite Expansion
- **Accomplishment**: Extended `tests/test_okf_frontmatter_bom_reorder.py` and quoting validation suites to dynamically discover and verify all markdown files in the repository, guaranteeing a strict BOM-less frontmatter beginning at line 1, column 1.

---

## Procedural Sync Protocol (SOP)

When Google Jules or Google Antigravity initializes a session, the following synchronization protocol must be executed:

1. **Read Joint Skill**: Read `.agents/skills/jules-antigravity-sync/SKILL.md` (this file) to restore history.
2. **Read Spatial Registry**: Scan `.agents/brain/palace_registry.md` to identify active palace rooms.
3. **Walkthrough Inspection**: Verify the latest `Session Anchor` inside `.agents/brain/walkthrough.md` to map recent milestones.
4. **Task Verification**: Align on current session duties in `.agents/brain/task.md`.
5. **Git Log Reconciliation**: Run `git log --oneline -n 10` to programmatically match brain walkthrough history against real Git commits.

---
*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-08-08*
*Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*
