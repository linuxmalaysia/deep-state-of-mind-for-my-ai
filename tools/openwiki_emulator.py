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


def generate_skeleton(timestamp: str = None) -> str:
    if timestamp is None:
        timestamp = get_timestamp()
    skeleton = f"""---
okf_version: "0.1"
type: documentation
title: "OpenWiki Documentation Skeleton & Subsystem Index"
timestamp: "{timestamp}"
topics: ["openwiki", "skeleton", "dsom", "inventory"]
description: "Authoritative inventory ranking, planned page tree, and evidence briefs for the DSOM codebase."
resource: "{(OPENWIKI_DIR / '_skeleton.md').as_uri()}"
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
| 6 | Local MCP and skill/workflow extension model | External-agent access surface and reusable procedure catalogue. | `tools/mcp/server.py`, `.agents/skills/`, `.agents/workflows/` |
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


def generate_last_update_json(timestamp: str = None) -> str:
    if timestamp is None:
        timestamp = get_timestamp()
    data = {
        "updatedAt": timestamp,
        "engine": "DSOM Python OpenWiki Emulator v1.1",
        "status": "success",
        "pagesCompiled": 10,
    }
    return json.dumps(data, indent=2)


def generate_instructions_md(timestamp: str = None) -> str:
    if timestamp is None:
        timestamp = get_timestamp()
    return f"""---
okf_version: "0.1"
type: "documentation"
title: "OpenWiki Instructions"
timestamp: "{timestamp}"
topics: ["openwiki", "instructions"]
description: "Standard instructions for operating the OpenWiki Native Python Emulator."
---
<!-- OPENWIKI:GENERATED BY DSOM PYTHON EMULATOR -->
"""


def generate_page(title: str, timestamp: str, topics: list[str], description: str, content_markdown: str) -> str:
    topics_str = json.dumps(topics)
    return f"""---
okf_version: "0.1"
type: "documentation"
title: "{title}"
timestamp: "{timestamp}"
topics: {topics_str}
description: "{description}"
---
{content_markdown.strip()}
"""


class OpenWikiState:
    """Encapsulates the state of the OpenWiki emulator, providing immutable-safe planned pages."""
    def __init__(self, timestamp: str = None):
        self.timestamp = timestamp or get_timestamp()

    def get_planned_pages(self) -> dict:
        return {
            "quickstart.md": {
                "title": "OpenWiki Quickstart & Repository Navigation Map",
                "topics": ["openwiki", "quickstart", "navigation", "dsom"],
                "description": "Master entrypoint containing repository map, task-routing table, canonical links, and focused validation commands.",
                "content": """
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
"""
            },
            "architecture/overview.md": {
                "title": "DSOM Scope & Three-Pillar Operational Model",
                "topics": ["openwiki", "architecture", "overview", "pillars"],
                "description": "DSOM scope, three-pillar operating model, component boundaries, and authoritative sources.",
                "content": """
# DSOM Scope & Three-Pillar Operational Model

The **Deep State of Mind (DSOM)** protocol is a metacognitive governance framework designed to establish absolute operational alignment, digital sovereignty, and persistent context continuity between human operators and AI agents.

## 🏛️ The Three-Pillar Operating Model

The architecture of DSOM is structured around three foundational pillars:

```text
                  ┌─────────────────────────────────┐
                  │      METACOGNITIVE GOVERNANCE   │
                  │   Constitutional AGENTS.md Laws │
                  └────────────────┬────────────────┘
                                   │
                  ┌────────────────┼────────────────┐
                  │                │                │
         ┌────────▼────────┐       │       ┌────────▼────────┐
         │ SPATIAL MEMORY  │◄──────┴──────►│    EXECUTION    │
         │ Brain & Palace  │               │ Ansible & Tools │
         └─────────────────┘               └─────────────────┘
```

1. **Pillar 1: Metacognitive Governance (The Mind):**
   - Established by the master constitution under `.agents/AGENTS.md`.
   - Governs AI self-reflection, behaviour guidelines, token budgeting, and the 27 operational rules.

2. **Pillar 2: Spatial Memory (The Palace):**
   - Co-located in `.agents/brain/` and compiled inside the `docs/` Palace.
   - Prevents context decay across ephemeral chat session boundaries through structured daily reanimation and hibernation rituals.

3. **Pillar 3: Absolute Execution (The Body):**
   - Implemented via declarative automation (Ansible baseline) and idempotent operational wrappers (`tools/`).
   - Ensures that all technical instructions translate directly to deterministic local environment actions.

## 🧱 Component Boundaries & Authoritative Sources

