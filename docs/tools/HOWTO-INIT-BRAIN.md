# HOWTO: init-brain — Cognitive Infrastructure Bootstrap

# docs/tools/HOWTO-INIT-BRAIN.md

> **Standard: DSOM For My AI Protocol v6.1 | Foundations**
> **Tools:** `init-brain.ps1`, `init-brain.sh`, `playbooks/dsom/init-brain.yml`
> **Platforms:** Windows Native (T1), Linux/WSL2 (T2)

---

## 1. Purpose

`init-brain` is the **Day Zero Initializer** for any DSOM-compliant repository. It creates the physical directory structure and the foundational Markdown artifacts required for an AI to store and retrieve persistent project state.

**Use it to:**
- Initialize the `.agent/brain/` directory at the repository root.
- Create the 4 core artifacts: `task.md`, `walkthrough.md`, `implementation_plan.md`, and the `DSOM_TEMPLATE.md`.
- Restore missing brain state files if they were accidentally deleted.
- Bootstrapping a fresh "External Memory" for your Cognitive Twin.

**Location:** 
- `tools/init-brain.ps1` (Windows)
- `tools/init-brain.sh` (Linux/WSL2)
- `playbooks/dsom/init-brain.yml` (Ansible)

---

## 2. Prerequisites

| Requirement | Minimum | Notes |
|:---|:---|:---|
| Git | `init` | The repository must be a Git repo (`.git` exists). |
| OS | Any | Works on standard shells. |

---

## 3. Usage

### 3.1 Standard Initialization

```powershell
# Windows (T1)
.\tools\init-brain.ps1
```

```bash
# WSL2 / Linux (T2)
bash tools/init-brain.sh
```

### 3.2 Ansible Provisioning

```bash
ansible-playbook playbooks/dsom/init-brain.yml
```

---

## 4. Manifest Items Created

The tool deploys the following structures safely (**it will not overwrite** existing files):

| Artifact | Purpose |
|:---|:---|
| `.agent/brain/` | The hidden AI context directory. |
| `task.md` | The AI's TODO list. |
| `walkthrough.md` | The session history and Mental Anchor log. |
| `implementation_plan.md` | The roadmap and design goals. |
| `DSOM_TEMPLATE.md` | Standardized format for deep walkthrough sections. |

---

## 5. Integration with the Daily Rituals

This is a **one-time setup** tool. Once the brain is initialized, you should switch to using `audit-pre-flight` at the start of every session to ensure these artifacts remain healthy.

---

## 6. Related Documents

| Document | Purpose |
|:---|:---|
| [`docs/OPERATIONAL-GUIDE.md`](../docs/OPERATIONAL-GUIDE.md) | How the brain files are used in practice. |
| [`HOWTO-AUDIT-PRE-FLIGHT.md`](HOWTO-AUDIT-PRE-FLIGHT.md) | Verification tool for these artifacts. |

---

*Standard: DSOM For My AI Protocol v6.1 | Harisfazillah Jamel | LinuxMalaysia*
*Document Version: v1.0 | Created: 2026-04-08*
