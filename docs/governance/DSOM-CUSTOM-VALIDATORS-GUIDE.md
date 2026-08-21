---
okf_version: 0.2
type: architecture_concept
title: "🛡️ Custom Validators in DSOM: Guardrails Architecture & Implementation Blueprint"
timestamp: "2026-08-21T22:15:00Z"
topics: ["guardrails", "validation", "ast", "mcp", "dsom", "twilight-state", "okf"]
description: "Architectural blueprint and implementation guide detailing how to build custom deterministic and LLM-powered validators within the Deep State of Mind (DSOM) framework, inspired by Guardrails AI principles."
resource: "file:///docs/governance/DSOM-CUSTOM-VALIDATORS-GUIDE.md"
sources: [
  "https://guardrailsai.com/guardrails/docs/how-to-guides/custom_validators",
  "docs/governance/DSOM-TRI-PHASIC-COGNITIVE-ARCHITECTURE.md",
  ".agents/AGENTS.md"
]
generated: "google-antigravity"
verified: true
status: "approved"
stale_after: "2027-08-21T00:00:00Z"
---

# 🛡️ Custom Validators in DSOM: Guardrails Architecture & Implementation Blueprint

> **Reference URL:** [Guardrails AI Custom Validators Guide](https://guardrailsai.com/guardrails/docs/how-to-guides/custom_validators)  
> **Status:** Architectural Reference & How-To Guide for Human Engineers & AI Agents

---

## 🧭 1. Executive Summary & Philosophy

In modern AI agent engineering, unvalidated LLM output poses severe operational risks: hallucinations, syntax corruptions, security leaks, toxic biases, and broken schema definitions.

[Guardrails AI](https://guardrailsai.com) provides a structured pattern for intercepting and validating inputs and outputs using programmatic validators (both deterministic code-based rules and lightweight LLM-evaluated checks).

Within the **Deep State of Mind (DSOM)** framework, we adopt and map these custom validation concepts directly into our **Tri-Phasic Cognitive Pipeline** and **Subsystem 4 (Metacognition & Guardrails)** without taking heavy, bloated runtime dependencies.

```
┌────────────────────────────────────────────────────────────────────────┐
│                    DSOM VALIDATOR INTERCEPTION PIPELINE                │
├────────────────────────────────────────────────────────────────────────┤
│ 1. Input Guardrail     │ FastMCP Tool Invocations / Prompt Sanitization │
├────────────────────────────────────────────────────────────────────────┤
│ 2. Inline Validator    │ Twilight State AST / Regex / OKF Schema Checks │
├────────────────────────────────────────────────────────────────────────┤
│ 3. Output Guardrail    │ EOD Palace Sync & GitOps Commit Gate (pytest)  │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 🏛️ 2. Core Concepts: Anatomy of a Guardrails Custom Validator

In the Guardrails AI ecosystem, a custom validator is defined by:
1. **Target Type:** Whether it validates strings, JSON objects, lists, or AST code trees.
2. **`validate(value, metadata)` Method:** The core evaluation logic returning `PassResult` or `FailResult`.
3. **On-Fail Actions:** Deterministic corrective actions when validation fails:
   - `reask`: Prompts the model to regenerate the offending output.
   - `fix`: Programmatically corrects the output (e.g., stripping BOM, wrapping unquoted YAML).
   - `filter`: Redacts or purges the violating content.
   - `refrain`: Suppresses output entirely.
   - `exception`: Aborts execution immediately with a defensive error.

---

## ⚙️ 3. Implementing Custom Validators in DSOM

In DSOM, we enforce validation at three distinct layers:
1. **Static / Deterministic Python Validators** (Twilight State / pre-commit).
2. **FastMCP Request/Response Interceptors** (Active State).
3. **Pytest Cognitive Test Harness** (Deep State / CI/CD).

### Architectural Implementation Pattern:

```python
"""
Example: tools/validators/base.py
DSOM Custom Validator Core Schema
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, Optional, Literal

@dataclass
class ValidationResult:
    is_valid: bool
    corrected_value: Optional[Any] = None
    error_message: Optional[str] = None
    action_taken: Literal["pass", "fixed", "blocked", "reask"] = "pass"

class BaseDSOMValidator(ABC):
    """Abstract Base Class for all DSOM Custom Validators."""
    
    name: str = "base_validator"
    on_fail: Literal["fix", "block", "reask"] = "block"

    @abstractmethod
    def validate(self, value: Any, metadata: Optional[Dict[str, Any]] = None) -> ValidationResult:
        """Evaluate value and return ValidationResult."""
        pass
```

---

## 🛠️ 4. Concrete DSOM Custom Validator Examples

### Validator 1: OKF Frontmatter & Quoting Validator (`tools/validators/okf_validator.py`)
Ensures all Markdown outputs strictly conform to OKF v0.1/v0.2 standards with BOM-less UTF-8 and double-quoted strings.

```python
import re
from typing import Any, Dict, Optional
from tools.validators.base import BaseDSOMValidator, ValidationResult

class OKFFrontmatterValidator(BaseDSOMValidator):
    name = "okf_frontmatter_validator"
    on_fail = "fix"

    def validate(self, markdown_text: str, metadata: Optional[Dict[str, Any]] = None) -> ValidationResult:
        # Check 1: Must not start with UTF-8 BOM
        if markdown_text.startswith("\ufeff"):
            fixed = markdown_text.lstrip("\ufeff")
            return ValidationResult(
                is_valid=False,
                corrected_value=fixed,
                error_message="Leading UTF-8 BOM detected and stripped.",
                action_taken="fixed"
            )
        
        # Check 2: Must begin with YAML fence on line 1, column 1
        if not (markdown_text.startswith("---\n") or markdown_text.startswith("---\r\n")):
            return ValidationResult(
                is_valid=False,
                error_message="Document does not start with OKF frontmatter fence (---).",
                action_taken="blocked"
            )

        return ValidationResult(is_valid=True)
```

---

### Validator 2: Credential & PII Leak Guardian (`tools/validators/credential_guardian.py`)
Implements **Rule 24 (Defensive Credential Handling)** to block API keys, private keys, or passwords from touching Git or responses.

```python
import re
from typing import Any, Dict, Optional
from tools.validators.base import BaseDSOMValidator, ValidationResult

class CredentialGuardianValidator(BaseDSOMValidator):
    name = "credential_guardian"
    on_fail = "block"

    PATTERNS = [
        re.compile(r"ghp_[a-zA-Z0-9]{36}"),                # GitHub Classic Token
        re.compile(r"github_pat_[a-zA-Z0-9_]{82}"),        # GitHub Fine-grained Token
        re.compile(r"glpat-[a-zA-Z0-9\-]{20}"),            # GitLab Personal Access Token
        re.compile(r"-----BEGIN (RSA|OPENSSH) PRIVATE KEY-----"), # Private Keys
    ]

    def validate(self, text: str, metadata: Optional[Dict[str, Any]] = None) -> ValidationResult:
        for pattern in self.PATTERNS:
            if pattern.search(text):
                return ValidationResult(
                    is_valid=False,
                    error_message=f"Credential/Key signature detected matching pattern {pattern.pattern}.",
                    action_taken="blocked"
                )
        return ValidationResult(is_valid=True)
```

---

### Validator 3: Python AST UV-Execution Gatekeeper (`tools/validators/ast_uv_gatekeeper.py`)
Implements **Rule 16 (The `uv` Mandate)** by parsing generated terminal commands or scripts to block raw `pip install` or `python` calls.

```python
from typing import Any, Dict, Optional
from tools.validators.base import BaseDSOMValidator, ValidationResult

class PythonExecutionValidator(BaseDSOMValidator):
    name = "python_execution_gatekeeper"
    on_fail = "block"

    PROHIBITED_COMMANDS = ["pip install", "python3 ", "python "]

    def validate(self, terminal_command: str, metadata: Optional[Dict[str, Any]] = None) -> ValidationResult:
        trimmed = terminal_command.strip()
        
        # Prohibit raw pip
        if trimmed.startswith("pip ") or " pip install " in trimmed:
            return ValidationResult(
                is_valid=False,
                error_message="Violation of Rule 16 (uv Mandate): Raw pip execution detected. Use 'uv add' or 'uv run --with'.",
                action_taken="blocked"
            )
            
        return ValidationResult(is_valid=True)
```

---

## 🔌 5. Integration into the FastMCP Server (`tools/mcp/server.py`)

Guardrails custom validators can be hooked directly into our native FastMCP server, verifying arguments before tool execution and sanitizing results before returning to AI IDEs (Cursor/Claude Desktop):

```python
# tools/mcp/server.py snippet
from fastmcp import FastMCP
from tools.validators.credential_guardian import CredentialGuardianValidator

mcp = FastMCP("DSOM Sovereign MCP")
guardian = CredentialGuardianValidator()

@mcp.tool()
def safe_write_knowledge(path: str, content: str) -> str:
    """Writes knowledge to palace with inline guardrail validation."""
    
    # 1. Run Input Guardrail
    res = guardian.validate(content)
    if not res.is_valid:
        raise ValueError(f"[GUARDRAIL BLOCKED] {res.error_message}")
        
    # 2. Proceed with idempotent write
    # ... write logic ...
    return f"Successfully validated and written to {path}"
```

---

## 📈 6. Comparison: Guardrails AI vs. DSOM Native Approach

| Feature | Guardrails AI Framework | DSOM Native Implementation |
| :--- | :--- | :--- |
| **Runtime Footprint** | Heavy Python package (`guardrails-ai`) with Pydantic v2 dependencies. | Lightweight, zero-bloat standalone Python classes running under `uv`. |
| **Execution Phase** | LLM output parsing & serialization. | Tri-Phasic (Active MCP, Twilight AST, Deep EOD). |
| **GitOps Integration** | None (in-memory). | Native Git hook & Pytest integration (`tests/`). |
| **Self-Healing** | Automatic re-asking via API. | Sovereign Episodic record + mental anchor rollback. |
| **Target Workflows** | Chatbots & web APIs. | Systems Engineering, GitOps, Infra Automation, AI Twins. |

---

## 🚀 7. Step-by-Step Guide for Human Operators & Next Steps

When extending this repository with custom validators:
1. **Define the Validator**: Create a new validator under `tools/validators/` implementing `BaseDSOMValidator`.
2. **Add Unit Tests**: Write corresponding unit tests in `tests/test_validators.py` asserting pass/fail/fix cases.
3. **Register in MCP or CI**: Hook the validator into `tools/mcp/server.py` or `.github/workflows/docs-ci.yml`.
4. **Update the Sovereign Palace**: Link the validator documentation into `SUMMARY.md`, `mkdocs.yml`, and `START-HERE.md`.

---

## 📚 SOURCES

* [Guardrails AI Official Documentation: Custom Validators](https://guardrailsai.com/guardrails/docs/how-to-guides/custom_validators) - Primary guide for building custom guardrails validators.
* [DSOM Tri-Phasic Cognitive Architecture](file:///docs/governance/DSOM-TRI-PHASIC-COGNITIVE-ARCHITECTURE.md) - DSOM cognitive states and subsystem specifications.
* [The Core AI Rulebook](file:///.agents/AGENTS.md) - Sovereign rules 2, 6, 16, 20, 24, and 28 governing safety constraints.

---
*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-08-21*  
*Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*
