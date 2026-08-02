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

import yaml  # type: ignore


def _find_repo_root(start: pathlib.Path) -> pathlib.Path:
    """
    Locate the repository root from a starting path.
    
    Parameters:
    	start (pathlib.Path): Path from which to search upward for the repository metadata directory.
    
    Returns:
    	pathlib.Path: The nearest ancestor containing a `.git` directory.
    
    Raises:
    	RuntimeError: If no ancestor contains a `.git` directory.
    """
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
        """
        Verify that the MkDocs configuration declares the expected GitHub Pages URL.
        """
        self.assertRegex(
            self.content,
            re.compile(rf"^site_url:\s*{re.escape(GITHUB_PAGES_URL)}\s*$", re.MULTILINE),
            "Expected mkdocs.yml to declare the GitHub Pages site_url",
        )


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
        """Load the llms.txt content for the test class."""
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


class OperationalSovereigntyFileSpecificTests(unittest.TestCase):
    """Precise wording/ordering checks for OPERATIONAL-SOVEREIGNTY.md."""

    PATH = REPO_ROOT / "docs" / "governance" / "OPERATIONAL-SOVEREIGNTY.md"

    @classmethod
    def setUpClass(cls):
        cls.content = cls.PATH.read_text(encoding="utf-8")

    def test_authoritative_references_line_present(self):
        self.assertIn(
            "* **Official Documentation (GitBook):** "
            f"[{GITBOOK_URL}]({GITBOOK_URL})",
            self.content,
        )

    def test_authoritative_references_ordering(self):
        # GitHub Pages entry must precede the GitBook entry, which in turn
        # must precede the Book of Busas entry, preserving the original
        # reference order plus the newly inserted GitBook line.
        github_pages_index = self.content.index(
            "* **Official Documentation (GitHub Pages):**"
        )
        gitbook_index = self.content.index(
            "* **Official Documentation (GitBook):**"
        )
        busas_index = self.content.index("* **Philosophical Foundations:**")
        self.assertLess(github_pages_index, gitbook_index)
        self.assertLess(gitbook_index, busas_index)

    def test_footer_signature_combines_both_urls_with_and(self):
        self.assertIn(
            f"*Official Documentation: <{GITHUB_PAGES_URL}> and <{GITBOOK_URL}>*",
            self.content,
        )

    def test_url_occurrence_counts_reflect_markdown_link_plus_footer(self):
        # Each URL appears twice in the markdown link `[URL](URL)` in the
        # Authoritative References section, plus once more in the footer
        # signature block, for three total occurrences each.
        self.assertEqual(self.content.count(GITHUB_PAGES_URL), 3)
        self.assertEqual(self.content.count(GITBOOK_URL), 3)


class AiMasterProtocolFileSpecificTests(unittest.TestCase):
    """Precise wording/ordering checks for AI-MASTER-PROTOCOL.md."""

    PATH = REPO_ROOT / "docs" / "governance" / "AI-MASTER-PROTOCOL.md"

    @classmethod
    def setUpClass(cls):
        cls.content = cls.PATH.read_text(encoding="utf-8")

    def test_numbered_reference_list_renumbered_correctly(self):
        self.assertIn(
            f"2. **Official Documentation (GitHub Pages):** [{GITHUB_PAGES_URL}]({GITHUB_PAGES_URL})",
            self.content,
        )
        self.assertIn(
            f"3. **Official Documentation (GitBook):** [{GITBOOK_URL}]({GITBOOK_URL})",
            self.content,
        )
        self.assertIn(
            "4. **The Book of Busas:** Refer to 'Buku Busas' for the "
            "philosophical foundations of Open Source sovereignty in Malaysia.",
            self.content,
        )

    def test_reference_ordering(self):
        github_pages_index = self.content.index(
            "2. **Official Documentation (GitHub Pages):**"
        )
        gitbook_index = self.content.index(
            "3. **Official Documentation (GitBook):**"
        )
        busas_index = self.content.index("4. **The Book of Busas:**")
        self.assertLess(github_pages_index, gitbook_index)
        self.assertLess(gitbook_index, busas_index)


