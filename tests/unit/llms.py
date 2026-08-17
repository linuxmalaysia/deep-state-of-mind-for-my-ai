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


if __name__ == "__main__":
    unittest.main()
