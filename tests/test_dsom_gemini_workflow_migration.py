"""
Unit tests for the Gemini API migration made to
`.github/workflows/dsom-pr-sync.yml` by this PR.

This PR updates the "Run DSOM Semantic Compaction" step so that it:

1. No longer passes `OPENAI_API_KEY` and instead exposes `GEMINI_API_KEY`
   and `GOOGLE_API_KEY` (either of which may authenticate the Gemini API
   call performed by `.github/scripts/action_update_dsom.py`).
2. Adds a new `ACTIVE_AGENT: "Jules"` environment variable selecting the
   default Semantic Compaction persona.
3. Changes the `uv run` invocation from `--with openai --with requests` to
   `--with requests --with pyyaml`, since the script now depends on PyYAML
   (for OKF frontmatter parsing/serialisation) instead of the OpenAI SDK.

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


class RunDsomSemanticCompactionStepTextTests(unittest.TestCase):
    """Regex/substring checks scoped to the "Run DSOM Semantic Compaction"
    step, which is the only part of this workflow touched by this PR."""

    @classmethod
    def setUpClass(cls):
        cls.content = WORKFLOW_PATH.read_text(encoding="utf-8")
        match = re.search(
            r"- name:\s*Run DSOM Semantic Compaction\r?\n(?P<body>(?:[ \t]+\S.*\r?\n?)+)",
            cls.content,
        )
        assert match is not None, 'Could not locate the "Run DSOM Semantic Compaction" step block'
        cls.step_block = match.group(0)

    def test_step_present(self):
        self.assertIn("name: Run DSOM Semantic Compaction", self.content)

    def test_openai_api_key_env_var_removed(self):
        # Regression guard: the OpenAI secret must no longer be threaded
        # through to the script.
        self.assertNotIn("OPENAI_API_KEY", self.step_block)

    def test_gemini_api_key_env_var_present(self):
        self.assertRegex(
            self.step_block,
            r"GEMINI_API_KEY:\s*\$\{\{\s*secrets\.GEMINI_API_KEY\s*\}\}",
        )

    def test_google_api_key_env_var_present(self):
        self.assertRegex(
            self.step_block,
            r"GOOGLE_API_KEY:\s*\$\{\{\s*secrets\.GOOGLE_API_KEY\s*\}\}",
        )

    def test_active_agent_env_var_defaults_to_jules(self):
        self.assertRegex(self.step_block, r'ACTIVE_AGENT:\s*"Jules"')

    def test_uv_run_no_longer_installs_openai_package(self):
        self.assertNotIn("--with openai", self.step_block)

    def test_uv_run_installs_requests_and_pyyaml(self):
        self.assertIn("--with requests", self.step_block)
        self.assertIn("--with pyyaml", self.step_block)

    def test_uv_run_still_targets_action_update_dsom_script_with_same_args(self):
        self.assertRegex(
            self.step_block,
            r"uv run --with requests --with pyyaml \.github/scripts/action_update_dsom\.py pr\.diff \.agents/brain/current_state\.dsom",
        )

    def test_no_tab_characters(self):
        self.assertNotIn("\t", self.content, "Workflow file should not contain tab characters")


@unittest.skipUnless(HAS_YAML, "PyYAML is not installed in this environment")
class RunDsomSemanticCompactionStepStructureTests(unittest.TestCase):
    """Structural checks against the parsed YAML document, scoped to the
    "Run DSOM Semantic Compaction" step that this PR modified."""

    @classmethod
    def setUpClass(cls):
        with WORKFLOW_PATH.open(encoding="utf-8") as fh:
            cls.doc = yaml.safe_load(fh)
        steps = cls.doc["jobs"]["update-dsom-state"]["steps"]
        cls.step = next(
            s for s in steps if s.get("name") == "Run DSOM Semantic Compaction"
        )

    def test_document_parses_to_a_mapping(self):
        self.assertIsInstance(self.doc, dict)

    def test_env_block_contains_expected_keys_only(self):
        env = self.step["env"]
        self.assertEqual(
            set(env.keys()), {"GEMINI_API_KEY", "GOOGLE_API_KEY", "ACTIVE_AGENT"}
        )

    def test_env_values_reference_expected_secrets(self):
        env = self.step["env"]
        self.assertEqual(env["GEMINI_API_KEY"], "${{ secrets.GEMINI_API_KEY }}")
        self.assertEqual(env["GOOGLE_API_KEY"], "${{ secrets.GOOGLE_API_KEY }}")
        self.assertEqual(env["ACTIVE_AGENT"], "Jules")

    def test_run_command_matches_expected_uv_invocation(self):
        run_cmd = self.step["run"].strip()
        self.assertEqual(
            run_cmd,
            "uv run --with requests --with pyyaml .github/scripts/action_update_dsom.py pr.diff .agents/brain/current_state.dsom",
        )

    def test_run_dsom_semantic_compaction_step_precedes_commit_step(self):
        steps = self.doc["jobs"]["update-dsom-state"]["steps"]
        step_names = [s.get("name") for s in steps]
        self.assertIn("Run DSOM Semantic Compaction", step_names)
        self.assertIn("Commit and push updated DSOM state", step_names)
        self.assertLess(
            step_names.index("Run DSOM Semantic Compaction"),
            step_names.index("Commit and push updated DSOM state"),
        )


if __name__ == "__main__":
    unittest.main()