---
okf_version: "0.1"
type: "documentation"
title: "Sovereign Automation Tools & Privacy Guardian Boundaries"
timestamp: "2026-08-10T12:54:57Z"
topics: ["openwiki", "automation", "tools", "privacy", "guardian"]
description: "Native Bash/PowerShell ritual tools, Privacy Guardian, onboarding/reset boundaries."
---
# Sovereign Automation Tools & Privacy Guardian Boundaries

Idempotent local script wrappers located in `tools/` handle multi-platform environment management while enforcing strict privacy filters.

## ⚙️ Core Automation Ritual Tools

All daily rituals are wrapped in unified PowerShell (`.ps1`) and Bash (`.sh`) scripts that run interactively or headlessly:

- `reanimate.sh` — Bootstraps the active session and loads files listed in the context manifest.
- `hibernation.sh` — Executes preflight checks, commits active changes, and prepares for hibernation.
- `git-ritual.sh` — Automates safe, non-interactive stashing, rebasing, and pushing across multiple remotes.
- `diagnostic.sh` — Verifies the physical health of brain files, frontmatter compliance, and system tools.

## 🛡️ Privacy Guardian Boundaries

The **Privacy Guardian (`tools/privacy-guardian.sh`)** acts as an inline data-leak prevention layer. Before staging any documentation or logs, it scans the active manifest for:
- Exposed credentials, tokens, or private API keys.
- Production IP addresses or sensitive database passwords.

Any flagged files are immediately quarantined, and Git actions are blocked until the sensitive data is successfully externalised.
