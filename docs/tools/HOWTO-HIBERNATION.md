# HOWTO: hibernation — Legacy Safety Verifier

# docs/tools/HOWTO-HIBERNATION.md

> **Standard: DSOM For My AI Protocol v6.1 | Core Framework**
> **Tools:** `hibernation.ps1`, `hibernation.sh`
> **Platforms:** Windows Native (T1), Linux/WSL2 (T2)

---

## 1. Purpose

The `hibernation` scripts function as safety gates that strictly prohibit the termination of a computing cycle until certain cognitive markers are recorded in the AI’s memory bank. If an AI or human fails to populate `.agent/brain/task.md` or anchor the session properly in `.agent/brain/walkthrough.md`, the repository refuses to enter a valid shutdown state.

**Location:** 
* `tools/hibernation.ps1`
* `tools/hibernation.sh`

---

## 2. Prerequisites

| Requirement | Minimum | Notes |
|:---|:---|:---|
| Structural Context | `task.md` | Required to test presence of completed `[x]`. |
| Structural Context | `walkthrough.md` | Required to scan for `YYYY-MM-DD` literal anchors. |

---

## 3. Usage

```powershell
.\tools\hibernation.ps1
```

```bash
bash tools/hibernation.sh
```

---

## 4. Reading the Output & Status Codes

| Output Keyword | Meaning | Action Needed |
|:---|:---|:---|
| `[OK] Progress detected` | Brain state verified. | Proceed to EOD push. |
| `[ERR] No Session Anchor` | AI missed the semantic tracking. | Open `walkthrough.md` and explicitly add `## Mental Anchor -- [Date]`. |
| `HIBERNATION BLOCKED` | Hard fatal failure exit code 1. | Read errors above to remediate environment. |

---

## 5. Integration with the Daily Rituals

> [!WARNING]  
> If you are utilizing the advanced spatial navigation protocol (**Palace v1.0**), you primarily do *not* need to run this tool standalone. The `tools/eod-palace.ps1` routines automatically bundle the hibernation safety checkpoints natively inside their operation flow.

Only use `hibernation.sh` directly if you operate in environments pre-dating Palace (e.g. legacy DSOM framework integrations).

---

## 6. Related Documents

| Document | Purpose |
|:---|:---|
| [`HOWTO-EOD-PALACE.md`](HOWTO-EOD-PALACE.md) | Modern EOD wrapper encompassing Hibernation logic. |

---

*Standard: DSOM For My AI Protocol v6.1 | Palace v1.0 | Harisfazillah Jamel*
*Document Version: v1.0 | Created: 2026-04-08*
