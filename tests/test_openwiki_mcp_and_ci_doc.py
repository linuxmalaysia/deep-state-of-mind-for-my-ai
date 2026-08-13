"""
Regression tests for `openwiki/integrations/mcp-and-ci.md`.

This PR appended a new "Troubleshooting CI Permissions" section to the
existing "FastMCP Server Integration & Continuous Integration Workflows"
page, documenting how to resolve the

    GitHub Actions is not permitted to create or approve pull requests.

error that the `openwiki-update.yml` workflow can hit when a repository's
"Workflow permissions" setting doesn't allow GitHub Actions to open pull
requests.

These tests pin down that new section (heading, error message, and the
step-by-step remediation instructions) without re-testing unrelated,
pre-existing parts of the document. Structural (frontmatter) assertions
are skipped gracefully if PyYAML is not installed, following the
convention used elsewhere in this test suite.
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
DOC_PATH = REPO_ROOT / "openwiki" / "integrations" / "mcp-and-ci.md"
FRONTMATTER_RE = re.compile(r"\A---\s*\r?\n(.*?)(?:\r?\n)?---\s*(?:\r?\n|\Z)", re.DOTALL)


class McpAndCiDocFileTests(unittest.TestCase):
    """Basic existence / readability checks."""

    def test_doc_file_exists(self):
        self.assertTrue(DOC_PATH.is_file(), f"Expected doc file at {DOC_PATH}")

    def test_doc_file_not_empty(self):
        content = DOC_PATH.read_text(encoding="utf-8")
        self.assertTrue(content.strip(), "Doc file should not be empty")

    def test_starts_with_frontmatter_fence(self):
        content = DOC_PATH.read_text(encoding="utf-8")
        self.assertTrue(content.startswith("---\n"))


class ExistingSectionsPreservedTests(unittest.TestCase):
    """Sanity checks that pre-existing content survived the new addition."""

    @classmethod
    def setUpClass(cls):
        cls.content = DOC_PATH.read_text(encoding="utf-8")

    def test_fastmcp_server_architecture_heading_present(self):
        self.assertIn("## 🔌 FastMCP Server Architecture", self.content)

    def test_ci_workflow_catalogue_heading_present(self):
        self.assertIn(
            "## 🤖 Continuous Integration Workflow Catalogue", self.content
        )

    def test_existing_workflow_bullets_still_present(self):
        self.assertIn("**`gh-pages.yml`:**", self.content)
        self.assertIn("**`openwiki-update.yml`:**", self.content)
        self.assertIn("**`snyk-scanning.yml`:**", self.content)


class TroubleshootingSectionTests(unittest.TestCase):
    """Regression tests for the new "Troubleshooting CI Permissions" section
    added by this PR."""

    @classmethod
    def setUpClass(cls):
        cls.content = DOC_PATH.read_text(encoding="utf-8")
        match = FRONTMATTER_RE.match(cls.content)
        assert match is not None
        cls.body = cls.content[match.end():]

    def test_troubleshooting_heading_present(self):
        self.assertIn("## 🛠️ Troubleshooting CI Permissions", self.body)

    def test_pull_request_creation_failures_subheading_present(self):
        self.assertIn("### Pull Request Creation Failures", self.body)

    def test_references_openwiki_update_workflow(self):
        self.assertIn("**`openwiki-update.yml`**", self.body)

    def test_error_message_quoted_verbatim(self):
        self.assertIn(
            "GitHub Actions is not permitted to create or approve pull requests.",
            self.body,
        )

    def test_error_message_docs_link_present(self):
        self.assertIn(
            "https://docs.github.com/rest/pulls/pulls#create-a-pull-request",
            self.body,
        )

    def test_error_message_is_fenced_as_code_block(self):
        fence_count = self.body.count("```")
        self.assertGreaterEqual(fence_count, 2)
        self.assertEqual(fence_count % 2, 0, "Code fences should be balanced")
        self.assertRegex(
            self.body,
            re.compile(
                r"```\nGitHub Actions is not permitted to create or approve pull requests\..*?```",
                re.DOTALL,
            ),
        )

    def test_remediation_steps_present_in_order(self):
        expected_snippets = [
            "Navigate to your repository's main page on GitHub.",
            "Click on **Settings**",
            "**Actions** -> **General**",
            "**Workflow permissions**",
            'Check the box for **"Allow GitHub Actions to create and approve pull requests"**.',
            "Click **Save**.",
            "Re-run the failed workflow.",
        ]
        last_index = -1
        for snippet in expected_snippets:
            with self.subTest(snippet=snippet):
                index = self.body.find(snippet)
                self.assertNotEqual(index, -1, f"Expected to find {snippet!r} in the doc body")
                self.assertGreater(
                    index, last_index, f"Expected {snippet!r} to appear after the previous step"
                )
                last_index = index

    def test_remediation_steps_are_a_numbered_list(self):
        self.assertRegex(self.body, r"1\. Navigate to your repository's main page on GitHub\.")
        self.assertRegex(self.body, r"7\. Re-run the failed workflow\.")

    def test_troubleshooting_section_appears_after_ci_workflow_catalogue(self):
        catalogue_index = self.body.index(
            "## 🤖 Continuous Integration Workflow Catalogue"
        )
        troubleshooting_index = self.body.index(
            "## 🛠️ Troubleshooting CI Permissions"
        )
        self.assertLess(catalogue_index, troubleshooting_index)

    def test_troubleshooting_section_is_the_last_top_level_heading(self):
        top_level_headings = re.findall(r"^## .+$", self.body, re.MULTILINE)
        self.assertTrue(top_level_headings, "Expected at least one '##' heading in the document body")
        self.assertEqual(top_level_headings[-1], "## 🛠️ Troubleshooting CI Permissions")


@unittest.skipUnless(HAS_YAML, "PyYAML is not installed in this environment")
class FrontmatterStructureTests(unittest.TestCase):
    """Structural checks confirming the frontmatter was not disturbed by the
    body-only addition made in this PR."""

    @classmethod
    def setUpClass(cls):
        cls.content = DOC_PATH.read_text(encoding="utf-8")
        match = FRONTMATTER_RE.match(cls.content)
        assert match is not None
        cls.frontmatter = yaml.safe_load(match.group(1))

    def test_mandatory_okf_fields_present(self):
        self.assertEqual(self.frontmatter["type"], "documentation")
        self.assertIn("openwiki", self.frontmatter["topics"])
        self.assertIn("ci-cd", self.frontmatter["topics"])

    def test_title_unchanged(self):
        self.assertEqual(
            self.frontmatter["title"],
            "FastMCP Server Integration & Continuous Integration Workflows",
        )


if __name__ == "__main__":
    unittest.main()