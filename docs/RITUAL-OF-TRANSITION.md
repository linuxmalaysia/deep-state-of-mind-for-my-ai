# 🕯️ The DSOM Ritual of Transition

> **"Intelligence is ephemeral; the Repository is eternal."**

This ritual ensures that the project's "State of Mind" survives when switching between AI models, different chat providers, or across sleep cycles. Follow this sequence to prevent "Context Decay."

## 🌅 Phase 1: Reanimation (Start of Session)
Before writing a single line of code in a new AI session:
1.  **Environment Check:** Run `tools/audit-pre-flight.sh` to align with physical reality.
2.  **Directive Injection:** Paste the content of `docs/AI-MASTER-PROTOCOL.md` to establish the AI's identity and Haris's authority.
3.  **Memory Sync:** Provide the contents of `.agent/brain/walkthrough.md` and `.agent/brain/task.md`.
4.  **Handshake:** Ask the AI: *"Summarize the current Mental Anchor and confirm you are ready to proceed with Task #[X]."*

## 🛠️ Phase 2: Active Flow (The Guardrails)
During the work session:
* **One Change, One Sync:** After every successful module update, update the `walkthrough.md`.
* **Atomic Logic:** If the AI suggests a massive refactor, stop it. Re-verify against the `implementation_plan.md`.

## 🌙 Phase 3: Hibernation (End of Session)
This is the most critical step for persistence. Do not close the chat until:
1.  **Define the Mental Anchor:** Write down exactly what you were thinking at the moment of stop. 
    * *Example: "We finished the loop, but the error handler still needs a try-catch for the DB connection."*
2.  **Update Artifacts:** Sync the anchor into `walkthrough.md` and update `task.md` for tomorrow.
3.  **Sovereign Save:** Perform an atomic commit:
    ```bash
    git add .agent/brain/*.md
    git commit -m "dsom(sync): hibernation save - [Anchor Summary]"
    git push
    ```
4.  **The Parting Instruction:** Tell the AI: *"Summarize the technical hurdles we faced today so I can brief the next agent."*

