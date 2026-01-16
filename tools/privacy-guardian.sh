#!/bin/bash
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
    "sk-[a-zA-Z0-9]{48}"                               # OpenAI Secret
    "xox[bap]-[a-zA-Z0-9-]+"                           # Slack Token
    "-----BEGIN [A-Z]+ PRIVATE KEY-----"               # PEM Private Key
    "\/home\/[a-z0-9_-]+\/"                            # Linux Home Path
)

LEAK_FOUND=0

# 4. Scanning Process
echo "🔍 Scanning for sensitive patterns..."
for pattern in "${PATTERNS[@]}"; do
    # Search and get line numbers
    FOUND=$(grep -Eon "$pattern" "$TARGET_FILE")
    if [ -n "$FOUND" ]; then
        echo ""
        echo "⚠️  POTENTIAL LEAK DETECTED (Line:Match):"
        echo "$FOUND"
        LEAK_FOUND=1
    fi
done

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

