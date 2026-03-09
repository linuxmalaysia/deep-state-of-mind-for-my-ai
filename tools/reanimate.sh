#!/bin/bash
set -e
# ==============================================================================
# 📜 DSOM Reanimation Manifest Generator (v2.0 - GitOps + AIOps + Ansible)
# 
# Date:    2026-03-09
# Author:  Harisfazillah Jamel (LinuxMalaysia)
# Partner: Generated with the help of Google Gemini
# License: GNU GPL v3.0 or later
# 
# Description:
# Aggregates ALL core DSOM artifacts including Cognitive Twin Protocol and
# Ansible inventory. Features an interactive multi-line input for EOD summaries.
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

# 2. Interactive Input with Clear Instructions
echo "----------------------------------------------------------------------"
echo "🧠 DSOM Manual State Injection"
echo "----------------------------------------------------------------------"
read -p "❓ Do you have a manual EOD Summary or Master Prompt addition? (y/N): " choice

MANUAL_INPUT=""
if [[ "$choice" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    echo ""
    echo "📝 PASTE/TYPE YOUR CONTENT BELOW:"
    echo "----------------------------------------------------------------------"
    echo "👉 [INSTRUCTION]: When finished, press [ENTER] then [CTRL+D] to save."
    echo "----------------------------------------------------------------------"
    
    # Capture multi-line input
    MANUAL_INPUT=$(cat)
    
    echo "----------------------------------------------------------------------"
    echo "✅ Input captured successfully."
fi

# 3. Define the Gathering Logic
generate_manifest() {
    echo "======================================================================"
    echo "🚀 DSOM START OF DAY REANIMATION MANIFEST"
    echo "Generated on: $(date)"
    echo "Project Root: $REPO_ROOT"
    echo "======================================================================"
    echo ""
# ==============================================================================
# 📜 DSOM Reanimation Script
# Protocol: Deep State of Mind (DSOM) For My AI Protocol
# ==============================================================================
    echo "------------------------------------------------------------"
    echo " 🧠 REANIMATING: Deep State of Mind (DSOM) For My AI Protocol"
    echo " 📍 NODE: $(hostname) | USER: Harisfazillah Jamel"
    echo "------------------------------------------------------------"
    echo ""
    echo "## 🛡️ CRISP STRATEGY MANDATE"
    echo "- **C**ontext Awareness: Read brain artifacts first."
    echo "- **R**eview & Record: Commit atomic changes; update walkthrough.md."
    echo "- **I**teration: Incremental progress; no monolithic refactors."
    echo "- **S**ingle-purpose: Focus on one sub-task at a time."
    echo "- **P**artnership: AI acts as a Senior Architect Digital Twin (Service Relationship)."
    echo ""

    # Sunday Audit Check
    DAY_OF_WEEK=$(date +%u)
    if [ "$DAY_OF_WEEK" -eq 7 ]; then
        echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        echo "🚨 SUNDAY AUDIT PROTOCOL ACTIVE"
        echo "   Today is Sunday. You MUST perform the Weekly Human Refresh."
        echo "   Refer to task.md -> 'Sunday Audit Protocol' for the checklist."
        echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        echo ""
    fi

    if [ -n "$MANUAL_INPUT" ]; then
        echo "### [0] MANUAL STATE INJECTION (Last Session EOD/Master Prompt)"
        echo "$MANUAL_INPUT"
        echo -e "\n---\n"
    fi

    echo "### [1] PROJECT README (Identity & Overview)"
    [ -f "$README_FILE" ] && cat "$README_FILE" || echo "README.md not found."
    echo -e "\n---\n"

    echo "### [2] SYSTEM TELEMETRY (Physical Constraints)"
    echo "- **OS:** $(uname -sr)"
    echo "- **Shell:** $SHELL"
    echo "- **Date:** $(date)"
    echo -e "\n---\n"

    echo "### [3] MASTER PROTOCOL (The Constitution)"
    cat "$DOCS_DIR/AI-MASTER-PROTOCOL.md"
    echo -e "\n---\n"

    echo "### [4] CURRENT TASK (The Cutting Edge)"
    cat "$BRAIN_DIR/task.md"
    echo -e "\n---\n"

    echo "### [5] FULL WALKTHROUGH (The Complete Narrative History)"
    cat "$BRAIN_DIR/walkthrough.md"
    echo -e "\n---\n"

    echo "### [6] IMPLEMENTATION PLAN (The Roadmap)"
    cat "$BRAIN_DIR/implementation_plan.md"
    echo -e "\n---\n"

    echo "### [7] PROJECT STRUCTURE (The Spatial Map)"
    echo "Files in repository (excluding hidden/git):"
    git ls-tree -r HEAD --name-only | while read file; do echo "  - $file"; done
    echo -e "\n---\n"

    echo "### [8] GIT HISTORY"
    echo "#### Recent Activity (Last 48 Hours)"
    git log --since="48 hours ago" --pretty=format:"%h - %an (%ar): %s"
    echo -e "\n"
    echo "#### Context (Last 30 Commits)"
    git log -n 30 --pretty=format:"%h - %an (%ar): %s"
    echo -e "\n\n---\n"

    echo "### [9] SOD RITUAL (The Cognitive Handshake)"
    cat "$DOCS_DIR/SOD-RITUAL.md"
    echo -e "\n\n---\n"

    echo "### [10] RITUAL OF TRANSITION (Operational Guidance)"
    cat "$DOCS_DIR/RITUAL-OF-TRANSITION.md"
    echo -e "\n\n---\n"

    # --- v2.0 NEW SECTIONS ---

    echo "### [11] COGNITIVE TWIN PROTOCOL (Project Identity Card)"
    if [ -f "$DOCS_DIR/AI-COGNITIVE-TWIN-PROTOCOL.md" ]; then
        cat "$DOCS_DIR/AI-COGNITIVE-TWIN-PROTOCOL.md"
    else
        echo "[MISSING] docs/AI-COGNITIVE-TWIN-PROTOCOL.md not found."
        echo "Create this file from the DSOM skeleton template for this project."
    fi
    echo -e "\n---\n"

    echo "### [12] ANSIBLE INVENTORY (Node Topology)"
    if [ -f "$REPO_ROOT/inventory/hosts.yml" ]; then
        echo "⚠️  NOTE: This file may contain hostnames/IPs. Run privacy-guardian.sh before sharing."
        cat "$REPO_ROOT/inventory/hosts.yml"
    else
        echo "[SKIP] inventory/hosts.yml not found (non-infra project or Ansible not yet configured)."
    fi
    echo -e "\n---\n"

    echo "### [13] GITOPS STRATEGY (Three-Pillar Doctrine Summary)"
    if [ -f "$DOCS_DIR/GITOPS-AIOPS-ANSIBLE-STRATEGY.md" ]; then
        head -n 60 "$DOCS_DIR/GITOPS-AIOPS-ANSIBLE-STRATEGY.md"
        echo -e "\n... (see full doc for details)"
    else
        echo "[SKIP] GITOPS-AIOPS-ANSIBLE-STRATEGY.md not found."
    fi
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
echo "📝 Manifest saved to: $OUTPUT_FILE"
echo "🛡️  REMINDER: Run tools/privacy-guardian.sh before sharing this manifest."

