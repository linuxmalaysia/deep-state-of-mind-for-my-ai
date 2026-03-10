# 🤝 Contributing to Deep State of Mind (DSOM)

> **"Every contribution is a Git commit with intent. Every commit is a sovereign act."**
> Standard: DSOM For My AI Protocol v6.1 | GitOps · AIOps · Ansible

Thank you for contributing to the **DSOM For My AI Protocol** — the governance skeleton that transforms any AI into a disciplined Cognitive Digital Twin.

This project is the **baseline template** for all DSOM-based projects. Every improvement here propagates downstream to every project that inherits this skeleton. Contributing here requires not just code, but **Cognitive Alignment** with the SOD/EOD ritual model and the three-pillar doctrine.

---

## 🧭 1. Overview: The Hybrid Development Model

DSOM uses a **Hybrid Development Model** — leveraging the strengths of both **Windows 11** (where AI agents often operate) and **Linux WSL2** (where Ansible and tools execute).

```
[ T1: Windows 11 + PowerShell + AI ]
          ↓ git push / AI generates code
[ T2: WSL2 dsom-control-almalinux10 ]  ← contributors work here
          ↓ ansible-playbook / testing
[ T3/T4: Target Nodes / Production ]
```

**Key rule:** Code is written on T1 (Windows/IDE), **tested** on T2 (WSL2), and deployed via Ansible to T3/T4. Never bypass this path.

---

## 🏗️ 2. Contributor Environment Setup

### 2.1 Required Software (T1 — Windows)
- **VS Code** with the DSOM/Antigravity extension
- **Git for Windows** (or Windows Terminal + Git)
- **PowerShell** terminal

### 2.2 Required Software (T2 — WSL2 AlmaLinux 10)

Set up the DSOM Ansible Control Node WSL2 instance:

```powershell
# Run from Windows PowerShell (as Administrator once)
.\tools\setup-wsl-almalinux10.ps1
```

This creates: `dsom-control-almalinux10` WSL2 instance with:
- `dsom-admin` identity (UID 2001)
- Ansible, Git, rsync pre-installed
- `/etc/wsl.conf` configured (systemd, default user, clean PATH)

> See [`docs/HOWTO-SETUP-WSL-ALMALINUX10.md`](docs/HOWTO-SETUP-WSL-ALMALINUX10.md) for the full guide.

### 2.3 The Mirror Environment (Path Synchronisation)

Maintain **absolute parity** between T1 and T2 at all times:

| T1 (Windows) | T2 (WSL2 Mount) |
|:---|:---|
| `D:\Users\[YOU]\Projects\[PROJECT]` | `/mnt/d/Users/[YOU]/Projects/[PROJECT]` |

**After every T1 push, sync T2:**
```bash
# Inside dsom-control-almalinux10
cd /mnt/d/Users/[YOU]/Projects/[PROJECT]
git pull origin main
```

---

## 🔐 3. Security First

| Rule | Detail |
|:---|:---|
| **No secrets in Git** | All secrets via `ansible-vault`. Never commit plaintext passwords, tokens, or keys. |
| **`vault/` is Git-ignored** | Local vault files must NEVER be committed. |
| **Privacy scan before sharing** | Always run `./tools/privacy-guardian.sh` before sharing any manifest. |
| **SSH keys only** | Ansible connects to target nodes via SSH key authentication only. |
| **No force-push to `main`** | Protected branch. PRs required. |

---

## 🤖 4. Human-AI Collaboration Protocol

### 4.1 The Human Architect Role
- **Authority:** Defines the mission, approves implementation plans
- **Verification:** Runs scripts in T2 WSL2, pastes output back to AI
- **Approval:** Every AI proposal must be reviewed and approved before execution
- **Git:** All `git add`, `git commit`, `git push` done from T1 (Windows/PowerShell)

### 4.2 The AI Agent Role
- **Advisory Only:** Proposes code, playbooks, configs — never executes directly
- **Explains Why:** Always explains the architectural reason before the technical what
- **Waits for output:** Does not proceed to next step until human pastes terminal output
- **Brain Keeper:** Updates `.agent/brain/task.md` and `walkthrough.md` during work

### 4.3 The Permanent Context (Mandatory Reading for AI)

