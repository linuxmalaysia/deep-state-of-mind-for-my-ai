"""
LLMs parser and compilation unit tests.
"""
import pathlib
import sys
import tempfile
import xml.etree.ElementTree as ET
import unittest

def _find_repo_root(start: pathlib.Path) -> pathlib.Path:
    current = start.resolve()
    for parent in [current, *current.parents]:
        if (parent / ".git").exists():
            return parent
    raise RuntimeError("Could not locate repository root (.git not found)")

REPO_ROOT = _find_repo_root(pathlib.Path(__file__).parent)
sys.path.insert(0, str(REPO_ROOT / "tools"))

import parse_llms_txt  # type: ignore # noqa: E402


class TestLlmsTxtParser(unittest.TestCase):
    """LLMs parser and compilation API tests."""

    def test_llms_txt2ctx_parser_api(self):
        """Verify parse_llms_txt API parses llms.txt and discovers Markdown files."""
        llms_path = REPO_ROOT / "llms.txt"
        self.assertTrue(llms_path.is_file(), "llms.txt must exist at repository root")

        discovered = parse_llms_txt.parse_llms_txt(llms_path, REPO_ROOT)
        self.assertIsInstance(discovered, list)
        self.assertGreater(len(discovered), 0, "parse_llms_txt should discover referenced Markdown files")

        for title, path in discovered:
            self.assertIsInstance(title, str)
            self.assertIsInstance(path, pathlib.Path)
            self.assertTrue(path.is_file(), f"Discovered file {path} must exist")

    def test_build_llms_full_compilation(self):
        """Verify generate_llms_full_txt and generate_llms_context_xml compilation functions."""
        llms_path = REPO_ROOT / "llms.txt"
        discovered = parse_llms_txt.parse_llms_txt(llms_path, REPO_ROOT)

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = pathlib.Path(tmpdir)
            out_txt = tmp_path / "llms-full.txt"
            out_xml = tmp_path / "llms-context.xml"

            parse_llms_txt.generate_llms_full_txt(discovered, out_txt, REPO_ROOT)
            self.assertTrue(out_txt.is_file(), "llms-full.txt output file must be created")
            txt_content = out_txt.read_text(encoding="utf-8")
            self.assertIn("FILE:", txt_content)

            parse_llms_txt.generate_llms_context_xml(discovered, out_xml, REPO_ROOT)
            self.assertTrue(out_xml.is_file(), "llms-context.xml output file must be created")

            tree = ET.parse(out_xml)
            root = tree.getroot()
            self.assertEqual(root.tag, "context")
            self.assertIn("total_files", root.attrib)

    def test_parse_llms_txt_raises_for_missing_input_file(self):
        """parse_llms_txt must raise FileNotFoundError when the index file is absent."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_root = pathlib.Path(tmpdir)
            missing_llms = tmp_root / "llms.txt"
            with self.assertRaises(FileNotFoundError):
                parse_llms_txt.parse_llms_txt(missing_llms, tmp_root)

    def test_parse_llms_txt_ignores_external_http_links(self):
        """External http(s) links referenced in llms.txt must be skipped."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_root = pathlib.Path(tmpdir)
            (tmp_root / "local.md").write_text("# Local\n", encoding="utf-8")
            llms_path = tmp_root / "llms.txt"
            llms_path.write_text(
                "[External](https://example.com/page.md)\n"
                "[Local](local.md)\n",
                encoding="utf-8",
            )
            discovered = parse_llms_txt.parse_llms_txt(llms_path, tmp_root)
            self.assertEqual(len(discovered), 1)
            self.assertEqual(discovered[0][0], "Local")
            self.assertEqual(discovered[0][1], (tmp_root / "local.md").resolve())

    def test_parse_llms_txt_raises_for_out_of_bounds_path(self):
        """A referenced path resolving outside repo_root must raise ValueError."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_root = pathlib.Path(tmpdir) / "repo"
            tmp_root.mkdir()
            llms_path = tmp_root / "llms.txt"
            llms_path.write_text("[Escape](../outside.md)\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                parse_llms_txt.parse_llms_txt(llms_path, tmp_root)

    def test_parse_llms_txt_raises_for_missing_referenced_file(self):
        """A referenced Markdown file that does not exist must raise FileNotFoundError."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_root = pathlib.Path(tmpdir)
            llms_path = tmp_root / "llms.txt"
            llms_path.write_text("[Ghost](ghost.md)\n", encoding="utf-8")
            with self.assertRaises(FileNotFoundError):
                parse_llms_txt.parse_llms_txt(llms_path, tmp_root)

    def test_parse_llms_txt_deduplicates_repeated_references(self):
        """The same Markdown path referenced multiple times must only appear once."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_root = pathlib.Path(tmpdir)
            (tmp_root / "dup.md").write_text("# Dup\n", encoding="utf-8")
            llms_path = tmp_root / "llms.txt"
            llms_path.write_text(
                "[First](dup.md)\n[Second](dup.md)\n",
                encoding="utf-8",
            )
            discovered = parse_llms_txt.parse_llms_txt(llms_path, tmp_root)
            self.assertEqual(len(discovered), 1)
            self.assertEqual(discovered[0][0], "First")

    def test_generate_llms_full_txt_wraps_read_failure_in_ioerror(self):
        """A discovered file that disappears before compilation must raise IOError."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_root = pathlib.Path(tmpdir)
            vanished = tmp_root / "vanished.md"
            vanished.write_text("# Gone\n", encoding="utf-8")
            discovered = [("Vanished", vanished)]
            vanished.unlink()
            with self.assertRaises(IOError):
                parse_llms_txt.generate_llms_full_txt(
                    discovered, tmp_root / "out.txt", tmp_root
                )


if __name__ == "__main__":
    unittest.main()
