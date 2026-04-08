# ♻️ Template Reset (template-reset.sh)

> **"Tabula Rasa."** - Returning to the beginning.

## 1. 🏛️ Purpose

**Version:** v1.0
**Description:** Prepares a DSOM clone for a new project. It purges old Git history (`.git`) and resets brain artifacts to a blank "Golden Image" state while preserving the Master Protocol and tools.

## 2. 🛡️ Safety Mechanisms

| Mechanism | Status | Description |
| :--- | :--- | :--- |
| **Confirmation Guard** | ✅ Active | Requires explicit `y` input to proceed. |
| **Destructive Warn** | ✅ Active | Clearly warns about Git history deletion. |
| **Exit-on-Error** | ✅ Active | `set -e` injected. |

## 3. ⚙️ Usage

```bash
./tools/template-reset.sh
```

## 4. 🧠 Logic Flow

1. **Repo Check:** Ensures execution inside a git repo.
2. **Confirmation:** Blocks execution until user confirms.
3. **Git Purge:** `rm -rf .git` and `git init`.
4. **Brain Wipe:** Overwrites `task.md`, `walkthrough.md`, `implementation_plan.md` with default "New Project" templates.
5. **Instruction:** Guides user to add files and start fresh history.

## 5. 📝 Extracted Comments
>
> "Prepares a DSOM clone for a new project. It purges old Git history and resets brain artifacts to a 'Golden Image' state."