class PersonalizationFileSpecificTests(unittest.TestCase):
    """Precise wording/ordering checks for docs/PERSONALIZATION.md Block 5."""

    PATH = REPO_ROOT / "docs" / "PERSONALIZATION.md"

    @classmethod
    def setUpClass(cls):
        cls.content = cls.PATH.read_text(encoding="utf-8")

    def test_numbered_block_5_items_renumbered_correctly(self):
        self.assertIn(
            "> 1. **Primary Repo:** "
            f"[{'https://github.com/linuxmalaysia/deep-state-of-mind-for-my-ai'}]"
            "(https://github.com/linuxmalaysia/deep-state-of-mind-for-my-ai)",
            self.content,
        )
        self.assertIn(
            f"> 2. **GitHub Pages:** [{GITHUB_PAGES_URL}]({GITHUB_PAGES_URL})",
            self.content,
        )
        self.assertIn(
            f"> 3. **GitBook:** [{GITBOOK_URL}]({GITBOOK_URL})",
            self.content,
        )
        self.assertIn(
            "> 4. **Buku Busas:** Philosophical foundations of Open Source sovereignty.",
            self.content,
        )

    def test_block_5_ordering(self):
        primary_repo_index = self.content.index("> 1. **Primary Repo:**")
        github_pages_index = self.content.index("> 2. **GitHub Pages:**")
        gitbook_index = self.content.index("> 3. **GitBook:**")
        busas_index = self.content.index("> 4. **Buku Busas:**")
        self.assertLess(primary_repo_index, github_pages_index)
        self.assertLess(github_pages_index, gitbook_index)
        self.assertLess(gitbook_index, busas_index)


class EfficiencyDocsFileSpecificTests(unittest.TestCase):
    """Precise wording/ordering checks shared by the efficiency docs."""

    PATHS = [
        REPO_ROOT / "docs" / "governance" / "DSOM-EFFICIENCY-PROTOCOLS.md",
        REPO_ROOT / "docs" / "governance" / "DSOM-TOKEN-EFFICIENCY-REPORT.md",
    ]

    def test_gitbook_line_matches_expected_format(self):
        expected_line = f"- **GitBook:** [DSOM GitBook Documentation]({GITBOOK_URL})"
        for path in self.PATHS:
            with self.subTest(path=path):
                content = path.read_text(encoding="utf-8")
                self.assertIn(expected_line, content)

    def test_github_pages_line_immediately_precedes_gitbook_line(self):
        github_pages_line = (
            f"- **GitHub Pages:** [DSOM Protocol Documentation]({GITHUB_PAGES_URL})"
        )
        gitbook_line = f"- **GitBook:** [DSOM GitBook Documentation]({GITBOOK_URL})"
        for path in self.PATHS:
            with self.subTest(path=path):
                content = path.read_text(encoding="utf-8")
                expected_block = f"{github_pages_line}\n{gitbook_line}"
                self.assertIn(expected_block, content)

    def test_github_and_gitlab_lines_unaffected(self):
        for path in self.PATHS:
            with self.subTest(path=path):
                content = path.read_text(encoding="utf-8")
                self.assertIn(
                    "- **GitHub:** [linuxmalaysia/deep-state-of-mind-for-my-ai]"
                    "(https://github.com/linuxmalaysia/deep-state-of-mind-for-my-ai)",
                    content,
                )
                self.assertIn(
                    "- **GitLab:** [linuxmalaysia/deep-state-of-mind-for-my-ai]"
                    "(https://gitlab.com/linuxmalaysia/deep-state-of-mind-for-my-ai)",
                    content,
                )


class PublishToBloggerSkillOrderingAndRegressionTests(unittest.TestCase):
    """Ordering and regression checks for the publish-to-blogger skill."""

    @classmethod
    def setUpClass(cls):
        cls.content = BLOGGER_SKILL_PATH.read_text(encoding="utf-8")

    def test_html_list_items_appear_in_expected_order(self):
        github_index = self.content.index("<strong>GitHub:</strong>")
        gitlab_index = self.content.index("<strong>GitLab:</strong>")
        github_pages_index = self.content.index("<strong>GitHub Pages:</strong>")
        gitbook_index = self.content.index("<strong>GitBook:</strong>")
        self.assertLess(github_index, gitlab_index)
        self.assertLess(gitlab_index, github_pages_index)
        self.assertLess(github_pages_index, gitbook_index)

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

    def test_instructions_no_longer_mention_stale_three_link_wording(self):
        # The prior wording ("GitHub, GitLab, and GitHub Pages links") must
        # have been fully replaced by the four-link wording, not merely
        # supplemented.
        self.assertNotIn(
            "GitHub, GitLab, and GitHub Pages links just above the DSOM signature",
            self.content,
        )

    def test_only_one_gitbook_list_item_present(self):
        self.assertEqual(
            self.content.count("<strong>GitBook:</strong>"), 1
        )


