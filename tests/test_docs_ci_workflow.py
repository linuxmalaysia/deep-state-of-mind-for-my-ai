"""
Unit tests for .github/workflows/docs-ci.yml

This workflow was added to continuously validate the new Diátaxis
documentation space (tutorials/, how-to/, reference/, explanation/) on every
push and pull request targeting `main`. It runs the relative link checker,
enforces OKF frontmatter compliance, and executes the link checker's own
unit test suite.

Two layers of testing are used, following the convention established by
tests/test_gh_pages_workflow.py:

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
WORKFLOW_PATH = REPO_ROOT / ".github" / "workflows" / "docs-ci.yml"


class DocsCiWorkflowFileTests(unittest.TestCase):
    """Basic existence / readability checks."""

    def test_workflow_file_exists(self):
        self.assertTrue(
            WORKFLOW_PATH.is_file(),
            f"Expected workflow file at {WORKFLOW_PATH}",
        )

    def test_workflow_file_not_empty(self):
        content = WORKFLOW_PATH.read_text(encoding="utf-8")
        self.assertTrue(content.strip(), "Workflow file should not be empty")

    def test_no_tab_characters(self):
        content = WORKFLOW_PATH.read_text(encoding="utf-8")
        self.assertNotIn("\t", content, "Workflow file should not contain tab characters")


class DocsCiWorkflowTextContentTests(unittest.TestCase):
    """Regex/substring based checks that don't require a YAML parser."""

    @classmethod
    def setUpClass(cls):
        cls.content = WORKFLOW_PATH.read_text(encoding="utf-8")

    def test_workflow_name_declared(self):
        self.assertRegex(
            self.content,
            re.compile(r"^name:\s*Documentation CI\s*$", re.MULTILINE),
            "Workflow should declare the expected top-level name",
        )

    def test_triggers_on_push_to_main(self):
        self.assertRegex(self.content, r"on:\s*\n\s+push:\s*\n\s+branches:\s*\n\s+-\s*main")

    def test_triggers_on_pull_request_to_main(self):
        self.assertRegex(
            self.content, r"pull_request:\s*\n\s+branches:\s*\n\s+-\s*main"
        )

    def test_triggers_manual_dispatch(self):
        self.assertIn("workflow_dispatch:", self.content)

    def test_concurrency_group_uses_branch_ref(self):
        self.assertIn("group: docs-ci-${{ github.ref }}", self.content)

    def test_concurrency_cancels_in_progress_runs(self):
        self.assertIn("cancel-in-progress: true", self.content)

    def test_permissions_grants_read_only_contents(self):
        self.assertRegex(self.content, r"permissions:\s*\n\s+contents:\s*read")

    def test_job_runs_on_ubuntu_latest(self):
        self.assertIn("runs-on: ubuntu-latest", self.content)

    def test_job_has_timeout(self):
        self.assertIn("timeout-minutes: 10", self.content)

    def test_checkout_step_present_and_pinned(self):
        self.assertIn("name: Checkout Repository", self.content)
        self.assertIn(
            "uses: actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd", self.content
        )
        self.assertIn("persist-credentials: false", self.content)

    def test_setup_node_step_present_with_expected_version(self):
        self.assertIn("name: Set up Node.js 24", self.content)
        self.assertIn(
            "uses: actions/setup-node@820762786026740c76f36085b0efc47a31fe5020", self.content
        )
        self.assertRegex(self.content, r'node-version:\s*"24"')

    def test_install_uv_step_present_with_expected_inputs(self):
        self.assertIn("name: Install uv", self.content)
        self.assertIn(
            "uses: astral-sh/setup-uv@ae62891fec2bb8e7d6c99fc78c9fec3a63790f8d", self.content
        )
        self.assertRegex(self.content, r"enable-cache:\s*true")
        self.assertRegex(self.content, r'cache-dependency-glob:\s*"requirements\.txt"')

    def test_setup_python_step_present_with_expected_version(self):
        self.assertIn(
            "uses: actions/setup-python@5fda3b95a4ea91299a34e894583c3862153e4b97", self.content
        )
        self.assertRegex(self.content, r'python-version:\s*"3\.12"')
        self.assertRegex(self.content, r'cache:\s*"pip"')

    def test_gitleaks_step_present(self):
        self.assertIn("name: Run Gitleaks Secret Scanner", self.content)
        self.assertIn("uses: gitleaks/gitleaks-action@v2", self.content)

    def test_install_dependencies_step_installs_expected_packages(self):
        self.assertIn("name: Install Dependencies", self.content)
        self.assertIn("uv pip install --system pyyaml pytest ansible-core ansible-lint", self.content)

    def test_ansible_lint_step_present(self):
        self.assertIn("name: Run Ansible Lint Static Analysis", self.content)
        self.assertIn("ansible-lint playbooks/ roles/", self.content)

    def test_relative_links_validation_step_present(self):
        self.assertIn("name: Run Relative Links Validation", self.content)
        self.assertIn("python tools/check_docs_links.py", self.content)

    def test_okf_frontmatter_compliance_step_covers_all_quadrants(self):
        self.assertIn("name: Run OKF Frontmatter Compliance Check", self.content)
        for quadrant in ("reference", "how-to", "tutorials", "explanation"):
            with self.subTest(quadrant=quadrant):
                self.assertIn(
                    f"python tools/apply_okf_frontmatter.py docs/{quadrant}/", self.content
                )

    def test_okf_frontmatter_step_fails_build_on_uncommitted_diff(self):
        # The compliance step must assert there is no drift left behind by
        # apply_okf_frontmatter.py, otherwise silently-fixed files would
        # never fail CI.
        self.assertIn("git diff --exit-code -- docs", self.content)

    def test_unit_tests_for_link_checker_step_present(self):
        self.assertIn("name: Run Unit Tests for Link Checker", self.content)
        self.assertIn("pytest tests/test_docs_links.py", self.content)

    def test_step_order_link_validation_precedes_frontmatter_and_tests(self):
        link_idx = self.content.index("Run Relative Links Validation")
        frontmatter_idx = self.content.index("Run OKF Frontmatter Compliance Check")
        tests_idx = self.content.index("Run Unit Tests for Link Checker")
        self.assertLess(link_idx, frontmatter_idx)
        self.assertLess(frontmatter_idx, tests_idx)


