"""
Unit tests for the guardrails_dsom package.
Validates all 10 DSOM Sovereign Custom Validators.
"""

import os
import sys
from datetime import datetime, timezone
import pytest

# Add src to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from guardrails_dsom import (
    GuardrailsOKFBOMValidator,
    GuardrailsOKFTrustValidator,
    GuardrailsSovereignSignatureValidator,
    GuardrailsCredentialGuardian,
    GuardrailsUVExecutionValidator,
    GuardrailsByteCapValidator,
    GuardrailsAtomicCommitValidator,
    GuardrailsSkillTokenGate,
    GuardrailsKnowledgeFirstValidator,
    GuardrailsRootCleanlinessValidator,
)


def test_guardrail_1_okf_bom_stripper():
    val = GuardrailsOKFBOMValidator(on_fail="fix")
    
    # Text with leading BOM
    raw_text = "\ufeff---\nokf_version: 0.2\ntitle: Test\n---\n# Content"
    res = val.validate(raw_text)
    assert res.is_valid is True
    assert res.action_taken == "fixed"
    assert not res.corrected_value.startswith("\ufeff")
    assert res.corrected_value.startswith("---\n")

    # Text missing fence
    raw_no_fence = "title: Test\n# Content"
    res2 = val.validate(raw_no_fence)
    assert res2.is_valid is True
    assert res2.corrected_value.startswith("---\n")


def test_guardrail_2_okf_trust_validator():
    val = GuardrailsOKFTrustValidator(on_fail="block")
    
    # Valid OKF v0.2
    valid_okf = """---
okf_version: 0.2
type: documentation
title: "Test"
timestamp: "2026-08-22T00:00:00Z"
topics: ["dsom", "test"]
sources: ["local"]
generated: "antigravity"
verified: true
status: "approved"
stale_after: "2027-08-22T00:00:00Z"
---
# Content"""
    res = val.validate(valid_okf)
    assert res.is_valid is True
    assert res.action_taken == "pass"

    # Missing trust fields in v0.2
    invalid_okf = """---
okf_version: 0.2
title: "Test"
---
# Content"""
    res2 = val.validate(invalid_okf)
    assert res2.is_valid is False
    assert res2.action_taken == "blocked"
    assert "missing mandatory trust signals" in res2.error_message


def test_guardrail_3_sovereign_signature():
    val = GuardrailsSovereignSignatureValidator(on_fail="fix")
    today_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # Text with stale date
    stale_text = """# Header
Content

---
*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-01-01*
*Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*"""
    res = val.validate(stale_text)
    assert res.is_valid is True
    assert res.action_taken == "fixed"
    assert f"| {today_str}*" in res.corrected_value

    # Text missing signature completely
    no_sig = "# Header\nContent"
    res2 = val.validate(no_sig)
    assert res2.is_valid is True
    assert res2.action_taken == "fixed"
    assert f"| {today_str}*" in res2.corrected_value


def test_guardrail_4_credential_guardian():
    val = GuardrailsCredentialGuardian(on_fail="block")

    # GitHub token
    leak1 = "Here is my secret token: ghp_123456789012345678901234567890123456"
    res1 = val.validate(leak1)
    assert res1.is_valid is False
    assert res1.action_taken == "blocked"

    # RSA Private Key
    leak2 = "-----BEGIN RSA PRIVATE KEY-----\nMIIEowIBAAKCAQEA0...\n-----END RSA PRIVATE KEY-----"
    res2 = val.validate(leak2)
    assert res2.is_valid is False
    assert res2.action_taken == "blocked"

    # Safe text
    safe = "This is safe text without secrets."
    res3 = val.validate(safe)
    assert res3.is_valid is True


def test_guardrail_5_uv_execution_gatekeeper():
    val = GuardrailsUVExecutionValidator(on_fail="fix")

    # Prohibited pip install
    cmd1 = "pip install requests"
    res1 = val.validate(cmd1)
    assert res1.is_valid is True
    assert res1.action_taken == "fixed"
    assert res1.corrected_value == "uv add requests"

    # Prohibited python call
    cmd2 = "python script.py"
    res2 = val.validate(cmd2)
    assert res2.is_valid is True
    assert res2.action_taken == "fixed"
    assert res2.corrected_value == "uv run script.py"

    # Block mode
    val_block = GuardrailsUVExecutionValidator(on_fail="block")
    res3 = val_block.validate("pip install requests")
    assert res3.is_valid is False
    assert res3.action_taken == "blocked"


def test_guardrail_6_byte_cap_validator():
    val = GuardrailsByteCapValidator(max_bytes=100, on_fail="fix")

    large_text = "A" * 250
    res = val.validate(large_text)
    assert res.is_valid is True
    assert res.action_taken == "fixed"
    assert "TRUNCATED BY DSOM BYTE-CAP GUARDRAIL" in res.corrected_value
    assert len(res.corrected_value.encode("utf-8")) < 250 + 200


def test_guardrail_7_atomic_commit_validator():
    val = GuardrailsAtomicCommitValidator(on_fail="block")

    # Block blanket commit
    cmd1 = "git commit -am 'quick fix'"
    res1 = val.validate(cmd1)
    assert res1.is_valid is False
    assert res1.action_taken == "blocked"

    # Valid conventional commit message
    msg1 = "feat(guardrails): add custom validator suite"
    res2 = val.validate(msg1)
    assert res2.is_valid is True

    # Invalid non-semantic commit message
    msg2 = "fixed stuff and updated docs"
    res3 = val.validate(msg2)
    assert res3.is_valid is False
    assert res3.action_taken == "blocked"


def test_guardrail_8_skill_token_gate():
    val = GuardrailsSkillTokenGate(max_tokens=50, on_fail="block")

    short_skill = "This is a short skill instruction."
    assert val.validate(short_skill).is_valid is True

    huge_skill = "word " * 200
    res = val.validate(huge_skill)
    assert res.is_valid is False
    assert res.action_taken == "blocked"
    assert "exceeded 50 tokens" in res.error_message


def test_guardrail_9_knowledge_first_validator():
    val = GuardrailsKnowledgeFirstValidator(on_fail="block")

    # Terminal command without local search
    res1 = val.validate("cat /etc/hosts", metadata={"is_terminal_execution": True, "has_queried_local_knowledge": False})
    assert res1.is_valid is False
    assert res1.action_taken == "blocked"

    # Terminal command after local search
    res2 = val.validate("cat /etc/hosts", metadata={"is_terminal_execution": True, "has_queried_local_knowledge": True})
    assert res2.is_valid is True


def test_guardrail_10_root_cleanliness_validator():
    val = GuardrailsRootCleanlinessValidator(on_fail="fix")

    # Permitted root file
    assert val.validate("README.md").is_valid is True
    assert val.validate("START-HERE.md").is_valid is True

    # Rogue root file auto-routed
    res1 = val.validate("MY-GUIDE.md")
    assert res1.is_valid is True
    assert res1.action_taken == "fixed"
    assert res1.corrected_value == "docs/MY-GUIDE.md"

    # Rogue script auto-routed
    res2 = val.validate("deploy.sh")
    assert res2.is_valid is True
    assert res2.action_taken == "fixed"
    assert res2.corrected_value == "tools/deploy.sh"