class LlmsTxtOrderingTests(unittest.TestCase):
    """Ordering and regression checks for llms.txt Core Entry Points."""

    @classmethod
    def setUpClass(cls):
        cls.content = LLMS_TXT_PATH.read_text(encoding="utf-8")

    def test_summary_md_still_referenced(self):
        # The underlying target file must not have been removed, only
        # relabelled/expanded.
        self.assertIn("(SUMMARY.md)", self.content)

    def test_github_pages_entry_precedes_gitbook_entry(self):
        github_pages_index = self.content.index(
            "[Official Live Documentation (GitHub Pages)]"
        )
        gitbook_index = self.content.index(
            "[Official Live Documentation (GitBook)]"
        )
        self.assertLess(github_pages_index, gitbook_index)

    def test_gitbook_summary_entry_precedes_both_live_doc_entries(self):
        summary_index = self.content.index(
            "[GitBook Summary / Documentation Index]"
        )
        github_pages_index = self.content.index(
            "[Official Live Documentation (GitHub Pages)]"
        )
        self.assertLess(summary_index, github_pages_index)

    def test_context7_entry_still_present_after_new_entries(self):
        # Regression guard: the pre-existing Context7 entry point must
        # remain intact and appear after the two newly inserted lines.
        gitbook_index = self.content.index(
            "[Official Live Documentation (GitBook)]"
        )
        context7_index = self.content.index("[Context7 Live RAG Payload")
        self.assertLess(gitbook_index, context7_index)


class ReadmeOrderingTests(unittest.TestCase):
    """Ordering and header-placement checks for README.md."""

    @classmethod
    def setUpClass(cls):
        cls.content = README_PATH.read_text(encoding="utf-8")

    def test_github_pages_badge_precedes_gitbook_badge(self):
        github_pages_badge_index = self.content.index("Docs-GitHub%20Pages")
        gitbook_badge_index = self.content.index("Docs-GitBook")
        self.assertLess(github_pages_badge_index, gitbook_badge_index)

    def test_github_pages_callout_precedes_gitbook_callout(self):
        github_pages_callout_index = self.content.index("- **GitHub Pages:**")
        gitbook_callout_index = self.content.index("- **GitBook:**")
        self.assertLess(github_pages_callout_index, gitbook_callout_index)

    def test_badges_and_callouts_appear_in_header_area(self):
        what_is_dsom_index = self.content.index("## 🎯 What is DSOM?")
        badge_index = self.content.index("Docs-GitBook")
        callout_index = self.content.index("**GitBook:**")
        self.assertLess(badge_index, what_is_dsom_index)
        self.assertLess(callout_index, what_is_dsom_index)

    def test_key_documents_table_github_pages_row_precedes_gitbook_row(self):
        github_pages_row_index = self.content.index(
            "[Official Live Documentation (GitHub Pages)]"
        )
        gitbook_row_index = self.content.index(
            "[Official Live Documentation (GitBook)]"
        )
        start_here_row_index = self.content.index(
            "[`START-HERE.md`](START-HERE.md)"
        )
        self.assertLess(github_pages_row_index, gitbook_row_index)
        self.assertLess(gitbook_row_index, start_here_row_index)


class RootAgentsOmniDocumentationSyncFullLineTests(unittest.TestCase):
    """Verify the full Omni-Documentation Sync table row text in AGENTS.md."""

    @classmethod
    def setUpClass(cls):
        cls.content = ROOT_AGENTS_PATH.read_text(encoding="utf-8")

    def test_root_agents_md_exists(self):
        self.assertTrue(ROOT_AGENTS_PATH.is_file())

    def test_full_table_row_matches_expected_text(self):
        expected_row = (
            "| **Omni-Documentation Sync** | New governance documents must be "
            "registered in `SUMMARY.md` (for GitBook navigation), `mkdocs.yml` "
            "(for MkDocs/GitHub Pages navigation), `START-HERE.md`, and "
            "`llms.txt`. |"
        )
        self.assertIn(expected_row, self.content)

    def test_other_table_rows_unaffected(self):
        # Regression guard: neighbouring rows in the same principles table
        # must remain intact.
        self.assertIn(
            "| **Zero-Global / Spatial Memory** | No global state. "
            "Operational memory lives in `.agents/brain/`. |",
            self.content,
        )
        self.assertIn(
            "| **Sovereign Signatures** | Every markdown or readable script "
            "modified by an AI must be processed via `dsom-signature-injector`. |",
            self.content,
        )


class UrlConstantSanityTests(unittest.TestCase):
    """Sanity checks on the URL constants used throughout these tests."""

    def test_github_pages_url_uses_https_and_has_trailing_slash(self):
        self.assertTrue(GITHUB_PAGES_URL.startswith("https://"))
        self.assertTrue(GITHUB_PAGES_URL.endswith("/"))

    def test_gitbook_url_uses_https_and_has_no_trailing_slash(self):
        self.assertTrue(GITBOOK_URL.startswith("https://"))
        self.assertFalse(GITBOOK_URL.endswith("/"))

    def test_urls_are_distinct(self):
        self.assertNotEqual(GITHUB_PAGES_URL, GITBOOK_URL)


if __name__ == "__main__":
    unittest.main()
