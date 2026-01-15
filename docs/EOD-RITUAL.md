# 🌙 The End-of-Day (EOD) Ritual: Sovereign Hibernation

> **"Rest is not the end unless the memory is lost. To hibernate is to prepare for rebirth."**

## 1. 🏛️ The Philosophy of Hibernation
The **End-of-Day (EOD)** is the critical "Save Game" point for the project. The Human Architect is tired, cognitive load is dropping, and the risk of "lazy commits" is high.

The EOD Ritual exists to **safeguard the Deep State of Mind**. It ensures that even if the Human sleeps for a week, the next reanimation will be perfectly context-aweare. It is about **closing the loop**.

## 2. 🔄 The Workflow (How to do it)

### Step 1: The Context Consolidation (AI & Human)
Before running the tools, the Human asks the AI to help finalize the artifacts.
*   **Update Task List:** Mark completed items. Move "In Progress" items to "Next Session".
*   **Update Walkthrough:** Create a "Session Anchor" summarizing *what* was done and *why*.
*   **Update Plan:** Adjust the roadmap if reality shifted today.

### Step 2: The Hibernation Sequence (System)
The script automates the safety checks for a tired human.
*   **Command:** `bash tools/hibernation.sh` (or `.\tools\hibernation.ps1` on Windows).
*   **What it Checks:**
    1.  **Dirty Artifacts:** Are `task.md` and `walkthrough.md` updated?
    2.  **Uncommitted Code:** Are there dangling changes?
    3.  **Next Steps:** It vividly displays *exactly* what is left for tomorrow.

### Step 3: The Final Push (Human)
*   The script will prompt for a final "Hibernation Commit".
*   This commit is special: it signals a clean break.
*   The Architect pushes to GitHub, verifying the "Green Light" of safety.

## 3. 🧠 What the AI Must Display
The Hibernation Tool must be **Sleepy-Friendly**:
1.  **Big, Clear Text:** No complex logs. Just "DONE" and "TODO".
2.  **Safety Nets:** explicitly warn if critical files (like `task.md`) haven't been touched in the last hour.
3.  **Positive Reinforcement:** summarized what was accomplished to provide a sense of closure.

## 4. 🛑 Stop Conditions
The EOD is **INCOMPLETE** if:
*   The script indicates `task.md` has no checked items for today.
*   The `walkthrough.md` is missing a new Session Anchor.
*   There are uncommitted changes in the `src/` or `docs/` directories.

**DO NOT SLEEP** until the Hibernation Sequence returns **GREEN**.
