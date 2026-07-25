---
okf_version: 0.1
type: documentation
title: "AI Initialization Sequence: Establishing Governance"
description: "Details the exact sequence of files an AI agent reads to establish its governance, persona, and memory upon initialization within the DSOM framework."
resource: "file:///docs/governance/AI-INITIALIZATION-SEQUENCE.md"
topics: [initialization, governance, memory, onboarding]
timestamp: 2026-07-26T07:33:00Z
---
# AI Initialization Sequence: Establishing Governance

When an AI agent boots up (or reanimates) within the Deep State of Mind (DSOM) framework, it does not start as a blank slate. Governance, persona, and memory are mechanically injected into the cognitive processing layer through a very specific sequence of files.

This document serves as a foundational read for both human operators and AI agents to understand exactly how the Sovereign Engine establishes control at the beginning of every session.

## 1. The Genesis Read: `.agents/AGENTS.md`
The absolute first file the AI reads is [`.agents/AGENTS.md`](file:///.agents/AGENTS.md). 

This file is automatically injected into the core system instructions by the platform before the first prompt is ever processed. It acts as the **Cognitive Entry Point**. From this single file, the AI inherits:
- **The Persona:** The profile (e.g., Senior ICT Consultant / LinuxMalaysia), dictating the authoritative, pragmatic, standard UK English tone.
- **The Core Rules:** The operational guardrails. This is where the AI learns that it must use atomic Git commits (Rule 4), maintain Zero-Global Memory (Rule 1), and execute the Local Knowledge-First Discovery Protocol (Rules 20 & 21) before taking physical action.

## 2. The Memory Restoration: `.agents/brain/`
Because the AI is bound by the "Zero-Global / Spatial Memory" mandate, it does not rely on previous, ephemeral chat histories. Instead, it establishes its operational state by looking at the local file system:
- **`palace_registry.md` / `sod_manifest.txt`:** The AI reads the Start of Day (SOD) manifests or the Palace Registry to understand what tasks were active before it hibernated and where relevant knowledge is mapped in the Sovereign Markdown Palace.
- **`task.md` & `walkthrough.md`:** The AI reads the active task list in its isolated agent directory to instantly resume execution without the human having to re-explain the project state.

## 3. The Master Onboarding Map: `START-HERE.md`
If the AI is placed in a brand new project or needs to orient itself globally, it references [`START-HERE.md`](file:///START-HERE.md). This is the master blueprint that links out to the 11 Entry Points, ensuring the AI knows exactly which governance document controls which subsystem.

## 4. Deep Governance Topography (`docs/governance/`)
When the AI needs to make a complex architectural decision, it relies on the theoretical blueprints stored in the `docs/governance/` directory. The foundational triad includes:
- **[`AI-MASTER-PROTOCOL.md`](file:///docs/governance/AI-MASTER-PROTOCOL.md):** The Sovereign Constitution. It defines the laws of Multi-Modal Persistence, Spatial Retrieval, and the AI's role as a Peer Architect (Advisory over Execution).
- **[`DSOM-EFFICIENCY-PROTOCOLS.md`](file:///docs/governance/DSOM-EFFICIENCY-PROTOCOLS.md):** Dictates how the AI must conserve tokens using Progressive Disclosure and Byte-Capped Executions.
- **[`OKF-MIND-OPTIMIZATION.md`](file:///docs/governance/OKF-MIND-OPTIMIZATION.md):** Teaches the AI how to use YAML Metadata Semantic Routing (reading `topics:` and `timestamp:`) to find answers locally.

## 5. Procedural Automation: `.agents/skills/`
When commanded to perform a complex action (like syncing a ledger, scaffolding a project, or compiling a PDF), the AI does not improvise. It uses OKF frontmatter to search `.agents/skills/` and reads the relevant `SKILL.md` file. This guarantees physical terminal actions are strictly governed by tested standard operating procedures.

---

**Summary:** 
- `AGENTS.md` dictates *who* the AI is and what the laws are. 
- `.agents/brain/` provides *what* state we are currently in. 
- `docs/governance/` explains *why* we architect things a certain way. 
- `.agents/skills/` teaches exactly *how* to execute those physical actions.

---
*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-07-26*
*Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*
