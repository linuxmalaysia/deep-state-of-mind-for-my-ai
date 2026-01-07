#!/bin/bash
# ==============================================================================
# 📜 DSOM Reanimation Manifest Generator (v1.4)
# 
# Date:    2026-01-08
# Author:  Harisfazillah Jamel (LinuxMalaysia)
# Partner: Generated with the help of Google Gemini
# License: GNU GPL v3.0 or later
# 
# Description:
# Aggregates ALL core DSOM artifacts, Git logs, and README. Prompts for manual
# EOD input. Ends with mandatory Handshake instructions to finalize the 
# Start of Day (SOD) reanimation.
# ==============================================================================

# 1. Setup Variables
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
if [ -z "$REPO_ROOT" ]; then
    echo "Error: Not in a Git repository."
    exit 1
fi

DATE_STAMP=$(date +"%Y-%m-%d")
OUTPUT_FILE="${REPO_ROOT}/sod_manifest_${DATE_STAMP}.txt"
BRAIN_DIR="$REPO_ROOT/.agent/brain"
DOCS_DIR="$REPO_ROOT/docs"
README_FILE="$REPO_ROOT/README.md"

# 2. Interactive Input
echo "----------------------------------------------------------------------"
echo "🧠 DSOM Manual State Injection"
echo "----------------------------------------------------------------------"
read -p "❓ Do you have a manual EOD Summary or Master Prompt addition? (y/N): " choice

MANUAL_INPUT=""
if [[ "$choice" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    echo "📝 Enter/Paste your summary/prompt (Press CTRL+D when finished):"
    MANUAL_INPUT=$(cat)
fi

# 3. Define the Gathering Logic
generate_manifest() {
    echo "======================================================================"
    echo "🚀 DSOM START OF DAY REANIMATION MANIFEST"
    echo "Generated on: $(date)"
    echo "Project Root: $REPO_ROOT"
    echo "======================================================================"
    echo ""

    if [ -n "$MANUAL_INPUT" ]; then
        echo "### [0] MANUAL STATE INJECTION (Last Session EOD/Master Prompt)"
        echo "$MANUAL_INPUT"
        echo -e "\n---\n"
    fi

    echo "### [1] PROJECT README (Identity & Overview)"
    [ -f "$README_FILE" ] && cat "$README_FILE" || echo "README.md not found."
    echo -e "\n---\n"

    echo "### [2] MASTER PROTOCOL (The Constitution)"
    cat "$DOCS_DIR/AI-MASTER-PROTOCOL.md"
    echo -e "\n---\n"

    echo "### [3] CURRENT TASK (The Cutting Edge)"
    cat "$BRAIN_DIR/task.md"
    echo -e "\n---\n"

    echo "### [4] FULL WALKTHROUGH (The Complete Narrative History)"
    cat "$BRAIN_DIR/walkthrough.md"
    echo -e "\n---\n"

    echo "### [5] IMPLEMENTATION PLAN (The Roadmap)"
    cat "$BRAIN_DIR/implementation_plan.md"
    echo -e "\n---\n"

    echo "### [6] GIT HISTORY (Last 30 Atomic Commits)"
    git log -n 30 --pretty=format:"%h - %an (%ar): %s"
    echo -e "\n\n---\n"

    echo "### [7] RITUAL OF TRANSITION (Operational Guidance)"
    cat "$DOCS_DIR/RITUAL-OF-TRANSITION.md"
    echo ""
    echo "======================================================================"
    echo "🏁 MANIFEST COMPLETE"
    echo "======================================================================"
    echo ""
    echo "Handshake: Ask the AI: \"Summarize the current Mental Anchor after you have read the file uploaded\""
    echo ""
    echo "⚠️  REMINDER: Upload this manifest file as part of your Start of Day (SOD)."
}

# 4. Execute and Capture
generate_manifest | tee "$OUTPUT_FILE"

echo ""
echo "📝 Manifest also saved to: $OUTPUT_FILE"
echo "🛡️  REMINDER: Run tools/privacy-guardian.sh before sharing this manifest."

