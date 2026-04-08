#!/usr/bin/env bash
# DSOM Framework Onboarding Bootstrap Script
# Downloads and executes the Ansible playbook to structure the target repository.

set -e

echo "============================================================"
echo "      🚀 DSOM Framework Onboarding Initiated"
echo "============================================================"

# Verify git repository
if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    echo "ERROR: You must run this script from inside a git repository."
    exit 1
fi

# Determine dates and temporary names
TIMESTAMP=$(date +%Y-%m-%d)
TMP_BRANCH="dsom-onboarding-${TIMESTAMP}-$(date +%H%M%S)"

echo "[1/4] Checking dependencies..."
if ! command -v ansible-playbook &> /dev/null; then
    echo "ERROR: ansible-playbook is required but could not be found."
    echo "Please install ansible before running the onboarding script."
    exit 1
fi

echo "[2/4] Creating temporary branch: $TMP_BRANCH"
# Create branch, error if working tree is not completely clean
if ! git diff-index --quiet HEAD --; then
    echo "WARNING: You have uncommitted changes. Stashing them..."
    git stash
fi
git checkout -b "$TMP_BRANCH"

echo "[3/4] Downloading DSOM Onboarding Playbook..."
PLAYBOOK_DIR="/tmp/dsom-onboard-${TIMESTAMP}-$$"
mkdir -p "$PLAYBOOK_DIR"
PLAYBOOK_FILE="$PLAYBOOK_DIR/onboard-dsom.yml"

# Get raw playbook from GitHub
if command -v curl &> /dev/null; then
    curl -sS -L "https://raw.githubusercontent.com/linuxmalaysia/deep-state-of-mind-for-my-ai/main/playbooks/dsom/onboard-dsom.yml" -o "$PLAYBOOK_FILE"
elif command -v wget &> /dev/null; then
    wget -qO "$PLAYBOOK_FILE" "https://raw.githubusercontent.com/linuxmalaysia/deep-state-of-mind-for-my-ai/main/playbooks/dsom/onboard-dsom.yml"
else
    echo "ERROR: curl or wget is required to download the playbook."
    exit 1
fi

echo "[4/4] Executing Ansible Playbook..."
export ANSIBLE_NOCOWS=1
ansible-playbook "$PLAYBOOK_FILE" -e "timestamp=${TIMESTAMP}"

echo ""
echo "Cleaning up Playbook..."
rm -rf "$PLAYBOOK_DIR"

echo "============================================================"
echo "      ✅ DSOM Onboarding Architecture Synchronized"
echo "============================================================"
echo ""
echo "ACTION REQUIRED:"
echo "----------------"
echo "1. We have fetched all required DSOM tools, playbooks, and docs into this branch ($TMP_BRANCH)."
echo "2. Any existing files that collided with DSOM files have been safely kept. The incoming DSOM files were renamed to include '$TIMESTAMP' in their names."
echo "3. Please review the changes using 'git status'."
echo "4. Commit the changes: git add . && git commit -m 'chore: onboard DSOM framework'"
echo "5. Merge into your main working branch to finalize the setup."
echo ""
