---
name: node-slide-generator
version: "1.0.0"
description: "Generates a PowerPoint presentation from a markdown outline using Node.js and pptxgenjs."
author: "Harisfazillah Jamel (LinuxMalaysia)"
license: "GPL-3.0-or-later"
okf_version: 0.2
type: agent_skill
topics: ["node", "pptx", "slides", "presentation", "generator"]
status: stable
stale_after: "2027-10-01"
title: node-slide-generator
timestamp: "2026-08-05T22:23:51Z"
resource: "/.agents/skills/node-slide-generator/SKILL.md"
sources: [{author: "Harisfazillah Jamel (LinuxMalaysia)", id: dsom-core-spec, resource: "/docs/governance/DSOM-TRI-PHASIC-COGNITIVE-ARCHITECTURE.md", title: "Deep State of Mind (DSOM) Governance Architecture", type: architecture_spec, url: "https://github.com/linuxmalaysia/deep-state-of-mind-for-my-ai/blob/main/docs/governance/DSOM-TRI-PHASIC-COGNITIVE-ARCHITECTURE.md"}, {author: Google Cloud Platform, id: google-okf-v02-spec, resource: "https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md", title: "Google Cloud Open Knowledge Format (OKF) v0.2 Specification", type: external_spec, url: "https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md"}]
spec_version: "0.2"
---
# node-slide-generator

Use this skill when the user asks to compile, generate, or format PowerPoint presentation slides using Node.js.

## Instructions
1. Ensure the source markdown outline exists (e.g., `docs/slides_outline.md` or `docs/client_name/client_slides.md`).
2. Run the Node.js compiler script passing the input markdown file and the desired output pptx file.
   Command: `node tools/compile_node_slides.js <input.md> <output.pptx>`
   Example: `node tools/compile_node_slides.js docs/slides_outline.md docs/Node_Migration_Presentation.pptx`
3. Verify the output was created successfully.


---
*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-07-04*
*Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*
