#!/usr/bin/env bash
# DSOM Start-of-Day (SOD) Ritual — Palace Edition (Linux/WSL2)
# Automates the Start-of-Day mechanical steps.

set -e

if ! command -v ansible-playbook &> /dev/null; then
    echo "  [ERROR] ansible-playbook is required but could not be found."
    exit 1
fi

export ANSIBLE_NOCOWS=1
ansible-playbook playbooks/dsom/sod-palace.yml
