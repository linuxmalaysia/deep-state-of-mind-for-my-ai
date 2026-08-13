"""
Regression tests for `.agents/brain/current_state.dsom` as updated by this PR.

This PR's diff to `current_state.dsom` demonstrates the new output format
produced by the rewritten `.github/scripts/action_update_dsom.py`:

1. `title` is now emitted bare/unquoted (`title: DSOM Current State`)
   because it contains no characters that trigger `needs_double_quotes()`.
2. `timestamp` and `topics` were moved up (immediately after `title`, before
   `description`) and are always double-quoted/JSON-style, matching
   `serialise_frontmatter()`'s fixed key order and `serialise_val()`'s
   quoting rules.
3. A new "Active State" bullet documents the Semantic Compaction pipeline
   upgrade, and a new "[Auto-Sync] Modified files: ..." bullet was inserted
   at the top of "Condensed History" by `local_compaction()`.

These tests pin down that on-disk state so future runs of the sync workflow
don't silently regress the frontmatter ordering/quoting or drop the new
history entries. Structural (YAML) assertions are skipped gracefully if
PyYAML is not installed, following the convention used elsewhere in this
test suite.
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


class CurrentStateFileTests(unittest.TestCase):
    def test_file_exists(self):
        self.assertTrue(STATE_PATH.is_file(), f"Expected {STATE_PATH} to exist")

    def test_no_leading_bom(self):
        raw_bytes = STATE_PATH.read_bytes()
        self.assertFalse(raw_bytes.startswith(b"\xef\xbb\xbf"))

    def test_starts_exactly_with_frontmatter_fence(self):
        content = STATE_PATH.read_text(encoding="utf-8")
        self.assertTrue(content.startswith("---\n"))


class FrontmatterTextFormatTests(unittest.TestCase):
    """Regex-based checks that don't require a YAML parser."""

    @classmethod
    def setUpClass(cls):
        cls.content = STATE_PATH.read_text(encoding="utf-8")
        match = FRONTMATTER_RE.match(cls.content)
        assert match is not None
        cls.frontmatter_raw = match.group(1)

    def test_title_is_emitted_unquoted(self):
        self.assertIn("title: DSOM Current State\n", self.frontmatter_raw)
        self.assertNotIn('title: "DSOM Current State"', self.frontmatter_raw)

    def test_timestamp_is_double_quoted(self):
        self.assertRegex(self.frontmatter_raw, r'timestamp: "\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z"')

    def test_topics_rendered_as_double_quoted_inline_array(self):
        self.assertIn('topics: ["state", "memory", "compaction"]', self.frontmatter_raw)

    def test_timestamp_and_topics_precede_description(self):
        timestamp_idx = self.frontmatter_raw.index("timestamp:")
        topics_idx = self.frontmatter_raw.index("topics:")
        description_idx = self.frontmatter_raw.index("description:")
        self.assertLess(timestamp_idx, topics_idx)
        self.assertLess(topics_idx, description_idx)

    def test_first_three_keys_are_okf_version_type_title(self):
        keys_in_order = [
            line.split(":", 1)[0]
            for line in self.frontmatter_raw.splitlines()
            if line.strip()
        ]
        self.assertEqual(keys_in_order[:3], ["okf_version", "type", "title"])


@unittest.skipUnless(HAS_YAML, "PyYAML is not installed in this environment")
class FrontmatterStructureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.content = STATE_PATH.read_text(encoding="utf-8")
        match = FRONTMATTER_RE.match(cls.content)
        assert match is not None
        cls.frontmatter = yaml.safe_load(match.group(1))

    def test_mandatory_okf_fields_present_with_expected_values(self):
        self.assertEqual(self.frontmatter["okf_version"], 0.1)
        self.assertEqual(self.frontmatter["type"], "dsom_state")
        self.assertEqual(self.frontmatter["title"], "DSOM Current State")
        self.assertEqual(self.frontmatter["topics"], ["state", "memory", "compaction"])

    def test_timestamp_parses_as_a_plain_string(self):
        # Guards against YAML auto-promoting an unquoted timestamp to a
        # datetime.datetime object; this file always double-quotes it.
        self.assertIsInstance(self.frontmatter["timestamp"], str)
        self.assertRegex(
            self.frontmatter["timestamp"], r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$"
        )

    def test_description_field_preserved(self):
        self.assertIn("Condensed, high-level operational state", self.frontmatter["description"])


