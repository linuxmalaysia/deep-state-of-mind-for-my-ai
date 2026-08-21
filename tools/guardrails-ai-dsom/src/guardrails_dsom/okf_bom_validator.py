"""
Guardrail 1: OKF Frontmatter & UTF-8 BOM Stripper
Rule Reference: Rule 2 & Rule 25
"""

from typing import Any, Dict, Optional
from guardrails_dsom.base import BaseDSOMValidator, ValidationResult

class GuardrailsOKFBOMValidator(BaseDSOMValidator):
    name = "dsom/okf_bom_validator"
    on_fail = "fix"

    def validate(self, value: Any, metadata: Optional[Dict[str, Any]] = None) -> ValidationResult:
        text = str(value)
        action_taken = "pass"
        has_fix = False

        # 1. Check for leading UTF-8 BOM
        if text.startswith("\ufeff"):
            text = text.lstrip("\ufeff")
            has_fix = True
            action_taken = "fixed"

        # 2. Check for frontmatter fence
        if not (text.startswith("---\n") or text.startswith("---\r\n")):
            if self.on_fail == "fix":
                # Prepend frontmatter delimiter if completely missing
                text = "---\n" + text
                return ValidationResult(
                    is_valid=True,
                    corrected_value=text,
                    error_message="Missing YAML frontmatter fence; auto-prepended.",
                    action_taken="fixed"
                )
            return ValidationResult(
                is_valid=False,
                error_message="Document must start with OKF frontmatter fence ('---').",
                action_taken="blocked"
            )

        if has_fix:
            return ValidationResult(
                is_valid=True,
                corrected_value=text,
                error_message="Leading UTF-8 BOM detected and stripped.",
                action_taken="fixed"
            )

        return ValidationResult(is_valid=True, corrected_value=text, action_taken="pass")
