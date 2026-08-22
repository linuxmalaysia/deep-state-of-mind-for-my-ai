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
import sys
from pathlib import Path
import yaml

try:
    from fastmcp import FastMCP
except ImportError:
    from mcp.server.fastmcp import FastMCP

# Determine project root (assuming this script is in tools/mcp/)
PROJECT_ROOT = Path(os.getenv("DSOM_ROOT", Path(__file__).parent.parent.parent)).resolve()
BRAIN_DIR = PROJECT_ROOT / ".agents" / "brain"
DOCS_DIR = PROJECT_ROOT / "docs"
OPENWIKI_DIR = PROJECT_ROOT / "openwiki"
REFERENCES_DIR = PROJECT_ROOT / "references"
AGENTS_FILE = PROJECT_ROOT / ".agents" / "AGENTS.md"

# Integrate DSOM Guardrails
GUARDRAILS_SRC = PROJECT_ROOT / "tools" / "guardrails-ai-dsom" / "src"
if str(GUARDRAILS_SRC) not in sys.path:
    sys.path.insert(0, str(GUARDRAILS_SRC))

try:
    from guardrails_dsom import (
        GuardrailsCredentialGuardian,
        GuardrailsOKFBOMValidator,
        GuardrailsOKFTrustValidator,
        GuardrailsByteCapValidator,
        GuardrailsRootCleanlinessValidator,
    )
    _CRED_GUARDIAN = GuardrailsCredentialGuardian(on_fail="block")
    _BOM_VALIDATOR = GuardrailsOKFBOMValidator(on_fail="fix")
    _TRUST_VALIDATOR = GuardrailsOKFTrustValidator(on_fail="block")
    _BYTE_CAP = GuardrailsByteCapValidator(max_bytes=8000, on_fail="fix")
    _ROOT_GUARD = GuardrailsRootCleanlinessValidator(on_fail="fix")
    HAS_GUARDRAILS = True
except ImportError:
    HAS_GUARDRAILS = False

# Initialize the FastMCP server
mcp = FastMCP("DSOM-Palace-Server")

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
def search_code_snippets(query: str, limit: int = 5) -> str:
    """Searches actionable code snippets, terminal commands, and configuration blocks from the Context7 indexed knowledge base.
    
    Args:
        query: Keyword or command phrase to match (e.g. 'ansible', 'guardrails', 'uv add', 'mint dev').
        limit: Maximum number of snippet blocks to return (default: 5).
    """
    context7_file = REFERENCES_DIR / "llms-from-context7.txt"
    if not context7_file.exists():
        return "Error: Local snapshot references/llms-from-context7.txt not found."

    try:
        content = context7_file.read_text(encoding="utf-8")
        blocks = content.split("--------------------------------")
        matched = []
        for block in blocks:
            b_clean = block.strip()
            if not b_clean:
                continue
            if query.lower() in b_clean.lower():
                matched.append(b_clean)

        if not matched:
            return f"No code snippets found matching query '{query}'."

        total_found = len(matched)
        result = [f"Found {total_found} matching snippet(s) (showing top {min(limit, total_found)}):\n"]
        result.extend(matched[:limit])
        return "\n\n" + ("\n\n---\n\n".join(result))
    except Exception as e:
        return f"Error reading code snippets: {str(e)}"

@mcp.tool()
def fetch_context7_stream(tokens: int = 83688, return_offline_sample: bool = False) -> str:
    """Fetches the compiled Context7 LLM RAG context stream endpoint URL, or returns a local offline snapshot sample.
    
    Args:
        tokens: Target token budget for the live stream (default: 83688).
        return_offline_sample: If True, returns the first 2,000 characters from the local offline references snapshot.
    """
    url = f"https://context7.com/gitlab_linuxmalaysia/deep-state-of-mind-for-my-ai/llms.txt?tokens={tokens}"
    out = [
        f"Context7 Live RAG Stream Endpoint: {url}",
        f"Target Token Budget: {tokens}",
        "Use this endpoint to stream fresh project context into external AI agents or RAG pipelines."
    ]

    context7_file = REFERENCES_DIR / "llms-from-context7.txt"
    if return_offline_sample and context7_file.exists():
        try:
            sample = context7_file.read_text(encoding="utf-8")[:2000]
            out.append("\n--- Offline Snapshot Preview (references/llms-from-context7.txt) ---")
            out.append(sample)
        except Exception:
            pass

    return "\n".join(out)

@mcp.tool()
def write_palace_document(relative_path: str, markdown_content: str) -> str:
    """Safely writes or updates a markdown document in the Palace with active DSOM guardrails validation."""
    if HAS_GUARDRAILS:
        # 1. Rule 24: Credential Leak Interception
        cred_res = _CRED_GUARDIAN.validate(markdown_content)
        if not cred_res.is_valid:
            return f"[ERROR: GUARDRAIL BLOCKED] {cred_res.error_message}"

        # 2. Rule 17: Root Cleanliness Guard
        root_res = _ROOT_GUARD.validate(relative_path)
        target_rel_path = root_res.corrected_value

        # 3. Rule 2 & 25: BOM Stripping & Fence Integrity
        bom_res = _BOM_VALIDATOR.validate(markdown_content)
        clean_content = bom_res.corrected_value
    else:
        target_rel_path = relative_path
        clean_content = markdown_content

    target_file = PROJECT_ROOT / target_rel_path
    target_file.parent.mkdir(parents=True, exist_ok=True)
    target_file.write_text(clean_content, encoding="utf-8")
    return f"Successfully validated and written to {target_rel_path}"

if __name__ == "__main__":
    # Start the FastMCP stdio server
    mcp.run()
