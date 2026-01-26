### 📜 docs/HUB-AND-SPOKE-MODEL.md (v1.2)

# 🏛️ The Hub-and-Spoke Collaboration Model

> **"Federated Intelligence. Centralised Strategy. Zero Conflict."**

## 1. Executive Summary

To enable multiple architects and developers to work within a single sovereign repository without triggering Git merge conflicts or "Context Leakage," the DSOM Protocol employs the **Hub-and-Spoke** model. The `global/` directory is the Hub (High-level vision), and the `member/` directories are the Spokes (Individual execution).

---

## 2. 🏛️ Detailed Brain Structure Display

```text
.agent/brain/
├── global/
│   └── task-master.md      <-- THE HUB: Managed by Lead Architect (Haris).
│                               Summarizes progress from all members.
│                               Defines the "Official" project status.
│
└── member/                 <-- THE SPOKES: Individual sandboxes.
    ├── haris/
    │   ├── task.md         <-- Haris's specific daily checklist.
    │   └── walkthrough.md  <-- Haris's technical logs/decisions.
    ├── hisham/
    │   ├── task.md         <-- Hisham's focus (Wazuh/Tuning).
    │   └── walkthrough.md  <-- Hisham's installation logs.
    ├── mawi/
    │   ├── task.md         <-- Mawi's focus (Shuffle/Automation).
    │   └── walkthrough.md  <-- Mawi's workflow logs.
    └── hidzuan/
        ├── task.md         <-- Hidzuan's focus (URS/UAT Docs).
        └── walkthrough.md  <-- Documentation draft progress.

```

---

## 3. 🤝 The 3 Golden Rules (Workflow)

### Rule 1: Isolation (Avoid Conflicts)

Members **only** edit files inside their own named folder (e.g., `member/hisham/*`). Since Git tracks changes by file, Hisham can update his logs at the same time Mawi updates his, and they will **never** have a merge conflict because they are touching different files.

### Rule 2: The Daily Branch Ritual

Everyone uses the `tools/git-ritual.sh` script to maintain **Atomic Git Hygiene**.

* **Start of Day (SOD):** Run `./tools/git-ritual.sh sod <username>`. This creates a personal branch (e.g., `member/hisham-20260123`).
* **Work:** Commit technical progress and brain updates specifically to this branch.
* **End of Day (EOD):** Run `./tools/git-ritual.sh eod`. This merges work into `main` and pushes to the sovereign repository.

### Rule 3: The Synchronization (Lead Architect Role)

As the Lead Architect, you periodically read the `member/*/walkthrough.md` files after they merge. You then:

1. **Summarise** progress into the `global/task-master.md`.
2. **Archive** major milestones into `HISTORY.md`.
3. **Update** the team using `task-master.md` as the agenda for sync meetings.

---

## 4. 💻 Visualization & Discovery

To see the full expanded tree including all member brains:

```bash
tree -a .agent/brain

```

If returning after an absence, check for member commits:

```bash
git pull origin main
ls .agent/brain/member/

```

---

*Created by Harisfazillah Jamel | Lead Architect*
*Standard: DSOM Protocol v5.6*

---

### 🧠 Pedagogical Logic: Why this format?

1. **Visual Grounding:** Including the `tree` structure directly in the documentation provides an immediate "Mental Map" for new members like Mr Hisham or Mr Mawi, reducing onboarding time.
2. **Ritual Enforcement:** By codifying the `git-ritual.sh` commands, we ensure that everyone follows the same **Operational Sovereignty** standards, preventing "Repo Drift."
3. **Governance Transparency:** Defining your role as the "Synchronizer" makes it clear that while execution is distributed, the **Sovereign Source of Truth** remains centralised and audited.

---

