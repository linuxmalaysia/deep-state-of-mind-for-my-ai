"""
Markdown OKF schema, DSOM governance footers, and UK English spelling unit tests.
"""
import os
import pathlib
import re
import unittest
import sys
import tempfile
import unittest
from unittest import mock

import yaml

def _find_repo_root(start: pathlib.Path) -> pathlib.Path:
    current = start.resolve()
    for parent in [current, *current.parents]:
        if (parent / ".git").exists():
            return parent
    raise RuntimeError("Could not locate repository root (.git not found)")

REPO_ROOT = _find_repo_root(pathlib.Path(__file__).parent)
FRONTMATTER_RE = re.compile(r"\A---\s*\r?\n(.*?)(?:\r?\n)?---\s*(?:\r?\n|\Z)", re.DOTALL)


class TestMarkdownCompliance(unittest.TestCase):
    """Markdown schema, governance footers, and spelling compliance tests."""

    def test_markdown_okf_compliance(self):
        """Verify Markdown files adhere to OKF v0.1 schema frontmatter rules."""
        exclude_files = {"CLAUDE.md"}
        exclude_dirs = {".git", "node_modules", ".pytest_cache", "venv", ".venv", "openwiki", "site"}

        md_files = []
        for dirpath, dirnames, filenames in os.walk(REPO_ROOT):
            dirnames[:] = [d for d in dirnames if d not in exclude_dirs]
            for filename in filenames:
                if filename.endswith(".md") and filename not in exclude_files:
                    filepath = pathlib.Path(dirpath) / filename
                    if not filepath.is_symlink():
                        # Handle Windows git text symlinks
                        try:
                            content = filepath.read_text(encoding="utf-8").strip()
                            if content.startswith("../") and "\n" not in content and len(content) < 250:
                                continue
                        except Exception:
                            pass
                        md_files.append(filepath)

        REQUIRED_FIELDS = {"okf_version", "type", "title", "timestamp", "topics"}

        for md_file in md_files:
            with self.subTest(file=md_file.relative_to(REPO_ROOT).as_posix()):
                raw_bytes = md_file.read_bytes()
                self.assertFalse(raw_bytes.startswith(b"\xef\xbb\xbf"), f"{md_file.name} must not contain UTF-8 BOM")

                text = raw_bytes.decode("utf-8")
                self.assertTrue(text.startswith("---\n") or text.startswith("---\r\n"), f"{md_file.name} must begin with frontmatter fence ---")

                match = FRONTMATTER_RE.match(text)
                self.assertIsNotNone(match, f"{md_file.name} must contain valid frontmatter block")

                data = yaml.safe_load(match.group(1))
                self.assertIsInstance(data, dict, f"Frontmatter in {md_file.name} must parse to a mapping")

                for field in REQUIRED_FIELDS:
                    self.assertIn(field, data, f"Frontmatter in {md_file.name} missing required field '{field}'")

    def test_markdown_governance_footers(self):
        """Verify presence of governance footers or copyright signatures in Markdown docs."""
        docs_dir = REPO_ROOT / "docs"
        doc_files = [p for p in docs_dir.glob("**/*.md") if p.is_file() and not p.is_symlink()]
        self.assertGreater(len(doc_files), 0, "docs directory must contain Markdown files")

        for doc_file in doc_files:
            with self.subTest(file=doc_file.relative_to(REPO_ROOT).as_posix()):
                text = doc_file.read_text(encoding="utf-8")
                has_license_ref = any(term in text for term in ("GPL", "License", "Copyright", "DSOM", "Deep State of Mind", "Governance"))
                self.assertTrue(has_license_ref, f"{doc_file.name} should reference license/DSOM governance")

    def test_uk_english_documentation_spellings(self):
        """Verify UK English spelling conventions across documentation corpus."""
        doc_files = [REPO_ROOT / "README.md"] + [p for p in (REPO_ROOT / "docs").glob("**/*.md") if p.is_file() and not p.is_symlink()]
        UK_TERMS = ["organisation", "optimisation", "behaviour", "standardised", "localised", "categorises"]

        combined_text = ""
        for doc in doc_files:
            if doc.exists():
                combined_text += doc.read_text(encoding="utf-8").lower() + "\n"

        for uk_term in UK_TERMS:
            with self.subTest(term=uk_term):
                self.assertIn(
                    uk_term,
                    combined_text,
                    f"Documentation corpus should incorporate standard UK English spelling '{uk_term}'"
                )

    def test_frontmatter_regex_matches_crlf_line_endings(self):
        """FRONTMATTER_RE must match a frontmatter block using CRLF line endings."""
        text = "---\r\nokf_version: 0.1\r\ntitle: X\r\n---\r\nBody text\r\n"
        match = FRONTMATTER_RE.match(text)
        self.assertIsNotNone(match)
        self.assertIn("okf_version: 0.1", match.group(1))

    def test_frontmatter_regex_returns_none_without_closing_fence(self):
        """FRONTMATTER_RE must not match when the closing --- fence is absent."""
        text = "---\nokf_version: 0.1\ntitle: X\nBody text with no closing fence\n"
        self.assertIsNone(FRONTMATTER_RE.match(text))

    def test_markdown_okf_compliance_accepts_valid_frontmatter(self):
        """A Markdown file with all required OKF fields must pass compliance."""
        module = sys.modules[__name__]
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_root = pathlib.Path(tmpdir)
            (tmp_root / "valid.md").write_text(
                "---\n"
                "okf_version: 0.1\n"
                "type: doc\n"
                "title: Valid Doc\n"
                'timestamp: "2026-01-01T00:00:00Z"\n'
                'topics: ["a"]\n'
                "---\n"
                "Body\n",
                encoding="utf-8",
            )
            with mock.patch.object(module, "REPO_ROOT", tmp_root):
                self.test_markdown_okf_compliance()  # must not raise

    def _run_okf_compliance_test_and_get_result(self):
        """Run test_markdown_okf_compliance in an isolated suite/result.

        The production test wraps its per-file assertions in
        ``self.subTest(...)``, which swallows individual assertion failures,
        so ``assertRaises(AssertionError)`` around a direct call would never
        observe them. A real TestSuite/TestResult surfaces them instead.
        """
        suite = unittest.TestSuite()
        suite.addTest(self.__class__("test_markdown_okf_compliance"))
        result = unittest.TestResult()
        suite.run(result)
        return result

    def test_markdown_okf_compliance_rejects_missing_required_field(self):
        """A Markdown file missing a required frontmatter field must fail compliance."""
        module = sys.modules[__name__]
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_root = pathlib.Path(tmpdir)
            (tmp_root / "invalid.md").write_text(
                "---\n"
                "okf_version: 0.1\n"
                "type: doc\n"
                "title: Invalid Doc\n"
                "---\n"
                "Body\n",
                encoding="utf-8",
            )
            with mock.patch.object(module, "REPO_ROOT", tmp_root):
                result = self._run_okf_compliance_test_and_get_result()
            self.assertFalse(result.wasSuccessful())

    def test_markdown_okf_compliance_flags_utf8_bom(self):
        """A Markdown file starting with a UTF-8 BOM must fail compliance."""
        module = sys.modules[__name__]
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_root = pathlib.Path(tmpdir)
            content = (
                "---\n"
                "okf_version: 0.1\n"
                "type: doc\n"
                "title: BOM Doc\n"
                'timestamp: "2026-01-01T00:00:00Z"\n'
                'topics: ["a"]\n'
                "---\n"
                "Body\n"
            )
            (tmp_root / "bom.md").write_bytes(b"\xef\xbb\xbf" + content.encode("utf-8"))
            with mock.patch.object(module, "REPO_ROOT", tmp_root):
                result = self._run_okf_compliance_test_and_get_result()
            self.assertFalse(result.wasSuccessful())

    def test_markdown_governance_footers_raises_when_docs_directory_missing(self):
        """Compliance must fail when the repository has no docs/ directory at all."""
        module = sys.modules[__name__]
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_root = pathlib.Path(tmpdir)
            with mock.patch.object(module, "REPO_ROOT", tmp_root):
                with self.assertRaises(AssertionError):
                    self.test_markdown_governance_footers()

    def test_markdown_governance_footers_rejects_missing_license_reference(self):
        """A docs Markdown file lacking any governance/license reference must fail."""
        module = sys.modules[__name__]
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_root = pathlib.Path(tmpdir)
            docs_dir = tmp_root / "docs"
            docs_dir.mkdir()
            (docs_dir / "no_footer.md").write_text("Just plain content.\n", encoding="utf-8")
            with mock.patch.object(module, "REPO_ROOT", tmp_root):
                suite = unittest.TestSuite()
                suite.addTest(self.__class__("test_markdown_governance_footers"))
                result = unittest.TestResult()
                suite.run(result)
            self.assertFalse(result.wasSuccessful())


if __name__ == "__main__":
    unittest.main()
