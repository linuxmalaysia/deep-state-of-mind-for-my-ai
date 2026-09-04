"""
Unit tests for .github/workflows/crda.yml

This PR added a "Set up Node.js 24" step and an "Install uv" step, and
switched the Python dependency installation from plain `pip install` to
`uv pip install --system`. These tests guard those specific changes without
re-testing unrelated, pre-existing parts of the workflow (e.g. the Snyk scan
and SARIF upload steps).

Following the convention established in tests/test_gh_pages_workflow.py,
two layers of testing are used:

1. Plain-text/regex based assertions that have no external dependencies
   and therefore always run.
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
WORKFLOW_PATH = REPO_ROOT / ".github" / "workflows" / "crda.yml"


class CrdaWorkflowFileTests(unittest.TestCase):
    """Basic existence / readability checks."""

    def test_workflow_file_exists(self):
        self.assertTrue(
            WORKFLOW_PATH.is_file(),
            f"Expected workflow file at {WORKFLOW_PATH}",
        )

    def test_workflow_file_not_empty(self):
        content = WORKFLOW_PATH.read_text(encoding="utf-8")
        self.assertTrue(content.strip(), "Workflow file should not be empty")


class CrdaWorkflowTextContentTests(unittest.TestCase):
    """Regex/substring based checks that don't require a YAML parser."""

    @classmethod
    def setUpClass(cls):
        cls.content = WORKFLOW_PATH.read_text(encoding="utf-8")

    def test_setup_node_step_present_with_expected_version(self):
        self.assertIn("name: Set up Node.js 24", self.content)
        self.assertIn("uses: actions/setup-node@820762786026740c76f36085b0efc47a31fe5020", self.content)
        self.assertRegex(self.content, r'node-version:\s*"24"')

    def test_install_uv_step_present_with_expected_inputs(self):
        self.assertIn("name: Install uv", self.content)
        self.assertIn("uses: astral-sh/setup-uv@ae62891fec2bb8e7d6c99fc78c9fec3a63790f8d", self.content)
        self.assertRegex(self.content, r"enable-cache:\s*true")
        self.assertRegex(
            self.content,
            r'cache-dependency-glob:\s*"requirements\.txt"',
        )

    def test_setup_python_step_still_present_with_expected_version(self):
        self.assertIn("uses: actions/setup-python@v7", self.content)
        self.assertRegex(self.content, r'python-version:\s*"3\.12"')
        self.assertRegex(self.content, r'cache:\s*"pip"')

    def test_installs_python_dependencies_via_uv(self):
        self.assertIn(
            "run: uv pip install --system -r requirements.txt", self.content
        )

    def test_no_longer_uses_plain_pip_install(self):
        # Regression guard: the plain `pip install -r requirements.txt`
        # invocation must have been fully replaced by uv, not merely
        # supplemented.
        self.assertNotIn("run: pip install -r requirements.txt", self.content)

    def test_snyk_scan_step_still_present(self):
        # Sanity check: the core purpose of this workflow (the Snyk scans)
        # must remain untouched by the tooling changes.
        self.assertIn("uses: snyk/actions/python@b2fe5f490a614741f238cb20d3fdbdcfa7d7675e", self.content)
        self.assertIn("uses: snyk/actions/node@b2fe5f490a614741f238cb20d3fdbdcfa7d7675e", self.content)

    def test_sarif_upload_step_still_present(self):
        self.assertIn("uses: github/codeql-action/upload-sarif@v4", self.content)
        self.assertIn("category: snyk-python-scan", self.content)
        self.assertIn("category: snyk-node-scan", self.content)

    def test_no_tab_characters(self):
        self.assertNotIn("\t", self.content, "Workflow file should not contain tab characters")


