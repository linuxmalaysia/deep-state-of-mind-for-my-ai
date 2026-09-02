---
okf_version: 0.1
type: agent_skill
title: "🔍 Documentation Review Skill"
timestamp: "2026-09-02T12:00:00Z"
description: "Facilitates systematic review of documentation changes, pull requests, and diffs to protect the source of truth and ensure compliance with writing standards."
topics: ["documentation", "review", "quality-assurance", "style-guide", "dsom"]
name: docs-review
---
# 🔍 Documentation Review Skill (`docs-review`)

## Purpose

The `docs-review` skill facilitates systematic review of documentation changes, pull requests, files, and diffs to ensure accuracy, completeness, maintainability, and style guide compliance. It protects the source of truth by comparing documentation claims against actual code, CLI flags, API schemas, and test outputs.

---

## Core Philosophy: Protect the Source of Truth

Documentation review is distinct from copy editing. While copy editing refines wording, documentation review verifies that:
- Instructions are true, tested, and complete.
- UI labels, CLI flags, and API endpoints match actual implementations.
- Troubleshooting steps address the most probable failure modes.
- Outdated or contradicted documentation is flagged for pruning.

---

## Review Modes

Check available tooling to determine the execution mode:
1. **Pull Request Review Mode**: Activated when GitHub API PR review tools (e.g. `mcp__github__create_pending_pull_request_review`) are available.
2. **Local Review Mode**: Uses standard read and search tools (`Read`, `Grep`, `Bash`, `Glob`) to evaluate local files or Git diffs.

---

## Categorisation & Severity Protocol

All feedback items must be categorised and numbered sequentially starting from **Issue 1**:

| Severity Tier | Description | Action |
|:---|:---|:---|
| **Incorrect** | Broken commands, inaccurate parameters, or invalid links. | Mandatory blocker. Must be fixed. |
| **Missing** | Omitted prerequisites, missing error cases, or undocumented flags. | High priority addition. |
| **Outdated** | Deprecated options or references to removed features. | Prune or update immediately. |
| **Confusing** | Ambiguous phrasing or unclear procedural steps. | Request clarification or rewrite. |
| **Style-Only** | Minor typos, grammar tweaks, or formatting adjustments. | Optional recommendation. |

*Note*: Skip flagging trivial style items if they make no material difference to reader comprehension.

---

## Review Checklist

- [ ] **Truth & Accuracy**: Do CLI commands, code samples, and API endpoints execute without error?
- [ ] **Completeness**: Are prerequisites, edge cases, and failure modes explicitly listed?
- [ ] **Structure**: Is the document mapped cleanly to a Diátaxis quadrant (Tutorial, How-To, Reference, Explanation)?
- [ ] **Formatting & Compliance**: Does the file contain OKF YAML frontmatter and pass linting (MD022/MD031)?

---
*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-09-02*
*Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*
