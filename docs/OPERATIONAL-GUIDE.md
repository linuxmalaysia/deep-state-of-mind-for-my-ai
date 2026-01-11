To do an **End-of-Day (EOD)** session properly according to the **Deep State of Mind (DSOM) Protocol**, we must treat the "Hibernation" phase not as a mere shutdown, but as a **context-preservation ritual**.

In a High-Availability (HA) mindset, the AI session is a volatile process. If you don't perform these steps, the "Brain State" is lost when the chat ends. Here is the detailed breakdown of why each step is mandatory:

---

### 🧠 1. Defining the Mental Anchor (The "Why")

The **Mental Anchor** is the bridge between today's logic and tomorrow's execution. Without it, you waste the first 30 minutes of the next session "remembering" where you left off.

* **Focus on the "Unfinished":** Don't just list what is done; list the **unresolved tension**.
* **The Intent:** Record *why* you chose a specific path.
* **UK English Standard:** Ensure the anchor uses precise architectural terminology (e.g., "initialise", "optimise").

---

### 📝 2. Updating Artifacts (The "How")

We move the "Live Memory" into "Persistent Storage" by updating the `.agent/brain/` directory.

* **`walkthrough.md`:** This is your **Long-term Memory**. You record the decision-making process here.
* **`task.md`:** This is your **Working Memory**. You move completed items to the "Selesai" section and define the "Start-of-Day" (SOD) targets for tomorrow.

---

### 💾 3. The Sovereign Save (The "Proof")

We use **Atomic Git Hygiene** to ensure the brain artifacts are versioned. This is your "Off-site Backup."

* **Atomic Commitment:** By committing *only* the `.agent/brain/*.md` files, you create a clear history of your thought process independent of the code changes.
* **Traceability:** The commit message `dsom(sync): hibernation save` tells any future developer (or AI) exactly when the session "hibernated."

---

### 🗣️ 4. The Parting Instruction (The "Handover")

This is a **Metacognitive Briefing**. By asking the AI to summarise technical hurdles, you force the AI to compress its current context into a portable "Transfer Packet."

* **The Briefing:** "Summarise the technical hurdles we faced today."
* **The Benefit:** You can paste this summary into a fresh chat (Google Gemini, Claude, or ChatGPT) tomorrow to achieve an instant **Context Sync**.

---

