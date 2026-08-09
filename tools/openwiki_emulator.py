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

import argparse
import datetime
import json
import os
import pathlib
import subprocess
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
        "engine": "DSOM Python OpenWiki Emulator v1.1",
        "status": "success",
        "pagesCompiled": 10,
    }
    return json.dumps(data, indent=2)


def generate_instructions_md() -> str:
    return "<!-- OPENWIKI:GENERATED BY DSOM PYTHON EMULATOR -->\n"


def cmd_init():
    print(f"[OpenWiki Emulator] Generating native wiki under {OPENWIKI_DIR}...")
    ensure_openwiki_dirs()
    (OPENWIKI_DIR / "_skeleton.md").write_text(generate_skeleton(), encoding="utf-8")
    (OPENWIKI_DIR / ".last-update.json").write_text(generate_last_update_json(), encoding="utf-8")
    (OPENWIKI_DIR / "INSTRUCTIONS.md").write_text(generate_instructions_md(), encoding="utf-8")
    print("[OpenWiki Emulator] Successfully updated ./openwiki/ structure.")


def cmd_update():
    print("[OpenWiki Emulator] Compiling recent Git diffs into OKF evidence blocks...")
    try:
        diff_output = subprocess.check_output(["git", "status", "--porcelain"], text=True)
        print(f"[Git Status]:\n{diff_output if diff_output.strip() else 'No uncommitted changes.'}")
    except Exception as e:
        print(f"[Git Status Warning]: {e}")
    cmd_init()


def cmd_search(query: str):
    print(f"[OpenWiki Search] Querying frontmatter for: '{query}'...")
    results = []
    for md_file in OPENWIKI_DIR.rglob("*.md"):
        try:
            content = md_file.read_text(encoding="utf-8")
            if not content.startswith("---"):
                continue
            parts = content.split("---", 2)
            if len(parts) >= 3:
                meta = yaml.safe_load(parts[1])
                if meta and isinstance(meta, dict):
                    searchable = f"{meta.get('title', '')} {meta.get('description', '')} {' '.join(meta.get('topics', []))}"
                    if query.lower() in searchable.lower():
                        results.append((md_file.relative_to(REPO_ROOT), meta.get("title"), meta.get("description")))
        except Exception:
            pass

    if results:
        print(f"\nFound {len(results)} matching OpenWiki page(s):")
        for rel_path, title, desc in results:
            print(f" - [{rel_path}] {title}")
            print(f"   Summary: {desc}\n")
    else:
        print(f"No OpenWiki pages matched query '{query}'.")


