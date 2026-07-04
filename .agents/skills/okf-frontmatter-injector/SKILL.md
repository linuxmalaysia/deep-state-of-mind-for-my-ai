---
okf_version: 0.1
type: agent_skill
title: okf-frontmatter-injector
description: Scans a target directory and automatically injects OKF v0.1 YAML frontmatter into any Markdown files missing it.
timestamp: 2026-07-04T10:00:00Z
---

# 💉 OKF Frontmatter Injector

## When to use this skill
Use this skill when the user asks to ensure documentation is OKF (Open Knowledge Format) compliant, or when importing new markdown files that lack standard YAML frontmatter headers.

## Instructions
1. This skill utilises a Python script embedded in `scripts/apply_okf.py`.
2. Ask the user for the target directory to scan (default is the project root `.`).
3. Execute the script using your terminal tools:
   ```bash
   python .agents/skills/okf-frontmatter-injector/scripts/apply_okf.py <TARGET_DIRECTORY>
   ```
4. The script will automatically skip files that already possess frontmatter. It categorizes files dynamically based on their folder structure (e.g. `agent_skill`, `governance_protocol`, etc.).
5. Inform the user of the total number of files modified based on the script's output.