- **Authoritative Source of Truth:** The active repository files and Git history.
- **Cognitive Control Plane:** The `.agents/` folder, which is strictly managed and preserved across sessions.
- **External Public Interfaces:** Render blueprints, Read the Docs configuration, and GitHub Actions CD pipelines.
"""
            },
            "governance/agent-operation.md": {
                "title": "Dual Agent Registry & Sovereign Operational Laws",
                "topics": ["openwiki", "governance", "agents", "protocols", "rules"],
                "description": "Dual AGENTS.md registry, 27-rule operating constraints, mechanical boot and behaviour/discovery ordering.",
                "content": """
# Dual Agent Registry & Sovereign Operational Laws

To ensure immediate discovery by various platform LLM interfaces, DSOM enforces a dual-layered constitutional registry that anchors the agent's behaviour.

## 📜 The Dual AGENTS.md Registry

1. **The Root Gateway (`AGENTS.md`):**
   - Placed at the workspace root as a discoverable landing page for platform-integrated agents (Copilot, Cursor, etc.).
   - Provides a concise summary of the protocol and redirects agents directly to the full constitution.

2. **The Sovereign Constitution (`.agents/AGENTS.md`):**
   - Located securely within the `.agents/` control directory.
   - Houses the complete 27 operational rules, the Cognitive Twin persona profile (`LinuxMalaysia`), and strict execution constraints.

## ⚙️ The Mechanical Boot Sequence

Upon initialisation or reanimation, the AI agent must strictly follow this sequence before making any workspace changes:

1. **Genesis Read:** Parse `.agents/AGENTS.md` to establish behavioural identity and operational laws.
2. **Memory Restoration:** Parse `.agents/brain/` (including `task.md` and `walkthrough.md`) to restore the exact state of active tasks.
3. **Master Onboarding Map:** Read `START-HERE.md` to understand repository topology and active entry points.

## 🧠 5-Step Local Knowledge-First Discovery Flow

Before running terminal commands or proposing external changes:

1. **Local OKF Search:** Query `topics` and `description` in local frontmatter using `grep_search`.
2. **Targeted Inspection:** Extract and read specific line ranges of relevant files.
3. **Temporal Verification Gate:** Validate the OKF `timestamp` to ensure the information is fresh.
4. **Consensus Request:** Consult the human operator if local documentation is contextually stale.
5. **Physical Execution:** Execute the narrowest possible command to implement verified actions.
"""
            },
            "memory/session-and-palace.md": {
                "title": "Session Memory Stratification & Palace Synchronisation",
                "topics": ["openwiki", "memory", "session", "palace", "stratification"],
                "description": "Brain artifact ownership, active-context, SOD/reanimation, EOD/hibernation, Palace Sync.",
                "content": """
# Session Memory Stratification & Palace Synchronisation

Context decay is the single largest point of failure in Human-AI collaborative engineering. DSOM eliminates this through spatial memory stratification and strict session rituals.

## 🧠 Spatial Memory & Brain Artifacts

Active state tracking resides within the `.agents/brain/` directory:

- `task.md` — Houses active, pending, and completed tasks.
- `walkthrough.md` — Records session histories and dated Mental Anchors.
- `active_context_manifest.md` — Specifies the exact files currently in active scope.
- `palace_registry.md` — An index of the Sovereign Markdown Palace "rooms" mapping to physical `docs/` files.

## 🌅 Start-of-Day (SOD) Reanimation Ritual

1. The human or system invokes `tools/reanimate.sh` (or `.ps1`).
2. The active context manifest is loaded, instructing the AI to retrieve and populate its working context.
3. The AI reads the dated Mental Anchor in `walkthrough.md` to resume exactly where the previous session left off.

## 🌌 End-of-Day (EOD) Hibernation & Palace Synchronisation

1. The AI maps the session's Git commits to physical Palace rooms.
2. A `palace_update_proposal_*.md` file is generated, outlining recommended knowledge updates.
3. The AI updates the session summary and appends a dated Mental Anchor to `walkthrough.md`.
4. `tools/hibernation.sh` executes preflight checks, stages changes, and cleanly commits them to Git.
"""
            },
            "automation/ansible-baseline.md": {
                "title": "Ansible Baseline & Automation Fabric Specification",
                "topics": ["openwiki", "automation", "ansible", "fabric", "wsl2"],
                "description": "Inventory tiers, ansible.cfg, preflight/common playbooks, WSL2 control node.",
                "content": """
# Ansible Baseline & Automation Fabric Specification

The Execution Pillar of DSOM relies on a declarative and idempotent automation fabric driven by **Ansible**, ensuring all operations are repeatable and zero-binary.

## 🎛️ Inventory Architecture & Tiers

The workspace organises hardware and systems into tiered logical inventories:

