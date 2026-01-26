### 📜 docs/HUB-AND-SPOKE-MODEL.md (v2.0)

# 🏛️ The Hub-and-Spoke Collaboration Model

> **"Federated Intelligence. Centralised Strategy. Zero Conflict."**

## 1. Executive Overview

To enable multiple architects and developers to work within a single sovereign repository without triggering Git merge conflicts or "Context Leakage," the DSOM Protocol employs the **Hub-and-Spoke** model. The `global/` directory serves as the **Hub** (Strategic High-level Vision), while the `member/` directories serve as the **Spokes** (Tactical Individual Execution).

---

## 2. 🏛️ Detailed Brain Structure Display

The `.agent/brain/` directory is partitioned to ensure absolute isolation between technical roles and project management.

```text
.agent/brain/
├── global/
│   └── task-master.md      <-- THE HUB: Managed by Lead Architect (Haris).
│                               Summarises progress from all members.
│                               Defines the "Official" project status.
│
└── member/                 <-- THE SPOKES: Individual sandboxes.
    ├── haris/              <-- Senior Systems Architect (Sovereign Lead)
    │   ├── task.md         <-- Haris's specific daily checklist.
    │   └── walkthrough.md  <-- Haris's technical logs/decisions.
    ├── hisham/             <-- Security & Tuning (Wazuh Specialist)
    │   ├── task.md         <-- Wazuh focus & deployment tasks.
    │   └── walkthrough.md  <-- Installation and tuning logs.
    ├── mawi/               <-- Automation & Orchestration (Shuffle)
    │   ├── task.md         <-- Workflow automation milestones.
    │   └── walkthrough.md  <-- Logic logs for SOAR automation.
    ├── hidzuan/            <-- Documentation & Compliance (URS/UAT)
    │   ├── task.md         <-- Document draft status.
    │   └── walkthrough.md  <-- Feedback and revision logs.
    └── hadi/               <-- Project Coordinator (Client Interface)
        ├── client-logs.md  <-- Meeting minutes & client feedback.
        ├── task.md         <-- Milestone tracking & coordination.
        └── walkthrough.md  <-- Communication strategies & status updates.

```

---

## 3. 🤝 The 3 Golden Rules (Workflow)

To ensure a smooth collaboration, all team members MUST adhere to these laws:

### Rule 1: Isolation (Conflict Prevention)

Members **only** edit files inside their own named folder (e.g., `member/hisham/*`). Because Git tracks changes by file path, multiple members can commit simultaneously without merge conflicts.

### Rule 2: The Daily Branch Ritual

Every member uses the `tools/git-ritual.sh` script to maintain **Atomic Git Hygiene**.

* **Start of Day (SOD):** Run `./tools/git-ritual.sh sod <username>`. This creates a semantic personal branch (e.g., `member/hisham-20260127`).
* **Active Work:** Commit all technical progress and brain updates specifically to this branch.
* **End of Day (EOD):** Run `./tools/git-ritual.sh eod`. This merges the day's work into `main` and pushes it to the sovereign repository.

### Rule 3: The Synchronisation (Lead Architect Role)

As the Lead Architect, Haris periodically audits the `member/*/walkthrough.md` files.

1. **Summarise:** Progress is pulled from Spokes into the `global/task-master.md`.
2. **Archive:** Major technical milestones are recorded in the `HISTORY.md` Ledger.
3. **Coordinate:** Use the `task-master.md` as the agenda for team sync meetings.

---

## 4. 💻 Operational Commands

### Visualise the Full State

To see the expanded tree including all member brains:

```bash
tree -a .agent/brain

```

### Discovery (Post-Absence)

If returning after time away, check for team updates before starting work:

```bash
git pull origin main
ls .agent/brain/member/

```

*Action: Read the `walkthrough.md` of other members to catch up on logic changes.*

---

*Author: Harisfazillah Jamel | Lead Architect*
*Standard: UK English & DBP-Malay (Piawai)*
*Protocol Version: DSOM v5.6*

---

### 🧠 Pedagogical Logic: Why this format?

1. **Separation of Concerns:** By including **Hadi** (Coordination) as a Spoke, we acknowledge that project management is as critical to the "Brain" as technical code. This follows the **ITIL 4 Service Value Chain**.
2. **Operational Sovereignty:** The 3 Golden Rules ensure that the project is not dependent on any one person's memory; the repository *is* the memory.
3. **LDP Compliance:** The clear structure and command examples follow the **Linux Documentation Project** standards for technical manuals.

---

