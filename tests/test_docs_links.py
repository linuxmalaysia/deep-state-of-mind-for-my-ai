"""
Unit tests for the Diátaxis documentation relative link checking utility.

Ensures that the check_docs_links.py validation logic correctly scans files,
identifies relative links, and flags errors on broken references.
"""
import pathlib
import sys
import unittest

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "tools"))

import check_docs_links  # type: ignore # noqa: E402

class TestDocsLinksValidation(unittest.TestCase):
    """Test the relative link verification logic in tools/check_docs_links.py."""

    def test_diataxis_relative_links_resolve_correctly(self):
        """Verify that the actual docs/ directory has zero broken references."""
        errors = check_docs_links.validate_links()
        self.assertEqual(len(errors), 0, f"Expected 0 broken links in Diátaxis docs, found {len(errors)}: {errors}")

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
