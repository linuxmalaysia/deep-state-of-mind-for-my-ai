"""
Unit tests for the GitHub Actions version bump introduced in this PR.

This PR performs routine maintenance updates to several workflow files:

1. `.github/workflows/crda.yml`: `actions/checkout` v4 -> v7 and
   `actions/setup-python` v5 -> v7.
2. `.github/workflows/dsom-pr-sync.yml`: `actions/checkout` v4 -> v7,
   `actions/setup-python` v5 -> v7, and the `uv run` invocation in the
   "Run DSOM Semantic Compaction" step drops the pinned
   `requests==2.34.2`/`pyyaml==6.0.3` versions in favour of unpinned
   `--with requests --with pyyaml`.
3. `.github/workflows/openwiki-update.yml`: `actions/checkout` v4 -> v7 and
   `peter-evans/create-pull-request` v7 -> v8.

`.github/workflows/gh-pages.yml`'s equivalent `actions/checkout` /
`actions/setup-python` bump is already covered by
`tests/test_gh_pages_workflow.py`.

Following the convention established in `tests/test_gh_pages_workflow.py`,
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
CRDA_PATH = REPO_ROOT / ".github" / "workflows" / "crda.yml"
DSOM_PR_SYNC_PATH = REPO_ROOT / ".github" / "workflows" / "dsom-pr-sync.yml"
OPENWIKI_UPDATE_PATH = REPO_ROOT / ".github" / "workflows" / "openwiki-update.yml"


# ------------------------------------------------------------------------
# crda.yml
# ------------------------------------------------------------------------
class CrdaWorkflowActionsVersionBumpTextTests(unittest.TestCase):
    """actions/checkout and actions/setup-python bumped to v7 in crda.yml."""

    @classmethod
    def setUpClass(cls):
        cls.content = CRDA_PATH.read_text(encoding="utf-8")

    def test_workflow_file_exists(self):
        self.assertTrue(CRDA_PATH.is_file(), f"Expected workflow file at {CRDA_PATH}")

    def test_checkout_step_pinned_to_v7(self):
        self.assertIn("uses: actions/checkout@v7", self.content)

    def test_setup_python_step_pinned_to_v7(self):
        self.assertIn("uses: actions/setup-python@v7", self.content)

    def test_does_not_use_old_checkout_v4_pin(self):
        self.assertNotIn("actions/checkout@v4", self.content)

    def test_does_not_use_old_setup_python_v5_pin(self):
        self.assertNotIn("actions/setup-python@v5", self.content)

    def test_setup_python_step_retains_expected_inputs(self):
        # Regression guard: the version bump should not have disturbed the
        # surrounding `with:` configuration for this step.
        self.assertRegex(self.content, r'python-version:\s*"3\.12"')
        self.assertRegex(self.content, r'cache:\s*"pip"')

    def test_no_tab_characters(self):
        self.assertNotIn("\t", self.content, "Workflow file should not contain tab characters")


@unittest.skipUnless(HAS_YAML, "PyYAML is not installed in this environment")
class CrdaWorkflowActionsVersionBumpStructureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with CRDA_PATH.open(encoding="utf-8") as fh:
            cls.doc = yaml.safe_load(fh)
        cls.steps = cls.doc["jobs"]["snyk-scan"]["steps"]

    def test_checkout_step_action_and_version(self):
        checkout_step = next(s for s in self.steps if s.get("name") == "Checkout repository")
        self.assertEqual(checkout_step["uses"], "actions/checkout@v7")

    def test_setup_python_step_action_and_version(self):
        setup_python_step = next(
            s for s in self.steps if s.get("name") == "Set up Python 3.12"
        )
        self.assertEqual(setup_python_step["uses"], "actions/setup-python@v7")
        self.assertEqual(setup_python_step["with"]["python-version"], "3.12")
        self.assertEqual(setup_python_step["with"]["cache"], "pip")


# ------------------------------------------------------------------------
# dsom-pr-sync.yml
# ------------------------------------------------------------------------
class DsomPrSyncActionsVersionBumpTextTests(unittest.TestCase):
    """actions/checkout, actions/setup-python bumped to v7, and the uv run
    dependency version pins dropped in dsom-pr-sync.yml."""

    @classmethod
    def setUpClass(cls):
        cls.content = DSOM_PR_SYNC_PATH.read_text(encoding="utf-8")
        match = re.search(
            r"- name:\s*Run DSOM Semantic Compaction\r?\n(?P<body>(?:[ \t]+\S.*\r?\n?)+)",
            cls.content,
        )
        assert match is not None, 'Could not locate the "Run DSOM Semantic Compaction" step block'
        cls.compaction_step = match.group(0)

    def test_workflow_file_exists(self):
        self.assertTrue(DSOM_PR_SYNC_PATH.is_file())

    def test_checkout_step_pinned_to_v7(self):
        self.assertIn("uses: actions/checkout@v7", self.content)

    def test_setup_python_step_pinned_to_v7(self):
        self.assertIn("uses: actions/setup-python@v7", self.content)

    def test_does_not_use_old_checkout_v4_pin(self):
        self.assertNotIn("actions/checkout@v4", self.content)

    def test_does_not_use_old_setup_python_v5_pin(self):
        self.assertNotIn("actions/setup-python@v5", self.content)

    def test_checkout_step_retains_fetch_depth(self):
        # Regression guard: the version bump should not disturb the
        # `fetch-depth: 2` input needed to diff the PR.
        self.assertRegex(
            self.content,
            r"actions/checkout@v7\s*\n\s*with:\s*\n\s*fetch-depth:\s*2",
        )

    def test_uv_run_dependencies_no_longer_version_pinned(self):
        self.assertIn("--with requests --with pyyaml", self.compaction_step)
        self.assertNotIn("requests==2.34.2", self.compaction_step)
        self.assertNotIn("pyyaml==6.0.3", self.compaction_step)

    def test_uv_run_invokes_the_correct_script_and_arguments(self):
        self.assertIn(
            "action_update_dsom.py pr.diff .agents/brain/current_state.dsom",
            self.compaction_step,
        )

    def test_no_tab_characters(self):
        self.assertNotIn("\t", self.content, "Workflow file should not contain tab characters")


@unittest.skipUnless(HAS_YAML, "PyYAML is not installed in this environment")
class DsomPrSyncActionsVersionBumpStructureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with DSOM_PR_SYNC_PATH.open(encoding="utf-8") as fh:
            cls.doc = yaml.safe_load(fh)
        cls.steps = cls.doc["jobs"]["update-dsom-state"]["steps"]

    def test_checkout_step_action_and_version(self):
        checkout_step = next(s for s in self.steps if s.get("name") == "Checkout repository")
        self.assertEqual(checkout_step["uses"], "actions/checkout@v7")
        self.assertEqual(checkout_step["with"]["fetch-depth"], 2)

    def test_setup_python_step_action_and_version(self):
        setup_python_step = next(s for s in self.steps if s.get("name") == "Set up Python")
        self.assertEqual(setup_python_step["uses"], "actions/setup-python@v7")

    def test_compaction_step_run_command_unpinned(self):
        compaction_step = next(
            s for s in self.steps if s.get("name") == "Run DSOM Semantic Compaction"
        )
        run_command = compaction_step["run"]
        self.assertIn("uv run --with requests --with pyyaml", run_command)
        self.assertNotIn("==", run_command)


# ------------------------------------------------------------------------
# openwiki-update.yml
# ------------------------------------------------------------------------
class OpenwikiUpdateActionsVersionBumpTextTests(unittest.TestCase):
    """actions/checkout bumped to v7 and peter-evans/create-pull-request
    bumped to v8 in openwiki-update.yml."""

    @classmethod
    def setUpClass(cls):
        cls.content = OPENWIKI_UPDATE_PATH.read_text(encoding="utf-8")

    def test_workflow_file_exists(self):
        self.assertTrue(OPENWIKI_UPDATE_PATH.is_file())

    def test_checkout_step_pinned_to_v7(self):
        self.assertIn("uses: actions/checkout@v7", self.content)

    def test_does_not_use_old_checkout_v4_pin(self):
        self.assertNotIn("actions/checkout@v4", self.content)

    def test_create_pull_request_step_pinned_to_v8(self):
        self.assertIn("uses: peter-evans/create-pull-request@v8", self.content)

    def test_does_not_use_old_create_pull_request_v7_pin(self):
        self.assertNotIn("peter-evans/create-pull-request@v7", self.content)

    def test_no_tab_characters(self):
        self.assertNotIn("\t", self.content, "Workflow file should not contain tab characters")


@unittest.skipUnless(HAS_YAML, "PyYAML is not installed in this environment")
class OpenwikiUpdateActionsVersionBumpStructureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with OPENWIKI_UPDATE_PATH.open(encoding="utf-8") as fh:
            cls.doc = yaml.safe_load(fh)
        cls.steps = cls.doc["jobs"]["update"]["steps"]

    def test_checkout_step_action_and_version(self):
        checkout_step = next(s for s in self.steps if s.get("name") == "Check out repository")
        self.assertEqual(checkout_step["uses"], "actions/checkout@v7")

    def test_create_pull_request_step_action_and_version(self):
        create_pr_step = next(
            s for s in self.steps if s.get("name") == "Create OpenWiki update pull request"
        )
        self.assertEqual(create_pr_step["uses"], "peter-evans/create-pull-request@v8")


if __name__ == "__main__":
    unittest.main()