# 📖 DSOM Operational Guide: Comprehensive AI Governance

This guide provides the technical depth behind the **Deep State of Mind (DSOM) Protocol**. It is designed for the Senior Systems Architect to maintain high-availability (HA) context and **Clean Architecture** integrity across disparate AI agents.

---

## 🏛️ Core Principles of Operation

1.  **Sovereign Logic First:** Business rules (Entities/Use Cases) must be defined before framework implementation (Adapters/Drivers).
2.  **Linguistic Precision:** All documentation and code comments strictly follow **UK English** and **DBP-standard Bahasa Melayu Malaysia (Piawai)**.
3.  **Metacognitive Persistence:** AI state is volatile; the Git repository is the only "Source of Truth."

---

### 🌅 Section 1: Reanimation (Start-of-Day Ritual)

Reanimation is the process of restoring the AI's "Mental State" from the repository's cold storage. It is not a casual greeting; it is a **Formal Initialisation Sequence** consisting of three critical verification gates.

#### 1.1 The Environment Audit (Physical Reality Sync)

Before engaging the AI, the Architect must verify that the physical infrastructure matches the last recorded state in the `.agent/brain/`.

* **Infrastructure Check:** Run `tools/audit-pre-flight.sh`. This script should verify container status (Podman/Docker), service health (Systemd), and directory integrity.
* **Log Inspection:** Check the last 50 lines of the system logs. If a service failed overnight, this "Physical Reality" must be fed to the AI as immediate context.
* **Artifact Integrity:** Ensure `walkthrough.md` was not left in a "Dirty State" from an uncommitted session.

#### 1.2 The Directive Injection (Establishing Sovereignty)

Loading `docs/AI-MASTER-PROTOCOL.md` is the act of defining the AI's **Operating System**. It overwrites generic AI training with **Sovereign Mandates**.

* **Linguistic Guardrails:** Re-establishes the requirement for **UK English** (e.g., 'initialise', 'centre') and **DBP-standard Bahasa Melayu Malaysia** (Piawai). This prevents "Linguistic Drift" into Indonesian vocabulary.
* **Architectural Guardrails:** Re-injects the **Zero-Global Pattern** and **HA-Ready** constraints.
* **Role Assumption:** Forces the AI to move from "General Assistant" to "Senior Systems Architect / Cognitive Digital Twin."

#### 1.3 The Contextual Handshake (Cognitive Alignment)

The Handshake is the final gate. You are verifying that the AI has successfully processed the **Clean Architecture** layers of the current project.

* **The Anchor Test:** Ask the AI to explain the *logic* (the "Why") behind the current **Mental Anchor**, not just repeat the text.
* **Layer Verification:** Require the AI to identify which Clean Architecture layer (Entity, Use Case, Adapter, or Driver) is the current priority.
* **The "Stop" Condition:** **If the AI fails to explain the connection between the current task and the sovereign laws, do not proceed.** You must re-inject the protocol or clear the context.

---

## 🛠️ Section 2: Active Flow (The Guardrails)

Maintaining a **Clean DSOM (C-DSOM)** requires constant vigilance.

* **The CRISP Filter:**
    - **Context Awareness:** Refer to `.agent/brain/` before every architectural decision.
    - **Review & Record:** Update `walkthrough.md` immediately after a logic breakthrough—*before* the code is even finished.
    - **Iteration:** Apply **Atomic Git Hygiene**. Commit one file at a time using `type(scope): message`.
    - **Single-purpose:** If a task spans multiple Clean Architecture layers, break it into separate prompts.
    - **Partnership:** Challenge the AI. If it suggests a global variable, invoke the **Zero-Global Pattern** law.

Maintaining a **Clean DSOM (C-DSOM)** requires constant vigilance. The "Active Flow" is the execution phase where the Architect and the Cognitive Twin work in tandem. To prevent the degradation of the **Sovereign Core**, the following CRISP filters must be applied to every interaction.

### 2.1 The CRISP Filter in Operation

#### **C - Context Awareness (The 'Anchor' Check)**

* **Artifact Consultation:** Never allow the AI to guess the project structure. Before every architectural decision, explicitly prompt: *"Refer to `.agent/brain/task.md` and `walkthrough.md` to ensure this logic aligns with our current trajectory."*
* **Boundary Enforcement:** Ensure the AI is aware of which **Clean Architecture** layer is being modified. If we are in the "Entity" layer, the AI must be prohibited from suggesting database-specific or framework-specific code.

