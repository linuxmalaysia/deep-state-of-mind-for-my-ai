# README.md

# 🧠 Deep State of Mind (DSOM) Protocol

> **Bridging the gap between Human Architectural Intent and AI Execution for Open Source Sovereignty.**

[![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)]()
[![License](https://img.shields.io/badge/License-GPL--3.0-orange.svg)]()
[![Author](https://img.shields.io/badge/Author-Harisfazillah%20Jamel-blue.svg)]()
[![Partner](https://img.shields.io/badge/AI%20Partner-Google%20Gemini-purple.svg)]()

## 📝 Description

**Deep State of Mind (DSOM)** is a metacognitive framework designed to prevent "Context Decay" in AI-assisted software development. While standard AI interactions are transactional, DSOM creates a **persistent and structural** bridge between the developer's expertise and the AI's generation capabilities.

This project provides the tools and directory structures necessary to transform a standard AI (like Google Gemini, Claude, or ChatGPT) into a **Cognitive Digital Twin** of the Lead Architect. It enforces high-availability standards, strict architectural laws, and pedagogical integrity across long-term open-source projects.

It was forged in the **CMSForNerd v3.5 Laboratory** to ensure that AI agents (Gemini, Copilot, Cursor) operate not just as coders, but as **Cognitive Digital Twins** of the Lead Architect. It enforces high-availability standards, strict architectural laws (Zero-Global, Pair-Logic), and pedagogical integrity across long-term open-source projects.

### Features

* **State Persistence:** Uses `.agent/brain/` artifacts to bridge sessions and maintain context across different AI chats.
* **Intelligence Audit:** A mandatory "Pre-Flight" script verifies the physical environment and Git state before any code is written.
* **Root-Aware Automation:** Tools are designed to function correctly from any subdirectory within a Git repository.
* **Sovereignty Focused:** Built specifically for Linux-agnostic, portable, and secure open-source development under the GPLv3 license.

---

## 🖼️ Visuals

The DSOM workflow ensures that the AI's "Mind" is always synced with the "Physical" state of the code.


```text
[ Physical Git State ] <---> [ .agent/brain/ ] <---> [ AI Agent Intelligence ]
          ^                        |                          ^
          |________________________|__________________________|
                         (The DSOM Handshake)

```

---

## ⚙️ Installation

### Requirements

* **Operating System:** Linux (Optimized for Enterprise distributions like Ubuntu, AlmaLinux, RHEL).
* **Version Control:** Git.
* **Environment:** Any programming language (The auditor auto-detects PHP, Node.js, Python, and Go).

### Setup
1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/linuxmalaysia/deep-state-of-mind-for-my-ai.git](https://github.com/linuxmalaysia/deep-state-of-mind-for-my-ai.git)
    cd deep-state-of-mind-for-my-ai
    ```
2.  **Initialize the Brain:**
    Create the required context files (this will not overwrite existing files):
    ```bash
    bash tools/init-brain.sh
    ```
3.  **Set Permissions:**
    ```bash
    chmod +x tools/*.sh
    ```

---

## 🚀 Usage

### 1. The Pre-Flight Audit

Before starting any development session, run the auditor to ensure your Git state and environment are ready:

```bash
./tools/audit-pre-flight.sh

```

### 2. Engaging the AI

Initialize your AI session by providing it with the contents of the `.agent/brain/` folder. This gives the AI your "Deep State of Mind" regarding:

* **task.md**: What we are doing right now.
* **walkthrough.md**: What we did in the last session.
* **implementation_plan.md**: The long-term roadmap.

The `implementation_plan.md` must serve as the **Long-Term Strategic Roadmap**. Unlike `task.md` (which is for today) or `walkthrough.md` (which is for the past), this file defines the **Vision** and **Phases** of the DSOM project.

To engage DSOM, initialize your AI session with the **Master Directive**.

**Example Prompt:**

> "Initialize DSOM Protocol. Reference `docs/AI-MASTER-PROTOCOL.md` and perform the Intelligence Audit. Synchronize with `.agent/brain/walkthrough.md` `.agent/brain/task.md` and `.agent/brain/implementation_plan.md` before proposing code."

**Expected Output:**
The AI will acknowledge your architectural laws (e.g., "Zero-Global Pattern") and refuse to proceed until it has verified the current Git delta.


## 🕯️ The Ritual of Transition (Persistence Logic)

To maintain the **Deep State of Mind** across different AI models (Gemini, Claude, or local LLMs) and different accounts, users must follow the **Ritual of Transition**. 

This protocol ensures that:
1.  The AI is **reanimated** with the correct architectural laws.
2.  The "Mental Anchor" is preserved so work resumes exactly where it stopped.
3.  The project remains **Sovereign**—independent of any specific AI provider's memory limits.

See [docs/RITUAL-OF-TRANSITION.md](docs/RITUAL-OF-TRANSITION.md) for the full checklist.

---

We will break down these three core files using the **Why, What, Who, When, and How** framework. This ensures that any user (or AI agent) understands not just the content, but the strategic intent behind them.

### 1. `.agent/brain/task.md`

**The "Cutting Edge" of Development**

* **WHY:** To solve "Short-Term Memory Loss" in AI. Without this, an AI agent often forgets the specific sub-task it was working on if the chat session is interrupted or hits a token limit.
* **WHAT:** A granular, checklist-oriented file that tracks immediate objectives. It represents the "Present" state of the project.
* **WHO:** Managed by the **AI Agent** (under human supervision). The AI updates this file as it completes sub-tasks to provide a "handover" for the next session.
* **WHEN:** Updated **continuously** during a work session. Every time a feature is finished or a bug is squashed, this file is modified.
* **HOW:** * Use Markdown checkboxes (`- [ ]` for pending, `- [x]` for done).
* Keep tasks "Atomic"—no task should be so large that it takes more than one session to complete.
* Always verify against this file during the "Morning Ritual" handshake.

---

### 2. `.agent/brain/implementation_plan.md`

**The Strategic Roadmap**

* **WHY:** To ensure the project doesn't suffer from "Scope Creep." It anchors the AI to the long-term vision so it doesn't suggest refactors that contradict the final goal.
* **WHAT:** A high-level document divided into Phases (e.g., Phase 1: Infrastructure, Phase 2: Core Logic). It represents the "Future" state of the project.
* **WHO:** Authored by the **Lead Architect (Harisfazillah Jamel)**. The AI refers to this as a "Non-Negotiable" map.
* **WHEN:** Created at the **start of a project** and updated only when there is a major shift in technical strategy or versioning (e.g., moving from v4.1 to v5.0).
* **HOW:**
* List major technical milestones (e.g., "Implement HA Clustering").
* Define the "Definition of Done" for each phase.
* The AI must trigger a **Stop Condition** if a user request deviates from this plan.

---

### 3. `docs/AI-MASTER-PROTOCOL.md`

**The Sovereign Constitution**

* **WHY:** To enforce "Architectural Sovereignty." It prevents the AI from acting like a generic chatbot and forces it to adopt the persona of a Senior Systems Architect who respects 35+ years of ICT standards.
* **WHAT:** The primary governance document containing the "Laws of the System" (Zero-Global Pattern, Sovereign Portability, Pedagogical Documentation).
* **WHO:** The **Supreme Authority** for all AI Agents. It is the first document "injected" into any new AI session.
* **WHEN:** Consulted **every time a new chat session begins** or when a model switch (e.g., Gemini to Claude) occurs.
* **HOW:**
* Contains the **Handshake Protocol** (The mandatory questions the AI must ask before coding).
* Defines the **Execution Standards** (VCS Hygiene, Language requirements like PHP 8.4+).
* Establishes the **Identity** of the AI as the "Cognitive Digital Twin" of the Lead Architect.

---

### 🏁 Summary Table for README.md Integration

You can add this table to your `README.md` to help others understand the "Trinity of Persistence":

| File | Temporal State | Primary Purpose | Authority |
| --- | --- | --- | --- |
| `task.md` | **Present** | Immediate focus & checklist. | AI-Driven |
| `walkthrough.md` | **Past** | Context, "Why", & Mental Anchors. | Hybrid |
| `implementation_plan.md` | **Future** | Roadmap & Strategic Guardrails. | Human-Driven |
| `AI-MASTER-PROTOCOL.md` | **Eternal** | Governance, Laws, & Identity. | Human-Driven |

---

## 🛠️ Included Tools

| Tool | Purpose | License |
| --- | --- | --- |
| `init-brain.sh` | Safely creates the `.agent/brain` structure without overwriting data. | GPLv3 |
| `audit-pre-flight.sh` | Checks for Git drift, required artifacts, and project environment. | GPLv3 |

---

## 🗺️ Roadmap

* [x] **v4.1:** Initial release with Root-Aware scripts.
* [x] **Licensing:** Full GPLv3 integration for open-source sovereignty.
* [ ] **v4.5:** Automated "Session Summary" generator for `walkthrough.md`.
* [ ] **v5.0:** Integration with local LLMs via Ollama for offline DSOM.

---

## 🤝 Contributing

I am open to contributions that enhance the strictness and reliability of the protocol.

* **Requirements:** All PRs must include a `walkthrough.md` logic update.
* **Standard:** Use Atomic Commits (one file per commit with descriptive messages).
* **Documentation:** New patterns must be documented in the Project Knowledge Graph.

I use **Atomic Commits** for this project. Please ensure each pull request or commit targets a single file or logic change with a descriptive message.

### Example: The Final Atomic Commit
Now, let's practice the "one-by-one" method you requested to save this to your repo:

```bash
# 1. Add the README
git add README.md

# 2. Commit with detailed comment
git commit -m "docs: finalize README.md with detailed DSOM architecture, visual workflow descriptions, and tool usage"

# 3. Push to GitHub
git push

```

---

### 🚦 Your Day 1 Starting Point

When you sit down tomorrow, your first prompt to the AI will be:

> *"Initialize DSOM Protocol. Perform the Intelligence Audit. Then, use DSOM_TEMPLATE.md to initialize today's session log in .agent/brain/walkthrough.md based on the current task."*

---

## 👤 Authors and Acknowledgment

* **Lead Architect & Author:** [Harisfazillah Jamel](https://www.google.com/search?q=https://github.com/harisfazillah) – A veteran with 35+ years of ICT & Open Source Leadership.
* **AI Thought Partner:** Google Gemini - Assisted in refactoring scripts and optimizing documentation.
* **Inspiration:** The CMSForNerd v3.5 Laboratory community.

---

## 📄 License

This project is licensed under the **GNU General Public License v3.0**. See the [LICENSE](https://www.google.com/search?q=LICENSE) file for details.

---

## 🚦 Project Status

**ACTIVE.** This framework is the primary governance model for LinuxMalaysia's AI-assisted development.
**ACTIVE.** The DSOM protocol is actively used to govern the development of CMSForNerd and related high-availability infrastructure projects.

20260107

