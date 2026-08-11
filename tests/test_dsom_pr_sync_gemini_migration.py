"""
Unit tests for `.github/workflows/dsom-pr-sync.yml`.

This PR migrates the "Run DSOM Semantic Compaction" step away from OpenAI
and towards the Gemini API (with a local fallback engine baked into
`action_update_dsom.py`):

1. The `OPENAI_API_KEY` secret/env var is removed and replaced with
   `GEMINI_API_KEY` and `GOOGLE_API_KEY`.
2. A new `ACTIVE_AGENT` env var (hard-coded to `"Jules"`) selects which AI
   persona system prompt the script should use.
3. The `uv run` invocation drops the `--with openai` dependency in favour
   of `--with requests --with pyyaml` (the script now talks to Gemini's
   REST API directly and parses/serialises YAML frontmatter itself).

Following the convention established in `tests/test_gh_pages_workflow.py`
and `tests/test_dsom_pr_sync_workflow.py`, two layers of testing are used:

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
WORKFLOW_PATH = REPO_ROOT / ".github" / "workflows" / "dsom-pr-sync.yml"


class DsomPrSyncGeminiMigrationTextTests(unittest.TestCase):
    """Regex/substring checks scoped to the "Run DSOM Semantic Compaction"
    step, which is the part of this workflow touched by this PR."""

    @classmethod
    def setUpClass(cls):
        cls.content = WORKFLOW_PATH.read_text(encoding="utf-8")
        match = re.search(
            r"- name:\s*Run DSOM Semantic Compaction\r?\n(?P<body>(?:[ \t]+\S.*\r?\n?)+)",
            cls.content,
        )
        assert match is not None, 'Could not locate the "Run DSOM Semantic Compaction" step block'
        cls.compaction_step = match.group(0)

    def test_workflow_file_exists(self):
        self.assertTrue(WORKFLOW_PATH.is_file())

    def test_compaction_step_present(self):
        self.assertIn("name: Run DSOM Semantic Compaction", self.content)

    def test_openai_api_key_no_longer_referenced(self):
        self.assertNotIn("OPENAI_API_KEY", self.content)

    def test_gemini_api_key_env_configured(self):
        self.assertRegex(
            self.compaction_step, r"GEMINI_API_KEY:\s*\$\{\{\s*secrets\.GEMINI_API_KEY\s*\}\}"
        )

    def test_google_api_key_env_configured(self):
        self.assertRegex(
            self.compaction_step, r"GOOGLE_API_KEY:\s*\$\{\{\s*secrets\.GOOGLE_API_KEY\s*\}\}"
        )

    def test_active_agent_env_hardcoded_to_jules(self):
        self.assertRegex(self.compaction_step, r'ACTIVE_AGENT:\s*"Jules"')

    def test_uv_run_no_longer_installs_openai(self):
        self.assertNotIn("--with openai", self.compaction_step)

    def test_uv_run_installs_requests_and_pyyaml(self):
        self.assertIn("--with requests", self.compaction_step)
        self.assertIn("--with pyyaml", self.compaction_step)

    def test_uv_run_invokes_the_correct_script_and_arguments(self):
        self.assertIn(
            "action_update_dsom.py pr.diff .agents/brain/current_state.dsom",
            self.compaction_step,
        )

    def test_no_tab_characters(self):
        self.assertNotIn("\t", self.content, "Workflow file should not contain tab characters")


@unittest.skipUnless(HAS_YAML, "PyYAML is not installed in this environment")
class DsomPrSyncGeminiMigrationStructureTests(unittest.TestCase):
    """Structural checks against the parsed YAML document, scoped to the
    "Run DSOM Semantic Compaction" step that this PR modified."""

    @classmethod
    def setUpClass(cls):
        with WORKFLOW_PATH.open(encoding="utf-8") as fh:
            cls.doc = yaml.safe_load(fh)
        steps = cls.doc["jobs"]["update-dsom-state"]["steps"]
        cls.compaction_step = next(
            s for s in steps if s.get("name") == "Run DSOM Semantic Compaction"
        )

    def test_document_parses_to_a_mapping(self):
        self.assertIsInstance(self.doc, dict)

    def test_env_block_contains_expected_keys_only(self):
        env = self.compaction_step["env"]
        self.assertEqual(
            env,
            {
                "GEMINI_API_KEY": "${{ secrets.GEMINI_API_KEY }}",
                "GOOGLE_API_KEY": "${{ secrets.GOOGLE_API_KEY }}",
                "ACTIVE_AGENT": "Jules",
            },
        )

    def test_run_command_uses_uv_with_requests_and_pyyaml(self):
        run_command = self.compaction_step["run"]
        self.assertIn("uv run --with requests --with pyyaml", run_command)
        self.assertNotIn("openai", run_command)

    def test_compaction_step_follows_set_up_python_step(self):
        steps = self.doc["jobs"]["update-dsom-state"]["steps"]
        step_names = [s.get("name") for s in steps]
        self.assertIn("Set up Python", step_names)
        self.assertIn("Run DSOM Semantic Compaction", step_names)
        self.assertLess(
            step_names.index("Set up Python"),
            step_names.index("Run DSOM Semantic Compaction"),
        )

    def test_commit_and_push_step_still_present_and_unaffected(self):
        # Regression guard: this PR should not have touched the final
        # commit/push step.
        steps = self.doc["jobs"]["update-dsom-state"]["steps"]
        commit_step = next(s for s in steps if s.get("name") == "Commit and push updated DSOM state")
        self.assertIn("git commit -m", commit_step["run"])
        self.assertIn("git push", commit_step["run"])


if __name__ == "__main__":
    unittest.main()