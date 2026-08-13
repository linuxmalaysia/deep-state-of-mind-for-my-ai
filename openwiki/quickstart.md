---
okf_version: "0.1"
type: "documentation"
title: "OpenWiki Quickstart & Repository Navigation Map"
timestamp: "2026-08-13T14:19:24Z"
topics: ["openwiki", "quickstart", "navigation", "dsom"]
description: "Master entrypoint containing repository map, task-routing table, canonical links, and focused validation commands."
---
# OpenWiki Quickstart & Repository Navigation Map

Welcome to the **Sovereign OpenWiki Quickstart**. This document serves as the master entrypoint and topology guide for both humans and AI agents navigating the Deep State of Mind (DSOM) framework.

## 🏛️ Repository Navigation Map

The workspace is organised into three distinct operational planes:

1. **Governance & Persona (The Constitution):**
   - `AGENTS.md` (Root) — High-level sovereign entrypoint.
   - `.agents/AGENTS.md` — Complete constitutional rulebook (27 core rules).
   - `START-HERE.md` — Onboarding map outlining 12 distinct entry points.

2. **Spatial Memory & State (The Palace):**
   - `.agents/brain/` — Real-time persistent state logs (`task.md`, `walkthrough.md`).
   - `.agents/brain/palace_registry.md` — Spatial index of the Sovereign Markdown Palace.
   - `docs/` — Human-readable compiled documentation rooms.

3. **Execution & Automation (The Control Plane):**
   - `tools/` — Idempotent cross-platform Bash and PowerShell operational scripts.
   - `playbooks/` — Ansible configuration and system automation specs.
   - `tests/` — Comprehensive multi-platform regression test suite.

## 📋 Active Task Routing Table

When executing operational workflows, use the following routing table to locate instructions:

| Task Class | Instruction Location | Primary Executor |
| :--- | :--- | :--- |
| **Session Initialisation** | `docs/tools/HOWTO-REANIMATE.md` | `tools/reanimate.sh` |
| **Daily State Sync** | `docs/tools/HOWTO-SOD-PALACE.md` | `tools/sod-palace.sh` |
| **Security Scanning** | `docs/governance/GITHUB-ACTIONS-SECURITY-SCANNING.md` | Snyk GitHub Action |
| **Session Hibernation** | `docs/tools/HOWTO-HIBERNATION.md` | `tools/hibernation.sh` |

## 🧪 Focused Validation Commands

Validate workspace integrity and compliance at any time using these zero-binary commands:

```bash
# Execute local test suite
uv run --with pyyaml --with pytest --with mcp==1.2.1 --with fastmcp --with pydantic-settings pytest

# Initialise/Update the OpenWiki Knowledge Graph
uv run --with pyyaml python tools/openwiki_emulator.py --init
```

## 🔗 Canonical Links

- **GitHub Pages:** https://linuxmalaysia.github.io/deep-state-of-mind-for-my-ai/
- **GitBook Mirror:** https://malaysia-open-source-community.gitbook.io/deep-state-of-mind-dsom-protocol-for-my-ai
- **Read the Docs:** https://deep-state-of-mind-for-my-ai.readthedocs.io/en/latest/
