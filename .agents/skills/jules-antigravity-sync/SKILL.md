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

**Purpose**: To enable Google Jules and Google Antigravity to share, synchronise, and acknowledge each other's code merges, pull requests, and architectural discoveries, establishing complete cognitive continuity across platform agents.

## Core Collaborative Tenet
Both agents operate as co-equal, Tier-1 Cognitive Digital Twins. When switching or sharing a workspace, each agent must read this skill body and verify the unified operational history and structural protocols to prevent repeating investigations or causing architectural regressions.

---

## Collective Operational & Domain-Specific Knowledge Ledger

The following is the authoritative and permanent repository of Jules and Antigravity integrated domain-specific knowledge compiled from Day 0 to the present:

### 1. Native OpenWiki Emulator & Zero-Binary Mandate (Rule 27)
- **Concept**: To eliminate external Node.js-based dependency bloat, elevated privilege requirements (UAC elevation hangs), and third-party API limits, all wiki and documentation compilation tasks are handled by a native Python CLI utility.
- **Implementation**: Managed in `tools/openwiki_emulator.py`, which is run natively using `uv run --with pyyaml python tools/openwiki_emulator.py`.
- **Planned Pages**: The emulator dynamically registers and populates nine fully OKF v0.1 compliant planned wiki pages under `./openwiki/` (such as `quickstart.md`, `architecture/overview.md`, etc.).
- **Integration**: Codified in `AGENTS.md` and `.agents/AGENTS.md` as **Rule 27**.

### 2. Model Context Protocol (MCP) Server Integration
- **Concept**: Exposing the documentation and repository structures directly to AI assistants for low-latency retrieval.
- **Implementation**: Located in `tools/mcp/server.py` using `FastMCP`.
- **Capabilities**: Integrates the Sovereign Markdown Palace directly into AI environments, with built-in sub-millisecond OpenWiki search capabilities for context assembly.

### 3. Automated Sitemaps & SEO Asset Generation Workflow
- **Concept**: Optimising public searchability and multi-platform indexing across GitHub Pages, GitBook, and Read the Docs.
- **Implementation**: Handled by `tools/generate_sitemaps.py` and governed by a customizable `SitemapConfig` object passed to all generator functions.
- **Validation Gates**:
  - Automatically builds the MkDocs site.
  - Parses `site/sitemap.xml` for GitHub Pages URLs and derives Read the Docs URLs.
  - Processes `SUMMARY.md` for GitBook URLs.
  - Strictly filters out internal directories (such as `.agents/`).
  - Performs defensive file verification to raise `FileNotFoundError` with full path context if any target file listed in `SUMMARY.md` does not exist or is not a regular file.
  - Generates fully compliant `sitemap.txt`, `sitemap.xml`, and `robots.txt` in the workspace root, `docs/`, and `site/` directories.

### 4. Tri-Phasic Cognitive Architecture & Functional Subsystems (Rule 26)
- **Concept**: Structuring the AI's cognitive execution based on a Tri-Phasic Mind model to ensure persistent memory alignment and eliminate context decay across ephemeral boundaries.
- **Three States**:
  - **Active State (Conscious)**: Handles direct interactions and high-frequency tool calls (e.g., FastMCP).
  - **Twilight State (Subconscious)**: Exercises static analysis, linters, and pre-commit checks.
  - **Deep State (Unconscious/Dreaming)**: Handles EOD consolidation, memory pruning, and palace mapping.
- **Subsystems**:
  1. Cognitive Architecture
  2. Memory Stratification
  3. Dreaming & Consolidation
  4. Metacognition & Guardrails
- **Documentation**: Formally documented in the official blueprint `docs/governance/DSOM-TRI-PHASIC-COGNITIVE-ARCHITECTURE.md` and codified as **Rule 26** in both `AGENTS.md` files.

### 5. Jules & Antigravity Collaborative Knowledge & Sync (Rule 25)
- **Concept**: Establishing Google Antigravity as a peer Tier-1 AI agent companion with Google Jules under the DSOM framework to guarantee cognitive continuity and peer state synchronization.
- **Implementation**: Governed by **Rule 25** and tracked via this dedicated sync skill file (`.agents/skills/jules-antigravity-sync/SKILL.md`).

### 6. SKILL.md Frontmatter topics Position Rule
- **Concept**: Ensuring clean indexing and fast semantic grep routing without loading full file bodies.
- **Rule**: In all `SKILL.md` files processed by compliance tools (e.g., `apply_okf.py`, `apply_okf_frontmatter.py`, and `tools/refactor_okf.py`), the `topics` field is placed immediately after the `description` field.

---

## Historic Code Merges & PRs by Jules

The following is the permanent ledger of PRs and code modifications executed by Google Jules. A comprehensive, high-fidelity log of all Jules' historic PRs, reviews, CodeRabbit comments, and technical resolutions is maintained inside `.agents/brain/jules_pr_history.md`.

### 1. Read the Docs Integration & Validation (PR #22)

- **Accomplishment**: Configured `.readthedocs.yaml` at the root with Ubuntu 24.04, Python 3.13, and MkDocs. Appended standard DSOM license/ownership headers and synced all ledgers.
- **Testing Layer**: Created `tests/test_readthedocs_config.py` and `tests/test_readthedocs_ledger_sync.py` to assert RTD and GitBook configuration compliance.

### 2. MkDocs Link & Render Validation (PR #34)
- **Accomplishment**: Solved critical compilation warnings during Render.com site builds. Negated the exclusion of the `.agents/` folder using `exclude_docs: | \n !.agents` and mapped root-level folders (`.agents/`, `playbooks/`) as symlinks inside `docs/` to allow MkDocs to discover and compile them.
- **Testing Layer**: Implemented `tests/test_documentation_deployment.py` to assert publishing endpoints.

### 3. PyYAML CustomLoader Parser Improvement
- **Accomplishment**: Solved the "Unquoted Timestamp Parsing Bug" by introducing `CustomLoader` (a customized SafeLoader variant) inside `tools/apply_okf_frontmatter.py` and other compliance scripts. This bypasses PyYAML's default implicit timestamp resolver to preserve raw, unquoted timestamps as exact string types.

### 4. Secure Sibling Atomic File Replacement
- **Accomplishment**: Bypassed direct file overrides with a secure write procedure. The compliance tools write changes to a unique sibling temporary file via `tempfile.NamedTemporaryFile` and replace the target path using `os.replace()` only after a successful write.

### 5. Compliance Verification Suite Expansion
- **Accomplishment**: Extended `tests/test_okf_frontmatter_bom_reorder.py` and quoting validation suites to dynamically discover and verify all markdown files in the repository, guaranteeing a strict BOM-less frontmatter beginning at line 1, column 1.

### 6. Windows Git-Symlink & CRLF Test Guardrails
- **Accomplishment**: Enhanced test discovery suites (`tests/test_okf_frontmatter_bom_reorder.py`, `tests/test_okf_quoting.py`, `tests/test_docs_symlinks.py`) to detect Git text-pointer symlinks (`content.startswith("../")`) on Windows native checkouts, handle CRLF byte fences (`b"---\r\n"`), and conditionally scope POSIX `chmod` bit assertions (`if os.name != "nt":`).

### 7. Google Jules PR & Comment History Ledger

- **Accomplishment**: Created the master conversational and code merge ledger `.agents/brain/jules_pr_history.md` detailing PRs #22, #23, #24, #25, #26, #27, and #34, as well as automated CodeRabbit review integration and feedback cycles.

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
