---
okf_version: 0.2
type: architecture_concept
title: "🛡️ DSOM Guardrail Catalog & Guardrails AI Submission Review Document"
timestamp: "2026-08-22T07:15:00Z"
topics: ["guardrails", "guardrails-hub", "dsom", "validation", "pypi", "security", "okf", "ast"]
description: "Comprehensive catalog and publication roadmap for the 10 DSOM Guardrails, prepared for human review and packaging as standalone PyPI packages under the Guardrails AI ecosystem."
resource: "file:///docs/governance/DSOM-GUARDRAILS-CATALOG-SUBMISSION-REVIEW.md"
sources: [
  "https://guardrailsai.com/guardrails/docs",
  "https://guardrailsai.com/guardrails/docs/how-to-guides/custom_validators",
  "docs/governance/AI-GUARDRAILS-MASTER-GUIDE.md",
  "docs/governance/DSOM-CUSTOM-VALIDATORS-GUIDE.md",
  ".agents/AGENTS.md"
]
generated: "google-antigravity"
verified: true
status: "approved"
stale_after: "2027-08-22T00:00:00Z"
---

# 🛡️ DSOM Guardrail Catalog & Guardrails AI Submission Review Document

> **Document Purpose:** Human Review & Publication Roadmap  
> **Target Audience:** Harisfazillah Jamel (LinuxMalaysia), Lead Architects, and Open-Source Community  
> **Ecosystem Target:** Guardrails AI PyPI Ecosystem (`guardrails-ai-<name>`) & DSOM Native Runtime  
> **Status:** Draft for Final Review | OKF v0.2 Compliant  
> **Live URL:** [`https://linuxmalaysia.github.io/deep-state-of-mind-for-my-ai/governance/DSOM-GUARDRAILS-CATALOG-SUBMISSION-REVIEW/`](https://linuxmalaysia.github.io/deep-state-of-mind-for-my-ai/governance/DSOM-GUARDRAILS-CATALOG-SUBMISSION-REVIEW/)

---

## 📌 1. Executive Summary & Hub Transition Note

This document presents the complete catalog of **10 specialized AI Guardrails** engineered for the **Deep State of Mind (DSOM)** protocol. Each guardrail protects a distinct vector of autonomous agent operation, digital sovereignty, token conservation, and GitOps hygiene.

### ⚠️ Critical Upstream Notice (Guardrails AI Hub Transition):
As documented in the official Guardrails AI architecture updates:
* **The Centralized Hub Cutoff:** Guardrails AI has transitioned away from the centralized `guardrails hub install` private registry towards **standard standalone Python packages on PyPI** (`guardrails-ai-<validator-name>`).
* **Contribution & Publishing Model:** We package our custom validators as open-source PyPI packages using standard Python build tooling (`uv build`, `flit`, or `hatchling`), allowing any developer in the global Guardrails AI community to install them via `uv add guardrails-ai-dsom-<validator>`.

---

## 🗂️ 2. The Complete DSOM 10-Guardrail Inventory

Below is the exhaustive inventory of all guardrails required to guarantee 100% compliance with the DSOM protocol.

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                THE 10 DSOM SOVEREIGN GUARDRAILS                                  │
├────────────────────────────────┬────────────────────────────────┬────────────────────────────────┤
│ 1. OKF Frontmatter & BOM       │ 2. OKF v0.2 Trust Signals      │ 3. Sovereign Signature Footer │
│ 4. Credential & PII Guardian   │ 5. Isolated Python Execution   │ 6. Byte-Capped Terminal Guard │
│ 7. Atomic Commit Gatekeeper    │ 8. Skill Token Window Gate     │ 9. Knowledge-First AST Router │
│ 10. Root Cleanliness Guardian  │                                │                                │
└────────────────────────────────┴────────────────────────────────┴────────────────────────────────┘
```

---

### 1️⃣ Guardrail 1: OKF Frontmatter & UTF-8 BOM Stripper (`guardrails-ai-dsom-okf-bom`)
* **DSOM Rule Reference:** **Rule 2 & Rule 25** (Open Knowledge Format & GitHub Web Compatibility).
* **Threat Vector:** Windows editors and raw LLM text generation inserting hidden UTF-8 Byte Order Marks (`\xef\xbb\xbf`) and missing opening YAML frontmatter fences (`---`), which breaks GitHub web rendering and downstream parser scripts.
* **Validation Logic:**
  1. Inspects raw string start.
  2. If `\ufeff` is detected, strips it immediately (`on_fail="fix"`).
  3. Asserts line 1 starts with `---`.
* **Guardrails AI Class:** `GuardrailsOKFBOMValidator`
* **On-Fail Actions:** `fix` (automatically strips BOM and normalizes fence) or `fail`.

```python
# Prototype Implementation
from guardrails.validators import Validator, register_validator, PassResult, FailResult

@register_validator(name="dsom/okf_bom_validator", data_type="string")
class GuardrailsOKFBOMValidator(Validator):
    def validate(self, value, metadata=None):
        text = str(value)
        if text.startswith("\ufeff"):
            return FailResult(error_message="BOM detected", fix_value=text.lstrip("\ufeff"))
        if not (text.startswith("---\n") or text.startswith("---\r\n")):
            return FailResult(error_message="Document must start on Line 1 with '---'")
        return PassResult()
```

---

### 2️⃣ Guardrail 2: OKF v0.2 Provenance & Trust Signal Gate (`guardrails-ai-dsom-okf-trust`)
* **DSOM Rule Reference:** **Rule 6 & Rule 21** (Opportunistic OKF v0.2 Migration & Temporal Verification).
* **Threat Vector:** LLMs creating or updating documentation without provenance metadata, leading to unverified hallucinations and stale architectural drift.
* **Validation Logic:**
  1. Parses YAML frontmatter into a dictionary.
  2. If `okf_version: 0.2`, asserts all 6 trust fields exist: `sources` (list), `generated` (string), `verified` (bool), `status` (string), `stale_after` (ISO timestamp), `topics` (list of 3-5 tags).
* **Guardrails AI Class:** `GuardrailsOKFTrustValidator`
* **On-Fail Actions:** `reask` (prompts LLM to supply missing source links and verification status).

---

### 3️⃣ Guardrail 3: Sovereign Signature & Modification Date Auditor (`guardrails-ai-dsom-sovereign-signature`)
* **DSOM Rule Reference:** **Rule 13** (Sovereign Signature & Modification Date Mandate).
* **Threat Vector:** Agents modifying markdown documents without refreshing the explicit footer signature date, causing human operators and peer agents (Jules/Antigravity) to lose track of document freshness.
* **Validation Logic:**
  1. Inspects the last 3 lines of markdown text.
  2. Verifies presence of the standard DSOM footer: `*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | YYYY-MM-DD*`.
  3. Verifies that `YYYY-MM-DD` matches the current session date.
* **Guardrails AI Class:** `GuardrailsSovereignSignatureValidator`
* **On-Fail Actions:** `fix` (automatically appends or updates the date signature) or `fail`.

---

### 4️⃣ Guardrail 4: Defensive Credential & Secret Interceptor (`guardrails-ai-dsom-credential-guardian`)
* **DSOM Rule Reference:** **Rule 24** (Defensive Credential Handling Mandate).
* **Threat Vector:** Agents or human prompts inadvertently pasting GitHub tokens (`ghp_*`), GitLab tokens (`glpat-*`), AWS keys (`AKIA*`), or SSH/RSA Private Keys into persistent files or chat logs.
* **Validation Logic:**
  1. Runs high-performance regular expressions across all output text and tool parameters.
  2. Blocks execution instantly if an API key or private key pattern is detected.
* **Guardrails AI Class:** `GuardrailsCredentialGuardian`
* **On-Fail Actions:** `exception` / `block` (refuses to proceed and advises human to rotate keys).

---

### 5️⃣ Guardrail 5: Isolated Python Execution & Tool Gatekeeper (`guardrails-ai-dsom-uv-gatekeeper`)
* **DSOM Rule Reference:** **Rule 16** (The `uv` Isolated Execution Mandate).
* **Threat Vector:** Agents running unmanaged `pip install`, `python`, or `python3` commands, polluting system Python and risking PATH hijacking on Windows.
* **Validation Logic:**
  1. Inspects CLI invocation commands.
  2. Intercepts and blocks commands containing `pip `, `python `, or `python3 `.
  3. Suggests `uv run` or `uv add`.
* **Guardrails AI Class:** `GuardrailsUVExecutionValidator`
* **On-Fail Actions:** `fix` (rewrites `pip install X` to `uv add X`) or `block`.

---

### 6️⃣ Guardrail 6: Byte-Capped Terminal Output Interceptor (`guardrails-ai-dsom-byte-cap`)
* **DSOM Rule Reference:** **Rule 10** (Byte-Capped Executions & Context Window Defense).
* **Threat Vector:** Commands returning massive payloads (e.g. `cat 50MB.log` or verbose build logs) that flood the LLM context window, triggering token budget exhaustion and memory amnesia.
* **Validation Logic:**
  1. Inspects terminal command outputs or tool string returns.
  2. Measures token/byte size.
  3. Truncates text exceeding 4,000 bytes and appends a `[TRUNCATED BY DSOM BYTE-CAP GUARDRAIL]` notice.
* **Guardrails AI Class:** `GuardrailsByteCapValidator`
* **On-Fail Actions:** `fix` (programmatically truncates and preserves context budget).

---

### 7️⃣ Guardrail 7: Granular Atomic Git Commit Enforcer (`guardrails-ai-dsom-atomic-commit`)
* **DSOM Rule Reference:** **Rule 4** (Git Sovereignty & Atomic Commits).
* **Threat Vector:** Agents running blanket `git commit -am "update"` or staging all unrelated files across the entire repo in one monolithic commit.
* **Validation Logic:**
  1. Inspects Git commands before execution.
  2. Blocks `git commit -am` or commits with non-semantic messages (e.g., "fixed stuff", "wip").
  3. Requires semantic Conventional Commit format (`feat(...)`, `docs(...)`, `fix(...)`, `refactor(...)`).
* **Guardrails AI Class:** `GuardrailsAtomicCommitValidator`
* **On-Fail Actions:** `block` (instructs agent to stage files logically and write semantic messages).

---

### 8️⃣ Guardrail 8: Skill Token Window Gatekeeper (`guardrails-ai-dsom-skill-token-gate`)
* **DSOM Rule Reference:** **Rule 19** (Skill Modification Quality Gate & Progressive Disclosure).
* **Threat Vector:** AI agents authoring massive `SKILL.md` documents (>4,000 tokens) that bloat context windows when semantic discovery triggers.
* **Validation Logic:**
  1. Uses `tiktoken` (cl100k_base or o200k_base) to measure `SKILL.md` payload token counts.
  2. Blocks any skill exceeding 4,000 tokens.
  3. Enforces offloading reference blocks to a `references/` subdirectory.
* **Guardrails AI Class:** `GuardrailsSkillTokenGate`
* **On-Fail Actions:** `block` (forces agent to offload detailed tables to `references/`).

---

### 9️⃣ Guardrail 9: Knowledge-First AST Discovery Interceptor (`guardrails-ai-dsom-knowledge-first`)
* **DSOM Rule Reference:** **Rule 20 & Rule 21** (Local Knowledge-First Discovery Protocol).
* **Threat Vector:** Agents jumping straight to terminal probe commands or external web queries without first checking local OKF documentation and spatial brain state.
* **Validation Logic:**
  1. Intercepts task initialization.
  2. Verifies that the agent has performed `grep_search` on `.agents/brain/` or `docs/` before executing system commands.
* **Guardrails AI Class:** `GuardrailsKnowledgeFirstValidator`
* **On-Fail Actions:** `reask` (prompts agent: *"You must search local OKF memory first before executing OS commands"*).

---

### 🔟 Guardrail 10: Root Workspace Cleanliness & SaaS Isolation Guard (`guardrails-ai-dsom-root-cleanliness`)
* **DSOM Rule Reference:** **Rule 17** (Root Workspace Cleanliness Mandate).
* **Threat Vector:** Agents dumping scratch files, temporary logs, or ad-hoc scripts into the repository root instead of `.agents/`, `docs/`, or `tools/`.
* **Validation Logic:**
  1. Checks target file paths for write operations.
  2. Permits only core governance files (`README.md`, `SUMMARY.md`, `START-HERE.md`, `llms.txt`, `.gitignore`, `ansible.cfg`) and SaaS verification files (`context7.json`).
  3. Redirects all other docs to `docs/` and tools to `tools/`.
* **Guardrails AI Class:** `GuardrailsRootCleanlinessValidator`
* **On-Fail Actions:** `fix` (redirects file path to appropriate subdirectory) or `block`.

---

## 📦 3. Packaging & PyPI Publishing Architecture

To distribute these guardrails to the broader AI community and the Guardrails AI ecosystem, we organize them into an open-source mono-package with individual plugin exports:

### Package Naming & Layout:
```
guardrails-ai-dsom/
├── pyproject.toml
├── README.md
├── LICENSE (GPL-3.0 / Apache-2.0 Dual License)
└── src/
    └── guardrails_dsom/
        ├── __init__.py
        ├── okf_bom_validator.py            # Guardrail 1
        ├── okf_trust_validator.py          # Guardrail 2
        ├── sovereign_signature.py          # Guardrail 3
        ├── credential_guardian.py          # Guardrail 4
        ├── uv_gatekeeper.py                # Guardrail 5
        ├── byte_cap_validator.py           # Guardrail 6
        ├── atomic_commit_validator.py      # Guardrail 7
        ├── skill_token_gate.py             # Guardrail 8
        ├── knowledge_first_validator.py    # Guardrail 9
        └── root_cleanliness_validator.py   # Guardrail 10
```

### PyPI Installation:
```bash
uv add guardrails-ai-dsom
```

### Universal Usage in Any Guardrails AI Application:
```python
from guardrails import Guard
from guardrails_dsom import (
    GuardrailsOKFBOMValidator,
    GuardrailsCredentialGuardian,
    GuardrailsSovereignSignatureValidator,
)

# Protect an AI Agent with DSOM Sovereign Guardrails
guard = Guard().use_many(
    GuardrailsOKFBOMValidator(on_fail="fix"),
    GuardrailsCredentialGuardian(on_fail="exception"),
    GuardrailsSovereignSignatureValidator(on_fail="fix"),
)

validated_output = guard.validate(llm_generated_content)
```

---

## 📋 4. Next Steps for Human Review & Release

| Milestone | Action Item | Responsible |
| :--- | :--- | :--- |
| **Review 1** | Human Architect (Harisfazillah Jamel) reviews the 10-guardrail list and approves scope. | Human |
| **Review 2** | Finalize license model (GPL v3.0 core vs. Apache 2.0 PyPI wrapper for Guardrails AI ecosystem). | Human |
| **Step 3** | Scaffold `tools/guardrails-ai-dsom/` package directory with automated unit test suites. | AI Twin |
| **Step 4** | Build wheel via `uv build` and publish to PyPI (`guardrails-ai-dsom`). | Human / CI |
| **Step 5** | Submit documentation PR / listing to Guardrails AI community showcase. | Human |

---

## 📚 SOURCES

* [Guardrails AI Official Documentation](https://guardrailsai.com/guardrails/docs) - Upstream architecture and validator development guide.
* [The Master Guide to AI Guardrails & Custom Validators](file:///docs/governance/AI-GUARDRAILS-MASTER-GUIDE.md) - Theoretical and technical foundation.
* [The Core AI Rulebook (DSOM)](file:///.agents/AGENTS.md) - Sovereign rules 2, 4, 6, 10, 13, 16, 17, 19, 20, 24, 25, and 29.

---
*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-08-22*  
*Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*
