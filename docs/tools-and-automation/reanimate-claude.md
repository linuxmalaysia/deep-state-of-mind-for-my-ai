---
okf_version: 0.1
type: automation_tool
title: "🤖 Claude Reanimation (reanimate-claude.sh)"
description: "OKF-compliant documentation for reanimate-claude.md."
resource: "file:///tools-and-automation/reanimate-claude.md"
timestamp: 2026-07-04T09:40:04Z
---
# 🤖 Claude Reanimation (reanimate-claude.sh)

> **"Hello, Claude."** - Provider-Specific Context Injection.

## 1. 🏛️ Purpose

**Version:** v1.0
**Description:** A lightweight variant of the Reanimation Engine specifically optimized for Claude.ai's "Project Knowledge" file size limits. It generates a cleaner, markdown-heavy context file.

## 2. 🛡️ Safety Mechanisms

| Mechanism | Status | Description |
| :--- | :--- | :--- |
| **Fail-Safe Cat** | ✅ Active | Uses `|| echo` fallback if Master Protocol is missing. |
| **Exit-on-Error** | ✅ Active | `set -e` injected. |
| **Fixed Output** | ✅ Active | Targets `DSOM-CLAUDE-INIT.md`. |

## 3. ⚙️ Usage

```bash
./tools/reanimate-claude.sh
```

## 4. 🧠 Logic Flow

1. **Header Generation:** Appends Date and Title.
2. **Protocol Injection:** Injects `AI-MASTER-PROTOCOL.md`.
3. **Brain Dump:** Injects Task, Walkthrough, and Implementation Plan.
4. **Finalization:** Writes to `DSOM-CLAUDE-INIT.md`.

## 5. 📝 Extracted Comments
>
> "Optimized for Claude.ai Project Knowledge Base."


---
*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-07-04*
*Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*
