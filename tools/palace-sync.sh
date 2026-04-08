#!/bin/bash
set -euo pipefail
# ==============================================================================
# 🏛️ DSOM Palace Sync Tool v1.0
#
# Author:  Harisfazillah Jamel (LinuxMalaysia)
# Partner: Generated with assistance from Google Antigravity
# License: GNU GPL v3.0 or later
#
# Description:
#   Reads the git commit history and generates a Palace Update Proposal —
#   a structured Markdown file mapping each commit to the relevant Palace Room.
#   The AI then reviews this proposal and updates the corresponding closet.md files.
#
# Modes:
#   Default (EOD Batch): Reads commits since the last sync marker.
#   --backfill          : Reads the FULL git history from day zero.
#
# Usage:
#   bash tools/palace-sync.sh              # EOD batch sync
#   bash tools/palace-sync.sh --backfill   # Full history backfill
# ==============================================================================

# --- Colors ---
CYAN='\033[0;36m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
MAGENTA='\033[0;35m'
DARKGRAY='\033[1;30m'
NC='\033[0m'

VERSION="v1.0"
MODE="eod"

# --- Parse arguments ---
for arg in "$@"; do
    case $arg in
        --backfill) MODE="backfill" ;;
        --help)
            echo "Usage: bash tools/palace-sync.sh [--backfill]"
            echo ""
            echo "  (no args)    EOD Batch: sync commits since last run"
            echo "  --backfill   Full scan: sync entire git history"
            exit 0
            ;;
    esac
done

# --- Setup ---
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || true)
if [ -z "${REPO_ROOT}" ]; then
    echo -e "${RED}[ERROR] Not in a Git repository.${NC}"
    exit 1
fi

BRAIN_DIR="$REPO_ROOT/.agent/brain"
PALACE_DIR="$BRAIN_DIR/wings"
REGISTRY="$BRAIN_DIR/palace_registry.md"
MARKER_FILE="$BRAIN_DIR/.palace-sync-marker"
DATE_STAMP=$(date +"%Y-%m-%d")
TIME_STAMP=$(date +"%Y-%m-%d_%H%M")
PROPOSAL_FILE="$BRAIN_DIR/palace_update_proposal_${TIME_STAMP}.md"

echo -e "${CYAN}======================================================================"
echo -e "  🏛️ DSOM Palace Sync Tool — $VERSION"
echo -e "  Mode: $(echo $MODE | tr '[:lower:]' '[:upper:]')"
echo -e "  Date: $DATE_STAMP"
echo -e "======================================================================${NC}"
echo ""

# --- Path-to-Room Mapping Function ---
# Returns: "WING|HALL|ROOM" for a given file path
map_path_to_room() {
    local filepath="$1"

    # Ansible/Infrastructure
    if echo "$filepath" | grep -qE "^(playbooks|inventory|roles|vault)/"; then
        echo "wing_dsom_core|hall_events|room_sovereign_fabric"
        return
    fi

    # Brain artifacts
    if echo "$filepath" | grep -qE "^\.agent/brain/"; then
        echo "wing_dsom_core|hall_events|room_brain_artifacts"
        return
    fi

    # Tools
    if echo "$filepath" | grep -qE "^tools/"; then
        echo "wing_dsom_core|hall_facts|room_tooling"
        return
    fi

    # Core documentation
    if echo "$filepath" | grep -qE "^docs/AI-MASTER-PROTOCOL|^docs/OPERATIONAL"; then
        echo "wing_dsom_core|hall_facts|room_dsom_protocol"
        return
    fi

    # Ledger files
    if echo "$filepath" | grep -qE "^(CHANGELOG|HISTORY)\.md$"; then
        echo "wing_dsom_core|hall_events|room_ledger"
        return
    fi

    # Navigation/Summary
    if echo "$filepath" | grep -qE "^(README|SUMMARY|mkdocs)"; then
        echo "wing_dsom_core|hall_facts|room_dsom_protocol"
        return
    fi

    # General docs
    if echo "$filepath" | grep -qE "^docs/"; then
        echo "wing_dsom_core|hall_facts|room_dsom_protocol"
        return
    fi

    # Fallback
    echo "wing_dsom_core|hall_discoveries|room_uncategorised"
}

# --- Determine git log range ---
if [ "$MODE" = "backfill" ]; then
    echo -e "${YELLOW}📚 Backfill mode: scanning FULL git history...${NC}"
    GIT_LOG_ARGS="--all"
    SINCE_LABEL="the beginning of the project"
else
    if [ -f "$MARKER_FILE" ]; then
        LAST_SYNC=$(cat "$MARKER_FILE")
        echo -e "${YELLOW}🔍 EOD mode: scanning commits since last sync ($LAST_SYNC)...${NC}"
        GIT_LOG_ARGS="--after=$LAST_SYNC"
        SINCE_LABEL="$LAST_SYNC"
    else
        echo -e "${YELLOW}⚠️  No sync marker found. Running full scan for first-time setup...${NC}"
        GIT_LOG_ARGS="--all"
        SINCE_LABEL="the beginning (first run)"
    fi
fi

echo ""

# --- Collect git log ---
COMMIT_LOG=$(git -C "$REPO_ROOT" log $GIT_LOG_ARGS \
    --pretty=format:"%H|%as|%s" \
    --name-only \
    --diff-filter=ACMR \
    2>/dev/null || true)

