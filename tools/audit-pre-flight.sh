#!/bin/bash
# ==============================================================================
# 📜 Universal DSOM Audit Pre-Flight (v4.1 - Root Aware)
# 
# Author:  Harisfazillah Jamel (LinuxMalaysia)
# Partner: Generated with the help of Google Gemini
# License: GNU GPL v3.0 or later
# 
# Description:
# Enforces synchronization between the physical environment, Git state, 
# and the AI's "External Brain" before starting a development session.
# ==============================================================================

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' 

# Find the Git root directory
ROOT_DIR=$(git rev-parse --show-toplevel 2>/dev/null)
if [ -z "$ROOT_DIR" ]; then
    echo -e "${RED}[ERROR] Audit failed: Not a git repository.${NC}"
    exit 1
fi

BRAIN_DIR="$ROOT_DIR/.agent/brain"

echo -e "${CYAN}==================================================${NC}"
echo -e "${CYAN}   DEEP STATE OF MIND (DSOM) INTELLIGENCE AUDIT   ${NC}"
echo -e "${CYAN}   Project Root: $ROOT_DIR${NC}"
echo -e "${CYAN}==================================================${NC}"

# 1. BRAIN CHECK
echo -e "${YELLOW}Step 1: Checking AI Brain Artifacts...${NC}"
REQUIRED_FILES=("task.md" "walkthrough.md")

for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$BRAIN_DIR/$file" ]; then
        echo -e "${RED}[ERROR] Missing Brain Artifact: $BRAIN_DIR/$file${NC}"
        echo -e "${YELLOW}Hint: Run ./tools/init-brain.sh to restore artifacts.${NC}"
        exit 1
    fi
done
echo -e "${GREEN}[PASS] AI Brain artifacts are present.${NC}"

# 2. GIT DRIFT CHECK
echo -e "\n${YELLOW}Step 2: Checking Version Control Sync...${NC}"
git -C "$ROOT_DIR" fetch origin > /dev/null 2>&1
LOCAL=$(git -C "$ROOT_DIR" rev-parse @)
REMOTE=$(git -C "$ROOT_DIR" rev-parse @{u} 2>/dev/null)

if [ -z "$REMOTE" ]; then
    echo -e "${YELLOW}[SKIP] No upstream found. Working in local mode.${NC}"
elif [ "$LOCAL" != "$REMOTE" ]; then
    echo -e "${RED}[WARNING] Git Drift detected! Local and Remote are out of sync.${NC}"
    echo -e "${YELLOW}Please run 'git pull' to align your state.${NC}"
else
    echo -e "${GREEN}[PASS] Git state is synchronized.${NC}"
fi

# 3. ENVIRONMENT DISCOVERY
echo -e "\n${YELLOW}Step 3: Discovering Language Environment...${NC}"
if [ -f "$ROOT_DIR/composer.json" ]; then
    echo -e "${CYAN}[DETECTED] PHP Project.${NC}"
    php -v | head -n 1
elif [ -f "$ROOT_DIR/package.json" ]; then
    echo -e "${CYAN}[DETECTED] Node.js Project.${NC}"
    node -v
elif [ -f "$ROOT_DIR/requirements.txt" ] || [ -f "$ROOT_DIR/pyproject.toml" ]; then
    echo -e "${CYAN}[DETECTED] Python Project.${NC}"
    python3 --version
else
    echo -e "${YELLOW}[NOTICE] Universal project detected (No standard manifest).${NC}"
fi

# 4. PROTOCOL GOVERNANCE
echo -e "\n${YELLOW}Step 4: Checking Governance Documents...${NC}"
if [ -f "$ROOT_DIR/docs/AI-MASTER-PROTOCOL.md" ] || [ -f "$ROOT_DIR/README.md" ]; then
    echo -e "${GREEN}[PASS] Project documentation found.${NC}"
else
    echo -e "${RED}[WARNING] No Master Protocol or README found.${NC}"
fi

echo -e "\n${GREEN}==================================================${NC}"
echo -e "${GREEN}   AUDIT COMPLETE: DSOM SECURED & READY FOR FLOW  ${NC}"
echo -e "${GREEN}==================================================${NC}"

