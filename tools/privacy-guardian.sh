#!/bin/bash

# ==============================================================================
# Protocol    : Deep State of Mind (DSOM) For My AI
# Author      : Harisfazillah Jamel (LinuxMalaysia)
# Timestamp   : 2026-07-12
# License     : GNU General Public License v3.0
# Standard    : UK English | DBP-standard Bahasa Melayu Malaysia (Piawai)
# ==============================================================================
set -e
# ==============================================================================
# 📜 DSOM Privacy Guardian (v1.0)
# 
# Date:    2026-01-08
# Author:  Harisfazillah Jamel (LinuxMalaysia)
# Partner: Generated with the help of Google Gemini
# License: GNU GPL v3.0 or later
# 
# Description:
# Scans the generated DSOM reanimation manifest for sensitive information 
# (IPv4 addresses, API keys, tokens, and local home paths) before it is 
# uploaded to an external AI model.
# ==============================================================================

# 1. Setup Variables
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
DATE_STAMP=$(date +"%Y-%m-%d")
TARGET_FILE="${REPO_ROOT}/sod_manifest_${DATE_STAMP}.txt"

# 2. Check if Manifest Exists
if [ ! -f "$TARGET_FILE" ]; then
    echo "❌ Error: Manifest for today ($DATE_STAMP) not found."
    echo "👉 Please run 'bash tools/reanimate.sh' first."
    exit 1
fi

echo "======================================================================"
echo "🛡️  DSOM PRIVACY GUARDIAN: SECURITY SCAN"
echo "Target: $TARGET_FILE"
echo "======================================================================"

# 3. Define Regex Patterns for Leaks
# Patterns: IPv4, Email, Google API, AWS Key, GitHub Token, Slack Token, Private Key, Home Path
declare -a PATTERNS=(
    "([0-9]{1,3}\.){3}[0-9]{1,3}"                      # IPv4
    "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"   # Email
    "AIza[0-9A-Za-z-_]{35}"                            # Google API
    "AKIA[0-9A-Z]{16}"                                 # AWS Access Key
    "gh[pousr]_[a-zA-Z0-9]{36}"                        # GitHub Token
    "github_pat_[a-zA-Z0-9_]{82}"                      # GitHub Fine-Grained Token
    "sk-[a-zA-Z0-9]{48}"                               # OpenAI Secret
    "xox[bap]-[a-zA-Z0-9-]+"                           # Slack Token
    "-----BEGIN [A-Z]+ PRIVATE KEY-----"               # PEM Private Key
    "\/home\/[a-z0-9_-]+\/"                            # Linux Home Path
)

LEAK_FOUND=0

echo "🔍 Scanning for sensitive patterns via Bash regex..."
for pattern in "${PATTERNS[@]}"; do
    # Search and get line numbers
    FOUND=$(grep -Eon "$pattern" "$TARGET_FILE" || true)
    if [ -n "$FOUND" ]; then
        echo ""
        echo "⚠️  POTENTIAL LEAK DETECTED (Line:Match):"
        echo "$FOUND"
        LEAK_FOUND=1
    fi
done

# 4b. Scanning via guardrails-ai-dsom Python Engine
echo "🔍 Scanning via guardrails-ai-dsom Python Engine..."
if uv run --with-editable "${REPO_ROOT}/tools/guardrails-ai-dsom" python -c "
import sys
from pathlib import Path
from guardrails_dsom import GuardrailsCredentialGuardian

content = Path('${TARGET_FILE}').read_text(encoding='utf-8')
res = GuardrailsCredentialGuardian().validate(content)
if not res.is_valid:
    print(f'GUARDRAIL_BLOCKED: {res.error_message}')
    sys.exit(1)
print('GUARDRAIL_PASS')
"; then
    echo "✅ [PASS] guardrails-ai-dsom Credential Guardian verified clean."
else
    echo "❌ ⚠️  GUARDRAILS-AI-DSOM LEAK DETECTED!"
    LEAK_FOUND=1
fi

echo "----------------------------------------------------------------------"

# 5. Final Report
if [ $LEAK_FOUND -eq 0 ]; then
    echo "✅ SCAN COMPLETE: No common sensitive patterns found."
    echo "🚀 You are clear to upload this manifest for AI reanimation."
else
    echo "❌ SCAN FAILED: Sensitive data detected."
    echo "👉 ACTION: Please edit $TARGET_FILE to mask these details before upload."
fi
echo "======================================================================"

