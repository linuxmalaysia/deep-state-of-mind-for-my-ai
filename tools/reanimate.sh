#!/bin/bash
set -euo pipefail
# ==============================================================================
# 📜 DSOM Reanimation Manifest Generator (v2.1 - GitOps + AIOps + Ansible)
#
# Author:  Harisfazillah Jamel (LinuxMalaysia)
# Partner: Generated with assistance from Google Antigravity
# License: GNU GPL v3.0 or later
#
# Description:
#   Aggregates ALL core DSOM artifacts including Cognitive Twin Protocol and
#   Ansible inventory. Features an interactive multi-line input for EOD summaries.
#   Generates a sod_manifest_YYYY-MM-DD.txt for AI session reanimation.
#
# Usage:
#   bash tools/reanimate.sh
#   Upload the resulting sod_manifest_*.txt in your AI session.
# ==============================================================================

# Colors
CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# 1. Setup Variables
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || true)
if [ -z "${REPO_ROOT}" ]; then
    echo -e "${RED}[ERROR] Not in a Git repository. Run from the project root.${NC}"
    exit 1
fi

DATE_STAMP=$(date +"%Y-%m-%d")
OUTPUT_FILE="${REPO_ROOT}/sod_manifest_${DATE_STAMP}.txt"
BRAIN_DIR="$REPO_ROOT/.agent/brain"
DOCS_DIR="$REPO_ROOT/docs"
README_FILE="$REPO_ROOT/README.md"
VERSION="v2.1"

echo -e "${CYAN}======================================================================"
echo -e "  🚀 DSOM Reanimation Manifest Generator $VERSION"
echo -e "  Output: sod_manifest_${DATE_STAMP}.txt"
echo -e "======================================================================${NC}"
echo ""

# 2. Validate required brain files
MISSING=0
for f in task.md walkthrough.md; do
    if [ ! -f "$BRAIN_DIR/$f" ]; then
        echo -e "${YELLOW}[WARNING] Missing brain artifact: $BRAIN_DIR/$f${NC}"
        MISSING=1
    fi
done
if [ $MISSING -eq 1 ]; then
    echo -e "${YELLOW}Hint: Run bash tools/init-brain.sh to initialise brain artifacts.${NC}"
fi

# 3. Interactive Input with Clear Instructions
echo "----------------------------------------------------------------------"
echo "🧠 DSOM Manual State Injection"
echo "----------------------------------------------------------------------"
read -r -p "❓ Do you have a manual EOD Summary or Master Prompt addition? (y/N): " choice

