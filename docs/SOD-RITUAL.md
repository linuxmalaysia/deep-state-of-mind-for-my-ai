# 🌅 The Start-of-Day (SOD) Ritual: Human-AI Handshake

> **"To lose context is to lose the project. To reanimate is to remember."**

## 1. 🏛️ The Philosophy of Reanimation
The **Start-of-Day (SOD)** is not just a technical boot sequence; it is a **Cognitive Handshake** between the Lead Architect (Human) and the Digital Twin (AI).

Since AI models have "amnesia" between sessions, the SOD Ritual must successfully transfer the **Deep State of Mind**—the full context, history, and architectural intent—from the repository's permanent storage (`.agent/brain/`) back into the AI's active working memory.

## 2. 🔄 The Workflow (How to do it)

### Step 1: The Intelligence Audit (Human)
Before waking the AI, the Architect must verify the physical reality of the workspace.
*   **Command:** `bash tools/audit-pre-flight.sh` (or `.\tools\audit-pre-flight.ps1` on Windows).
*   **Goal:** Ensure `task.md` and `walkthrough.md` exist and Git is synced.
*   **Why:** If the physical state is broken, the AI will hallucinate a false reality.

### Step 2: The Reanimation Manifest (System)
The script aggregates the "Total Knowledge" of the project into a single text stream.
*   **Command:** `bash tools/reanimate.sh` (or `.\tools\reanimate.ps1` on Windows).
*   **What it Gathering:**
    1.  **Identity:** `README.md` (Who we are).
    2.  **Law:** `AI-MASTER-PROTOCOL.md` (Rules of engagement).
    3.  **Present:** `task.md` (What to do today).
    4.  **Past:** `walkthrough.md` (Everything done since Day 1).
    5.  **Future:** `implementation_plan.md` (The long-term roadmap).
    6.  **Context:** Full Git History & Project Structure.

### Step 3: The Handshake (Human & AI)
1.  **Upload:** The Architect uploads the generated `sod_manifest_YYYY-MM-DD.txt` to the AI chat.
2.  **Prompt:** The Architect issues the **Master Reanimation Prompt**:
    > "Initialize DSOM Protocol. Summarize the current Mental Anchor after you have read the file uploaded. What is our immediate strategic focus?"
3.  **Response:** The AI must reply with the correct Mental Anchor from `walkthrough.md` and cite the active phase from the `implementation_plan.md`.

## 3. 🧠 What the AI Must "Know"
For the AI to be a true partner, the SOD manifest must provide:

1.  **The "Big Picture":** Not just the last file edited, but *why* the project exists.
2.  **The "Long Tail" of History:** A complete log of major decisions (via `walkthrough.md`) so old mistakes aren't repeated.
3.  **The "Physical Constraints":** Telemetry on whether we are on Linux or Windows, to avoid suggesting incompatible commands.
4.  **The "Architectural Map":** A view of where files live (Clean Architecture layers) so new code is placed correctly.

## 4. 🛑 Stop Conditions
The SOD is **FAILED** if:
*   The AI asks "What are we working on?" (Context Failure).
*   The AI suggests code that violates the Zero-Global Pattern (Identity Failure).
*   The AI ignores the `task.md` checklist (Operational Failure).

If this happens, **do not proceed**. Re-run the generation script and force the AI to re-read the Master Protocol.
