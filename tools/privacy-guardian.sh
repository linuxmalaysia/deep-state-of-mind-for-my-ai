#!/bin/bash
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
# Patterns: IPv4, Google API, Generic Secret, Slack Token, Local User Path
declare -a PATTERNS=(
    "([0-9]{1,3}\.){3}[0-9]{1,3}"      
    "AIza[0-9A-Za-z-_]{35}"            
    "sk-[a-zA-Z0-9]{48}"               
    "xox[bap]-[a-zA-Z0-9-]+"           
    "\/home\/[a-z0-9_-]+\/"            
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

