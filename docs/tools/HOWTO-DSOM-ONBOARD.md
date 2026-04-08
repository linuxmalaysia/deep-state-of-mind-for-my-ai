# HOWTO: dsom-onboard — Repository Adoption Engine

# docs/tools/HOWTO-DSOM-ONBOARD.md

> **Standard: DSOM For My AI Protocol v6.1 | External Adoption**
> **Tools:** `dsom-onboard.ps1`, `dsom-onboard.sh`, `onboard-dsom.yml`
> **Platforms:** Windows Native (T1), Linux/WSL2 (T2)

---

## 1. Purpose

`dsom-onboard` is the **Architectural Grafting Tool**. It allows you to take any existing Git repository and "Onboard" it into the Deep State of Mind framework. It automates the complex process of injecting the `.agent/brain/`, `playbooks/dsom/`, and `tools/` ecosystems into a foreign project without causing file collisions or git history corruption.

**Use it to:**
- Convert a normal project into a DSOM-compliant repository.
- Safe-import the DSOM orchestration fleet into a brand new project.
- Ensure "Zero-Debt" adoption by utilizing temporary Git branch isolation.
- Automatically merge core governance docs (Identity, Master Protocol, etc.) into the target.

**Location:** 
- `tools/dsom-onboard.ps1` (Windows)
- `tools/dsom-onboard.sh` (Linux/WSL2)
- `playbooks/dsom/onboard-dsom.yml` (Ansible)

---

## 2. Prerequisites

| Requirement | Minimum | Notes |
|:---|:---|:---|
| Git | Yes | Repository must be initialized. |
| Ansible | Yes | Required for the file-matching and merging backend. |
| WSL2 | Yes | Required for Windows execution (proxies via `wsl`). |

---

## 3. Usage

### 3.1 Bootstrap Execution

You do NOT need to manually download the DSOM repository to use this. You only need the bootstrap script:

```powershell
# Windows (T1)
.\tools\dsom-onboard.ps1
```

```bash
# WSL2 / Linux (T2)
bash tools/dsom-onboard.sh
```

---

## 4. Operation Workflow (The 4 Steps)

The tool performs a non-destructive multi-phase integration:

1. **Dependency Check:** Verifies Git, WSL, and Ansible are present.
2. **Branch Isolation:** Creates a new branch (e.g., `dsom-onboarding-YYYY-MM-DD`). 
3. **Payload Download:** Fetches the latest `onboard-dsom.yml` directly from the main DSOM GitHub.
4. **Ansible Fusion:** Executes the playbook to physically copy and rename files into your target repo.

---

## 5. Collision Handling

> [!NOTE]  
> If your target repository already has a file with the same name as a DSOM file (e.g., `README.md`), the tool **will not overwrite it**. Instead, it renames the incoming DSOM file to include the today's timestamp so you can manually reconcile the contents.

---

## 6. Finalizing the Adoption

After the script finishes, you must perform the following Git manual steps:

1. Review the changes using `git status`.
2. Commit the incoming framework: `git add . && git commit -m 'chore(dsom): onboard framework architecture'`.
3. Merge the onboarding branch into your `main` branch.
4. Run `init-brain` to finalize the cognitive infrastructure.

---

## 7. Related Documents

| Document | Purpose |
|:---|:---|
| [`docs/HOWTO-DSOM-ONBOARDING.md`](../docs/HOWTO-DSOM-ONBOARDING.md) | High-level procedural guide for humans. |
| [`HOWTO-INIT-BRAIN.md`](HOWTO-INIT-BRAIN.md) | The next tool to run after a successful onboard. |

---

*Standard: DSOM For My AI Protocol v6.1 | Harisfazillah Jamel | LinuxMalaysia*
*Document Version: v1.0 | Created: 2026-04-08*
