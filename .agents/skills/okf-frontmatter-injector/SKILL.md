---
okf_version: 0.1
type: agent_skill
title: okf-frontmatter-injector
timestamp: "2026-08-20T23:30:00Z"
description: "Scans a target directory and automatically injects OKF (v0.1/v0.2) YAML frontmatter into any Markdown files missing it."
topics: ["okf", "frontmatter", "yaml", "compliance", "markdown"]
---
# 💉 OKF Frontmatter Injector

## When to use this skill
Use this skill when the user asks to ensure documentation is OKF (Open Knowledge Format) compliant, or when importing, generating, or modifying Markdown files that lack standard YAML frontmatter headers.

## Instructions
1. This skill utilizes native Python tools (`tools/apply_okf_frontmatter.py`) and the skill helper script `scripts/apply_okf.py`.
2. Ask the user for the target directory to scan (default is the project root `.`).
3. Execute the compliance script using `uv`:
   ```bash
   # Primary execution via tools/apply_okf_frontmatter.py
   uv run python tools/apply_okf_frontmatter.py <TARGET_DIRECTORY>

   # Or invoke the skill mirror script directly
   python .agents/skills/okf-frontmatter-injector/scripts/apply_okf.py <TARGET_DIRECTORY>
   ```
4. The script automatically skips files that already possess valid frontmatter. It categorises files dynamically based on folder structure (`agent_skill`, `governance_protocol`, `architecture_concept`, etc.).
5. Run `python .agents/skills/dsom-signature-injector/scripts/inject.py <TARGET_DIRECTORY>` to ensure all updated Markdown documents carry the GPL v3.0 signature footer.
6. Inform the user of the total number of files scanned and modified based on output telemetry.


---
*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-08-20*
*Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*
