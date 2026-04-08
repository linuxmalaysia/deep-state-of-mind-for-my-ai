#!/bin/bash
set -e
# ==============================================================================
# 🐧 DSOM AlmaLinux 10 Control Node Bootstrap (v1.0)
#
# Date:    2026-03-10
# Author:  Harisfazillah Jamel (LinuxMalaysia)
# License: GNU GPL v3.0 or later
#
# Description:
# Run INSIDE AlmaLinux 10 WSL2 (as root) immediately after import.
# Sets up the DSOM Ansible Control Node environment:
#   - System update
#   - Creates dsom-admin user (UID 2001, wheel group)
#   - Installs Ansible, Git, rsync, python3-pip
#   - Configures /etc/wsl.conf
#   - Generates SSH key for dsom-admin
#   - Verifies Ansible installation
#
# Usage (from PowerShell):
#   wsl -d dsom-control-almalinux10 -u root -- bash tools/setup-dsom-control-node.sh
# ==============================================================================

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

WSL_NAME="dsom-control-almalinux10"
DSOM_USER="dsom-admin"
DSOM_UID=2001
DSOM_GID=2001

echo -e "${CYAN}=====================================================${NC}"
echo -e "${CYAN}   DSOM Control Node Bootstrap v1.0                 ${NC}"
echo -e "${CYAN}   WSL: ${WSL_NAME}                                 ${NC}"
echo -e "${CYAN}=====================================================${NC}"
echo ""

# Guard: Must run as root
if [ "$(id -u)" != "0" ]; then
    echo -e "${RED}[ERROR] This script must be run as root.${NC}"
    echo -e "${YELLOW}        Run: wsl -d ${WSL_NAME} -u root -- bash tools/setup-dsom-control-node.sh${NC}"
    exit 1
fi

# Guard: Must be AlmaLinux
if ! grep -qi "almalinux" /etc/os-release 2>/dev/null; then
    echo -e "${RED}[ERROR] This script is designed for AlmaLinux only.${NC}"
    exit 1
fi

# ── Step 1: System Update ─────────────────────────────────────────────────────
echo -e "${YELLOW}[Step 1] Updating system packages...${NC}"
dnf update -y --quiet
echo -e "${GREEN}[PASS] System updated.${NC}"

# ── Step 2: Install Core Dependencies ────────────────────────────────────────
echo -e "\n${YELLOW}[Step 2] Installing core dependencies (Git, Python3, pip, rsync)...${NC}"
dnf install -y --quiet \
    git \
    python3 \
    python3-pip \
    rsync \
    openssh-clients \
    sudo \
    curl \
    wget \
    vim
echo -e "${GREEN}[PASS] Core dependencies installed.${NC}"

# ── Step 3: Install Ansible ───────────────────────────────────────────────────
echo -e "\n${YELLOW}[Step 3] Installing Ansible...${NC}"

# Try DNF first (AlmaLinux 10 EPEL)
dnf install -y --quiet epel-release 2>/dev/null || true
dnf install -y --quiet ansible 2>/dev/null || {
    echo -e "${YELLOW}[INFO] DNF install unavailable, falling back to pip...${NC}"
    pip3 install ansible --quiet
}

ANSIBLE_VER=$(ansible --version | head -1)
echo -e "${GREEN}[PASS] Ansible installed: ${ANSIBLE_VER}${NC}"

# ── Step 4: Create dsom-admin User (UID 2001) ─────────────────────────────────
echo -e "\n${YELLOW}[Step 4] Creating DSOM identity: ${DSOM_USER} (UID ${DSOM_UID})...${NC}"

if id "${DSOM_USER}" &>/dev/null; then
    echo -e "${YELLOW}[SKIP] User ${DSOM_USER} already exists.${NC}"
else
    groupadd -g "${DSOM_GID}" "${DSOM_USER}" 2>/dev/null || true
    useradd -u "${DSOM_UID}" -g "${DSOM_GID}" -m -s /bin/bash \
            -c "DSOM Ansible Control Identity" "${DSOM_USER}"
    echo -e "${GREEN}[PASS] User ${DSOM_USER} created with UID ${DSOM_UID}.${NC}"
fi

# Add to wheel group (sudo access)
usermod -aG wheel "${DSOM_USER}"
echo -e "${GREEN}[PASS] ${DSOM_USER} added to wheel group.${NC}"

# Configure passwordless sudo for dsom-admin (Control Node needs this for Ansible)
SUDOERS_FILE="/etc/sudoers.d/dsom-admin"
if [ ! -f "${SUDOERS_FILE}" ]; then
    echo "${DSOM_USER} ALL=(ALL) NOPASSWD:ALL" > "${SUDOERS_FILE}"
    chmod 440 "${SUDOERS_FILE}"
    echo -e "${GREEN}[PASS] Passwordless sudo configured for ${DSOM_USER}.${NC}"
