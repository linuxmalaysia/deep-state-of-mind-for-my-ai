#!/usr/bin/env bash
# DSOM Checkpoint Ritual (Linux/WSL2)
# Executes the fast mid-task checkpoint sequence.

set -e

echo "  [INIT] Validating environment for DSOM Checkpoint..."

if ! command -v ansible-playbook &> /dev/null; then
    echo "  [ERROR] ansible-playbook is required but could not be found."
    exit 1
fi

export ANSIBLE_NOCOWS=1
ansible-playbook playbooks/dsom/checkpoint-palace.yml
