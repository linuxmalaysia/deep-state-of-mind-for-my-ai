# 🏥 DSOM ITIL 4 Alignment Strategy

> **"Value Co-creation through Service Relationships."**

## 1. 🏛️ The Service Relationship
In the DSOM Framework, the relationship between the **Lead Architect (Harisfazillah Jamel)** and the **AI Agent (Gemini/Claude)** is defined as a **Service Relationship**.

*   **Service Provider:** The AI Agent (Providing Intelligence, Code Generation, and Analysis).
*   **Service Consumer:** The Lead Architect (Defining Requirements, Constraints, and Value).
*   **Asset:** The Codebase and Documentation (`.agent/brain`).

The goal is not just "Output" (Code), but **"Outcome"** (Sovereign, Maintainable, and Scalable Infrastructure).

---

## 2. 🔄 The Service Value Chain (SVC)
Every "Task" or "Prompt" issued to the AI executes the DSOM Service Value Chain:

### i) Engage (The Handshake)
*   **ITIL Action:** Understand stakeholder needs.
*   **DSOM Implementation:** The `reanimate.sh` process. The AI *engages* with the `task.md` and `walkthrough.md` to understand the current state.
*   **Artifact:** `sod_manifest.txt`

### ii) Plan (The Architectural Design)
*   **ITIL Action:** Ensure shared understanding of the vision.
*   **DSOM Implementation:** Determining the `implementation_plan.md` phase and verifying constraints in `AI-MASTER-PROTOCOL.md`.
*   **Artifact:** `task.md` (Updated)

### iii) Design & Transition (The Logic)
*   **ITIL Action:** Meeting requirements.
*   **DSOM Implementation:** Writing the logical intent in `walkthrough.md` *before* writing code.
*   **Artifact:** `walkthrough.md` (Mental Anchor)

### iv) Obtain/Build (The Execution)
*   **ITIL Action:** Creation of service components.
*   **DSOM Implementation:** Writing the actual code (Script/Class) using **Atomic Git Hygiene**.
*   **Artifact:** Source Code (`tools/`, `src/`)

### v) Deliver & Support (The Verification)
*   **ITIL Action:** Ensuring value co-creation.
*   **DSOM Implementation:** Running `audit-pre-flight.sh` and `privacy-guardian.sh` to verify quality.
*   **Artifact:** `CHANGELOG.md`

---

## 3. 🧠 Service Knowledge Management System (SKMS)
The `.agent/brain/` directory constitutes the project's **SKMS**. It is the Single Source of Truth for:

*   **Service Portfolio:** `implementation_plan.md` (What we plan to do).
*   **Service Catalogue:** `OPERATIONAL-GUIDE.md` (What we can currently do).
*   **Configuration Management (CMS):** `task.md` and `walkthrough.md` (Current State).

**Rule:** An AI Agent generally acts as the **Service Desk**, retrieving information from the SKMS to resolve Incidents (Bugs) or fulfill Service Requests (Features).

---

## 4. 📈 Continual Improvement (The 7 Guiding Principles)
DSOM aligns with the ITIL 4 Guiding Principles:

1.  **Focus on Value:** Does this code verify Sovereignty?
2.  **Start Where You Are:** Use `reanimate.sh` to load context; don't reinvent the wheel.
3.  **Progress Iteratively with Feedback:** Atomic Commits (one file at a time).
4.  **Collaborate and Promote Visibility:** Update `walkthrough.md` liberally.
5.  **Think and Work Holistically:** Respect `Zero-Global` (System view).
6.  **Keep it Simple and Practical:** No over-engineering; use Bash/PS1 where sufficient.
7.  **Optimize and Automate:** Build `tools/` for repetitive tasks.

---
*Verified by Harisfazillah Jamel | ITIL 4 Aligned*