fi

# ── Step 5: Generate SSH Key for dsom-admin ───────────────────────────────────
echo -e "\n${YELLOW}[Step 5] Generating SSH key for ${DSOM_USER}...${NC}"
DSOM_HOME="/home/${DSOM_USER}"
SSH_DIR="${DSOM_HOME}/.ssh"

if [ ! -f "${SSH_DIR}/id_ed25519" ]; then
    mkdir -p "${SSH_DIR}"
    ssh-keygen -t ed25519 -C "${DSOM_USER}@${WSL_NAME}" \
               -f "${SSH_DIR}/id_ed25519" -N ""
    chmod 700 "${SSH_DIR}"
    chmod 600 "${SSH_DIR}/id_ed25519"
    chmod 644 "${SSH_DIR}/id_ed25519.pub"
    chown -R "${DSOM_UID}:${DSOM_GID}" "${SSH_DIR}"
    echo -e "${GREEN}[PASS] SSH key generated.${NC}"
    echo -e "${CYAN}[INFO] Public key (distribute to target nodes):${NC}"
    cat "${SSH_DIR}/id_ed25519.pub"
else
    echo -e "${YELLOW}[SKIP] SSH key already exists.${NC}"
    echo -e "${CYAN}[INFO] Existing public key:${NC}"
    cat "${SSH_DIR}/id_ed25519.pub"
fi

# ── Step 6: Configure /etc/wsl.conf ──────────────────────────────────────────
echo -e "\n${YELLOW}[Step 6] Configuring /etc/wsl.conf...${NC}"
cat > /etc/wsl.conf << EOF
[user]
default=dsom-admin

[boot]
systemd=true

[interop]
appendWindowsPath=false

[automount]
enabled=true
root=/mnt/
options="metadata,umask=77,fmask=11"
EOF
echo -e "${GREEN}[PASS] /etc/wsl.conf configured.${NC}"

# ── Step 7: Set Up Ansible Configuration for dsom-admin ───────────────────────
echo -e "\n${YELLOW}[Step 7] Creating default Ansible config for ${DSOM_USER}...${NC}"
ANSIBLE_CFG_DIR="${DSOM_HOME}/.ansible"
mkdir -p "${ANSIBLE_CFG_DIR}"

cat > "${DSOM_HOME}/.ansible.cfg" << 'EOF'
[defaults]
host_key_checking   = False
stdout_callback     = yaml
bin_ansible_callbacks = True
forks               = 10
retry_files_enabled = False
gathering           = smart
fact_caching        = memory

[ssh_connection]
pipelining          = True
ssh_args            = -o ControlMaster=auto -o ControlPersist=60s -o ServerAliveInterval=30
EOF

chown -R "${DSOM_UID}:${DSOM_GID}" "${ANSIBLE_CFG_DIR}" "${DSOM_HOME}/.ansible.cfg"
echo -e "${GREEN}[PASS] Ansible config created at ${DSOM_HOME}/.ansible.cfg.${NC}"

# ── Step 8: Verify Everything ─────────────────────────────────────────────────
echo -e "\n${YELLOW}[Step 8] Final verification...${NC}"
echo -e "${CYAN}--- User Identity ---${NC}"
id "${DSOM_USER}"

echo -e "\n${CYAN}--- Ansible Version ---${NC}"
su - "${DSOM_USER}" -c "ansible --version | head -3"

echo -e "\n${CYAN}--- Ansible Localhost Ping ---${NC}"
su - "${DSOM_USER}" -c "ansible localhost -m ping"

echo -e "\n${CYAN}--- WSL Config ---${NC}"
cat /etc/wsl.conf

# ── Final Summary ─────────────────────────────────────────────────────────────
echo ""
echo -e "${GREEN}=====================================================${NC}"
echo -e "${GREEN}   DSOM CONTROL NODE BOOTSTRAP COMPLETE             ${NC}"
echo -e "${GREEN}=====================================================${NC}"
echo ""
echo -e "${CYAN}Identity: ${DSOM_USER} (UID ${DSOM_UID})${NC}"
echo -e "${CYAN}Ansible:  $(ansible --version | head -1)${NC}"
echo ""
echo -e "${YELLOW}IMPORTANT: Restart the WSL instance to apply wsl.conf:${NC}"
echo -e "${YELLOW}  wsl --terminate dsom-control-almalinux10${NC}"
echo -e "${YELLOW}  wsl -d dsom-control-almalinux10${NC}"
echo ""
echo -e "${CYAN}Next: Copy your SSH public key to target nodes:${NC}"
echo -e "${CYAN}  ssh-copy-id -i ~/.ssh/id_ed25519.pub [USER]@[TARGET_IP]${NC}"
echo -e "${CYAN}  Then run: ansible all -m ping -i inventory/hosts.yml${NC}"
