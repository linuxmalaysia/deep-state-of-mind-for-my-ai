"""
Unit tests for the new Diátaxis Developer Space documentation added by this PR.

This PR introduces a brand-new Diátaxis-structured documentation quadrant
under `docs/` (tutorials/, how-to/, reference/, explanation/) plus a
dedicated `docs/SUMMARY.md`, and wires it up in `mkdocs.yml` (nav),
`SUMMARY.md` / `llms.txt` (cross-linking), and the unified sitemaps.

These tests validate that:
1. Every new Diátaxis Markdown file exists, is non-empty, and carries valid
   OKF v0.1 frontmatter (`okf_version`, `type`, `title`, `timestamp`, `topics`).
2. `mkdocs.yml` registers a "Diátaxis Developer Space" nav section whose
   entries all resolve to real files under `docs/`.
3. `llms.txt` registers a "Diátaxis Developer Space" section whose linked
   files all resolve to real files under the repository root.
4. `docs/SUMMARY.md` exists, has valid OKF frontmatter, and every relative
   link inside it resolves to a real file (relative to `docs/`).
5. The unified sitemaps (`sitemap.txt`) contain the newly generated
   Diátaxis URLs for both GitHub Pages and Read the Docs.
"""
import pathlib
import re
import unittest

try:
    import yaml  # type: ignore
    HAS_YAML = True
except ImportError:  # pragma: no cover - environment dependent
    HAS_YAML = False


def _find_repo_root(start: pathlib.Path) -> pathlib.Path:
    current = start.resolve()
    for parent in [current, *current.parents]:
        if (parent / ".git").exists():
            return parent
    raise RuntimeError("Could not locate repository root (.git not found)")


REPO_ROOT = _find_repo_root(pathlib.Path(__file__).parent)
DOCS_DIR = REPO_ROOT / "docs"
MKDOCS_PATH = REPO_ROOT / "mkdocs.yml"
LLMS_TXT_PATH = REPO_ROOT / "llms.txt"
SUMMARY_MD_PATH = REPO_ROOT / "docs" / "SUMMARY.md"

FRONTMATTER_RE = re.compile(r"\A---\s*\r?\n(.*?)(?:\r?\n)?---\s*(?:\r?\n|\Z)", re.DOTALL)

GITHUB_PAGES_BASE = "https://linuxmalaysia.github.io/deep-state-of-mind-for-my-ai/"
READTHEDOCS_BASE = "https://deep-state-of-mind-for-my-ai.readthedocs.io/en/latest/"

# (relative path under docs/, expected title)
NEW_DIATAXIS_FILES = [
    ("SUMMARY.md", "Table of Contents (GitBook Summary)"),
    ("tutorials/index.md", "Tutorials Index"),
    ("tutorials/getting-started.md", "Tutorial: Getting Started with DSOM Tools"),
    ("how-to/index.md", "How-To Guides Index"),
    ("how-to/audit-and-apply-frontmatter.md", "How-To: Check and Apply OKF Compliance"),
    ("how-to/run-fastmcp-server.md", "How-To: Run the FastMCP Server"),
    ("how-to/generate-sitemaps-seo.md", "How-To: Generate SEO Assets and Sitemaps"),
    ("how-to/use-openwiki-emulator.md", "How-To: Operate the OpenWiki Emulator"),
    ("how-to/google-search-console.md", "How-To: Verify and Monitor Site with Google Search Console"),
    ("reference/index.md", "Reference Material Index"),
    ("reference/generate_sitemaps.md", "Reference: generate_sitemaps.py"),
    ("reference/openwiki_emulator.md", "Reference: openwiki_emulator.py"),
    ("reference/mcp_server.md", "Reference: mcp_server.md"),
    ("reference/apply_okf_frontmatter.md", "Reference: apply_okf_frontmatter.py"),
    ("reference/refactor_okf.md", "Reference: refactor_okf.py"),
    ("reference/bench_brain.md", "Reference: bench_brain.py"),
    ("reference/dsom_token_auditor.md", "Reference: dsom_token_auditor.py"),
    ("reference/mkdocs_hooks.md", "Reference: mkdocs_hooks.py"),
    ("explanation/index.md", "Explanation Index"),
    ("explanation/openwiki-mcp-architecture.md", "Explanation: OpenWiki & FastMCP Architecture"),
    ("explanation/diataxis.md", "Explanation: Diátaxis Framework Adoption"),
]

