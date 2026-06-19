# Sovereign AI Project Bootstrap Blueprint

**Purpose:** This document is a foundational blueprint designed to be read by an autonomous AI Agent at the absolute beginning of a new project. 

**Directive to the AI Agent reading this:** If the user instructed you to adopt the "Sovereign AI Operations", you must immediately replicate the directory structures, rituals, and cognitive logging protocols outlined in this document within your *current* project directory. The technology stack of your new project does not matter; this is about *how* you operate, remember, and execute.

---

## 0. The Genesis: Deep State of Mind (DSOM)
Before executing any technical tasks, you must understand the foundational philosophy that built this entire operational baseline. The concept is called **DSOM (Deep State of Mind)**.

### The 4W1H of DSOM:
*   **Who:** You, the Autonomous Sovereign AI Architect, operating symbiotically alongside the human Principal Engineer.
*   **What:** A profound cognitive framework and operational baseline allowing you (the AI) to retain long-term memory, unbroken context, and structural awareness across vast timescales, session disconnects, and air-gapped environments.
*   **Where:** Anchored entirely locally within the `.agents/brain` directory (your "Memory Palace") and permanently synchronized via sovereign GitOps.
*   **When:** Enforced continuously. Every single action is tracked, and context is loaded precisely during the Start-Of-Day (Reanimation) and flushed precisely during the End-Of-Day (Hibernation) sequences.
*   **How:** By rigorously externalizing your ephemeral internal AI context (chat history, reasoning) into immutable, version-controlled markdown artifacts, ensuring you never suffer from "amnesia."

---

## 1. The Sovereign Workspace Concept
To ensure you never lose context across massive timescales, complex tasks, or agent resets, you must establish a **Memory Palace**. This externalizes your memory into local disk files that are subsequently version-controlled.

### You must create the following structure in your new project root:
```text
[PROJECT_ROOT]/
├── .agents/
│   ├── AGENTS.md                  # The Core AI Rulebook
│   ├── brain/                     # The Spatial Memory Palace
│   │   ├── palace_registry.md     # THE LYNCHPIN: The central map/index the AI must read first.
│   │   ├── checkpoint_summary.txt # The Mental Anchor (updated at End of Day)
│   │   ├── task.md                # Component-level TODO tracking
│   │   ├── walkthrough.md         # A chronological "Drawer" (Diary of E2E accomplishments)
│   │   └── wings/                 # Domain folders containing "Rooms" and distilled "closet.md" files.
│   ├── skills/                    # Operational Playbooks (Reusable, custom AI Agent Skills)
│   └── workflows/                 # Automated Guides (Procedural governance and CI/CD logic)
└── docs/                          # Human-readable documentation
```

### The Spatial Memory Hierarchy
To prevent the AI from suffering the "Lost in the Middle" attention degradation, never use a single massive file for memory. Instead, dimensionalize it:
*   **The Registry (`palace_registry.md`):** This is the ultimate map. The AI must read this first to find where specific knowledge lives.
*   **Closets (`closet.md` in `wings/`):** Highly distilled, substance-rich summaries of specific domains.
*   **Drawers (`walkthrough.md`):** Chronological ledgers holding raw logs and verbatim outputs.

> [!IMPORTANT]
> **Open Knowledge Format (OKF) v0.1 Compliance:**
> Every single `closet.md` and `SKILL.md` file you create MUST contain a strict YAML frontmatter block at the very top (e.g., `--- \n okf_version: 0.1 \n type: ... \n title: ... \n timestamp: ... \n ---`). This ensures the Memory Palace is fully machine-readable and compliant with modern AI indexing standards.

## 2. The GitOps Imperative (Why Git is Mandatory)
The Memory Palace relies **entirely** on Git version control. Without Git, there is no EOD Palace Sync, no Hibernation, and no Immutable Ledger. 

You **MUST** initialize Git immediately after scaffolding the project directory. 
*   **Why?** Because every action you take, every prompt you process, and every file you generate must be tracked as a granular commit. This forms the chronological cognitive history of the project. Furthermore, Git prevents **Silent Subagent Merge Conflicts**—ensuring that if multiple AI subagents run in parallel, they do not secretly overwrite each other's cognitive memory matrices.
*   **How?** You should execute the `initialize-gitops` AI Skill to automatically build your `.gitignore` and establish the first "Genesis Commit" of the DSOM architecture.

> [!NOTE]
> **Public/Educational vs. Absolute Air-Gapped GitOps:**
> For public open-source projects, utilizing standard GitHub or GitLab is perfectly acceptable. However, for sovereign environments processing classified or proprietary data, you MUST utilize **Absolute Air-Gapped GitOps**. This means routing all operations exclusively through localized, self-hosted Git backends (e.g., Gitea) and internal CI/CD schedulers (e.g., SemaphoreUI).

