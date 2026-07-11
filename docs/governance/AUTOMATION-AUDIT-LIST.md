---
okf_version: 0.1
type: documentation
title: "Automation & Script Audit Ledger"
description: "A comprehensive index of all executable scripts (.ps1, .sh) and Ansible playbooks/variables (.yml) currently active in the DSOM framework for human auditing purposes."
resource: "file:///docs/governance/AUTOMATION-AUDIT-LIST.md"
timestamp: 2026-07-12T07:16:00Z
---
# Automation & Script Audit Ledger

This document serves as a human-auditable index of all executable automation scripts and configuration files currently present in the DSOM workspace. It is segmented by file type to facilitate security, syntax, and operational auditing.

## 1. Shell Scripts (`.sh`)
*POSIX-compliant scripts used for Linux and Termux environments.*

- `tools/audit-pre-flight.sh`
- `tools/build_sovereign_book.sh`
- `tools/check-usage.sh`
- `tools/checkpoint.sh`
- `tools/diagnostic.sh`
- `tools/dsom-onboard.sh`
- `tools/eod-palace.sh`
- `tools/generate-walkthrough.sh`
- `tools/git-ritual.sh`
- `tools/hibernation.sh`
- `tools/init-brain.sh`
- `tools/palace-sync.sh`
- `tools/privacy-guardian.sh`
- `tools/reanimate-claude.sh`
- `tools/reanimate.sh`
- `tools/setup-dsom-control-node.sh`
- `tools/sod-palace.sh`
- `tools/template-reset.sh`

## 2. PowerShell Scripts (`.ps1`)
*Cross-platform orchestration scripts designed for Windows and PowerShell Core.*

- `tools/audit-pre-flight.ps1`
- `tools/checkpoint.ps1`
- `tools/CheckUsage.ps1`
- `tools/diagnostic.ps1`
- `tools/dsom-onboard.ps1`
- `tools/eod-palace.ps1`
- `tools/generate-walkthrough.ps1`
- `tools/git-ritual.ps1`
- `tools/hibernation.ps1`
- `tools/init-brain.ps1`
- `tools/palace-sync.ps1`
- `tools/privacy-guardian.ps1`
- `tools/reanimate-claude.ps1`
- `tools/reanimate.ps1`
- `tools/setup-wsl-almalinux10.ps1`
- `tools/sod-palace.ps1`
- `tools/template-reset.ps1`

## 3. YAML Configurations & Playbooks (`.yml`)
*Ansible playbooks, role tasks, and inventory configurations.*

### Root & Inventory
- `mkdocs.yml`
- `inventory/hosts.yml`
- `inventory/group_vars/all.yml`

### Ansible Playbooks
- `playbooks/common.yml`
- `playbooks/preflight.yml`
- `playbooks/dsom/audit-preflight.yml`
- `playbooks/dsom/checkpoint-palace.yml`
- `playbooks/dsom/eod-palace.yml`
- `playbooks/dsom/init-brain.yml`
- `playbooks/dsom/onboard-dsom.yml`
- `playbooks/dsom/privacy-scan.yml`
- `playbooks/dsom/site.yml`
- `playbooks/dsom/sod-palace.yml`

### Ansible Roles (Common)
- `roles/common/defaults/main.yml`
- `roles/common/handlers/main.yml`
- `roles/common/meta/main.yml`
- `roles/common/tasks/directories.yml`
- `roles/common/tasks/main.yml`
- `roles/common/tasks/packages.yml`
- `roles/common/tasks/sysctl.yml`
- `roles/common/tasks/timezone.yml`

---
*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-07-12*
*Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*
