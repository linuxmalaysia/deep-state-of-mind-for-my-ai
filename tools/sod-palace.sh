#!/usr/bin/env bash

# ==============================================================================
# Protocol    : Deep State of Mind (DSOM) For My AI
# Author      : Harisfazillah Jamel (LinuxMalaysia)
# Timestamp   : 2026-07-12
# License     : GNU General Public License v3.0
# Standard    : UK English | DBP-standard Bahasa Melayu Malaysia (Piawai)
# ==============================================================================
# DSOM Start-of-Day (SOD) Ritual — Palace Edition (Linux/WSL2)
# Automates the Start-of-Day mechanical steps.

set -e

if ! command -v ansible-playbook &> /dev/null; then
    echo "  [ERROR] ansible-playbook is required but could not be found."
    exit 1
fi

export ANSIBLE_NOCOWS=1
ansible-playbook playbooks/dsom/sod-palace.yml
