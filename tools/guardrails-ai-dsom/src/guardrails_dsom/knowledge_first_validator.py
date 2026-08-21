"""
Guardrail 9: Knowledge-First AST Discovery Interceptor
Rule Reference: Rule 20 & Rule 21
"""

from typing import Any, Dict, Optional
from guardrails_dsom.base import BaseDSOMValidator, ValidationResult

class GuardrailsKnowledgeFirstValidator(BaseDSOMValidator):
    name = "dsom/knowledge_first_validator"
    on_fail = "block"

    def validate(self, value: Any, metadata: Optional[Dict[str, Any]] = None) -> ValidationResult:
        meta = metadata or {}
        has_queried_memory = meta.get("has_queried_local_knowledge", False)
        is_terminal_command = meta.get("is_terminal_execution", False)

        if is_terminal_command and not has_queried_memory:
            return ValidationResult(
                is_valid=False,
                error_message=(
                    "Rule 20 & 21 Violation: Local Knowledge-First Discovery Mandate. "
                    "You must search local OKF metadata in .agents/brain/ or docs/ before executing terminal commands."
                ),
                action_taken="blocked",
            )

        return ValidationResult(is_valid=True, corrected_value=value, action_taken="pass")