# mkdocs.yml nav entries under the "Diátaxis Developer Space" section
# (label, path relative to docs/)
DIATAXIS_NAV_ENTRIES = [
    ("Overview", "tutorials/index.md"),
    ("Getting Started with DSOM Tools", "tutorials/getting-started.md"),
    ("Overview", "how-to/index.md"),
    ("Audit and Apply OKF Frontmatter", "how-to/audit-and-apply-frontmatter.md"),
    ("Run FastMCP Server", "how-to/run-fastmcp-server.md"),
    ("Generate SEO Assets and Sitemaps", "how-to/generate-sitemaps-seo.md"),
    ("Operate OpenWiki Emulator", "how-to/use-openwiki-emulator.md"),
    ("Verify Google Search Console", "how-to/google-search-console.md"),
    ("Overview", "reference/index.md"),
    ("generate_sitemaps.py", "reference/generate_sitemaps.md"),
    ("openwiki_emulator.py", "reference/openwiki_emulator.md"),
    ("tools/mcp/server.py", "reference/mcp_server.md"),
    ("apply_okf_frontmatter.py", "reference/apply_okf_frontmatter.md"),
    ("refactor_okf.py", "reference/refactor_okf.md"),
    ("bench_brain.py", "reference/bench_brain.md"),
    ("dsom_token_auditor.py", "reference/dsom_token_auditor.md"),
    ("mkdocs_hooks.py", "reference/mkdocs_hooks.md"),
    ("Overview", "explanation/index.md"),
    ("OpenWiki & FastMCP Architecture", "explanation/openwiki-mcp-architecture.md"),
    ("Diátaxis Framework Adoption", "explanation/diataxis.md"),
]

# A representative sample of the newly generated Diátaxis sitemap paths.
DIATAXIS_SITEMAP_SAMPLE_PATHS = [
    "tutorials/",
    "tutorials/getting-started/",
    "how-to/",
    "how-to/audit-and-apply-frontmatter/",
    "how-to/run-fastmcp-server/",
    "how-to/generate-sitemaps-seo/",
    "how-to/use-openwiki-emulator/",
    "how-to/google-search-console/",
    "reference/",
    "reference/apply_okf_frontmatter/",
    "reference/bench_brain/",
    "reference/dsom_token_auditor/",
    "reference/generate_sitemaps/",
    "reference/mcp_server/",
    "reference/mkdocs_hooks/",
    "reference/openwiki_emulator/",
    "reference/refactor_okf/",
    "explanation/",
    "explanation/diataxis/",
    "explanation/openwiki-mcp-architecture/",
]


def _extract_frontmatter(content: str):
    """Return (raw_yaml_text, parsed_mapping_or_None) for the leading frontmatter block."""
    match = FRONTMATTER_RE.match(content)
    if not match:
        return None, None
    raw = match.group(1)
    parsed = yaml.safe_load(raw) if HAS_YAML else None
    return raw, parsed


class DiataxisFileExistenceTests(unittest.TestCase):
    """Every new Diátaxis file must exist, be non-empty, and start with clean frontmatter."""

    def test_all_new_files_exist(self):
        for relative_path, _ in NEW_DIATAXIS_FILES:
            with self.subTest(path=relative_path):
                self.assertTrue(
                    (DOCS_DIR / relative_path).is_file(),
                    f"Expected docs/{relative_path} to exist",
                )

    def test_all_new_files_are_non_empty(self):
        for relative_path, _ in NEW_DIATAXIS_FILES:
            with self.subTest(path=relative_path):
                content = (DOCS_DIR / relative_path).read_text(encoding="utf-8")
                self.assertTrue(content.strip(), f"docs/{relative_path} should not be empty")

    def test_all_new_files_have_no_leading_bom(self):
        for relative_path, _ in NEW_DIATAXIS_FILES:
            with self.subTest(path=relative_path):
                raw_bytes = (DOCS_DIR / relative_path).read_bytes()
                self.assertFalse(raw_bytes.startswith(b"\xef\xbb\xbf"))

    def test_all_new_files_start_with_frontmatter_fence(self):
        for relative_path, _ in NEW_DIATAXIS_FILES:
            with self.subTest(path=relative_path):
                content = (DOCS_DIR / relative_path).read_text(encoding="utf-8")
                self.assertTrue(content.startswith("---\n"))


