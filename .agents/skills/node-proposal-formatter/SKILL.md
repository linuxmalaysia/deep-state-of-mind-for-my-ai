---
name: node-proposal-formatter
version: "1.0.0"
description: "Compiles a markdown proposal document into a professionally formatted DOCX file using Node.js and the docx npm package."
author: "Harisfazillah Jamel (LinuxMalaysia)"
license: "GPL-3.0-or-later"
okf_version: 0.2
type: agent_skill
topics: ["node", "docx", "proposal", "document", "formatter"]
status: stable
stale_after: "2027-10-01"
title: node-proposal-formatter
timestamp: "2026-08-05T22:23:51Z"
resource: "/.agents/skills/node-proposal-formatter/SKILL.md"
sources: [{author: "Harisfazillah Jamel (LinuxMalaysia)", id: dsom-core-spec, resource: "/docs/governance/DSOM-TRI-PHASIC-COGNITIVE-ARCHITECTURE.md", title: "Deep State of Mind (DSOM) Governance Architecture", type: architecture_spec, url: "https://github.com/linuxmalaysia/deep-state-of-mind-for-my-ai/blob/main/docs/governance/DSOM-TRI-PHASIC-COGNITIVE-ARCHITECTURE.md"}, {author: Google Cloud Platform, id: google-okf-v02-spec, resource: "https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md", title: "Google Cloud Open Knowledge Format (OKF) v0.2 Specification", type: external_spec, url: "https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md"}]
spec_version: "0.2"
---
# node-proposal-formatter

Use this skill when the user asks to compile or generate a DOCX proposal using the Node.js compiler, or when updating a document formatted via Node.

## Instructions
1. Ensure the source markdown file exists (e.g., `docs/proposal.md` or `docs/client_name/client_proposal.md`).
2. Run the Node.js compiler script passing the input markdown file and the desired output docx file.
   Command: `node tools/compile_node_proposal.js <input.md> <output.docx>`
   Example: `node tools/compile_node_proposal.js docs/proposal.md docs/Node_Proposal.docx`
3. Verify the output was created successfully.


---
*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-07-04*
*Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*
