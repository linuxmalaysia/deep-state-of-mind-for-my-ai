"""
Unit tests for the GitBook -> GitHub Pages documentation migration.

This PR retires the legacy GitBook documentation host
(`https://malaysia-open-source-community.gitbook.io/...`) in favour of the
project's own GitHub Pages site
(`https://linuxmalaysia.github.io/deep-state-of-mind-for-my-ai/`), which is
now built and published automatically via `.github/workflows/gh-pages.yml`.

The migration touches several independent surfaces that must all stay in
sync:

1. `mkdocs.yml` gains a canonical `site_url` pointing at the GitHub Pages
   host, which MkDocs uses to generate a `sitemap.xml` and absolute
   canonical URLs.
2. `README.md` gains a documentation badge and an "Official Live
   Documentation" callout linking to the new site, plus a corresponding
   entry in the "Key Documents" table.
3. `llms.txt` renames the "GitBook Summary" entry point to a host-neutral
   "Documentation Index".
4. Several governance documents (`AI-MASTER-PROTOCOL.md`,
   `DSOM-EFFICIENCY-PROTOCOLS.md`, `DSOM-TOKEN-EFFICIENCY-REPORT.md`,
   `OPERATIONAL-SOVEREIGNTY.md`, `PERSONALIZATION.md`) that referenced the
   old GitBook URL now reference the GitHub Pages URL instead.
5. `.agents/skills/publish-to-blogger/SKILL.md` updates both its prose
   instructions and its embedded HTML snippet to link to GitHub Pages
   instead of GitBook.
6. `.agents/AGENTS.md` Rule 14 (Omni-Documentation Sync) is reworded to
   describe `SUMMARY.md` and `mkdocs.yml` as GitBook/GitHub Pages and
   MkDocs/GitHub Pages layers respectively.

These tests validate both the presence of the new GitHub Pages references
and the absence of the retired GitBook URL, to guard against regressions
that would leave stale links in the documentation.
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
BLOGGER_SKILL_PATH = REPO_ROOT / ".agents" / "skills" / "publish-to-blogger" / "SKILL.md"

GITHUB_PAGES_URL = "https://linuxmalaysia.github.io/deep-state-of-mind-for-my-ai/"
OLD_GITBOOK_URL = (
    "https://malaysia-open-source-community.gitbook.io/"
    "deep-state-of-mind-dsom-protocol-for-my-ai"
)

# Governance/personalisation docs whose GitBook reference was swapped for
# the GitHub Pages URL by this PR.
GOVERNANCE_DOCS_WITH_GITHUB_PAGES_LINK = [
    REPO_ROOT / "docs" / "governance" / "AI-MASTER-PROTOCOL.md",
    REPO_ROOT / "docs" / "governance" / "DSOM-EFFICIENCY-PROTOCOLS.md",
    REPO_ROOT / "docs" / "governance" / "DSOM-TOKEN-EFFICIENCY-REPORT.md",
    REPO_ROOT / "docs" / "governance" / "OPERATIONAL-SOVEREIGNTY.md",
    REPO_ROOT / "docs" / "PERSONALIZATION.md",
]

# The full set of files this PR touched to perform the migration; used for
# the repo-wide "old URL is gone" regression guard.
ALL_MIGRATED_FILES = GOVERNANCE_DOCS_WITH_GITHUB_PAGES_LINK + [
    README_PATH,
    LLMS_TXT_PATH,
    BLOGGER_SKILL_PATH,
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

    def test_site_url_declared_after_repo_url(self):
        # site_url was added directly below the pre-existing repo_url line;
        # confirm the ordering/adjacency was preserved.
        repo_url_index = self.content.index("repo_url:")
        site_url_index = self.content.index("site_url:")
        self.assertLess(repo_url_index, site_url_index)

    def test_site_url_declared_before_edit_uri(self):
        site_url_index = self.content.index("site_url:")
        edit_uri_index = self.content.index("edit_uri:")
        self.assertLess(site_url_index, edit_uri_index)

    def test_site_url_uses_https_scheme(self):
        self.assertTrue(GITHUB_PAGES_URL.startswith("https://"))

    def test_site_url_has_trailing_slash(self):
        # MkDocs recommends a trailing slash on site_url so that relative
        # asset/link resolution behaves correctly when deployed.
        self.assertTrue(GITHUB_PAGES_URL.endswith("/"))


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

    def test_repo_url_unaffected(self):
        self.assertEqual(
            self.config["repo_url"],
            "https://github.com/linuxmalaysia/deep-state-of-mind-for-my-ai",
        )


class ReadmeGithubPagesTests(unittest.TestCase):
    """Verify README.md surfaces the official GitHub Pages documentation."""

    @classmethod
    def setUpClass(cls):
        cls.content = README_PATH.read_text(encoding="utf-8")

    def test_readme_exists(self):
        self.assertTrue(README_PATH.is_file())

    def test_documentation_badge_present(self):
        self.assertIn(
            "[![Documentation](https://img.shields.io/badge/Docs-GitHub%20Pages-blue.svg)]"
            f"({GITHUB_PAGES_URL})",
            self.content,
        )

    def test_official_live_documentation_callout_present(self):
        self.assertIn(
            f"📖 **Official Live Documentation:** [{GITHUB_PAGES_URL}]({GITHUB_PAGES_URL})",
            self.content,
        )

    def test_key_documents_table_lists_official_documentation_first(self):
        self.assertRegex(
            self.content,
            re.compile(
                rf"\| \[Official Live Documentation\]\({re.escape(GITHUB_PAGES_URL)}\) \|.*GitHub Pages.*\|"
            ),
        )

    def test_key_documents_row_precedes_start_here_row(self):
        # The new row was inserted directly above the pre-existing
        # START-HERE.md row in the same table.
        official_docs_index = self.content.index("[Official Live Documentation]")
        start_here_row_index = self.content.index("[`START-HERE.md`](START-HERE.md)")
        self.assertLess(official_docs_index, start_here_row_index)

    def test_badge_and_callout_appear_in_header_area(self):
        # Confirms the badge/callout sit in the header area of the README,
        # above the "What is DSOM?" section, not buried further down the
        # document.
        what_is_dsom_index = self.content.index("## 🎯 What is DSOM?")
        badge_index = self.content.index("Docs-GitHub%20Pages")
        callout_index = self.content.index("Official Live Documentation:")
        self.assertLess(badge_index, what_is_dsom_index)
        self.assertLess(callout_index, what_is_dsom_index)

    def test_old_gitbook_url_absent(self):
        self.assertNotIn(OLD_GITBOOK_URL, self.content)


class LlmsTxtDocumentationIndexTests(unittest.TestCase):
    """Verify llms.txt no longer references GitBook by name."""

    @classmethod
    def setUpClass(cls):
        cls.content = LLMS_TXT_PATH.read_text(encoding="utf-8")

    def test_llms_txt_exists(self):
        self.assertTrue(LLMS_TXT_PATH.is_file())

    def test_documentation_index_entry_present(self):
        self.assertIn(
            "- [Documentation Index](SUMMARY.md): Navigation index for "
            "documentation integration.",
            self.content,
        )

    def test_gitbook_summary_label_removed(self):
        self.assertNotIn("GitBook Summary", self.content)

    def test_gitbook_integration_description_removed(self):
        self.assertNotIn("Navigation index for GitBook integration.", self.content)

    def test_summary_md_still_referenced(self):
        # The underlying target file must not have been removed, only
        # relabelled.
        self.assertIn("(SUMMARY.md)", self.content)

    def test_old_gitbook_url_absent(self):
        self.assertNotIn(OLD_GITBOOK_URL, self.content)


class GovernanceDocsGitHubPagesLinkTests(unittest.TestCase):
    """Verify governance/personalisation docs link to GitHub Pages."""

    def test_docs_exist(self):
        for path in GOVERNANCE_DOCS_WITH_GITHUB_PAGES_LINK:
            with self.subTest(path=path):
                self.assertTrue(path.is_file(), f"Expected {path} to exist")

    def test_github_pages_url_present(self):
        for path in GOVERNANCE_DOCS_WITH_GITHUB_PAGES_LINK:
            with self.subTest(path=path):
                content = path.read_text(encoding="utf-8")
                self.assertIn(
                    GITHUB_PAGES_URL,
                    content,
                    f"Expected {path} to reference the GitHub Pages URL",
                )

    def test_old_gitbook_url_absent(self):
        for path in GOVERNANCE_DOCS_WITH_GITHUB_PAGES_LINK:
            with self.subTest(path=path):
                content = path.read_text(encoding="utf-8")
                self.assertNotIn(
                    OLD_GITBOOK_URL,
                    content,
                    f"Found stale GitBook URL still present in {path}",
                )

    def test_operational_sovereignty_updates_both_occurrences(self):
        # This file references the docs host in two places: once as a
        # markdown link (`[URL](URL)`, i.e. two literal occurrences of the
        # URL string) in the "Authoritative References" section, and once
        # in the footer signature block. Both locations must be migrated.
        content = (REPO_ROOT / "docs" / "governance" / "OPERATIONAL-SOVEREIGNTY.md").read_text(
            encoding="utf-8"
        )
        self.assertEqual(content.count(GITHUB_PAGES_URL), 3)
        self.assertIn(
            f"* **Official Documentation (GitHub Pages):** [{GITHUB_PAGES_URL}]({GITHUB_PAGES_URL})",
            content,
        )
        self.assertIn(f"*Official Documentation: <{GITHUB_PAGES_URL}>*", content)

    def test_ai_master_protocol_authoritative_reference_updated(self):
        content = (REPO_ROOT / "docs" / "governance" / "AI-MASTER-PROTOCOL.md").read_text(
            encoding="utf-8"
        )
        self.assertIn(
            f"2. **Official Documentation (GitHub Pages):** [{GITHUB_PAGES_URL}]({GITHUB_PAGES_URL})",
            content,
        )

    def test_personalization_doc_reference_updated(self):
        content = (REPO_ROOT / "docs" / "PERSONALIZATION.md").read_text(encoding="utf-8")
        self.assertIn(
            f"> 2. **GitHub Pages:** [{GITHUB_PAGES_URL}]({GITHUB_PAGES_URL})",
            content,
        )

    def test_efficiency_protocols_and_token_report_share_identical_link_format(self):
        efficiency_content = (
            REPO_ROOT / "docs" / "governance" / "DSOM-EFFICIENCY-PROTOCOLS.md"
        ).read_text(encoding="utf-8")
        report_content = (
            REPO_ROOT / "docs" / "governance" / "DSOM-TOKEN-EFFICIENCY-REPORT.md"
        ).read_text(encoding="utf-8")
        expected_line = f"- **GitHub Pages:** [DSOM Protocol Documentation]({GITHUB_PAGES_URL})"
        self.assertIn(expected_line, efficiency_content)
        self.assertIn(expected_line, report_content)


class PublishToBloggerSkillGitHubPagesTests(unittest.TestCase):
    """Verify the publish-to-blogger skill emits GitHub Pages links."""

    @classmethod
    def setUpClass(cls):
        cls.content = BLOGGER_SKILL_PATH.read_text(encoding="utf-8")

    def test_skill_file_exists(self):
        self.assertTrue(BLOGGER_SKILL_PATH.is_file())

    def test_instructions_mention_github_pages_links(self):
        self.assertIn(
            "GitHub, GitLab, and GitHub Pages links just above the DSOM signature",
            self.content,
        )

    def test_instructions_no_longer_mention_gitbook_links(self):
        self.assertNotIn("GitHub, GitLab, and GitBook links", self.content)

    def test_html_snippet_contains_github_pages_list_item(self):
        self.assertIn(
            '<strong>GitHub Pages:</strong> <a href="'
            f'{GITHUB_PAGES_URL}" target="_blank">DSOM Protocol Documentation</a>',
            self.content,
        )

    def test_html_snippet_no_longer_contains_gitbook_list_item(self):
        self.assertNotRegex(self.content, r"<strong>GitBook:</strong>")

    def test_github_and_gitlab_list_items_unaffected(self):
        self.assertIn(
            '<strong>GitHub:</strong> <a href="https://github.com/linuxmalaysia/'
            'deep-state-of-mind-for-my-ai" target="_blank">'
            "linuxmalaysia/deep-state-of-mind-for-my-ai</a>",
            self.content,
        )
        self.assertIn(
            '<strong>GitLab:</strong> <a href="https://gitlab.com/linuxmalaysia/'
            'deep-state-of-mind-for-my-ai" target="_blank">'
            "linuxmalaysia/deep-state-of-mind-for-my-ai</a>",
            self.content,
        )

    def test_old_gitbook_url_absent(self):
        self.assertNotIn(OLD_GITBOOK_URL, self.content)


class AgentsOmniDocumentationSyncRuleTests(unittest.TestCase):
    """Verify .agents/AGENTS.md Rule 14 wording reflects GitHub Pages."""

    @classmethod
    def setUpClass(cls):
        cls.content = AGENTS_PATH.read_text(encoding="utf-8")

    def test_agents_md_exists(self):
        self.assertTrue(AGENTS_PATH.is_file())

    def test_rule_14_describes_summary_md_as_gitbook_or_github_pages(self):
        self.assertIn(
            "`SUMMARY.md` (for GitBook/GitHub Pages summary)", self.content
        )

    def test_rule_14_describes_mkdocs_yml_as_mkdocs_or_github_pages(self):
        self.assertIn("`mkdocs.yml` (for MkDocs/GitHub Pages)", self.content)

    def test_rule_14_still_lists_all_four_navigation_layers(self):
        for layer in ("SUMMARY.md", "mkdocs.yml", "START-HERE.md", "llms.txt"):
            with self.subTest(layer=layer):
                self.assertIn(layer, self.content)

    def test_rule_14_old_wording_removed(self):
        # The old wording described mkdocs.yml as solely "for MkDocs"
        # without the GitHub Pages qualifier.
        self.assertNotIn("`mkdocs.yml` (for MkDocs), ", self.content)


class RepoWideGitBookUrlRegressionTests(unittest.TestCase):
    """Broad regression guard: the retired GitBook URL must not resurface
    in any of the files this PR migrated to GitHub Pages."""

    def test_no_migrated_file_contains_old_gitbook_url(self):
        for path in ALL_MIGRATED_FILES:
            with self.subTest(path=path):
                content = path.read_text(encoding="utf-8")
                self.assertNotIn(
                    OLD_GITBOOK_URL,
                    content,
                    f"Stale GitBook URL reintroduced in {path}",
                )

    def test_every_migrated_file_exists(self):
        for path in ALL_MIGRATED_FILES:
            with self.subTest(path=path):
                self.assertTrue(path.is_file(), f"Expected {path} to exist")


if __name__ == "__main__":
    unittest.main()