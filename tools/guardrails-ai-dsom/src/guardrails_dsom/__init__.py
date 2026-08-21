"""
guardrails_dsom
Public API exports for the 10 DSOM Sovereign Custom Validators.
"""

from guardrails_dsom.base import BaseDSOMValidator, ValidationResult
from guardrails_dsom.okf_bom_validator import GuardrailsOKFBOMValidator
from guardrails_dsom.okf_trust_validator import GuardrailsOKFTrustValidator
from guardrails_dsom.sovereign_signature import GuardrailsSovereignSignatureValidator
from guardrails_dsom.credential_guardian import GuardrailsCredentialGuardian
from guardrails_dsom.uv_gatekeeper import GuardrailsUVExecutionValidator
from guardrails_dsom.byte_cap_validator import GuardrailsByteCapValidator
from guardrails_dsom.atomic_commit_validator import GuardrailsAtomicCommitValidator
from guardrails_dsom.skill_token_gate import GuardrailsSkillTokenGate
from guardrails_dsom.knowledge_first_validator import GuardrailsKnowledgeFirstValidator
from guardrails_dsom.root_cleanliness_validator import GuardrailsRootCleanlinessValidator

# Register with official Guardrails AI framework if present
try:
    from guardrails.validators import register_validator as _register_validator

    _register_validator("dsom/okf_bom_validator", data_type="string")(GuardrailsOKFBOMValidator)
    _register_validator("dsom/okf_trust_validator", data_type="string")(GuardrailsOKFTrustValidator)
    _register_validator("dsom/sovereign_signature", data_type="string")(GuardrailsSovereignSignatureValidator)
    _register_validator("dsom/credential_guardian", data_type="string")(GuardrailsCredentialGuardian)
    _register_validator("dsom/uv_execution_gatekeeper", data_type="string")(GuardrailsUVExecutionValidator)
    _register_validator("dsom/byte_cap_validator", data_type="string")(GuardrailsByteCapValidator)
    _register_validator("dsom/atomic_commit_validator", data_type="string")(GuardrailsAtomicCommitValidator)
    _register_validator("dsom/skill_token_gate", data_type="string")(GuardrailsSkillTokenGate)
    _register_validator("dsom/knowledge_first_validator", data_type="string")(GuardrailsKnowledgeFirstValidator)
    _register_validator("dsom/root_cleanliness_validator", data_type="string")(GuardrailsRootCleanlinessValidator)
except ImportError:
    pass

__all__ = [
    "BaseDSOMValidator",
    "ValidationResult",
    "GuardrailsOKFBOMValidator",
    "GuardrailsOKFTrustValidator",
    "GuardrailsSovereignSignatureValidator",
    "GuardrailsCredentialGuardian",
    "GuardrailsUVExecutionValidator",
    "GuardrailsByteCapValidator",
    "GuardrailsAtomicCommitValidator",
    "GuardrailsSkillTokenGate",
    "GuardrailsKnowledgeFirstValidator",
    "GuardrailsRootCleanlinessValidator",
]
