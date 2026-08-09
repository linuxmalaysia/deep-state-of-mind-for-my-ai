# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "mcp[cli]>=1.1.2",
#     "fastmcp>=0.1.0",
#     "pyyaml>=6.0",
# ]
# ///

"""
DSOM MCP Server
Provides read-only access to the DSOM Sovereign Markdown Palace, Brain files,
and OpenWiki Knowledge Graph via the Model Context Protocol.

Run this server via uv to ensure isolated dependencies:
uv run tools/mcp/server.py
"""

import os
from pathlib import Path
import yaml

try:
    from fastmcp import FastMCP
except ImportError:
    from mcp.server.fastmcp import FastMCP

# Initialize the FastMCP server
mcp = FastMCP("DSOM-Palace-Server")

# Determine project root (assuming this script is in tools/mcp/)
PROJECT_ROOT = Path(os.getenv("DSOM_ROOT", Path(__file__).parent.parent.parent)).resolve()
BRAIN_DIR = PROJECT_ROOT / ".agents" / "brain"
DOCS_DIR = PROJECT_ROOT / "docs"
OPENWIKI_DIR = PROJECT_ROOT / "openwiki"
AGENTS_FILE = PROJECT_ROOT / ".agents" / "AGENTS.md"

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

@mcp.resource("dsom://governance/agents")
def read_agents_rulebook() -> str:
    """Reads the full DSOM Core AI Rulebook (27 Constitutional Rules)."""
    if not AGENTS_FILE.exists():
        return "AGENTS.md file not found."
    return AGENTS_FILE.read_text(encoding="utf-8")

@mcp.resource("dsom://openwiki/skeleton")
def read_openwiki_skeleton() -> str:
    """Reads the OpenWiki documentation skeleton and subsystem ranking."""
    skeleton_file = OPENWIKI_DIR / "_skeleton.md"
    if not skeleton_file.exists():
        return "OpenWiki skeleton file not found."
    return skeleton_file.read_text(encoding="utf-8")

@mcp.resource("dsom://openwiki/quickstart")
def read_openwiki_quickstart() -> str:
    """Reads the OpenWiki master entrypoint and task-routing table."""
    quickstart_file = OPENWIKI_DIR / "quickstart.md"
    if not quickstart_file.exists():
        return "OpenWiki quickstart file not found."
    return quickstart_file.read_text(encoding="utf-8")

# ----------------------------------------------------------------------
# TOOLS
# ----------------------------------------------------------------------

@mcp.tool()
def search_palace(query: str) -> str:
    """Searches the Sovereign Markdown Palace (docs/) for the query string."""
    if not DOCS_DIR.exists():
        return "Docs directory not found."
    
    results = []
    # Recursive text search
    for filepath in DOCS_DIR.rglob("*.md"):
        try:
            content = filepath.read_text(encoding="utf-8")
            lines = content.splitlines()
            for i, line in enumerate(lines):
                if query.lower() in line.lower():
                    start = max(0, i - 1)
                    end = min(len(lines), i + 2)
                    context = "\n".join(lines[start:end])
                    results.append(f"--- File: {filepath.relative_to(PROJECT_ROOT)} ---\n{context}\n")
        except Exception:
            continue
            
    if not results:
        return f"No results found for '{query}' in the Palace."
    
    output = "\n".join(results)
    if len(output) > 8000:
        return output[:8000] + "\n...[TRUNCATED]"
    return output

@mcp.tool()
def search_openwiki(query: str) -> str:
    """Performs sub-millisecond search over OpenWiki OKF frontmatter metadata (title, topics, description)."""
    if not OPENWIKI_DIR.exists():
        return "OpenWiki directory not found."

    results = []
    for filepath in OPENWIKI_DIR.rglob("*.md"):
        try:
            content = filepath.read_text(encoding="utf-8")
            if not content.startswith("---"):
                continue
            parts = content.split("---", 2)
            if len(parts) >= 3:
                meta = yaml.safe_load(parts[1])
                if meta and isinstance(meta, dict):
                    searchable = f"{meta.get('title', '')} {meta.get('description', '')} {' '.join(meta.get('topics', []))}"
                    if query.lower() in searchable.lower():
                        results.append(f"--- Page: {filepath.relative_to(PROJECT_ROOT)} ---\nTitle: {meta.get('title')}\nDescription: {meta.get('description')}\n")
        except Exception:
            pass

    if not results:
        return f"No matching pages found for query '{query}' in OpenWiki."

    return "\n".join(results)

@mcp.tool()
def fetch_context7_stream(tokens: int = 83688) -> str:
    """Fetches the compiled Context7 LLM RAG context stream endpoint URL and usage metadata."""
    url = f"https://context7.com/gitlab_linuxmalaysia/deep-state-of-mind-for-my-ai/llms.txt?tokens={tokens}"
    return (
        f"Context7 Live RAG Stream Endpoint: {url}\n"
        f"Target Token Budget: {tokens}\n"
        "Use this endpoint to provide full project context to external AI agents or RAG pipelines."
    )

if __name__ == "__main__":
    # Start the FastMCP stdio server
    mcp.run()
