#!/bin/bash
set -e
# ==============================================================================
# 📜 DSOM Claude Reanimation Generator (v2.0 - GitOps + AIOps + Ansible)
#
# Author:  Harisfazillah Jamel (LinuxMalaysia)
# Partner: Generated with assistance from Google Antigravity
# License: GNU GPL v3.0 or later
#
# Description:
#   Generates a targeted context file (DSOM-CLAUDE-INIT.md) for upload to
#   Claude.ai Project Knowledge Base. This file contains the full DSOM
#   Cognitive Twin context including: Sovereign Constitution, Brain Artifacts,
#   4-Tier Environment Map, Ansible Inventory, and GitOps Strategy.
#
# Usage:
#   bash tools/reanimate-claude.sh
#   Then upload the resulting DSOM-CLAUDE-INIT.md to your Claude Project.
# ==============================================================================

# 1. Setup
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
if [ -z "$REPO_ROOT" ]; then
    echo "[ERROR] Not in a Git repository. Run from the project root."
    exit 1
fi

DATE_STAMP=$(date +"%Y-%m-%d_%H%M")
OUTPUT_FILE="${REPO_ROOT}/DSOM-CLAUDE-INIT.md"
BRAIN_DIR="$REPO_ROOT/.agent/brain"
DOCS_DIR="$REPO_ROOT/docs"

# Colors
CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${CYAN}======================================================================"
echo -e "  🧠 DSOM Claude Reanimation Generator v2.0"
echo -e "  Generating: DSOM-CLAUDE-INIT.md"
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

