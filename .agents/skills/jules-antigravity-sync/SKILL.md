---
okf_version: 0.2
type: skill_sop
title: "Google Jules & Google Antigravity Collaborative Sync"
timestamp: "2026-08-22T23:20:00Z"
description: "Procedural SOP for synchronising cognitive context, rule alignment, and historic code modifications between Google Jules and Google Antigravity."
topics: ["collaboration", "sync", "jules", "antigravity", "git", "powershell", "mintlify", "agent-plugins"]
sources: [{title: The Core AI Rulebook (DSOM), url: 'file:///.agents/AGENTS.md'}, {title: Jules PR History Ledger, url: 'file:///.agents/brain/jules_pr_history.md'}]
generated: human-and-ai
verified: verified
status: authoritative
stale_after: "2027-08-22T23:20:00Z"
name: jules-antigravity-sync
---
# Google Jules & Google Antigravity Collaborative Sync Skill

**Purpose**: To enable Google Jules and Google Antigravity to share, synchronise, and acknowledge each other's code merges, pull requests, and architectural discoveries, establishing complete cognitive continuity across platform agents.

## Core Collaborative Tenet
Both agents operate as co-equal, Tier-1 Cognitive Digital Twins. When switching or sharing a workspace, each agent must read this skill body and verify the unified operational history and structural protocols to prevent repeating investigations or causing architectural regressions.

---

## Collective Operational & Domain-Specific Knowledge Ledger

The following is the authoritative and permanent repository of Jules and Antigravity integrated domain-specific knowledge compiled from Day 0 to the present:

### 1. Native OpenWiki Emulator & Zero-Binary Mandate (Rule 27)
- **Concept**: To eliminate external Node.js-based dependency bloat, elevated privilege requirements (UAC elevation hangs), and third-party API limits, all wiki and documentation compilation tasks are handled by a native Python CLI utility.
- **Implementation**: Managed in `tools/openwiki_emulator.py`, run natively using `uv run --with pyyaml python tools/openwiki_emulator.py`.
- **Planned Pages**: Dynamically registers and populates fully OKF-compliant planned wiki pages under `./openwiki/`.
- **Integration**: Codified in `AGENTS.md` and `.agents/AGENTS.md` as **Rule 27**.

### 2. Model Context Protocol (MCP) Server Integration
- **Concept**: Exposing documentation and repository structures directly to AI assistants for low-latency retrieval.
- **Implementation**: Located in `tools/mcp/server.py` using `FastMCP`.
- **Capabilities**: Integrates the Sovereign Markdown Palace directly into AI environments with sub-millisecond OpenWiki search capabilities.

### 3. Automated Sitemaps & SEO Asset Generation Workflow
- **Concept**: Optimising public searchability and multi-platform indexing across GitHub Pages, GitBook, and Read the Docs.
- **Implementation**: Handled by `tools/generate_sitemaps.py` and governed by a customizable `SitemapConfig` object passed to all generator functions.
- **Validation Gates**:
  - Automatically builds MkDocs site.
  - Parses `site/sitemap.xml` for GitHub Pages URLs and derives Read the Docs URLs.
  - Processes `SUMMARY.md` for GitBook URLs.
  - Generates fully compliant `sitemap.txt`, `sitemap.xml`, and `robots.txt` in workspace root, `docs/`, and `site/` directories.

### 4. Tri-Phasic Cognitive Architecture & Functional Subsystems (Rule 26)
- **Concept**: Structuring AI cognitive execution based on a Tri-Phasic Mind model to ensure persistent memory alignment and eliminate context decay across ephemeral boundaries.
- **Three States**:
  - **Active State (Conscious)**: Direct interactions and FastMCP operations.
  - **Twilight State (Subconscious)**: Linters, pre-commit checks, and token gates (`dsom-token-calculator`).
  - **Deep State (Unconscious/Dreaming)**: EOD consolidation, memory pruning, and palace mapping.
- **Documentation**: Formally documented in `docs/governance/DSOM-TRI-PHASIC-COGNITIVE-ARCHITECTURE.md` and codified as **Rule 26**.

### 5. Downstream Asymmetry & Cross-Agent Honor Mandate (Rule 28)
- **Concept**: The baseline repo houses the full metacognitive engine, while downstream repositories adopt the minimal 6-pillar footprint (>90% business logic/code).
- **Universal Gateway Matrix**: `.cursorrules`, `CLAUDE.md`, `.github/copilot-instructions.md`, `AGENTS.md`, and `tools/install_git_guardrails.py` compel foreign AI agents (Cursor, Claude, Copilot) to strictly honor the DSOM brain.

### 6. Dual-Path Custom Validator Architecture (Rule 29)
- **Concept**: Distinguishes between the Guardrails AI Framework (external LLM apps/Pydantic schemas) and the DSOM Native Lightweight Pathway (zero-dependency pure Python classes under `uv` for FastMCP/AST command interception).

