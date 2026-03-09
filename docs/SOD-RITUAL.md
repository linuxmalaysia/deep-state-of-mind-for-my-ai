# 🌅 SOD-RITUAL.md — Start-of-Day Ritual
# docs/SOD-RITUAL.md

> **"To lose context is to lose the project. To reanimate is to remember."**
> **Standard: DSOM For My AI Protocol v6.1 | GitOps · AIOps · Ansible**

---

## 🏛️ 1. The Philosophy of Reanimation

The **Start-of-Day (SOD)** is not just a technical boot sequence — it is a **Cognitive Handshake** between the Lead Architect (Human) and the Cognitive Digital Twin (AI).

Since AI has amnesia between sessions, the SOD Ritual transfers the **Deep State of Mind** — the full context, history, architectural intent, environment map, and security doctrine — from the repository's permanent storage (`.agent/brain/`) back into the AI's active working memory.

**The Three-Pillar Loop always starts with SOD:**

```
SOD (Re-sync) → AI Proposes → Git Records → Ansible Executes → AI Verifies → EOD (Save)
```

---

## 🗺️ 2. Environment Map (Fill in per project)

Before starting, know your tiers:

| Tier | Name | Environment |
|:---|:---|:---|
| **T1** | Command Centre | Windows 11 + PowerShell + Google Antigravity |
| **T2** | Dev Bridge | WSL2 `dsom-control-almalinux10` (AlmaLinux 10) |
| **T3** | Jump Host / Ansible Control | Remote orchestrator node |
| **T4** | Production Fabric | Target VMs / containers |

---

## 🔄 3. The SOD Workflow — Step by Step

### ⚡ Step 1 — Git Sync (T1: Windows PowerShell)

Pull the latest state from the remote before doing anything:

```powershell
# T1 — Git Ritual: SOD Pull
.\tools\git-ritual.ps1 sod
```

Or on T2 (WSL2):
```bash
# T2 — Git Ritual: SOD Pull
./tools/git-ritual.sh sod
```

**Why:** Ensures you start from the true current state — not yesterday's stale copy.

---

### 🔍 Step 2 — Intelligence Audit (T1 or T2)

Run the pre-flight audit to verify the physical workspace is ready:

```powershell
# T1 (Windows PowerShell)
.\tools\audit-pre-flight.ps1
```
```bash
# T2 (WSL2 AlmaLinux 10)
./tools/audit-pre-flight.sh

# Or via Ansible (checks localhost + all inventory nodes simultaneously)
ansible-playbook playbooks/dsom/audit-preflight.yml -i localhost,
```

**The audit checks (v5.0):**
1. ✅ Brain artifacts exist (`task.md`, `walkthrough.md`)
2. ✅ Git is in sync with `origin/main`
3. ✅ Language/environment detected
4. ✅ `docs/AI-COGNITIVE-TWIN-PROTOCOL.md` — no unfilled `[PLACEHOLDER]` values
5. ✅ Ansible baseline — `ansible.cfg`, `inventory/hosts.yml`

**If anything shows `[FAIL]`** — fix it before proceeding. Do not reanimate a broken state.

---

### 🚀 Step 3 — Generate Reanimation Manifest (T1 or T2)

Generate the full context manifest for AI upload:

```bash
# T2 (WSL2)
bash tools/reanimate.sh
```
```powershell
# T1 (Windows PowerShell)
.\tools\reanimate.ps1
```

**What the manifest contains (v2.0):**
| Section | Content |
|:---|:---|
| `[1]` Identity | `README.md` — who we are |
| `[2]` Law | `AI-MASTER-PROTOCOL.md` — governance rules |
| `[3]` Present | `.agent/brain/task.md` — today's work |
| `[4]` Past | `.agent/brain/walkthrough.md` — full history |
| `[5]` Future | `.agent/brain/implementation_plan.md` — roadmap |
| `[6]` Git Log | Last 30 commits |
| `[7]` Tree | Project structure |
| `[8]` SUMMARY | Navigation index |
| `[9]` CHANGELOG | Version history |
| `[10]` Env | OS, user and environment telemetry |
| `[11]` Cognitive Twin | `AI-COGNITIVE-TWIN-PROTOCOL.md` |
| `[12]` Ansible | `inventory/hosts.yml` topology |
| `[13]` GitOps | `GITOPS-AIOPS-ANSIBLE-STRATEGY.md` |