Every AI agent session must begin by reading:
1. `docs/HUMAN-HANDOVER-CONTEXT.md` — Project Identity Card + Session Handover
2. `.agent/brain/task.md` — Current tasks
3. `.agent/brain/walkthrough.md` — Project history + Mental Anchor
4. `docs/AI-MASTER-PROTOCOL.md` — Governance laws

### 4.4 The SOD/EOD Handover Ritual

Every contributor — human or AI — must follow the daily ritual:

**Start of Day (SOD):**
```bash
./tools/git-ritual.sh sod         # Pull latest
./tools/audit-pre-flight.sh       # Verify workspace
bash tools/reanimate.sh           # Generate AI context manifest
# → Upload manifest or paste Hibernation Notes → AI reads → begin
```
> Full guide: [`docs/SOD-RITUAL.md`](docs/SOD-RITUAL.md)

**End of Day (EOD):**
```bash
# 1. Ask AI to update task.md + walkthrough.md Mental Anchor
# 2. Run Hibernation Notes Export prompt (see EOD-RITUAL.md Step 1b)
./tools/hibernation.sh            # Safety check
./tools/git-ritual.sh             # Interactive EOD commit + push
```
> Full guide: [`docs/EOD-RITUAL.md`](docs/EOD-RITUAL.md)

---

## 🚀 5. Step-by-Step Contribution Workflow

### Step 0 — Environment Setup
Follow Section 2 above. Verify:
```bash
# Inside dsom-control-almalinux10
ansible --version
ansible localhost -m ping
```

### Step 1 — Fork and Clone
```bash
# Fork on GitHub first, then:
git clone https://github.com/[YOUR_FORK]/deep-state-of-mind-for-my-ai.git
cd deep-state-of-mind-for-my-ai
chmod +x tools/*.sh
```

### Step 2 — Initialise the Brain
```bash
bash tools/init-brain.sh
# Or via Ansible:
ansible-playbook playbooks/dsom/init-brain.yml -i localhost,
```

### Step 3 — Run Pre-Flight Audit
```bash
./tools/audit-pre-flight.sh
# All steps must show [PASS]
```

### Step 4 — Create a Feature Branch
```bash
git checkout -b feat/[your-feature-name]
# Example: feat/add-template-reset-playbook
```

### Step 5 — The Development Loop

1. **Modify** — Edit files in VS Code (T1) or directly in T2 WSL2
2. **Ansible-lint** (for playbooks) — Run inside T2:
   ```bash
   ansible-lint playbooks/dsom/[your-playbook].yml
   ```
3. **Test** — Run your changes on localhost first:
   ```bash
   ansible-playbook playbooks/dsom/[your-playbook].yml -i localhost, --check
   ansible-playbook playbooks/dsom/[your-playbook].yml -i localhost,
   ```
4. **Update Brain** — Update `.agent/brain/task.md` and `walkthrough.md` with what you changed and why
5. **Commit** — Every sub-task gets its own atomic commit:
   ```bash
   git add [specific-file]
   git commit -m "type(scope): description [Phase/vX.X]"
   ```

### Step 6 — Atomic Git Mastery

**Critical before pushing** — parity check on T1 AND T2:
```powershell
# T1 (Windows PowerShell)
git status
```
```bash
# T2 (WSL2)
git status
```
Both must show the same state. Then push:
```bash
git push origin feat/[your-feature-name]
```

### Step 7 — Open a Pull Request

Use the PR template (`.github/PULL_REQUEST_TEMPLATE.md`). Your PR must include:

- **What changed** — specific files and what they do
- **Why** — the architectural reason (the "Why" before the "What")
- **Test evidence** — paste the output of your audit and test runs
- **Walkthrough update** — confirm `walkthrough.md` has a new Session Anchor

---

## ⚖️ 6. Architectural Mandates

### 6.1 The CRISP² Operational Strategy
| Pillar | Requirement |
|:---|:---|
| **Context** | Always sync with `.agent/brain/` before changes |
| **Review & Record** | Document "Why" in `walkthrough.md` *before* committing |
| **Iteration** | Atomic Git: one logical change per commit |
| **Single-purpose** | PRs must address one specific sub-task |
| **Partnership** | Maintain the Senior Architect persona at all times |

