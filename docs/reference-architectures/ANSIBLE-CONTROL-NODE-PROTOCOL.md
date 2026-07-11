---
okf_version: 0.1
type: documentation
title: "🎮 DSOM Ansible Control Node Protocol (Example Elastic SOC v1.0)"
description: "OKF-compliant documentation for ANSIBLE-CONTROL-NODE-PROTOCOL.md."
resource: "file:///docs/reference-architectures/ANSIBLE-CONTROL-NODE-PROTOCOL.md"
timestamp: 2026-07-04T10:17:05Z
---
# 🎮 DSOM Ansible Control Node Protocol (Example Elastic SOC v1.0)
# docs/ANSIBLE-CONTROL-NODE-PROTOCOL.md

## [CONSTRUCT] Role: The Orchestrator (`ansible01` / `example-node`)
The `example-node` host (aliased as `ansible01`) acts as the primary Control Node / Jumphost for the **Example Elastic SOC Fabric**. (Note: `proxy-node-alpha` is separately designated as the entry point `proxy01`). `example-node` serves as the authoritative bridge between the Design environment (Tier 1/2) and the Production backbone (Tier 4).

1.  **Sovereign Orchestration**: Executes all fabric-level automation natively as the **dsom-admin** identity.
2.  **Governance Anchor**: All production actions (deployments, OS baseline tuning, scaling) MUST be triggered from this node to ensure audit parity across the entire 16-node cluster.
3.  **Topology Resolution**: As the central orchestrator, `example-node` dynamically resolves all nodes via the injected `/etc/hosts` mapping, bypassing local network DNS failures.

---

## 🛰️ Connectivity Map (4-Tier Command Highway)

| Node | Function | Connection Path |
| :--- | :--- | :--- |
| **Workstation** | Tier 1 (Windows) / Tier 2 (WSL2) | **SOURCE / COMMAND CENTRE** |
| **example-node / ansible01** | Tier 3 (Orchestrator VM) | **THE BRIDGE** (192.168.50.28) |
| **Fabric Nodes** | Tier 4 (15x Targets) | **TARGET BACKBONE** (192.168.50.x) |

---

## [TOOL] Synchronisation Ritual

### 1. Project Promotion (Tier 1 -> Tier 3)
There are two approved methods for synchronizing logic from the Command Centre to the Orchestrator:

**Method A: The GitOps Sync (Standard Workflow)**
After performing `git add`, `commit`, and `push` commands on Windows (Tier 1), the Sovereign Architect will manually SSH into the Jumphost to pull the authoritative changes:
```bash
ssh dsom-admin@example-node
cd /opt/um-elastic-soc
git pull origin main
```

**Method B: The Push Script (Rapid Prototyping)**
To bypass Windows Git locking issues or push uncommitted drafts, use the custom Agent Skill to cleanly mirror the codebase:
```powershell
# Mirror the local Windows codebase directly to the example-node Jumphost
.\tools\push-to-jumphost.ps1
```
*This script uses SCP to rapidly sync all project files while automatically fixing POSIX file permissions.*

### 2. Control Node Verification
Once logged into the Jumphost (`ssh dsom-admin@example-node`), navigate to the project root and ensure the Ansible environment is healthy:

```bash
cd /opt/um-elastic-soc
# Verify orchestration dependencies
ansible --version
```

### 3. Execution (The Sovereign Ritual)
All primary orchestration must occur within the established project root on Tier 3 (`/opt/um-elastic-soc`).

```bash
# Step 1: Verify distributed connectivity across the 16 nodes
ansible -i inventory/hosts.yml all -m ping

# Step 2: Execute the baseline Fabric Playbooks
ansible-playbook -i inventory/hosts.yml playbooks/site.yml
```

---

## 👤 Identity & Security
- **Sovereign Identity**: `dsom-admin` (**UID:GID 2001:2001**) is the absolute authority for all fabric resources.
- **Rootful Control**: Ansible leverages `become: yes` for OS-level tuning (UFW, Sysctl, Lynis) but drops to `dsom-admin:2001` for application execution (Elasticsearch/Wazuh).
- **Key Forwarding**: The orchestrator relies on strict SSH keys (`id_dsom_ed25519`). Passwords are computationally rejected.

---

## [TEST] Operational Audit
To verify the orchestrator's command of the fabric, we utilize specialized **AI Agent Skills** rather than monolithic bash scripts:
1.  **Node Pulse**: Run `node-health-check` skill to verify UFW, Fail2Ban, Auditd, and Chrony.
2.  **Compliance Pulse**: Run `audit-node-security` skill to verify the CIS baseline Lynis score remains at 70+.

---
*Maintained by the DSOM Engineering Team & AI Cognitive Twin | Example Elastic SOC v1.0*


---
*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-07-04*
*Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*
