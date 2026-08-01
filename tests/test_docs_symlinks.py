"""
Unit tests for the docs/SECURITY.md and docs/START-HERE.md symlinks.

mkdocs resolves nav entries relative to `docs_dir` (which defaults to the
`docs/` folder). The `mkdocs.yml` nav references top-level docs such as
`README.md`, `START-HERE.md` and `SECURITY.md`, but those canonical files
live at the repository root, not inside `docs/`. Without a corresponding
file inside `docs/`, MkDocs would 404 on these nav entries when building
the site.

This PR adds `docs/SECURITY.md` and `docs/START-HERE.md` as relative
symlinks (mirroring the pre-existing `docs/README.md -> ../README.md`
pattern) that point back to the canonical root-level files, so a single
source of truth is preserved while still satisfying MkDocs' `docs_dir`
requirement.

These tests validate:
1. The two new paths exist and are *real* symlinks (not plain-text
   stand-ins containing the target path as a string, which is how some
   git providers render symlinks in a diff).
2. The symlinks use the expected relative target strings.
3. The symlinks resolve to, and their content matches, the canonical
   root-level files.
4. Git's index records these paths using symlink mode (120000).
5. `mkdocs.yml` still declares the corresponding nav entries that these
   symlinks exist to satisfy.
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
DOCS_DIR = REPO_ROOT / "docs"
GIT_AVAILABLE = shutil.which("git") is not None

# (path relative to docs/, expected relative symlink target, root filename)
SYMLINK_SPECS = [
    ("SECURITY.md", "../SECURITY.md", "SECURITY.md"),
    ("START-HERE.md", "../START-HERE.md", "START-HERE.md"),
]

DIR_SYMLINK_SPECS = [
    (".agents", "../.agents", ".agents"),
    ("playbooks", "../playbooks", "playbooks"),
]


class DocsSymlinkExistenceTests(unittest.TestCase):
    """Basic existence / symlink-type checks."""

    def test_security_symlink_path_exists(self):
        path = DOCS_DIR / "SECURITY.md"
        self.assertTrue(path.exists(), f"Expected {path} to exist")

    def test_start_here_symlink_path_exists(self):
        path = DOCS_DIR / "START-HERE.md"
        self.assertTrue(path.exists(), f"Expected {path} to exist")

    def test_agents_symlink_path_exists(self):
        path = DOCS_DIR / ".agents"
        self.assertTrue(path.exists(), f"Expected {path} to exist")

    def test_playbooks_symlink_path_exists(self):
        path = DOCS_DIR / "playbooks"
        self.assertTrue(path.exists(), f"Expected {path} to exist")

    def test_security_is_a_symlink(self):
        path = DOCS_DIR / "SECURITY.md"
        self.assertTrue(
            path.is_symlink(),
            "docs/SECURITY.md must be a real symlink, not a plain-text "
            "file containing the target path",
        )

    def test_start_here_is_a_symlink(self):
        path = DOCS_DIR / "START-HERE.md"
        self.assertTrue(
            path.is_symlink(),
            "docs/START-HERE.md must be a real symlink, not a plain-text "
            "file containing the target path",
        )

    def test_agents_is_a_symlink(self):
        path = DOCS_DIR / ".agents"
        self.assertTrue(
            path.is_symlink(),
            "docs/.agents must be a real symlink, not a plain-text "
            "file containing the target path",
        )

    def test_playbooks_is_a_symlink(self):
        path = DOCS_DIR / "playbooks"
        self.assertTrue(
            path.is_symlink(),
            "docs/playbooks must be a real symlink, not a plain-text "
            "file containing the target path",
        )


class DocsSymlinkTargetTests(unittest.TestCase):
    """Verify the symlinks point at the expected relative targets."""

    def test_symlink_targets_are_expected_relative_paths(self):
        for doc_relative, expected_target, _ in SYMLINK_SPECS + DIR_SYMLINK_SPECS:
            with self.subTest(doc=doc_relative):
                path = DOCS_DIR / doc_relative
                self.assertEqual(
                    pathlib.Path(pathlib.os.readlink(path)).as_posix(),
                    expected_target,
                )

    def test_symlink_targets_are_relative_not_absolute(self):
        # Relative symlinks keep the repo portable across clone locations
        # (e.g. CI runners, contributor machines).
        for doc_relative, _, _ in SYMLINK_SPECS + DIR_SYMLINK_SPECS:
            with self.subTest(doc=doc_relative):
                path = DOCS_DIR / doc_relative
                target = pathlib.os.readlink(path)
                self.assertFalse(
                    pathlib.PurePath(target).is_absolute(),
                    f"{path} should use a relative symlink target",
                )


class DocsSymlinkResolutionTests(unittest.TestCase):
    """Verify the symlinks resolve to, and mirror, the root-level files/dirs."""

    def test_symlinks_resolve_to_root_level_files(self):
        for doc_relative, _, root_filename in SYMLINK_SPECS:
            with self.subTest(doc=doc_relative):
                path = DOCS_DIR / doc_relative
                self.assertEqual(
                    path.resolve(),
                    (REPO_ROOT / root_filename).resolve(),
                )

    def test_symlinks_do_not_dangle(self):
        for doc_relative, _, _ in SYMLINK_SPECS:
            with self.subTest(doc=doc_relative):
                path = DOCS_DIR / doc_relative
                self.assertTrue(
                    path.resolve().is_file(),
                    f"{path} resolves to a path that is not a regular file",
                )

    def test_dir_symlinks_resolve_to_root_level_dirs(self):
        for doc_relative, _, root_dirname in DIR_SYMLINK_SPECS:
            with self.subTest(doc=doc_relative):
                path = DOCS_DIR / doc_relative
                self.assertEqual(
                    path.resolve(),
                    (REPO_ROOT / root_dirname).resolve(),
                )

    def test_dir_symlinks_do_not_dangle(self):
        for doc_relative, _, _ in DIR_SYMLINK_SPECS:
            with self.subTest(doc=doc_relative):
                path = DOCS_DIR / doc_relative
                self.assertTrue(
                    path.resolve().is_dir(),
                    f"{path} resolves to a path that is not a directory",
                )

    def test_symlink_content_matches_root_file_content(self):
        for doc_relative, _, root_filename in SYMLINK_SPECS:
            with self.subTest(doc=doc_relative):
                via_symlink = (DOCS_DIR / doc_relative).read_text(encoding="utf-8")
                via_root = (REPO_ROOT / root_filename).read_text(encoding="utf-8")
                self.assertEqual(via_symlink, via_root)

    def test_root_files_are_non_empty(self):
        # Guards against the symlink "succeeding" by pointing at an
        # accidentally-empty root file.
        for _, _, root_filename in SYMLINK_SPECS:
            with self.subTest(root_filename=root_filename):
                content = (REPO_ROOT / root_filename).read_text(encoding="utf-8")
                self.assertTrue(content.strip())


@unittest.skipUnless(GIT_AVAILABLE, "git executable not available")
class DocsSymlinkGitIndexTests(unittest.TestCase):
    """Verify Git itself tracks these paths using symlink mode (120000)."""

    @classmethod
    def setUpClass(cls):
        result = subprocess.run(
            ["git", "ls-files", "-s", "docs/SECURITY.md", "docs/START-HERE.md", "docs/.agents", "docs/playbooks"],
            cwd=REPO_ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )
        cls.entries = {}
        for line in result.stdout.splitlines():
            # Format: "<mode> <sha> <stage>\t<path>"
            meta, path = line.split("\t", 1)
            mode = meta.split(" ", 1)[0]
            cls.entries[path] = mode

    def test_security_tracked_with_symlink_mode(self):
        self.assertEqual(self.entries.get("docs/SECURITY.md"), "120000")

    def test_start_here_tracked_with_symlink_mode(self):
        self.assertEqual(self.entries.get("docs/START-HERE.md"), "120000")

    def test_agents_tracked_with_symlink_mode(self):
        self.assertEqual(self.entries.get("docs/.agents"), "120000")

    def test_playbooks_tracked_with_symlink_mode(self):
        self.assertEqual(self.entries.get("docs/playbooks"), "120000")

    def test_all_new_symlinks_present_in_index(self):
        self.assertEqual(
            set(self.entries.keys()),
            {"docs/SECURITY.md", "docs/START-HERE.md", "docs/.agents", "docs/playbooks"},
        )


class MkdocsNavReferencesTests(unittest.TestCase):
    """Verify mkdocs.yml still declares the nav entries these symlinks fix."""

    @classmethod
    def setUpClass(cls):
        cls.content = (REPO_ROOT / "mkdocs.yml").read_text(encoding="utf-8")

    def test_nav_declares_security_policy_entry(self):
        self.assertRegex(self.content, r"Security Policy:\s*SECURITY\.md")

    def test_nav_declares_start_here_entry(self):
        self.assertRegex(self.content, r"START HERE:\s*START-HERE\.md")

    def test_nav_entries_resolve_within_docs_dir(self):
        # mkdocs resolves bare "SECURITY.md" / "START-HERE.md" nav values
        # relative to docs_dir; confirm the resolved paths actually exist
        # thanks to the new symlinks.
        for nav_value in ("SECURITY.md", "START-HERE.md"):
            with self.subTest(nav_value=nav_value):
                self.assertTrue((DOCS_DIR / nav_value).exists())


if __name__ == "__main__":
    unittest.main()