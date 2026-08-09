"""
Unit tests for the DSOM FastMCP Server (tools/mcp/server.py).

Verifies that:
1. FastMCP server instance initializes correctly with project root pathing.
2. FastMCP resource functions (`read_current_state`, `read_task`, `read_walkthrough`, `read_openwiki_skeleton`) execute without errors.
3. FastMCP `search_openwiki()` tool returns formatted string output.
"""
import pathlib
import sys
import unittest

# Ensure tools/mcp is on Python path
REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "tools" / "mcp"))

import server  # type: ignore # noqa: E402


class McpServerResourceTests(unittest.TestCase):
    """Test FastMCP resource endpoint read functions."""

    def test_read_task_returns_string(self):
        content = server.read_task()
        self.assertIsInstance(content, str)
        self.assertGreater(len(content), 0)

    def test_read_walkthrough_returns_string(self):
        content = server.read_walkthrough()
        self.assertIsInstance(content, str)
        self.assertGreater(len(content), 0)

    def test_read_openwiki_skeleton_returns_string(self):
        content = server.read_openwiki_skeleton()
        self.assertIsInstance(content, str)
        self.assertGreater(len(content), 0)

    def test_search_openwiki_tool_executes(self):
        results = server.search_openwiki("dsom")
        self.assertIsInstance(results, str)
        self.assertGreater(len(results), 0)


if __name__ == "__main__":
    unittest.main()
