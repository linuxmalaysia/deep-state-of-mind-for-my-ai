"""
Unit tests for the "Legal Notice & Disclaimer" feature introduced by this PR.

This PR adds:

1. `LEGAL-NOTICE.md` (new, repo root) - an OKF-frontmatter'd documentation
   page containing the project's educational-purpose statement, critical
   assumptions, privacy statement, and liability disclaimer.
2. `docs/LEGAL-NOTICE.md` (new) - a relative symlink (`../LEGAL-NOTICE.md`)
   mirroring the pre-existing `docs/SECURITY.md -> ../SECURITY.md` pattern,
   so MkDocs (which resolves nav entries relative to `docs_dir`) can serve
   the root-level file.
3. `SUMMARY.md` - a new top-level GitBook table-of-contents entry linking to
   `LEGAL-NOTICE.md`.
4. `mkdocs.yml` - a new `copyright:` footer string (containing an inline
   disclaimer and a link back to the published Legal Notice page) and a new
   top-level nav entry `Legal Notice & Disclaimer: LEGAL-NOTICE.md`.
5. `sitemap.txt` / `docs/sitemap.txt` and `sitemap.xml` / `docs/sitemap.xml`
   - three new URLs (one per publishing platform: GitHub Pages, Read the
   Docs, GitBook) pointing at the new Legal Notice page.

These tests validate each of the above, following the conventions already
established in `tests/test_docs_symlinks.py`, `tests/test_mkdocs_nav.py`
and `tests/test_seo_sitemaps.py`.
"""
import os
import pathlib
import re
import shutil
import subprocess
import unittest
import xml.etree.ElementTree as ET

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
LEGAL_NOTICE_PATH = REPO_ROOT / "LEGAL-NOTICE.md"
DOCS_LEGAL_NOTICE_PATH = DOCS_DIR / "LEGAL-NOTICE.md"
MKDOCS_PATH = REPO_ROOT / "mkdocs.yml"
SUMMARY_PATH = REPO_ROOT / "SUMMARY.md"
GIT_AVAILABLE = shutil.which("git") is not None

GITHUB_PAGES_BASE = "https://linuxmalaysia.github.io/deep-state-of-mind-for-my-ai/"
READTHEDOCS_BASE = "https://deep-state-of-mind-for-my-ai.readthedocs.io/en/latest/"
GITBOOK_BASE = "https://malaysia-open-source-community.gitbook.io/deep-state-of-mind-dsom-protocol-for-my-ai/"

LEGAL_NOTICE_URLS = {
    "github_pages": f"{GITHUB_PAGES_BASE}LEGAL-NOTICE/",
    "readthedocs": f"{READTHEDOCS_BASE}LEGAL-NOTICE/",
    "gitbook": f"{GITBOOK_BASE}legal-notice",
}

FRONTMATTER_RE = re.compile(r"\A---\s*\r?\n(.*?)(?:\r?\n)?---\s*(?:\r?\n|\Z)", re.DOTALL)


def _is_symlink_or_windows_git_symlink(path: pathlib.Path) -> bool:
    if path.is_symlink():
        return True
    if os.name == "nt" and path.exists():
        try:
            if path.is_file():
                content = path.read_text(encoding="utf-8").strip()
                return content.startswith("../") and "\n" not in content
        except Exception:
            pass
    return False


def _read_symlink_target(path: pathlib.Path) -> str:
    if path.is_symlink():
        return os.readlink(path)
    if os.name == "nt" and path.exists():
        try:
            return path.read_text(encoding="utf-8").strip()
        except Exception:
            pass
    return os.readlink(path)


def _resolve_path(path: pathlib.Path) -> pathlib.Path:
    if path.is_symlink():
        return path.resolve()
    if os.name == "nt" and path.exists():
        try:
            if path.is_file():
                target_str = path.read_text(encoding="utf-8").strip()
                if target_str.startswith("../"):
                    resolved = (path.parent / target_str).resolve()
                    if resolved.exists():
                        return resolved
        except Exception:
            pass
    return path.resolve()


