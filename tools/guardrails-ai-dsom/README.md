---
okf_version: 0.2
type: reference
title: "🛡️ guardrails-ai-dsom: Sovereign AI Guardrails for DSOM"
timestamp: "2026-08-22T07:25:00Z"
topics: ["guardrails", "guardrails-ai", "dsom", "validation", "pypi", "security"]
description: "Documentation and usage reference for the guardrails-ai-dsom standalone Python package."
resource: "file:///tools/guardrails-ai-dsom/README.md"
sources: [
  "docs/governance/AI-GUARDRAILS-MASTER-GUIDE.md",
  "docs/governance/DSOM-GUARDRAILS-CATALOG-SUBMISSION-REVIEW.md",
  ".agents/AGENTS.md"
]
generated: "google-antigravity"
verified: true
status: "approved"
stale_after: "2027-08-22T00:00:00Z"
---

# 🛡️ guardrails-ai-dsom

> **Sovereign AI Guardrails and Custom Validators for the Deep State of Mind (DSOM) Protocol**

`guardrails-ai-dsom` is an open-source, dual-mode Python package providing **10 custom validators** for AI agents, FastMCP servers, and LLM applications operating under the **Deep State of Mind (DSOM)** protocol.

---

## 🚀 Installation

```bash
# Standard installation
uv add guardrails-ai-dsom

# With optional Guardrails AI & Token dependencies
uv add "guardrails-ai-dsom[all]"
```

---

## 🗂️ The 10 DSOM Sovereign Custom Validators

| # | Validator Class | Purpose | On-Fail Action |
| :-: | :--- | :--- | :--- |
| **1** | `GuardrailsOKFBOMValidator` | Strips leading UTF-8 Byte Order Marks (`\ufeff`) & enforces frontmatter fences. | `fix` / `block` |
| **2** | `GuardrailsOKFTrustValidator` | Validates OKF v0.2 trust profile metadata (`sources`, `verified`, `stale_after`). | `block` / `reask` |
| **3** | `GuardrailsSovereignSignatureValidator` | Verifies and refreshes the standard DSOM footer signature and modification date. | `fix` / `block` |
| **4** | `GuardrailsCredentialGuardian` | Intercepts GitHub/GitLab tokens, AWS keys, and RSA/OpenSSH private keys. | `block` |
| **5** | `GuardrailsUVExecutionValidator` | Enforces Rule 16 (`uv` execution), blocking raw unmanaged `pip` or `python`. | `fix` / `block` |
| **6** | `GuardrailsByteCapValidator` | Truncates command outputs exceeding 4,000 bytes to protect LLM context windows. | `fix` |
| **7** | `GuardrailsAtomicCommitValidator` | Blocks `git commit -am` and requires semantic Conventional Commit format. | `block` |
| **8** | `GuardrailsSkillTokenGate` | Measures `SKILL.md` token budgets via `tiktoken`, enforcing the 4,000-token cap. | `block` |
| **9** | `GuardrailsKnowledgeFirstValidator` | Enforces local OKF memory search before executing system terminal commands. | `block` / `reask` |
| **10** | `GuardrailsRootCleanlinessValidator` | Prevents rogue file dumping at the repository root, auto-routing docs & tools. | `fix` / `block` |

---

## 💡 Usage Example: Standalone (DSOM Native Mode)

```python
from guardrails_dsom import (
    GuardrailsOKFBOMValidator,
    GuardrailsCredentialGuardian,
    GuardrailsUVExecutionValidator,
)

# 1. Strip BOM from markdown
bom_val = GuardrailsOKFBOMValidator(on_fail="fix")
res = bom_val.validate("\ufeff---\nokf_version: 0.2\ntitle: Example\n---\n")
print(res.corrected_value)

# 2. Block credential leak
cred_val = GuardrailsCredentialGuardian()
res = cred_val.validate("Here is my secret token: ghp_123456789012345678901234567890123456")
if not res.is_valid:
    print(f"Blocked: {res.error_message}")
```

---

## 💡 Usage Example: With Guardrails AI Framework

```python
from guardrails import Guard
from guardrails_dsom import (
    GuardrailsOKFBOMValidator,
    GuardrailsCredentialGuardian,
    GuardrailsSovereignSignatureValidator,
)

# Guard your LLM pipeline
guard = Guard().use_many(
    GuardrailsOKFBOMValidator(on_fail="fix"),
    GuardrailsCredentialGuardian(on_fail="exception"),
    GuardrailsSovereignSignatureValidator(on_fail="fix"),
)

validated = guard.validate(llm_output)
```

---

## 📄 License
GNU General Public License v3.0 (GPLv3+) / Standard Open-Source Sovereign Stack.

---
*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-08-22*  
*Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*
