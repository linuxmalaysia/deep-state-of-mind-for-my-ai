#!/bin/bash
# ==============================================================================
# 🌙 DSOM Hibernation Sequence (End-of-Day)
# ==============================================================================

# 1. Setup
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
if [ -z "$REPO_ROOT" ]; then
    echo "❌ Error: Not in a Git repository."
    exit 1
fi
BRAIN_DIR="$REPO_ROOT/.agent/brain"
TASK_FILE="$BRAIN_DIR/task.md"
WALKTHROUGH_FILE="$BRAIN_DIR/walkthrough.md"

# 2. Safety Checks
echo "======================================================================"
echo "🌙 DSOM HIBERNATION SEQUENCE INITIATED"
echo "======================================================================"
echo ""

# Check Task List Status
echo "🔍 Checking Task List..."
if grep -q "\[x\]" "$TASK_FILE"; then
    echo "✅ progress detected in task.md."
else
    echo "⚠️  WARNING: No completed tasks found in task.md today. Did you forget to update it?"
fi

# Check Walkthrough Status
echo ""
echo "🔍 Checking Session Anchor..."
TODAY=$(date +"%Y-%m-%d")
if grep -q "$TODAY" "$WALKTHROUGH_FILE"; then
    echo "✅ Session Anchor for today found in walkthrough.md."
else
    echo "❌ CRITICAL: No Session Anchor for $TODAY found in walkthrough.md!"
    echo "   You MUST summarize your work before sleeping."
fi

# 3. Context Summary
echo ""
echo "----------------------------------------------------------------------"
echo "📅 SESSION SUMMARY (What we did)"
echo "----------------------------------------------------------------------"
# Show last 5 commits for context
git log -n 5 --pretty=format:"%C(yellow)%h%Creset - %s %C(green)(%ar)%Creset"
echo ""
echo "----------------------------------------------------------------------"

# 4. Next Steps Generator
echo ""
echo "🔮 NEXT STEPS (For Tomorrow)"
echo "----------------------------------------------------------------------"
grep "\[ \]" "$TASK_FILE" | head -n 5
echo "----------------------------------------------------------------------"

# 5. Final Confirmation
echo ""
echo "😴 Are you ready to hibernate? (This will push all changes to GitHub)"
read -p "Confirm (y/N): " confirm

if [[ "$confirm" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    echo ""
    echo "🚀 Committing context..."
    git add .
    git commit -m "chore(hibernation): End-of-Day safe shutdown $(date +'%Y-%m-%d')"
    git push origin main
    echo ""
    echo "✅ SLEEP WELL, ARCHITECT. YOUR STATE IS SAVED."
else
    echo ""
    echo "🛑 Hibernation aborted. Stay awake."
fi
