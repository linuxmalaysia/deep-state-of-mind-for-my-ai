"""
Unit tests for .github/workflows/openwiki-update.yml

This PR bumped the `astral-sh/setup-uv` action from v3 to v5 and added an
explicit `cache-dependency-glob` input so that uv's cache key is scoped to
`requirements.txt`. A subsequent change added a "Set up Node.js 24" step
right after checkout, and a "Set up Python" step (pinned to 3.12) between
"Install uv" and "Run Native OpenWiki Emulator". These tests guard those
specific changes (and the surrounding "Install uv" step configuration)
without re-testing unrelated, pre-existing parts of the workflow.

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
WORKFLOW_PATH = REPO_ROOT / ".github" / "workflows" / "openwiki-update.yml"


class OpenwikiUpdateWorkflowFileTests(unittest.TestCase):
    """Basic existence / readability checks."""

    def test_workflow_file_exists(self):
        self.assertTrue(
            WORKFLOW_PATH.is_file(),
            f"Expected workflow file at {WORKFLOW_PATH}",
        )

    def test_workflow_file_not_empty(self):
        content = WORKFLOW_PATH.read_text(encoding="utf-8")
        self.assertTrue(content.strip(), "Workflow file should not be empty")


class OpenwikiUpdateSetupUvStepTextTests(unittest.TestCase):
    """Regex/substring checks scoped to the "Install uv" step, which is the
    only part of this workflow touched by this PR."""

    @classmethod
    def setUpClass(cls):
        cls.content = WORKFLOW_PATH.read_text(encoding="utf-8")
        match = re.search(
            r"- name:\s*Install uv\r?\n(?P<body>(?:[ \t]+\S.*\r?\n?)+)",
            cls.content,
        )
        assert match is not None, 'Could not locate the "Install uv" step block'
        cls.install_uv_step = match.group(0)

    def test_install_uv_step_present(self):
        self.assertIn("name: Install uv", self.content)

    def test_uses_setup_uv_action_pinned_to_v5(self):
        self.assertIn("uses: astral-sh/setup-uv@v10.0.0", self.install_uv_step)

    def test_does_not_use_old_v3_pin(self):
        # Regression guard: ensure the upgrade from v3 to v5 wasn't reverted
        # or accidentally duplicated elsewhere in the step.
        self.assertNotIn("astral-sh/setup-uv@v3", self.install_uv_step)

    def test_enable_cache_still_true(self):
        self.assertRegex(self.install_uv_step, r"enable-cache:\s*true")

    def test_cache_dependency_glob_added_and_scoped_to_requirements_txt(self):
        self.assertRegex(
            self.install_uv_step,
            r'cache-dependency-glob:\s*"requirements\.txt"',
        )

    def test_cache_dependency_glob_appears_within_install_uv_with_block(self):
        # Make sure the new input lives under the "Install uv" step's `with:`
        # mapping, immediately alongside enable-cache, not in some unrelated
        # step of the workflow.
        self.assertRegex(
            self.install_uv_step,
            r"with:\s*\n\s+enable-cache:\s*true\s*\n\s+cache-dependency-glob:\s*\"requirements\.txt\"",
        )

    def test_no_tab_characters(self):
        self.assertNotIn("\t", self.content, "Workflow file should not contain tab characters")


class OpenwikiUpdateSetupNodeAndPythonStepTextTests(unittest.TestCase):
    """Regex/substring checks scoped to the new "Set up Node.js 24" and
    "Set up Python" steps added by this PR."""

    @classmethod
    def setUpClass(cls):
        cls.content = WORKFLOW_PATH.read_text(encoding="utf-8")
        node_match = re.search(
            r"- name:\s*Set up Node\.js 24\r?\n(?P<body>(?:[ \t]+\S.*\r?\n?)+)",
            cls.content,
        )
        assert node_match is not None, 'Could not locate the "Set up Node.js 24" step block'
        cls.setup_node_step = node_match.group(0)

        python_match = re.search(
            r"- name:\s*Set up Python\r?\n(?P<body>(?:[ \t]+\S.*\r?\n?)+)",
            cls.content,
        )
        assert python_match is not None, 'Could not locate the "Set up Python" step block'
        cls.setup_python_step = python_match.group(0)

    def test_setup_node_step_present(self):
        self.assertIn("name: Set up Node.js 24", self.content)

    def test_uses_setup_node_action(self):
        self.assertIn("uses: actions/setup-node@v7", self.setup_node_step)

    def test_node_version_pinned_to_24(self):
        self.assertRegex(self.setup_node_step, r'node-version:\s*"24"')

    def test_setup_node_step_precedes_install_uv_step(self):
        self.assertLess(
            self.content.index("name: Set up Node.js 24"),
            self.content.index("name: Install uv"),
        )

    def test_setup_python_step_present(self):
        self.assertIn("name: Set up Python", self.content)

    def test_uses_setup_python_action(self):
        self.assertIn("uses: actions/setup-python@v7", self.setup_python_step)

    def test_python_version_pinned_to_3_12(self):
        self.assertRegex(self.setup_python_step, r'python-version:\s*"3\.12"')

    def test_setup_python_step_between_install_uv_and_emulator_step(self):
        install_uv_index = self.content.index("name: Install uv")
        setup_python_index = self.content.index("name: Set up Python")
        emulator_index = self.content.index("name: Run Native OpenWiki Emulator")
        self.assertLess(install_uv_index, setup_python_index)
        self.assertLess(setup_python_index, emulator_index)


@unittest.skipUnless(HAS_YAML, "PyYAML is not installed in this environment")
class OpenwikiUpdateSetupNodeAndPythonStepStructureTests(unittest.TestCase):
    """Structural checks against the parsed YAML document, scoped to the
    "Set up Node.js 24" and "Set up Python" steps added by this PR."""

    @classmethod
    def setUpClass(cls):
        with WORKFLOW_PATH.open(encoding="utf-8") as fh:
            cls.doc = yaml.safe_load(fh)
        cls.steps = cls.doc["jobs"]["update"]["steps"]
        cls.step_names = [s.get("name") for s in cls.steps]

    def test_setup_node_step_action_and_inputs(self):
        step = self.steps[self.step_names.index("Set up Node.js 24")]
        self.assertEqual(step["uses"], "actions/setup-node@v7")
        self.assertEqual(step["with"]["node-version"], "24")

    def test_setup_python_step_action_and_inputs(self):
        step = self.steps[self.step_names.index("Set up Python")]
        self.assertEqual(step["uses"], "actions/setup-python@v7")
        self.assertEqual(step["with"]["python-version"], "3.12")

    def test_setup_node_step_is_second_step(self):
        self.assertEqual(self.step_names[0], "Check out repository")
        self.assertEqual(self.step_names[1], "Set up Node.js 24")

    def test_setup_python_step_precedes_emulator_step(self):
        self.assertLess(
            self.step_names.index("Set up Python"),
            self.step_names.index("Run Native OpenWiki Emulator"),
        )

    def test_no_duplicate_step_names(self):
        self.assertEqual(
            len(self.step_names),
            len(set(self.step_names)),
            "Step names should be unique",
        )


@unittest.skipUnless(HAS_YAML, "PyYAML is not installed in this environment")
class OpenwikiUpdateSetupUvStepStructureTests(unittest.TestCase):
    """Structural checks against the parsed YAML document, scoped to the
    "Install uv" step that this PR modified."""

    @classmethod
    def setUpClass(cls):
        with WORKFLOW_PATH.open(encoding="utf-8") as fh:
            cls.doc = yaml.safe_load(fh)
        steps = cls.doc["jobs"]["update"]["steps"]
        cls.install_uv_step = next(
            s for s in steps if s.get("name") == "Install uv"
        )

    def test_document_parses_to_a_mapping(self):
        self.assertIsInstance(self.doc, dict)

    def test_install_uv_step_action_and_version(self):
        self.assertEqual(self.install_uv_step["uses"], "astral-sh/setup-uv@v10.0.0")

    def test_install_uv_step_with_inputs(self):
        with_block = self.install_uv_step["with"]
        self.assertTrue(with_block["enable-cache"])
        self.assertEqual(with_block["cache-dependency-glob"], "requirements.txt")

    def test_install_uv_step_precedes_emulator_step(self):
        steps = self.doc["jobs"]["update"]["steps"]
        step_names = [s.get("name") for s in steps]
        self.assertIn("Install uv", step_names)
        self.assertIn("Run Native OpenWiki Emulator", step_names)
        self.assertLess(
            step_names.index("Install uv"),
            step_names.index("Run Native OpenWiki Emulator"),
        )


if __name__ == "__main__":
    unittest.main()