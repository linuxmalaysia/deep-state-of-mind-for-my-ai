"""
Guardrail 3: Sovereign Signature & Modification Date Auditor
Rule Reference: Rule 13
"""

import re
from datetime import datetime, timezone
from typing import Any

from guardrails_dsom.base import BaseDSOMValidator, ValidationResult


class GuardrailsSovereignSignatureValidator(BaseDSOMValidator):
    name = "dsom/sovereign_signature"
    on_fail = "fix"

    SIGNATURE_REGEX = re.compile(
        r"\*Deep State of Mind \(DSOM\) For My AI Protocol \| Harisfazillah Jamel \(LinuxMalaysia\) \| (\d{4}-\d{2}-\d{2})\*"
    )

    def validate(self, value: Any, metadata: dict[str, Any] | None = None) -> ValidationResult:
        """Check that the first matching DSOM signature has today's UTC date.

        In fix mode, append a missing footer or update all matching signatures
        when the first has a different date. Other modes return blocked for
        these cases. Passing or fixed results contain the resulting text.
        No files are modified, and metadata is unused.
        """
        text = str(value)
        today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        expected_footer = (
            f"*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | {today_str}*\n"
            f"*Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*"
        )

        match = self.SIGNATURE_REGEX.search(text)
        if not match:
            if self.on_fail == "fix":
                fixed_text = text.rstrip() + "\n\n---\n" + expected_footer + "\n"
                return ValidationResult(
                    is_valid=True,
                    corrected_value=fixed_text,
                    error_message="Missing DSOM sovereign signature; auto-appended.",
                    action_taken="fixed",
                )
            return ValidationResult(
                is_valid=False,
                error_message="Document missing mandatory DSOM sovereign footer signature.",
                action_taken="blocked",
            )

        # Match exists; check if date is fresh
        found_date = match.group(1)
        if found_date != today_str:
            if self.on_fail == "fix":
                fixed_text = self.SIGNATURE_REGEX.sub(
                    f"*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | {today_str}*",
                    text,
                )
                return ValidationResult(
                    is_valid=True,
                    corrected_value=fixed_text,
                    error_message=f"Signature date stale ({found_date}); auto-updated to {today_str}.",
                    action_taken="fixed",
                )
            return ValidationResult(
                is_valid=False,
                error_message=f"Signature date stale ({found_date}); expected {today_str}.",
                action_taken="blocked",
            )

        return ValidationResult(is_valid=True, corrected_value=text, action_taken="pass")
