"""
Unit tests for the Diátaxis documentation relative link checking utility.

Ensures that the check_docs_links.py validation logic correctly scans files,
identifies relative links, and flags errors on broken references.
"""
import pathlib
import sys
import tempfile
import unittest

# Resolve repo root dynamically to avoid global namespace pollution
_current_dir = pathlib.Path(__file__).resolve().parent
_repo_root = _current_dir.parent
if str(_repo_root / "tools") not in sys.path:
    sys.path.insert(0, str(_repo_root / "tools"))

import check_docs_links  # type: ignore # noqa: E402

class TestDocsLinksValidation(unittest.TestCase):
    """Test the relative link verification logic in tools/check_docs_links.py."""

    def test_diataxis_relative_links_resolve_correctly(self):
        """Verify that the actual docs/ directory has zero broken references."""
        # Inject the real repository root dynamically
        real_root = _repo_root
        errors = check_docs_links.validate_links(real_root)
        self.assertEqual(len(errors), 0, f"Expected 0 broken links in Diátaxis docs, found {len(errors)}: {errors}")

    def test_broken_link_in_fixture(self):
        """Verify that a broken relative link inside a scanned directory is caught."""
        with tempfile.TemporaryDirectory() as tmpdir:
            temp_root = pathlib.Path(tmpdir)

            # Create target scanned quadrant docs/tutorials
            docs_dir = temp_root / "docs"
            docs_dir.mkdir()
            tutorials_dir = docs_dir / "tutorials"
            tutorials_dir.mkdir()

            # Create a file with a broken relative link pointing to non-existent sibling
            test_file = tutorials_dir / "test.md"
            test_file.write_text("Here is a [Broken Link](nonexistent.md)", encoding="utf-8")

            errors = check_docs_links.validate_links(temp_root)
            self.assertEqual(len(errors), 1)
            self.assertIn("Broken link 'nonexistent.md'", errors[0])

    def test_out_of_bounds_link_in_fixture(self):
        """Verify that a relative link resolving outside the repository root is caught."""
        with tempfile.TemporaryDirectory() as tmpdir:
            temp_root = pathlib.Path(tmpdir)

            docs_dir = temp_root / "docs"
            docs_dir.mkdir()
            tutorials_dir = docs_dir / "tutorials"
            tutorials_dir.mkdir()

            # Create a file with a link that escapes the repository root
            test_file = tutorials_dir / "test.md"
            test_file.write_text("Here is an [Out-of-Bounds Link](../../../../outside_repo.md)", encoding="utf-8")

            errors = check_docs_links.validate_links(temp_root)
            self.assertEqual(len(errors), 1)
            self.assertIn("goes outside repository bounds", errors[0])

    def test_is_external_or_special_identifies_special_schemes(self):
        """Verify that external or special URL patterns are correctly recognized."""
        special_links = [
            "http://example.com",
            "https://linuxmalaysia.github.io",
            "mailto:admin@linuxmalaysia.github.io",
            "ftp://ftp.example.com",
            "#some-anchor",
            "file:///START-HERE.md"
        ]
        for url in special_links:
            with self.subTest(url=url):
                self.assertTrue(check_docs_links.is_external_or_special(url))

    def test_is_external_or_special_allows_relative_links(self):
        """Verify that standard relative file paths are not treated as special/external."""
        relative_links = [
            "getting-started.md",
            "../how-to/run-fastmcp-server.md",
            "reference/generate_sitemaps.md"
        ]
        for url in relative_links:
            with self.subTest(url=url):
                self.assertFalse(check_docs_links.is_external_or_special(url))

if __name__ == "__main__":
    unittest.main()
