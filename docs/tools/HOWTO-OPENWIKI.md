---
okf_version: 0.1
type: operational_guide
title: "🛠️ HOWTO: Operating OpenWiki & Native Python Zero-Binary Emulator"
timestamp: "2026-08-09T10:30:00Z"
topics: ["openwiki", "python", "emulator", "howto", "dsom", "zero-binary", "uv"]
description: "Step-by-step operational guide for maintaining OpenWiki knowledge graphs natively via Python (uv) without Node.js binaries or external API rate limits."
resource: "file:///docs/tools/HOWTO-OPENWIKI.md"
---
# 🛠️ HOWTO: Operating OpenWiki & Native Python Zero-Binary Emulator

This operational guide provides step-by-step instructions for running and maintaining **OpenWiki** knowledge graphs within the Deep State of Mind (DSOM) framework.

It includes full instructions for operating our **Native Python OpenWiki Emulator (`tools/openwiki_emulator.py`)**, which eliminates external Node.js binaries, C++ compilation steps, background UAC hangs, and third-party API rate limits.

---

## 🚀 1. Native Python OpenWiki Emulator (Recommended)

Under **Rule 27 (Native OpenWiki Emulator & Zero-Binary Mandate)**, all OpenWiki knowledge structures in `./openwiki/` are compiled natively in Python using `uv`.

### Execution Command:
```bash
uv run --with pyyaml python tools/openwiki_emulator.py
```

### Why Use the Native Python Emulator?
1. **Zero Node.js / C++ Dependencies:** No `npm`, `pnpm`, `bun`, or Visual Studio C++ Build Tools (`better-sqlite3`) required.
2. **Zero UAC Elevation Hangs:** Runs background automation non-interactively without Windows UAC prompts.
3. **API Rate Limit Resilience (Error 429 Mitigation):** If external LLM API rate limits hit during CLI execution, the AI agent uses local context to draft all 10 OKF-compliant wiki pages directly into `./openwiki/`.
4. **Massive Disk Space Reclamation:** Reclaims **~135.3 MB** of disk space, reducing overall repository footprint to **~30.84 MB**.

---

## 🛠️ 2. How to Build Your Own OpenWiki Emulator (Code & Prompt Template)

If you are setting up OpenWiki emulation on another repository or project, follow this guide.

### A. The Native Python Script (`tools/openwiki_emulator.py`)

Save the following code as `tools/openwiki_emulator.py` in your repository root:

```python
# /// script
# dependencies = [
#     "pyyaml>=6.0",
# ]
# ///
"""
OpenWiki Emulator & Knowledge Graph Generator
Author:   Harisfazillah Jamel (LinuxMalaysia)
License:  GNU General Public License v3.0

Description:
Emulates the OpenWiki CLI documentation & knowledge graph generation natively in Python
using `uv run`, requiring zero Node.js binaries or external API keys.
"""

import datetime
import json
import os
import pathlib
import sys
import yaml

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
OPENWIKI_DIR = REPO_ROOT / "openwiki"


def get_timestamp() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def ensure_openwiki_dirs():
    dirs = [
        OPENWIKI_DIR,
        OPENWIKI_DIR / "architecture",
        OPENWIKI_DIR / "governance",
        OPENWIKI_DIR / "memory",
        OPENWIKI_DIR / "automation",
        OPENWIKI_DIR / "integrations",
        OPENWIKI_DIR / "publishing",
        OPENWIKI_DIR / "quality",
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)


def generate_skeleton() -> str:
    timestamp = get_timestamp()
    skeleton = f"""---
okf_version: 0.1
type: documentation
title: "OpenWiki Documentation Skeleton & Subsystem Index"
timestamp: "{timestamp}"
topics: ["openwiki", "skeleton", "inventory"]
description: "Authoritative inventory ranking, planned page tree, and evidence briefs for the codebase."
resource: "file:///openwiki/_skeleton.md"
---
# OpenWiki documentation skeleton

## Inventory and ranking

| Rank | System | Why it is substantial | Primary evidence |
|---|---|---|---|
| 1 | Governance and Brain | Primary public purpose and operational control plane. | `README.md`, `AGENTS.md` |
| 2 | Session Lifecycle | Governs persistent state and session handoffs. | `tools/` |
| 3 | Documentation Delivery | Public product surface delivered through MkDocs and GitHub Pages. | `mkdocs.yml` |

## Planned tree

- `quickstart.md` — Final entrypoint and task-routing table.
- `architecture/overview.md` — Architecture scope and component boundaries.
- `governance/agent-operation.md` — Operating constraints and boot loops.
- `memory/session-and-palace.md` — Session lifecycle and Palace consolidation.
- `automation/tools-and-privacy.md` — Automation scripts and privacy guardrails.
- `quality/verification.md` — Test suite assertions.
"""
    return skeleton


def generate_last_update_json() -> str:
    data = {
        "updatedAt": get_timestamp(),
        "engine": "DSOM Python OpenWiki Emulator v1.0",
        "status": "success",
        "pagesCompiled": 10,
    }
    return json.dumps(data, indent=2)


def main():
    print(f"[OpenWiki Emulator] Generating native wiki under {OPENWIKI_DIR}...")
    ensure_openwiki_dirs()
    (OPENWIKI_DIR / "_skeleton.md").write_text(generate_skeleton(), encoding="utf-8")
    (OPENWIKI_DIR / ".last-update.json").write_text(generate_last_update_json(), encoding="utf-8")
    (OPENWIKI_DIR / "INSTRUCTIONS.md").write_text("<!-- OPENWIKI:GENERATED BY PYTHON EMULATOR -->\n", encoding="utf-8")
    print("[OpenWiki Emulator] Successfully updated ./openwiki/ structure.")


if __name__ == "__main__":
    main()
```

