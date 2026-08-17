"""
Sitemaps consistency and Context7 configuration unit tests.
"""
import json
import pathlib
import sys
import tempfile
import xml.etree.ElementTree as ET
import unittest
from unittest import mock

def _find_repo_root(start: pathlib.Path) -> pathlib.Path:
    current = start.resolve()
    for parent in [current, *current.parents]:
        if (parent / ".git").exists():
            return parent
    raise RuntimeError("Could not locate repository root (.git not found)")

REPO_ROOT = _find_repo_root(pathlib.Path(__file__).parent)


class TestSitemapsAndContext7(unittest.TestCase):
    """Sitemaps consistency and Context7 configuration tests."""

    def test_sitemaps_consistency(self):
        """Verify existence, consistency, and URL structure of sitemap.txt and sitemap.xml."""
        root_txt = REPO_ROOT / "sitemap.txt"
        docs_txt = REPO_ROOT / "docs" / "sitemap.txt"
        root_xml = REPO_ROOT / "sitemap.xml"
        docs_xml = REPO_ROOT / "docs" / "sitemap.xml"

        self.assertTrue(root_txt.is_file(), "sitemap.txt must exist at repository root")
        self.assertTrue(docs_txt.is_file(), "sitemap.txt must exist in docs/")
        self.assertTrue(root_xml.is_file(), "sitemap.xml must exist at repository root")
        self.assertTrue(docs_xml.is_file(), "sitemap.xml must exist in docs/")

        # Verify root and docs/ copies are identical
        self.assertEqual(root_txt.read_text(encoding="utf-8"), docs_txt.read_text(encoding="utf-8"))
        self.assertEqual(root_xml.read_text(encoding="utf-8"), docs_xml.read_text(encoding="utf-8"))

        # Verify sitemap.txt structure
        txt_lines = [l.strip() for l in root_txt.read_text(encoding="utf-8").splitlines() if l.strip()]
        self.assertGreater(len(txt_lines), 0, "sitemap.txt must not be empty")
        for line in txt_lines:
            self.assertTrue(line.startswith("https://") or line.startswith("http://"), f"URL in sitemap.txt must be absolute: {line}")

        # Verify sitemap.xml parses cleanly
        tree = ET.parse(root_xml)
        root_elem = tree.getroot()
        self.assertIn("urlset", root_elem.tag)

    def test_context7_configuration(self):
        """Verify context7.json and context7-indexer skill configuration."""
        ctx7_file = REPO_ROOT / "context7.json"
        self.assertTrue(ctx7_file.is_file(), "context7.json must exist at repository root")

        ctx7_data = json.loads(ctx7_file.read_text(encoding="utf-8"))
        self.assertIsInstance(ctx7_data, dict, "context7.json must parse to a dict")

        skill_file = REPO_ROOT / ".agents" / "skills" / "context7-indexer" / "SKILL.md"
        self.assertTrue(skill_file.is_file(), ".agents/skills/context7-indexer/SKILL.md must exist")
        skill_content = skill_file.read_text(encoding="utf-8")
        self.assertTrue(skill_content.startswith("---\n"), "context7-indexer SKILL.md must start with frontmatter")

    @staticmethod
    def _write_matching_sitemap_fixture(tmp_root, txt_body, xml_body):
        (tmp_root / "docs").mkdir(exist_ok=True)
        (tmp_root / "sitemap.txt").write_text(txt_body, encoding="utf-8")
        (tmp_root / "docs" / "sitemap.txt").write_text(txt_body, encoding="utf-8")
        (tmp_root / "sitemap.xml").write_text(xml_body, encoding="utf-8")
        (tmp_root / "docs" / "sitemap.xml").write_text(xml_body, encoding="utf-8")

    def test_sitemaps_consistency_passes_for_matching_minimal_fixture(self):
        """Identical, well-formed root/docs sitemap copies must pass cleanly."""
        module = sys.modules[__name__]
        txt_body = "https://example.com/\n"
        xml_body = (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
            "<url><loc>https://example.com/</loc></url></urlset>\n"
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_root = pathlib.Path(tmpdir)
            self._write_matching_sitemap_fixture(tmp_root, txt_body, xml_body)
            with mock.patch.object(module, "REPO_ROOT", tmp_root):
                self.test_sitemaps_consistency()  # must not raise

    def test_sitemaps_consistency_fails_when_root_and_docs_diverge(self):
        """Diverging root and docs/ sitemap.txt copies must fail consistency."""
        module = sys.modules[__name__]
        xml_body = (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
            "<url><loc>https://example.com/</loc></url></urlset>\n"
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_root = pathlib.Path(tmpdir)
            self._write_matching_sitemap_fixture(tmp_root, "https://example.com/\n", xml_body)
            # Diverge the docs/ copy after writing the matching fixture.
            (tmp_root / "docs" / "sitemap.txt").write_text("https://example.com/other\n", encoding="utf-8")
            with mock.patch.object(module, "REPO_ROOT", tmp_root):
                with self.assertRaises(AssertionError):
                    self.test_sitemaps_consistency()

    def test_sitemaps_consistency_fails_for_relative_url(self):
        """A non-absolute URL entry in sitemap.txt must fail the structure check."""
        module = sys.modules[__name__]
        xml_body = (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
            "<url><loc>https://example.com/</loc></url></urlset>\n"
        )
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_root = pathlib.Path(tmpdir)
            self._write_matching_sitemap_fixture(tmp_root, "/relative/path\n", xml_body)
            with mock.patch.object(module, "REPO_ROOT", tmp_root):
                with self.assertRaises(AssertionError):
                    self.test_sitemaps_consistency()

    def test_sitemaps_consistency_fails_when_a_required_file_is_missing(self):
        """Missing sitemap.xml (root or docs) must fail the existence check."""
        module = sys.modules[__name__]
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_root = pathlib.Path(tmpdir)
            (tmp_root / "docs").mkdir()
            (tmp_root / "sitemap.txt").write_text("https://example.com/\n", encoding="utf-8")
            (tmp_root / "docs" / "sitemap.txt").write_text("https://example.com/\n", encoding="utf-8")
            # sitemap.xml intentionally omitted.
            with mock.patch.object(module, "REPO_ROOT", tmp_root):
                with self.assertRaises(AssertionError):
                    self.test_sitemaps_consistency()

    def test_context7_configuration_fails_when_json_is_invalid(self):
        """Malformed JSON in context7.json must surface as a parse error."""
        module = sys.modules[__name__]
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_root = pathlib.Path(tmpdir)
            (tmp_root / "context7.json").write_text("{not valid json", encoding="utf-8")
            with mock.patch.object(module, "REPO_ROOT", tmp_root):
                with self.assertRaises(json.JSONDecodeError):
                    self.test_context7_configuration()

    def test_context7_configuration_fails_when_skill_file_missing(self):
        """A missing context7-indexer SKILL.md must fail the configuration check."""
        module = sys.modules[__name__]
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_root = pathlib.Path(tmpdir)
            (tmp_root / "context7.json").write_text('{"url": "https://example.com"}', encoding="utf-8")
            with mock.patch.object(module, "REPO_ROOT", tmp_root):
                with self.assertRaises(AssertionError):
                    self.test_context7_configuration()


if __name__ == "__main__":
    unittest.main()
