"""
Unit tests for the Diátaxis documentation relative link checking utility.

Ensures that the check_docs_links.py validation logic correctly scans files,
identifies relative links, and flags errors on broken references.
"""
import io
import pathlib
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from unittest import mock

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

    def test_valid_relative_link_produces_no_errors(self):
        """Verify that a correctly resolving relative link raises no errors."""
        with tempfile.TemporaryDirectory() as tmpdir:
            temp_root = pathlib.Path(tmpdir)
            tutorials_dir = temp_root / "docs" / "tutorials"
            tutorials_dir.mkdir(parents=True)

            (tutorials_dir / "index.md").write_text("# Index", encoding="utf-8")
            (tutorials_dir / "test.md").write_text(
                "See [Overview](index.md) for details.", encoding="utf-8"
            )

            errors = check_docs_links.validate_links(temp_root)
            self.assertEqual(errors, [])

    def test_link_with_anchor_fragment_resolves_against_target_file(self):
        """Verify that anchor fragments are stripped before resolving the file path."""
        with tempfile.TemporaryDirectory() as tmpdir:
            temp_root = pathlib.Path(tmpdir)
            how_to_dir = temp_root / "docs" / "how-to"
            how_to_dir.mkdir(parents=True)

            (how_to_dir / "target.md").write_text("# Target", encoding="utf-8")
            (how_to_dir / "test.md").write_text(
                "See [Section](target.md#some-section) for details.", encoding="utf-8"
            )

            errors = check_docs_links.validate_links(temp_root)
            self.assertEqual(errors, [])

    def test_pure_anchor_link_is_skipped(self):
        """A link that is only an in-page anchor (e.g. '#section') must not be flagged."""
        with tempfile.TemporaryDirectory() as tmpdir:
            temp_root = pathlib.Path(tmpdir)
            reference_dir = temp_root / "docs" / "reference"
            reference_dir.mkdir(parents=True)

            (reference_dir / "test.md").write_text(
                "Jump to [Section](#some-section) below.", encoding="utf-8"
            )

            errors = check_docs_links.validate_links(temp_root)
            self.assertEqual(errors, [])

    def test_multiple_links_only_broken_ones_are_reported(self):
        """Verify that only the broken links among several are reported, each individually."""
        with tempfile.TemporaryDirectory() as tmpdir:
            temp_root = pathlib.Path(tmpdir)
            explanation_dir = temp_root / "docs" / "explanation"
            explanation_dir.mkdir(parents=True)

            (explanation_dir / "index.md").write_text("# Index", encoding="utf-8")
            (explanation_dir / "test.md").write_text(
                "Valid: [Index](index.md). "
                "Broken one: [Missing1](missing1.md). "
                "Broken two: [Missing2](missing2.md).",
                encoding="utf-8",
            )

            errors = check_docs_links.validate_links(temp_root)
            self.assertEqual(len(errors), 2)
            self.assertTrue(any("missing1.md" in e for e in errors))
            self.assertTrue(any("missing2.md" in e for e in errors))

    def test_summary_md_file_target_is_scanned_directly(self):
        """Verify that docs/SUMMARY.md itself (a file, not a directory) is scanned."""
        with tempfile.TemporaryDirectory() as tmpdir:
            temp_root = pathlib.Path(tmpdir)
            docs_dir = temp_root / "docs"
            docs_dir.mkdir()

            (docs_dir / "SUMMARY.md").write_text(
                "* [Broken](nonexistent.md)", encoding="utf-8"
            )

            errors = check_docs_links.validate_links(temp_root)
            self.assertEqual(len(errors), 1)
            self.assertIn("SUMMARY.md", errors[0])

    def test_files_outside_target_quadrants_are_not_scanned(self):
        """Verify that markdown files outside the Diátaxis quadrant paths are ignored."""
        with tempfile.TemporaryDirectory() as tmpdir:
            temp_root = pathlib.Path(tmpdir)
            other_dir = temp_root / "docs" / "governance"
            other_dir.mkdir(parents=True)

            # This link is broken, but the governance/ directory is not one of
            # the scanned Diátaxis quadrant paths, so it should be ignored.
            (other_dir / "test.md").write_text(
                "[Broken](nonexistent.md)", encoding="utf-8"
            )

            errors = check_docs_links.validate_links(temp_root)
            self.assertEqual(errors, [])

    def test_unreadable_file_reports_an_error(self):
        """Verify that a file which raises on read is reported as an error, not silently skipped."""
        with tempfile.TemporaryDirectory() as tmpdir:
            temp_root = pathlib.Path(tmpdir)
            tutorials_dir = temp_root / "docs" / "tutorials"
            tutorials_dir.mkdir(parents=True)
            bad_file = tutorials_dir / "bad.md"
            bad_file.write_text("placeholder", encoding="utf-8")

            original_read_text = pathlib.Path.read_text

            def _raise_for_bad_file(self, *args, **kwargs):
                if self == bad_file:
                    raise UnicodeDecodeError("utf-8", b"\xff", 0, 1, "bad byte")
                return original_read_text(self, *args, **kwargs)

            with mock.patch.object(pathlib.Path, "read_text", _raise_for_bad_file):
                errors = check_docs_links.validate_links(temp_root)

            self.assertEqual(len(errors), 1)
            self.assertIn("Could not read file", errors[0])

    def test_find_repo_root_locates_git_directory(self):
        """Verify find_repo_root() walks up parents to find the nearest .git directory."""
        result = check_docs_links.find_repo_root()
        self.assertTrue((result / ".git").exists())
        self.assertEqual(result, _repo_root)

    def test_find_repo_root_falls_back_when_no_git_found(self):
        """Verify find_repo_root() falls back to the script's grandparent directory
        when no ancestor contains a `.git` directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            fake_tools_dir = pathlib.Path(tmpdir) / "fakeproject" / "tools"
            fake_tools_dir.mkdir(parents=True)
            fake_script = fake_tools_dir / "check_docs_links.py"
            fake_script.write_text("", encoding="utf-8")

            with mock.patch.object(check_docs_links, "__file__", str(fake_script)):
                result = check_docs_links.find_repo_root()

            self.assertEqual(result, fake_tools_dir.parent)


class TestDocsLinksMain(unittest.TestCase):
    """Test the CLI entry point (`main()`) exit codes and output."""

    def test_main_exits_zero_and_prints_success_when_no_broken_links(self):
        with mock.patch.object(check_docs_links, "find_repo_root", return_value=_repo_root), \
                mock.patch.object(check_docs_links, "validate_links", return_value=[]):
            buffer = io.StringIO()
            with redirect_stdout(buffer):
                with self.assertRaises(SystemExit) as ctx:
                    check_docs_links.main()

        self.assertEqual(ctx.exception.code, 0)
        self.assertIn("validated successfully", buffer.getvalue())

    def test_main_exits_one_and_prints_errors_when_broken_links_found(self):
        fake_errors = ["In docs/tutorials/test.md: Broken link 'nonexistent.md'"]
        with mock.patch.object(check_docs_links, "find_repo_root", return_value=_repo_root), \
                mock.patch.object(check_docs_links, "validate_links", return_value=fake_errors):
            buffer = io.StringIO()
            with redirect_stdout(buffer):
                with self.assertRaises(SystemExit) as ctx:
                    check_docs_links.main()

        self.assertEqual(ctx.exception.code, 1)
        output = buffer.getvalue()
        self.assertIn("Broken Links", output)
        self.assertIn("nonexistent.md", output)
        self.assertIn("Total broken references found: 1", output)


if __name__ == "__main__":
    unittest.main()
