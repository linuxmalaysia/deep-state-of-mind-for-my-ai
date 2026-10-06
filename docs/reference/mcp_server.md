---
okf_version: 0.2
type: documentation
title: "Reference: mcp_server.md"
timestamp: "2026-08-13T12:00:00Z"
topics: ["dsom", "reference", "mcp", "fastmcp"]
resource: "/docs/reference/mcp_server.md"
sources: [{author: "Harisfazillah Jamel (LinuxMalaysia)", id: dsom-core-spec, resource: "/docs/governance/DSOM-TRI-PHASIC-COGNITIVE-ARCHITECTURE.md", title: "Deep State of Mind (DSOM) Governance Architecture", type: architecture_spec, url: "https://github.com/linuxmalaysia/deep-state-of-mind-for-my-ai/blob/main/docs/governance/DSOM-TRI-PHASIC-COGNITIVE-ARCHITECTURE.md"}, {author: Google Cloud Platform, id: google-okf-v02-spec, resource: "https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md", title: "Google Cloud Open Knowledge Format (OKF) v0.2 Specification", type: external_spec, url: "https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md"}]
status: stable
generated: {by: "agent/dsom-subagent-01", timestamp: "2026-08-13T12:00:00Z"}
stale_after: "2027-01-01"
spec_version: "0.2"
concept_id: mcp_server
---
# tools/mcp/server.py reference

FastMCP Model Context Protocol (MCP) server implementation for the DSOM Palace.

## Description

The `server.py` utility exposes the Sovereign Markdown Palace, active brain assets, and local OpenWiki knowledge indexes directly to AI clients. It serves context via standard JSON-RPC over `stdio`.

## Script path

`tools/mcp/server.py`

## CLI signature

```bash
uv run tools/mcp/server.py

```

## Environment variables

- **DSOM_ROOT:** Overrides project base directory path. Defaults to parent of script path.

## Resources exposed

AI clients can subscribe to and read these standardised read-only streams:
- **dsom://brain/state:** Output of condensed system state `current_state.dsom`.
- **dsom://brain/task:** Real-time session checklists inside `.agents/brain/task.md`.
- **dsom://brain/walkthrough:** Episodic session walkthrough records.
- **dsom://governance/agents:** Complete 27 Sovereign AI constitutional rules.
- **dsom://openwiki/skeleton:** Subsystem structural hierarchy ranking file.
- **dsom://openwiki/quickstart:** Interactive routing table and system entry-points.

## Tools registered

AI clients can execute these tools dynamically:
- **search_palace(query):** Text search across `docs/` Markdown files.
- **search_openwiki(query):** Sub-millisecond OKF metadata search.
- **fetch_context7_stream(tokens):** Retrieves URL pointers to external pre-indexed token streams.

## Dependencies

- **mcp[cli]:** Model Context Protocol Python library.
- **fastmcp:** Modern FastMCP helper wrapper.
- **pyyaml:** YAML loader configuration parser.


---
*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-08-14*
*Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*