if [ -z "$COMMIT_LOG" ]; then
    echo -e "${GREEN}✅ No new commits to process since ${SINCE_LABEL}.${NC}"
    echo -e "   The Palace is already up to date."
    # Update marker even if no commits
    date +"%Y-%m-%d" > "$MARKER_FILE"
    exit 0
fi

# --- Parse commits and build proposal ---
echo -e "${CYAN}📝 Building Palace Update Proposal...${NC}"

{
    echo "# 🏛️ Palace Update Proposal"
    echo ""
    echo "> **Generated:** $TIME_STAMP  "
    echo "> **Mode:** $(echo $MODE | tr '[:lower:]' '[:upper:]')  "
    echo "> **Scope:** Commits since $SINCE_LABEL  "
    echo "> **Status:** PENDING AI REVIEW — Do not commit until closets are updated."
    echo ""
    echo "---"
    echo ""
    echo "## 📋 Instructions for AI"
    echo ""
    echo "For each entry below:"
    echo "1. Read the **Commit Subject** and **Files Changed**."
    echo "2. Navigate to the **Target Closet** path listed."
    echo "3. Add a concise, high-density entry to that closet's knowledge summary."
    echo "4. Cross-link back to this proposal file's date for audit trail."
    echo "5. Update \`palace_registry.md\` if a new Room was created."
    echo ""
    echo "---"
    echo ""
} > "$PROPOSAL_FILE"

# --- Process each commit ---
declare -A ROOM_COMMITS  # associative array: room -> list of commits

CURRENT_HASH=""
CURRENT_DATE=""
CURRENT_MSG=""
CURRENT_FILES=()

process_commit() {
    if [ -z "$CURRENT_HASH" ]; then return; fi

    declare -A ROOMS_SEEN

    for f in "${CURRENT_FILES[@]}"; do
        MAPPING=$(map_path_to_room "$f")
        IFS='|' read -r wing hall room <<< "$MAPPING"
        ROOM_KEY="$wing/$hall/$room"

        if [ -z "${ROOMS_SEEN[$ROOM_KEY]+x}" ]; then
            ROOMS_SEEN[$ROOM_KEY]=1
            ROOM_COMMITS["$ROOM_KEY"]+="### \`${CURRENT_HASH:0:7}\` — $CURRENT_DATE\n"
            ROOM_COMMITS["$ROOM_KEY"]+="**Subject:** $CURRENT_MSG\n"
            ROOM_COMMITS["$ROOM_KEY"]+="**Files:** "
        fi

        ROOM_COMMITS["$ROOM_KEY"]+=" \`$f\`"
    done

    for ROOM_KEY in "${!ROOMS_SEEN[@]}"; do
        IFS='/' read -r wing hall room <<< "$ROOM_KEY"
        CLOSET_PATH="wings/$wing/$hall/$room/closet.md"
        ROOM_COMMITS["$ROOM_KEY"]+="\n**Target Closet:** \`.agent/brain/$CLOSET_PATH\`\n\n"
    done
}

while IFS= read -r line; do
    # Detect commit line (hash|date|message)
    if echo "$line" | grep -qE "^[0-9a-f]{40}\|"; then
        process_commit
        CURRENT_HASH=$(echo "$line" | cut -d'|' -f1)
        CURRENT_DATE=$(echo "$line" | cut -d'|' -f2)
        CURRENT_MSG=$(echo "$line" | cut -d'|' -f3-)
        CURRENT_FILES=()
    elif [ -n "$line" ]; then
        CURRENT_FILES+=("$line")
    fi
done <<< "$COMMIT_LOG"
process_commit  # process last commit

# --- Write grouped output to proposal ---
if [ ${#ROOM_COMMITS[@]} -eq 0 ]; then
    echo "*(No file changes detected in the commit range.)*" >> "$PROPOSAL_FILE"
else
    for ROOM_KEY in $(echo "${!ROOM_COMMITS[@]}" | tr ' ' '\n' | sort); do
        IFS='/' read -r wing hall room <<< "$ROOM_KEY"
        {
            echo "## 🚪 Room: \`$room\`"
            echo "> **Wing:** \`$wing\` | **Hall:** \`$hall\`"
            echo ""
            echo -e "${ROOM_COMMITS[$ROOM_KEY]}"
            echo "---"
            echo ""
        } >> "$PROPOSAL_FILE"
    done
fi

# --- Append AI handshake instructions ---
{
    echo ""
    echo "## ✅ Post-Review Checklist"
    echo ""
    echo "- [ ] All closets updated with new knowledge"
    echo "- [ ] \`palace_registry.md\` updated if new Rooms were created"
    echo "- [ ] This proposal file committed to Git alongside closet updates"
    echo ""
    echo "---"
    echo "*Generated by palace-sync.sh $VERSION | DSOM Protocol v6.1*"
} >> "$PROPOSAL_FILE"

# --- Update sync marker ---
date +"%Y-%m-%d" > "$MARKER_FILE"

# --- Summary ---
ROOM_COUNT=${#ROOM_COMMITS[@]}
echo ""
echo -e "${GREEN}======================================================================"
echo -e "  ✅ Palace Update Proposal generated."
echo -e "======================================================================"
echo -e "  📄 File:  $(basename $PROPOSAL_FILE)"
echo -e "  🚪 Rooms: $ROOM_COUNT Rooms affected"
echo -e "  📍 Path:  $PROPOSAL_FILE"
echo -e ""
echo -e "  NEXT STEP: Ask your AI to review this proposal and update"
echo -e "  the corresponding closet.md files in .agent/brain/wings/"
echo -e "======================================================================${NC}"
echo ""