class DiataxisFrontmatterTextFormatTests(unittest.TestCase):
    """Regex-based OKF frontmatter checks that don't require a YAML parser."""

    def test_frontmatter_declares_okf_version(self):
        for relative_path, _ in NEW_DIATAXIS_FILES:
            with self.subTest(path=relative_path):
                content = (DOCS_DIR / relative_path).read_text(encoding="utf-8")
                raw, _ = _extract_frontmatter(content)
                self.assertIsNotNone(raw, f"docs/{relative_path} missing frontmatter block")
                self.assertRegex(raw, r"okf_version:\s*0\.[12]")

    def test_frontmatter_declares_type_documentation(self):
        for relative_path, _ in NEW_DIATAXIS_FILES:
            with self.subTest(path=relative_path):
                content = (DOCS_DIR / relative_path).read_text(encoding="utf-8")
                raw, _ = _extract_frontmatter(content)
                self.assertRegex(raw, r"type:\s*documentation")

    def test_frontmatter_declares_expected_title(self):
        for relative_path, expected_title in NEW_DIATAXIS_FILES:
            with self.subTest(path=relative_path):
                content = (DOCS_DIR / relative_path).read_text(encoding="utf-8")
                raw, _ = _extract_frontmatter(content)
                # Title may or may not be quoted depending on special characters.
                self.assertTrue(
                    f'title: "{expected_title}"' in raw or f"title: {expected_title}" in raw,
                    f"docs/{relative_path} frontmatter missing expected title {expected_title!r}",
                )

    def test_frontmatter_declares_timestamp_and_topics(self):
        for relative_path, _ in NEW_DIATAXIS_FILES:
            with self.subTest(path=relative_path):
                content = (DOCS_DIR / relative_path).read_text(encoding="utf-8")
                raw, _ = _extract_frontmatter(content)
                self.assertRegex(raw, r'timestamp:\s*"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z"')
                self.assertIn("topics:", raw)
                self.assertIn('"dsom"', raw)


@unittest.skipUnless(HAS_YAML, "PyYAML is not installed in this environment")
class DiataxisFrontmatterStructureTests(unittest.TestCase):
    """Structural (parsed-YAML) OKF frontmatter checks."""

    def test_all_mandatory_okf_fields_present_and_typed(self):
        for relative_path, expected_title in NEW_DIATAXIS_FILES:
            with self.subTest(path=relative_path):
                content = (DOCS_DIR / relative_path).read_text(encoding="utf-8")
                _, parsed = _extract_frontmatter(content)
                self.assertIsInstance(parsed, dict)
                self.assertIn(parsed["okf_version"], (0.1, 0.2))
                self.assertEqual(parsed["type"], "documentation")
                self.assertEqual(parsed["title"], expected_title)
                self.assertIsInstance(parsed["timestamp"], str)
                self.assertIsInstance(parsed["topics"], list)
                self.assertIn("dsom", parsed["topics"])


