"""
Guardrail 10: Root Workspace Cleanliness & SaaS Isolation Guard
Rule Reference: Rule 17
"""

import os
from pathlib import Path
from typing import Any, Dict, Optional, List
from guardrails_dsom.base import BaseDSOMValidator, ValidationResult

class GuardrailsRootCleanlinessValidator(BaseDSOMValidator):
    name = "dsom/root_cleanliness_validator"
    on_fail = "block"

    PERMITTED_ROOT_FILES = {
        "README.md",
        "SUMMARY.md",
        "START-HERE.md",
        "AGENTS.md",
        "LEGAL-NOTICE.md",
        "CHANGELOG.md",
        "HISTORY.md",
        "ROADMAP.md",
        "llms.txt",
        "mkdocs.yml",
        ".gitignore",
        "ansible.cfg",
        "render.yaml",
        ".readthedocs.yaml",
        "context7.json",
        "pyproject.toml",
    }

    def validate(self, value: Any, metadata: Optional[Dict[str, Any]] = None) -> ValidationResult:
        file_path_str = str(value).replace("\\", "/")
        path = Path(file_path_str)
        filename = path.name

        # If path has only 1 part (or starts with ./ and has 1 part), it's in the root
        parts = [p for p in path.parts if p not in (".", "/")]
        is_root_file = len(parts) == 1

        if is_root_file and filename not in self.PERMITTED_ROOT_FILES:
            # Check if SaaS verification file (e.g., .well-known)
            if filename.startswith(".well-known") or filename.startswith("context7"):
                return ValidationResult(is_valid=True, corrected_value=file_path_str, action_taken="pass")

            if self.on_fail == "fix":
                # Redirect markdown to docs/ and scripts to tools/
                if filename.endswith(".md"):
                    fixed_path = f"docs/{filename}"
                elif filename.endswith((".py", ".sh", ".ps1")):
                    fixed_path = f"tools/{filename}"
                else:
                    fixed_path = f"docs/{filename}"

                return ValidationResult(
                    is_valid=True,
                    corrected_value=fixed_path,
                    error_message=f"Root cleanliness violation: Auto-routed {filename} to {fixed_path}.",
                    action_taken="fixed",
                )

            return ValidationResult(
                is_valid=False,
                error_message=(
                    f"Rule 17 Violation: Root workspace cleanliness. File '{filename}' is not permitted at repository root. "
                    f"Route documentation to 'docs/' and automation scripts to 'tools/'."
                ),
                action_taken="blocked",
            )

        return ValidationResult(is_valid=True, corrected_value=file_path_str, action_taken="pass")