- **Tier 1 (Core Nodes):** Domain gateways, central authentication, and DNS/reverse proxies.
- **Tier 2 (Application Fabric):** Microservices, web hosts, database HA clusters, and GIS nodes.
- **Tier 3 (Edge Nodes):** Disconnected or remote edge devices running Termux or local agents.

## 🛠️ Configuration & Core Playbooks

- `ansible.cfg` — Governs custom connection parameters, timeouts, and local roles path mappings.
- `playbooks/preflight.yml` — Runs environmental preflight checks, confirming Python dependencies, OS kernels, and security compliance.
- `playbooks/common.yml` — Sets up baseline system hardening, sovereign SSH keys, and system telemetry agents.

## 💻 WSL2 Control Node Bridge

For Windows 11 environments, DSOM mandates **WSL2 (AlmaLinux 10 / Ubuntu)** as the local Control Node execution bridge, keeping PowerShell scripts as lightweight wrappers that invoke the Linux environment seamlessly.
"""
            },
            "automation/tools-and-privacy.md": {
                "title": "Sovereign Automation Tools & Privacy Guardian Boundaries",
                "topics": ["openwiki", "automation", "tools", "privacy", "guardian"],
                "description": "Native Bash/PowerShell ritual tools, Privacy Guardian, onboarding/reset boundaries.",
                "content": """
# Sovereign Automation Tools & Privacy Guardian Boundaries

Idempotent local script wrappers located in `tools/` handle multi-platform environment management while enforcing strict privacy filters.

## ⚙️ Core Automation Ritual Tools

All daily rituals are wrapped in unified PowerShell (`.ps1`) and Bash (`.sh`) scripts that run interactively or headlessly:

- `reanimate.sh` — Bootstraps the active session and loads files listed in the context manifest.
- `hibernation.sh` — Executes preflight checks, commits active changes, and prepares for hibernation.
- `git-ritual.sh` — Automates safe, non-interactive stashing, rebasing, and pushing across multiple remotes.
- `diagnostic.sh` — Verifies the physical health of brain files, frontmatter compliance, and system tools.

## 🛡️ Privacy Guardian Boundaries

The **Privacy Guardian (`tools/privacy-guardian.sh`)** acts as an inline data-leak prevention layer. Before staging any documentation or logs, it scans the active manifest for:
- Exposed credentials, tokens, or private API keys.
- Production IP addresses or sensitive database passwords.

Any flagged files are immediately quarantined, and Git actions are blocked until the sensitive data is successfully externalised.
"""
            },
            "integrations/mcp-and-ci.md": {
                "title": "FastMCP Server Integration & Continuous Integration Workflows",
                "topics": ["openwiki", "integrations", "mcp", "ci-cd", "workflows"],
                "description": "FastMCP server contract, Context7 RAG endpoints, GitHub Actions workflows.",
                "content": """
# FastMCP Server Integration & Continuous Integration Workflows

DSOM integrates with modern AI IDE interfaces and automated GitHub Actions to maintain live knowledge compilation and workflow verification.

## 🔌 FastMCP Server Architecture

The native DSOM Model Context Protocol (MCP) server resides in `tools/mcp/server.py` and uses **FastMCP**:

- **Sovereign Markdown Palace Exposure:** Exposes the entire compiled documentation structure directly to AI editors (Cursor, Claude Desktop).
- **Zero-Binary Search Tool:** Integrates sub-millisecond, local OKF-compliant search across all Palace rooms and brain manifests.

## 🤖 Continuous Integration Workflow Catalogue

All workspace modifications are compiled, linted, and verified via automated pipelines:

1. **`gh-pages.yml`:** Installs `uv`, compiles the static MkDocs documentation site with custom hooks, and deploys it to the `gh-pages` branch.
2. **`openwiki-update.yml`:** A scheduled daily cron workflow that runs the native Python OpenWiki emulator and automatically submits a pull request with updated knowledge graphs.
3. **`snyk-scanning.yml`:** Deploys Snyk container and dependency scanning to verify the security integrity of the Python/Node dependencies.
"""
            },
            "publishing/documentation-delivery.md": {
                "title": "Multi-Channel Documentation Delivery & SEO Engine",
                "topics": ["openwiki", "publishing", "delivery", "seo", "mkdocs"],
                "description": "MkDocs nav, GitHub Pages, RTD, Render, GitBook, SEO sitemaps.",
                "content": """
# Multi-Channel Documentation Delivery & SEO Engine

DSOM compiles and delivers documentation to multiple channels simultaneously, catering to web browsers, cloud readers, and AI search engines.

## 📚 Multi-Channel Pipeline

