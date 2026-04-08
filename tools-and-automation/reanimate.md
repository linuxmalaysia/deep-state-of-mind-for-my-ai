# 🌅 Reanimation Engine (reanimate.sh)

> **"Wake up, Neo."** - Ingesting the Project State.

## 1. 🏛️ Purpose

**Version:** v1.5
**Description:** The heart of the Start-of-Day (SOD) ritual. It aggregates ALL core artifacts (`README`, `AI-MASTER-PROTOCOL`, `task.md`, etc.), file topology, and git history into a single text manifest (`sod_manifest.txt`) that brings the AI up to speed instantly.

## 2. 🛡️ Safety Mechanisms

| Mechanism | Status | Description |
| :--- | :--- | :--- |
| **Interactive Input** | ✅ Active | Captures multi-line manual summaries via `cat` and `CTRL+D`. |
| **Sunday Audit** | ✅ Active | Auto-detects if today is Sunday and prompts for Weekly Audit. |
| **System Telemetry** | ✅ Active | Injects OS, Shell, and Date info for context. |
| **Exit-on-Error** | ✅ Active | `set -e` prevents partial manifests. |

## 3. ⚙️ Usage

```bash
./tools/reanimate.sh
```

## 4. 🧠 Logic Flow

1. **Manual Injection:** Prompts user for "EOD Summary" or "Master Prompt" additions.
2. **Context Aggregation:** Concatenates:
    * `README.md`
    * `docs/AI-MASTER-PROTOCOL.md`
    * `.agent/brain/*` (Task, Walkthrough, Plan)
    * `git ls-tree` (Project Structure)
    * `git log` (Recent History)
3. **Governance Warning:** Checks Day-of-Week. Triggers Sunday Audit alert if applicable.
4. **Output:** Generates `sod_manifest_[DATE].txt` in root.

## 5. 📝 Extracted Comments
>
> "Aggregates ALL core DSOM artifacts. Features an interactive multi-line input for EOD summaries."
