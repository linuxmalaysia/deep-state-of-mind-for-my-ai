# 🧠 Deep State of Mind (DSOM) For My AI Protocol

> **"Make AI work for you — not the other way around. Sovereign Intelligence through GitOps, AIOps, and Ansible."**

[![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)]()
[![Version](https://img.shields.io/badge/Version-10.0.0--palace-blue.svg)]()
[![Palace](https://img.shields.io/badge/Palace-v1.0-9b59b6.svg)](docs/DIGITAL-SOVEREIGNTY-OPERATIONAL-MODEL-PALACE.md)
[![License](https://img.shields.io/badge/License-GPL--3.0-orange.svg)]()
[![Author](https://img.shields.io/badge/Author-Harisfazillah%20Jamel-blue.svg)]()
[![Standard](https://img.shields.io/badge/AI%20Standard-Cognitive%20Digital%20Twin-purple.svg)]()

---

## 🎯 What is DSOM?

**Deep State of Mind (DSOM)** is a **metacognitive governance framework** that transforms any AI (Gemini, Claude, Copilot, ChatGPT) into a disciplined **Cognitive Digital Twin** — an AI agent that thinks and operates like your Senior Systems Architect.

It solves three critical AI problems:

| Problem | DSOM Solution |
|:---|:---|
| **Context Decay** — AI forgets everything after each session | `.agent/brain/` artifacts persist the project state permanently |
| **Vendor Lock-in** — Moving between AI tools loses all context | All knowledge lives in your Git repo, not inside the AI |
| **Uncontrolled Execution** — AI runs commands you didn't approve | Advisory Mode + GitOps + Ansible enforce human-approval-first |

---

## 🏛️ The Three Pillars (v6.1)

Every project built on this skeleton operates under **three non-negotiable pillars**:

```
┌─────────────────────────────────────────────────────┐
│                DSOM OPERATING MODEL                 │
│                                                     │
│  ┌──────────┐   ┌──────────┐   ┌─────────────────┐ │
│  │  AIOps   │──▶│  GitOps  │──▶│    Ansible      │ │
│  │  (Mind)  │   │ (Record) │   │ (Hand/Executor) │ │
│  └──────────┘   └──────────┘   └─────────────────┘ │
│       │               │                 │           │
│  AI proposes    Git records       Ansible runs      │
│  & analyses     all state         on target nodes   │
│       ▲               │                 │           │
│       └───────────────┴─── AI verifies ─┘           │
└─────────────────────────────────────────────────────┘
```

**The core loop:**
> **AI Proposes → Git Records → Ansible Executes → AI Verifies**

### The Three Hard Rules
1. **AI never runs commands directly on remote nodes.** It writes Ansible playbooks. You run them.
2. **No manual edits to production servers.** If it's not committed to Git, it doesn't exist.
3. **Every playbook is idempotent.** Safe to re-run at any time.

---

## 🚀 Quick Start: Using This as Your Project Template

### Prerequisites
| Tool | Purpose | Min Version |
|:---|:---|:---|
| `git` | Version control (GitOps backbone) | 2.30+ |
| `bash` or `PowerShell` | Running tools | Any |
| `ansible` | OS-level automation (infra projects) | 2.15+ |
| Any AI | Your Cognitive Twin | Any |

### Step 1 — Clone and Reset
```bash
# Clone the DSOM skeleton
git clone https://github.com/linuxmalaysia/deep-state-of-mind-for-my-ai.git my-new-project
cd my-new-project

# Reset for your new project (clears old Git history and brain files)
bash tools/template-reset.sh
```

### Step 2 — Initialise the Brain
```bash
# Linux / WSL2
bash tools/init-brain.sh
chmod +x tools/*.sh

# Windows (PowerShell)
.\tools\init-brain.ps1
```

This creates your `.agent/brain/` directory with:
- `task.md` — What to do right now
- `walkthrough.md` — Session history and Mental Anchors
- `implementation_plan.md` — Project roadmap

### Step 3 — Fill in Your Project Identity Card ⚠️ CRITICAL
This is the most important step. Open and fill in every `[PLACEHOLDER]`:

```bash
# Open and edit with your project-specific details
nano docs/AI-COGNITIVE-TWIN-PROTOCOL.md
```

Fill in:
- `[YOUR_PROJECT_NAME]` — e.g., `my-kafka-pipeline`
- `[T1]` Command Centre path on your Windows/Mac
- `[T2]` Dev Bridge path (WSL2/VM)
- `[T3/T4]` Production host, user, UID, path
- Security doctrine — who runs as root vs. which UID for apps
- Mental Anchor §8 — set to `"Fresh project. Phase 1 pending."`

> ⚠️ **The AI will NOT operate properly until this file is filled in.** `audit-pre-flight.sh` checks for unfilled placeholders and will warn you.

### Step 4 — Set Up Ansible Baseline (Infrastructure Projects)
```bash
# Follow the full LDP guide
cat docs/HOWTO-SETUP-ANSIBLE-BASELINE.md

# Verify connectivity to your nodes
ansible all -m ping -i inventory/hosts.yml
```

### Step 5 — Run the Pre-Flight Audit
```bash
# Linux / WSL2
./tools/audit-pre-flight.sh

# Windows (PowerShell)
.\tools\audit-pre-flight.ps1
```

**Everything should show `[PASS]` or `[OK]`.** Fix any `[FAIL]` before continuing.

### Step 6 — Brief Your AI (The Cognitive Handshake)
Generate the context manifest and upload it to your AI:

```bash
# Linux / WSL2
bash tools/reanimate.sh

# Windows (PowerShell)
.\tools\reanimate.ps1
```

Then upload the generated `sod_manifest_YYYY-MM-DD.txt` to your AI and say:

> *"Initialise DSOM Protocol. Read the uploaded manifest. Summarise the current Mental Anchor and confirm the 4-Tier environment map from the AI-COGNITIVE-TWIN-PROTOCOL.md section. State: 'Sovereign State Synchronised' when ready."*

**Your AI is now operational as a Cognitive Digital Twin.**

---

## 🏛️ The Sovereign Markdown Palace (v10.0.0-palace)

> **New in v10.0:** The DSOM brain has evolved from a flat file system to a **spatial memory architecture** — the Sovereign Markdown Palace.

### What Is the Palace?

The Palace gives your AI **organised, fast, spatial recall** across months of project history — without reading entire session logs. It works as a second layer alongside the existing `walkthrough.md` (The Drawer).

```
.agent/brain/
├── palace_registry.md        ← AI reads this at SOD (spatial map)
├── walkthrough.md            ← Linear session log (The Drawer)
└── wings/                    ← Spatial Palace Rooms
    └── wing_dsom_core/
        ├── hall_facts/       ← Immutable laws, tools, architecture
        └── hall_events/      ← Milestones, versions, history
```

Each Room has a `closet.md` — a distilled, high-density knowledge summary the AI reads **instead of** scanning hundreds of lines.

### Palace Quick Start

| If you are... | Go to... |
|---|---|
| **First-time user or AI agent** | [`docs/HOWTO-PALACE-ONBOARDING.md`](docs/HOWTO-PALACE-ONBOARDING.md) |
| **Existing DSOM user upgrading** | [`docs/HOWTO-MIGRATE-TO-PALACE.md`](docs/HOWTO-MIGRATE-TO-PALACE.md) |
| **Reading how the Palace was built** | [`docs/PALACE-BUILD-STORY.md`](docs/PALACE-BUILD-STORY.md) |
| **Full Palace specification** | [`docs/DIGITAL-SOVEREIGNTY-OPERATIONAL-MODEL-PALACE.md`](docs/DIGITAL-SOVEREIGNTY-OPERATIONAL-MODEL-PALACE.md) |

### 🧩 Known Gap: The Reasoning Problem

> **Research Finding (2026-04-08):** DSOM solves *state persistence* and *cost efficiency* — but there is one gap: **live reasoning capture**.

Six months of daily AI use = ~19.5 million tokens. Every decision, every debugging session, every tradeoff debate. Gone when the session ends.

| Approach | Tokens/Session | Annual Cost |
|---|---|---|
| Paste everything | 19.5M — impossible | — |
| LLM summaries | ~650K | ~$507/yr |
| MemPalace (external) | ~170 tokens | ~$0.70/yr |
| **DSOM Palace (ours)** | **~1,500–3,000 tokens** | **~$1–3/yr** |

✅ DSOM matches MemPalace on cost and efficiency.
⚠️ **The gap:** DSOM does not automatically capture *why* decisions were made — only *what* was decided. The reasoning lives in the chat window, not in Git.

**The fix (Decision Log Protocol):** At key decisions, immediately ask the AI:
```
"Log this decision to walkthrough.md:
 Decision: [what] | Alternatives rejected: [what and why] | Reason: [why this]"
```

📖 **Full analysis:** [`docs/RESEARCH-REASONING-GAP.md`](docs/RESEARCH-REASONING-GAP.md)

---

## 📅 Daily Operating Rituals

> **Full ritual guides:** [`docs/SOD-RITUAL.md`](docs/SOD-RITUAL.md) | [`docs/EOD-RITUAL.md`](docs/EOD-RITUAL.md)

---

### 🌅 Start of Day (SOD) — 5 Steps

**Step 1 — Git Sync** *(Pull latest state)*
```powershell
.\tools\git-ritual.ps1 sod        # Windows (T1)
```
```bash
./tools/git-ritual.sh sod         # WSL2 (T2)
```

**Step 2 — Intelligence Audit** *(Verify workspace is healthy)*
```powershell
.\tools\audit-pre-flight.ps1      # Windows
```
```bash
./tools/audit-pre-flight.sh       # WSL2
```
All steps must show `[PASS]`. Fix any `[FAIL]` before continuing.

**Step 3 — Generate Reanimation Manifest**
```bash
bash tools/reanimate.sh           # WSL2
```
Optional — scan before sharing:
```bash
./tools/privacy-guardian.sh
```

**Step 4 — Brief Your AI (The Cognitive Handshake)**

*Option A — Upload manifest to AI chat, then say:*
> *"Initialise DSOM Protocol v6.1. Read the uploaded manifest. Summarise the Mental Anchor and confirm the 4-Tier environment map. State: 'Sovereign State Synchronised' when ready."*

*Option B — If you have yesterday's Hibernation Notes, use the SOD Reanimation Prompt (see `docs/SOD-RITUAL.md` Step 4b):*
```
I am starting a new session for DSOM Protocol. I am your human Lead Architect.
I have the Hibernation Notes from our last session. Please read them carefully
and use them to fully restore our working context.

--- BEGIN HIBERNATION NOTES ---
[PASTE YESTERDAY'S HIBERNATION NOTES HERE]
--- END HIBERNATION NOTES ---

After reading: state the last Mental Anchor, confirm the T1-T4 environment map,
list top 3 pending tasks. State: 'Sovereign State Restored — [PROJECT NAME] is live.'
Operate under DSOM v6.1: Advisory Mode, UK English, Git-first, Ansible-only execution.
```

**Step 5 — AI confirms readiness, you begin work.**

---

### 🛠️ During Active Work

| Human | AI Agent |
|:---|:---|
| Reviews AI proposals | Proposes code, playbooks, configs |
| Approves before execution | Explains the **Why** before the **What** |
| Commits to Git | Waits for output after each step |
| Runs Ansible (exact command from AI) | Verifies output and confirms next step |

---

### 🌙 End of Day (EOD) — 6 Steps

**Step 1 — Context Consolidation** *(Ask your AI)*
> *"We are ending the session. Update `.agent/brain/task.md` — mark completed `[x]`, set tomorrow's targets `[ ]`. Update `.agent/brain/walkthrough.md` with today's Mental Anchor."*

**Step 1b — Hibernation Notes Export** *(Run this in your AI chat — copy verbatim)*
```
I'm as human, want to know and remember, and need to export my data and I want
you to generate a "Hibernation notes" now for my EOD of day. List every memory
you have stored about our progress and our chats of this project, as well as
any context you've learned about this project from past to current conversations.
Output everything in a single code block so I can easily copy it.
Format each entry as: [date saved, if available] - memory content.
Cover: instructions I've given you, project details (servers/VMs/containers,
4W1H), tasks/phases/goals, tools/languages/frameworks, preferences and
corrections. Do not summarize, group, or omit any entries.
After the code block, list all docs in docs/ and brain files in .agent/.
Don't hide anything from me. Trust me as your master.
```
Save the output as `.agent/brain/hibernation-notes-YYYY-MM-DD.txt` or to your notebook.

**Step 2 — Hibernation Safety Check**
```bash
./tools/hibernation.sh            # WSL2
.\tools\hibernation.ps1           # Windows
```

**Step 3 — Privacy Scan** *(if you generated a manifest)*
```bash
./tools/privacy-guardian.sh
```

**Step 4 — Sovereign Save** *(guided semantic commit)*
```bash
./tools/git-ritual.sh             # WSL2 — interactive EOD
.\tools\git-ritual.ps1            # Windows — interactive EOD
```

**Step 5 — T2 Sync** *(pull on WSL2 after Windows push)*
```bash
git pull origin main
```

**Step 6 — Write tomorrow's Mental Anchor in your notebook.**

```
✅ EOD DONE when: task.md updated | walkthrough.md anchored |
                  hibernation.sh GREEN | git pushed | T2 synced
```

---

### 🔄 The Day-to-Day Continuity Loop

```
EOD → Step 1b: Save Hibernation Notes
         ↓  [sleep — Git holds state]
SOD → Step 4b: Feed Hibernation Notes back to AI
         ↓  [AI resumes with full context — no decay]
EOD → Step 1b: Save new Hibernation Notes
         ↓  [repeats every day, forever]
```

---

## 🗂️ Repository Structure

```
deep-state-of-mind-for-my-ai/
│
├── docs/                                  # Governance & Protocol Documents
│   ├── AI-MASTER-PROTOCOL.md              # The Sovereign Constitution (v6.1 + Palace v1.0)
│   ├── AI-COGNITIVE-TWIN-PROTOCOL.md      # ⭐ Project Identity Card Template
│   ├── GITOPS-AIOPS-ANSIBLE-STRATEGY.md   # Three-Pillar Doctrine
│   ├── HOWTO-SETUP-ANSIBLE-BASELINE.md    # Ansible setup guide (LDP standard)
│   ├── OPERATIONAL-GUIDE.md               # How-to for daily rituals
│   ├── REANIMATION-PROMPT-TEMPLATE.md     # AI session prompt templates
│   └── ...
│
├── .agent/brain/                          # 🧠 The AI's External Memory (SSoT)
│   ├── task.md                            # Present: What to do NOW
│   ├── walkthrough.md                     # Past: Session history & Mental Anchors
│   ├── implementation_plan.md             # Future: Project roadmap
│   ├── palace_registry.md                 # 🏛️ Palace spatial index (AI reads at SOD)
│   └── wings/                             # 🏛️ Sovereign Markdown Palace Rooms
│       └── wing_dsom_core/
│           ├── hall_facts/                # Laws, tools, architecture
│           └── hall_events/              # Milestones, versions, ledger
│
├── tools/                                 # Automation Scripts
│   ├── audit-pre-flight.sh / .ps1         # ✅ Run first every session
│   ├── git-ritual.sh / .ps1               # 🔄 SOD pull + EOD commit/push
│   ├── reanimate.sh / .ps1                # 🚀 Generate AI context manifest (v2.2/v2.1)
│   ├── hibernation.sh / .ps1              # 🌙 EOD safety check + Palace Sync (v2.1)
│   ├── palace-sync.sh / .ps1             # 🏛️ Map git commits → Palace Rooms (v1.0)
│   ├── init-brain.sh / .ps1               # 🧠 One-time brain initialisation
│   └── privacy-guardian.sh / .ps1         # 🛡️ Scan manifest before sharing
│
├── inventory/                             # Ansible Node Topology (your project)
│   ├── hosts.yml                          # Target nodes (fill in after adoption)
│   └── group_vars/
│
├── playbooks/                             # Ansible Playbooks (your project)
└── roles/                                 # Ansible Roles (your project)
```

**The `⭐ AI-COGNITIVE-TWIN-PROTOCOL.md` is the most important file.** Without it filled in, the AI has no project context.

---

## 🧠 The AI Brain — Understanding the Four Artifacts

| Artifact | Time | Purpose | Who Updates |
|:---|:---|:---|:---|
| `AI-MASTER-PROTOCOL.md` | **Eternal** | Governance laws, hard rules, identity | Human (rarely changes) |
| `implementation_plan.md` | **Future** | Project phases and roadmap | Human-led, AI assists |
| `task.md` | **Present** | Today's checklist and focus | AI updates, Human approves |
| `walkthrough.md` | **Past** | Session history, Mental Anchors, decisions | AI writes, Human audits |

> **The Mental Anchor** is the most critical entry in `walkthrough.md`. It is the exact logical stopping point of the last session — the sentence that allows a **brand new AI session** to resume exactly where you left off, in under 3 prompts.

---

## 🔀 Session Handover (Moving to a New AI)

When switching AI models, chat windows, or accounts, use the **Sovereign Handover Prompt** to export all context:

Copy from [`docs/REANIMATION-PROMPT-TEMPLATE.md`](docs/REANIMATION-PROMPT-TEMPLATE.md) → **Prompt Variant 2: Session Handover**.

Paste it into the **old** AI session first to get a full memory dump, then load the dump into the **new** AI session along with your manifest.

---

## 🛠️ Tools Reference

| Script | When to Run | What It Does |
|:---|:---|:---|
| `audit-pre-flight.sh` | **Every session start** | Checks Brain, Git sync, Cognitive Twin Protocol, Ansible baseline |
| `git-ritual.sh sod` | **Morning** | Pulls latest state from `origin/main` |
| `reanimate.sh` | **Before AI session** | Generates the full context manifest for AI upload |
| `privacy-guardian.sh` | **Before sharing manifest** | Scans for leaked IPs, keys, tokens, paths |
| `git-ritual.sh` | **Evening** | Guided semantic commit + push (EOD Sovereign Save) |
| `hibernation.sh` | **Session end** | Verifies walkthrough + task updated, then pushes |
| `template-reset.sh` | **Once (new project)** | Clears Git history and brain for fresh project |

**Windows users:** All `.sh` scripts have a `.ps1` PowerShell equivalent.

---

## 📋 The 6-Step Boot Checklist (New Project)

```
[ ] 1. Clone and run template-reset.sh
[ ] 2. Run init-brain.sh
[ ] 3. Fill in docs/AI-COGNITIVE-TWIN-PROTOCOL.md (ALL [PLACEHOLDER] fields)
[ ] 4. Run HOWTO-SETUP-ANSIBLE-BASELINE.md (infra projects)
[ ] 5. Run audit-pre-flight.sh — confirm all PASS
[ ] 6. Run reanimate.sh — upload manifest to AI — get Handshake
```

Once Step 6 is complete, the AI knows:
- ✅ Your 4-Tier environment (T1 → T4)
- ✅ Your security doctrine (who runs as root, who runs as UID X)
- ✅ Your Git commit convention
- ✅ Your production identity and isolation rules
- ✅ The current Mental Anchor (last known state)
- ✅ All governance laws and hard rules

---

## 📚 Key Documents

| Document | Purpose |
|:---|:---|
| [`docs/AI-MASTER-PROTOCOL.md`](docs/AI-MASTER-PROTOCOL.md) | The Sovereign Constitution — AI governance laws |
| [`docs/AI-COGNITIVE-TWIN-PROTOCOL.md`](docs/AI-COGNITIVE-TWIN-PROTOCOL.md) | ⭐ **Fill this in first** — Project Identity Card |
| [`docs/DIGITAL-SOVEREIGNTY-OPERATIONAL-MODEL-PALACE.md`](docs/DIGITAL-SOVEREIGNTY-OPERATIONAL-MODEL-PALACE.md) | 🏛️ Full Sovereign Markdown Palace specification |
| [`docs/HOWTO-PALACE-ONBOARDING.md`](docs/HOWTO-PALACE-ONBOARDING.md) | 🏛️ First-time guide for users and AI agents |
| [`docs/HOWTO-MIGRATE-TO-PALACE.md`](docs/HOWTO-MIGRATE-TO-PALACE.md) | 🔄 Upgrade guide — existing DSOM → Palace v1.0 |
| [`docs/PALACE-BUILD-STORY.md`](docs/PALACE-BUILD-STORY.md) | 📖 How and why the Palace was built |
| [`docs/SOD-RITUAL.md`](docs/SOD-RITUAL.md) | 🌅 Full Start-of-Day ritual guide |
| [`docs/EOD-RITUAL.md`](docs/EOD-RITUAL.md) | 🌙 Full End-of-Day ritual guide |
| [`docs/HUMAN-HANDOVER-CONTEXT.md`](docs/HUMAN-HANDOVER-CONTEXT.md) | 🤝 Session handover prompt |
| [`docs/GITOPS-AIOPS-ANSIBLE-STRATEGY.md`](docs/GITOPS-AIOPS-ANSIBLE-STRATEGY.md) | Three-pillar strategic doctrine |
| [`docs/HOWTO-SETUP-ANSIBLE-BASELINE.md`](docs/HOWTO-SETUP-ANSIBLE-BASELINE.md) | Step-by-step Ansible baseline setup |
| [`docs/REANIMATION-PROMPT-TEMPLATE.md`](docs/REANIMATION-PROMPT-TEMPLATE.md) | AI session prompt templates |

---

## 🤖 Supported AI Providers

This framework is provider-agnostic. Tested and configured for:

| AI | Setup Guide |
|:---|:---|
| Google Gemini | [`docs/PERSONALIZATION.md`](docs/PERSONALIZATION.md) |
| Anthropic Claude | [`docs/CLAUDE-SETUP.md`](docs/CLAUDE-SETUP.md) |
| GitHub Copilot | [`docs/COPILOT-SETUP.md`](docs/COPILOT-SETUP.md) |
| Google Antigravity | Direct — uses this repo as workspace |

---

## 🗺️ Roadmap

- [x] **v4.1** — Brain artifacts and Root-Aware scripts
- [x] **v5.2** — ITIL 4 alignment, Privacy Guardian, Multi-agent protocols
- [x] **v6.0** — GitOps + AIOps + Ansible three-pillar model, Cognitive Twin Protocol template, Git Ritual tool
- [x] **v6.1** — Ansible baseline playbooks, human handover, Google Antigravity integration
- [x] **v6.2** — Ansible `roles/common`, 19-node Elastic fabric hardened (v9.8.0)
- [x] **v10.0.0-palace** — 🏛️ Sovereign Markdown Palace v1.0: spatial memory, `palace-sync`, 8 Rooms backfilled
- [ ] **v7.0** — Local LLM support (Ollama) for offline Sovereign AI

---

## 🤝 Contributing

All contributions must follow the DSOM standards:
- Atomic commits: `type(scope): description [Phase/vX.X]`
- All PRs must include a `walkthrough.md` update
- UK English only in all documentation
- No secrets in any committed file

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for full guidelines.

---

## 👤 Authors

- **Lead Architect:** [Harisfazillah Jamel](https://github.com/linuxmalaysia) — 35+ years ICT & Open Source Leadership
- **AI Partners:** Google Gemini, Google Antigravity, Anthropic Claude
- **Framework:** Built for the LinuxMalaysia Open Source Community

---

## 📄 License

Licensed under **GNU General Public License v3.0**. See [`LICENSE`](LICENSE) for details.

**At Your Own Risk:** Shared for educational purposes. The author is not liable for data loss or AI hallucinations. Validate your own Cognitive Twins.

---

*Deep State of Mind (DSOM) For My AI Protocol | v10.0.0-palace | 2026-04-08*
*Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai)*
