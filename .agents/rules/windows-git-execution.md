---
okf_version: 0.1
type: rule
title: "Windows Git Execution Guardrail"
timestamp: "2026-08-18T06:00:00Z"
description: "Forces all background Git commands to fail fast instead of hanging on credential prompts."
topics: ["git", "windows", "execution", "guardrail"]
---

# Windows Git Execution Guardrail

When executing `git` commands (such as `git push`, `git fetch`, or `git pull`) via the terminal on a Windows environment, you MUST prepend the following environment variable exports to the command to prevent the Git Credential Manager (GCM) from spawning blocking GUI prompts.

For PowerShell commands, always format your execution as follows:

```powershell
$env:GIT_TERMINAL_PROMPT="0"; $env:GCM_INTERACTIVE="never"; git push ...
```

If the command fails due to missing authentication, do not attempt to bypass it. Instead, kill any stuck background tasks and instruct the user to run the command manually in their interactive terminal.
