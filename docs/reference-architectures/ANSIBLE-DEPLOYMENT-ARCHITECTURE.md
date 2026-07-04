---
okf_version: 0.1
type: documentation
title: "[CONSTRUCT] Ansible Deployment Architecture: Example Elastic SOC (v1.0)"
description: "OKF-compliant documentation for ANSIBLE-DEPLOYMENT-ARCHITECTURE.md."
resource: "file:///docs/reference-architectures/ANSIBLE-DEPLOYMENT-ARCHITECTURE.md"
timestamp: 2026-07-04T10:17:05Z
---
# [CONSTRUCT] Ansible Deployment Architecture: Example Elastic SOC (v1.0)
# docs/ANSIBLE-DEPLOYMENT-ARCHITECTURE.md

## 🎯 Overview
This document provides the technical blueprint for the **Example Elastic SOC** orchestration layer. The architecture unifies OS hardening, persistence, and visualization to support a highly stabilized 16-node backbone. It integrates Elasticsearch, Wazuh SIEM, Nginx Reverse Proxy, and Elastic Fleet Agents under a single Sovereign Fabric.

---

## [PATH] The Project Phases (Execution Strategy)

Unlike legacy architectures that split ingestion and persistence across separate Git repositories, Example Elastic SOC unifies the pipeline under a phased deployment model:

| Phase | **Focus** | **Key Components** | **Status** |
| :--- | :--- | :--- | :--- |
| **Phase 1** | VM Injection & Identity | `sysadmin-vm-prep.sh`, `dsom-admin` user | Active |
| **Phase 2** | OS Hardening & Tuning | `setup_os` Role, UFW, Auditd, Sysctl | Active |
| **Phase 3** | Persistence Fabric | Elasticsearch, Wazuh Manager | Pending |
| **Phase 4** | Visualization & Ingest | Kibana, Nginx Proxy, Fleet, Logstash | Pending |

---

## 🦾 Software-to-Role Mapping

| Component | Ansible Role / Path | Category | Logic Focus |
| :--- | :--- | :--- | :--- |
| **Infrastructure** | `setup_os` | Foundation | UFW, Auditd, RAM-Aware Sysctl, 16-Node Topology |
| **Persistence** | `elasticsearch` | Engine | Distributed SIEM Storage (Pending Phase 3) |
| **SIEM Engine** | `wazuh` | Security | Event Correlation & Agent Management (Pending Phase 3) |
| **Verification** | `.agents/skills/` | AI Audit | **Sovereign Agent Pulse (Lynis & Service Audits)** |

---

## [SHIELD] The Doctrine: "Rootful Orchestration, Rootless Execution"
We enforce a **Hybrid Security Model** optimized for high-performance distributed SIEM loads:

1.  **Rootful Orchestration**: Ansible orchestration from the Jumphost (Tier 3) operates with `become: yes` to manage OS-level kernel tuning (e.g., massive 134MB TCP buffers for >=64GB nodes), firewall administration, and audit daemons.
2.  **Rootless Execution**: All persistence applications (Elasticsearch, Wazuh) will execute strictly as non-privileged users within their namespaces.
3.  **Identity Sovereignty**: 
    - The `dsom-admin` (**UID 2001**) is strictly enforced across all 16 nodes.
    - Application volumes are natively owned by `dsom-admin`, allowing non-sudo maintenance and preventing root escalation vulnerabilities.

---

## 🛰️ Distributed Node Strategy (16-Node Backbone)

To support production horizontal scaling for the University of Malaya, the fabric follows the **Topology Trinity**:
1.  **DNS-less Routing**: The 16-node mapping is hardcoded natively via Ansible `blockinfile` into every node's `/etc/hosts` file. This guarantees cluster inter-connectivity even during a campus-wide DNS outage.
2.  **Dynamic Kernel Scaling**: The `setup_os` role natively calculates system RAM. Nodes >= 64GB receive massive SIEM data buffers, while nodes < 32GB receive standard routing buffers to prevent OOM panics.
3.  **Idempotent Protection**: Conflicting manual OS configurations (like dangerous 2-billion socket limits) are safely regex-detected and commented out, rather than blindly overwritten.

---

## [VAULT] Sovereign Trust & Telemetry

DSOM Persistence is anchored in **Sovereign Trust Projection**:

- **Unified Trust Fabric (ED25519)**: The architecture enforces `id_dsom_ed25519` key projection. Passwords are computationally rejected by SSH.
- **Fail2Ban Isolation**: Telemetry protects port 22 automatically, temporarily banishing IP addresses after 3 failed handshakes.
- **Project Isolation Law**: All operations are confined to `/opt/um-elastic-soc` on the Jumphost Orchestrator.

---

## [TEST] High-Fidelity AI Pulse Verification
Unlike monolithic bash scripts of the past, Example Elastic SOC employs **AI Agent Skills** for verification:
- **Security Validation**: The `audit-node-security` skill remotely triggers a CIS Lynis 3.0.9 audit and parses the result, demanding a Hardening Index of 70+ before Phase 3 can begin.
- **Service Validation**: The `node-health-check` skill natively queries `systemctl`, `ufw status`, `chronyc`, and `auditctl` to guarantee the OS baseline is enforcing the policy.

---
*Maintained by the DSOM Engineering Team & AI Cognitive Twin | Example Elastic SOC v1.0*