@unittest.skipUnless(HAS_YAML, "PyYAML is not installed in this environment")
class DocsCiWorkflowStructureTests(unittest.TestCase):
    """Structural checks against the parsed YAML document."""

    @classmethod
    def setUpClass(cls):
        with WORKFLOW_PATH.open(encoding="utf-8") as fh:
            cls.doc = yaml.safe_load(fh)

    def test_document_parses_to_a_mapping(self):
        self.assertIsInstance(self.doc, dict)

    def test_top_level_name(self):
        self.assertEqual(self.doc.get("name"), "Documentation CI")

    def test_on_triggers_structure(self):
        # PyYAML parses the bare 'on:' key as the boolean True in YAML 1.1,
        # so check both possible keys to be resilient to parser behavior.
        triggers = self.doc.get("on", self.doc.get(True))
        self.assertIsNotNone(triggers, "Expected an 'on' trigger section")
        self.assertEqual(triggers["push"].get("branches"), ["main"])
        self.assertEqual(triggers["pull_request"].get("branches"), ["main"])
        self.assertIn("workflow_dispatch", triggers)

    def test_concurrency_settings(self):
        concurrency = self.doc["concurrency"]
        self.assertEqual(concurrency["group"], "docs-ci-${{ github.ref }}")
        self.assertTrue(concurrency["cancel-in-progress"])

    def test_permissions_settings(self):
        self.assertEqual(self.doc["permissions"], {"contents": "read"})

    def test_single_job_definition(self):
        jobs = self.doc["jobs"]
        self.assertIn("validate-docs", jobs)
        job = jobs["validate-docs"]
        self.assertEqual(job["name"], "Validate Diátaxis Documentation")
        self.assertEqual(job["runs-on"], "ubuntu-latest")
        self.assertEqual(job["timeout-minutes"], 10)

    def test_steps_present_and_ordered(self):
        steps = self.doc["jobs"]["validate-docs"]["steps"]
        step_names = [s.get("name") for s in steps]
        self.assertEqual(
            step_names,
            [
                "Checkout Repository",
                "Run Gitleaks Secret Scanner",
                "Set up Node.js 24",
                "Install uv",
                "Set up Python",
                "Install Dependencies",
                "Run Ansible Lint Static Analysis",
                "Run Relative Links Validation",
                "Run OKF Frontmatter Compliance Check",
                "Run Unit Tests for Link Checker",
            ],
        )

    def test_checkout_step_configuration(self):
        steps = self.doc["jobs"]["validate-docs"]["steps"]
        checkout_step = steps[0]
        self.assertEqual(
            checkout_step["uses"], "actions/checkout@de0fac2e4500dabe0009e67214ff5f5447ce83dd"
        )
        self.assertFalse(checkout_step["with"]["persist-credentials"])

    def test_gitleaks_step_configuration(self):
        steps = self.doc["jobs"]["validate-docs"]["steps"]
        gitleaks_step = steps[1]
        self.assertEqual(gitleaks_step["uses"], "gitleaks/gitleaks-action@v2")

    def test_install_dependencies_step_command(self):
        steps = self.doc["jobs"]["validate-docs"]["steps"]
        install_step = steps[5]
        self.assertIn("uv pip install --system pyyaml pytest ansible-core ansible-lint", install_step["run"])

    def test_ansible_lint_step_command(self):
        steps = self.doc["jobs"]["validate-docs"]["steps"]
        ansible_lint_step = steps[6]
        self.assertIn("ansible-lint playbooks/ roles/", ansible_lint_step["run"])

    def test_relative_links_step_command(self):
        steps = self.doc["jobs"]["validate-docs"]["steps"]
        link_step = steps[7]
        self.assertIn("python tools/check_docs_links.py", link_step["run"])

    def test_frontmatter_compliance_step_command_covers_all_quadrants_and_diff_guard(self):
        steps = self.doc["jobs"]["validate-docs"]["steps"]
        frontmatter_step = steps[8]
        run_lines = frontmatter_step["run"]
        for quadrant in ("reference", "how-to", "tutorials", "explanation"):
            with self.subTest(quadrant=quadrant):
                self.assertIn(f"python tools/apply_okf_frontmatter.py docs/{quadrant}/", run_lines)
        self.assertIn("git diff --exit-code -- docs", run_lines)

    def test_unit_tests_step_command(self):
        steps = self.doc["jobs"]["validate-docs"]["steps"]
        tests_step = steps[9]
        self.assertIn("pytest tests/test_docs_links.py", tests_step["run"])


if __name__ == "__main__":
    unittest.main()