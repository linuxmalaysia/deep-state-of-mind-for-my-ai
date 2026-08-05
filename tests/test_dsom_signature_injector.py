# ==============================================================================
# Protocol    : Deep State of Mind (DSOM) For My AI
# Author      : Harisfazillah Jamel (LinuxMalaysia)
# Timestamp   : 2026-08-05
# License     : GNU General Public License v3.0
# Standard    : UK English | DBP-standard Bahasa Melayu Malaysia (Piawai)
# ==============================================================================
"""
Unit tests for the dsom-signature-injector skill's `inject_signature` function.

This PR extended `inject_signature()` in
`.agents/skills/dsom-signature-injector/scripts/inject.py` so that it also
recognises Python (`.py`) files:

1. When walking a directory, `.py` files are now included in the set of
   files that get processed (previously only `.md`, `.sh`, `.ps1`, `.yml`,
   and `.yaml` were considered).
2. When injecting the signature, `.py` files are now handled by the same
   branch as `.sh`/`.yml`/`.yaml` files: a "#"-style comment header is
   prepended (after a leading shebang line, if present), rather than being
   left untouched or mishandled by the Markdown/PowerShell branches.

These tests exercise `inject_signature` directly against temporary files
and directories so that the real repository tree is never modified.
"""
import importlib.util
import pathlib
import tempfile
import unittest


def _find_repo_root(start: pathlib.Path) -> pathlib.Path:
    """Locate the repository root from a starting path."""
    current = start.resolve()
    for parent in [current, *current.parents]:
        if (parent / ".git").exists():
            return parent
    raise RuntimeError("Could not locate repository root (.git not found)")


REPO_ROOT = _find_repo_root(pathlib.Path(__file__).parent)
INJECT_SCRIPT_PATH = (
    REPO_ROOT
    / ".agents"
    / "skills"
    / "dsom-signature-injector"
    / "scripts"
    / "inject.py"
)


def _load_inject_module():
    """Load the inject.py module directly from its file path.

    The containing directory name (`dsom-signature-injector`) contains
    hyphens and is therefore not importable as a regular Python package, so
    the module is loaded dynamically via importlib.
    """
    spec = importlib.util.spec_from_file_location(
        "dsom_signature_inject", INJECT_SCRIPT_PATH
    )
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


inject_module = _load_inject_module()
inject_signature = inject_module.inject_signature

SIGNATURE_MARKER = "Deep State of Mind (DSOM) For My AI Protocol"
# The "#"-style header used for .sh/.yml/.py files (see get_sh_yml_header)
# renders the protocol name without a trailing "Protocol" suffix, unlike
# the Markdown footer, so a distinct marker is needed to check for it.
HEADER_PROTOCOL_LINE = "Protocol    : Deep State of Mind (DSOM) For My AI"
SH_YML_HEADER_START = "# =============================================================================="


class InjectSignatureScriptTests(unittest.TestCase):
    """Sanity checks that the script file itself exists and is loadable."""

    def test_inject_script_exists(self):
        self.assertTrue(
            INJECT_SCRIPT_PATH.is_file(),
            f"Expected {INJECT_SCRIPT_PATH} to exist",
        )

    def test_supported_extensions_include_py_for_directory_walk(self):
        source = INJECT_SCRIPT_PATH.read_text(encoding="utf-8")
        self.assertIn(
            "('.md', '.sh', '.ps1', '.yml', '.yaml', '.py')",
            source,
            "Expected directory walk file filter to include '.py'",
        )

    def test_supported_extensions_include_py_for_header_injection(self):
        source = INJECT_SCRIPT_PATH.read_text(encoding="utf-8")
        self.assertIn(
            "('.sh', '.yml', '.yaml', '.py')",
            source,
            "Expected header-injection branch to include '.py'",
        )


