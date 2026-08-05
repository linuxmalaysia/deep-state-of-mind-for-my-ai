# ==============================================================================
# Protocol    : Deep State of Mind (DSOM) For My AI
# Author      : Harisfazillah Jamel (LinuxMalaysia)
# Timestamp   : 2026-08-05
# License     : GNU General Public License v3.0
# Standard    : UK English | DBP-standard Bahasa Melayu Malaysia (Piawai)
# ==============================================================================
"""
Unit tests for the DSOM Signature Injector script
(`.agents/skills/dsom-signature-injector/scripts/inject.py`).

This PR extended `inject_signature()` so that Python (`.py`) files are now
recognised both when walking a directory and when deciding which comment
style (shebang/hash-style header) to apply. These tests verify:

1. A single `.py` file passed directly is signed with the SH/YAML-style
   hash-comment header (not the PowerShell block-comment header).
2. A shebang line (`#!...`) on the first line of a `.py` file is preserved
   as the very first line, with the header inserted immediately after it.
3. Files whose content already contains the exact DSOM skip-trigger phrase
   ("...For My AI Protocol") are left untouched (idempotency guard).
4. Walking a directory now picks up `.py` files alongside the previously
   supported extensions, while files with unsupported extensions are
   still ignored.
5. Directories named `.git` are still skipped during the directory walk.
6. Characterisation of the pre-existing duplicate-detection quirk: since
   the SH/YAML/PY header text reads "Protocol    : Deep State of Mind
   (DSOM) For My AI" (label-first, no trailing "Protocol"), it does not
   itself match the skip-trigger phrase, so a freshly generated header is
   not recognised as a signature on a second pass.
"""
import importlib.util
import os
import pathlib
import shutil
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
    """Dynamically load inject.py as a module (its parent dirs are not valid
    Python package names, so a normal import is not possible)."""
    spec = importlib.util.spec_from_file_location("dsom_inject", INJECT_SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


inject = _load_inject_module()

# Generic phrase present in every header/footer variant (.md, .sh/.yml/.py,
# and .ps1), regardless of word order.
HEADER_MARKER = "Deep State of Mind (DSOM) For My AI"

# The exact phrase inject_signature() checks for to decide whether a file is
# already signed. Present verbatim in the Markdown footer and the PowerShell
# header, but NOT in the SH/YAML/PY hash-comment header (see module docstring
# point 6 above).
SKIP_TRIGGER_PHRASE = "Deep State of Mind (DSOM) For My AI Protocol"


class InjectScriptExistsTests(unittest.TestCase):
    """Sanity check that the script under test is present and loadable."""

    def test_inject_script_exists(self):
        self.assertTrue(INJECT_SCRIPT_PATH.is_file())

    def test_module_exposes_inject_signature(self):
        self.assertTrue(hasattr(inject, "inject_signature"))
        self.assertTrue(callable(inject.inject_signature))


class InjectSignatureSinglePyFileTests(unittest.TestCase):
    """Verify behaviour when a single .py file is passed directly."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def _write(self, name, content):
        path = os.path.join(self.tmpdir, name)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return path

    def _read(self, path):
        with open(path, encoding="utf-8") as f:
            return f.read()

    def test_prepends_hash_style_header_to_py_file(self):
        path = self._write("sample.py", "print('hello')\n")
        inject.inject_signature(path)
        content = self._read(path)
        self.assertIn(HEADER_MARKER, content)
        self.assertIn("print('hello')", content)
        # Header must precede the original code.
        self.assertLess(content.index(HEADER_MARKER), content.index("print('hello')"))

    def test_py_header_uses_hash_comments_not_powershell_block(self):
        path = self._write("style_check.py", "value = 42\n")
        inject.inject_signature(path)
        content = self._read(path)
        self.assertIn("# Protocol    : Deep State of Mind (DSOM) For My AI", content)
        self.assertNotIn("<#", content)
        self.assertNotIn(".SYNOPSIS", content)

    def test_shebang_line_preserved_as_first_line(self):
        path = self._write("script.py", "#!/usr/bin/env python3\nprint('hi')\n")
        inject.inject_signature(path)
        with open(path, encoding="utf-8") as f:
            lines = f.readlines()
        self.assertEqual(lines[0], "#!/usr/bin/env python3\n")
        content = "".join(lines)
        self.assertIn(HEADER_MARKER, content)
        self.assertLess(content.index("#!/usr/bin/env python3"), content.index(HEADER_MARKER))
        self.assertIn("print('hi')", content)

    def test_already_signed_py_file_is_left_unchanged(self):
        original = (
            f"# {SKIP_TRIGGER_PHRASE} header already here\n"
            "print('unchanged')\n"
        )
        path = self._write("already_signed.py", original)
        inject.inject_signature(path)
        self.assertEqual(self._read(path), original)

    def test_repeated_invocation_duplicates_header_on_py_files(self):
        """Characterisation test for a pre-existing quirk (not introduced by
        this PR): the SH/YAML/PY header does not contain the exact
        SKIP_TRIGGER_PHRASE, so inject_signature() cannot detect that a .py
        file it previously signed is already signed, and prepends a second
        header block on a second invocation."""
        path = self._write("run_twice.py", "print('once')\n")
        inject.inject_signature(path)
        first_pass = self._read(path)
        inject.inject_signature(path)
        second_pass = self._read(path)
        self.assertNotEqual(first_pass, second_pass)
        self.assertEqual(second_pass.count(HEADER_MARKER), 2)
        self.assertTrue(second_pass.endswith(first_pass))


class InjectSignatureDirectoryWalkTests(unittest.TestCase):
    """Verify directory traversal now includes .py files."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def _write(self, rel_path, content):
        full_path = os.path.join(self.tmpdir, rel_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)
        return full_path

    def _read(self, rel_path):
        with open(os.path.join(self.tmpdir, rel_path), encoding="utf-8") as f:
            return f.read()

    def test_py_files_are_signed_when_walking_a_directory(self):
        self._write("module_a.py", "x = 1\n")
        inject.inject_signature(self.tmpdir)
        self.assertIn(HEADER_MARKER, self._read("module_a.py"))

    def test_unsupported_extensions_are_left_untouched(self):
        self._write("notes.txt", "should not be touched\n")
        inject.inject_signature(self.tmpdir)
        self.assertEqual(self._read("notes.txt"), "should not be touched\n")

    def test_git_directory_is_skipped_during_walk(self):
        self._write(os.path.join(".git", "hook.py"), "raise SystemExit\n")
        # Should not raise, and the file inside .git must remain untouched.
        inject.inject_signature(self.tmpdir)
        self.assertNotIn(
            HEADER_MARKER, self._read(os.path.join(".git", "hook.py"))
        )

    def test_mixed_directory_only_signs_supported_extensions(self):
        self._write("script.sh", "echo hi\n")
        self._write("module.py", "y = 2\n")
        self._write("data.json", '{"key": "value"}\n')
        inject.inject_signature(self.tmpdir)
        self.assertIn(HEADER_MARKER, self._read("script.sh"))
        self.assertIn(HEADER_MARKER, self._read("module.py"))
        self.assertNotIn(HEADER_MARKER, self._read("data.json"))


class InjectSignatureEdgeCaseTests(unittest.TestCase):
    """Boundary/negative cases for inject_signature()."""

    def test_nonexistent_path_does_not_raise(self):
        missing_path = os.path.join(tempfile.gettempdir(), "does-not-exist-dsom-test")
        # Neither a file nor a directory: the function should simply have
        # nothing to process and must not raise.
        try:
            inject.inject_signature(missing_path)
        except Exception as exc:  # pragma: no cover - defensive assertion
            self.fail(f"inject_signature raised unexpectedly for a missing path: {exc}")

    def test_markdown_file_still_receives_footer_not_header(self):
        tmpdir = tempfile.mkdtemp()
        try:
            path = os.path.join(tmpdir, "doc.md")
            with open(path, "w", encoding="utf-8") as f:
                f.write("# Title\n\nBody text.\n")
            inject.inject_signature(path)
            with open(path, encoding="utf-8") as f:
                content = f.read()
            self.assertIn(SKIP_TRIGGER_PHRASE, content)
            # Markdown uses an appended footer, so the original body must
            # precede the injected signature (opposite of the .py/.sh case).
            self.assertLess(content.index("Body text."), content.index(SKIP_TRIGGER_PHRASE))
        finally:
            shutil.rmtree(tmpdir, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()