class MkdocsDiataxisNavTests(unittest.TestCase):
    """Verify the 'Diátaxis Developer Space' nav section in mkdocs.yml."""

    @classmethod
    def setUpClass(cls):
        cls.content = MKDOCS_PATH.read_text(encoding="utf-8")

    def test_diataxis_section_declared(self):
        self.assertIn("Diátaxis Developer Space:", self.content)

    def test_diataxis_subsections_declared(self):
        for subsection in ("Tutorials:", "How-To Guides:", "Reference Material:", "Explanation:"):
            with self.subTest(subsection=subsection):
                self.assertIn(subsection, self.content)

    def test_all_nav_entries_present_with_docs_relative_paths(self):
        for label, path in DIATAXIS_NAV_ENTRIES:
            with self.subTest(label=label, path=path):
                pattern = re.compile(
                    rf"{re.escape(label)}:\s*{re.escape(path)}\s*$", re.MULTILINE
                )
                self.assertRegex(
                    self.content, pattern, f"Expected nav entry {label!r} -> {path!r}"
                )

    def test_all_nav_entries_resolve_to_real_files(self):
        for _, path in DIATAXIS_NAV_ENTRIES:
            with self.subTest(path=path):
                self.assertTrue(
                    (DOCS_DIR / path).is_file(),
                    f"Nav path {path!r} does not resolve to a file under docs/",
                )

    def test_no_diataxis_nav_value_has_doubly_prefixed_docs_path(self):
        for _, path in DIATAXIS_NAV_ENTRIES:
            with self.subTest(path=path):
                self.assertNotIn(f"docs/{path}", self.content)


@unittest.skipUnless(HAS_YAML, "PyYAML is not installed in this environment")
class MkdocsDiataxisNavYamlStructureTests(unittest.TestCase):
    """Structural validation of the Diátaxis nav tree."""

    @classmethod
    def setUpClass(cls):
        with MKDOCS_PATH.open(encoding="utf-8") as fh:
            cls.config = yaml.safe_load(fh)

    def _find_diataxis_section(self):
        for entry in self.config["nav"]:
            if isinstance(entry, dict) and "Diátaxis Developer Space" in entry:
                return entry["Diátaxis Developer Space"]
        raise AssertionError("Could not find 'Diátaxis Developer Space' nav section")

    def test_diataxis_section_has_four_quadrant_subsections(self):
        section = self._find_diataxis_section()
        labels = [next(iter(item.keys())) for item in section]
        self.assertEqual(
            labels, ["Tutorials", "How-To Guides", "Reference Material", "Explanation"]
        )

    def test_reference_material_subsection_has_ten_entries(self):
        section = self._find_diataxis_section()
        reference_entries = None
        for item in section:
            if "Reference Material" in item:
                reference_entries = item["Reference Material"]
        self.assertIsNotNone(reference_entries)
        # Overview + 9 Python module reference pages == 10 entries.
        self.assertEqual(len(reference_entries), 10)


class LlmsTxtDiataxisSectionTests(unittest.TestCase):
    """Verify the 'Diátaxis Developer Space' section registered in llms.txt."""

    @classmethod
    def setUpClass(cls):
        cls.content = LLMS_TXT_PATH.read_text(encoding="utf-8")

    def test_section_header_present(self):
        self.assertIn("## Diátaxis Developer Space", self.content)

    def test_section_links_resolve_to_real_files(self):
        section_match = re.search(
            r"## Diátaxis Developer Space\n(.*?)(?:\n## |\Z)", self.content, re.DOTALL
        )
        self.assertIsNotNone(section_match, "Could not locate Diátaxis Developer Space section")
        section_text = section_match.group(1)
        links = re.findall(r"\[[^\]]+\]\(([^)]+\.md)\)", section_text)
        self.assertGreater(len(links), 0, "Expected markdown links inside the Diátaxis section")
        for relative_path in links:
            with self.subTest(path=relative_path):
                self.assertTrue(
                    (REPO_ROOT / relative_path).is_file(),
                    f"llms.txt references a non-existent file: {relative_path}",
                )