class LegalNoticeRootFileExistenceTests(unittest.TestCase):
    """Basic existence checks for the new root-level LEGAL-NOTICE.md."""

    def test_legal_notice_file_exists(self):
        self.assertTrue(LEGAL_NOTICE_PATH.is_file(), f"Expected {LEGAL_NOTICE_PATH} to exist")

    def test_legal_notice_file_is_non_empty(self):
        content = LEGAL_NOTICE_PATH.read_text(encoding="utf-8")
        self.assertTrue(content.strip())

    def test_no_leading_bom(self):
        raw_bytes = LEGAL_NOTICE_PATH.read_bytes()
        self.assertFalse(raw_bytes.startswith(b"\xef\xbb\xbf"))

    def test_starts_exactly_with_frontmatter_fence(self):
        content = LEGAL_NOTICE_PATH.read_text(encoding="utf-8")
        self.assertTrue(content.startswith("---\n"))


class LegalNoticeFrontmatterTextFormatTests(unittest.TestCase):
    """Regex-based checks that don't require a YAML parser."""

    @classmethod
    def setUpClass(cls):
        cls.content = LEGAL_NOTICE_PATH.read_text(encoding="utf-8")
        match = FRONTMATTER_RE.match(cls.content)
        assert match is not None, "LEGAL-NOTICE.md must start with a frontmatter block"
        cls.frontmatter_raw = match.group(1)
        cls.body = cls.content[match.end():]

    def test_okf_version_present(self):
        self.assertIn("okf_version: 0.1", self.frontmatter_raw)

    def test_type_is_documentation(self):
        self.assertIn("type: documentation", self.frontmatter_raw)

    def test_title_is_double_quoted_and_mentions_legal_notice(self):
        self.assertRegex(
            self.frontmatter_raw,
            r'title:\s*"Legal Notice & Disclaimer.*DSOM.*"',
        )

    def test_timestamp_is_double_quoted_iso8601(self):
        self.assertRegex(
            self.frontmatter_raw, r'timestamp: "\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z"'
        )

    def test_topics_include_expected_tags(self):
        self.assertIn(
            'topics: ["legal", "disclaimer", "privacy", "governance"]',
            self.frontmatter_raw,
        )

    def test_description_field_present(self):
        self.assertIn("description:", self.frontmatter_raw)
        self.assertIn("disclaimer of liability", self.frontmatter_raw.lower())

    def test_resource_field_points_to_root_file(self):
        self.assertIn('resource: "file:///LEGAL-NOTICE.md"', self.frontmatter_raw)


class LegalNoticeBodyContentTests(unittest.TestCase):
    """Verify the required sections and disclaimer language are present."""

    @classmethod
    def setUpClass(cls):
        content = LEGAL_NOTICE_PATH.read_text(encoding="utf-8")
        match = FRONTMATTER_RE.match(content)
        assert match is not None
        cls.body = content[match.end():]

    def test_top_level_heading_present(self):
        self.assertIn("# Legal Notice & Disclaimer", self.body)

    def test_all_four_numbered_sections_present(self):
        expected_headings = [
            "## 1. Educational and Training Purpose",
            "## 2. Reliance on Critical Assumptions",
            "## 3. Privacy Statement & Data Protection",
            "## 4. Assumption of Risk & Liability Disclaimer",
        ]
        for heading in expected_headings:
            with self.subTest(heading=heading):
                self.assertIn(heading, self.body)

    def test_sections_appear_in_ascending_order(self):
        headings = [
            "## 1. Educational and Training Purpose",
            "## 2. Reliance on Critical Assumptions",
            "## 3. Privacy Statement & Data Protection",
            "## 4. Assumption of Risk & Liability Disclaimer",
        ]
        indices = [self.body.index(h) for h in headings]
        self.assertEqual(indices, sorted(indices))

    def test_as_is_disclaimer_present(self):
        self.assertIn('provided "as-is" without warranty', self.body)

    def test_use_at_own_risk_statement_present(self):
        self.assertIn("Use of this project, its code, and its documents is at your own risk.", self.body)

    def test_privacy_statement_mentions_no_pii_storage(self):
        self.assertIn(
            "does not harvest, process, or store any actual personally identifying information (PII)",
            self.body,
        )

    def test_footer_mentions_license_and_author(self):
        self.assertIn("Harisfazillah Jamel (LinuxMalaysia)", self.body)
        self.assertIn("GNU General Public License v3.0", self.body)


