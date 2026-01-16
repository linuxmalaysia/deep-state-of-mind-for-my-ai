#!/bin/bash
set -e
# ==============================================================================
# 🧠 DSOM Brain Initializer (v4.1 - Root Aware)
# 
# Author:  Harisfazillah Jamel (LinuxMalaysia)
# Partner: Generated with the help of Google Gemini
# License: GNU GPL v3.0 or later
# 
# Description:
# Safely initializes the Deep State of Mind (DSOM) directory and artifacts 
# at the repository root to ensure cognitive continuity for AI agents.
# ==============================================================================

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

# Find the Git root directory
ROOT_DIR=$(git rev-parse --show-toplevel 2>/dev/null)
if [ -z "$ROOT_DIR" ]; then
    echo -e "${RED}[ERROR] This directory is not a Git repository.${NC}"
    echo -e "${YELLOW}Please run 'git init' first.${NC}"
    exit 1
fi

BRAIN_DIR="$ROOT_DIR/.agent/brain"
echo -e "${CYAN}Targeting DSOM Root: $ROOT_DIR${NC}"

# 1. Create Directory Structure
if [ ! -d "$BRAIN_DIR" ]; then
    mkdir -p "$BRAIN_DIR"
    echo -e "${GREEN}[NEW] Created directory: $BRAIN_DIR${NC}"
else
    echo -e "${YELLOW}[SKIP] Directory $BRAIN_DIR already exists.${NC}"
fi

# 2. Define Files and Content
declare -A FILES
FILES=(
    ["task.md"]="# 🎯 Current Task\n\n- [ ] Task 1: Initialize project\n- [ ] Task 2: Sync state with AI"
    ["walkthrough.md"]="# 🏁 Walkthrough\n\n## Session Log\n- Project initialized using DSOM Protocol v4.1."
    ["implementation_plan.md"]="# 🗺️ Implementation Plan\n\n## Phase 1: Infrastructure\n- [x] Brain artifacts deployment\n- [ ] Project logic hardening"
    ["DSOM_TEMPLATE.md"]="# 🧠 Deep State Walkthrough Template\n\n## 🏗️ 1. The Architectural \"Why\"\n\n## 🛠️ 2. Implementation Logic\n\n## 🏁 3. Mental Anchor"
)

# 3. Create Files Safely
for file in "${!FILES[@]}"; do
    TARGET_PATH="$BRAIN_DIR/$file"
    if [ ! -f "$TARGET_PATH" ]; then
        echo -e "${FILES[$file]}" > "$TARGET_PATH"
        echo -e "${GREEN}[NEW] Created file: $TARGET_PATH${NC}"
    else
        echo -e "${YELLOW}[SKIP] File $TARGET_PATH already exists.${NC}"
    fi
done

echo -e "${CYAN}==================================================${NC}"
echo -e "${GREEN}DSOM Brain is Ready. Open Source Sovereignty Secured.${NC}"
echo -e "${CYAN}==================================================${NC}"

