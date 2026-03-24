#!/bin/bash
set -e
# ==============================================================================
# 🚀 DSOM Git Ritual Tool (v1.0 - GitOps Sovereign Save)
#
# Date:    2026-03-09
# Author:  Harisfazillah Jamel (LinuxMalaysia)
# Partner: Generated with the help of Google Gemini
# License: GNU GPL v3.0 or later
#
# Description:
# Performs a structured, documented Sovereign Save (Git commit + push) for the
# DSOM GitOps ritual. Enforces semantic commit messages with Phase/version tags.
# Equivalent of the "Atomic Git Hygiene" law from AI-MASTER-PROTOCOL.md.
#
# Usage:
#   ./tools/git-ritual.sh                   # Interactive mode
#   ./tools/git-ritual.sh sod               # Start-of-Day sync (pull)
#   ./tools/git-ritual.sh eod               # End-of-Day commit + push
#   ./tools/git-ritual.sh push "msg"        # Direct push with message
# ==============================================================================

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
if [ -z "$REPO_ROOT" ]; then
    echo -e "${RED}[ERROR] Not a Git repository.${NC}"
    exit 1
fi

MODE="${1:-interactive}"
COMMIT_MSG="${2:-}"

echo -e "${CYAN}=====================================================${NC}"
echo -e "${CYAN}   DSOM GIT RITUAL v1.0 | GitOps Sovereign Tool     ${NC}"
echo -e "${CYAN}   Repo: $REPO_ROOT${NC}"
echo -e "${CYAN}=====================================================${NC}"
echo ""

# ── Helper: Show current Git status ───────────────────────────────────────────
show_status() {
    echo -e "${YELLOW}--- Current Git Status ---${NC}"
    git -C "$REPO_ROOT" status --short
    echo ""
    echo -e "${YELLOW}--- Last 5 Commits ---${NC}"
    git -C "$REPO_ROOT" log --oneline -5
    echo ""
}

# ── MODE: SOD (Start-of-Day) ─────────────────────────────────────────────────
if [ "$MODE" = "sod" ]; then
    echo -e "${CYAN}[SOD] Start-of-Day Sync — pulling latest from origin/main${NC}"
    git -C "$REPO_ROOT" fetch origin
    LOCAL=$(git -C "$REPO_ROOT" rev-parse @)
    REMOTE=$(git -C "$REPO_ROOT" rev-parse @{u} 2>/dev/null || echo "")
    if [ -z "$REMOTE" ]; then
        echo -e "${YELLOW}[SKIP] No upstream. Working in local mode.${NC}"
    elif [ "$LOCAL" = "$REMOTE" ]; then
        echo -e "${GREEN}[OK] Already up to date. No pull needed.${NC}"
    else
        git -C "$REPO_ROOT" pull origin main
        echo -e "${GREEN}[DONE] Pulled latest changes from origin/main.${NC}"
    fi
    show_status
    echo -e "${GREEN}SOD Sync Complete. Read .agent/brain/ artifacts and begin.${NC}"
    exit 0
fi

# ── MODE: PUSH (Direct commit + push with provided message) ──────────────────
if [ "$MODE" = "push" ]; then
    if [ -z "$COMMIT_MSG" ]; then
        echo -e "${RED}[ERROR] Provide a commit message. Usage: ./tools/git-ritual.sh push \"type(scope): message\"${NC}"
        exit 1
    fi
    show_status
    echo -e "${CYAN}[PUSH] Staging all changes and committing...${NC}"
    git -C "$REPO_ROOT" add -A
    git -C "$REPO_ROOT" commit -m "$COMMIT_MSG"
    git -C "$REPO_ROOT" push origin main
    echo -e "${GREEN}[DONE] Pushed: $COMMIT_MSG${NC}"
    exit 0
fi

# ── MODE: EOD (End-of-Day Sovereign Save) or INTERACTIVE ─────────────────────
show_status

# Check for uncommitted changes
DIRTY=$(git -C "$REPO_ROOT" status --porcelain)
if [ -z "$DIRTY" ]; then
    echo -e "${GREEN}[CLEAN] Working tree is clean. Nothing to commit.${NC}"
    exit 0
fi

echo -e "${YELLOW}Uncommitted changes detected. Starting EOD Sovereign Save...${NC}"
echo ""

# Commit type selection
echo -e "${CYAN}Select commit type (Conventional Commits standard):${NC}"
echo "  1) feat     — New feature or capability"
echo "  2) fix      — Bug fix or correction"
echo "  3) docs     — Documentation only"
echo "  4) chore    — Maintenance, brain artifacts, EOD save"
echo "  5) refactor — Code restructure without behaviour change"
echo "  6) ci       — Continuous integration / deployment changes"
echo ""
read -p "Enter number [1-6]: " type_choice

case "$type_choice" in
    1) COMMIT_TYPE="feat" ;;
    2) COMMIT_TYPE="fix" ;;
    3) COMMIT_TYPE="docs" ;;
    4) COMMIT_TYPE="chore" ;;
    5) COMMIT_TYPE="refactor" ;;
    6) COMMIT_TYPE="ci" ;;
    *) COMMIT_TYPE="chore" ;;
esac

read -p "Scope (e.g., kafka, logstash, brain, ansible): " SCOPE
read -p "Short description: " DESCRIPTION
read -p "Phase/Version tag (e.g., Phase-12/v2.3, or press Enter to skip): " PHASE_TAG

# Build the commit message
if [ -n "$PHASE_TAG" ]; then
    FULL_MSG="${COMMIT_TYPE}(${SCOPE}): ${DESCRIPTION} [${PHASE_TAG}]"
else
    FULL_MSG="${COMMIT_TYPE}(${SCOPE}): ${DESCRIPTION}"
fi

echo ""
echo -e "${CYAN}Commit message: ${YELLOW}${FULL_MSG}${NC}"
read -p "Confirm and push? (y/N): " confirm

if [[ "$confirm" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    git -C "$REPO_ROOT" add -A
    git -C "$REPO_ROOT" commit -m "$FULL_MSG"
    git -C "$REPO_ROOT" push origin main
    echo ""
    echo -e "${GREEN}=====================================================${NC}"
    echo -e "${GREEN}   SOVEREIGN SAVE COMPLETE. STATE IS PRESERVED.     ${NC}"
    echo -e "${GREEN}=====================================================${NC}"
else
    echo -e "${YELLOW}[ABORTED] Nothing committed. State not saved.${NC}"
    exit 0
fi
