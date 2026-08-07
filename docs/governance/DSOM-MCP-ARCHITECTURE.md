---
okf_version: 0.1
type: documentation
title: "DSOM-MCP-ARCHITECTURE.md — Model Context Protocol Native Server"
timestamp: "2026-07-31T00:00:00Z"
topics: ["mcp", "architecture", "rag", "context7", "server"]
description: "Research and architectural blueprint for converting the DSOM Palace into a native MCP server for AI clients."
---
# DSOM-MCP-ARCHITECTURE.md

> **"Context is not a static text block; it is an interactive resource. Let the AI query the Palace itself."**

---

## 1. The Context7 Inspiration
Traditional DSOM interactions required passing context into the chat explicitly via `.dsom` state files, `palace_update_proposals`, or the human manually injecting references. Services like Context7 demonstrated a better approach: **RAG (Retrieval-Augmented Generation) exposed natively to the AI client.**

Instead of pushing context *to* the AI, the AI *pulls* exactly what it needs from the Sovereign Markdown Palace through a standardized API: the **Model Context Protocol (MCP)**.

## 2. Core Architecture of DSOM-MCP
We are building a native Python MCP Server (`dsom-mcp-server`) that completely replaces the need for external third-party syncs for local development.

### 2.1 The Transport Layer (STDIO)
The MCP server operates as a local subprocess spawned by your AI editor (Cursor, Google Jules, Claude Desktop). Communication happens over `stdio` using JSON-RPC.
- **Rule:** The MCP script must strictly output JSON-RPC to `stdout`. All logs or debugging MUST be written to `stderr`. Using `print()` without redirecting to `sys.stderr` will instantly break the protocol.

### 2.2 Framework & Ecosystem (Rule 16 Compliance)
- **Executor:** The server is executed exclusively via `uv run` to maintain Python environmental isolation.
- **Framework:** We utilize the `fastmcp` (or official `mcp`) Python SDK to define resources and tools asynchronously.

## 3. The 3 Pillars of the DSOM-MCP Server

### Pillar A: Exposed Resources (Memory & State)
Resources are static or dynamic data blobs the AI can "read" at will without using a tool.
- `dsom://state/current` → Serves `.agents/brain/current_state.dsom`
- `dsom://state/task` → Serves `.agents/brain/task.md`
- `dsom://state/walkthrough` → Serves `.agents/brain/walkthrough.md`

When an AI boots up, it reads these URIs immediately to achieve the "Genesis Read" without the human typing a single prompt.

### Pillar B: Exposed Tools (The Rituals)
Tools are executable functions. We expose our existing DSOM automation to the AI natively.
- `search_palace(query)`: Executes a semantic or `grep` search across `docs/`.
- `palace_sync()`: Triggers the EOD spatial reflection engine natively.

### Pillar C: Execution Bridge
Because Windows (T1) and WSL2 (T2) possess execution boundaries, the MCP server must detect its environment and invoke the `tools/` Bash or PowerShell scripts appropriately.

## 4. MCP Client Configuration Example
To attach the DSOM-MCP server to Claude Desktop (or Cursor), the human operator modifies their client config (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "dsom-palace": {
      "command": "uv",
      "args": [
        "run",
        "--with", "mcp",
        "tools/mcp/server.py"
      ],
      "env": {
        "DSOM_ROOT": "/absolute/path/to/project"
      }
    }
  }
}
```

## 5. Security Posture
- **Zero-Network Surface:** The server runs exclusively on local `stdio`. No HTTP ports are opened.
- **No External Exfiltration:** Unlike passing codebase context to third-party RAG providers, all semantic searching and reading happens strictly on the local machine.

---
*Standard: DSOM For My AI Protocol v6.1 | Harisfazillah Jamel | LinuxMalaysia*
