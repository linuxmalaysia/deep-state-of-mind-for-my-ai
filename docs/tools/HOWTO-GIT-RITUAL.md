# HOWTO: git-ritual — Sovereign GitOps Hygene

# docs/tools/HOWTO-GIT-RITUAL.md

> **Standard: DSOM For My AI Protocol v6.1 | GitOps Sovereign Tool**
> **Tools:** `git-ritual.ps1`, `git-ritual.sh`
> **Platforms:** Windows Native (T1), Linux/WSL2 (T2)

---

## 1. Purpose

`git-ritual` is the **Atomic Git Hygene** enforcer for the DSOM framework. It ensures that every session save (Sovereign Save) follows the **Conventional Commits** standard and includes mandatory Phase/Version metadata for long-term project auditability.

**Use it to:**
- Perform a structured Start-of-Day (SOD) sync (pull from origin).
- Build semantic commit messages with correct scopes and type tags.
- Execute the "Sovereign Save" during End-of-Day (EOD) or mid-task milestones.
- Maintain a clean, human-and-AI-readable git history.

**Location:** 
- `tools/git-ritual.ps1` (Windows)
- `tools/git-ritual.sh` (Linux/WSL2)

---

## 2. Prerequisites

| Requirement | Minimum | Notes |
|:---|:---|:---|
| Git | 2.0+ | Must be installed and in the PATH. |
| Remote | `origin` | Must have an upstream named `origin`. |
| Branch | `main` | Default operations target the `main` branch. |

---

## 3. Usage

### 3.1 Start-of-Day Sync (SOD)

```powershell
.\tools\git-ritual.ps1 sod
```

```bash
bash tools/git-ritual.sh sod
```

Fetches from origin and performs a rebase pull if the branch has diverged.

### 3.2 Interactive Sovereign Save (EOD/Default)

```powershell
.\tools\git-ritual.ps1
```

```bash
bash tools/git-ritual.sh
```

Follow the interactive prompts to:
1. Select a **Type** (feat, fix, docs, chore, etc.).
2. Define a **Scope** (e.g., `ansible`, `brain`, `infrastructure`).
3. Write a **Description**.
4. (Optional) Add a **Phase Tag** (e.g., `Phase-5/v1.2`).

### 3.3 Direct Commit and Push

```powershell
.\tools\git-ritual.ps1 push "feat(auth): add login flow [v1.0]"
```

```bash
bash tools/git-ritual.sh push "feat(auth): add login flow [v1.0]"
```

Stages all changes (`git add -A`), commits with the provided message, and pushes to `origin main`.

---

## 4. Reading the Output & Status Codes

| Label | Meaning | Action |
|:---|:---|:---|
| `[OK]` | Already up to date. | Proceed with the ritual. |
| `[DONE]` | Operation successful. | None needed. |
| `[CLEAN]` | Nothing to commit. | You are already syncronised. |
| `[ERROR]` | Invalid input or git failure. | Check the error message and retry. |
| `[ABORTED]` | User cancelled the push. | State remains unsaved in Git. |

---

## 5. Integration with the Daily Rituals

### 5.1 Start-of-Day (SOD)
Run `git-ritual sod` to ensure you are building on the latest state before executing `audit-pre-flight`.

### 5.2 End-of-Day (EOD)
Run the interactive `git-ritual` to finalize the session. It is often triggered as the final step of the **EOD Ritual** to cement the "Sovereign State".

---

## 6. Related Documents

| Document | Purpose |
|:---|:---|
| [`docs/SOD-RITUAL.md`](../SOD-RITUAL.md) | Standard Operating Procedure for Start-of-Day. |
| [`docs/EOD-RITUAL.md`](../EOD-RITUAL.md) | Standard Operating Procedure for End-of-Day. |
| [`AI-MASTER-PROTOCOL.md`](../AI-MASTER-PROTOCOL.md) | Governance laws requiring Atomic Git Hygiene. |

---

*Standard: DSOM For My AI Protocol v6.1 | Harisfazillah Jamel | LinuxMalaysia*
*Document Version: v1.0 | Created: 2026-04-08*