MANUAL_INPUT=""
if [[ "$choice" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    echo ""
    echo "📝 PASTE/TYPE YOUR CONTENT BELOW:"
    echo "----------------------------------------------------------------------"
    echo "👉 [INSTRUCTION]: When finished, press [ENTER] then [CTRL+D] to save."
    echo "----------------------------------------------------------------------"
    MANUAL_INPUT=$(cat)
    echo "----------------------------------------------------------------------"
    echo -e "${GREEN}✅ Input captured successfully.${NC}"
fi

# 4. Helper — safe cat
filecat() {
    local path="$1"
    local fallback="${2:-[MISSING] File not found: $path}"
    if [ -f "$path" ]; then
        cat "$path"
    else
        echo "$fallback"
    fi
}

# 5. Generate the manifest
generate_manifest() {
    local date_now
    date_now=$(date)

    echo "======================================================================"
    echo "🚀 DSOM START OF DAY REANIMATION MANIFEST — $VERSION"
    echo "Generated on: $date_now"
    echo "Project Root: $REPO_ROOT"
    echo "======================================================================"
    echo ""
    echo "------------------------------------------------------------"
    echo " 🧠 REANIMATING: Deep State of Mind (DSOM) For My AI Protocol"
    echo " 📍 NODE: $(hostname) | USER: $(whoami)"
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

    # Manual Injection
    if [ -n "$MANUAL_INPUT" ]; then
        echo "### [0] MANUAL STATE INJECTION (Last Session EOD/Master Prompt)"
        echo "$MANUAL_INPUT"
        echo -e "\n---\n"
    fi

    echo "### [1] PROJECT README (Identity & Overview)"
    filecat "$README_FILE" "README.md not found."
    echo -e "\n---\n"

    echo "### [2] SYSTEM TELEMETRY (Physical Constraints)"
    echo "- **OS:** $(uname -sr)"
    echo "- **Host:** $(hostname)"
    echo "- **User:** $(whoami)"
    echo "- **Shell:** $SHELL"
    echo "- **Date:** $date_now"
    echo -e "\n---\n"

    echo "### [3] MASTER PROTOCOL (The Constitution)"
    filecat "$DOCS_DIR/AI-MASTER-PROTOCOL.md"
    echo -e "\n---\n"

    echo "### [4] COGNITIVE TWIN PROTOCOL (Project Identity Card)"
    filecat "$DOCS_DIR/AI-COGNITIVE-TWIN-PROTOCOL.md" \
        "[MISSING] docs/AI-COGNITIVE-TWIN-PROTOCOL.md not found. Run HOWTO-ADOPT-DSOM.md."
    echo -e "\n---\n"

    echo "### [5] CURRENT TASK (The Cutting Edge)"
    filecat "$BRAIN_DIR/task.md"
    echo -e "\n---\n"

    echo "### [6] FULL WALKTHROUGH (The Complete Narrative History)"
    filecat "$BRAIN_DIR/walkthrough.md"
    echo -e "\n---\n"

    echo "### [7] IMPLEMENTATION PLAN (The Roadmap)"
    filecat "$BRAIN_DIR/implementation_plan.md"
    echo -e "\n---\n"

    echo "### [8] PROJECT STRUCTURE (The Spatial Map)"
    echo "Files in repository (excluding hidden/git):"
    git -C "$REPO_ROOT" ls-tree -r HEAD --name-only | while read -r file; do echo "  - $file"; done
    echo -e "\n---\n"

    echo "### [9] GIT HISTORY"
    echo "#### Recent Activity (Last 48 Hours)"
    git -C "$REPO_ROOT" log --since="48 hours ago" --pretty=format:"%h - %an (%ar): %s"
    echo ""
    echo ""
    echo "#### Context (Last 30 Commits)"
    git -C "$REPO_ROOT" log -n 30 --pretty=format:"%h - %an (%ar): %s"
    echo -e "\n\n---\n"

    echo "### [10] SOD RITUAL (The Cognitive Handshake — Summary)"
    if [ -f "$DOCS_DIR/SOD-RITUAL.md" ]; then
        head -n 60 "$DOCS_DIR/SOD-RITUAL.md"
        echo ""
        echo "... (see full doc: docs/SOD-RITUAL.md)"
    else
        echo "[MISSING] docs/SOD-RITUAL.md"
    fi
    echo -e "\n\n---\n"

    echo "### [11] RITUAL OF TRANSITION (Cross-AI Handover — Summary)"
    if [ -f "$DOCS_DIR/RITUAL-OF-TRANSITION.md" ]; then
        head -n 60 "$DOCS_DIR/RITUAL-OF-TRANSITION.md"
        echo ""
        echo "... (see full doc: docs/RITUAL-OF-TRANSITION.md)"
    else
        echo "[MISSING] docs/RITUAL-OF-TRANSITION.md"
    fi
    echo -e "\n\n---\n"

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
        echo ""
        echo "... (see full doc: docs/GITOPS-AIOPS-ANSIBLE-STRATEGY.md)"
    else
        echo "[SKIP] GITOPS-AIOPS-ANSIBLE-STRATEGY.md not found."
    fi
    echo ""
    echo "======================================================================"
    echo "🏁 MANIFEST COMPLETE — DSOM For My AI Protocol v6.1"
    echo "======================================================================"
    echo ""
    echo "Handshake: Ask the AI:"
    echo '  "Summarise the current Mental Anchor from .agent/brain/walkthrough.md.'
    echo '   Confirm the 4-Tier environment. State: Sovereign State Synchronised when ready."'
    echo ""
    echo "⚠️  REMINDER: Upload this manifest file as part of your Start of Day (SOD)."
}

# 6. Execute and Capture
generate_manifest | tee "$OUTPUT_FILE"

echo ""
echo -e "${GREEN}📝 Manifest saved to: $OUTPUT_FILE${NC}"
echo -e "${YELLOW}🛡️  REMINDER: Run tools/privacy-guardian.sh before sharing this manifest.${NC}"
echo ""
