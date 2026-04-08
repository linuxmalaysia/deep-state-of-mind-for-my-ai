#!/bin/bash
set -e
# ==============================================================================
# 📜 DSOM Template Reset Tool (v1.0)
# 
# Date:    2026-01-08
# Author:  Harisfazillah Jamel (LinuxMalaysia)
# Partner: Generated with the help of Google Gemini
# License: GNU GPL v3.0 or later
# 
# Description:
# Prepares a DSOM clone for a new project. It purges old Git history and 
# resets brain artifacts to a "Golden Image" state while preserving 
# the Master Protocol and core tools.
# ==============================================================================

REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)

if [ -z "$REPO_ROOT" ]; then
    echo "❌ Error: Not in a Git repository."
    exit 1
fi

echo "⚠️  WARNING: This will reset brain files and remove Git history."
read -p "Are you sure you want to proceed? (y/N): " confirm

if [[ ! "$confirm" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    echo "Operation cancelled."
    exit 0
fi

# 1. Purge Git History (Optional but recommended for new projects)
echo "🧹 Removing old Git history..."
rm -rf "$REPO_ROOT/.git"
git -C "$REPO_ROOT" init

# 2. Reset Brain Artifacts to Template State
BRAIN_DIR="$REPO_ROOT/.agent/brain"

echo "🧠 Resetting Brain Artifacts..."

# Reset Task.md
cat <<EOF > "$BRAIN_DIR/task.md"
# 🎯 Current Task: Project Initialization
- [ ] Define initial architectural goals.
- [ ] Update implementation_plan.md with the new vision.
- [ ] Run tools/reanimate.sh for the first handshake.
EOF

# Reset Walkthrough.md (Keep only the header)
cat <<EOF > "$BRAIN_DIR/walkthrough.md"
# 🏁 DSOM Project Walkthrough & Session Log

## 📜 Historical Context
This project is derived from the DSOM Template.

## 🏁 Session Anchor: $(date +"%Y-%m-%d") (Initialization)
- **Accomplished:** Project cloned and reset using template-reset.sh.
- **Current State:** New project logic initialized.
- **Mental Anchor:** Ready for the first Architectural Handshake.
EOF

# Reset Implementation Plan
cat <<EOF > "$BRAIN_DIR/implementation_plan.md"
# 🗺️ New Project Implementation Plan
- [ ] Phase 1: Requirement Analysis
- [ ] Phase 2: Core Logic Development
EOF

echo "✅ Template Reset Complete."
echo "👉 Next steps: Update README.md and run 'git add .' to start your new history."

