---
okf_version: 0.1
type: standard_operating_procedure
title: "SOP: Knowledge-First Discovery & Context Preservation Protocol"
description: "SOP detailing how AI agents and human operators leverage OKF YAML frontmatter (topics, description) in .agents/brain/ and docs/ to perform fast local discovery before terminal execution."
timestamp: 2026-07-26T07:07:00Z
topics: [okf, discovery, context-management, brain, dsom, SOP]
---

# 📚 SOP: Local Knowledge-First Discovery & OKF Context Protocol

## 1. Executive Intent
To prevent unnecessary exploratory terminal commands, token window exhaustion, and context loss during agentic sessions, AI agents must adhere to the **Local Knowledge-First Protocol**. All project facts, architectural specifications, inventory mappings, and operational rules are indexed via **OKF v0.1 YAML Frontmatter** in `.agents/brain/` and `docs/`.

---

## 2. Standard Operating Procedure (4-Step Discovery Flow)

```
[ Step 1: User Request ]
         │
         ▼
[ Step 2: Local OKF Search ] ──▶ grep_search on .agents/brain/ & docs/ (topics: / description:)
         │
         ▼
[ Step 3: Local Context Inspection ] ──▶ view_file line ranges on targeted .md files
         │
         ▼
[ Step 4: Terminal Execution ] (ONLY if live runtime state or deployment change is needed)
```

### Step 1: Local Frontmatter & Metadata Search (`grep_search`)
Before issuing any exploratory terminal command (e.g. `uv run`, `powershell`, `bash`, `ansible`):
1. Search local OKF frontmatter for relevant `topics:` or `description:` keywords:
   ```bash
   grep_search Query="topics: \[ansible" SearchPath="docs/"
   ```
2. Search `.agents/brain/` checkpoint summaries and active context manifests.

### Step 2: Targeted File Viewing (`view_file`)
Once the relevant document is located via OKF frontmatter:
- Read specific line ranges using `view_file` to preserve token efficiency (Rule 10).

### Step 3: Terminal Execution Gate
Terminal commands against the T1 Operator Node or T2 Control Node are authorized **ONLY** when:
- Applying code/configuration updates to production.
- Fetching live runtime data or logs that cannot be answered by local documentation.

---

## 3. Mandatory Rules Reference
- **Rule 6 (OKF Topics)**: All `.md` files must open on line 1 with `---` and contain `topics: [3-5 keywords]`.
- **Rule 12 (Metadata-First Discovery)**: Always query `topics:` and `description:` metadata before reading full file bodies.
- **Rule 20 (Local Knowledge-First Mandate)**: Search `.agents/brain/` and `docs/` locally before terminal execution.

---
*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-07-26*
*Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*
