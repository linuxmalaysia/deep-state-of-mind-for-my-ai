#!/bin/bash
set -e
# ==============================================================================
# 📜 Universal DSOM Audit Pre-Flight (v5.0 - GitOps + AIOps + Ansible)
# 
# Author:  Harisfazillah Jamel (LinuxMalaysia)
# Partner: Generated with the help of Google Gemini
# License: GNU GPL v3.0 or later
# 
# Description:
# Enforces synchronization between the physical environment, Git state,
# the AI's "External Brain", Cognitive Twin Protocol, and the Ansible
# baseline before starting a development session.
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

# 4. COGNITIVE TWIN PROTOCOL CHECK
echo -e "\n${YELLOW}Step 4: Checking Cognitive Twin Protocol...${NC}"
if [ -f "$ROOT_DIR/docs/AI-COGNITIVE-TWIN-PROTOCOL.md" ]; then
    # Check if it still has unfilled placeholders
    if grep -q "\[YOUR_PROJECT_NAME\]" "$ROOT_DIR/docs/AI-COGNITIVE-TWIN-PROTOCOL.md"; then
        echo -e "${YELLOW}[WARNING] AI-COGNITIVE-TWIN-PROTOCOL.md exists but still has [PLACEHOLDER] values.${NC}"
        echo -e "${YELLOW}          Fill in all [YOUR_*] fields to configure the Cognitive Twin for this project.${NC}"
    else
        echo -e "${GREEN}[PASS] AI-COGNITIVE-TWIN-PROTOCOL.md exists and appears configured.${NC}"
    fi
else
    echo -e "${RED}[WARNING] docs/AI-COGNITIVE-TWIN-PROTOCOL.md is MISSING.${NC}"
    echo -e "${YELLOW}          Copy from the DSOM skeleton and fill in your project details.${NC}"
    echo -e "${YELLOW}          See: docs/HOWTO-SETUP-ANSIBLE-BASELINE.md${NC}"
fi

# 5. ANSIBLE BASELINE CHECK
echo -e "\n${YELLOW}Step 5: Checking Ansible Baseline...${NC}"
ANSIBLE_OK=1

if ! command -v ansible &>/dev/null; then
    echo -e "${YELLOW}[SKIP] Ansible not installed — skipping Ansible checks (non-infra project or setup pending).${NC}"
    ANSIBLE_OK=0
else
    echo -e "${GREEN}[OK] Ansible: $(ansible --version | head -1)${NC}"
    if [ -f "$ROOT_DIR/inventory/hosts.yml" ]; then
        echo -e "${GREEN}[OK] inventory/hosts.yml exists.${NC}"
    else
        echo -e "${YELLOW}[WARN] inventory/hosts.yml missing. Run HOWTO-SETUP-ANSIBLE-BASELINE.md to create it.${NC}"
    fi
    if [ -f "$ROOT_DIR/ansible.cfg" ]; then
        echo -e "${GREEN}[OK] ansible.cfg exists.${NC}"
    else
        echo -e "${YELLOW}[WARN] ansible.cfg missing.${NC}"
    fi
fi

echo -e "\n${GREEN}==================================================${NC}"
echo -e "${GREEN}   AUDIT COMPLETE: DSOM SECURED & READY FOR FLOW  ${NC}"
echo -e "${GREEN}   Protocol v5.0 | GitOps · AIOps · Ansible        ${NC}"
echo -e "${GREEN}==================================================${NC}"