class DocsSummaryMdTests(unittest.TestCase):
    """Verify the new docs/SUMMARY.md file (GitBook-style ToC scoped to docs/)."""

    @classmethod
    def setUpClass(cls):
        cls.content = SUMMARY_MD_PATH.read_text(encoding="utf-8")

    def test_file_exists_and_not_empty(self):
        self.assertTrue(SUMMARY_MD_PATH.is_file())
        self.assertTrue(self.content.strip())

    def test_has_valid_okf_frontmatter(self):
        raw, _ = _extract_frontmatter(self.content)
        self.assertIsNotNone(raw)
        self.assertRegex(raw, r"okf_version:\s*0\.1")
        self.assertIn('title: "Table of Contents (GitBook Summary)"', raw)

    def test_declares_all_four_diataxis_sections(self):
        for heading in ("Tutorials", "How-To Guides", "Reference Material", "Explanation and Design"):
            with self.subTest(heading=heading):
                self.assertIn(heading, self.content)

    def test_all_relative_markdown_links_resolve(self):
        """Every relative link in docs/SUMMARY.md must resolve to a real file,
        interpreted relative to docs/SUMMARY.md's own directory (docs/)."""
        links = re.findall(r"\[[^\]]+\]\(([^)]+\.md)\)", self.content)
        self.assertGreater(len(links), 0, "docs/SUMMARY.md has no markdown links")
        for relative_path in links:
            with self.subTest(path=relative_path):
                resolved = (SUMMARY_MD_PATH.parent / relative_path).resolve()
                self.assertTrue(
                    resolved.is_file(),
                    f"docs/SUMMARY.md references a non-existent file: {relative_path} "
                    f"(resolved to {resolved})",
                )


class GoogleSearchConsoleVerificationTests(unittest.TestCase):
    """Verify Google Search Console meta tag override and HTML verification file."""

    def test_override_main_html_exists_and_contains_meta_tag(self):
        override_file = DOCS_DIR / "overrides" / "main.html"
        self.assertTrue(override_file.is_file(), "Expected docs/overrides/main.html to exist")
        content = override_file.read_text(encoding="utf-8")
        self.assertIn('{% extends "base.html" %}', content)
        self.assertIn('<meta name="google-site-verification" content="OKJ30rPxLeaG-OocY3C2xkXbYEVgwfMMoaOycjWQJJw" />', content)

    def test_verification_html_files_exist_and_contain_token(self):
        root_html = REPO_ROOT / "google953c3228b9041989.html"
        docs_html = DOCS_DIR / "google953c3228b9041989.html"
        expected_body = "google-site-verification: google953c3228b9041989.html"

        self.assertTrue(root_html.is_file(), "Expected google953c3228b9041989.html at root")
        self.assertTrue(docs_html.is_file(), "Expected docs/google953c3228b9041989.html")

        self.assertEqual(root_html.read_text(encoding="utf-8").strip(), expected_body)
        self.assertEqual(docs_html.read_text(encoding="utf-8").strip(), expected_body)


class SitemapDiataxisRegressionTests(unittest.TestCase):
    """Regression tests confirming the new Diátaxis URLs made it into the
    unified sitemaps generated by tools/generate_sitemaps.py."""

    @classmethod
    def setUpClass(cls):
        cls.root_lines = {
            line.strip()
            for line in (REPO_ROOT / "sitemap.txt").read_text(encoding="utf-8").splitlines()
            if line.strip()
        }
        cls.docs_lines = {
            line.strip()
            for line in (REPO_ROOT / "docs" / "sitemap.txt").read_text(encoding="utf-8").splitlines()
            if line.strip()
        }

    def test_diataxis_sample_urls_present_for_github_pages(self):
        for path in DIATAXIS_SITEMAP_SAMPLE_PATHS:
            with self.subTest(path=path):
                self.assertIn(f"{GITHUB_PAGES_BASE}{path}", self.root_lines)

    def test_diataxis_sample_urls_present_for_readthedocs(self):
        for path in DIATAXIS_SITEMAP_SAMPLE_PATHS:
            with self.subTest(path=path):
                self.assertIn(f"{READTHEDOCS_BASE}{path}", self.root_lines)

    def test_root_and_docs_sitemap_txt_agree_on_diataxis_urls(self):
        for path in DIATAXIS_SITEMAP_SAMPLE_PATHS:
            with self.subTest(path=path):
                url = f"{GITHUB_PAGES_BASE}{path}"
                self.assertIn(url, self.root_lines)
                self.assertIn(url, self.docs_lines)


if __name__ == "__main__":
    unittest.main()