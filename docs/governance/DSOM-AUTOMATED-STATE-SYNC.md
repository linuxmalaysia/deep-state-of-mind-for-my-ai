---
okf_version: 0.1
type: documentation
title: DSOM Automated State Sync
timestamp: "2026-07-27T00:00:00Z"
topics: ["compaction", "state", "action", "github"]
description: "Governance rules for Semantic Compaction via GitHub Actions."
---

# DSOM Automated State Sync

## 1. Vectorized Memory Tiering

Instead of pushing an entire project history into every prompt, DSOM categorizes information into distinct operational layers:
*   **Active Layer**: Houses only the immediate, high-priority variables for the current task.
*   **Compressed Layer**: Stores foundational rules and past decisions as dense, key-value indices (`.agents/brain/current_state.dsom`).
*   **Archival Layer**: Offloads long-term data to the Git history and Sovereign Markdown Palace.

## 2. Semantic Compaction (Token Distillation)

DSOM applies a "distillation loop" using an automated GitHub Action. 
When a Pull Request is merged, `.github/workflows/dsom-pr-sync.yml` triggers `.github/scripts/action_update_dsom.py`.
This script calls an LLM (e.g. OpenAI) to review the PR diff and update `.agents/brain/current_state.dsom` strictly in OKF v0.1 format, eliminating redundant conversational fluff and appending only critical architectural decisions.

## 3. Configuration

- Ensure the `OPENAI_API_KEY` secret is available to the GitHub Action.
- The state is persisted in `.agents/brain/current_state.dsom`.


---
*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-08-14*
*Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*