class InjectSignatureSinglePyFileTests(unittest.TestCase):
    """Behaviour of inject_signature() when called directly on a .py file."""

    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmpdir.cleanup)
        self.tmp_path = pathlib.Path(self._tmpdir.name)

    def _write(self, name: str, content: str) -> pathlib.Path:
        target = self.tmp_path / name
        target.write_text(content, encoding="utf-8")
        return target

    def test_prepends_comment_header_to_py_file_without_shebang(self):
        target = self._write("sample.py", "import os\n\nprint('hello')\n")

        inject_signature(str(target))

        result = target.read_text(encoding="utf-8")
        self.assertTrue(
            result.startswith("# "),
            "Expected the DSOM header to be prepended as '#' comments",
        )
        self.assertIn(HEADER_PROTOCOL_LINE, result)
        self.assertIn(SH_YML_HEADER_START, result)
        # Original content must be fully preserved after the header.
        self.assertIn("import os\n\nprint('hello')\n", result)

    def test_inserts_header_after_shebang_line(self):
        original = "#!/usr/bin/env python3\nimport sys\nprint(sys.argv)\n"
        target = self._write("with_shebang.py", original)

        inject_signature(str(target))

        result = target.read_text(encoding="utf-8")
        lines = result.splitlines()
        self.assertEqual(
            lines[0],
            "#!/usr/bin/env python3",
            "Expected the shebang to remain the first line",
        )
        self.assertIn(HEADER_PROTOCOL_LINE, result)
        # The rest of the original file content must still be present.
        self.assertIn("import sys\nprint(sys.argv)\n", result)

    def test_skips_py_file_if_signature_already_present(self):
        original = f"# {SIGNATURE_MARKER}\nprint('already signed')\n"
        target = self._write("already_signed.py", original)

        inject_signature(str(target))

        result = target.read_text(encoding="utf-8")
        self.assertEqual(
            result, original, "Expected file to be left untouched when already signed"
        )

    def test_header_uses_hash_comment_style_not_powershell_style(self):
        target = self._write("style_check.py", "x = 1\n")

        inject_signature(str(target))

        result = target.read_text(encoding="utf-8")
        self.assertNotIn(
            "<#", result, "Python files must not receive the PowerShell-style header"
        )
        self.assertIn("# Author      : Harisfazillah Jamel (LinuxMalaysia)", result)


class InjectSignatureDirectoryWalkTests(unittest.TestCase):
    """Behaviour of inject_signature() when called on a directory tree."""

    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmpdir.cleanup)
        self.tmp_path = pathlib.Path(self._tmpdir.name)

    def test_py_files_are_discovered_and_signed_in_directory_walk(self):
        py_file = self.tmp_path / "module.py"
        py_file.write_text("def foo():\n    return 1\n", encoding="utf-8")

        inject_signature(str(self.tmp_path))

        result = py_file.read_text(encoding="utf-8")
        self.assertIn(HEADER_PROTOCOL_LINE, result)
        self.assertIn("def foo():\n    return 1\n", result)

    def test_unsupported_extension_is_not_modified(self):
        # Negative/regression case: files with extensions outside the
        # supported set (still, after adding '.py') must be left untouched.
        txt_file = self.tmp_path / "notes.txt"
        original = "just some plain notes\n"
        txt_file.write_text(original, encoding="utf-8")

        inject_signature(str(self.tmp_path))

        self.assertEqual(txt_file.read_text(encoding="utf-8"), original)

    def test_py_files_inside_git_directory_are_skipped(self):
        git_dir = self.tmp_path / ".git"
        git_dir.mkdir()
        py_in_git = git_dir / "hook.py"
        original = "print('a git hook')\n"
        py_in_git.write_text(original, encoding="utf-8")

        inject_signature(str(self.tmp_path))

        self.assertEqual(
            py_in_git.read_text(encoding="utf-8"),
            original,
            "Expected .py files under a .git directory to remain untouched",
        )

    def test_mixed_supported_files_all_signed(self):
        py_file = self.tmp_path / "script.py"
        py_file.write_text("x = 1\n", encoding="utf-8")
        md_file = self.tmp_path / "doc.md"
        md_file.write_text("# Title\n\nBody text.\n", encoding="utf-8")

        inject_signature(str(self.tmp_path))

        self.assertIn(HEADER_PROTOCOL_LINE, py_file.read_text(encoding="utf-8"))
        self.assertIn(SIGNATURE_MARKER, md_file.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()