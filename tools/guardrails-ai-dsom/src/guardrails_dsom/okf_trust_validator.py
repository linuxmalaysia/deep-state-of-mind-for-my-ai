"""
Guardrail 2: OKF v0.2 Provenance & Trust Signal Gate
Rule Reference: Rule 6 & Rule 21
"""

import re
from typing import Any, Dict, Optional, List
from guardrails_dsom.base import BaseDSOMValidator, ValidationResult

class GuardrailsOKFTrustValidator(BaseDSOMValidator):
    name = "dsom/okf_trust_validator"
    on_fail = "block"

    REQUIRED_V02_FIELDS = [
        "okf_version",
        "type",
        "title",
        "timestamp",
        "topics",
        "sources",
        "generated",
        "verified",
        "status",
        "stale_after",
    ]

    def validate(self, value: Any, metadata: Optional[Dict[str, Any]] = None) -> ValidationResult:
        text = str(value)
        if not text.startswith("---"):
            return ValidationResult(
                is_valid=False,
                error_message="Document missing YAML frontmatter block.",
                action_taken="blocked",
            )

        try:
            parts = text.split("---", 2)
            if len(parts) < 3:
                return ValidationResult(
                    is_valid=False,
                    error_message="Unclosed YAML frontmatter fence.",
                    action_taken="blocked",
                )

            header_content = parts[1]
            missing_fields = []
            
            # Check version
            if "okf_version: 0.2" in header_content:
                for field in self.REQUIRED_V02_FIELDS:
                    if not re.search(rf"^{field}\s*:", header_content, re.MULTILINE):
                        missing_fields.append(field)

                if missing_fields:
                    return ValidationResult(
                        is_valid=False,
                        error_message=f"OKF v0.2 document missing mandatory trust signals: {missing_fields}",
                        action_taken="blocked",
                    )

            return ValidationResult(is_valid=True, corrected_value=text, action_taken="pass")
        except Exception as exc:
            return ValidationResult(
                is_valid=False,
                error_message=f"Error validating OKF trust signals: {str(exc)}",
                action_taken="blocked",
            )
