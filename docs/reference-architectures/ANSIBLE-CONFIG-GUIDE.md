---
okf_version: 0.1
type: documentation
title: "[DOC] DSOM Ansible Configuration Guide (Example Elastic SOC v1.0)"
description: "OKF-compliant documentation for ANSIBLE-CONFIG-GUIDE.md."
resource: "file:///docs/reference-architectures/ANSIBLE-CONFIG-GUIDE.md"
timestamp: 2026-07-04T10:17:05Z
---
# [DOC] DSOM Ansible Configuration Guide (Example Elastic SOC v1.0)
# docs/ANSIBLE-CONFIG-GUIDE.md

> **"Orchestration for Uptime. Sovereignty for Intelligence."**

---

## 🛠️ [TOOL] The Ansible Blueprint (`ansible.cfg`)

The `ansible.cfg` file is explicitly optimized for the **DSOM Sovereign Fabric**:
* **Pipelining**: Enabled to reduce SSH handshake latency across our distributed 16-node backbone.
* **YAML Callback**: Standardized for high-fidelity human/AI audit of deployment steps.
* **Rootful Orchestration**: Enabled via `become: true` at the task level for OS tuning (networking, dynamic kernel buffers, UFW rules, and topology mappings).
* **Orchestrator User**: Ansible connects natively via the `dsom-admin` identity using `ed25519` keys.
* **Remote Temp Resilience**: Ansible is configured to seamlessly utilize `/tmp` with `allow_world_readable_tmpfiles = True` to bypass strict unprivileged execution limits during root escalations.

---

## 🛡️ [SHIELD] The Doctrine: "Rootful Orchestration, Rootless Execution"

In the Example Elastic SOC architecture, we enforce a strict hybrid privilege model to ensure production-grade performance with sovereign-grade security:

- **Rootful Orchestration**: Ansible runs tasks requiring kernel tuning (`sysctl` max map counts and dynamic TCP buffers) or firewall management (`UFW`) as root (`become: yes`).
- **Idempotent Mitigation**: Ansible proactively checks for manual configuration drift (e.g. legacy sysctl limits) and safely comments them out via regex rather than blindly overwriting them.
- **Rootless Execution**: All containers and persistent services (Elasticsearch, Wazuh) will be strictly started as non-privileged sovereign users.
    - *Production Identity*: Strictly enforced **UID:GID 2001:2001** (`dsom-admin`).
- **Sovereign Topology**: Inter-cluster DNS is guaranteed by injecting the hardcoded 16-node `/etc/hosts` mapping natively via Ansible `blockinfile`, surviving external DNS outages.

---

## 🌳 Example Elastic SOC Structure (16-Node Fabric)

```text
.
├── ansible.cfg                # Project performance tuning
├── playbooks/
│   └── site.yml               # Master Orchestrator (Rootful Control)
├── inventory/
│   └── hosts.yml              # 16-Node Backbone & IP Mapping
├── roles/
│   └── setup_os/              # Foundation: OS Hardening, Dynamic Buffers, UFW, Lynis 3.0.9+
├── .agents/
│   ├── brain/                 # Sovereign AI Cognitive State (Palace)
│   └── skills/                # AI Agent Skills (Audit, Health, Backup)
│       ├── audit-node-security/
│       └── node-health-check/
└── tools/                     # Operational Lifecycle Tools
    ├── sysadmin-vm-prep.sh    # Dual-Stage VM Bootstrapper (Bash)
    ├── eod-palace.ps1         # End-of-Day GitOps Hibernation
    └── sod-palace.ps1         # Start-of-Day AI Reanimation
```

---

## 🔐 [VAULT] Sovereign Secrets & Identity

- **Registry**: `vault/vpn_credentials.yml`, `vault/ssh_config_template.txt`.
- **Identity (Production)**:
    - `ansible_user`: Set to `dsom-admin`.
    - `ansible_become`: Must be `true` for `setup_os` tasks.
    - **UID:GID**: Standardized at **2001:2001**.
- **Container Sovereignty**: `keep-id` prevents data directory ownership leaks to root during volume mounting.
    > **[BRAIN] Logic**: In rootless environments, `keep-id` ensures the host UID **exactly mirrors** the container UID (2001->2001). This allows the Sovereign Architect to natively own the Elasticsearch and Wazuh NVMe data, enabling manual maintenance without `sudo`.

---

## 🌐 Example Elastic SOC Core Ports

| Port | Service | Role | Data Flow |
| :--- | :--- | :--- | :--- |
| **9200** | ES HTTPS | Persistence | External API / Wazuh Ingest |
| **9300** | ES Transport | Node-to-Node | Internal Cluster Traffic (Backbone) |
| **5601** | Kibana UI | Visualization | User Access / Dashboard |
| **1514/1515** | Wazuh | SIEM | Agent Registration & Events |
| **55000** | Wazuh API | Integration | API interactions |
| **8220** | Elastic Fleet | Management | Elastic Agent endpoint monitoring |
| **5044** | Logstash | Ingestion | Beats/Syslog pipeline ingestion |
| **22** | SSH | Orchestration | Ansible Control & T2 Bridging |

---

## 🚀 Deployment Sequence (The Sovereign Rhythm)

1.  **Stage 1 - VM Injection**: Execute `bash tools/sysadmin-vm-prep.sh <ip>` from the Jumphost to standardize the OS base, standardize SSH keys, and inject the `dsom-admin` user.
2.  **Stage 2 - Baseline Hardening**: Ansible runs `roles/setup_os` to install security tooling (Lynis, Auditd), deploy UFW rules, and dynamically inject RAM-aware `sysctl` buffers for Elasticsearch.
3.  **Stage 3 - Autonomous Audit**: AI runs the `node-health-check` and `audit-node-security` skills to guarantee the node hits a Lynis score of 70+ before proceeding.
4.  **Stage 4 - Persistence Fabric**: Deploy Elasticsearch and Wazuh infrastructure (Pending Phase 3).

---
*Maintained by the DSOM Engineering Team & AI Cognitive Twin | Example Elastic SOC v1.0*
