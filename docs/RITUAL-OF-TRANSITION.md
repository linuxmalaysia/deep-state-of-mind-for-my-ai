# 🕯️ The DSOM Ritual of Transition (v2.0)

> **"Intelligence is ephemeral; the Repository is eternal."**

This ritual is the core mechanism of the **Deep State of Mind (DSOM) Protocol**. It prevents context decay and ensures that **Clean Architecture** layers remain unpolluted when transitioning between AI agents or sessions.

---

## 🌅 Phase 1: Reanimation (Start of Session)
*Objective: Re-establish the CRISP Context.*

1.  **Environment Audit:** Run `tools/audit-pre-flight.sh`. Ensure the physical state (files/logs) matches your mental state.
2.  **Protocol Injection:** Load `docs/AI-MASTER-PROTOCOL.md`. This forces the AI to adopt the **Cognitive Twin** persona and apply **UK English/DBP Malay** standards.
3.  **Brain Synchronisation:** Provide `.agent/brain/walkthrough.md` and `task.md`.
4.  **The Handshake:** Ask the AI: *"Summarise the current Mental Anchor and verify how it fits within our Clean Architecture layers (Entities/Use Cases)."*

---

## 🛠️ Phase 2: Active Flow (The Guardrails)
*Objective: Enforce CRISP Pillars & Layered Sovereignty.*

* **Context Awareness:** Never start a task without checking the `.agent/brain/`.
* **Review & Record:** Use **Atomic Git Hygiene**. Every logic change requires a corresponding update to the `walkthrough.md`.
* **Iteration:** Do not refactor the 'Inner Circle' (Entities) while working on 'Outer Circles' (Frameworks).
* **Single-purpose:** One chat thread = One Clean Architecture Use Case. Avoid "Big Ball of Mud" prompts.
* **Partnership:** Treat the AI as a peer architect. If the AI violates **Sovereign Portability**, challenge it.

---

## 🌙 Phase 3: Hibernation (End of Session)
*Objective: Secure the Mental Anchor.*

1.  **Define the Mental Anchor:** Document the exact logical "stopping point." 
    * *Constraint:* Identify which **Clean Architecture** layer is currently "open" (e.g., "The Sitemap Interactor is written but not yet injected with the Repository interface").
2.  **Sync Artifacts:** Update `task.md` with the **Start-of-Day (SOD)** targets for the next session.
3.  **Sovereign Save:**
    ```bash
    git add .agent/brain/*.md
    git commit -m "dsom(sync): hibernation save - [Layer: UseCase] - [Anchor Detail]"
    git push
    ```
4.  **Metacognitive Briefing:** Instruct the AI: *"Compress our technical hurdles and architectural decisions from today into a single transfer packet for the next session."*

---
*Standard: Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel*