### 6.2 The Three Pillars (Non-Negotiable)
1. **AIOps** — AI is Advisory only. Proposes, never executes.
2. **GitOps** — If it is not in Git, it does not exist.
3. **Ansible** — The exclusive OS-level executor. No ad-hoc SSH changes to nodes.

### 6.3 Coding Laws
| Law | Rule |
|:---|:---|
| **Idempotency** | Every Ansible playbook must be safe to re-run |
| **No Secrets** | `ansible-vault` only. Zero plaintext secrets |
| **UK English** | All documentation, comments, and commit messages |
| **Sovereign Portability** | Code must be Linux-agnostic, no vendor lock-in |

---

## 📝 7. Commit Message Standard

Format: `type(scope): description [Phase/vX.X]`

| Type | When to use |
|:---|:---|
| `feat` | New feature or capability |
| `fix` | Bug fix or correction |
| `docs` | Documentation only changes |
| `chore` | Brain artifacts, EOD saves, maintenance |
| `refactor` | Restructure without behaviour change |
| `ci` | CI/CD pipeline changes |

**Good examples:**
```
feat(playbooks): add template-reset Ansible playbook [Phase-2/v6.2]
docs(sod): add Step 4c for Claude-specific reanimation [v6.1]
fix(audit): correct Ansible baseline check for AlmaLinux 10 [Phase-1/v6.1]
chore(brain): EOD sovereign save — AlmaLinux 10 WSL setup complete [v6.1.1]
```

**Bad examples:**
```
update files
fix bug
done
```

---

## 🔄 8. Contribution Types We Welcome

| Type | Examples |
|:---|:---|
| **New Ansible Playbooks** | DSOM operational tools for `playbooks/dsom/` |
| **New tools/ scripts** | bash or PowerShell tools for SOD/EOD rituals |
| **Documentation** | Improve HOWTO guides, SOD/EOD rituals, protocol docs |
| **New AI formats** | Reanimation prompt templates for new AI providers |
| **Bug fixes** | Fix issues in existing tools or playbooks |
| **Template improvements** | Enhance `AI-COGNITIVE-TWIN-PROTOCOL.md` or `HUMAN-HANDOVER-CONTEXT.md` |

---

## 📡 9. Providing Output for Review

When the AI asks for output, use one of these methods:

| Method | Command |
|:---|:---|
| **Direct paste** | Copy full terminal output into AI chat |
| **Log file** | `bash tools/audit-pre-flight.sh \| tee audit.log` — share file content |
| **Ansible output** | `ansible-playbook playbooks/dsom/audit-preflight.yml -i localhost, \| tee audit_ansible.log` |

AI will **wait for your results** before proceeding. Never assume success.

---

## 📄 10. License

All contributions are licensed under the **GNU General Public License v3.0**.
By submitting a PR, you agree that your contribution is licensed under GPL v3.0.

---

## 🔗 Key Documents for Contributors

| Document | Read When |
|:---|:---|
| [`docs/SOD-RITUAL.md`](docs/SOD-RITUAL.md) | Every morning before starting work |
| [`docs/EOD-RITUAL.md`](docs/EOD-RITUAL.md) | Every evening before stopping work |
| [`docs/HUMAN-HANDOVER-CONTEXT.md`](docs/HUMAN-HANDOVER-CONTEXT.md) | First message to your AI agent |
| [`docs/AI-MASTER-PROTOCOL.md`](docs/AI-MASTER-PROTOCOL.md) | Understanding AI governance laws |
| [`docs/HOWTO-SETUP-WSL-ALMALINUX10.md`](docs/HOWTO-SETUP-WSL-ALMALINUX10.md) | Setting up your T2 environment |
| [`docs/HOWTO-SETUP-ANSIBLE-BASELINE.md`](docs/HOWTO-SETUP-ANSIBLE-BASELINE.md) | Configuring Ansible for your project |
| [`docs/GITOPS-AIOPS-ANSIBLE-STRATEGY.md`](docs/GITOPS-AIOPS-ANSIBLE-STRATEGY.md) | Understanding the three-pillar doctrine |

---

*Open Source Sovereignty | Harisfazillah Jamel (LinuxMalaysia)*
*DSOM For My AI Protocol v6.1 | GitOps · AIOps · Ansible*
*Last Updated: 2026-03-10*
