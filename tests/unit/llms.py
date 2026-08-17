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


class TestLlmsTxtParser(unittest.TestCase):
    """LLMs parser and compilation API tests."""

    @classmethod
    def setUpClass(cls):
        cls.repo_root = _find_repo_root(pathlib.Path(__file__).parent)
        tools_dir = str(cls.repo_root / "tools")
        if tools_dir not in sys.path:
            sys.path.insert(0, tools_dir)
        import parse_llms_txt  # type: ignore # noqa: E402
        cls.parse_llms_txt = parse_llms_txt

    def test_llms_txt2ctx_parser_api(self):
        """Verify parse_llms_txt API parses llms.txt and discovers Markdown files."""
        llms_path = self.repo_root / "llms.txt"
        self.assertTrue(llms_path.is_file(), "llms.txt must exist at repository root")

        discovered = self.parse_llms_txt.parse_llms_txt(llms_path, self.repo_root)
        self.assertIsInstance(discovered, list)
        self.assertGreater(len(discovered), 0, "parse_llms_txt should discover referenced Markdown files")

        for title, path in discovered:
            self.assertIsInstance(title, str)
            self.assertIsInstance(path, pathlib.Path)
            self.assertTrue(path.is_absolute(), f"Returned path {path} must be absolute")
            self.assertTrue(path.is_file(), f"Discovered file {path} must exist")
            # Verify path is inside repo_root
            self.assertEqual(path.resolve().relative_to(self.repo_root.resolve()).parents[-1], pathlib.Path("."))

    def test_parse_llms_txt_path_validation_isolated_cases(self):
        """Verify path validation contracts for parse_llms_txt."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmproot = pathlib.Path(tmpdir)

            # Case 1: Missing input llms.txt file
            missing_llms = tmproot / "missing_llms.txt"
            with self.assertRaises(FileNotFoundError):
                self.parse_llms_txt.parse_llms_txt(missing_llms, tmproot)

            # Case 2: Missing referenced Markdown file
            llms_file = tmproot / "llms.txt"
            llms_file.write_text("[Missing](non_existent.md)\n", encoding="utf-8")
            with self.assertRaises(FileNotFoundError):
                self.parse_llms_txt.parse_llms_txt(llms_file, tmproot)

            # Case 3: Non-file reference (e.g., directory matching .md)
            dir_md = tmproot / "folder.md"
            dir_md.mkdir()
            llms_file.write_text("[Dir](folder.md)\n", encoding="utf-8")
            with self.assertRaises(FileNotFoundError):
                self.parse_llms_txt.parse_llms_txt(llms_file, tmproot)

            # Case 4: Out-of-bounds path reference
            llms_file.write_text("[OOB](../outside.md)\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                self.parse_llms_txt.parse_llms_txt(llms_file, tmproot)

            # Case 5: Duplicate links deduplication and valid absolute in-repo path
            valid_file = tmproot / "valid.md"
            valid_file.write_text("# Valid\n", encoding="utf-8")
            llms_file.write_text("[V1](valid.md)\n[V2](valid.md)\n", encoding="utf-8")
            discovered = self.parse_llms_txt.parse_llms_txt(llms_file, tmproot)
            self.assertEqual(len(discovered), 1, "Duplicate references must be deduplicated")
            title, path = discovered[0]
            self.assertEqual(title, "V1")
            self.assertTrue(path.is_absolute())
            self.assertEqual(path, valid_file.resolve())

    def test_build_llms_full_compilation(self):
        """Verify generate_llms_full_txt and generate_llms_context_xml compilation functions."""
        llms_path = self.repo_root / "llms.txt"
        discovered = self.parse_llms_txt.parse_llms_txt(llms_path, self.repo_root)

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = pathlib.Path(tmpdir)
            out_txt = tmp_path / "llms-full.txt"
            out_xml = tmp_path / "llms-context.xml"

            self.parse_llms_txt.generate_llms_full_txt(discovered, out_txt, self.repo_root)
            self.assertTrue(out_txt.is_file(), "llms-full.txt output file must be created")
            txt_content = out_txt.read_text(encoding="utf-8")
            self.assertIn("FILE:", txt_content)

            # Assert every discovered relative path appears in txt_content
            for title, filepath in discovered:
                rel_path = filepath.relative_to(self.repo_root).as_posix()
                self.assertIn(rel_path, txt_content, f"Relative path {rel_path} must appear in llms-full.txt")

            self.parse_llms_txt.generate_llms_context_xml(discovered, out_xml, self.repo_root)
            self.assertTrue(out_xml.is_file(), "llms-context.xml output file must be created")

            tree = ET.parse(out_xml)
            root = tree.getroot()
            self.assertEqual(root.tag, "context")
            self.assertIn("total_files", root.attrib)
            self.assertEqual(root.attrib["total_files"], str(len(discovered)))

            docs_elems = root.findall("document")
            self.assertEqual(len(docs_elems), len(discovered), "XML document count must match discovered files count")


if __name__ == "__main__":
    unittest.main()
