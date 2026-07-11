#!/usr/bin/env bash
# Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-04-08
# Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0

# DSOM Start-of-Day (SOD) Ritual — Palace Edition (Linux/WSL2)
# Automates the Start-of-Day mechanical steps.

set -e

if ! command -v ansible-playbook &> /dev/null; then
    echo "  [ERROR] ansible-playbook is required but could not be found."
    exit 1
fi

export ANSIBLE_NOCOWS=1
ansible-playbook playbooks/dsom/sod-palace.yml
