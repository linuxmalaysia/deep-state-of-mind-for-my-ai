# HOWTO: setup-wsl-almalinux10 — T2 Control Node Provisioner

# docs/tools/HOWTO-SETUP-WSL-ALMALINUX.md

> **Standard: DSOM For My AI Protocol v6.1 | Infrastructure as Code**
> **Tools:** `setup-wsl-almalinux10.ps1`, `setup-dsom-control-node.sh`
> **Platforms:** Windows Native (T1) → WSL2 (T2)

---

## 1. Purpose

`setup-wsl-almalinux10` is the **Control Node Automator**. It bridges your Windows Tier 1 environment to a hardened Linux Tier 2 environment by automatically downloading, importing, and configuring an **AlmaLinux 10** WSL2 instance. This instance becomes your primary DSOM/Ansible control node.

**Use it to:**
- Install a clean, official AlmaLinux 10 rootfs into WSL2.
- Provision a dedicated `dsom-control-almalinux10` instance.
- Automatically trigger the internal Linux bootstrap for Ansible and users.
- Standardize the development bridge across a Windows fleet.

**Location:** 
- `tools/setup-wsl-almalinux10.ps1` (Main Windows Orchestrator)
- `tools/setup-dsom-control-node.sh` (Internal Linux Bootstrap)

---

## 2. Prerequisites

| Requirement | Minimum | Notes |
|:---|:---|:---|
| OS | Windows 11 | Required for full WSL2 `--mount` and official app support. |
| Access | **Administrator** | Script must enable Windows Features (WSL2/Hyper-V). |
| Storage | ~5 GB | For the rootfs download and instance import. |

---

## 3. Usage

Run this once from an elevated (Administrator) PowerShell terminal:

```powershell
# From the project root
.\tools\setup-wsl-almalinux10.ps1
```

---

## 4. Operation Workflow (The 6 Steps)

1. **System Check:** Verifies WSL is enabled. If not, it enables the Virtual Machine Platform and requests a **REBOOT**.
2. **Download:** Fetches the latest official AlmaLinux 10 WSL tarball from GitHub.
3. **Directory Prep:** Creates `C:\WSL\dsom-control-almalinux10` for high-performance virtual disk storage.
4. **Import:** Registers the instance via `wsl --import`.
5. **Verification:** Boots the kernel and checks `/etc/almalinux-release`.
6. **Handover Bootstrap:** Executes `setup-dsom-control-node.sh` inside the new instance to install `ansible`, `git`, and configure `wsl.conf`.

---

## 5. Reading the Output & Status Codes

| Label | Meaning | Action Needed |
|:---|:---|:---|
| `[ACTION REQUIRED]` | Feature set updated. | **Reboot** Windows manually. |
| `[PASS]` | Milestone achieved. | Proceed to next step. |
| `[WARNING]` | Instance exists. | Select `y` to wipe and reinstall if corrupted. |
| `[ERROR]` | Network or binary failure. | Check internet connection or WSL subsystem health. |

---

## 6. Security Advisory

> [!IMPORTANT]
> This script installs the Linux environment at `C:\WSL\`. Do not delete this directory while the instance is registered, or you will lose all data inside the T2 control node.

---

## 7. Related Documents

| Document | Purpose |
|:---|:---|
| [`docs/HOWTO-SETUP-WSL-ALMALINUX10.md`](../docs/HOWTO-SETUP-WSL-ALMALINUX10.md) | Full manual setup alternative and troubleshooting. |
| [`HOWTO-SETUP-DSOM-CONTROL-NODE.md`](HOWTO-SETUP-DSOM-CONTROL-NODE.md) | Detailed view of the internal Linux setup phase. |

---

*Standard: DSOM For My AI Protocol v6.1 | Harisfazillah Jamel | LinuxMalaysia*
*Document Version: v1.0 | Created: 2026-04-08*
