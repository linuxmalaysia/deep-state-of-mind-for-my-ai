"""
Unit tests for `.agents/skills/dsom-signature-injector/scripts/inject.py`.

This PR extends `inject_signature()` so that Python (`.py`) files are:
1. Discovered during a directory walk (previously only `.md`, `.sh`,
   `.ps1`, `.yml`, and `.yaml` files were picked up).
2. Processed using the same shell/YAML-style comment header as `.sh`,
   `.yml`, and `.yaml` files (a `#`-prefixed block, inserted after a
   leading shebang line if present) rather than the Markdown footer or
   PowerShell block-comment styles.

These tests exercise the module in isolation using temporary
directories so that the real repository tree is never modified.
"""
import importlib.util
import os
import pathlib
import tempfile
import unittest


def _find_repo_root(start: pathlib.Path) -> pathlib.Path:
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

SIGNATURE_MARKER = "Deep State of Mind (DSOM) For My AI"


def _load_inject_module():
    """Load inject.py as a standalone module (its directory contains dashes)."""
    spec = importlib.util.spec_from_file_location(
        "dsom_signature_injector_inject", INJECT_SCRIPT_PATH
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class InjectScriptFileTests(unittest.TestCase):
    def test_script_exists(self):
        self.assertTrue(INJECT_SCRIPT_PATH.is_file(), f"Expected {INJECT_SCRIPT_PATH} to exist")


class InjectSignaturePythonSupportTests(unittest.TestCase):
    """Regression/behaviour tests for the newly added `.py` extension support."""

    @classmethod
    def setUpClass(cls):
        cls.inject = _load_inject_module()

    def test_py_file_passed_directly_is_processed(self):
        with tempfile.TemporaryDirectory() as tmp:
            filepath = os.path.join(tmp, "script.py")
            with open(filepath, "w", encoding="utf-8") as fh:
                fh.write("print('hello')\n")

            self.inject.inject_signature(filepath)

            content = pathlib.Path(filepath).read_text(encoding="utf-8")
            self.assertIn(SIGNATURE_MARKER, content)
            self.assertIn("print('hello')", content)

    def test_py_file_is_discovered_during_directory_walk(self):
        # Before this PR, .py files were not part of the extension tuple
        # used by os.walk() and would have been silently skipped.
        with tempfile.TemporaryDirectory() as tmp:
            filepath = os.path.join(tmp, "module.py")
            with open(filepath, "w", encoding="utf-8") as fh:
                fh.write("x = 1\n")

            self.inject.inject_signature(tmp)

            content = pathlib.Path(filepath).read_text(encoding="utf-8")
            self.assertIn(SIGNATURE_MARKER, content)

    def test_py_file_uses_sh_yml_header_style_not_markdown_or_powershell(self):
        with tempfile.TemporaryDirectory() as tmp:
            filepath = os.path.join(tmp, "script.py")
            with open(filepath, "w", encoding="utf-8") as fh:
                fh.write("print('hello')\n")

            self.inject.inject_signature(filepath)

            content = pathlib.Path(filepath).read_text(encoding="utf-8")
            # Shell/YAML header style: '#'-prefixed block, prepended.
            self.assertTrue(content.startswith("# =="))
            self.assertIn("# Protocol    : Deep State of Mind (DSOM) For My AI", content)
            # Must NOT use the PowerShell comment-block style.
            self.assertNotIn("<#", content)
            self.assertNotIn(".SYNOPSIS", content)
            # Must NOT use the Markdown footer style (appended, not prepended).
            self.assertFalse(content.rstrip().endswith("GNU General Public License v3.0*"))

    def test_py_file_with_shebang_inserts_header_after_shebang(self):
        with tempfile.TemporaryDirectory() as tmp:
            filepath = os.path.join(tmp, "run.py")
            with open(filepath, "w", encoding="utf-8") as fh:
                fh.write("#!/usr/bin/env python3\nprint('hi')\n")

            self.inject.inject_signature(filepath)

            content = pathlib.Path(filepath).read_text(encoding="utf-8")
            lines = content.splitlines()
            self.assertEqual(lines[0], "#!/usr/bin/env python3")
            self.assertIn("Protocol    : Deep State of Mind (DSOM) For My AI", content)
            self.assertIn("print('hi')", content)
            # The shebang must remain the very first line, before the header.
            self.assertLess(
                lines.index("#!/usr/bin/env python3"),
                content.index("Protocol    : Deep State of Mind (DSOM) For My AI"),
            )

    def test_py_file_signature_is_not_duplicated_when_already_present(self):
        original = "# Deep State of Mind (DSOM) For My AI Protocol\nprint('noop')\n"
        with tempfile.TemporaryDirectory() as tmp:
            filepath = os.path.join(tmp, "already.py")
            with open(filepath, "w", encoding="utf-8") as fh:
                fh.write(original)

            self.inject.inject_signature(filepath)

            content = pathlib.Path(filepath).read_text(encoding="utf-8")
            self.assertEqual(content, original, "File should be left untouched when already signed")

    def test_py_file_inside_git_directory_is_excluded_from_walk(self):
        # Confirms the pre-existing `.git` exclusion still applies now
        # that `.py` files are eligible for processing.
        with tempfile.TemporaryDirectory() as tmp:
            git_dir = os.path.join(tmp, ".git")
            os.makedirs(git_dir)
            filepath = os.path.join(git_dir, "hook.py")
            with open(filepath, "w", encoding="utf-8") as fh:
                fh.write("pass\n")

            self.inject.inject_signature(tmp)

            content = pathlib.Path(filepath).read_text(encoding="utf-8")
            self.assertEqual(content, "pass\n")

    def test_yaml_file_still_processed_alongside_py_in_same_directory(self):
        # Regression guard: adding '.py' support must not break the
        # pre-existing '.yaml' handling.
        with tempfile.TemporaryDirectory() as tmp:
            py_path = os.path.join(tmp, "a.py")
            yaml_path = os.path.join(tmp, "b.yaml")
            with open(py_path, "w", encoding="utf-8") as fh:
                fh.write("a = 1\n")
            with open(yaml_path, "w", encoding="utf-8") as fh:
                fh.write("key: value\n")

            self.inject.inject_signature(tmp)

            py_content = pathlib.Path(py_path).read_text(encoding="utf-8")
            yaml_content = pathlib.Path(yaml_path).read_text(encoding="utf-8")
            self.assertIn(SIGNATURE_MARKER, py_content)
            self.assertIn(SIGNATURE_MARKER, yaml_content)

    def test_unsupported_extension_is_left_untouched(self):
        with tempfile.TemporaryDirectory() as tmp:
            filepath = os.path.join(tmp, "notes.txt")
            with open(filepath, "w", encoding="utf-8") as fh:
                fh.write("just some notes\n")

            self.inject.inject_signature(tmp)

            content = pathlib.Path(filepath).read_text(encoding="utf-8")
            self.assertEqual(content, "just some notes\n")

    def test_md_file_still_gets_footer_appended_not_header_prepended(self):
        # Regression guard: Markdown handling must remain unaffected by
        # the new '.py' branch.
        with tempfile.TemporaryDirectory() as tmp:
            filepath = os.path.join(tmp, "doc.md")
            with open(filepath, "w", encoding="utf-8") as fh:
                fh.write("# Title\n")

            self.inject.inject_signature(filepath)

            content = pathlib.Path(filepath).read_text(encoding="utf-8")
            self.assertTrue(content.startswith("# Title"))
            self.assertIn(f"{SIGNATURE_MARKER} Protocol", content)


if __name__ == "__main__":
    unittest.main()