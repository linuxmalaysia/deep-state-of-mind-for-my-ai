#!/usr/bin/env bash

# ==============================================================================
# Protocol    : Deep State of Mind (DSOM) For My AI
# Author      : Harisfazillah Jamel (LinuxMalaysia)
# Timestamp   : 2026-07-31
# License     : GNU General Public License v3.0
# Standard    : UK English | DBP-standard Bahasa Melayu Malaysia (Piawai)
# ==============================================================================
# Universal DSOM Framework Onboarding Bootstrap Script
# Bootstraps any repository/website with DSOM baseline structure, tools,
# native MCP server support, and Context7 indexer guidance.
#
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/linuxmalaysia/deep-state-of-mind-for-my-ai/main/tools/dsom-onboard.sh | bash
#   OR:
#   chmod +x dsom-onboard.sh && ./dsom-onboard.sh
# ==============================================================================

set -e

echo "============================================================"
echo "      🚀 Universal DSOM Framework Onboarding Initiated"
echo "============================================================"

# Verify git repository
if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    echo "ERROR: You must run this script from inside a git repository."
    echo "Run 'git init' first if this is a new project."
    exit 1
fi

TARGET_DIR="$(pwd)"
TIMESTAMP=$(date +%Y-%m-%d)
TIME_SUFFIX=$(date +%H%M%S)
TMP_BRANCH="dsom-onboarding-${TIMESTAMP}-${TIME_SUFFIX}"

echo "[1/4] Preparing Git workspace..."
# Stash uncommitted changes if working tree is dirty
if ! git diff-index --quiet HEAD -- 2>/dev/null; then
    echo "WARNING: Uncommitted changes detected. Stashing transient state..."
    git stash
fi

# Create and checkout onboarding branch
git checkout -b "$TMP_BRANCH"

echo "[2/4] Resolving execution engine (Ansible vs Native Fallback)..."
PLAYBOOK_DIR="/tmp/dsom-onboard-${TIMESTAMP}-$$"
mkdir -p "$PLAYBOOK_DIR"

DSOM_REPO_URL="https://github.com/linuxmalaysia/deep-state-of-mind-for-my-ai.git"

if command -v ansible-playbook &> /dev/null; then
    echo " -> Ansible detected. Utilizing Ansible engine..."
    PLAYBOOK_FILE="$PLAYBOOK_DIR/onboard-dsom.yml"
    
    if command -v curl &> /dev/null; then
        curl -sS -L "https://raw.githubusercontent.com/linuxmalaysia/deep-state-of-mind-for-my-ai/main/playbooks/dsom/onboard-dsom.yml" -o "$PLAYBOOK_FILE"
    elif command -v wget &> /dev/null; then
        wget -qO "$PLAYBOOK_FILE" "https://raw.githubusercontent.com/linuxmalaysia/deep-state-of-mind-for-my-ai/main/playbooks/dsom/onboard-dsom.yml"
    fi
    
    export ANSIBLE_NOCOWS=1
    ansible-playbook "$PLAYBOOK_FILE" -e "timestamp=${TIMESTAMP}"
else
    echo " -> Ansible not found. Falling back to Native Pure-Bash Git Engine..."
    CLONE_DIR="$PLAYBOOK_DIR/dsom-main"
    git clone --depth 1 "$DSOM_REPO_URL" "$CLONE_DIR" >/dev/null 2>&1

    echo "[3/4] Copying DSOM Baseline Architecture with Conflict Resolution..."
    
    # Directories to copy
    for DIR in "tools" "playbooks/dsom" "docs" ".agents"; do
        if [ -d "$CLONE_DIR/$DIR" ]; then
            cd "$CLONE_DIR"
            find "$DIR" -type f | while read -r FILE; do
                DEST_FILE="$TARGET_DIR/$FILE"
                mkdir -p "$(dirname "$DEST_FILE")"
                
                if [ -f "$DEST_FILE" ]; then
                    EXT="${FILE##*.}"
                    BASE="${FILE%.*}"
                    if [ "$EXT" = "$FILE" ]; then
                        cp "$CLONE_DIR/$FILE" "${DEST_FILE}-${TIMESTAMP}"
                        echo "  [CONFLICT] Preserved target file. Saved incoming as ${FILE}-${TIMESTAMP}"
                    else
                        cp "$CLONE_DIR/$FILE" "$TARGET_DIR/${BASE}-${TIMESTAMP}.${EXT}"
                        echo "  [CONFLICT] Preserved target file. Saved incoming as ${BASE}-${TIMESTAMP}.${EXT}"
                    fi
                else
                    cp "$CLONE_DIR/$FILE" "$DEST_FILE"
                    echo "  [ADDED] $FILE"
                fi
            done
        fi
    done

    # Root governance & configuration files
    cd "$CLONE_DIR"
    for FILE in ".gitattributes" ".markdownlint.json" "README.md" "CHANGELOG.md" "HISTORY.md" "SUMMARY.md" "START-HERE.md" "AGENTS.md" "llms.txt"; do
        if [ -f "$FILE" ]; then
            DEST_FILE="$TARGET_DIR/$FILE"
            if [ -f "$DEST_FILE" ]; then
                EXT="${FILE##*.}"
                BASE="${FILE%.*}"
                if [[ "$FILE" == .* ]]; then
                    cp "$CLONE_DIR/$FILE" "$TARGET_DIR/${FILE}-${TIMESTAMP}"
                elif [ "$EXT" = "$FILE" ]; then
                    cp "$CLONE_DIR/$FILE" "${DEST_FILE}-${TIMESTAMP}"
                else
                    cp "$CLONE_DIR/$FILE" "$TARGET_DIR/${BASE}-${TIMESTAMP}.${EXT}"
                fi
                echo "  [CONFLICT] Preserved target file. Saved incoming as ${FILE}-${TIMESTAMP}"
            else
                cp "$CLONE_DIR/$FILE" "$DEST_FILE"
                echo "  [ADDED] $FILE"
            fi
        fi
    done
    cd "$TARGET_DIR"
fi

echo "[4/4] Cleaning up temporary workspace..."
rm -rf "$PLAYBOOK_DIR"

echo ""
echo "============================================================"
echo "      ✅ DSOM Onboarding Architecture Synchronized"
echo "============================================================"
echo ""
echo "NEXT STEPS & ACTION REQUIRED:"
echo "------------------------------"
echo "1. Review branch changes: git status"
echo "2. Commit baseline:       git add . && git commit -m 'chore: onboard DSOM framework'"
echo "3. Merge into main:       git checkout main && git merge $TMP_BRANCH"
echo ""
echo "SOVEREIGN AI & MCP INTEGRATION:"
echo "------------------------------"
echo "• Local MCP Server: Configure Cursor/Claude Desktop using tools/mcp/server.py:"
echo "  { \"mcpServers\": { \"dsom-palace\": { \"command\": \"uv\", \"args\": [\"run\", \"tools/mcp/server.py\"] } } }"
echo ""
echo "• Context7 Semantic RAG Service:"
echo "  Add 'context7.json' to your repository root for domain verification."
echo "  Live Payload Endpoint: https://context7.com/gitlab_linuxmalaysia/deep-state-of-mind-for-my-ai/llms.txt?tokens=10000"
echo "============================================================"
