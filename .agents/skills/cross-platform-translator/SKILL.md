---
name: cross-platform-translator
description: Analyzes a Windows PowerShell (.ps1) or Linux Bash (.sh) script and automatically generates its functional equivalent in the other shell language, enforcing the Cross-Platform Mandate.
okf_version: 0.1
---

# 🔄 Cross-Platform Translator Skill

## When to use this skill
Use this skill when a new automation script is created in one shell language, and the workspace Constitution requires its equivalent to be generated for cross-platform compliance.

## Instructions
1. **Analyze Source:** Read the source script (e.g., `tools/myscript.ps1`) to understand its exact logical flow, variable assignments, standard output formats, and error handling.
2. **Determine Target:** If the source is `.ps1`, the target is `.sh` (Bash). If the source is `.sh`, the target is `.ps1` (PowerShell).
3. **Translation Rules:**
   - **Banners:** Preserve the exact DSOM banner text and colors (using ANSI escape codes in Bash, or `Write-Host -ForegroundColor` in PowerShell).
   - **Paths:** Ensure path separators are idiomatic (use `/` or `\` appropriately, though PowerShell often accepts `/`).
   - **Error Handling:** Map PowerShell's `try/catch` or `$ErrorActionPreference = "Stop"` to Bash's `set -e` or specific `if ! command; then ... fi` checks.
   - **Dependencies:** If the script calls another script, ensure it calls the correct extension for its platform (e.g., a `.ps1` script should call `reanimate.ps1`, not `reanimate.sh`).
4. **Output Generation:** Write the translated script to the target file.
5. **Update Documentation:** If the script is documented in `docs/tools/`, ensure the documentation accurately lists both the `.ps1` and `.sh` file names.