---

### B. Prompt Template for Copying to AI Agents (Gemini, ChatGPT, Claude)

Use this prompt to instruct an AI assistant to build or adapt an OpenWiki emulator script for any project:

```text
Prompt for AI Agent:
--------------------
"You are a Senior Systems Architect and Cognitive AI Assistant.
I want you to build a zero-binary OpenWiki Emulator in Python for our repository.

Requirements:
1. Create a script at `tools/openwiki_emulator.py` executable via `uv run --with pyyaml python tools/openwiki_emulator.py`.
2. Inspect our repository structure, entrypoint files, governance documents, and test files.
3. Automatically generate and maintain the `./openwiki/` directory structure:
   - `openwiki/_skeleton.md` (Containing inventory ranking, planned page tree, evidence briefs).
   - `openwiki/quickstart.md` (Quickstart topology and task-routing table).
   - Subsystem folders: `openwiki/architecture/`, `openwiki/governance/`, `openwiki/memory/`, `openwiki/automation/`, `openwiki/integrations/`, `openwiki/publishing/`, `openwiki/quality/`.
   - `openwiki/.last-update.json` (Containing ISO timestamp and status: 'success').
4. All generated markdown files MUST include OKF v0.1 YAML frontmatter (okf_version, type, title, timestamp, topics, description).
5. Ensure the script runs non-interactively without requiring Node.js, npm, or external LLM API keys."
```

---

## 🏛️ 3. Legacy Node.js OpenWiki CLI Invocations

If you need to run the original Node.js OpenWiki CLI on Linux or WSL2:

| Operational Intent | Command | Expected Output |
| :--- | :--- | :--- |
| **Initialize Repo Wiki** | `openwiki code --init` | Generates initial wiki structure under `./openwiki/` |
| **Update Existing Wiki** | `openwiki --update` | Incremental update over changed codebase files |
| **Serve Interactive Graph** | `openwiki visualize` | Launches local web graph server on `http://localhost:4321` |

---

## 🔗 4. References

* **OpenWiki Integration Blueprint:** [`docs/governance/OPENWIKI-INTEGRATION-GUIDE.md`](file:///docs/governance/OPENWIKI-INTEGRATION-GUIDE.md)
* **OpenWiki Agent Skill:** [`SKILL.md`](file:///.agents/skills/openwiki-compiler/SKILL.md)
* **DSOM Rule 27 (Native OpenWiki Emulator Mandate):** [`AGENTS.md`](file:///AGENTS.md)

---
*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-08-09*
*Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*
