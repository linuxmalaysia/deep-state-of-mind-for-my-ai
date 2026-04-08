# HOWTO: audit-pre-flight — Intelligence Integrity Sync

# docs/tools/HOWTO-AUDIT-PRE-FLIGHT.md

> **Standard: DSOM For My AI Protocol v6.1 | Deterministic Operations**
> **Tools:** `audit-pre-flight.ps1`, `audit-pre-flight.sh`, `playbooks/dsom/audit-preflight.yml`
> **Platforms:** Windows Native (T1), Linux/WSL2 (T2)

---

## 1. Purpose

`audit-pre-flight` is the **Hardened Gatekeeper** of the DSOM workflow. Before a single line of code is written or an Ansible playbook is run, the audit tool verifies that the environment, the AI's "External Brain", and the Version Control state are in perfect synchronization.

**Use it to:**
- Detect **Git Drift** (divergence between local and origin).
- Verify the physical existence of required **Brain Artifacts** (`task.md`, `walkthrough.md`).
- Validate that the **Cognitive Twin Protocol** is correctly configured (no placeholders).
- Sanity check the **Ansible Baseline** (inventory and configuration files).
- Auto-discover the local language environment (PHP, Node.js, Python).

**Location:** 
- `tools/audit-pre-flight.ps1` (Windows)
- `tools/audit-pre-flight.sh` (Linux/WSL2)
- `playbooks/dsom/audit-preflight.yml` (Ansible)

---

## 2. Prerequisites

| Requirement | Minimum | Notes |
|:---|:---|:---|
| Protocol | DSOM v5.0+ | Compatible with current v6.1 framework. |
| Git | Yes | Repository must be initialized. |
| Brain | Init'd | `.agent/brain/` must exist. |

---

## 3. Usage

### 3.1 Standard Execution

```powershell
# Windows (T1)
.\tools\audit-pre-flight.ps1
```

```bash
# WSL2 / Linux (T2)
bash tools/audit-pre-flight.sh
```

### 3.2 Ansible Validation

```bash
ansible-playbook playbooks/dsom/audit-preflight.yml
```

---

## 4. The 5-Step Health Check

The tool executes these checks in order:

| Step | Check | Success Criteria |
|:---|:---|:---|
| **1** | **Brain Check** | `task.md` and `walkthrough.md` both exist. |
| **2** | **Git Sync** | Local branch matches `origin/main` (or local-only mode). |
| **3** | **Discovery** | Identifies project type and prints version (e.g., `Node v20.x`). |
| **4** | **Cognitive Twin** | `AI-COGNITIVE-TWIN-PROTOCOL.md` has no `[PLACEHOLDERS]`. |
| **5** | **Ansible Baseline** | `ansible` command works and `hosts.yml` exists. |

---

## 5. Reading the Output & Status Codes

| Label | Meaning | Action Needed |
|:---|:---|:---|
| `[PASS]` | Requirement met. | Proceed to next check. |
| `[OK]` | Environment feature active. | Informational only. |
| `[SKIP]` | Optional feature missing. | No action if not using that feature. |
| `[WARNING]` | Non-fatal drift/config. | Recommend fixing before workflow. |
| `[ERROR]` | **CRITICAL FAILURE**. | Full stop. Fix dependency before work. |

---

## 6. Integration with the Daily Rituals

This script is natively integrated into **`sod-palace`**. Under the **Start-of-Day Ritual**, you should run either `sod-palace` (which includes this audit) or run `audit-pre-flight` standalone before sharing any manifest with the AI.

---

## 7. Related Documents

| Document | Purpose |
|:---|:---|
| [`docs/SOD-RITUAL.md`](../SOD-RITUAL.md) | Where this audit fits in the daily cycle. |
| [`HOWTO-SOD-PALACE.md`](HOWTO-SOD-PALACE.md) | Automated SOD wrapper including this tool. |

---

*Standard: DSOM For My AI Protocol v6.1 | Harisfazillah Jamel | LinuxMalaysia*
*Document Version: v1.0 | Created: 2026-04-08*
