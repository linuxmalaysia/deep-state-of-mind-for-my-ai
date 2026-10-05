---
okf_version: 0.2
type: documentation
title: "Explanation: OpenWiki & FastMCP Architecture"
timestamp: "2026-08-13T12:00:00Z"
topics: ["dsom", "explanation", "architecture", "mcp", "openwiki"]
resource: "/docs/explanation/openwiki-mcp-architecture.md"
sources: [{author: Harisfazillah Jamel (LinuxMalaysia), id: dsom-core-spec, resource: /docs/governance/DSOM-TRI-PHASIC-COGNITIVE-ARCHITECTURE.md,
  title: Deep State of Mind (DSOM) Governance Architecture, type: architecture_spec,
  url: 'https://github.com/linuxmalaysia/deep-state-of-mind-for-my-ai/blob/main/docs/governance/DSOM-TRI-PHASIC-COGNITIVE-ARCHITECTURE.md'}, {author: Google Cloud Platform, id: google-okf-v02-spec, resource: 'https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md',
  title: Google Cloud Open Knowledge Format (OKF) v0.2 Specification, type: external_spec,
  url: 'https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md'}]
status: stable
generated: {by: agent/dsom-subagent-01, timestamp: '2026-08-13T12:00:00Z'}
stale_after: "2027-01-01"
spec_version: "0.2"
concept_id: openwiki_mcp_architecture
---
# OpenWiki and FastMCP architecture

An in-depth explanation of the technical design, data flows, and reasoning behind OpenWiki and FastMCP integrations.

## High-level architecture

The DSOM knowledge layer bridges localised documents to active AI agents via two complementary components:

```mermaid
flowchart TD
    Files["Sovereign Markdown Files<br/>(docs/, openwiki/)"] -->|Local Indexing| Server["FastMCP Server<br/>(tools/mcp/server.py)"]
    Files -->|Compilation| Web["Static Docs Site<br/>(GitHub Pages / RTD)"]
    Server -->|JSON-RPC via stdio| Agent["AI Agent<br/>(Cursor, Copilot, Claude)"]

```

## Why pure Python OpenWiki?

Historically, OpenWiki implementations required heavy Node.js runtimes or cloud compiler keys. This design violated **Sovereign AI Rule 27 (Zero-Binary Mandate)**.

Replacing Node binaries with the pure Python `openwiki_emulator.py` provides:
- **Zero Node.js dependencies:** The script runs offline using standard Python library APIs and the `pyyaml` package.
- **In-place self-healing:** The emulator scans embedded diagrams, detects syntactical errors, degrades blocks gracefully, and heals them when fixed.

## FastMCP context routing

The FastMCP server (`tools/mcp/server.py`) acts as the primary API broker for AI engines.

Rather than feeding the entire documentation codebase into the context window, the server enables **Progressive Disclosure**:
1. The AI reads condensed states (`dsom://brain/state`).
2. If further details are needed, the AI calls targeted tools (`search_palace` or `search_openwiki`).
3. Only the relevant context fragments are returned, reducing overall token usage.

---
*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-08-14*
*Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*
