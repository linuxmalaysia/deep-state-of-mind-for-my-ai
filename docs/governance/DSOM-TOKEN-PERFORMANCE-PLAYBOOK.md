---
okf_version: 0.1
type: l1_synthesis
title: "DSOM Token Performance Playbook"
description: "Master playbook for token-efficient DSOM operation. Covers tools, rules, benchmarks, and procedures for minimising LLM context window consumption across all DSOM projects."
topics: [tokens, performance, tiktoken, byte-cap, context-optimisation]
resource: "file:///docs/governance/DSOM-TOKEN-PERFORMANCE-PLAYBOOK.md"
timestamp: 2026-07-19T11:27:00+08:00
---

# DSOM Token Performance Playbook

> **Artifact Level:** L1 (Synthesis)
> **Status:** Active Baseline — embed into all new DSOM projects.
> **Audience:** Any AI agent or human operator bootstrapping a new DSOM project.

## Abstract

With this playbook, any new or existing DSOM project inherits the complete token efficiency architecture proven in the `deep-state-of-mind-for-my-ai` baseline repository. The core finding: **DSOM's Progressive Disclosure, OKF frontmatter tagging, and Byte-Capped Executions reduce per-session context consumption by 96.23%** versus monolithic document loading strategies.

---

## 1. The Core Problem This Solves

Every LLM agent has a finite context window. Without discipline, agents waste the majority of that window loading files they do not need, duplicate content, and verbose prose that could have been filtered at the frontmatter level.

**DSOM solves this at three layers:**

| Layer | Mechanism | Token Saving |
|---|---|---|
| **L1 — Discovery** | `topics:` OKF frontmatter grep routing | Avoids loading 14,400+ body tokens per skill-discovery pass |
| **L2 — Gate** | 4,000-token circuit breaker via `dsom-token-calculator` | Prevents any single file from flooding context |
| **L3 — Session** | `active_context_manifest.md` + Episodic Resume | Loads only declared files; no orphaned state |

---

## 2. Mandatory Tools (Embed in Every Project)

### 2.1 Token Calculator Skill

**Location:** `.agents/skills/dsom-token-calculator/`

**Usage:**
```bash
# Scan entire skills directory
uv run --with tiktoken .agents/skills/dsom-token-calculator/scripts/calculate-tokens.py .agents/skills/

# Audit a single file with per-section breach report
uv run --with tiktoken .agents/skills/dsom-token-calculator/scripts/calculate-tokens.py path/to/SKILL.md --sections
```

**Gate logic:**
- `[OK]` — file is safe to load wholesale into context
- `[BLOCKED]` — file exceeds 4,000 tokens; use `view_file` with line ranges only

### 2.2 Active Context Manifest

**Location:** `.agents/brain/active_context_manifest.md`

Update this file at every SOD ritual. The agent loads **only the files declared here**. Never load `.agents/brain/` wholesale — three archival files alone contain 120,000+ tokens.

```markdown
## Active Files
- .agents/brain/task.md
- .agents/brain/walkthrough.md
- .agents/brain/palace_registry.md
- .agents/brain/wings/[relevant wing]/[relevant closet].md
```

### 2.3 Token Auditor Script

**Location:** `tools/dsom_token_auditor.py`

Run for a full workspace token efficiency audit:
```bash
uv run --with tiktoken tools/dsom_token_auditor.py
```

---

## 3. Mandatory OKF Frontmatter Standards

Every `SKILL.md` must contain these five fields in this order:

```yaml
---
okf_version: 0.1
type: skill
title: "Skill Title"
description: "Single-sentence description of what this skill does."
topics: [keyword1, keyword2, keyword3, keyword4, keyword5]
---
```

**Why `topics:` matters:**
The agent performs skill discovery by grepping only `topics:` and `description:` fields — never loading the full body. For 25 skills, this reduces discovery cost from ~14,400 tokens (full bodies) to ~375 tokens (frontmatter only). That is a **97.4% token reduction on every skill lookup**.

**Topics rules:**
- 3–5 keywords maximum
- All lowercase, hyphenated for multi-word terms
- Must be placed immediately after `description:`

---

## 4. Benchmark Results (T1 Node — Windows/NVMe)

Captured 2026-07-19 on the baseline repository:

| Metric | Value |
|---|---|
| Brain directory files | 38 |
| Total brain tokens | 145,729 |
| Average read per file | ~23.9 ms |
| Average tokenise per file | ~8.9 ms |
| **Largest single file** | `palace_update_proposal` — 55,726 tokens |
| **Brain files exceeding gate** | 3 files (all archival proposals) |

> **Termux/T2 note:** Android FUSE filesystem adds an estimated 2–5× read latency. Benchmark your T2 node using `tools/bench_brain.py` and update this table.