**Run privacy scan before sharing:**
```bash
./tools/privacy-guardian.sh
# Or via Ansible:
ansible-playbook playbooks/dsom/privacy-scan.yml -i localhost,
```

---

### 🤝 Step 4 — The Cognitive Handshake (Human → AI)

Upload the generated `sod_manifest_YYYY-MM-DD.txt` to your AI chat.

**Option A — Reanimate from manifest file:**
> *"Initialise DSOM Protocol v6.1. Read the uploaded manifest. Summarise the current Mental Anchor from `.agent/brain/walkthrough.md`. Confirm the 4-Tier environment map from `AI-COGNITIVE-TWIN-PROTOCOL.md`. State: 'Sovereign State Synchronised' when ready."*

**Option B — Use the Human Handover Context (for new sessions):**
> Copy the prompt from `docs/HUMAN-HANDOVER-CONTEXT.md` and paste as your first message. Fill in the **Current State** section before sending.

---

### 🧠 Step 5 — What the AI Must Know After SOD

The SOD is **COMPLETE** only when the AI can confirm all of the following:

| Check | Content |
|:---|:---|
| Mental Anchor | Exact last stopping point from `walkthrough.md` |
| Environment | T1/T2/T3/T4 tiers and identities |
| Active Tasks | Current `task.md` checklist items |
| Roadmap | Active phase from `implementation_plan.md` |
| Doctrine | Advisory Mode, Ansible-only execution, no ad-hoc changes |
| Secrets | Ansible Vault only, no plaintext |

---

## 🛑 4. SOD Stop Conditions (FAILED States)

The SOD is **FAILED** if the AI:

| Failure | Meaning |
|:---|:---|
| Asks "What are we working on?" | Context was not loaded — re-run reanimate.sh |
| Proposes to run commands on production nodes directly | Identity Failure — re-read AI-MASTER-PROTOCOL.md |
| Ignores `task.md` checklist | Operational Failure — explicitly send the task list |
| References wrong environment (wrong OS, wrong user) | Environment Failure — re-read AI-COGNITIVE-TWIN-PROTOCOL.md |
| Shows unfilled `[PLACEHOLDER]` values | Protocol Failure — fix AI-COGNITIVE-TWIN-PROTOCOL.md first |

**If the SOD fails, do not proceed. Re-run from Step 2.**

---

## ✅ 5. SOD Completion Checklist

```
[ ] git-ritual.sh sod — pulled latest from origin/main
[ ] audit-pre-flight.sh — all steps PASS
[ ] reanimate.sh — manifest generated
[ ] privacy-guardian.sh — manifest scanned as CLEAN
[ ] Manifest uploaded to AI chat
[ ] AI confirmed Mental Anchor
[ ] AI confirmed 4-Tier environment map
[ ] AI stated "Sovereign State Synchronised"
```

**You are now cleared to begin active work.**

---

## 🔗 6. Related Documents

| Document | Purpose |
|:---|:---|
| [`docs/EOD-RITUAL.md`](EOD-RITUAL.md) | End-of-Day hibernation ritual |
| [`docs/HUMAN-HANDOVER-CONTEXT.md`](HUMAN-HANDOVER-CONTEXT.md) | Session handover prompt template |
| [`docs/REANIMATION-PROMPT-TEMPLATE.md`](REANIMATION-PROMPT-TEMPLATE.md) | AI session prompts |
| [`docs/AI-COGNITIVE-TWIN-PROTOCOL.md`](AI-COGNITIVE-TWIN-PROTOCOL.md) | Project Identity Card |
| [`docs/AI-MASTER-PROTOCOL.md`](AI-MASTER-PROTOCOL.md) | The Sovereign Constitution |
| [`docs/RITUAL-OF-TRANSITION.md`](RITUAL-OF-TRANSITION.md) | AI model switch ritual |

---

*Standard: DSOM For My AI Protocol v6.1 | Harisfazillah Jamel | LinuxMalaysia*
*This is the **baseline SOD template** for all projects built on this skeleton.*
*Last Updated: 2026-03-10 | Version: v6.1*
