# HOWTO: template-reset — Project Purification Tool

## docs/tools/HOWTO-TEMPLATE-RESET.md

> **Standard: DSOM For My AI Protocol v6.1 | Template Utility**
> **Tools:** `template-reset.ps1`, `template-reset.sh`
> **Platforms:** Windows Native (T1), Linux/WSL2 (T2)

---

## 1. Purpose

`template-reset` is the **Project Destructor & Rebirth** script. It is used when you have cloned the DSOM "Skeleton" or a previous project and wish to wipe the historical slate clean to start an entirely new development lifecycle. 

**Use it to:**
- **Purge Git History:** Completely deletes the `.git` directory and re-initializes a fresh repo with no history.
- **Factory Reset Brain:** Overwrites `task.md`, `walkthrough.md`, and `implementation_plan.md` with "Golden Image" starting templates.
- **Cognitive Decoupling:** Ensures the AI doesn't inherit baggage or mental anchors from the project you cloned from.

**Location:** 
- `tools/template-reset.ps1` (Windows)
- `tools/template-reset.sh` (Linux/WSL2)

---

## 2. Prerequisites

| Requirement | Minimum | Notes |
|:---|:---|:---|
| Safe state | **BACKUP** | This tool is **destructive**. Ensure you have no unsaved progress in the source repo. |
| Git | Yes | Git must be present in the path to run `git init`. |

---

## 3. Usage

```powershell
# Windows (T1)
.\tools\template-reset.ps1
```

```bash
# WSL2 / Linux (T2)
bash tools/template-reset.sh
```

### 3.1 Confirmation Prompt

The tool will issue a hard warning before proceeding. You must type `y` or `yes` to authorize the purge of the Git history and brain artifacts.

---

## 4. Operation Workflow (The 2 Purges)

1. **Git Purge:** The script physically deletes the `.git` folder and runs `git init` locally. You will be at "Commit 0".
2. **Artifact Reset:** 
    - `task.md` is reset to "Project Initialization".
    - `walkthrough.md` is reset with a fresh "Session Anchor" for today's date.
    - `implementation_plan.md` is reset to empty Phase 1 goals.

---

## 5. Security Advisory

> [!CAUTION]  
> **Irreversible Action.** This tool does not have an "Undo" feature. Once the `.git` directory is deleted, all historical branches, tags, and commit messages are lost forever from the local copy.

---

## 6. Integration with the Daily Rituals

This is a **Pre-Lifecycle** tool. It is run exactly once after cloning a template but *before* performing your first **Start-of-Day (SOD) Ritual**.

---

## 7. Related Documents

| Document | Purpose |
|:---|:---|
| [`HOWTO-INIT-BRAIN.md`](HOWTO-INIT-BRAIN.md) | A non-destructive alternative that only adds missing files. |
| [`docs/HOWTO-ADOPT-DSOM.md`](../docs/HOWTO-ADOPT-DSOM.md) | Strategy for long-term project adoption. |

---

*Standard: DSOM For My AI Protocol v6.1 | Harisfazillah Jamel | LinuxMalaysia*
*Document Version: v1.0 | Created: 2026-04-08*
