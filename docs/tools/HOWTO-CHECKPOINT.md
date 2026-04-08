# HOWTO: checkpoint — Quick Sync

# docs/tools/HOWTO-CHECKPOINT.md

> **Standard: DSOM For My AI Protocol v6.1 | Palace v1.0 | GitOps**
> **Tools:** `checkpoint.ps1`, `checkpoint.sh`, `playbooks/dsom/checkpoint-palace.yml`
> **Platforms:** Windows Native (T1), Linux/WSL2 (T2)

---

## 1. Purpose

The `checkpoint` tool is the **agile mid-task preservation algorithm**. While the formal `eod-palace` ritual restricts and gates git commits behind rigid checklist compliance, the checkpoint workflow allows humans and AIs to dump work-in-progress directly into remote servers rapidly.

**Automated steps performed:**
1. Triggers `palace-sync` to parse the git log without forcing a pause or waiting for user interaction.
2. Identifies all currently tracked modifications. Commits them independently safely as `chore(checkpoint): modified tracked files`.
3. Identifies absolutely all untracked configurations. Generates an independent boundary commit `chore(checkpoint): untracked new files`.
4. Executes `git push origin main`.

**Location:** 
* `tools/checkpoint.ps1` (Native Windows)
* `tools/checkpoint.sh` (Proxy wrapper)
* `playbooks/dsom/checkpoint-palace.yml` (Ansible)

---

## 2. Prerequisites

| Requirement | Minimum | Notes |
|:---|:---|:---|
| Safe state | Compiling Code | Even though testing is skipped, do not drop a checkpoint that bricks the framework syntax. |

---

## 3. Usage

```powershell
# Windows (T1)
.\tools\checkpoint.ps1
```

```bash
# WSL2 / Linux (T2)
bash tools/checkpoint.sh
```

---

## 4. Reading the Output & Status Codes

| Event Message | Meaning |
|:---|:---|
| `Committed tracked modifications` | Previously watched files were updated. |
| `Committed untracked configurations` | Brand new `.md` or scripts were included. |

*(The script gracefully handles entirely clean workspaces without throwing git or PowerShell null-value execution exceptions.)*

---

## 5. Integration with the Daily Rituals

Use this continuously every 60-90 minutes throughout active development. Since checkpoint operations securely bundle Palace update proposals alongside them recursively, you can run multiple checkpoints safely without disrupting the final End-of-Day Palace reconciliation phase.

---

## 6. Related Documents

| Document | Purpose |
|:---|:---|
| [`HOWTO-EOD-PALACE.md`](HOWTO-EOD-PALACE.md) | Use EOD at the absolute end of the human sequence. |
| [`HOWTO-PALACE-SYNC.md`](HOWTO-PALACE-SYNC.md) | Details how the background Palace proposal is continuously merged in. |

---

*Standard: DSOM For My AI Protocol v6.1 | Palace v1.0 | Harisfazillah Jamel*
*Document Version: v1.0 | Created: 2026-04-08*
