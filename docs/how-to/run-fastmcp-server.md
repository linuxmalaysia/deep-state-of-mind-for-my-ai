---
okf_version: 0.1
type: documentation
title: "How-To: Run the FastMCP Server"
timestamp: "2026-08-13T12:00:00Z"
topics: ["dsom", "how-to", "mcp", "server"]
---
# Run the FastMCP server

This guide explains how to configure, start, and debug the local Model Context Protocol (MCP) server to expose the Sovereign Palace to AI editors.

## Prerequisites

- **Python 3.11+** and **`uv`** must be installed.
- **MCP client** (e.g. Cursor, Claude Desktop, or Windsurf) running locally.

## Step 1: Start the server

Launch the server using `uv run` to isolate and resolve dependencies dynamically. This starts the JSON-RPC interface over standard input/output (`stdio`):

```bash
uv run tools/mcp/server.py

```

## Step 2: Configure AI editors (Cursor / Claude Desktop)

To connect your IDE to the server, append the following configuration block to your client settings.

### Claude Desktop config (`claudedesktopconfig.json`)

Open `~/.code/claude_desktop_config.json` (macOS/Linux) or `%APPDATA%/Claude/claude_desktop_config.json` (Windows) and insert:

```json
{
  "mcpServers": {
    "dsom-palace": {
      "command": "uv",
      "args": [
        "run",
        "--with", "mcp[cli]>=1.1.2",
        "--with", "fastmcp>=0.1.0",
        "--with", "pyyaml>=6.0",
        "tools/mcp/server.py"
      ],
      "env": {
        "DSOM_ROOT": "/absolute/path/to/deep-state-of-mind-for-my-ai"
      }
    }
  }
}

```

## Step 3: Verify server functionality

Execute the standard test suite to confirm that the server registers all required resources and tools:

```bash
uv run --with pyyaml --with pytest --with mcp==1.2.1 --with fastmcp pytest tests/test_mcp_server.py

```

---
*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-08-14*
*Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*
