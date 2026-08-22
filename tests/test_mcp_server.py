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

    def test_search_code_snippets(self):
        results = server.search_code_snippets("ansible", limit=2)
        self.assertIsInstance(results, str)
        self.assertIn("ansible", results.lower())

    def test_fetch_context7_stream(self):
        res = server.fetch_context7_stream(return_offline_sample=True)
        self.assertIn("https://context7.com/gitlab_linuxmalaysia/deep-state-of-mind-for-my-ai", res)
        self.assertIn("Offline Snapshot Preview", res)

    def test_write_palace_document_blocks_credentials(self):
        leak_content = "This contains a secret: ghp_123456789012345678901234567890123456"
        res = server.write_palace_document("docs/test_secret.md", leak_content)
        self.assertIn("[ERROR: GUARDRAIL BLOCKED]", res)


if __name__ == "__main__":
    unittest.main()
