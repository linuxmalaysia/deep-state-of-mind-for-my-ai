"""
Sitemaps consistency and Context7 configuration unit tests.
"""
import json
import pathlib
import xml.etree.ElementTree as ET
import unittest

def _find_repo_root(start: pathlib.Path) -> pathlib.Path:
    """
    Locate the repository root by searching the starting path and its ancestors for a `.git` entry.
    
    Parameters:
        start (pathlib.Path): Path from which to begin the search.
    
    Returns:
        pathlib.Path: The nearest ancestor containing a `.git` entry.
    
    Raises:
        RuntimeError: If no repository root is found.
    """
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


if __name__ == "__main__":
    unittest.main()
