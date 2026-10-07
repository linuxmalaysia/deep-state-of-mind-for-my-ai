"""
Guardrail 6: Byte-Capped Terminal Output Interceptor
Rule Reference: Rule 10
"""

from typing import Any

from guardrails_dsom.base import BaseDSOMValidator, ValidationResult


class GuardrailsByteCapValidator(BaseDSOMValidator):
    name = "dsom/byte_cap_validator"
    on_fail = "fix"

    def __init__(self, max_bytes: int = 4000, on_fail: str = "fix", **kwargs):
        super().__init__(on_fail=on_fail, **kwargs)
        self.max_bytes = max_bytes

    def validate(self, value: Any, metadata: dict[str, Any] | None = None) -> ValidationResult:
        """Check the UTF-8 byte length of value converted to text.

        Text at or below max_bytes passes unchanged. Larger text is truncated
        in fix mode, dropping any partial trailing character and appending a
        notice outside the byte budget. Other modes return blocked. metadata
        is unused.

        Raises:
            UnicodeEncodeError: If the text contains unpaired surrogates.
        """
        text = str(value)
        encoded = text.encode("utf-8")

        if len(encoded) > self.max_bytes:
            if self.on_fail == "fix":
                truncated_bytes = encoded[: self.max_bytes]
                # Decode ignoring broken trailing multibyte character
                truncated_text = truncated_bytes.decode("utf-8", errors="ignore")
                capped_output = (
                    truncated_text
                    + f"\n\n[TRUNCATED BY DSOM BYTE-CAP GUARDRAIL: Original size was {len(encoded)} bytes (limit: {self.max_bytes})]"
                )
                return ValidationResult(
                    is_valid=True,
                    corrected_value=capped_output,
                    error_message=f"Output exceeded byte cap ({len(encoded)} > {self.max_bytes} bytes); truncated.",
                    action_taken="fixed",
                )
            return ValidationResult(
                is_valid=False,
                error_message=f"Rule 10 Violation: Output exceeded byte cap ({len(encoded)} > {self.max_bytes} bytes).",
                action_taken="blocked",
            )

        return ValidationResult(is_valid=True, corrected_value=text, action_taken="pass")
