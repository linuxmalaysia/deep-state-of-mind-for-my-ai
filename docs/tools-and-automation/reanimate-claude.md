---
okf_version: 0.2
type: automation_tool
title: "🤖 Claude Reanimation (reanimate-claude.sh)"
timestamp: "2026-07-04T09:40:04Z"
topics: ["dsom", "automation", "tool"]
resource: "file:///docs/tools-and-automation/reanimate-claude.md"
sources: [{author: Harisfazillah Jamel (LinuxMalaysia), id: dsom-core-spec, resource: /docs/governance/DSOM-TRI-PHASIC-COGNITIVE-ARCHITECTURE.md,
  title: Deep State of Mind (DSOM) Governance Architecture, type: architecture_spec}, {author: Google Cloud Platform, id: google-okf-v02-spec, resource: 'https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md',
  title: Google Cloud Open Knowledge Format (OKF) v0.2 Specification, type: external_spec}]
spec_version: "0.2"
description: "OKF-compliant documentation for reanimate-claude.md."
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
