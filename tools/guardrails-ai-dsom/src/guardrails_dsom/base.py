"""
guardrails_dsom.base
Base classes and result models for DSOM custom validators.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, Optional, Literal

@dataclass
class ValidationResult:
    """Unified validation result object supporting both fix and block actions."""
    is_valid: bool
    corrected_value: Optional[Any] = None
    error_message: Optional[str] = None
    action_taken: Literal["pass", "fixed", "blocked", "reask"] = "pass"

    @property
    def value(self) -> Any:
        return self.corrected_value

class BaseDSOMValidator(ABC):
    """
    Abstract Base Class for all DSOM Native & Guardrails AI Validators.
    Provides standard library execution with zero required external dependencies.
    """

    name: str = "base_dsom_validator"
    on_fail: Literal["fix", "block", "reask", "exception"] = "block"

    def __init__(self, on_fail: Optional[str] = None, **kwargs):
        if on_fail:
            self.on_fail = on_fail
        self.kwargs = kwargs

    @abstractmethod
    def validate(self, value: Any, metadata: Optional[Dict[str, Any]] = None) -> ValidationResult:
        """Validate input value and return ValidationResult."""
        pass

    def __call__(self, value: Any, metadata: Optional[Dict[str, Any]] = None) -> ValidationResult:
        return self.validate(value, metadata)