class BodyContentRegressionTests(unittest.TestCase):
    """Pin down the body content changes introduced by this PR's diff."""

    @classmethod
    def setUpClass(cls):
        cls.content = STATE_PATH.read_text(encoding="utf-8")
        match = FRONTMATTER_RE.match(cls.content)
        assert match is not None
        cls.body = cls.content[match.end():]

    def test_active_state_documents_semantic_compaction_upgrade(self):
        self.assertIn(
            "Semantic Compaction pipeline upgraded to support Google Jules "
            "& Google Antigravity personas with a robust, zero-API local "
            "Python fallback engine.",
            self.body,
        )

    def test_condensed_history_contains_auto_sync_entry_for_script_change(self):
        self.assertRegex(
            self.body,
            r"- \[Auto-Sync\] Modified files:.*\.github/scripts/action_update_dsom\.py \(\+\d+, -\d+\)",
        )

    def test_auto_sync_entry_precedes_older_history_entries(self):
        auto_sync_idx = self.body.index("[Auto-Sync] Modified files:")
        older_entry_idx = self.body.index("Initial boilerplate replaced")
        self.assertLess(auto_sync_idx, older_entry_idx)

    def test_pre_existing_sections_still_present(self):
        self.assertIn("## Active State", self.body)
        self.assertIn("## Condensed History", self.body)
        self.assertIn("## Archival Pointers", self.body)


class NewestAutoSyncEntryRegressionTests(unittest.TestCase):
    """Pin down this PR's specific diff to the "Condensed History" list:
    a new entry documenting the test-file changes was inserted above the
    previous newest entry (the `action_update_dsom.py` rewrite), and two
    stale entries that were compacted away by an earlier sync are gone.
    """

    @classmethod
    def setUpClass(cls):
        cls.content = STATE_PATH.read_text(encoding="utf-8")
        match = FRONTMATTER_RE.match(cls.content)
        assert match is not None
        cls.body = cls.content[match.end():]

    def test_condensed_history_contains_newest_auto_sync_entry_for_test_files(self):
        self.assertRegex(
            self.body,
            r"- \[Auto-Sync\] Modified files: tests/test_crda_workflow\.py "
            r"\(\+\d+, -\d+\), tests/test_dsom_pr_sync_workflow\.py \(\+\d+, -\d+\)\.",
        )

    def test_newest_entry_precedes_action_update_dsom_entry(self):
        newest_idx = self.body.index("tests/test_crda_workflow.py")
        script_change_idx = self.body.index(
            "[Auto-Sync] Modified files: .github/scripts/action_update_dsom.py"
        )
        self.assertLess(newest_idx, script_change_idx)

    def test_stale_sitemap_seo_generator_skill_entry_removed(self):
        # This entry was present in an earlier PR's diff and was compacted
        # away; it must not resurface.
        self.assertNotIn("test_sitemap_seo_generator_skill.py (+624, -0)", self.body)

    def test_stale_legal_notice_bundle_entry_removed(self):
        # This large combined entry (LEGAL-NOTICE.md, sitemap regeneration,
        # etc.) was present in an earlier PR's diff and was compacted away;
        # it must not resurface.
        self.assertNotIn("LEGAL-NOTICE.md (+48, -0)", self.body)
        self.assertNotIn("docs/sitemap.xml (+488, -476)", self.body)


if __name__ == "__main__":
    unittest.main()