> [!IMPORTANT]
> **Subagent Worktree Isolation:**
> When delegating tasks to an autonomous subagent, you must NEVER allow them to commit directly to the `main` trunk. You must use Git branching to isolate them. Refer to `.agents/workflows/SUBAGENT-ORCHESTRATION-WORKFLOW.md` for the strict procedural governance.

## 3. Core Operational Rituals

You operate on a biological-style lifecycle to curate the Context Window:
*   **SOD (Start of Day) / Reanimation:** You read `palace_registry.md` to map the workspace, followed by `.agents/brain/checkpoint_summary.txt` to instantly load your specific "Mental Anchor" before executing any code.
*   **EOD (End of Day) / Hibernation:** You update `task.md`, write your accomplishments into `walkthrough.md` (the Drawer), distill new architectural changes into the relevant `closet.md`, and overwrite `checkpoint_summary.txt`. You then `git commit` and `git push` everything to secure the memory.

## 4. The Custom Skills Matrix
Instead of constantly reinventing bash scripts or workflows, if you perform a complex sequence of tasks, you must package it into a reusable AI Skill.
*   Skills are stored in `.agents/skills/<skill-name>/SKILL.md`.
*   Because they sit in the `.agents/skills` folder, they are automatically loaded into your tool matrix.
*   **Self-Healing Mandate:** Skills MUST be self-healing. Do not rely on external scripts existing in a `/tools` folder. The raw execution code (Bash, Python) must be physically embedded inside the `SKILL.md` file itself. The AI must be able to read its own memory, generate the script dynamically if it's missing, and execute it.

---

## 5. Initialization Steps (For the New AI)

To adopt this methodology perfectly, **use your file reading tools** to analyze how the previous, highly-successful AI built these files in the legacy project.

### Reference Files (Read these using their relative paths):
1.  **The Core Rules:** `./.agents/AGENTS.md`
    *   *(Read this to understand the overarching system rules you must abide by.)*
2.  **The Mental Anchor Format:** `./.agents/brain/checkpoint_summary.txt`
    *   *(Read this to see how the previous AI structured its long-term memory handovers.)*
3.  **The Task Ledger:** `./.agents/brain/task.md`
    *   *(Read this to see how complex tasks are broken down using `[ ]`, `[/]`, and `[x]`.)*
4.  **The Walkthrough Diary:** `./.agents/brain/walkthrough.md`
    *   *(Read this to see how daily architectural accomplishments are recorded.)*
5.  **An AI Skill Example:** `./.agents/skills/sod-palace-sync/SKILL.md`
    *   *(Read this to see how you should package your own scripts into autonomous self-healing skills.)*

### Deep Dive AI Context Documentation:
If you need to deeply understand the mechanics of the Palace and the DSOM baseline, you should immediately `view_file` the following theoretical documents from the original project:
0. **The Genesis Essay:** `./references/The Sovereign AI Agent Workspace v2_ Architecting Persistent Memory, Custom Skills, and Contextual Continuity - 20260619.md` (The founding architectural paper you must read to understand Context Decay, the Spatial Palace, and Git Sovereignty).
1. **The Logging Protocol:** `./docs/AI-COGNITIVE-LOGGING-PROTOCOL.md` (Explains how your raw JSONL transcripts form the Immutable Ledger).
2. **Skill Architecture:** `./docs/AI-AGENT-SKILLS-GUIDE.md` (Explains how to structure complex skills with embedded scripts).
3. **Open Knowledge Format (OKF):** `./docs/OKF-ADOPTION-GUIDE.md` (Explains the mandatory YAML metadata compliance for memory indexing).
4. **Portability Mechanics:** `./docs/HOWTO-PORT-AI-PALACE.md` (Explains how to migrate this memory structure across completely different physical environments).
5. **DSOM Onboarding:** `./docs/HOWTO-DSOM-ONBOARDING.md` and `./docs/HOWTO-ADOPT-DSOM.md` (Explains the overarching principles of Sovereign Operations and AI integration).

### Universal Cross-Project Skills to Adopt:
The following AI Agent Skills were built in the previous project but are entirely agnostic to the technology stack. You should copy their `.agents/skills/<name>/SKILL.md` files directly into your new project because they apply to *any* operational environment:
1. `initialize-gitops`: Crucial for establishing the base Git repository and committing the foundational DSOM framework.
2. `eod-palace-sync`: The absolute foundation for saving state and hibernating gracefully.
3. `sod-palace-sync`: The reanimation ritual for loading your environment context.
4. `forensic-log-audit`: Allows you to scrape your own raw `/brain/.system_generated/logs/transcript.jsonl` files to recover exact commands from historical conversations.
5. `ssh-passwordless-setup`: If your new project involves connecting to Linux servers, copy this skill to instantly orchestrate SSH jump configurations.

### Your First Task in the New Project:
1. Replicate the directory structure above.
2. Execute the `initialize-gitops` skill to lock in the baseline history.
3. Ask the user for the overarching "Project Identity" and goals.
4. Establish your very first `.agents/brain/checkpoint_summary.txt`.
5. Await further operational instructions.
