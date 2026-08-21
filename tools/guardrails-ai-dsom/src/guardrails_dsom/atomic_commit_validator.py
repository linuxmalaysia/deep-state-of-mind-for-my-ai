"""
Guardrail 7: Granular Atomic Git Commit Enforcer
Rule Reference: Rule 4
"""

import re
from typing import Any, Dict, Optional
from guardrails_dsom.base import BaseDSOMValidator, ValidationResult

class GuardrailsAtomicCommitValidator(BaseDSOMValidator):
    name = "dsom/atomic_commit_validator"
    on_fail = "block"

    SEMANTIC_PREFIXES = [
        "feat",
        "fix",
        "docs",
        "style",
        "refactor",
        "perf",
        "test",
        "build",
        "ci",
        "chore",
        "revert",
    ]

    COMMIT_MSG_REGEX = re.compile(
        r"^(" + "|".join(SEMANTIC_PREFIXES) + r")(\([a-zA-Z0-9_\-\.\/]+\))?!?: .+$"
    )

    def validate(self, value: Any, metadata: Optional[Dict[str, Any]] = None) -> ValidationResult:
        cmd_or_msg = str(value).strip()

        # Check 1: Block blanket commit -a / -am
        if re.search(r"git\s+commit\s+-[a-zA-Z]*a", cmd_or_msg):
            return ValidationResult(
                is_valid=False,
                error_message="Rule 4 Violation: Monolithic blanket commit flag (-a / -am) prohibited. Stage granularly via 'git add <files>'.",
                action_taken="blocked",
            )

        # Check 2: If validating a raw commit message
        if not cmd_or_msg.startswith("git "):
            if not self.COMMIT_MSG_REGEX.match(cmd_or_msg):
                return ValidationResult(
                    is_valid=False,
                    error_message=(
                        f"Rule 4 Violation: Commit message '{cmd_or_msg}' does not conform to Conventional Commits "
                        f"(e.g., 'docs(guardrails): add custom validators'). Allowed prefixes: {self.SEMANTIC_PREFIXES}."
                    ),
                    action_taken="blocked",
                )

        return ValidationResult(is_valid=True, corrected_value=cmd_or_msg, action_taken="pass")
