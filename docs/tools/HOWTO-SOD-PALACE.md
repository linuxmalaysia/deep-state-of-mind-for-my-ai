# HOWTO: sod-palace — Start-of-Day Ritual

# docs/tools/HOWTO-SOD-PALACE.md

> **Standard: DSOM For My AI Protocol v6.1 | Palace v1.0 | GitOps**
> **Tools:** `sod-palace.ps1`, `sod-palace.sh`, `playbooks/dsom/sod-palace.yml`
> **Platforms:** Windows Native (T1), Linux/WSL2 (T2)

---

## 1. Purpose

The `sod-palace` toolkit natively automates the **Sovereign Start-of-Day (SOD) Mechanical Loop** utilizing Palace Registry bindings. It unifies operations that previously had to be executed sequentially by hand, safely bringing your local workspace into convergence with `origin/main` while validating your cognitive twin state.

**Automated steps performed:**
1. Triggers `git pull --rebase` to ensure tracking parity.
2. Invokes the `audit-pre-flight` checks to scan structural/config deviations.
3. Detects if `.agent/brain/palace_registry.md` is initialized.
4. Binds the entire output into the dense `sod_manifest_YYYY-MM-DD.txt` artifact using the `reanimate` payload.

**Location:** 
* `tools/sod-palace.ps1` (Native Windows Execution)
* `tools/sod-palace.sh` (Proxy Execution for Bash)
* `playbooks/dsom/sod-palace.yml` (Ansible Backend for Linux environments)

---

## 2. Prerequisites

| Requirement | Minimum | Notes |
|:---|:---|:---|
| Protocol Level | DSOM v6.1 / Palace v1.0 | Requires the `palace_registry.md` artifact framework. |
| Platform (Windows) | Windows 10/11 | Pure PowerShell fallback (No Ansible needed). |
| Platform (Linux) | Any POSIX system | Ansible core must be installed. |

---

## 3. Usage

### 3.1 Standard Execution 

```powershell
# Windows (T1)
.\tools\sod-palace.ps1
```

```bash
# WSL2 / Linux (T2)
bash tools/sod-palace.sh
```

### 3.2 Output Workflow

You will sequentially see the Git operations flow, followed by the outcome of `[PASS] / [FAIL]` diagnostics from the audit. At the conclusion, the tool will drop an explicit path pointing definitively to your new SOD Manifest.

---

## 4. Reading the Output & Status Codes

| Output Keyword | Meaning | Action Needed |
|:---|:---|:---|
| `[OK] Palace Registry found` | Spatial integration is primed. | Proceed normally. |
| `[WARN] Palace Registry missing` | Workspace is missing index. | Run `tools/palace-sync` to initialize. |
| `[FAIL] Security Validation` | Audit mechanism found issues. | Investigate failed tests before continuing. |

---

## 5. Integration with the Daily Rituals

This script completely replaces Steps 1 through 3 of the legacy DSOM `docs/SOD-RITUAL.md`. Execute it as the absolute **first action** upon starting your work sequence. After completion, simply share the created `.txt` manifest with the AI context to initiate full session awareness.

---

## 6. Related Documents

| Document | Purpose |
|:---|:---|
| [`docs/SOD-RITUAL.md`](../SOD-RITUAL.md) | Full workflow guide integrating this hook. |
| [`HOWTO-REANIMATE.md`](HOWTO-REANIMATE.md) | Details the internal generation mechanism driving the `.txt` manifest. |
| [`HOWTO-PALACE-SYNC.md`](HOWTO-PALACE-SYNC.md) | Mechanism for managing the Palace array structure. |

---

*Standard: DSOM For My AI Protocol v6.1 | Palace v1.0 | Harisfazillah Jamel*
*Document Version: v1.0 | Created: 2026-04-08*
