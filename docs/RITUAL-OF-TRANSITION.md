# 🕯️ The DSOM Ritual of Transition (v2.0)

> **"Intelligence is ephemeral; the Repository is eternal."**

This ritual ensures that the project's "State of Mind" survives when switching between AI models, different chat providers, or across sleep cycles.

---

## 🌅 Phase 1: Reanimation (Start of Session)
Before writing a single line of code in a new AI session:
1.  **Environment Check:** Run `tools/audit-pre-flight.sh` to align with physical reality.
2.  **Directive Injection:** Paste the content of `docs/AI-MASTER-PROTOCOL.md` to establish the AI's identity and Haris's authority.
3.  **Memory Sync:** Provide the contents of `.agent/brain/walkthrough.md` and `.agent/brain/task.md`.
4.  **Handshake:** Ask the AI: *"Summarise the current Mental Anchor and confirm you are ready to proceed with Task #[X]."*

---

## 🛠️ Phase 2: Active Flow (The Guardrails)
During the work session:
* **One Change, One Sync:** After every successful module update, update the `walkthrough.md`.
* **Atomic Logic:** If the AI suggests a massive refactor, stop it. Re-verify against the `implementation_plan.md`.
* **CRISP Filter:** Ensure every prompt is **S**ingle-purpose to prevent context bleed.

---

## 🌙 Phase 3: Hibernation (End of Session)
This is the most critical step for **Context Persistence**. Do not close the chat until:

1.  **Define the Mental Anchor:** Write down the exact logic state at the moment of stop.
    * *Example:* "SitemapNode entity is validated; next is the RecursiveCrawler interactor for depth-limited searches."
2.  **Update Artifacts:** Sync the anchor into `walkthrough.md` and update `task.md` with the "Start-of-Day" (SOD) targets for the next session.
3.  **Sovereign Save:** Perform an **Atomic Git Hygiene** commit:
    ```bash
    git add .agent/brain/*.md
    git commit -m "dsom(sync): hibernation save - [Anchor Summary]"
    git push
    ```
4.  **The Metacognitive Briefing:** Tell the AI: *"Summarise the technical hurdles we faced today so I can brief the next agent."*