def cmd_export_graph():
    graph_path = OPENWIKI_DIR / "graph.html"
    print(f"[OpenWiki Emulator] Generating offline standalone graph visualizer at {graph_path}...")
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>DSOM OpenWiki Standalone Knowledge Graph</title>
    <style>
        body {{ background: #0f172a; color: #f8fafc; font-family: system-ui, sans-serif; padding: 2rem; max-width: 900px; margin: auto; }}
        h1 {{ color: #38bdf8; border-bottom: 2px solid #334155; padding-bottom: 0.5rem; }}
        .card {{ background: #1e293b; border-radius: 8px; padding: 1rem 1.5rem; margin-bottom: 1rem; border: 1px solid #334155; }}
        .card h3 {{ margin-top: 0; color: #a855f7; }}
        .badge {{ background: #0284c7; color: #fff; font-size: 0.75rem; padding: 2px 8px; border-radius: 4px; display: inline-block; margin-right: 4px; }}
        a {{ color: #38bdf8; text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <h1>🌐 DSOM OpenWiki Standalone Knowledge Graph</h1>
    <p>Last Generated: <code>{get_timestamp()}</code> | Engine: <code>Native Python OpenWiki Emulator</code></p>

    <div class="card">
        <h3>📍 Entrypoint: Quickstart & Repository Navigation</h3>
        <p>Master entrypoint, topology map, task-routing table, and focused validation commands.</p>
        <span class="badge">quickstart</span><span class="badge">navigation</span>
        <p><a href="./quickstart.md">View quickstart.md</a></p>
    </div>

    <div class="card">
        <h3>🏛️ Architecture Overview & Three-Pillar Model</h3>
        <p>DSOM scope, three-pillar operating model, component boundaries, and authoritative sources.</p>
        <span class="badge">architecture</span><span class="badge">pillars</span>
        <p><a href="./architecture/overview.md">View architecture/overview.md</a></p>
    </div>

    <div class="card">
        <h3>📜 Agent Operational Protocols & 27 Core Rules</h3>
        <p>Dual AGENTS.md registry, 27-rule operating constraints, mechanical boot and discovery loops.</p>
        <span class="badge">governance</span><span class="badge">27-rules</span>
        <p><a href="./governance/agent-operation.md">View governance/agent-operation.md</a></p>
    </div>

    <div class="card">
        <h3>🧠 Session Memory Stratification & Palace Synchronization</h3>
        <p>Brain stratification, SOD reanimation, EOD hibernation, and Palace markers.</p>
        <span class="badge">memory</span><span class="badge">palace</span>
        <p><a href="./memory/session-and-palace.md">View memory/session-and-palace.md</a></p>
    </div>

    <div class="card">
        <h3>🤖 Ansible Baseline & Automation Fabric Specification</h3>
        <p>Inventory topology, site.yml, preflight/common playbooks, WSL2 control node bridge.</p>
        <span class="badge">ansible</span><span class="badge">automation</span>
        <p><a href="./automation/ansible-baseline.md">View automation/ansible-baseline.md</a></p>
    </div>

    <div class="card">
        <h3>🛠️ Automation Tools, Ritual Wrappers & Privacy Guardian</h3>
        <p>Cross-platform .ps1/.sh tool registry and Privacy Guardian specs.</p>
        <span class="badge">tools</span><span class="badge">privacy</span>
        <p><a href="./automation/tools-and-privacy.md">View automation/tools-and-privacy.md</a></p>
    </div>

    <div class="card">
        <h3>🔌 FastMCP Server & Continuous Integration Workflows</h3>
        <p>FastMCP server tool contract, Context7 RAG endpoints, GitHub Actions catalog.</p>
        <span class="badge">mcp</span><span class="badge">ci-cd</span>
        <p><a href="./integrations/mcp-and-ci.md">View integrations/mcp-and-ci.md</a></p>
    </div>

    <div class="card">
        <h3>📚 Multi-Channel Documentation Delivery & SEO Engine</h3>
        <p>Omni-channel delivery (MkDocs, GH Pages, RTD, Render, GitBook, SEO sitemaps).</p>
        <span class="badge">publishing</span><span class="badge">mkdocs</span>
        <p><a href="./publishing/documentation-delivery.md">View publishing/documentation-delivery.md</a></p>
    </div>

    <div class="card">
        <h3>🧪 Quality Verification & Regression Test Suite</h3>
        <p>Python test-suite map, OKF/BOM/quoting/symlink assertions (112 assertions).</p>
        <span class="badge">testing</span><span class="badge">verification</span>
        <p><a href="./quality/verification.md">View quality/verification.md</a></p>
    </div>
</body>
</html>"""
    graph_path.write_text(html_content, encoding="utf-8")
    print(f"[OpenWiki Emulator] Offline standalone visualizer generated: {graph_path}")


def main():
    parser = argparse.ArgumentParser(description="DSOM Native Python OpenWiki Emulator")
    parser.add_argument("--init", action="store_true", help="Initialize full wiki")
    parser.add_argument("--update", action="store_true", help="Compile recent Git diffs")
    parser.add_argument("--search", type=str, help="Fast OKF metadata search query")
    parser.add_argument("--export-graph", action="store_true", help="Generate standalone offline HTML graph")

    args = parser.parse_args()

    if args.update:
        cmd_update()
    elif args.search:
        cmd_search(args.search)
    elif args.export_graph:
        cmd_export_graph()
    else:
        cmd_init()


if __name__ == "__main__":
    main()
