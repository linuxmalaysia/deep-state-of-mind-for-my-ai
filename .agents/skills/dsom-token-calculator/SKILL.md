---
name: dsom-token-calculator
version: "1.0.0"
description: "Calculates token counts via tiktoken in isolated uv Python runspaces."
topics: ["tokens", "tiktoken", "performance", "byte-cap", "context"]
author: "Harisfazillah Jamel (LinuxMalaysia)"
license: "GPL-3.0-or-later"
okf_version: 0.2
type: procedural_skill
status: stable
stale_after: "2027-10-01"
title: "Procedural Specification: DSOM Token Calculator"
timestamp: "2026-07-18T14:52:39Z"
resource: "/.agents/skills/dsom-token-calculator/SKILL.md"
sources: [{author: "Harisfazillah Jamel (LinuxMalaysia)", id: dsom-core-spec, resource: "/docs/governance/DSOM-TRI-PHASIC-COGNITIVE-ARCHITECTURE.md", title: "Deep State of Mind (DSOM) Governance Architecture", type: architecture_spec, url: "https://github.com/linuxmalaysia/deep-state-of-mind-for-my-ai/blob/main/docs/governance/DSOM-TRI-PHASIC-COGNITIVE-ARCHITECTURE.md"}, {author: Google Cloud Platform, id: google-okf-v02-spec, resource: "https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md", title: "Google Cloud Open Knowledge Format (OKF) v0.2 Specification", type: external_spec, url: "https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md"}]
spec_version: "0.2"
---
# Operational Enforcements:

- Trigger this skill dynamically before any output loop that handles extensive datasets or raw configurations.
- If payload calculations return totals greater than **4000 tokens**, the system must block raw screen serialization and switch to targeted `view_file` calls or chunked reading.

---
*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-07-18*
*Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*