class DocsLegalNoticeSymlinkExistenceTests(unittest.TestCase):
    """The new docs/LEGAL-NOTICE.md must be a real (or git-portable) symlink."""

    def test_docs_legal_notice_path_exists(self):
        self.assertTrue(DOCS_LEGAL_NOTICE_PATH.exists(), f"Expected {DOCS_LEGAL_NOTICE_PATH} to exist")

    def test_docs_legal_notice_is_a_symlink(self):
        self.assertTrue(
            _is_symlink_or_windows_git_symlink(DOCS_LEGAL_NOTICE_PATH),
            "docs/LEGAL-NOTICE.md must be a real symlink or git symlink pointer",
        )


class DocsLegalNoticeSymlinkTargetTests(unittest.TestCase):
    def test_symlink_target_is_expected_relative_path(self):
        target = pathlib.Path(_read_symlink_target(DOCS_LEGAL_NOTICE_PATH)).as_posix()
        self.assertEqual(target, "../LEGAL-NOTICE.md")

    def test_symlink_target_is_relative_not_absolute(self):
        target = _read_symlink_target(DOCS_LEGAL_NOTICE_PATH)
        self.assertFalse(pathlib.PurePath(target).is_absolute())


class DocsLegalNoticeSymlinkResolutionTests(unittest.TestCase):
    def test_symlink_resolves_to_root_level_file(self):
        self.assertEqual(
            _resolve_path(DOCS_LEGAL_NOTICE_PATH),
            LEGAL_NOTICE_PATH.resolve(),
        )

    def test_symlink_does_not_dangle(self):
        self.assertTrue(_resolve_path(DOCS_LEGAL_NOTICE_PATH).is_file())

    def test_symlink_content_matches_root_file_content(self):
        via_symlink_target = _resolve_path(DOCS_LEGAL_NOTICE_PATH)
        via_symlink = via_symlink_target.read_text(encoding="utf-8")
        via_root = LEGAL_NOTICE_PATH.read_text(encoding="utf-8")
        self.assertEqual(via_symlink, via_root)


@unittest.skipUnless(GIT_AVAILABLE, "git executable not available")
class DocsLegalNoticeGitIndexTests(unittest.TestCase):
    """Verify Git itself tracks docs/LEGAL-NOTICE.md using symlink mode (120000)."""

    @classmethod
    def setUpClass(cls):
        git_path = shutil.which("git")
        if git_path is None:
            raise RuntimeError("git executable not found in PATH")  # noqa: TRY003
        git_executable = str(pathlib.Path(git_path).resolve())
        result = subprocess.run(
            [git_executable, "ls-files", "-s", "docs/LEGAL-NOTICE.md", "LEGAL-NOTICE.md"],
            cwd=REPO_ROOT,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )
        cls.entries = {}
        for line in result.stdout.splitlines():
            meta, path = line.split("\t", 1)
            mode = meta.split(" ", 1)[0]
            cls.entries[path] = mode

    def test_docs_copy_tracked_with_symlink_mode(self):
        self.assertEqual(self.entries.get("docs/LEGAL-NOTICE.md"), "120000")

    def test_root_copy_tracked_with_regular_file_mode(self):
        self.assertEqual(self.entries.get("LEGAL-NOTICE.md"), "100644")


class SummaryMdLegalNoticeLinkTests(unittest.TestCase):
    """Verify SUMMARY.md links to the new Legal Notice page."""

    @classmethod
    def setUpClass(cls):
        cls.content = SUMMARY_PATH.read_text(encoding="utf-8")

    def test_legal_notice_link_present(self):
        self.assertIn("* [⚖️ Legal Notice & Disclaimer](LEGAL-NOTICE.md)", self.content)

    def test_legal_notice_link_target_resolves_to_real_file(self):
        matches = re.findall(r"\[[^\]]*Legal Notice[^\]]*\]\(([^)]+)\)", self.content)
        self.assertEqual(len(matches), 1)
        target = REPO_ROOT / matches[0]
        self.assertTrue(target.is_file())

    def test_legal_notice_entry_appears_after_security_policy_entry(self):
        security_idx = self.content.index("[🛡️ Security Policy](SECURITY.md)")
        legal_idx = self.content.index("[⚖️ Legal Notice & Disclaimer](LEGAL-NOTICE.md)")
        self.assertLess(security_idx, legal_idx)

    def test_legal_notice_entry_appears_in_top_level_table_of_contents(self):
        # The top-level ToC section ends where "## 🏛️ 1. Sovereign Governance" begins.
        toc_end = self.content.index("## 🏛️ 1. Sovereign Governance")
        legal_idx = self.content.index("[⚖️ Legal Notice & Disclaimer](LEGAL-NOTICE.md)")
        self.assertLess(legal_idx, toc_end)


