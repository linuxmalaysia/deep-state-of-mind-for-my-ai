"""
Unit tests for the DSOM FastMCP Server (tools/mcp/server.py).

Verifies that:
1. FastMCP server instance initializes correctly with project root pathing.
2. FastMCP resource functions (`read_current_state`, `read_task`, `read_walkthrough`, `read_openwiki_skeleton`) execute without errors.
3. FastMCP `search_openwiki()` tool returns formatted string output.
"""
import pathlib
import subprocess
import sys
import unittest
from unittest.mock import patch

# Ensure tools/mcp is on Python path
REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "tools" / "mcp"))

import server  # type: ignore


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

    def test_search_brain_tool_executes(self):
        import tempfile
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_root = pathlib.Path(tmpdir)
            tmp_brain = tmp_root / ".agents" / "brain"
            tmp_brain.mkdir(parents=True, exist_ok=True)
            (tmp_brain / "memory.md").write_text("# Memory\nThis file contains dsom state history.\n", encoding="utf-8")

            with patch.object(server, "PROJECT_ROOT", tmp_root), patch.object(server, "BRAIN_DIR", tmp_brain):
                results = server.search_brain("dsom")
                self.assertIsInstance(results, str)
                self.assertGreater(len(results), 0)
                self.assertIn("Memory File:", results)
                self.assertIn("dsom state history", results)

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

    def test_run_council_tool_executes(self):
        topic = "Zero Binary Architecture Adoption"
        res = server.run_council(topic=topic, mode="quick")
        self.assertIsInstance(res, str)
        self.assertIn("Council Decision Record", res)
        self.assertIn(topic, res)

    def test_run_council_rejects_absolute_output_path(self):
        res = server.run_council(topic="Test", output_path="/tmp/evil_cdr.md")
        self.assertIn("Error: Invalid output_path. Absolute paths are not permitted", res)

    def test_run_council_rejects_parent_traversal_path(self):
        res = server.run_council(topic="Test", output_path="../evil_cdr.md")
        self.assertIn("Error: Invalid output_path. Parent directory traversal is not permitted", res)

    @patch("shutil.which", return_value="/usr/bin/qmd")
    @patch("subprocess.run")
    def test_qmd_search_invocation_and_output(self, mock_run, mock_which):
        mock_run.return_value = subprocess.CompletedProcess(
            args=["/usr/bin/qmd", "query", "architecture", "-c", "oss-docs", "-n", "3"],
            returncode=0,
            stdout="qmd://oss-docs/architecture.md:1:10\nMatch content",
            stderr=""
        )
        res = server.qmd_search(query="architecture", collection="oss-docs", mode="query", limit=3)
        mock_run.assert_called_once_with(
            ["/usr/bin/qmd", "query", "architecture", "-c", "oss-docs", "-n", "3"],
            capture_output=True,
            text=True,
            timeout=30,
            check=False
        )
        self.assertEqual(res, "qmd://oss-docs/architecture.md:1:10\nMatch content")

    @patch("shutil.which", return_value="/usr/bin/qmd")
    @patch("subprocess.run")
    def test_qmd_search_modes_and_parameters(self, mock_run, mock_which):
        mock_run.return_value = subprocess.CompletedProcess(args=[], returncode=0, stdout="Result", stderr="")

        res_bm25 = server.qmd_search(query="podman", collection="oss-docs", mode="search", limit=1)
        self.assertEqual(res_bm25, "Result")
        self.assertEqual(mock_run.call_args_list[0].args[0], ["/usr/bin/qmd", "search", "podman", "-c", "oss-docs", "-n", "1"])

        res_vec = server.qmd_search(query="sovereign governance", collection="oss-agents", mode="vsearch", limit=2)
        self.assertEqual(res_vec, "Result")
        self.assertEqual(mock_run.call_args_list[1].args[0], ["/usr/bin/qmd", "vsearch", "sovereign governance", "-c", "oss-agents", "-n", "2"])

        res_brain = server.qmd_search(query="episodic memory", collection="oss-brain", mode="query", limit=3)
        self.assertEqual(res_brain, "Result")
        self.assertEqual(mock_run.call_args_list[2].args[0], ["/usr/bin/qmd", "query", "episodic memory", "-c", "oss-brain", "-n", "3"])

    @patch("shutil.which", return_value="/usr/bin/qmd")
    @patch("subprocess.run")
    def test_qmd_search_nonzero_exit_error_distinct_from_results(self, mock_run, mock_which):
        mock_run.return_value = subprocess.CompletedProcess(
            args=["/usr/bin/qmd", "query", "invalid"],
            returncode=1,
            stdout="",
            stderr="Collection 'invalid' not found"
        )
        res = server.qmd_search(query="invalid", mode="query")
        self.assertIn("QMD search error (exit code 1): Collection 'invalid' not found", res)
        self.assertNotIn("qmd://", res)

    @patch("shutil.which", return_value=None)
    @patch("pathlib.Path.is_file", return_value=False)
    def test_qmd_search_binary_missing_fallback(self, mock_is_file, mock_which):
        res = server.qmd_search(query="test")
        self.assertIn("Error: QMD binary not found", res)


if __name__ == "__main__":
    unittest.main()
