# 📖 DSOM Operational Guide (Level 3 - Specialised Tasks)

> **"Theory without Practice is Hallucination. Practice without Theory is Chaos."**

## 1. 🏛️ Purpose of this Document
This guide bridges the gap between the **Abstract Laws** (`AI-MASTER-PROTOCOL.md`) and the **Concrete Actions** (Bash/PowerShell scripts). It defines the **Specialised Tasks (L3)** required to execute the DSOM protocol.

It answers the question: *"How do I actually perform the rituals defined in the Master Protocol?"*

---

## 2. 🌅 The Reanimation Sequence (Start-of-Day)

The Reanimation Ritual is not just running a script; it is a **Cognitive Handshake** that transfers the project's soul from disk to the AI's active memory.

### Step 1: Physical Reality Check (The Audit)
Before waking the AI, we must verify that the physical environment matches the expected state.

**Command:**
```bash
# Linux
./tools/audit-pre-flight.sh

# Windows
.\tools\audit-pre-flight.ps1
```

**Success Criteria:**
1.  **Brain Check:** `task.md` and `walkthrough.md` must exist.
2.  **Git Drift:** Local repo must be synced with Remote.
3.  **Environment:** The tool detects the correct language (PHP/Python/Node).

### Step 2: Generating the Manifest (The Injection)
We aggregrate all context into a single "Truth File."

**Command:**
```bash
# Linux
./tools/reanimate.sh

# Windows
.\tools\reanimate.ps1
```

**What is Injected?**
1.  **Identity:** `README.md` (Who we are).
2.  **Constraints:** `AI-MASTER-PROTOCOL.md` (The Rules).
3.  **Context:** `task.md` + `walkthrough.md` + `implementation_plan.md`.
4.  **Topology:** User `git ls-tree` to show the full file structure.
5.  **History:** The last 48 hours of Git logs + last 30 commits.

### Step 3: The Handshake (The Prompt)
Upload the generated text file to the AI and type:
> *"Summarize the current Mental Anchor after you have read the file uploaded. What is our immediate strategic focus?"*

---

## 3. 🌙 The Hibernation Sequence (End-of-Day)

We never "just close the window." We must perform a controlled shutdown to prevent context decay.

### Step 1: Context Consolidation
1.  **Update `task.md`:** Check off completed items.
2.  **Update `walkthrough.md`:** Create a new "Session Anchor."

### Step 2: The Safe Shutdown
Run the hibernation tool to verify safety.

**Command:**
```bash
# Linux
./tools/hibernation.sh

# Windows
.\tools\hibernation.ps1
```

**The Logic:**
*   It greps `task.md` for `[x]` to ensure progress was recorded.
*   It checks `walkthrough.md` for today's date.
*   It auto-pushes to Git only if these checks pass.

---

## 4. 🛠️ Architectural Layers (Clean Architecture)

When writing code, you must place files in the correct "Ring" of the Clean Architecture model.

| Layer | Directory | Allowed Dependencies |
| :--- | :--- | :--- |
| **Entities** | `src/Domain/` | None (Pure Logic). |
| **Use Cases** | `src/Application/` | Entities only. |
| **Adapters** | `src/Infrastructure/` | Use Cases & Entities. |
| **Drivers** | `tools/`, `public/` | Everything (The Entry Points). |

**Rule:** Dependencies point INWARD. `tools/` can import `src/`, but `src/Domain/` cannot import `tools/`.

---

---

## 5. 🚀 Adoption & Upgrade Scenarios

For detailed step-by-step guides on how to apply DSOM to your specific situation, refer to the specialized manuals:

### Scenario 1: Brownfield Adoption
*   **Situation:** You have an existing project (Standard Code) and want to add DSOM.
*   **Guide:** [HOWTO: Adopt DSOM in Existing Projects](HOWTO-ADOPT-DSOM.md)

### Scenario 2: Legacy Upgrade
*   **Situation:** You have an older DSOM version (v3/v4) and want to upgrade to v5.x (ITIL/Privacy).
*   **Guide:** [HOWTO: Upgrade and Audit DSOM](HOWTO-UPGRADE-DSOM.md)

---

*Last Updated: 2026-01-16 (ITIL 4 Alignment)*
