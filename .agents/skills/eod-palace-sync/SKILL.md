---
name: eod-palace-sync
version: "1.0.0"
description: "The Hibernation (End of Day) ritual to externalise memory into the Palace and push to Git."
author: "Harisfazillah Jamel (LinuxMalaysia)"
license: "GPL-3.0-or-later"
okf_version: 0.2
type: agent_skill
topics: ["eod", "palace", "sync", "git", "ritual"]
status: stable
stale_after: "2027-10-01"
title: eod-palace-sync
timestamp: "2026-06-19T14:00:00Z"
resource: "/.agents/skills/eod-palace-sync/SKILL.md"
sources: [{author: "Harisfazillah Jamel (LinuxMalaysia)", id: dsom-core-spec, resource: "/docs/governance/DSOM-TRI-PHASIC-COGNITIVE-ARCHITECTURE.md", title: "Deep State of Mind (DSOM) Governance Architecture", type: architecture_spec, url: "https://github.com/linuxmalaysia/deep-state-of-mind-for-my-ai/blob/main/docs/governance/DSOM-TRI-PHASIC-COGNITIVE-ARCHITECTURE.md"}, {author: Google Cloud Platform, id: google-okf-v02-spec, resource: "https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md", title: "Google Cloud Open Knowledge Format (OKF) v0.2 Specification", type: external_spec, url: "https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md"}]
spec_version: "0.2"
---
# 🌙 EOD Palace Sync (Hibernation)

## When to use this skill
Use this skill when the user declares "End of Day" (EOD), "Save memory", or requests to update the palace and hibernate the agent.

## Instructions
1. **Walkthrough Update:** Append the day's major accomplishments, tested commands, and E2E results to `.agents/brain/walkthrough.md`.
2. **Anchor Creation:** Update `.agents/brain/checkpoint_summary.txt` with a clear, concise "[MENTAL ANCHOR]" for the next agent to resume from.
3. **Palace Sync:** Update any modified architectural rules inside the specific `closet.md` spatial rooms.
4. **Memory Dump Generation:** Compile a comprehensive checkpoint summary documenting project details, instructions, frameworks, and active phases.
5. Save this summary directly to `.agents/brain/checkpoint_summary.txt`.
6. Ensure `HISTORY.md`, `CHANGELOG.md`, `README.md`, and `.agents/brain/task.md` are up to date.
7. Instruct the user to execute the final git commit and push via the EOD script:
   ```powershell
   # On Windows
   .\tools\eod-palace.ps1
   ```
   ```bash
   # On Linux/macOS
   bash tools/eod-palace.sh
   ```
8. Confirm to the user that state has been fully externalized and archived.

## Architecture & Implementation
If `tools/eod-palace.ps1` or `tools/eod-palace.sh` are missing, agents must reconstruct them with the following logic:
1. **Validation:** Check that `.agents/brain/task.md` has completed tasks (`[x]`), and `.agents/brain/walkthrough.md` contains today's `yyyy-MM-dd` anchor.
2. **Summary Verification:** Check that `.agents/brain/checkpoint_summary.txt` exists. If it does not, output a massive terminal warning instructing the user to prompt the AI to generate it.
3. **Palace Sync:** Run `.\tools\palace-sync.ps1` to generate any update proposals.
4. **Staging:** `git add` the core artifacts: `task.md`, `walkthrough.md`, `palace_registry.md`, `checkpoint_summary.txt`, and `implementation_plan.md`.
5. **Commit & Push:** Execute `git commit -m "eod: <contents of checkpoint_summary>"` and `git push origin main`.
*(Note: On Linux/macOS, `eod-palace.sh` simply wraps `ansible-playbook playbooks/dsom/eod-palace.yml` with `ANSIBLE_NOCOWS=1`)*


---
*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-06-19*
*Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*
