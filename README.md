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

To engage DSOM, initialize your AI session with the **Master Directive**.

**Example Prompt:**

> "Initialize DSOM Protocol. Reference `docs/AI-MASTER-PROTOCOL.md` and perform the Intelligence Audit. Synchronize with `.agent/brain/walkthrough.md` `.agent/brain/task.md` and `.agent/brain/implementation_plan.md` before proposing code."

**Expected Output:**
The AI will acknowledge your architectural laws (e.g., "Zero-Global Pattern") and refuse to proceed until it has verified the current Git delta.

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