---

## 5. Rules Governing Token Efficiency (AGENTS.md)

These core rules enforce token discipline automatically:

| Rule | Mandate |
|---|---|
| **Rule 6** | All `SKILL.md` files must include `topics:` (3–5 keywords) in OKF frontmatter. |
| **Rule 10** | Byte-Capped Executions — all exploratory terminal operations must be output-capped. |
| **Rule 12** | Skill discovery uses frontmatter metadata only; full body loaded only at execution time. |
| **Rule 16** | All Python execution via `uv` only — no raw `python` or `pip`. |
| **Rule 18** | Episodic Resume Protocol — session state serialised at every EOD. |
| **Rule 19** | Skill Modification Quality Gate — run token calculator before and after every skill edit. |

---

## 6. Procedures for New Project Bootstrap

When cloning this repository as a baseline for a new project, execute these steps to inherit full token efficiency:

### Step 1 — Verify skill token health
```bash
uv run --with tiktoken .agents/skills/dsom-token-calculator/scripts/calculate-tokens.py .agents/skills/
```
Expected: all files `[OK]`, zero `[BLOCKED]`.

### Step 2 — Initialise active context manifest
Copy `.agents/brain/active_context_manifest.md` and update the `## Active Files` section for your project's domain.

### Step 3 — Run baseline token audit
```bash
uv run --with tiktoken tools/dsom_token_auditor.py
```
Document the initial token footprint in your project's `docs/governance/DSOM-TOKEN-EFFICIENCY-REPORT.md`.

### Step 4 — Verify all skills have `topics:` tags
```powershell
Get-ChildItem -Recurse -Path ".agents/skills" -Filter "SKILL.md" | ForEach-Object {
    $content = Get-Content $_.FullName -Raw
    $hasTopics = $content -match "(?m)^topics:"
    [PSCustomObject]@{ Skill = $_.Directory.Name; Topics = if($hasTopics){"YES"}else{"MISSING"} }
} | Format-Table -AutoSize
```
All skills must return `YES`. If any return `MISSING`, run the `inject_topics.py` remediation script from `docs/governance/DSOM-INGESTION-LATENCY-ARCHITECTURE.md`.

### Step 5 — Gate archival brain files
Identify any `.agents/brain/` files exceeding 4,000 tokens and add them to the `## Excluded` section of `active_context_manifest.md` with their token count annotated.

---

## 7. Anti-Patterns (Never Do This)

| Anti-Pattern | Why It Fails | Correct Alternative |
|---|---|---|
| `git add -A && git commit -m "update"` | Monolithic — violates Rule 4. Makes history unreadable. | Stage and commit each logical unit separately. |
| Loading `.agents/brain/` directory wholesale | Three files = 120,000+ tokens. Context window collapse. | Use `active_context_manifest.md`. |
| Creating a `SKILL.md` without `topics:` | Forces full-body read on every discovery pass. | Always include `topics: [...]` in frontmatter. |
| Using raw `python` or `pip` | PATH hijacking risk on Windows, no isolation. | Always use `uv run` and `uv add`. |
| Loading a `palace_update_proposal` file directly | 30,000–55,000 tokens each. Instant context flood. | Use `view_file` with targeted line ranges. |

---

## SOURCES

| Document | Description |
|---|---|
| [DSOM-TOKEN-EFFICIENCY-REPORT.md](DSOM-TOKEN-EFFICIENCY-REPORT.md) | Empirical proof: 96.23% token reduction via DSOM protocol. |
| [BYTE-CAPPED-EXECUTION-FRAMEWORK.md](BYTE-CAPPED-EXECUTION-FRAMEWORK.md) | Enforcement model for Rule 10 Byte-Capped Executions. |
| [DSOM-INGESTION-LATENCY-ARCHITECTURE.md](DSOM-INGESTION-LATENCY-ARCHITECTURE.md) | L2 analysis: local OKF reads vs. remote RAG/vector latency with empirical benchmarks. |
| [PYTHON-UV-ENVIRONMENT-GUIDE.md](PYTHON-UV-ENVIRONMENT-GUIDE.md) | Mandated `uv` execution environment (Rule 16). |
| [dsom-token-calculator SKILL.md](../../.agents/skills/dsom-token-calculator/SKILL.md) | Executable skill: local token footprint measurement with per-section breach alerting. |
| [active_context_manifest.md](../../.agents/brain/active_context_manifest.md) | OKF manifest declaring active session files — replaces symlink pattern. |
| [AGENTS.md](../../.agents/AGENTS.md) | Core rulebook: Rules 6, 10, 12, 16, 18, 19 govern token efficiency. |

---

*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-07-19*
*Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*