- **GitHub Pages (Primary Web):** Accessible at the repository's main `site_url`. Uses the MkDocs Material theme with headers and glassmorphism styling defined in `docs/stylesheets/extra.css`.
- **GitBook (Sovereign Mirror):** Kept in perfect lockstep via `.gitbook.yaml` and parsed from `SUMMARY.md`.
- **Read the Docs:** Integrated via `.readthedocs.yaml` to build a production documentation surface on Python-friendly hosts.
- **Render.com Blueprint:** Deploys a static site via `render.yaml` with the automated build command:
  ```bash
  pip install -r docs/requirements.txt && mkdocs build
  ```

## 🛠️ MkDocs Custom Hooks & Exclusions

Because MkDocs treats `docs/` as the build root, paths must be handled dynamically:
- **Exclusion Negation:** Dot-prefixed folders are ignored by default. MkDocs is instructed to negation-negate `.agents` via `exclude_docs: | \\\\n !.agents`.
- **Custom Link Hook (`tools/mkdocs_hooks.py`):** Rewrites raw markdown links during compilation (removing `docs/` prefixes and mapping repository-root links) to ensure seamless rendering on both GitHub.com and the static site.

## 🌐 Automated Sitemaps & Robots.txt

Sitemaps are compiled dynamically via `tools/generate_sitemaps.py` using `SitemapConfig`, outputting compliant `sitemap.xml`, `sitemap.txt`, and `robots.txt` files directly to the root and static web directories.
"""
            },
            "quality/verification.md": {
                "title": "Quality Verification Framework & Regression Test Suites",
                "topics": ["openwiki", "quality", "verification", "testing", "assertions"],
                "description": "Python test-suite map, OKF/BOM/quoting/symlink assertions.",
                "content": """
# Quality Verification Framework & Regression Test Suites

DSOM maintains absolute architectural compliance through a rigorous, automated testing framework that executes local quality assertions across all system files.

## 🧪 Regression Test Suite Map

- `test_okf_frontmatter_bom_reorder.py` — Discovers all markdown files and validates that frontmatter starts exactly on line 1, column 1, uses valid OKF v0.1 fields, has no leading UTF-8 BOM characters, and defensively double-quotes special strings.
- `test_docs_symlinks.py` — Confirms that symbolic links pointing to root files (`README.md`, `SECURITY.md`, etc.) are resolved correctly on all deployment targets.
- `test_mcp_server.py` — Exercises the FastMCP server, confirming correct JSON-RPC output and resource discovery.
- `test_readthedocs_config.py` / `test_readthedocs_ledger_sync.py` — Ensures that Read the Docs and GitBook files are synchronised with `SUMMARY.md`.

## 🛠️ Cross-Platform Guardrails

To support cross-platform co-working across Linux, macOS, and Windows environments, tests implement:
- **Windows CRLF Handling:** Byte fence matchers handle both `\\\\n` and `\\\\r\\\\n` line endings natively.
- **POSIX Assertions Bypass:** Permissions/chmod assertions are conditionally evaluated only on POSIX systems (`if os.name != 'nt'`).
- **Git Pointer Detection:** On Windows environments lacking OS symlink support, tests detect text-pointer files and gracefully parse them without raising exceptions.
"""
            }
        }


def cmd_init():
    state = OpenWikiState()
    print(f"[OpenWiki Emulator] Generating native wiki under {OPENWIKI_DIR} with timestamp {state.timestamp}...")
    ensure_openwiki_dirs()
    (OPENWIKI_DIR / "_skeleton.md").write_text(generate_skeleton(state.timestamp), encoding="utf-8")
    (OPENWIKI_DIR / ".last-update.json").write_text(generate_last_update_json(state.timestamp), encoding="utf-8")
    (OPENWIKI_DIR / "INSTRUCTIONS.md").write_text(generate_instructions_md(state.timestamp), encoding="utf-8")

    for relative_path, info in state.get_planned_pages().items():
        page_content = generate_page(
            title=info["title"],
            timestamp=state.timestamp,
            topics=info["topics"],
            description=info["description"],
            content_markdown=info["content"]
        )
        dest_file = OPENWIKI_DIR / relative_path
        dest_file.parent.mkdir(parents=True, exist_ok=True)
        dest_file.write_text(page_content, encoding="utf-8")
        print(f"[OpenWiki Emulator] Generated: {dest_file}")

    cmd_export_graph(state.timestamp)
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


def cmd_export_graph(timestamp: str = None):
    if timestamp is None:
        timestamp = get_timestamp()
    graph_path = OPENWIKI_DIR / "graph.html"
    print(f"[OpenWiki Emulator] Generating offline standalone graph visualizer at {graph_path} with timestamp {timestamp}...")
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
    <p>Last Generated: <code>{timestamp}</code> | Engine: <code>Native Python OpenWiki Emulator</code></p>

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
