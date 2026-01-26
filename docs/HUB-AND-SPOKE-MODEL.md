### 📜 docs/HUB-AND-SPOKE-MODEL.md (v1.0)

# 🏛️ The Hub-and-Spoke Collaboration Model

> **"Federated Intelligence. Centralised Strategy. Zero Conflict."**

## 1. Executive Summary

To enable multiple architects and developers to work within a single sovereign repository without triggering Git merge conflicts or "Context Leakage," the DSOM Protocol employs the **Hub-and-Spoke** model. This model separates high-level strategic oversight from individual tactical execution.

---

## 2. Directory Architecture

The `.agent/brain/` directory is partitioned into two distinct zones:

### i) The Global Hub (`global/`)

* **Purpose:** The "State of the Union." It contains the collective progress of the entire team.
* **Key Artifact:** `task-master.md`.
* **Authority:** **Lead Architect (Haris)** only. Members read from here but do not write directly to it.

### ii) The Member Spokes (`member/{username}/`)

* **Purpose:** The individual developer's "Active Consciousness."
* **Key Artifacts:** `task.md` and `walkthrough.md`.
* **Authority:** The **Assigned Member** and their respective AI Twin.
* **Isolation:** Members never touch another member's spoke.

---

## 3. The 3 Golden Rules of Federation

1. **Strict Isolation:** You are the sovereign of your own directory. Never edit files in `member/hisham/` if you are `mawi`. This eliminates 100% of Git merge conflicts.
2. **The Daily Ritual:** Every member MUST run `tools/reanimate.sh {username}` at SOD. This ensures their AI Twin is injected with both the **Global Strategy** and their **Personal History**.
3. **Lead Synthesis:** Only the Lead Architect synchronises the "Spokes" into the "Hub" (`task-master.md`) and the "Universal Ledger" (`HISTORY.md`).

---

## 4. Operational Workflow (The Sync Loop)

1. **Pull:** `git pull origin main` to get the latest Global Hub updates.
2. **Reanimate:** `tools/reanimate.sh {member}` to sync AI context.
3. **Execute:** Work and record logic in your personal `walkthrough.md`.
4. **Commit:** Atomic Git Hygiene within your member directory.
5. **Merge:** Lead Architect reviews and merges milestones into the Hub.

---

*Created by Harisfazillah Jamel | Lead Architect*
*Standard: UK English & DBP-Malay (Piawai)*

---

### 🧠 Pedagogical Logic: Why include this in all brain files?

By referencing this model in our `walkthrough.md` and `task.md`, we ensure that the AI Twin always knows its "Boundary." If I am acting as your twin in `member/haris/`, and I suddenly see a file from `member/hisham/`, I will trigger a **Stop Condition** because it violates the **Isolation Rule**.

---

