"""
Unit tests for .github/workflows/gh-pages.yml

This workflow was added to automatically build the MkDocs documentation
site and publish it to the `gh-pages` branch for GitHub Pages hosting.

Two layers of testing are used:

1. Plain-text/regex based assertions that have no external dependencies
   and therefore always run, regardless of which Python interpreter/
   environment executes the suite.
2. Structural assertions based on a parsed YAML document (via PyYAML),
   which are skipped gracefully if PyYAML is not installed.
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
WORKFLOW_PATH = REPO_ROOT / ".github" / "workflows" / "gh-pages.yml"


class GhPagesWorkflowFileTests(unittest.TestCase):
    """Basic existence / readability checks."""

    def test_workflow_file_exists(self):
        self.assertTrue(
            WORKFLOW_PATH.is_file(),
            f"Expected workflow file at {WORKFLOW_PATH}",
        )

    def test_workflow_file_not_empty(self):
        content = WORKFLOW_PATH.read_text(encoding="utf-8")
        self.assertTrue(content.strip(), "Workflow file should not be empty")


class GhPagesWorkflowTextContentTests(unittest.TestCase):
    """Regex/substring based checks that don't require a YAML parser."""

    @classmethod
    def setUpClass(cls):
        cls.content = WORKFLOW_PATH.read_text(encoding="utf-8")

    def test_workflow_name_declared(self):
        self.assertRegex(
            self.content,
            re.compile(r"^name:\s*Deploy MkDocs to GitHub Pages\s*$", re.MULTILINE),
            "Workflow should declare the expected top-level name",
        )

    def test_triggers_on_push_to_main(self):
        # 'on: push: branches: [main]' section must exist
        self.assertRegex(self.content, r"on:\s*\n\s+push:\s*\n\s+branches:\s*\n\s+-\s*main")

    def test_triggers_manual_dispatch(self):
        self.assertIn("workflow_dispatch:", self.content)

    def test_does_not_trigger_on_pull_request(self):
        # This deploy workflow should only run on push/manual dispatch,
        # never directly on pull_request events.
        self.assertNotRegex(self.content, r"\n\s*pull_request\s*:")

    def test_concurrency_group_uses_branch_ref(self):
        self.assertIn("group: github-pages-${{ github.ref }}", self.content)

    def test_concurrency_cancels_in_progress_runs(self):
        self.assertIn("cancel-in-progress: true", self.content)

    def test_permissions_grants_contents_write(self):
        self.assertRegex(self.content, r"permissions:\s*\n\s+contents:\s*write")

    def test_job_runs_on_ubuntu_latest(self):
        self.assertIn("runs-on: ubuntu-latest", self.content)

    def test_job_has_timeout(self):
        self.assertIn("timeout-minutes: 15", self.content)

    def test_checkout_step_present(self):
        self.assertIn("uses: actions/checkout@v7", self.content)

    def test_setup_python_step_present_with_expected_version(self):
        """Verify that the workflow configures the expected Python version and pip caching."""
        self.assertIn("uses: actions/setup-python@v7", self.content)
        self.assertRegex(self.content, r'python-version:\s*"3\.12"')
        self.assertRegex(self.content, r'cache:\s*"pip"')

    def test_installs_mkdocs_material(self):
        self.assertIn("pip install mkdocs-material", self.content)

    def test_builds_site_with_mkdocs(self):
        self.assertTrue("mkdocs build" in self.content or "generate_sitemaps.py" in self.content)

    def test_deploy_step_uses_peaceiris_action(self):
        self.assertIn("uses: peaceiris/actions-gh-pages@v4", self.content)

    def test_deploy_publishes_expected_directory_and_branch(self):
        self.assertRegex(self.content, r"publish_dir:\s*\./site")
        self.assertRegex(self.content, r"publish_branch:\s*gh-pages")

    def test_deploy_uses_github_token_secret(self):
        self.assertIn("github_token: ${{ secrets.GITHUB_TOKEN }}", self.content)

    def test_deploy_commit_message_skips_ci(self):
        # Prevents the automated deploy commit from re-triggering CI loops.
        self.assertRegex(self.content, r"commit_message:.*\[skip ci\]")

    def test_deploy_bot_identity_configured(self):
        self.assertIn("user_name: 'github-actions[bot]'", self.content)
        self.assertIn(
            "user_email: 'github-actions[bot]@users.noreply.github.com'",
            self.content,
        )

    def test_no_tab_characters(self):
        # YAML is whitespace-sensitive; tabs are a common source of subtle bugs.
        self.assertNotIn("\t", self.content, "Workflow file should not contain tab characters")


