"""
Unit tests for unified sitemaps and SEO assets.

This test suite validates that:
1. `sitemap.txt`, `sitemap.xml`, and `robots.txt` exist in both the root directory
   and the docs/ directory.
2. `sitemap.txt` is correctly formatted (plain text, one URL per line, unique, and sorted).
3. `sitemap.xml` parses as valid XML and contains expected SEO URL tags (`<loc>`, `<lastmod>`).
4. Both sitemaps contain URLs pointing to GitHub Pages, GitBook, and Read the Docs.
5. All GitBook URLs mapped from SUMMARY.md correspond to actual, existing physical files.
6. `robots.txt` is standard and points to the sitemaps.
"""
import pathlib
import re
import urllib.parse
import xml.etree.ElementTree as ET
import unittest

def _find_repo_root(start: pathlib.Path) -> pathlib.Path:
    """
    Locate the repository root containing the `.git` entry.
    
    Parameters:
    	start (pathlib.Path): Path from which to begin searching.
    
    Returns:
    	pathlib.Path: The repository root directory.
    
    Raises:
    	RuntimeError: If no ancestor contains a `.git` entry.
    """
    current = start.resolve()
    for parent in [current, *current.parents]:
        if (parent / ".git").exists():
            return parent
    raise RuntimeError("Could not locate repository root (.git not found)")

REPO_ROOT = _find_repo_root(pathlib.Path(__file__).parent)

GITHUB_PAGES_BASE = "https://linuxmalaysia.github.io/deep-state-of-mind-for-my-ai/"
READTHEDOCS_BASE = "https://deep-state-of-mind-for-my-ai.readthedocs.io/en/latest/"
GITBOOK_BASE = "https://malaysia-open-source-community.gitbook.io/deep-state-of-mind-dsom-protocol-for-my-ai/"

class SeoFileExistenceTests(unittest.TestCase):
    """Verify sitemaps and robots.txt exist in required locations."""

    def test_sitemap_txt_exists_in_root_and_docs(self):
        """Verify that sitemap.txt exists in both the repository root and the docs directory."""
        self.assertTrue((REPO_ROOT / "sitemap.txt").is_file())
        self.assertTrue((REPO_ROOT / "docs" / "sitemap.txt").is_file())

    def test_sitemap_xml_exists_in_root_and_docs(self):
        self.assertTrue((REPO_ROOT / "sitemap.xml").is_file())
        self.assertTrue((REPO_ROOT / "docs" / "sitemap.xml").is_file())

    def test_robots_txt_exists_in_root_and_docs(self):
        self.assertTrue((REPO_ROOT / "robots.txt").is_file())
        self.assertTrue((REPO_ROOT / "docs" / "robots.txt").is_file())


class SitemapTxtFormatTests(unittest.TestCase):
    """Verify that sitemap.txt contains correctly formatted, sorted, and de-duplicated URLs."""

    @classmethod
    def setUpClass(cls):
        """Load and prepare the root sitemap text for class-level tests.
        
        Sets `content` to the file contents and `lines` to its non-empty, stripped lines.
        """
        cls.content = (REPO_ROOT / "sitemap.txt").read_text(encoding="utf-8")
        cls.lines = [line.strip() for line in cls.content.splitlines() if line.strip()]

    def test_sitemap_txt_not_empty(self):
        self.assertGreater(len(self.lines), 0)

    def test_sitemap_txt_only_absolute_urls(self):
        for line in self.lines:
            with self.subTest(url=line):
                self.assertTrue(line.startswith("https://") or line.startswith("http://"))

    def test_sitemap_txt_no_duplicates(self):
        self.assertEqual(len(self.lines), len(set(self.lines)), "Duplicate URLs found in sitemap.txt")

    def test_sitemap_txt_is_alphabetically_sorted(self):
        self.assertEqual(self.lines, sorted(self.lines), "Sitemap URLs are not alphabetically sorted")

    def test_sitemap_txt_contains_all_three_platforms(self):
        has_gh = any(line.startswith(GITHUB_PAGES_BASE) for line in self.lines)
        has_rtd = any(line.startswith(READTHEDOCS_BASE) for line in self.lines)
        has_gb = any(line.startswith(GITBOOK_BASE) for line in self.lines)

        self.assertTrue(has_gh, "Sitemap must contain GitHub Pages URLs")
        self.assertTrue(has_rtd, "Sitemap must contain Read the Docs URLs")
        self.assertTrue(has_gb, "Sitemap must contain GitBook URLs")


class SitemapXmlStructureTests(unittest.TestCase):
    """Verify that sitemap.xml is valid, correctly structured, and comprehensive."""

    @classmethod
    def setUpClass(cls):
        cls.xml_path = REPO_ROOT / "sitemap.xml"
        cls.tree = ET.parse(cls.xml_path)
        cls.root = cls.tree.getroot()

    def test_root_element_tag_is_urlset(self):
        # Strip namespace if present
        tag = self.root.tag
        if '}' in tag:
            tag = tag.split('}', 1)[1]
        self.assertEqual(tag, "urlset")

    def test_xml_has_url_nodes(self):
        namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        urls = self.root.findall('.//ns:url', namespace)
        self.assertGreater(len(urls), 0)

        # Verify each <url> contains <loc> and <lastmod>
        for url_node in urls:
            loc = url_node.find('ns:loc', namespace)
            lastmod = url_node.find('ns:lastmod', namespace)

            self.assertIsNotNone(loc, "<url> is missing <loc> element")
            self.assertIsNotNone(lastmod, "<url> is missing <lastmod> element")
            self.assertTrue(loc.text.startswith("https://"))
            self.assertRegex(lastmod.text, r'^\d{4}-\d{2}-\d{2}$')