class MkdocsYamlLegalNoticeNavTests(unittest.TestCase):
    """Verify mkdocs.yml declares the new nav entry for Legal Notice & Disclaimer."""

    @classmethod
    def setUpClass(cls):
        cls.content = MKDOCS_PATH.read_text(encoding="utf-8")

    def test_nav_declares_legal_notice_entry(self):
        self.assertRegex(self.content, r"Legal Notice & Disclaimer:\s*LEGAL-NOTICE\.md")

    def test_nav_entry_resolves_within_docs_dir(self):
        self.assertTrue((DOCS_DIR / "LEGAL-NOTICE.md").exists())

    def test_nav_entry_appears_after_security_policy_and_before_governance(self):
        security_idx = self.content.index("Security Policy: SECURITY.md")
        legal_idx = self.content.index("Legal Notice & Disclaimer: LEGAL-NOTICE.md")
        governance_idx = self.content.index("Governance:")
        self.assertLess(security_idx, legal_idx)
        self.assertLess(legal_idx, governance_idx)


class MkdocsYamlCopyrightFieldTests(unittest.TestCase):
    """Verify the new `copyright:` footer field added to mkdocs.yml."""

    @classmethod
    def setUpClass(cls):
        cls.content = MKDOCS_PATH.read_text(encoding="utf-8")
        match = re.search(r"^copyright:\s*'(.*)'\s*$", cls.content, re.MULTILINE)
        assert match is not None, "Expected a single-quoted 'copyright:' scalar in mkdocs.yml"
        cls.copyright_value = match.group(1)

    def test_copyright_field_present(self):
        self.assertIn("copyright:", self.content)

    def test_copyright_mentions_educational_purpose(self):
        self.assertIn(
            "compiled strictly for training, educational, and planning proposal purposes",
            self.copyright_value,
        )

    def test_copyright_mentions_use_at_own_risk(self):
        self.assertIn("Use at your own risk.", self.copyright_value)

    def test_copyright_mentions_not_responsible_disclaimer(self):
        self.assertIn("We are not going to be responsible.", self.copyright_value)

    def test_copyright_contains_link_to_published_legal_notice_page(self):
        self.assertIn(
            'href="https://linuxmalaysia.github.io/deep-state-of-mind-for-my-ai/LEGAL-NOTICE/"',
            self.copyright_value,
        )

    def test_copyright_link_anchor_text_matches_nav_label(self):
        self.assertIn(">Legal Notice & Disclaimer</a>", self.copyright_value)

    def test_copyright_field_precedes_hooks_section(self):
        copyright_idx = self.content.index("copyright:")
        hooks_idx = self.content.index("hooks:")
        self.assertLess(copyright_idx, hooks_idx)


@unittest.skipUnless(HAS_YAML, "PyYAML not installed")
class MkdocsYamlLegalNoticeStructureTests(unittest.TestCase):
    """Structural (YAML-parsed) validation, skipped if PyYAML is absent."""

    @classmethod
    def setUpClass(cls):
        with MKDOCS_PATH.open(encoding="utf-8") as fh:
            cls.config = yaml.safe_load(fh)

    def test_copyright_key_parses_as_a_string(self):
        self.assertIsInstance(self.config.get("copyright"), str)

    def test_top_level_nav_contains_legal_notice_entry(self):
        top_level_labels = {
            list(entry.keys())[0]
            for entry in self.config["nav"]
            if isinstance(entry, dict)
        }
        self.assertIn("Legal Notice & Disclaimer", top_level_labels)

    def test_legal_notice_nav_entry_maps_to_expected_path(self):
        for entry in self.config["nav"]:
            if isinstance(entry, dict) and "Legal Notice & Disclaimer" in entry:
                self.assertEqual(entry["Legal Notice & Disclaimer"], "LEGAL-NOTICE.md")
                return
        self.fail("Legal Notice & Disclaimer nav entry not found")


