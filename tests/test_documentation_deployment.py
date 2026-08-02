"""
Unit tests for the GitBook and GitHub Pages dual documentation deployment.

This verifies that both the legacy GitBook documentation host
(`https://malaysia-open-source-community.gitbook.io/...`) and the
project's own GitHub Pages site
(`https://linuxmalaysia.github.io/deep-state-of-mind-for-my-ai/`) are active,
fully documented, and configured side-by-side.

The deployment touches several independent surfaces that must all stay in
sync:

1. `mkdocs.yml` declares the canonical `site_url` pointing at the GitHub Pages host.
2. `README.md` gains both documentation badges and "Official Live
   Documentation" callouts linking to both sites, plus corresponding
   entries in the "Key Documents" table.
3. `llms.txt` references both GitHub Pages and GitBook.
4. Several governance documents (`AI-MASTER-PROTOCOL.md`,
   `DSOM-EFFICIENCY-PROTOCOLS.md`, `DSOM-TOKEN-EFFICIENCY-REPORT.md`,
   `OPERATIONAL-SOVEREIGNTY.md`, `PERSONALIZATION.md`) reference both hosts.
5. `.agents/skills/publish-to-blogger/SKILL.md` updates both its prose
   instructions and its embedded HTML snippet to link to both hosts.
6. Rule 14 (Omni-Documentation Sync) in `AGENTS.md` / `.agents/AGENTS.md`
   describes `SUMMARY.md` and `mkdocs.yml` as GitBook navigation and
   MkDocs/GitHub Pages navigation layers respectively.
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

MKDOCS_PATH = REPO_ROOT / "mkdocs.yml"
README_PATH = REPO_ROOT / "README.md"
LLMS_TXT_PATH = REPO_ROOT / "llms.txt"
AGENTS_PATH = REPO_ROOT / ".agents" / "AGENTS.md"
ROOT_AGENTS_PATH = REPO_ROOT / "AGENTS.md"
BLOGGER_SKILL_PATH = REPO_ROOT / ".agents" / "skills" / "publish-to-blogger" / "SKILL.md"

GITHUB_PAGES_URL = "https://linuxmalaysia.github.io/deep-state-of-mind-for-my-ai/"
GITBOOK_URL = (
    "https://malaysia-open-source-community.gitbook.io/"
    "deep-state-of-mind-dsom-protocol-for-my-ai"
)

# Governance/personalisation docs referencing both hosts
GOVERNANCE_DOCS_WITH_BOTH_LINKS = [
    REPO_ROOT / "docs" / "governance" / "AI-MASTER-PROTOCOL.md",
    REPO_ROOT / "docs" / "governance" / "DSOM-EFFICIENCY-PROTOCOLS.md",
    REPO_ROOT / "docs" / "governance" / "DSOM-TOKEN-EFFICIENCY-REPORT.md",
    REPO_ROOT / "docs" / "governance" / "OPERATIONAL-SOVEREIGNTY.md",
    REPO_ROOT / "docs" / "PERSONALIZATION.md",
]


class MkdocsSiteUrlTests(unittest.TestCase):
    """Verify mkdocs.yml declares the canonical GitHub Pages site_url."""

    @classmethod
    def setUpClass(cls):
        cls.content = MKDOCS_PATH.read_text(encoding="utf-8")

    def test_mkdocs_yml_exists(self):
        self.assertTrue(MKDOCS_PATH.is_file())

    def test_site_url_declared_with_expected_value(self):
        self.assertRegex(
            self.content,
            re.compile(rf"^site_url:\s*{re.escape(GITHUB_PAGES_URL)}\s*$", re.MULTILINE),
            "Expected mkdocs.yml to declare the GitHub Pages site_url",
        )


@unittest.skipUnless(HAS_YAML, "PyYAML not installed")
class MkdocsSiteUrlYamlStructureTests(unittest.TestCase):
    """Structural validation of site_url via a parsed YAML document."""

    @classmethod
    def setUpClass(cls):
        with MKDOCS_PATH.open(encoding="utf-8") as fh:
            cls.config = yaml.safe_load(fh)

    def test_site_url_key_present(self):
        self.assertIn("site_url", self.config)

    def test_site_url_value_matches_expected_github_pages_host(self):
        self.assertEqual(self.config["site_url"], GITHUB_PAGES_URL)


class ReadmeDualDeploymentTests(unittest.TestCase):
    """Verify README.md surfaces both GitHub Pages and GitBook documentation."""

    @classmethod
    def setUpClass(cls):
        cls.content = README_PATH.read_text(encoding="utf-8")

    def test_readme_exists(self):
        self.assertTrue(README_PATH.is_file())

    def test_documentation_badges_present(self):
        self.assertIn(
            "[![Documentation](https://img.shields.io/badge/Docs-GitHub%20Pages-blue.svg)]"
            f"({GITHUB_PAGES_URL})",
            self.content,
        )
        self.assertIn(
            f"[![GitBook](https://img.shields.io/badge/Docs-GitBook-blue.svg)]({GITBOOK_URL})",
            self.content,
        )

    def test_official_live_documentation_callouts_present(self):
        self.assertIn(
            f"- **GitHub Pages:** [{GITHUB_PAGES_URL}]({GITHUB_PAGES_URL})",
            self.content,
        )
        self.assertIn(
            f"- **GitBook:** [{GITBOOK_URL}]({GITBOOK_URL})",
            self.content,
        )

    def test_key_documents_table_lists_both_official_documentations(self):
        self.assertIn(
            f"| [Official Live Documentation (GitHub Pages)]({GITHUB_PAGES_URL}) | 🌐 **Web-Based Sovereign Book** — Official compiled, searchable documentation on GitHub Pages. |",
            self.content,
        )
        self.assertIn(
            f"| [Official Live Documentation (GitBook)]({GITBOOK_URL}) | 📖 **Cloud Sovereign Book** — Official compiled, searchable documentation hosted on GitBook. |",
            self.content,
        )


class LlmsTxtDualDeploymentTests(unittest.TestCase):
    """Verify llms.txt references both GitHub Pages and GitBook."""

    @classmethod
    def setUpClass(cls):
        cls.content = LLMS_TXT_PATH.read_text(encoding="utf-8")

    def test_llms_txt_exists(self):
        self.assertTrue(LLMS_TXT_PATH.is_file())

    def test_gitbook_summary_label_present(self):
        self.assertIn("GitBook Summary / Documentation Index", self.content)

    def test_both_live_documentations_present(self):
        self.assertIn(
            f"- [Official Live Documentation (GitHub Pages)]({GITHUB_PAGES_URL}): Web-based compiled, searchable documentation.",
            self.content,
        )
        self.assertIn(
            f"- [Official Live Documentation (GitBook)]({GITBOOK_URL}): Cloud-hosted compiled, searchable documentation.",
            self.content,
        )


class GovernanceDocsDualLinkTests(unittest.TestCase):
    """Verify governance/personalisation docs link to both GitHub Pages and GitBook."""

    def test_docs_exist(self):
        for path in GOVERNANCE_DOCS_WITH_BOTH_LINKS:
            with self.subTest(path=path):
                self.assertTrue(path.is_file(), f"Expected {path} to exist")

    def test_both_urls_present(self):
        for path in GOVERNANCE_DOCS_WITH_BOTH_LINKS:
            with self.subTest(path=path):
                content = path.read_text(encoding="utf-8")
                self.assertIn(
                    GITHUB_PAGES_URL,
                    content,
                    f"Expected {path} to reference the GitHub Pages URL",
                )
                self.assertIn(
                    GITBOOK_URL,
                    content,
                    f"Expected {path} to reference the GitBook URL",
                )


class PublishToBloggerSkillDualDeploymentTests(unittest.TestCase):
    """Verify the publish-to-blogger skill emits both GitHub Pages and GitBook links."""

    @classmethod
    def setUpClass(cls):
        cls.content = BLOGGER_SKILL_PATH.read_text(encoding="utf-8")

    def test_skill_file_exists(self):
        self.assertTrue(BLOGGER_SKILL_PATH.is_file())

    def test_instructions_mention_both_links(self):
        self.assertIn(
            "GitHub, GitLab, GitHub Pages, and GitBook links just above the DSOM signature",
            self.content,
        )

    def test_html_snippet_contains_both_list_items(self):
        self.assertIn(
            '<strong>GitHub Pages:</strong> <a href="'
            f'{GITHUB_PAGES_URL}" target="_blank">DSOM Protocol Documentation</a>',
            self.content,
        )
        self.assertIn(
            '<strong>GitBook:</strong> <a href="'
            f'{GITBOOK_URL}" target="_blank">DSOM GitBook Documentation</a>',
            self.content,
        )


class AgentsOmniDocumentationSyncRuleTests(unittest.TestCase):
    """Verify AGENTS.md Rule 14 wording reflects both platforms."""

    def test_rule_14_describes_summary_md_as_gitbook_navigation(self):
        content = AGENTS_PATH.read_text(encoding="utf-8")
        self.assertIn(
            "`SUMMARY.md` (for GitBook navigation)", content
        )

    def test_rule_14_describes_mkdocs_yml_as_mkdocs_or_github_pages(self):
        content = AGENTS_PATH.read_text(encoding="utf-8")
        self.assertIn(
            "`mkdocs.yml` (for MkDocs/GitHub Pages navigation)", content
        )

    def test_root_rule_14_contains_gitbook_and_github_pages(self):
        content = ROOT_AGENTS_PATH.read_text(encoding="utf-8")
        self.assertIn(
            "`SUMMARY.md` (for GitBook navigation)", content
        )
        self.assertIn(
            "`mkdocs.yml` (for MkDocs/GitHub Pages navigation)", content
        )


if __name__ == "__main__":
    unittest.main()
