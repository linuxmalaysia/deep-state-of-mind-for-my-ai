# 🎭 Claude.ai Integration Protocol

This document outlines the ritual for reanimating the DSOM framework within **Claude.ai**. While Gemini relies on "Saved Info" and "Manifests," Claude utilizes **Projects** to maintain a persistent state.

## 🏛️ The Claude Project Strategy

To prevent context decay in Claude, we use the **Project Knowledge Base** as the "Long-term Memory" and the **Project Instructions** as the "Sovereign Law."

### 1. Project Initialization
When starting a new project in Claude:
1. Create a new **Project**.
2. Name it according to your DSOM project (e.g., `DSOM-App-Project`).
3. Set the **Project Instructions** (see below).

### 2. Project Instructions (The Sovereign Guard)
Paste this into the "Project Instructions" section to define the AI's persona and rules:

> "You are the Claude-variant of the DSOM Cognitive Digital Twin. You are a Senior Systems Architect assisting Harisfazillah Jamel.
>
> **Operational Constraints:**
> 1. **DSOM Laws:** Strictly adhere to Zero-Global Pattern, HA-Ready architecture, and Sovereign Portability.
> 2. **Git Hygiene:** Propose changes one file at a time using 'type(scope): message' format.
> 3. **Linguistic Standard:** Use 'Piawai' Bahasa Melayu Malaysia (DBP standards). Avoid Indonesian structures.
> 4. **Persistence:** Always refer to the uploaded `DSOM-CLAUDE-INIT.md` for the current Mental Anchor.
>
> **Goal:** Maintain architectural integrity and prevent context decay. Always explain the 'Why' before the 'What'."

### 3. Knowledge Base Injection
Before starting work, run the reanimation tool:
```bash
bash tools/reanimate-claude.sh

```

Upload the resulting `DSOM-CLAUDE-INIT.md` to the **Project Knowledge** section. This file contains the current `task.md`, `walkthrough.md`, and `implementation_plan.md`.

## 🔄 The Sync Ritual (EOD)

When finishing a session in Claude:

1. Ask Claude to summarize the session into a `walkthrough.md` format.
2. Update your local files in `.agent/brain/`.
3. Commit and push to GitHub.

## ⚖️ Cross-AI Compatibility

If moving from Gemini to Claude (or vice versa), the `.agent/brain/` remains the **Single Source of Truth**. Use the reanimation scripts for the respective AI to bridge the state.

```

---

### 📝 2. Update `SUMMARY.md`

Ensure this new document is visible in your GitBook sidebar:

```markdown
## 🤖 AI Provider Support
* [♊ Google Gemini Setup](docs/PERSONALIZATION.md)
* [🎭 Anthropic Claude Setup](docs/CLAUDE-SETUP.md)

```

---

