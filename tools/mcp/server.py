# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "mcp[cli]>=1.1.2",
# ]
# ///

"""
DSOM MCP Server
Provides read-only access to the DSOM Sovereign Markdown Palace and Brain files via the Model Context Protocol.

Run this server via uv to ensure isolated dependencies:
uv run tools/mcp/server.py
"""

import os
from pathlib import Path
from mcp.server.fastmcp import FastMCP

# Initialize the FastMCP server
mcp = FastMCP("DSOM-Palace-Server")

# Determine project root (assuming this script is in tools/mcp/)
PROJECT_ROOT = Path(os.getenv("DSOM_ROOT", Path(__file__).parent.parent.parent)).resolve()
BRAIN_DIR = PROJECT_ROOT / ".agents" / "brain"
DOCS_DIR = PROJECT_ROOT / "docs"

# ----------------------------------------------------------------------
# RESOURCES
# ----------------------------------------------------------------------

@mcp.resource("dsom://brain/state")
def read_current_state() -> str:
    """Reads the current condensed DSOM state file."""
    state_file = BRAIN_DIR / "current_state.dsom"
    if not state_file.exists():
        return "State file not found."
    return state_file.read_text(encoding="utf-8")

@mcp.resource("dsom://brain/task")
def read_task() -> str:
    """Reads the active session task list."""
    task_file = BRAIN_DIR / "task.md"
    if not task_file.exists():
        return "Task file not found."
    return task_file.read_text(encoding="utf-8")

@mcp.resource("dsom://brain/walkthrough")
def read_walkthrough() -> str:
    """Reads the episodic walkthrough memory (Session Anchors)."""
    walkthrough_file = BRAIN_DIR / "walkthrough.md"
    if not walkthrough_file.exists():
        return "Walkthrough file not found."
    return walkthrough_file.read_text(encoding="utf-8")

# ----------------------------------------------------------------------
# TOOLS
# ----------------------------------------------------------------------

@mcp.tool()
def search_palace(query: str) -> str:
    """Searches the Sovereign Markdown Palace (docs/) for the query string."""
    if not DOCS_DIR.exists():
        return "Docs directory not found."
    
    results = []
    # Simple recursive text search
    for filepath in DOCS_DIR.rglob("*.md"):
        try:
            content = filepath.read_text(encoding="utf-8")
            lines = content.splitlines()
            for i, line in enumerate(lines):
                if query.lower() in line.lower():
                    # Return the line and surrounding context
                    start = max(0, i - 1)
                    end = min(len(lines), i + 2)
                    context = "\n".join(lines[start:end])
                    results.append(f"--- File: {filepath.relative_to(PROJECT_ROOT)} ---\n{context}\n")
        except Exception:
            continue
            
    if not results:
        return f"No results found for '{query}' in the Palace."
    
    # Truncate results to avoid overwhelming the context window
    output = "\n".join(results)
    if len(output) > 8000:
        return output[:8000] + "\n...[TRUNCATED]"
    return output

if __name__ == "__main__":
    # Start the FastMCP stdio server
    mcp.run()
