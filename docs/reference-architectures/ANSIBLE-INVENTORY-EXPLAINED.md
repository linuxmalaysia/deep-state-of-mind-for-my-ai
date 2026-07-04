---
okf_version: 0.1
type: documentation
title: "[CONSTRUCT] Ansible Inventory Architecture (Example Elastic SOC v1.0)"
description: "OKF-compliant documentation for ANSIBLE-INVENTORY-EXPLAINED.md."
resource: "file:///docs/reference-architectures/ANSIBLE-INVENTORY-EXPLAINED.md"
timestamp: 2026-07-04T10:17:05Z
---
# [CONSTRUCT] Ansible Inventory Architecture (Example Elastic SOC v1.0)
# docs/ANSIBLE-INVENTORY-EXPLAINED.md

## 🎯 Purpose
This document explains the technical "Why" behind the structure of `inventory/hosts.yml`. It is designed for future human maintainers to understand why the DSOM fabric uses these specific groupings and settings for the 16+ node Example Elastic SOC environment.

---

## 🏛️ 1. The Layer of Sovereignty (UID/GID 2001)

Regardless of whether a service runs as a native `systemd` process or inside a future container, the identity standard remains absolute:

- **Identity**: `dsom-admin:2001`
- **Why it exists**: If Elasticsearch or Wazuh runs as a native package, `2001` owns the `/opt` data directories. If we elect to run isolated services (like Shuffle or MISP) via **Podman** later, we map the internal container user `1000` to the host's `dsom-admin` account (`2001`) via `keep-id`.
- **Benefit**: Even if an attacker escapes a future container or breaches a daemon, they only inherit the limited, unprivileged scope of `dsom-admin` on the host, preventing root escalation.
- **Persistence**: All data remains bit-perfectly owned by the Sovereign Architect, allowing log manipulation and maintenance without `sudo`.

---

## 📡 2. The Network Layer (Host Native vs Containerized)

In Example Elastic SOC, the core backbone (Elasticsearch/Wazuh) utilizes **Host Networking (VM Native)** via the `192.168.50.x` subnet.

However, as we expand to complex microservices (like MISP, Shuffle SOAR), we may leverage **Podman**:
- **Why Podman?**: It provides rootless execution and prevents dependency hell (e.g., Python version conflicts) on the host VM.
- **Network Overhead**: If Podman is used, we may attach containers directly to the host network (or via Macvlan) to bypass NAT overhead, ensuring the container inherits the native `192.168.50.x` IP and its high-speed throughput.

---

## 🧠 3. The Functional Tiers (Logic Grouping)

Unlike monolithic legacy clusters, `hosts.yml` is strictly divided into specialized functional units to prevent "noisy neighbor" failures:

### 🛡️ Orchestration & Access
- **`jumphosts`** (`example-node`): The orchestrator. No persistent SIEM data lives here.
- **`proxy_nodes`** (`proxy-node-alpha`): The ingress layer. Shields the backend APIs from direct user traffic.

### 🔍 Elastic Stack (The Core)
- **`elastic_nodes`** (`elastic-nodes-group`): Heavy compute/RAM nodes dedicated solely to indexing and search.
- **`kibana_nodes`**, **`logstash_nodes`**, **`fleet_nodes`**: Separated to ensure UI rendering or heavy ingestion pipelines do not steal CPU from the core Elasticsearch indices.

### 🚨 Wazuh Stack (The SIEM)
- **`wazuh_indexer`** (`indexer-nodes-group`): Dedicated storage for Wazuh telemetry.
- **`wazuh_manager`** (`manager-nodes-group`): Processes agent telemetry and runs decoding/correlation rules.
- **`wazuh_dashboard`** (`dashboard-node-alpha`): The UI layer for SOC analysts.

### 🔬 Threat Intel & Analysis (Future Expansion)
- **`misp_nodes`**, **`drif_iris_nodes`**, **`shuffle_nodes`**: Isolated nodes meant for SOAR (automation) and Threat Intel. *These are prime candidates for future Podman deployments to isolate their complex software dependencies.*

---

## 📜 Summary for the Future
This inventory is complex because it treats the **Cluster as a Single Supercomputer**. It separates compute-heavy tasks (Logstash/Wazuh Managers) from memory-heavy tasks (Elasticsearch Indexers) across distinct IP addresses.

Whether a service is deployed natively via `apt` or isolated via `podman`, the **Sovereign Rule** applies: it must run as `dsom-admin:2001` and bind strictly to the assigned `192.168.50.x` IP.

---
*Maintained by the DSOM Engineering Team | Example Elastic SOC v1.0*
