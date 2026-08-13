---
okf_version: "0.1"
type: documentation
title: "OpenWiki Documentation Skeleton & Subsystem Index"
timestamp: "2026-08-13T20:31:31Z"
topics: ["openwiki", "skeleton", "dsom", "inventory"]
description: "Authoritative inventory ranking, planned page tree, and evidence briefs for the DSOM codebase."
resource: "file:///home/runner/work/deep-state-of-mind-for-my-ai/deep-state-of-mind-for-my-ai/openwiki/_skeleton.md"
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
