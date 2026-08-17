"""
Sitemaps consistency and Context7 configuration unit tests.
"""
import json
import pathlib
import tempfile
import xml.etree.ElementTree as ET
import unittest

def _find_repo_root(start: pathlib.Path) -> pathlib.Path:
    current = start.resolve()
    for parent in [current, *current.parents]:
        if (parent / ".git").exists():
            return parent
    raise RuntimeError("Could not locate repository root (.git not found)")


class TestSitemapsAndContext7(unittest.TestCase):
    """Sitemaps consistency and Context7 configuration tests."""

    @classmethod
    def setUpClass(cls):
        cls.repo_root = _find_repo_root(pathlib.Path(__file__).parent)

    def _validate_sitemaps(self, root_dir: pathlib.Path):
        root_txt = root_dir / "sitemap.txt"
        docs_txt = root_dir / "docs" / "sitemap.txt"
        root_xml = root_dir / "sitemap.xml"
        docs_xml = root_dir / "docs" / "sitemap.xml"

        self.assertTrue(root_txt.is_file(), "sitemap.txt must exist at repository root")
        self.assertTrue(docs_txt.is_file(), "sitemap.txt must exist in docs/")
        self.assertTrue(root_xml.is_file(), "sitemap.xml must exist at repository root")
        self.assertTrue(docs_xml.is_file(), "sitemap.xml must exist in docs/")

        # Verify root and docs/ copies are identical
        self.assertEqual(root_txt.read_text(encoding="utf-8"), docs_txt.read_text(encoding="utf-8"))
        self.assertEqual(root_xml.read_text(encoding="utf-8"), docs_xml.read_text(encoding="utf-8"))

        # Verify sitemap.txt structure
        txt_lines = [line.strip() for line in root_txt.read_text(encoding="utf-8").splitlines() if line.strip()]
        self.assertGreater(len(txt_lines), 0, "sitemap.txt must not be empty")
        for line in txt_lines:
            self.assertTrue(line.startswith("https://") or line.startswith("http://"), f"URL in sitemap.txt must be absolute: {line}")

        # Verify sitemap.xml parses cleanly
        tree = ET.parse(root_xml)
        root_elem = tree.getroot()
        self.assertIn("urlset", root_elem.tag)

    def _validate_context7(self, root_dir: pathlib.Path):
        ctx7_file = root_dir / "context7.json"
        self.assertTrue(ctx7_file.is_file(), "context7.json must exist at repository root")

        ctx7_data = json.loads(ctx7_file.read_text(encoding="utf-8"))
        self.assertIsInstance(ctx7_data, dict, "context7.json must parse to a dict")

        skill_file = root_dir / ".agents" / "skills" / "context7-indexer" / "SKILL.md"
        self.assertTrue(skill_file.is_file(), ".agents/skills/context7-indexer/SKILL.md must exist")
        skill_content = skill_file.read_text(encoding="utf-8")
        self.assertTrue(skill_content.startswith("---\n"), "context7-indexer SKILL.md must start with frontmatter")

    def test_sitemaps_consistency(self):
        """Verify existence, consistency, and URL structure of sitemap.txt and sitemap.xml on repository root."""
        self._validate_sitemaps(self.repo_root)

    def test_context7_configuration(self):
        """Verify context7.json and context7-indexer skill configuration on repository root."""
        self._validate_context7(self.repo_root)

    def test_sitemaps_consistency_fixture_cases(self):
        """Verify isolated fixture cases for sitemap consistency validation."""
        valid_xml = '<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>https://example.com/</loc></url></urlset>'
        valid_txt = "https://example.com/index.html\n"

        with tempfile.TemporaryDirectory() as tmpdir:
            tmproot = pathlib.Path(tmpdir)
            docs_dir = tmproot / "docs"
            docs_dir.mkdir()

            # Case 1: Matching valid copies
            (tmproot / "sitemap.txt").write_text(valid_txt, encoding="utf-8")
            (docs_dir / "sitemap.txt").write_text(valid_txt, encoding="utf-8")
            (tmproot / "sitemap.xml").write_text(valid_xml, encoding="utf-8")
            (docs_dir / "sitemap.xml").write_text(valid_xml, encoding="utf-8")
            self._validate_sitemaps(tmproot)

            # Case 2: Divergent copies
            (docs_dir / "sitemap.txt").write_text("https://example.com/other.html\n", encoding="utf-8")
            with self.assertRaises(AssertionError):
                self._validate_sitemaps(tmproot)

            # Case 3: Relative URLs
            (tmproot / "sitemap.txt").write_text("relative/path/index.html\n", encoding="utf-8")
            (docs_dir / "sitemap.txt").write_text("relative/path/index.html\n", encoding="utf-8")
            with self.assertRaises(AssertionError):
                self._validate_sitemaps(tmproot)

            # Case 4: Missing sitemap file
            (docs_dir / "sitemap.txt").unlink()
            with self.assertRaises(AssertionError):
                self._validate_sitemaps(tmproot)

    def test_context7_configuration_fixture_cases(self):
        """Verify isolated fixture cases for Context7 validation."""
        valid_ctx7 = '{"schemaVersion": "1.0", "title": "Test"}'
        valid_skill = "---\nokf_version: 0.1\ntype: agent_skill\ntitle: test\n---\n# Skill"

        with tempfile.TemporaryDirectory() as tmpdir:
            tmproot = pathlib.Path(tmpdir)
            skill_dir = tmproot / ".agents" / "skills" / "context7-indexer"
            skill_dir.mkdir(parents=True)

            # Case 1: Valid configuration
            (tmproot / "context7.json").write_text(valid_ctx7, encoding="utf-8")
            (skill_dir / "SKILL.md").write_text(valid_skill, encoding="utf-8")
            self._validate_context7(tmproot)

            # Case 2: Invalid JSON
            (tmproot / "context7.json").write_text("{invalid_json", encoding="utf-8")
            with self.assertRaises(json.JSONDecodeError):
                self._validate_context7(tmproot)

            # Case 3: Missing skill file
            (tmproot / "context7.json").write_text(valid_ctx7, encoding="utf-8")
            (skill_dir / "SKILL.md").unlink()
            with self.assertRaises(AssertionError):
                self._validate_context7(tmproot)


if __name__ == "__main__":
    unittest.main()
