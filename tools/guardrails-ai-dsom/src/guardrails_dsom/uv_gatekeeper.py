"""
Guardrail 5: Isolated Python Execution & Tool Gatekeeper
Rule Reference: Rule 16
"""

import re
from typing import Any, Dict, Optional
from guardrails_dsom.base import BaseDSOMValidator, ValidationResult

class GuardrailsUVExecutionValidator(BaseDSOMValidator):
    name = "dsom/uv_execution_gatekeeper"
    on_fail = "block"

    def validate(self, value: Any, metadata: Optional[Dict[str, Any]] = None) -> ValidationResult:
        cmd = str(value).strip()

        # Check for prohibited commands
        if re.search(r"(^|\s|&&|;)pip\s+install", cmd):
            if self.on_fail == "fix":
                fixed = re.sub(r"(^|\s|&&|;)pip\s+install", r"\1uv add", cmd)
                return ValidationResult(
                    is_valid=True,
                    corrected_value=fixed,
                    error_message="Prohibited raw 'pip install' converted to 'uv add'.",
                    action_taken="fixed",
                )
            return ValidationResult(
                is_valid=False,
                error_message="Rule 16 Violation: Raw 'pip install' prohibited. Use 'uv add' or 'uv run --with'.",
                action_taken="blocked",
            )

        if re.search(r"(^|\s|&&|;)python(3)?\s+([a-zA-Z0-9_\-\./]+\.py)", cmd):
            if self.on_fail == "fix":
                fixed = re.sub(r"(^|\s|&&|;)python(3)?\s+", r"\1uv run ", cmd)
                return ValidationResult(
                    is_valid=True,
                    corrected_value=fixed,
                    error_message="Prohibited unmanaged 'python' converted to 'uv run'.",
                    action_taken="fixed",
                )
            return ValidationResult(
                is_valid=False,
                error_message="Rule 16 Violation: Raw unmanaged 'python' execution prohibited. Use 'uv run <script>'.",
                action_taken="blocked",
            )

        return ValidationResult(is_valid=True, corrected_value=cmd, action_taken="pass")
