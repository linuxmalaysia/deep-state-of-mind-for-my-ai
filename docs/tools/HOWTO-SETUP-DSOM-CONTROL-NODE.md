# HOWTO: setup-dsom-control-node — Linux Environment Hardening

# docs/tools/HOWTO-SETUP-DSOM-CONTROL-NODE.md

> **Standard: DSOM For My AI Protocol v6.1 | OS Hardening**
> **Tools:** `setup-dsom-control-node.sh`
> **Platforms:** Linux / AlmaLinux 10 (WSL2 / Bare Metal)

---

## 1. Purpose

`setup-dsom-control-node` is the **System Configuration Engine** for a fresh DSOM Tier 2 node. It transforms a vanilla Linux installation into a fully hardened, Ansible-ready control node with standardized user identities and performance-tuned WSL interoperability settings.

**Use it to:**
- Provision the standard **`dsom-admin`** service user (UID 2001).
- Install the DSOM toolstack: `ansible`, `git`, `rsync`, and `python3-pip`.
- Configure `wsl.conf` for **systemd** support and optimized disk mounting metadata.
- Generate a project-specific ED25519 SSH keypair.
- Set up the global `~/.ansible.cfg` for high-concurrency pipe-lining.

**Location:** 
- `tools/setup-dsom-control-node.sh`

---

## 2. Prerequisites

| Requirement | Minimum | Notes |
|:---|:---|:---|
| OS | AlmaLinux / RHEL 9+ | Specifically tested on AlmaLinux 10. |
| Access | **Root** | Must run as the root user or via `sudo`. |
| Network | External | Requires access to DNF repositories and PyPI (pip). |

---

## 3. Usage

### 3.1 Targeted WSL Deployment

If you used the `setup-wsl-almalinux10.ps1` orchestrator, this tool is run **automatically** on your behalf. To re-run it manually:

```bash
# Run as root inside the WSL instance
bash tools/setup-dsom-control-node.sh
```

---

## 4. Configuration Changes

The tool performs several persistent system modifications:

### 4.1 Identity Management
- Creates group `dsom-admin` (GID 2001).
- Creates user `dsom-admin` (UID 2001).
- Adds user to the `wheel` group.
- Configures **passwordless sudo** via `/etc/sudoers.d/dsom-admin`.

### 4.2 WSL Interoperability (`/etc/wsl.conf`)
- Sets `default=dsom-admin`.
- Enables `systemd=true`.
- Disables `appendWindowsPath=false` (to prevent PATH pollution).
- Mounts `/mnt/c` with `metadata` options enabled (improves permission handling).

### 4.3 SSH Hardening
- Generates `~/.ssh/id_ed25519` for the `dsom-admin` user.
- Sets strict permission 700/600 on the `.ssh` directory.

---

## 5. Reading the Output & Status Codes

| Label | Meaning | Action Needed |
|:---|:---|:---|
| `[PASS]` | Component configured. | None. |
| `[SKIP]` | Feature already exists. | Useful for idempotency checks. |
| `[ERROR]` | Root access missing. | Rerun using `sudo` or `wsl -u root`. |
| `[INFO]` | Public Key displayed. | **Copy this key** to your target node's `authorized_keys`. |

---

## 6. Security Advisory

> [!WARNING]  
> This script disables `appendWindowsPath` in WSL. This means Windows executables (like `code.exe` or `git.exe` from T1) will no longer be in your Linux PATH. This is intentional to ensure your T2 Ansible operations are purely deterministic and isolated.

---

## 7. Related Documents

| Document | Purpose |
|:---|:---|
| [`HOWTO-SETUP-WSL-ALMALINUX.md`](HOWTO-SETUP-WSL-ALMALINUX.md) | The Windows orchestrator that calls this script. |
| [`docs/HOWTO-SETUP-ANSIBLE-BASELINE.md`](../docs/HOWTO-SETUP-ANSIBLE-BASELINE.md) | Next steps for inventory management. |

---

*Standard: DSOM For My AI Protocol v6.1 | Harisfazillah Jamel | LinuxMalaysia*
*Document Version: v1.0 | Created: 2026-04-08*
