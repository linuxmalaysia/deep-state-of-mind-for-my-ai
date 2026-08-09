---
okf_version: 0.1
type: operational_guide
title: "🛠️ HOWTO: Operating DSOM FastMCP Knowledge Server"
timestamp: "2026-08-09T10:35:00Z"
topics: ["mcp", "fastmcp", "howto", "dsom", "server", "cursor", "claude"]
description: "Step-by-step operational guide for running, configuring, and connecting the DSOM FastMCP Server to Cursor, Claude Desktop, and IDE assistants."
resource: "file:///docs/tools/HOWTO-MCP-SERVER.md"
---
# 🛠️ HOWTO: Operating DSOM FastMCP Knowledge Server

This operational guide provides step-by-step instructions for running, configuring, and connecting the **DSOM FastMCP Knowledge Server (`tools/mcp/server.py`)** via Model Context Protocol (MCP) to AI IDEs such as Cursor, Claude Desktop, and VSCode.

---

## ⚡ 1. Fast Execution Protocol (Rule 16 `uv` Mandate)

The MCP server runs natively in Python using `uv` with PEP 723 inline script dependencies (`mcp`, `fastmcp`, `pyyaml`). Zero global installation required.

### Launching the Stdio MCP Server:
```bash
uv run tools/mcp/server.py
```

---

## 🔌 2. IDE Integration & Configuration Guides

### A. Cursor IDE (`.cursor/mcp.json` or Settings -> MCP):
Add the following JSON configuration to Cursor under **Settings > Features > MCP**:

```json
{
  "mcpServers": {
    "dsom-palace": {
      "command": "uv",
      "args": [
        "run",
        "tools/mcp/server.py"
      ],
      "cwd": "${workspaceFolder}"
    }
  }
}
```

---

### B. Claude Desktop (`claude_desktop_config.json`):
Add the server entry to `%APPDATA%\Claude\claude_desktop_config.json` (Windows) or `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS):

```json
{
  "mcpServers": {
    "dsom-palace": {
      "command": "uv",
      "args": [
        "run",
        "D:\\Users\\LinuxMalaysia\\Projects\\deep-state-of-mind-for-my-ai\\tools\\mcp\\server.py"
      ]
    }
  }
}
```

---

## 📊 3. Exposed MCP Endpoint Matrix (Resources & Tools)

### A. MCP Resources (6 Read-Only Protocol URIs)

| Resource URI | Description / Source File |
| :--- | :--- |
| **`dsom://brain/state`** | Reads condensed DSOM state (`.agents/brain/current_state.dsom`). |
| **`dsom://brain/task`** | Reads active session task list (`.agents/brain/task.md`). |
| **`dsom://brain/walkthrough`** | Reads session walkthrough anchors (`.agents/brain/walkthrough.md`). |
| **`dsom://governance/agents`** | Reads the 27 Constitutional AI Rules (`.agents/AGENTS.md`). |
| **`dsom://openwiki/skeleton`** | Reads OpenWiki subsystem rankings (`openwiki/_skeleton.md`). |
| **`dsom://openwiki/quickstart`** | Reads OpenWiki master entrypoint (`openwiki/quickstart.md`). |

---

### B. MCP Tools (3 Executable Tools)

| Tool Name | Parameters | Purpose |
| :--- | :--- | :--- |
| **`search_palace`** | `query: str` | Performs bounded text search over `docs/*.md` (capped at 8,000 chars). |
| **`search_openwiki`** | `query: str` | Performs sub-millisecond search over OpenWiki OKF frontmatter metadata (`topics:`, `title:`, `description:`). |
| **`fetch_context7_stream`** | `tokens: int = 83688` | Returns the live Context7 LLM RAG context stream endpoint URL. |

---

## 🧪 4. Troubleshooting & Verification

1. **Verify Python Environment:**
   Ensure `uv` is installed and accessible on your PATH (`uv --version`).
2. **Test Server Startup:**
   ```bash
   uv run tools/mcp/server.py --help
   ```
3. **Verify Regression Suite:**
   ```bash
   uv run --with pyyaml python -m unittest tests/test_okf_frontmatter_bom_reorder.py tests/test_okf_quoting.py tests/test_seo_sitemaps.py tests/test_docs_symlinks.py
   ```

---

## 🔗 5. References

* **MCP Server Script:** [`tools/mcp/server.py`](file:///tools/mcp/server.py)
* **Native OpenWiki Emulator:** [`tools/openwiki_emulator.py`](file:///tools/openwiki_emulator.py)
* **OpenWiki Integration Blueprint:** [`docs/governance/OPENWIKI-INTEGRATION-GUIDE.md`](file:///docs/governance/OPENWIKI-INTEGRATION-GUIDE.md)

---
*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-08-09*
*Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*
