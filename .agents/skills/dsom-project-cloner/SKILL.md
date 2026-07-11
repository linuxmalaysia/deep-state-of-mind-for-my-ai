---
name: dsom-project-cloner
description: Scaffolds a new DSOM project by copying the Sovereign Engine, Intelligence Payload, Governance, and Ritual Scripts from the baseline repository to a user-specified target path.
okf_version: 0.1
type: skill
title: "DSOM Project Cloner Skill"
timestamp: 2026-07-04T11:15:00Z
---

# 🏗️ DSOM Project Cloner Skill

## When to use this skill
Use this skill when the user asks to create, clone, scaffold, or bootstrap a **new** DSOM project based on the current baseline repository (e.g., "Create a new project at D:\Projects\my-new-app").

## Prerequisites
- The user must provide the **absolute path** to the new target repository. Ask for it if not provided.

## Instructions

1. **Verify Target Path:** Ensure you have the absolute path for the new target repository from the user.
2. **Establish Directories:** Use your terminal execution tools (`run_command`) to create the mandatory folder structures in the target path:
   - `<target_path>/.agents/brain/wings`
   - `<target_path>/.agents/skills`
   - `<target_path>/docs/agent-configs`
   - `<target_path>/docs/governance`
   - `<target_path>/tools`
3. **Copy the Four Pillars:** Use your terminal execution tools (`run_command`) to copy the assets from the CURRENT repository (baseline) to the TARGET repository:
   - **Pillar A (The Engine):** Copy `.agents/AGENTS.md` to `<target_path>/.agents/`
   - **Pillar B (The Intelligence Payload):** Recursively copy all contents of `.agents/skills/` to `<target_path>/.agents/skills/`
   - **Pillar C (Governance & Configuration):**
     - Recursively copy `docs/agent-configs/` to `<target_path>/docs/agent-configs/`
     - Recursively copy `docs/governance/` to `<target_path>/docs/governance/`
     - Copy `docs/AI-AGENT-SKILLS-GUIDE.md` to `<target_path>/docs/`
     - Copy all `docs/HOWTO-*.md` files to `<target_path>/docs/`
   - **Pillar D (Ritual Scripts):** Recursively copy `tools/` to `<target_path>/tools/`
4. **Persona Injection Check:** Ask the user if they wish to automatically inject their persona using the `persona-injector` skill for the new project.
5. **Finalization:** Output a success message to the user, providing them with the initialization commands for their new workspace:
   - `bash tools/reanimate.sh` or `.\tools\reanimate.ps1`
   - `git add .`
   - `git commit -m "chore(dsom): scaffold genesis dsom architecture and AI skills"`


---
*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-07-04*
*Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*
