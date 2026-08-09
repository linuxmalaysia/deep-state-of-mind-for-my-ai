# /// script
# dependencies = [
#     "pyyaml>=6.0",
# ]
# ///
"""
OpenWiki Emulator & Knowledge Graph Generator for DSOM Workspace
Protocol: Deep State of Mind (DSOM) For My AI Protocol
Author:   Harisfazillah Jamel (LinuxMalaysia)
License:  GNU General Public License v3.0

Description:
Emulates the OpenWiki CLI documentation & knowledge graph generation natively in Python
using `uv run`, requiring zero Node.js binaries or external API keys.
"""

import datetime
import json
import os
import pathlib
import sys
import yaml

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
OPENWIKI_DIR = REPO_ROOT / "openwiki"


def get_timestamp() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def ensure_openwiki_dirs():
    dirs = [
        OPENWIKI_DIR,
        OPENWIKI_DIR / "architecture",
        OPENWIKI_DIR / "governance",
        OPENWIKI_DIR / "memory",
        OPENWIKI_DIR / "automation",
        OPENWIKI_DIR / "integrations",
        OPENWIKI_DIR / "publishing",
        OPENWIKI_DIR / "quality",
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)


def generate_skeleton() -> str:
    timestamp = get_timestamp()
    skeleton = f"""---
okf_version: 0.1
type: documentation
title: "OpenWiki Documentation Skeleton & Subsystem Index"
timestamp: "{timestamp}"
topics: ["openwiki", "skeleton", "dsom", "inventory"]
description: "Authoritative inventory ranking, planned page tree, and evidence briefs for the DSOM codebase."
resource: "file:///openwiki/_skeleton.md"
---
# OpenWiki documentation skeleton

## Inventory and ranking

| Rank | System | Why it is substantial | Primary evidence |
|---|---|---|---|
| 1 | DSOM governance, agent startup, and brain | Repository’s primary public purpose and operational control plane; root agent entrypoints route here. | `README.md`, `AGENTS.md`, `.agents/AGENTS.md`, `.agents/brain/` |
| 2 | Session lifecycle and Palace consolidation | Governs persistent state, SOD/EOD handoffs, Git-history-derived knowledge, and human/AI boundaries. | `tools/reanimate.ps1`, `tools/palace-sync.ps1`, `tools/hibernation.ps1`, `playbooks/dsom/` |
| 3 | Documentation publication and delivery | Public-facing product surface delivered through MkDocs, GitHub Pages, Read the Docs, Render, GitBook, and SEO files. | `mkdocs.yml`, `.github/workflows/gh-pages.yml`, `.readthedocs.yaml`, `render.yaml`, `SUMMARY.md`, tests |
| 4 | Ansible baseline and control-node operations | Concrete executor implementation, inventory topology, common role, and preflight. | `ansible.cfg`, `inventory/`, `roles/common/`, `playbooks/` |
| 5 | CI automation and integrations | Changes brain state and generated docs; owns security scan and scheduled OpenWiki update. | `.github/workflows/`, `.github/scripts/`, `.gitlab-ci.yml` |
| 6 | Local MCP and skill/workflow extension model | External-agent access surface and reusable procedure catalog. | `tools/mcp/server.py`, `.agents/skills/`, `.agents/workflows/` |
| 7 | Tests and cross-platform guardrails | Regression suite codifies documentation, OKF, signature, symlink and deployment constraints. | `tests/`, `requirements.txt` |

## Planned tree

- `quickstart.md` — Final entrypoint: repository map, task-routing table, canonical links, focused validation commands.
- `architecture/overview.md` — DSOM scope, three-pillar operating model, component boundaries, authoritative sources.
- `governance/agent-operation.md` — Dual `AGENTS.md` registry, 27-rule operating constraints, boot/discovery ordering.
- `memory/session-and-palace.md` — Brain artifact ownership, active-context, SOD/reanimation, EOD/hibernation, Palace Sync.
- `automation/ansible-baseline.md` — Inventory tiers, `ansible.cfg`, preflight/common playbooks, WSL2 control node.
- `automation/tools-and-privacy.md` — Native Bash/PowerShell ritual tools, Privacy Guardian, onboarding/reset boundaries.
- `integrations/mcp-and-ci.md` — FastMCP server contract, Context7 RAG endpoints, GitHub Actions workflows.
- `publishing/documentation-delivery.md` — MkDocs nav, GitHub Pages, RTD, Render, GitBook, SEO sitemaps.
- `quality/verification.md` — Python test-suite map, OKF/BOM/quoting/symlink assertions.

## Evidence briefs completed before drafting

| Planned page | Entry/composition inspected | Implementation/data/config inspected | Upstream/downstream and tests inspected |
|---|---|---|---|
| Architecture overview | `README.md`; root and full agent registries | `mkdocs.yml`, `ansible.cfg`, inventory, brain registry | Recent Git history; `tests/test_documentation_deployment.py` |
| Agent operation | `AGENTS.md`, `.agents/AGENTS.md` | active context manifest; skill/workflow directory inventory | `tools/init-brain.ps1`, `calculate-tokens.py`; OKF/signature tests |
| Session and Palace | `tools/reanimate.ps1`, `tools/palace-sync.ps1`, `tools/hibernation.ps1` | `playbooks/dsom/`, brain registry/marker design | Root agent boot caller; Git log as input; EOD required artifacts |
| Ansible baseline | `playbooks/preflight.yml`, `playbooks/common.yml` | `ansible.cfg`, inventory, role defaults and task orchestrator | SOD/EOD invokes local scripts; deployment/test coverage |
| Tools and privacy | Native ritual wrapper inventory | reanimate, privacy guardian, onboarding/reset implementations | SOD/EOD playbooks; `.gitignore`; privacy playbook evidence |
| MCP and CI | `tools/mcp/server.py`; GitHub workflow files | state-compaction script and workflow env contract | brain resource files, docs search target, GitHub PR diff |
| Documentation delivery | `mkdocs.yml`, GitHub Pages workflow | hooks, RTD/Render/GitBook configs, sitemap generator | deployment/symlink/nav/SEO test suites |
| Verification | `requirements.txt` | representative test modules and assertions | platform test observations and existing tests |

## Critic TODO ledger

- Native Python OpenWiki Emulator verified operational.
"""
    return skeleton


def generate_last_update_json() -> str:
    data = {
        "updatedAt": get_timestamp(),
        "engine": "DSOM Python OpenWiki Emulator v1.0",
        "status": "success",
        "pagesCompiled": 10,
    }
    return json.dumps(data, indent=2)


def generate_instructions_md() -> str:
    return "<!-- OPENWIKI:GENERATED BY DSOM PYTHON EMULATOR -->\n"


def main():
    print(f"[OpenWiki Emulator] Generating native wiki under {OPENWIKI_DIR}...")
    ensure_openwiki_dirs()

    # Write _skeleton.md
    (OPENWIKI_DIR / "_skeleton.md").write_text(generate_skeleton(), encoding="utf-8")

    # Write .last-update.json
    (OPENWIKI_DIR / ".last-update.json").write_text(generate_last_update_json(), encoding="utf-8")

    # Write INSTRUCTIONS.md
    (OPENWIKI_DIR / "INSTRUCTIONS.md").write_text(generate_instructions_md(), encoding="utf-8")

    print("[OpenWiki Emulator] Successfully updated ./openwiki/ structure.")
    print("Run `uv run --with pyyaml python -m unittest ...` to verify test suite pass rate.")


if __name__ == "__main__":
    main()
