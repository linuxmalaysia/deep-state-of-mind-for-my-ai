"""
Unit tests for DSOM utility tools (bench_brain.py, mkdocs_hooks.py).

Verifies that:
1. `bench_brain.py` correctly discovers files and measures byte read volume.
2. `mkdocs_hooks.py` rewrites Markdown link URLs (stripping 'docs/' and adjusting relative paths) for MkDocs compilation.
"""
import pathlib
import sys
import tempfile
import unittest

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "tools"))

import bench_brain  # type: ignore # noqa: E402
import mkdocs_hooks  # type: ignore # noqa: E402


class BenchBrainTests(unittest.TestCase):
    """Test tools/bench_brain.py utility functions."""

    def test_get_files_discovers_md_files(self):
        target_dirs = [str(REPO_ROOT / ".agents" / "brain")]
        files = bench_brain.get_files(target_dirs, extension=".md")
        self.assertIsInstance(files, list)
        self.assertGreater(len(files), 0)

    def test_bench_read_measures_bytes_and_time(self):
        sample_content = b"Hello DSOM Benchmarking"
        with tempfile.NamedTemporaryFile("wb", delete=False) as tmp:
            tmp.write(sample_content)
            tmp_path = tmp.name

        try:
            total_bytes, elapsed = bench_brain.bench_read([tmp_path])
            self.assertEqual(total_bytes, len(sample_content))
            self.assertGreaterEqual(elapsed, 0.0)
        finally:
            pathlib.Path(tmp_path).unlink(missing_ok=True)


class MkdocsHooksLinkRewritingTests(unittest.TestCase):
    """Test tools/mkdocs_hooks.py Markdown link rewriting hook."""

    def test_on_page_markdown_strips_docs_prefix(self):
        input_markdown = "Check [Governance](docs/governance/AI-MASTER-PROTOCOL.md) for details."
        output_markdown = mkdocs_hooks.on_page_markdown(input_markdown, page=None, config=None, files=None)
        self.assertEqual(output_markdown, "Check [Governance](governance/AI-MASTER-PROTOCOL.md) for details.")

    def test_on_page_markdown_converts_double_parent_relative_link(self):
        input_markdown = "See [AGENTS](../../AGENTS.md) root rulebook."
        output_markdown = mkdocs_hooks.on_page_markdown(input_markdown, page=None, config=None, files=None)
        self.assertEqual(output_markdown, "See [AGENTS](../AGENTS.md) root rulebook.")

    def test_on_page_markdown_preserves_external_links(self):
        input_markdown = "Visit [GitHub](https://github.com/linuxmalaysia) website."
        output_markdown = mkdocs_hooks.on_page_markdown(input_markdown, page=None, config=None, files=None)
        self.assertEqual(output_markdown, input_markdown)


class PrivacyGuardianSecurityTests(unittest.TestCase):
    """Test tools/privacy-guardian.sh and privacy-guardian.ps1 regex patterns."""

    @classmethod
    def setUpClass(cls):
        cls.sh_content = (REPO_ROOT / "tools" / "privacy-guardian.sh").read_text(encoding="utf-8")
        cls.ps1_content = (REPO_ROOT / "tools" / "privacy-guardian.ps1").read_text(encoding="utf-8")

    def test_fine_grained_github_pat_pattern_present(self):
        self.assertIn("github_pat_", self.sh_content)
        self.assertIn("github_pat_", self.ps1_content)


if __name__ == "__main__":
    unittest.main()
