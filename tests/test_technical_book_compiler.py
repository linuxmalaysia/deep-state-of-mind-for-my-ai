"""
Unit tests for Technical Ebook & Handbook Compiler skill and script.
"""

import unittest
import tempfile
import shutil
from pathlib import Path
import importlib.util

spec = importlib.util.spec_from_file_location("compile_book", ".agents/skills/dsom-technical-book-compiler/scripts/compile-book.py")
compile_book = importlib.util.module_from_spec(spec)
spec.loader.exec_module(compile_book)
audit_artifact = compile_book.audit_artifact


class TestTechnicalBookCompiler(unittest.TestCase):
    """Test suite for dsom-technical-book-compiler script functions."""

    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_audit_artifact_clean(self):
        clean_file = self.test_dir / "clean.html"
        clean_file.write_text("<h1>Hello World</h1><p>Clean content without leaks.</p>", encoding="utf-8")
        self.assertFalse(audit_artifact(clean_file))

    def test_audit_artifact_file_uri_leak(self):
        leak_file = self.test_dir / "leak_uri.html"
        leak_file.write_text("<h1>Hello</h1><a href='file:///C:/Users/test/doc.md'>Link</a>", encoding="utf-8")
        self.assertTrue(audit_artifact(leak_file))

    def test_audit_artifact_drive_letter_leak(self):
        leak_file = self.test_dir / "leak_drive.html"
        leak_file.write_text("<h1>Hello</h1><a href='D:/Users/test/doc.md'>Link</a>", encoding="utf-8")
        self.assertTrue(audit_artifact(leak_file))

    def test_audit_artifact_build_prefix_leak(self):
        leak_file = self.test_dir / "leak_build.html"
        leak_file.write_text("<h1>Hello</h1><a href='build/book/chap1.html'>Link</a>", encoding="utf-8")
        self.assertTrue(audit_artifact(leak_file))


if __name__ == "__main__":
    unittest.main()
