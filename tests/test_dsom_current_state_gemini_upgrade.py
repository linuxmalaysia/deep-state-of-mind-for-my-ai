"""
Unit tests for `.agents/brain/current_state.dsom`.

This PR updates the DSOM current-state file to reflect the Semantic
Compaction pipeline's migration to Gemini (Jules/Antigravity personas)
with a local Python fallback engine:

1. The YAML frontmatter `timestamp` is now an explicitly double-quoted
   string (`"2026-08-11T13:40:00Z"`) rather than a bare/unquoted scalar.
2. The `topics` list is now rendered as an inline, double-quoted JSON-style
   array (`["state", "memory", "compaction"]`) rather than a bare list.
3. A new bullet describing the Jules/Antigravity + local-fallback upgrade
   was added under `## Active State`.
4. A new bullet describing the `action_update_dsom.py` refactor was added
   under `## Condensed History`.

These tests validate the frontmatter's structure/quoting style and the
presence of the new narrative bullets, without asserting on content that
is expected to keep changing on every future automated sync (e.g. the
exact timestamp value or the auto-generated "[Auto-Sync] ..." diff-summary
bullet that the workflow prepends on each run).
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
STATE_PATH = REPO_ROOT / ".agents" / "brain" / "current_state.dsom"

FRONTMATTER_RE = re.compile(r"\A---\s*\r?\n(.*?)(?:\r?\n)?---\s*(?:\r?\n|\Z)", re.DOTALL)


class DsomCurrentStateFileTests(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue(STATE_PATH.is_file(), f"Expected {STATE_PATH} to exist")

    def test_file_not_empty(self):
        content = STATE_PATH.read_text(encoding="utf-8")
        self.assertTrue(content.strip())

    def test_no_utf8_bom(self):
        raw_bytes = STATE_PATH.read_bytes()
        self.assertFalse(raw_bytes.startswith(b"\xef\xbb\xbf"))

    def test_starts_with_frontmatter_fence(self):
        content = STATE_PATH.read_text(encoding="utf-8")
        self.assertTrue(content.startswith(("---\n", "---\r\n")))


class DsomCurrentStateFrontmatterTextTests(unittest.TestCase):
    """Regex/substring checks that don't require a YAML parser."""

    @classmethod
    def setUpClass(cls):
        cls.content = STATE_PATH.read_text(encoding="utf-8")
        match = FRONTMATTER_RE.match(cls.content)
        assert match is not None, "Expected a parseable frontmatter block"
        cls.raw_frontmatter = match.group(1)

    def test_timestamp_field_is_double_quoted(self):
        self.assertRegex(
            self.raw_frontmatter,
            r'timestamp:\s*"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z"',
        )

    def test_topics_field_is_inline_double_quoted_array(self):
        self.assertRegex(
            self.raw_frontmatter,
            r'topics:\s*\["state",\s*"memory",\s*"compaction"\]',
        )

    def test_okf_version_and_type_present(self):
        self.assertIn("okf_version: 0.1", self.raw_frontmatter)
        self.assertIn("type: dsom_state", self.raw_frontmatter)


@unittest.skipUnless(HAS_YAML, "PyYAML is not installed in this environment")
class DsomCurrentStateFrontmatterStructureTests(unittest.TestCase):
    """Structural checks against the parsed YAML document."""

    @classmethod
    def setUpClass(cls):
        cls.content = STATE_PATH.read_text(encoding="utf-8")
        match = FRONTMATTER_RE.match(cls.content)
        assert match is not None
        cls.frontmatter = yaml.safe_load(match.group(1))
        cls.body = cls.content[match.end():]

    def test_frontmatter_is_a_mapping(self):
        self.assertIsInstance(self.frontmatter, dict)

    def test_okf_version_and_type(self):
        self.assertEqual(self.frontmatter.get("okf_version"), 0.1)
        self.assertEqual(self.frontmatter.get("type"), "dsom_state")

    def test_timestamp_is_a_string_not_a_datetime(self):
        # A bare/unquoted timestamp would be auto-parsed by PyYAML into a
        # datetime object; the quoting introduced by this PR keeps it a str.
        timestamp = self.frontmatter.get("timestamp")
        self.assertIsInstance(timestamp, str)
        self.assertRegex(timestamp, r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")

    def test_topics_is_a_list_of_the_expected_strings(self):
        self.assertEqual(self.frontmatter.get("topics"), ["state", "memory", "compaction"])
        for topic in self.frontmatter["topics"]:
            self.assertIsInstance(topic, str)

    def test_description_field_present(self):
        self.assertIn("description", self.frontmatter)
        self.assertIsInstance(self.frontmatter["description"], str)


class DsomCurrentStateBodyContentTests(unittest.TestCase):
    """Checks for the new narrative bullets added by this PR."""

    @classmethod
    def setUpClass(cls):
        cls.content = STATE_PATH.read_text(encoding="utf-8")

    def test_active_state_section_present(self):
        self.assertIn("## Active State", self.content)

    def test_condensed_history_section_present(self):
        self.assertIn("## Condensed History", self.content)

    def test_active_state_mentions_jules_and_antigravity_upgrade(self):
        self.assertIn(
            "Semantic Compaction pipeline upgraded to support Google Jules & "
            "Google Antigravity personas with a robust, zero-API local "
            "Python fallback engine.",
            self.content,
        )

    def test_condensed_history_mentions_action_update_dsom_refactor(self):
        self.assertIn(
            "Refactored .github/scripts/action_update_dsom.py to integrate "
            "Gemini/Google API for Jules/Antigravity and local automated "
            "compaction fallback.",
            self.content,
        )

    def test_new_bullets_appear_after_pre_existing_bullets_in_their_sections(self):
        # Regression guard: confirms the new bullets were appended to the
        # existing lists rather than replacing prior history.
        active_state_idx = self.content.index("## Active State")
        sovereign_bullet_idx = self.content.index(
            "Sovereign Engine and Security Policies defined.", active_state_idx
        )
        jules_bullet_idx = self.content.index(
            "Semantic Compaction pipeline upgraded", active_state_idx
        )
        self.assertLess(sovereign_bullet_idx, jules_bullet_idx)

        history_idx = self.content.index("## Condensed History")
        boilerplate_idx = self.content.index(
            "Initial boilerplate replaced with DSOM-specific policies.", history_idx
        )
        refactor_idx = self.content.index(
            "Refactored .github/scripts/action_update_dsom.py", history_idx
        )
        self.assertLess(refactor_idx, boilerplate_idx)


if __name__ == "__main__":
    unittest.main()