#### **R - Review & Record (The 'Black Box' Logger)**

* **Immediate Capture:** Update `walkthrough.md` immediately after a logic breakthrough—*before* the code is even finished. This captures the **Pedagogical Logic** while it is fresh.
* **Peer Review:** The Architect must review the AI’s output not just for "Does it work?" but for "Does it follow the Sovereign Laws?" (e.g., UK English, Zero-Global Pattern).

#### **I - Iteration (Atomic Git Hygiene)**

* **Single-File Focus:** Apply **Atomic Git Hygiene**. Commit one file at a time using the `type(scope): message` format (e.g., `feat(domain): initialise sitemap entity`).
* **Incremental Stability:** Avoid monolithic blocks of code. Each iteration must be a "functional unit" that could theoretically be deployed or tested in isolation.

#### **S - Single-purpose (Anti-Complexity Filter)**

* **Layer Isolation:** If a task spans multiple Clean Architecture layers (e.g., adding a new field to an Entity and updating the Database Driver), break it into **separate prompts**.
* **Prompt Precision:** A prompt should only ask for one outcome. This reduces "AI Hallucinations" by limiting the cognitive load on the LLM's attention mechanism.

#### **P - Partnership (The Peer Challenge)**

* **Socratic Dialogue:** Challenge the AI. If it suggests a global variable, invoke the **Zero-Global Pattern** law.
* **Correction Ritual:** If the AI uses Indonesian vocabulary (e.g., *standar* instead of *piawai*), immediately correct it to maintain **DBP-standard Bahasa Melayu Malaysia**. The AI must acknowledge the correction before proceeding.

---

### 🏛️ 2.2 Enforcing Clean Architecture during Flow

During Active Flow, the **Dependency Rule** is your primary guardrail. All dependencies must point inwards.

| Layer | Guardrail Action |
| --- | --- |
| **Entities** | Strictly no imports from external libraries or other layers. Pure logic only. |
| **Use Cases** | Must only interact with Entities and Interfaces. No knowledge of the UI or DB. |
| **Adapters** | This is the only place where data transformation occurs. |
| **Frameworks** | Isolate specific tools (e.g., Podman commands) here to ensure **Sovereign Portability**. |

---

## 🌙 Section 3: Hibernation (The Context-Preservation Ritual)

In an HA-Ready mindset, Hibernation is a **Graceful Shutdown** with state persistence.

### 🧠 1. Defining the Mental Anchor (The "Why")
The **Mental Anchor** is the bridge between today's logic and tomorrow's execution. Without it, you waste the first 30 minutes of the next session "remembering" where you left off.
* **Focus on the "Unfinished":** Don't just list what is done; list the **unresolved tension**.
* **The Intent:** Record *why* you chose a specific path (e.g., "Used Python Dataclasses for immutability to support HA state sharing").

### 📝 2. Updating Artifacts (The "How")
We move the "Live Memory" into "Persistent Storage" by updating the `.agent/brain/` directory.
* **`walkthrough.md`:** This is your **Long-term Memory**. Every decision, failure, and pivot is recorded here to prevent repeating mistakes.
* **`task.md`:** This is your **Working Memory**. Update the "Tugasan" list to reflect real-world progress and set the next SOD (Start-of-Day) target.

### 💾 3. The Sovereign Save (The "Proof")
We use **Atomic Git Hygiene** to ensure the brain artifacts are versioned. This is your "Off-site Backup."
* **Atomic Commitment:** Committing `.agent/brain/*.md` separately creates a historical timeline of your **Cognitive Digital Twin's** evolution.
* **Traceability:** Use the commit format `dsom(sync): hibernation save - [Anchor Summary]`.

### 🗣️ 4. The Parting Instruction (The "Handover")
This is a **Metacognitive Briefing**. By asking the AI to summarise technical hurdles, you force the AI to compress its current context into a portable **Transfer Packet**.
* **The Benefit:** This summary serves as the "Pre-flight Briefing" for the next session, allowing for an instant **Context Sync** across different AI models.

---
*Standard: Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel*

