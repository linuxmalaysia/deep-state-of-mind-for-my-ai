"""
Unit tests for the .gitignore change that adds a `site/` entry.

The `site/` directory is the default output directory produced by
`mkdocs build` (see .github/workflows/gh-pages.yml). It should never be
committed to the repository, but must not interfere with any of the
pre-existing negation ("un-ignore") rules for other tracked paths.

These tests exercise real `git check-ignore` behavior (rather than a
hand-rolled glob matcher) so that they validate the exact semantics Git
itself will apply.
"""
import pathlib
import shutil
import subprocess
import unittest


def _find_repo_root(start: pathlib.Path) -> pathlib.Path:
    current = start.resolve()
    for parent in [current, *current.parents]:
        if (parent / ".git").exists():
            return parent
    raise RuntimeError("Could not locate repository root (.git not found)")


REPO_ROOT = _find_repo_root(pathlib.Path(__file__).parent)
GITIGNORE_PATH = REPO_ROOT / ".gitignore"
GIT_AVAILABLE = shutil.which("git") is not None


def _is_ignored(relative_path: str) -> bool:
    """Return True if `git check-ignore` reports the path as ignored."""
    result = subprocess.run(
        ["git", "check-ignore", "-q", relative_path],
        cwd=REPO_ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    if result.returncode not in (0, 1):
        raise RuntimeError(
            f"git check-ignore failed unexpectedly (exit={result.returncode}) "
            f"for path {relative_path!r}"
        )
    return result.returncode == 0


class GitignoreFileTests(unittest.TestCase):
    def test_gitignore_exists(self):
        self.assertTrue(GITIGNORE_PATH.is_file())

    def test_gitignore_declares_site_entry(self):
        lines = GITIGNORE_PATH.read_text(encoding="utf-8").splitlines()
        self.assertIn(
            "site/",
            [line.strip() for line in lines],
            "Expected a 'site/' entry to ignore the MkDocs build output",
        )


@unittest.skipUnless(GIT_AVAILABLE, "git executable not available")
class GitignoreSiteDirectoryBehaviorTests(unittest.TestCase):
    """Verify the built MkDocs `site/` output is actually ignored by Git."""

    def test_top_level_site_file_is_ignored(self):
        self.assertTrue(_is_ignored("site/index.html"))

    def test_nested_site_asset_is_ignored(self):
        self.assertTrue(_is_ignored("site/assets/css/style.css"))

    def test_site_directory_itself_is_ignored(self):
        self.assertTrue(_is_ignored("site/"))

    def test_site_directory_nested_under_another_path_is_ignored(self):
        # 'site/' with no leading slash matches a directory named 'site'
        # at any depth in the tree.
        self.assertTrue(_is_ignored("docs/site/file.txt"))

    def test_similarly_named_directory_is_not_ignored(self):
        # Guards against overly broad matching, e.g. accidentally matching
        # any path containing the substring 'site'.
        self.assertFalse(_is_ignored("notsite/index.html"))
        self.assertFalse(_is_ignored("website/index.html"))

    def test_file_named_site_without_slash_is_not_matched_by_directory_rule(self):
        # A plain file literally named 'site' (no trailing slash in the
        # pattern in .gitignore refers to a directory) should not match
        # via this rule; unrelated top-level file names containing "site"
        # as a prefix should also be untouched.
        self.assertFalse(_is_ignored("sitemap.xml"))


@unittest.skipUnless(GIT_AVAILABLE, "git executable not available")
class GitignoreRegressionTests(unittest.TestCase):
    """Ensure the new `site/` rule doesn't regress other existing rules."""

    def test_docs_markdown_still_tracked(self):
        # !docs/*.md negation must still take effect after adding site/.
        self.assertFalse(_is_ignored("docs/index.md"))

    def test_agents_brain_markdown_still_tracked(self):
        self.assertFalse(_is_ignored(".agents/brain/example.md"))

    def test_other_preexisting_ignores_still_effective(self):
        self.assertTrue(_is_ignored("notes.tmp"))
        self.assertTrue(_is_ignored("backup.bak"))
        self.assertTrue(_is_ignored("secrets.key"))


if __name__ == "__main__":
    unittest.main()