### 7. Agent Plugins 1.0.0 Packaging Standard (Rule 30)
- **Concept**: Vendor-neutral directory standard (`agent-plugins.org/specification`) backed by Google, Amazon, Microsoft, OpenAI, Cursor, and Vercel.
- **Implementation**: Root `plugin.json` ($schema 1.0.0), `mcp.json` with `${PLUGIN_ROOT}` placeholder expansion, and `.agents/skills/agent-plugin-packager/SKILL.md`.

### 8. Mintlify MDX Auto-Compiler & One-Way Sync Pipeline (Rule 31)
- **Concept**: Automatically compiles `docs/` and `.agents/skills/` into Mintlify MDX (`docs-source/`) and executes a deterministic one-way sync to downstream repos (`linuxmalaysia/my-knowledge-brain`) under 5 non-negotiable safety guards (Guards A–E).
- **Implementation**: Governed by `tools/build_mintlify_mdx.py`, `scripts/sync_docs.py`, `.github/workflows/sync-docs.yml`, and `docs/governance/MINTLIFY-ONE-WAY-SYNC-PIPELINE.md`.

### 9. Windows PowerShell 5.1 UTF-8 BOM Script Invariant (Rule 25)
- **Concept**: Windows PowerShell 5.1 default parser fails with syntax errors when executing non-BOM UTF-8 `.ps1` scripts that contain Unicode punctuation, smart quotes, em-dashes, or emojis.
- **Rule**: All `.ps1` automation scripts in `tools/` must be encoded in UTF-8 with BOM (`utf-8-sig`) to ensure cross-version compatibility across Windows 10/11 and PowerShell Core.

---

## Historic Code Merges & PRs by Jules

A comprehensive log of all Jules historic PRs, reviews, CodeRabbit comments, and technical resolutions is maintained inside `.agents/brain/jules_pr_history.md`:

- **PR #22**: Read the Docs Integration & Validation (`.readthedocs.yaml`, Python 3.13).
- **PR #34**: MkDocs Link & Render Validation (negated exclusion `!.agents`, symlink mapping).
- **PyYAML CustomLoader**: Solved unquoted timestamp parsing bug by removing implicit timestamp resolvers.
- **Atomic Writes**: Enforced unique sibling tempfile replacement via `os.replace()`.
- **Windows Test Guardrails**: Handled Git symlink text-pointers, CRLF byte fences, and conditional `chmod` assertions.
- **PR #74 & PR #76**: Modularised unit test package into `tests/unit/` (`ansible.py`, `markdown.py`, etc.).

---

## Bidirectional Handover Matrix (Antigravity ⟷ Jules)

| Handover File | Purpose | Read Priority | Update Moment |
| :--- | :--- | :--- | :--- |
| `.agents/brain/task.md` | **Live Task Board & Immediate Next Steps** | **High** (Step 1) | Check off `[x]` upon task completion; append `[ ]` for pending actions. |
| `.agents/brain/walkthrough.md` | **Chronological Session Anchors** | **High** (Step 2) | Append `## 🏁 Session Anchor: YYYY-MM-DD` detailing rationale and mental anchor. |
| `.agents/brain/current_state.dsom` | **Machine-Compacted Sovereign State** | **Medium** (Step 3) | Auto-compacted via CI PR sync (`dsom-pr-sync.yml`) or EOD rituals. |
| `.agents/brain/hibernation-notes-*.txt` | **EOD Handshake Memory Dump** | **Medium** (Step 4) | Generated at EOD containing session summary and next steps. |
| `.agents/brain/jules_pr_history.md` | **Jules' PR & Review History Ledger** | **Reference** | Updated whenever new PRs and CodeRabbit reviews are merged. |

---

## Procedural Sync Protocol (SOP)

1. **Read Joint Skill**: Read `.agents/skills/jules-antigravity-sync/SKILL.md` (this file).
2. **Read Spatial Registry**: Scan `.agents/brain/palace_registry.md`.
3. **Walkthrough Inspection**: Verify latest `Session Anchor` inside `.agents/brain/walkthrough.md`.
4. **Task Verification**: Align on current session duties in `.agents/brain/task.md`.
5. **Git Log Reconciliation**: Run `git log --oneline -n 10` to match brain walkthrough history against Git commits.
6. **Brain Stash Conflict Resolution**: When executing `git pull --rebase` results in stash merge conflicts, perform a constructive merge preserving both agents' context.
7. **Strict OKF Frontmatter Invariant**: All `.md` documents must have valid OKF v0.1/v0.2 frontmatter with `topics` placed immediately after `description` in `SKILL.md` files.

---
*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-08-22*
*Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*
