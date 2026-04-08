# HOWTO: eod-palace — End-of-Day Saves

# docs/tools/HOWTO-EOD-PALACE.md

> **Standard: DSOM For My AI Protocol v6.1 | Palace v1.0 | GitOps**
> **Tools:** `eod-palace.ps1`, `eod-palace.sh`, `playbooks/dsom/eod-palace.yml`
> **Platforms:** Windows Native (T1), Linux/WSL2 (T2)

---

## 1. Purpose

The `eod-palace` toolkit natively automates the **Sovereign End-of-Day (EOD) Loop**. It aggressively hardens your work by systematically enforcing rules from the DSOM specification—prohibiting pushes unless tasks are actually completed and cognitive state logic is stored.

**Automated steps performed:**
1. Validates that `task.md` contains completed `[x]` markings.
2. Validates that `walkthrough.md` contains today's `YYYY-MM-DD` mental anchor.
3. Automatically evaluates `git log` and invokes `tools/palace-sync` to map changed files to `.agent/brain/wings/` logic.
4. Stages the precise brain artifacts and specific active files instead of blindly invoking `git add .`
5. Formats the explicit semantic commit `chore(eod): Palace sync + sovereign save`.
6. Triggers `git push origin main`.

**Location:** 
* `tools/eod-palace.ps1` (Native Windows format)
* `tools/eod-palace.sh` (Proxy wrapper)
* `playbooks/dsom/eod-palace.yml` (Ansible backend)

---

## 2. Prerequisites

| Requirement | Minimum | Notes |
|:---|:---|:---|
| Protocol Level | DSOM v6.1 / Palace v1.0 | Depends on the physical existence of `task.md` |
| Connectivity | Online | Must reach `origin` upstream or it will flag. |

---

## 3. Usage

```powershell
# Windows (T1)
.\tools\eod-palace.ps1
```

```bash
# WSL2 / Linux (T2)
bash tools/eod-palace.sh
```

---

## 4. Reading the Output & Status Codes

| Output Flag | Colour | Meaning | Remediation |
|:---|:---|:---|:---|
| `[FAIL] No completed tasks found` | Red | Guardrail block. | Check `[x]` items inside `task.md`. |
| `[FAIL] Session anchor NOT found` | Red | Guardrail block. | Ensure today's date exists in `walkthrough.md`. |
| `(nothing new to commit)` | Dark Grey | Safe skip. | Working tree was already clean from Checkpoints. |

---

## 5. Integration with the Daily Rituals

This script enforces final Git execution before shutdown and replaces manual interactions entirely for Palace implementations. Following a successful run, the script deposits a `palace_update_proposal_YYYY-MM-DD.md` holding Git mappings. It expects that the AI will read this proposal and make modifications to `closet.md` locations on the *next day's* SOD context.

---

## 6. Related Documents

| Document | Purpose |
|:---|:---|
| [`docs/EOD-RITUAL.md`](../EOD-RITUAL.md) | Overall End-of-Day structure details. |
| [`HOWTO-CHECKPOINT.md`](HOWTO-CHECKPOINT.md) | Using continuous saves dynamically throughout the day safely *without* EOD validation tests. |

---

*Standard: DSOM For My AI Protocol v6.1 | Palace v1.0 | Harisfazillah Jamel*
*Document Version: v1.0 | Created: 2026-04-08*
