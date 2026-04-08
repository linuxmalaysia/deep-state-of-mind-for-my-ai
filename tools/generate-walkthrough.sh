#!/bin/bash
set -e
# ==============================================================================
# 📝 DSOM Session Scribe (Walkthrough Generator)
# 
# Description:
# Automates the creation of the "Session Anchor" for walkthrough.md by 
# extracting data from Git history and the Task list.
# ==============================================================================

REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
TODAY=$(date +"%Y-%m-%d")

# 1. Harvest Git Data
echo "🔍 Harvesting Session Data for $TODAY..."
COMMITS=$(git log --since="today" --pretty=format:"    - %s" --reverse | grep -v "chore(hibernation)")

# 2. Harvest Task Data
TASKS=$(grep "\[x\]" "$REPO_ROOT/.agent/brain/task.md" | grep "(SELESAI)" || echo "    - No tasks marked as SELESAI found.")

# 3. Generate Markdown Block
echo ""
echo "## 🏁 Session Anchor: $TODAY (Auto-Generated)"
echo "- **Accomplished:**"
echo "$TASKS"
echo "$COMMITS"
echo "- **Current State:** [UPDATE ME]"
echo "- **Mental Anchor:** [UPDATE ME]"
echo ""
