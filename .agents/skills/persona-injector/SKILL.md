---
name: persona-injector
version: "1.0.0"
description: "Guides a user to define their Sovereign Persona and safely injects it into the agent's core AGENTS.md rulebook."
author: "Harisfazillah Jamel (LinuxMalaysia)"
license: "GPL-3.0-or-later"
okf_version: 0.2
type: agent_skill
topics: ["persona", "profile", "identity", "dsom", "agent"]
status: stable
stale_after: "2027-10-01"
title: persona-injector
timestamp: "2026-07-04T10:00:00Z"
resource: "/.agents/skills/persona-injector/SKILL.md"
sources: [{author: "Harisfazillah Jamel (LinuxMalaysia)", id: dsom-core-spec, resource: "/docs/governance/DSOM-TRI-PHASIC-COGNITIVE-ARCHITECTURE.md", title: "Deep State of Mind (DSOM) Governance Architecture", type: architecture_spec, url: "https://github.com/linuxmalaysia/deep-state-of-mind-for-my-ai/blob/main/docs/governance/DSOM-TRI-PHASIC-COGNITIVE-ARCHITECTURE.md"}, {author: Google Cloud Platform, id: google-okf-v02-spec, resource: "https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md", title: "Google Cloud Open Knowledge Format (OKF) v0.2 Specification", type: external_spec, url: "https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md"}]
spec_version: "0.2"
---
# 🎭 Persona Injector

## When to use this skill
Use this skill when a user says "I want to inject my persona", "make the AI act like me", or "setup my identity matrix".

## Instructions
1. **Fetch Template:** Read the `docs/agent-configs/SOVEREIGN-PERSONA-TEMPLATE.md` file using your file reading tools.
2. **Interview User:** Present the categories from the template to the user (e.g., Identity, Core Profile, Writing Style, Architectural Principles). Ask them to provide their specifics either all at once or step-by-step.
3. **Format Matrix:** Once the user has provided their details, format the data exactly as defined in the `<RULE[PERSONA.md]>` OKF block from the template.
4. **Inject Rule:** Use your file editing tools to append this formatted block to the bottom of `.agents/AGENTS.md`.
5. **Verify:** Confirm to the user that the AI operating in this workspace has now permanently inherited their identity, constraints, and linguistic DNA.


---
*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-07-04*
*Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*
