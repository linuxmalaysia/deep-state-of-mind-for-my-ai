"""
Guardrail 4: Defensive Credential & Secret Interceptor
Rule Reference: Rule 24
"""

import re
from typing import Any, Dict, Optional, List
from guardrails_dsom.base import BaseDSOMValidator, ValidationResult

class GuardrailsCredentialGuardian(BaseDSOMValidator):
    name = "dsom/credential_guardian"
    on_fail = "block"

    PATTERNS: List[tuple[str, re.Pattern]] = [
        ("GitHub Classic PAT", re.compile(r"ghp_[a-zA-Z0-9]{36}")),
        ("GitHub Fine-grained PAT", re.compile(r"github_pat_[a-zA-Z0-9_]{82}")),
        ("GitLab PAT", re.compile(r"glpat-[a-zA-Z0-9\-]{20}")),
        ("AWS Access Key", re.compile(r"AKIA[0-9A-Z]{16}")),
        ("Private Key Fence", re.compile(r"-----BEGIN (RSA|OPENSSH|EC|DSA) PRIVATE KEY-----")),
        ("Slack Bot Token", re.compile(r"xoxb-[0-9]{11}-[0-9]{11}-[a-zA-Z0-9]{24}")),
    ]

    def validate(self, value: Any, metadata: Optional[Dict[str, Any]] = None) -> ValidationResult:
        text = str(value)
        for label, pattern in self.PATTERNS:
            if pattern.search(text):
                return ValidationResult(
                    is_valid=False,
                    error_message=f"Rule 24 Violation: Sensitive credential detected ({label}).",
                    action_taken="blocked",
                )
        return ValidationResult(is_valid=True, corrected_value=text, action_taken="pass")