class SitemapLegalNoticeUrlTests(unittest.TestCase):
    """Verify the three new Legal Notice URLs exist in every sitemap copy."""

    @classmethod
    def setUpClass(cls):
        cls.root_txt_lines = {
            line.strip()
            for line in (REPO_ROOT / "sitemap.txt").read_text(encoding="utf-8").splitlines()
            if line.strip()
        }
        cls.docs_txt_lines = {
            line.strip()
            for line in (REPO_ROOT / "docs" / "sitemap.txt").read_text(encoding="utf-8").splitlines()
            if line.strip()
        }
        namespace = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        cls.root_xml_locs = {
            loc.text
            for loc in ET.parse(REPO_ROOT / "sitemap.xml").getroot().findall(".//ns:url/ns:loc", namespace)
        }
        cls.docs_xml_locs = {
            loc.text
            for loc in ET.parse(REPO_ROOT / "docs" / "sitemap.xml").getroot().findall(".//ns:url/ns:loc", namespace)
        }

    def test_all_platform_urls_present_in_root_sitemap_txt(self):
        for platform, url in LEGAL_NOTICE_URLS.items():
            with self.subTest(platform=platform):
                self.assertIn(url, self.root_txt_lines)

    def test_all_platform_urls_present_in_docs_sitemap_txt(self):
        for platform, url in LEGAL_NOTICE_URLS.items():
            with self.subTest(platform=platform):
                self.assertIn(url, self.docs_txt_lines)

    def test_all_platform_urls_present_in_root_sitemap_xml(self):
        for platform, url in LEGAL_NOTICE_URLS.items():
            with self.subTest(platform=platform):
                self.assertIn(url, self.root_xml_locs)

    def test_all_platform_urls_present_in_docs_sitemap_xml(self):
        for platform, url in LEGAL_NOTICE_URLS.items():
            with self.subTest(platform=platform):
                self.assertIn(url, self.docs_xml_locs)

    def test_github_pages_and_readthedocs_urls_use_uppercase_trailing_slash_form(self):
        self.assertTrue(LEGAL_NOTICE_URLS["github_pages"].endswith("LEGAL-NOTICE/"))
        self.assertTrue(LEGAL_NOTICE_URLS["readthedocs"].endswith("LEGAL-NOTICE/"))

    def test_gitbook_url_uses_lowercase_no_trailing_slash_form(self):
        self.assertTrue(LEGAL_NOTICE_URLS["gitbook"].endswith("legal-notice"))
        self.assertFalse(LEGAL_NOTICE_URLS["gitbook"].endswith("/"))

    def test_lowercase_github_pages_variant_is_not_present(self):
        # Regression guard: GitHub Pages / Read the Docs slugs must stay
        # uppercase ("LEGAL-NOTICE"), matching the on-disk filename casing;
        # a lowercase variant would indicate an inconsistent slug generator.
        lowercase_variant = f"{GITHUB_PAGES_BASE}legal-notice/"
        self.assertNotIn(lowercase_variant, self.root_txt_lines)

    def test_xml_lastmod_present_for_each_legal_notice_url(self):
        namespace = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        root = ET.parse(REPO_ROOT / "sitemap.xml").getroot()
        for platform, url in LEGAL_NOTICE_URLS.items():
            with self.subTest(platform=platform):
                found = False
                for url_node in root.findall(".//ns:url", namespace):
                    loc = url_node.find("ns:loc", namespace)
                    if loc is not None and loc.text == url:
                        lastmod = url_node.find("ns:lastmod", namespace)
                        self.assertIsNotNone(lastmod, f"<url> for {url} is missing <lastmod>")
                        self.assertRegex(lastmod.text, r"^\d{4}-\d{2}-\d{2}$")
                        found = True
                        break
                self.assertTrue(found, f"Could not find <url> entry for {url} in sitemap.xml")

    def test_root_and_docs_sitemap_txt_copies_stay_identical(self):
        self.assertEqual(self.root_txt_lines, self.docs_txt_lines)

    def test_root_and_docs_sitemap_xml_copies_stay_identical(self):
        self.assertEqual(self.root_xml_locs, self.docs_xml_locs)


if __name__ == "__main__":
    unittest.main()