# 3. Generate the manifest
{
    echo "# 🧠 DSOM CLAUDE INITIALIZATION MANIFEST"
    echo "# Standard: DSOM For My AI Protocol v6.1"
    echo "# Generated: $(date)"
    echo "# Project Root: $REPO_ROOT"
    echo ""
    echo "> **PURPOSE:** Upload this file to your Claude Project Knowledge Base."
    echo "> It contains your full Cognitive Digital Twin context. After uploading,"
    echo "> use the SOD Handshake prompt in docs/CLAUDE-SETUP.md to reanimate."
    echo ""
    echo "---"

    # --- Section 1: Sovereign Constitution ---
    echo ""
    echo "## ⚖️ [1] SOVEREIGN CONSTITUTION (The Law)"
    echo ""
    if [ -f "$DOCS_DIR/AI-MASTER-PROTOCOL.md" ]; then
        cat "$DOCS_DIR/AI-MASTER-PROTOCOL.md"
    else
        echo "[MISSING] docs/AI-MASTER-PROTOCOL.md not found."
        echo "Fallback Laws:"
        echo "1. Zero-Global Pattern — No global variables."
        echo "2. Sovereign Portability — Linux-agnostic, no vendor lock-in."
        echo "3. HA-Ready — Design for clusters and zero-downtime."
        echo "4. Atomic Git Hygiene — One logical change per commit."
        echo "5. Pedagogical Logic — Explain Why before What."
        echo "6. GitOps Rule — If not in Git, it does not exist."
        echo "7. Ansible-First Execution — No ad-hoc commands on target nodes."
    fi
    echo ""
    echo "---"

    # --- Section 2: Cognitive Twin Protocol ---
    echo ""
    echo "## 🗺️ [2] COGNITIVE TWIN PROTOCOL (Project Identity Card)"
    echo ""
    if [ -f "$DOCS_DIR/AI-COGNITIVE-TWIN-PROTOCOL.md" ]; then
        cat "$DOCS_DIR/AI-COGNITIVE-TWIN-PROTOCOL.md"
    else
        echo "[MISSING] docs/AI-COGNITIVE-TWIN-PROTOCOL.md not found."
        echo "Fill in this template from the DSOM skeleton to define the 4-Tier environment."
    fi
    echo ""
    echo "---"

    # --- Section 3: Current Task ---
    echo ""
    echo "## 🎯 [3] CURRENT TASK (What to do NOW)"
    echo ""
    if [ -f "$BRAIN_DIR/task.md" ]; then
        cat "$BRAIN_DIR/task.md"
    else
        echo "[MISSING] .agent/brain/task.md"
    fi
    echo ""
    echo "---"

    # --- Section 4: Mental Anchor / Walkthrough ---
    echo ""
    echo "## 🏁 [4] MENTAL ANCHOR — WALKTHROUGH (The History)"
    echo ""
    if [ -f "$BRAIN_DIR/walkthrough.md" ]; then
        cat "$BRAIN_DIR/walkthrough.md"
    else
        echo "[MISSING] .agent/brain/walkthrough.md"
    fi
    echo ""
    echo "---"

    # --- Section 5: Implementation Plan ---
    echo ""
    echo "## 🗺️ [5] IMPLEMENTATION PLAN (The Roadmap)"
    echo ""
    if [ -f "$BRAIN_DIR/implementation_plan.md" ]; then
        cat "$BRAIN_DIR/implementation_plan.md"
    else
        echo "[MISSING] .agent/brain/implementation_plan.md"
    fi
    echo ""
    echo "---"

    # --- Section 6: Git History ---
    echo ""
    echo "## 📜 [6] GIT HISTORY (Recent Activity)"
    echo ""
    echo "### Last 30 Commits"
    git -C "$REPO_ROOT" log -n 30 --pretty=format:"%h - %an (%ar): %s"
    echo ""
    echo ""
    echo "---"

    # --- Section 7: Project Structure ---
    echo ""
    echo "## 🗂️ [7] PROJECT STRUCTURE"
    echo ""
    git -C "$REPO_ROOT" ls-tree -r HEAD --name-only | while read -r file; do echo "  - $file"; done
    echo ""
    echo "---"

    # --- Section 8: Ansible Inventory (if present) ---
    echo ""
    echo "## ⚙️ [8] ANSIBLE INVENTORY (Node Topology)"
    echo ""
    if [ -f "$REPO_ROOT/inventory/hosts.yml" ]; then
        echo "⚠️  NOTE: This file may contain hostnames/IPs."
        echo "   Run tools/privacy-guardian.sh before sharing."
        echo ""
        cat "$REPO_ROOT/inventory/hosts.yml"
    else
        echo "[SKIP] inventory/hosts.yml not found (non-infra project or Ansible not yet configured)."
    fi
    echo ""
    echo "---"

    # --- Section 9: GitOps Strategy Summary ---
    echo ""
    echo "## 🔱 [9] GITOPS STRATEGY (Three-Pillar Doctrine)"
    echo ""
    if [ -f "$DOCS_DIR/GITOPS-AIOPS-ANSIBLE-STRATEGY.md" ]; then
        head -n 60 "$DOCS_DIR/GITOPS-AIOPS-ANSIBLE-STRATEGY.md"
        echo ""
        echo "... (see full doc: docs/GITOPS-AIOPS-ANSIBLE-STRATEGY.md)"
    else
        echo "[SKIP] GITOPS-AIOPS-ANSIBLE-STRATEGY.md not found."
    fi
    echo ""
    echo "---"

    # --- Footer ---
    echo ""
    echo "## ✅ UPLOAD INSTRUCTIONS"
    echo ""
    echo "1. Upload this file (DSOM-CLAUDE-INIT.md) to your Claude Project Knowledge Base."
    echo "2. Start a new Claude conversation and use the SOD Handshake prompt:"
    echo ""
    echo '   > "Initialise DSOM Protocol v6.1. Read the uploaded manifest.'
    echo '   > Summarise the current Mental Anchor from .agent/brain/walkthrough.md.'
    echo '   > Confirm the 4-Tier environment map from AI-COGNITIVE-TWIN-PROTOCOL.md.'
    echo '   > State: Sovereign State Synchronised when ready."'
    echo ""
    echo "See: docs/CLAUDE-SETUP.md for the full ritual."
    echo ""
    echo "======================================================================"
    echo "🏁 MANIFEST COMPLETE — DSOM For My AI Protocol v6.1"
    echo "======================================================================"

} > "$OUTPUT_FILE"

echo ""
echo -e "${GREEN}✅ Manifest saved to: $OUTPUT_FILE${NC}"
echo -e "${YELLOW}🛡️  REMINDER: Run tools/privacy-guardian.sh before uploading this manifest.${NC}"
echo ""
echo "  📤 Next step: Upload DSOM-CLAUDE-INIT.md to your Claude Project Knowledge Base."
echo "  📖 Then follow the SOD ritual in docs/CLAUDE-SETUP.md."
echo ""