class SitemapAgentsUrlRegressionTests(unittest.TestCase):
    """Regression tests for the `.agents/` URLs newly generated into the
    unified sitemaps (previously the sitemaps only listed top-level docs
    pages, omitting the `.agents/` tree entirely)."""

    # A representative sample of `.agents/` pages that must now be present,
    # covering brain notes, skills, and workflows subtrees.
    AGENTS_SAMPLE_PATHS = [
        ".agents/AGENTS/",
        ".agents/brain/DSOM_TEMPLATE/",
        ".agents/brain/palace_registry/",
        ".agents/skills/dsom-bootstrap/SKILL/",
        ".agents/skills/openwiki-compiler/SKILL/",
        ".agents/workflows/SUBAGENT-ORCHESTRATION-WORKFLOW/",
    ]

    @classmethod
    def setUpClass(cls):
        cls.txt_lines = {
            line.strip()
            for line in (REPO_ROOT / "sitemap.txt").read_text(encoding="utf-8").splitlines()
            if line.strip()
        }
        namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        xml_root = ET.parse(REPO_ROOT / "sitemap.xml").getroot()
        cls.xml_locs = {
            loc.text
            for loc in xml_root.findall('.//ns:url/ns:loc', namespace)
        }

    def test_agents_sample_urls_present_for_github_pages_in_txt(self):
        for path in self.AGENTS_SAMPLE_PATHS:
            with self.subTest(path=path):
                self.assertIn(f"{GITHUB_PAGES_BASE}{path}", self.txt_lines)

    def test_agents_sample_urls_present_for_readthedocs_in_txt(self):
        for path in self.AGENTS_SAMPLE_PATHS:
            with self.subTest(path=path):
                self.assertIn(f"{READTHEDOCS_BASE}{path}", self.txt_lines)

    def test_agents_sample_urls_present_in_xml(self):
        for path in self.AGENTS_SAMPLE_PATHS:
            with self.subTest(path=path):
                self.assertIn(f"{GITHUB_PAGES_BASE}{path}", self.xml_locs)
                self.assertIn(f"{READTHEDOCS_BASE}{path}", self.xml_locs)

    def test_sitemap_txt_and_xml_have_matching_url_sets(self):
        # sitemap.txt and sitemap.xml are generated from the same source
        # list, so both formats must expose exactly the same URLs.
        self.assertEqual(self.txt_lines, self.xml_locs)


class RootAndDocsSitemapConsistencyTests(unittest.TestCase):
    """Verify the root and docs/ copies of each sitemap stay in sync."""

    def test_sitemap_txt_root_and_docs_copies_are_identical(self):
        root_content = (REPO_ROOT / "sitemap.txt").read_text(encoding="utf-8")
        docs_content = (REPO_ROOT / "docs" / "sitemap.txt").read_text(encoding="utf-8")
        self.assertEqual(root_content, docs_content)

    def test_sitemap_xml_root_and_docs_copies_are_identical(self):
        root_content = (REPO_ROOT / "sitemap.xml").read_text(encoding="utf-8")
        docs_content = (REPO_ROOT / "docs" / "sitemap.xml").read_text(encoding="utf-8")
        self.assertEqual(root_content, docs_content)


class SummaryMdIntegrityAndGitBookUrlTests(unittest.TestCase):
    """Verify the integrity of SUMMARY.md links and check for dead links."""

    @classmethod
    def setUpClass(cls):
        cls.summary_path = REPO_ROOT / "SUMMARY.md"

    def test_all_markdown_links_in_summary_exist(self):
        """Parse all markdown links inside SUMMARY.md and verify they resolve to real files."""
        content = self.summary_path.read_text(encoding="utf-8")
        matches = re.findall(r'\[[^\]]+\]\(([^)]+\.md)\)', content)

        self.assertGreater(len(matches), 0, "SUMMARY.md has no markdown links")

        for relative_path in matches:
            with self.subTest(file_path=relative_path):
                # Percent-decode paths (e.g. spaces/emojis)
                decoded_path = urllib.parse.unquote(relative_path.strip())
                target_file = REPO_ROOT / decoded_path
                self.assertTrue(
                    target_file.is_file(),
                    f"SUMMARY.md references a non-existent file: {decoded_path}"
                )


class RobotsTxtContentTests(unittest.TestCase):
    """Verify robots.txt content."""

    @classmethod
    def setUpClass(cls):
        """Load the repository's robots.txt content for the test class."""
        cls.content = (REPO_ROOT / "robots.txt").read_text(encoding="utf-8")

    def test_robots_allows_indexing(self):
        self.assertIn("User-agent: *", self.content)
        self.assertIn("Allow: /", self.content)

    def test_robots_lists_sitemaps(self):
        """Verify that robots.txt lists the GitHub Pages and Read the Docs sitemaps."""
        self.assertIn(f"Sitemap: {GITHUB_PAGES_BASE}sitemap.xml", self.content)
        self.assertIn(f"Sitemap: {READTHEDOCS_BASE}sitemap.xml", self.content)


if __name__ == "__main__":
    unittest.main()
