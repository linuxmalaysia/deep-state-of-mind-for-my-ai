"""
Guardrail 8: Skill Token Window Gatekeeper
Rule Reference: Rule 19
"""

from typing import Any, Dict, Optional
from guardrails_dsom.base import BaseDSOMValidator, ValidationResult

class GuardrailsSkillTokenGate(BaseDSOMValidator):
    name = "dsom/skill_token_gate"
    on_fail = "block"

    def __init__(self, max_tokens: int = 4000, on_fail: str = "block", **kwargs):
        super().__init__(on_fail=on_fail, **kwargs)
        self.max_tokens = max_tokens

    def _count_tokens(self, text: str) -> int:
        try:
            import tiktoken
            encoding = tiktoken.get_encoding("cl100k_base")
            return len(encoding.encode(text))
        except ImportError:
            # Approximate token count: ~4 characters per token
            return len(text) // 4

    def validate(self, value: Any, metadata: Optional[Dict[str, Any]] = None) -> ValidationResult:
        text = str(value)
        token_count = self._count_tokens(text)

        if token_count > self.max_tokens:
            return ValidationResult(
                is_valid=False,
                error_message=(
                    f"Rule 19 Violation: Skill content exceeded {self.max_tokens} tokens "
                    f"(actual: {token_count} tokens). Offload reference tables and examples into a references/ subdirectory."
                ),
                action_taken="blocked",
            )

        return ValidationResult(is_valid=True, corrected_value=text, action_taken="pass")
