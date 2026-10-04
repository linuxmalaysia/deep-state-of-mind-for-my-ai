---
okf_version: 0.2
type: rule
title: Windows Git Execution Guardrail
timestamp: "2026-08-18T06:00:00Z"
topics: ["git", "windows", "execution", "guardrail"]
resource: "/.agents/rules/windows-git-execution.md"
sources: [{author: Harisfazillah Jamel (LinuxMalaysia), id: dsom-core-spec, resource: /docs/governance/DSOM-TRI-PHASIC-COGNITIVE-ARCHITECTURE.md,
  title: Deep State of Mind (DSOM) Governance Architecture, type: architecture_spec}, {author: Google Cloud Platform, id: google-okf-v02-spec, resource: 'https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md',
  title: Google Cloud Open Knowledge Format (OKF) v0.2 Specification, type: external_spec}]
spec_version: "0.2"
description: "Forces all background Git commands to fail fast instead of hanging on credential prompts."
---
# Windows Git Execution Guardrail

When executing `git` commands (such as `git push`, `git fetch`, or `git pull`) via the terminal on a Windows environment, you MUST prepend the following environment variable exports to the command to prevent the Git Credential Manager (GCM) from spawning blocking GUI prompts.

For PowerShell commands, always format your execution as follows:

```powershell
$env:GIT_TERMINAL_PROMPT="0"; $env:GCM_INTERACTIVE="never"; git push ...
```

If the command fails due to missing authentication, do not attempt to bypass it. Instead, kill any stuck background tasks and instruct the user to run the command manually in their interactive terminal.
