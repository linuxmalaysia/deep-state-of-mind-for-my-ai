---
name: dsom-state-sync
version: "1.0.0"
description: "Executes Semantic Compaction locally by analyzing a Git diff and updating current_state.dsom using OpenAI."
topics: ["compaction", "state", "sync", "openai", "dsom"]
author: "Harisfazillah Jamel (LinuxMalaysia)"
license: "GPL-3.0-or-later"
okf_version: 0.2
type: skill
status: stable
stale_after: "2027-10-01"
title: DSOM State Sync Skill
timestamp: "2026-07-27T00:00:00Z"
resource: "/.agents/skills/dsom-state-sync/SKILL.md"
sources: [{author: "Harisfazillah Jamel (LinuxMalaysia)", id: dsom-core-spec, resource: "/docs/governance/DSOM-TRI-PHASIC-COGNITIVE-ARCHITECTURE.md", title: "Deep State of Mind (DSOM) Governance Architecture", type: architecture_spec, url: "https://github.com/linuxmalaysia/deep-state-of-mind-for-my-ai/blob/main/docs/governance/DSOM-TRI-PHASIC-COGNITIVE-ARCHITECTURE.md"}, {author: Google Cloud Platform, id: google-okf-v02-spec, resource: "https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md", title: "Google Cloud Open Knowledge Format (OKF) v0.2 Specification", type: external_spec, url: "https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md"}]
spec_version: "0.2"
---
# DSOM State Sync Skill

## Purpose
This skill allows AI agents to manually execute the **Semantic Compaction** process outside of the standard GitHub Actions PR workflow. It analyzes a provided diff file and uses an LLM to condense and append significant architectural changes into the project's compressed memory tier (`.agents/brain/current_state.dsom`).

## Prerequisites
1. **Python & `uv`**: The `uv` package manager must be available on the system.
2. **Gemini API Key (Optional)**: The environment variable `GEMINI_API_KEY` or `GOOGLE_API_KEY` can be set in the executing terminal to leverage the Gemini AI API for compaction. If neither credential is set, the system automatically falls back to a zero-API local Semantic Compaction engine.
3. **Diff File**: A valid Git diff file or text file containing changes must be prepared.

## Execution Flow

When tasked with running the state sync locally, execute the following terminal command (ensure you replace `<diff_file>` with the actual path to your diff):

```bash
uv run --with requests==2.34.2 --with pyyaml==6.0.3 .github/scripts/action_update_dsom.py <diff_file> .agents/brain/current_state.dsom
```

### Execution Rules
1. **Never write the API key to disk**: If the API key is not present in the environment, instruct the human operator to export it manually in their terminal session before proceeding.
2. **Review before execution**: Generate the diff file locally first (e.g., `git diff > local.diff`) and verify its contents to prevent bloating the compaction prompt with irrelevant artifact changes.
3. **Verify Timestamp**: After successful execution, check `.agents/brain/current_state.dsom` to ensure the `timestamp` in the OKF frontmatter was correctly updated.

---
*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-07-27*
*Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*
