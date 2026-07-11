# Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-04-08
# Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0

#!/usr/bin/env bash
# DSOM End-of-Day (EOD) Ritual — Palace Edition (Linux/WSL2)
# Automates the End-of-Day saves, validations and commit.

set -e

if ! command -v ansible-playbook &> /dev/null; then
    echo "  [ERROR] ansible-playbook is required but could not be found."
    exit 1
fi

export ANSIBLE_NOCOWS=1
ansible-playbook playbooks/dsom/eod-palace.yml