@unittest.skipUnless(HAS_YAML, "PyYAML is not installed in this environment")
class GhPagesWorkflowStructureTests(unittest.TestCase):
    """Structural checks against the parsed YAML document."""

    @classmethod
    def setUpClass(cls):
        with WORKFLOW_PATH.open(encoding="utf-8") as fh:
            cls.doc = yaml.safe_load(fh)

    def test_document_parses_to_a_mapping(self):
        self.assertIsInstance(self.doc, dict)

    def test_top_level_name(self):
        self.assertEqual(self.doc.get("name"), "Deploy MkDocs to GitHub Pages")

    def test_on_triggers_structure(self):
        # PyYAML parses the bare 'on:' key as the boolean True in YAML 1.1,
        # so check both possible keys to be resilient to parser behavior.
        triggers = self.doc.get("on", self.doc.get(True))
        self.assertIsNotNone(triggers, "Expected an 'on' trigger section")
        self.assertIn("push", triggers)
        self.assertEqual(triggers["push"].get("branches"), ["main"])
        self.assertIn("workflow_dispatch", triggers)

    def test_concurrency_settings(self):
        concurrency = self.doc["concurrency"]
        self.assertEqual(concurrency["group"], "github-pages-${{ github.ref }}")
        self.assertTrue(concurrency["cancel-in-progress"])

    def test_permissions_settings(self):
        self.assertEqual(self.doc["permissions"], {"contents": "write"})

    def test_single_job_definition(self):
        jobs = self.doc["jobs"]
        self.assertIn("deploy-pages", jobs)
        job = jobs["deploy-pages"]
        self.assertEqual(job["name"], "Build and Deploy MkDocs")
        self.assertEqual(job["runs-on"], "ubuntu-latest")
        self.assertEqual(job["timeout-minutes"], 15)

    def test_steps_present_and_ordered(self):
        steps = self.doc["jobs"]["deploy-pages"]["steps"]
        step_names = [s.get("name") for s in steps]
        self.assertEqual(len(step_names), 5)
        self.assertEqual(step_names[0], "Checkout Repository")
        self.assertEqual(step_names[1], "Set up Python")
        self.assertEqual(step_names[2], "Install Dependencies")
        self.assertTrue(step_names[3].startswith("Build MkDocs Site"))
        self.assertEqual(step_names[4], "Deploy to GitHub Pages")

    def test_checkout_step_action_pinned(self):
        steps = self.doc["jobs"]["deploy-pages"]["steps"]
        checkout_step = steps[0]
        self.assertEqual(checkout_step["uses"], "actions/checkout@v7")

    def test_setup_python_step_inputs(self):
        steps = self.doc["jobs"]["deploy-pages"]["steps"]
        setup_python_step = steps[1]
        self.assertEqual(setup_python_step["uses"], "actions/setup-python@v7")
        self.assertEqual(setup_python_step["with"]["python-version"], "3.12")
        self.assertEqual(setup_python_step["with"]["cache"], "pip")

    def test_install_dependencies_step_commands(self):
        steps = self.doc["jobs"]["deploy-pages"]["steps"]
        install_step = steps[2]
        run_lines = install_step["run"]
        self.assertIn("pip install --upgrade pip", run_lines)
        self.assertIn("pip install mkdocs-material", run_lines)

    def test_build_step_command(self):
        steps = self.doc["jobs"]["deploy-pages"]["steps"]
        build_step = steps[3]
        self.assertTrue("mkdocs build" in build_step["run"] or "generate_sitemaps.py" in build_step["run"])

    def test_deploy_step_configuration(self):
        steps = self.doc["jobs"]["deploy-pages"]["steps"]
        deploy_step = steps[4]
        self.assertEqual(deploy_step["uses"], "peaceiris/actions-gh-pages@v4")
        deploy_with = deploy_step["with"]
        self.assertEqual(deploy_with["github_token"], "${{ secrets.GITHUB_TOKEN }}")
        self.assertEqual(deploy_with["publish_dir"], "./site")
        self.assertEqual(deploy_with["publish_branch"], "gh-pages")
        self.assertEqual(deploy_with["user_name"], "github-actions[bot]")
        self.assertEqual(
            deploy_with["user_email"], "github-actions[bot]@users.noreply.github.com"
        )
        self.assertIn("[skip ci]", deploy_with["commit_message"])

    def test_no_duplicate_step_names(self):
        steps = self.doc["jobs"]["deploy-pages"]["steps"]
        names = [s.get("name") for s in steps]
        self.assertEqual(len(names), len(set(names)), "Step names should be unique")


if __name__ == "__main__":
    unittest.main()