@unittest.skipUnless(HAS_YAML, "PyYAML is not installed in this environment")
class CrdaWorkflowStructureTests(unittest.TestCase):
    """Structural checks against the parsed YAML document."""

    @classmethod
    def setUpClass(cls):
        with WORKFLOW_PATH.open(encoding="utf-8") as fh:
            cls.doc = yaml.safe_load(fh)
        cls.steps = cls.doc["jobs"]["snyk-scan"]["steps"]
        cls.step_names = [s.get("name") for s in cls.steps]

    def test_snyk_scan_steps_detailed_mapping(self):
        steps_by_name = {s.get("name"): s for s in self.steps}

        py_step = steps_by_name["Run Snyk Python vulnerability scan"]
        self.assertEqual(py_step["uses"], "snyk/actions/python@b2fe5f490a614741f238cb20d3fdbdcfa7d7675e")
        self.assertEqual(py_step["with"]["args"], "--sarif-file-output=snyk-python.sarif --severity-threshold=low")

        py_upload = steps_by_name["Upload Python SARIF to GitHub Code Scanning"]
        self.assertEqual(py_upload["uses"], "github/codeql-action/upload-sarif@v4")
        self.assertEqual(py_upload["with"]["sarif_file"], "snyk-python.sarif")
        self.assertEqual(py_upload["with"]["category"], "snyk-python-scan")

        node_step = steps_by_name["Run Snyk Node.js vulnerability scan"]
        self.assertEqual(node_step["uses"], "snyk/actions/node@b2fe5f490a614741f238cb20d3fdbdcfa7d7675e")
        self.assertEqual(node_step["with"]["args"], "--sarif-file-output=snyk-node.sarif --severity-threshold=low")

        node_upload = steps_by_name["Upload Node.js SARIF to GitHub Code Scanning"]
        self.assertEqual(node_upload["uses"], "github/codeql-action/upload-sarif@v4")
        self.assertEqual(node_upload["with"]["sarif_file"], "snyk-node.sarif")
        self.assertEqual(node_upload["with"]["category"], "snyk-node-scan")
    """Structural checks against the parsed YAML document."""

    @classmethod
    def setUpClass(cls):
        with WORKFLOW_PATH.open(encoding="utf-8") as fh:
            cls.doc = yaml.safe_load(fh)
        cls.steps = cls.doc["jobs"]["snyk-scan"]["steps"]
        cls.step_names = [s.get("name") for s in cls.steps]

    def test_document_parses_to_a_mapping(self):
        self.assertIsInstance(self.doc, dict)

    def test_steps_present_and_ordered(self):
        self.assertEqual(
            self.step_names,
            [
                "Checkout repository",
                "Set up Node.js 24",
                "Install uv",
                "Set up Python 3.12",
                "Install Python dependencies",
                "Run Snyk Python vulnerability scan",
                "Upload Python SARIF to GitHub Code Scanning",
                "Run Snyk Node.js vulnerability scan",
                "Upload Node.js SARIF to GitHub Code Scanning",
            ],
        )

    def test_setup_node_step_inputs(self):
        step = self.steps[self.step_names.index("Set up Node.js 24")]
        self.assertEqual(step["uses"], "actions/setup-node@820762786026740c76f36085b0efc47a31fe5020")
        self.assertEqual(step["with"]["node-version"], "24")

    def test_install_uv_step_inputs(self):
        step = self.steps[self.step_names.index("Install uv")]
        self.assertEqual(step["uses"], "astral-sh/setup-uv@ae62891fec2bb8e7d6c99fc78c9fec3a63790f8d")
        self.assertTrue(step["with"]["enable-cache"])
        self.assertEqual(step["with"]["cache-dependency-glob"], "requirements.txt")

    def test_setup_python_step_inputs(self):
        step = self.steps[self.step_names.index("Set up Python 3.12")]
        self.assertEqual(step["uses"], "actions/setup-python@v7")
        self.assertEqual(step["with"]["python-version"], "3.12")
        self.assertEqual(step["with"]["cache"], "pip")

    def test_install_dependencies_step_uses_uv(self):
        step = self.steps[self.step_names.index("Install Python dependencies")]
        self.assertEqual(step["run"], "uv pip install --system -r requirements.txt")

    def test_node_and_uv_steps_precede_python_setup(self):
        self.assertLess(
            self.step_names.index("Set up Node.js 24"),
            self.step_names.index("Install uv"),
        )
        self.assertLess(
            self.step_names.index("Install uv"),
            self.step_names.index("Set up Python 3.12"),
        )
        self.assertLess(
            self.step_names.index("Set up Python 3.12"),
            self.step_names.index("Install Python dependencies"),
        )

    def test_no_duplicate_step_names(self):
        self.assertEqual(
            len(self.step_names),
            len(set(self.step_names)),
            "Step names should be unique",
        )


if __name__ == "__main__":
    unittest.main()