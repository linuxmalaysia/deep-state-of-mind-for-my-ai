"""
Unit tests for `.github/scripts/action_update_dsom.py`.

This PR replaces the previous OpenAI-only Semantic Compaction pipeline with:

1. A Gemini (Google Generative Language API) integration supporting both a
   "Jules" and an "Antigravity" persona, selected via the `ACTIVE_AGENT`
   environment variable and authenticated via `GEMINI_API_KEY` or
   `GOOGLE_API_KEY`.
2. A dependency-free local Python fallback engine (`local_compaction`) that
   is used whenever no API key is configured, or whenever the Gemini API
   call fails for any reason.
3. Robust OKF v0.1 frontmatter handling (BOM stripping, multi-block parsing,
   metadata normalisation/serialisation, and atomic file replacement) that
   mirrors the sibling implementation in `tools/apply_okf_frontmatter.py`.

These tests exercise each new/rewritten helper function directly, and also
exercise `main()` end-to-end against temporary files (mocking `requests.post`
for the Gemini-API-enabled code path) to confirm the on-disk output matches
the documented behaviour. Tests that require `PyYAML`/`requests` to import
the module are skipped gracefully if those packages are unavailable in the
current environment, following the convention already established in
`tests/test_dsom_pr_sync_workflow.py`.
"""
import importlib.util
import json
import os
import pathlib
import stat
import sys
import tempfile
import unittest
from unittest import mock

try:
    import yaml  # type: ignore
    import requests  # type: ignore
    HAS_DEPS = True
except ImportError:  # pragma: no cover - environment dependent
    HAS_DEPS = False


def _find_repo_root(start: pathlib.Path) -> pathlib.Path:
    current = start.resolve()
    for parent in [current, *current.parents]:
        if (parent / ".git").exists():
            return parent
    raise RuntimeError("Could not locate repository root (.git not found)")


REPO_ROOT = _find_repo_root(pathlib.Path(__file__).parent)
SCRIPT_PATH = REPO_ROOT / ".github" / "scripts" / "action_update_dsom.py"


def _load_module():
    """Load action_update_dsom.py as a standalone module.

    The script lives under a dot-prefixed directory (`.github/scripts`),
    so it is loaded via `importlib.util` rather than relying on package
    imports, matching the convention used in
    `tests/test_dsom_signature_injector.py`.
    """
    spec = importlib.util.spec_from_file_location("action_update_dsom", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ScriptFileExistsTests(unittest.TestCase):
    def test_script_exists(self):
        self.assertTrue(SCRIPT_PATH.is_file(), f"Expected {SCRIPT_PATH} to exist")

    def test_script_no_longer_requires_openai_package(self):
        # Regression guard: the OpenAI SDK dependency was fully removed by
        # this PR in favour of raw `requests` calls to the Gemini API.
        content = SCRIPT_PATH.read_text(encoding="utf-8")
        self.assertNotIn("from openai import OpenAI", content)
        self.assertNotIn("OPENAI_API_KEY", content)


@unittest.skipUnless(HAS_DEPS, "PyYAML and requests are required to import action_update_dsom.py")
class NeedsDoubleQuotesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod = _load_module()

    def test_plain_alphanumeric_string_does_not_need_quotes(self):
        self.assertFalse(self.mod.needs_double_quotes("dsom_state"))

    def test_string_with_spaces_underscores_and_hyphens_does_not_need_quotes(self):
        self.assertFalse(self.mod.needs_double_quotes("DSOM Current State_v1-final"))

    def test_empty_string_needs_quotes(self):
        self.assertTrue(self.mod.needs_double_quotes(""))

    def test_string_with_leading_or_trailing_whitespace_needs_quotes(self):
        self.assertTrue(self.mod.needs_double_quotes(" DSOM Current State"))
        self.assertTrue(self.mod.needs_double_quotes("DSOM Current State "))

    def test_string_with_newline_needs_quotes(self):
        self.assertTrue(self.mod.needs_double_quotes("line one\nline two"))

    def test_string_with_tab_needs_quotes(self):
        self.assertTrue(self.mod.needs_double_quotes("col1\tcol2"))

    def test_string_with_emoji_needs_quotes(self):
        self.assertTrue(self.mod.needs_double_quotes("\U0001F9E0 DSOM Current State"))

    def test_string_with_colon_needs_quotes(self):
        self.assertTrue(self.mod.needs_double_quotes("2026-08-11T13:48:53Z"))

    def test_string_with_square_brackets_needs_quotes(self):
        self.assertTrue(self.mod.needs_double_quotes("[Auto-Sync]"))

    def test_non_string_int_does_not_need_quotes(self):
        self.assertFalse(self.mod.needs_double_quotes(1))

    def test_non_string_none_does_not_need_quotes(self):
        self.assertFalse(self.mod.needs_double_quotes(None))

    def test_non_string_list_does_not_need_quotes(self):
        self.assertFalse(self.mod.needs_double_quotes(["state", "memory"]))

    def test_non_string_float_does_not_need_quotes(self):
        self.assertFalse(self.mod.needs_double_quotes(0.1))


@unittest.skipUnless(HAS_DEPS, "PyYAML and requests are required to import action_update_dsom.py")
class SerialiseValTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod = _load_module()

    def test_list_of_plain_strings_renders_as_inline_double_quoted_array(self):
        result = self.mod.serialise_val(["state", "memory", "compaction"], "topics")
        self.assertEqual(result, '["state", "memory", "compaction"]')

    def test_empty_list_renders_as_empty_brackets(self):
        self.assertEqual(self.mod.serialise_val([], "topics"), "[]")

    def test_list_with_special_characters_is_still_double_quoted(self):
        result = self.mod.serialise_val(["git:history", "a b"], "topics")
        self.assertEqual(result, '["git:history", "a b"]')

    def test_list_result_is_valid_yaml_flow_sequence(self):
        result = self.mod.serialise_val(["state", "memory"], "topics")
        self.assertEqual(yaml.safe_load(result), ["state", "memory"])

    def test_list_with_non_string_items_uses_yaml_fallback_serialisation(self):
        self.assertEqual(self.mod.serialise_val([1, 2, 3], "numbers"), "[1, 2, 3]")

    def test_plain_string_returned_unquoted(self):
        self.assertEqual(self.mod.serialise_val("dsom_state", "type"), "dsom_state")

    def test_string_needing_quotes_is_json_double_quoted(self):
        result = self.mod.serialise_val("2026-08-11T13:48:53Z", "timestamp")
        self.assertEqual(result, '"2026-08-11T13:48:53Z"')

    def test_string_with_embedded_double_quote_is_escaped(self):
        result = self.mod.serialise_val('say "hi"', "title")
        self.assertEqual(yaml.safe_load(result), 'say "hi"')

    def test_float_uses_yaml_safe_dump_fallback(self):
        self.assertEqual(self.mod.serialise_val(0.1, "okf_version"), "0.1")

    def test_none_uses_yaml_safe_dump_fallback(self):
        self.assertEqual(self.mod.serialise_val(None, "assignees"), "null")


@unittest.skipUnless(HAS_DEPS, "PyYAML and requests are required to import action_update_dsom.py")
class ReadFileAndStripBomTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod = _load_module()

    def setUp(self):
        self.fd, self.path = tempfile.mkstemp(suffix=".dsom")
        os.close(self.fd)

    def tearDown(self):
        if os.path.exists(self.path):
            os.remove(self.path)

    def test_plain_utf8_file_has_no_bom_detected(self):
        with open(self.path, "w", encoding="utf-8") as f:
            f.write("---\ntitle: Plain\n---\nBody\n")

        content, had_bom = self.mod.read_file_and_strip_bom(self.path)
        self.assertFalse(had_bom)
        self.assertEqual(content, "---\ntitle: Plain\n---\nBody\n")

    def test_bom_prefixed_file_is_detected_and_stripped(self):
        with open(self.path, "w", encoding="utf-8-sig") as f:
            f.write("---\ntitle: BOM\n---\nBody\n")

        content, had_bom = self.mod.read_file_and_strip_bom(self.path)
        self.assertTrue(had_bom)
        self.assertNotIn("\ufeff", content)
        self.assertTrue(content.startswith("---\n"))

    def test_missing_file_raises_file_not_found_error(self):
        os.remove(self.path)
        with self.assertRaises(FileNotFoundError):
            self.mod.read_file_and_strip_bom(self.path)


@unittest.skipUnless(HAS_DEPS, "PyYAML and requests are required to import action_update_dsom.py")
class ParseFrontmatterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod = _load_module()

    def test_single_frontmatter_block_is_extracted(self):
        content = "---\nokf_version: 0.1\ntitle: Hello\n---\n# Hello\nBody text.\n"
        frontmatter, rest = self.mod.parse_frontmatter(content, "state.dsom")
        self.assertEqual(frontmatter, {"okf_version": 0.1, "title": "Hello"})
        self.assertEqual(rest, "# Hello\nBody text.\n")

    def test_no_frontmatter_block_returns_empty_dict_and_original_content(self):
        content = "# Just a heading\nNo frontmatter here.\n"
        frontmatter, rest = self.mod.parse_frontmatter(content, "state.dsom")
        self.assertEqual(frontmatter, {})
        self.assertEqual(rest, content)

    def test_consecutive_frontmatter_blocks_merge_with_later_taking_precedence(self):
        content = (
            "---\n"
            "okf_version: 0.1\n"
            "title: First\n"
            "---\n"
            "---\n"
            "title: Second\n"
            "topics: [a, b]\n"
            "---\n"
            "Body.\n"
        )
        frontmatter, rest = self.mod.parse_frontmatter(content, "state.dsom")
        self.assertEqual(frontmatter["okf_version"], 0.1)
        self.assertEqual(frontmatter["title"], "Second")
        self.assertEqual(frontmatter["topics"], ["a", "b"])
        self.assertEqual(rest, "Body.\n")

    def test_non_mapping_frontmatter_block_raises_value_error(self):
        content = "---\n- item1\n- item2\n---\nBody\n"
        with self.assertRaises(ValueError):
            self.mod.parse_frontmatter(content, "state.dsom")

    def test_malformed_yaml_raises_value_error(self):
        content = "---\nkey: [unterminated\n---\nBody\n"
        with self.assertRaises(ValueError):
            self.mod.parse_frontmatter(content, "state.dsom")

    def test_bare_iso_timestamp_is_parsed_as_string_not_datetime(self):
        # CustomLoader strips the implicit YAML timestamp resolver so that
        # unquoted ISO-8601 values stay plain strings rather than being
        # promoted to datetime.datetime objects.
        content = "---\ntimestamp: 2026-08-11T13:48:53Z\n---\nBody\n"
        frontmatter, _ = self.mod.parse_frontmatter(content, "state.dsom")
        self.assertIsInstance(frontmatter["timestamp"], str)
        self.assertEqual(frontmatter["timestamp"], "2026-08-11T13:48:53Z")

    def test_empty_frontmatter_block_returns_empty_dict(self):
        content = "---\n---\nBody\n"
        frontmatter, rest = self.mod.parse_frontmatter(content, "state.dsom")
        self.assertEqual(frontmatter, {})
        self.assertEqual(rest, "Body\n")


@unittest.skipUnless(HAS_DEPS, "PyYAML and requests are required to import action_update_dsom.py")
class NormaliseMetadataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod = _load_module()

    def test_defaults_are_applied_when_frontmatter_is_empty(self):
        updated = self.mod.normalise_metadata({}, "state.dsom", "state.dsom")
        self.assertEqual(updated["okf_version"], 0.1)
        self.assertEqual(updated["type"], "dsom_state")
        self.assertEqual(updated["title"], "DSOM Current State")
        self.assertEqual(updated["topics"], ["state", "memory", "compaction"])
        self.assertRegex(updated["timestamp"], r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")

    def test_existing_title_type_and_topics_are_preserved(self):
        existing = {
            "okf_version": 0.1,
            "type": "custom_type",
            "title": "Custom Title",
            "timestamp": "2000-01-01T00:00:00Z",
            "topics": ["custom", "topic"],
        }
        updated = self.mod.normalise_metadata(existing, "state.dsom", "state.dsom")
        self.assertEqual(updated["type"], "custom_type")
        self.assertEqual(updated["title"], "Custom Title")
        self.assertEqual(updated["topics"], ["custom", "topic"])

    def test_timestamp_is_always_refreshed_even_if_already_present(self):
        # Unlike tools/apply_okf_frontmatter.py's normalise_metadata (which
        # only fills in a timestamp when missing), this script's version
        # unconditionally overwrites the timestamp on every run.
        existing = {"timestamp": "2000-01-01T00:00:00Z"}
        updated = self.mod.normalise_metadata(existing, "state.dsom", "state.dsom")
        self.assertNotEqual(updated["timestamp"], "2000-01-01T00:00:00Z")
        self.assertRegex(updated["timestamp"], r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")

    def test_extra_fields_are_preserved(self):
        existing = {"description": "Some description", "custom_field": 42}
        updated = self.mod.normalise_metadata(existing, "state.dsom", "state.dsom")
        self.assertEqual(updated["description"], "Some description")
        self.assertEqual(updated["custom_field"], 42)

    def test_core_fields_come_before_extra_fields_in_key_order(self):
        existing = {"description": "Some description"}
        updated = self.mod.normalise_metadata(existing, "state.dsom", "state.dsom")
        keys = list(updated.keys())
        self.assertEqual(keys[:5], ["okf_version", "type", "title", "timestamp", "topics"])
        self.assertIn("description", keys[5:])


@unittest.skipUnless(HAS_DEPS, "PyYAML and requests are required to import action_update_dsom.py")
class SerialiseFrontmatterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod = _load_module()

    def test_output_is_wrapped_in_frontmatter_fences(self):
        updated = {
            "okf_version": 0.1,
            "type": "dsom_state",
            "title": "DSOM Current State",
            "timestamp": "2026-08-11T13:48:53Z",
            "topics": ["state", "memory", "compaction"],
        }
        block = self.mod.serialise_frontmatter(updated, "current_state.dsom")
        self.assertTrue(block.startswith("---\n"))
        self.assertTrue(block.endswith("---\n"))

    def test_core_keys_are_emitted_in_fixed_order(self):
        updated = {
            "topics": ["state"],
            "title": "DSOM Current State",
            "okf_version": 0.1,
            "timestamp": "2026-08-11T13:48:53Z",
            "type": "dsom_state",
        }
        block = self.mod.serialise_frontmatter(updated, "current_state.dsom")
        lines = [l for l in block.splitlines() if l and l != "---"]
        keys_in_order = [l.split(":", 1)[0] for l in lines]
        self.assertEqual(keys_in_order[:5], ["okf_version", "type", "title", "timestamp", "topics"])

    def test_extra_keys_appended_after_core_keys(self):
        updated = {
            "okf_version": 0.1,
            "type": "dsom_state",
            "title": "DSOM Current State",
            "timestamp": "2026-08-11T13:48:53Z",
            "topics": ["state"],
            "description": "A description with: a colon",
        }
        block = self.mod.serialise_frontmatter(updated, "current_state.dsom")
        self.assertIn('description: "A description with: a colon"', block)
        self.assertLess(block.index("topics:"), block.index("description:"))

    def test_title_needing_quotes_is_double_quoted_and_plain_title_is_not(self):
        plain = self.mod.serialise_frontmatter(
            {"okf_version": 0.1, "type": "t", "title": "PlainTitle", "timestamp": "x", "topics": []},
            "f.dsom",
        )
        self.assertIn("title: PlainTitle\n", plain)

        quoted = self.mod.serialise_frontmatter(
            {"okf_version": 0.1, "type": "t", "title": "Quoted: Title", "timestamp": "x", "topics": []},
            "f.dsom",
        )
        self.assertIn('title: "Quoted: Title"', quoted)

    def test_result_round_trips_through_yaml_as_valid_mapping(self):
        updated = {
            "okf_version": 0.1,
            "type": "dsom_state",
            "title": "DSOM Current State",
            "timestamp": "2026-08-11T13:48:53Z",
            "topics": ["state", "memory", "compaction"],
        }
        block = self.mod.serialise_frontmatter(updated, "current_state.dsom")
        inner = block[len("---\n"):-len("---\n")]
        parsed = yaml.safe_load(inner)
        self.assertEqual(parsed, updated)


@unittest.skipUnless(HAS_DEPS, "PyYAML and requests are required to import action_update_dsom.py")
class AtomicReplaceFileTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod = _load_module()

    def setUp(self):
        self.fd, self.path = tempfile.mkstemp(suffix=".dsom")
        os.close(self.fd)

    def tearDown(self):
        if os.path.exists(self.path):
            os.remove(self.path)

    def test_content_is_replaced(self):
        with open(self.path, "w", encoding="utf-8") as f:
            f.write("old content")

        self.mod.atomic_replace_file(self.path, "new content", os.path.basename(self.path))

        with open(self.path, "r", encoding="utf-8") as f:
            self.assertEqual(f.read(), "new content")

    def test_permission_mode_is_preserved(self):
        with open(self.path, "w", encoding="utf-8") as f:
            f.write("old content")
        original_mode = os.stat(self.path).st_mode
        target_mode = original_mode | stat.S_IXUSR
        os.chmod(self.path, target_mode)

        self.mod.atomic_replace_file(self.path, "new content", os.path.basename(self.path))

        if os.name != "nt":
            self.assertEqual(stat.S_IMODE(os.stat(self.path).st_mode), stat.S_IMODE(target_mode))

    def test_no_leftover_temp_files_after_successful_replace(self):
        with open(self.path, "w", encoding="utf-8") as f:
            f.write("old content")
        directory = os.path.dirname(self.path)
        before = set(os.listdir(directory))

        self.mod.atomic_replace_file(self.path, "new content", os.path.basename(self.path))

        after = set(os.listdir(directory))
        self.assertEqual(before, after)

    def test_failure_during_replace_cleans_up_temp_file_and_reraises(self):
        with open(self.path, "w", encoding="utf-8") as f:
            f.write("original content")
        directory = os.path.dirname(self.path)
        before = set(os.listdir(directory))

        with mock.patch.object(self.mod.os, "replace", side_effect=OSError("boom")):
            with self.assertRaises(OSError):
                self.mod.atomic_replace_file(self.path, "new content", os.path.basename(self.path))

        # Original file must remain untouched, and no stray temp file left behind.
        with open(self.path, "r", encoding="utf-8") as f:
            self.assertEqual(f.read(), "original content")
        after = set(os.listdir(directory))
        self.assertEqual(before, after)


@unittest.skipUnless(HAS_DEPS, "PyYAML and requests are required to import action_update_dsom.py")
class LocalCompactionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod = _load_module()

    def test_no_files_modified_produces_placeholder_summary(self):
        rest = "## Condensed History\n- Existing entry.\n"
        result = self.mod.local_compaction("not a real diff", rest)
        self.assertIn("[Auto-Sync] No code files modified in diff.", result)

    def test_single_file_diff_counts_additions_and_deletions_correctly(self):
        diff = (
            "diff --git a/foo.py b/foo.py\n"
            "index 1111111..2222222 100644\n"
            "--- a/foo.py\n"
            "+++ b/foo.py\n"
            "@@ -1,2 +1,3 @@\n"
            " unchanged line\n"
            "-removed line\n"
            "+added line one\n"
            "+added line two\n"
        )
        rest = "## Condensed History\n- Existing entry.\n"
        result = self.mod.local_compaction(diff, rest)
        self.assertIn("[Auto-Sync] Modified files: foo.py (+2, -1).", result)

    def test_header_lines_are_excluded_from_added_and_deleted_counts(self):
        # The "+++"/"---" file header lines must not be counted as an
        # added/deleted content line, including for brand new files.
        diff = (
            "diff --git a/new_file.py b/new_file.py\n"
            "new file mode 100644\n"
            "index 0000000..1111111\n"
            "--- /dev/null\n"
            "+++ b/new_file.py\n"
            "@@ -0,0 +1,2 @@\n"
            "+line one\n"
            "+line two\n"
        )
        rest = "## Condensed History\n- Existing entry.\n"
        result = self.mod.local_compaction(diff, rest)
        self.assertIn("[Auto-Sync] Modified files: new_file.py (+2, -0).", result)

    def test_multiple_files_are_joined_with_commas_in_order(self):
        diff = (
            "diff --git a/a.py b/a.py\n"
            "--- a/a.py\n"
            "+++ b/a.py\n"
            "+added to a\n"
            "diff --git a/b.py b/b.py\n"
            "--- a/b.py\n"
            "+++ b/b.py\n"
            "-removed from b\n"
            "-removed from b again\n"
        )
        rest = "## Condensed History\n- Existing entry.\n"
        result = self.mod.local_compaction(diff, rest)
        self.assertIn(
            "[Auto-Sync] Modified files: a.py (+1, -0), b.py (+0, -2).", result
        )

    def test_bullet_is_inserted_before_first_existing_bullet_after_blank_line(self):
        rest = "## Condensed History\n\n- Existing entry one.\n- Existing entry two.\n"
        diff = "diff --git a/x.py b/x.py\n+++ b/x.py\n+added\n"
        result = self.mod.local_compaction(diff, rest)
        lines = result.splitlines()
        auto_sync_idx = next(i for i, l in enumerate(lines) if l.startswith("- [Auto-Sync]"))
        existing_idx = next(i for i, l in enumerate(lines) if l == "- Existing entry one.")
        self.assertLess(auto_sync_idx, existing_idx)

    def test_bullet_inserted_immediately_when_no_blank_line_before_first_bullet(self):
        rest = "## Condensed History\n- Existing entry one.\n"
        diff = "diff --git a/x.py b/x.py\n+++ b/x.py\n+added\n"
        result = self.mod.local_compaction(diff, rest)
        lines = result.splitlines()
        bullet_lines = [l for l in lines if l.startswith("-")]
        self.assertTrue(bullet_lines[0].startswith("- [Auto-Sync]"))
        self.assertEqual(bullet_lines[1], "- Existing entry one.")

    def test_missing_condensed_history_heading_appends_new_section(self):
        rest = "# DSOM Current State\n\n## Active State\n- Some state.\n"
        diff = "diff --git a/x.py b/x.py\n+++ b/x.py\n+added\n"
        result = self.mod.local_compaction(diff, rest)
        self.assertTrue(result.rstrip("\n").endswith(
            "[Auto-Sync] Modified files: x.py (+1, -0)."
        ))
        self.assertIn("## Condensed History", result)

    def test_result_preserves_content_before_condensed_history_heading(self):
        rest = "# DSOM Current State\n\n## Active State\n- Some state.\n\n## Condensed History\n- Old entry.\n"
        diff = "diff --git a/x.py b/x.py\n+++ b/x.py\n+added\n"
        result = self.mod.local_compaction(diff, rest)
        self.assertIn("## Active State\n- Some state.", result)
        self.assertIn("- Old entry.", result)


@unittest.skipUnless(HAS_DEPS, "PyYAML and requests are required to import action_update_dsom.py")
class MainIntegrationTests(unittest.TestCase):
    """End-to-end tests for `main()` against temporary diff/state files."""

    @classmethod
    def setUpClass(cls):
        cls.mod = _load_module()

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.diff_path = os.path.join(self.tmpdir, "pr.diff")
        self.state_path = os.path.join(self.tmpdir, "current_state.dsom")

    def _write_diff(self, content):
        with open(self.diff_path, "w", encoding="utf-8") as f:
            f.write(content)

    def _write_state(self, content, encoding="utf-8"):
        with open(self.state_path, "w", encoding=encoding) as f:
            f.write(content)

    def _read_state(self):
        with open(self.state_path, "r", encoding="utf-8") as f:
            return f.read()

    def _run_main(self, env=None):
        env = env or {}
        with mock.patch.object(sys, "argv", ["action_update_dsom.py", self.diff_path, self.state_path]):
            with mock.patch.dict(os.environ, env, clear=True):
                self.mod.main()

    def test_wrong_number_of_arguments_exits_with_status_1(self):
        with mock.patch.object(sys, "argv", ["action_update_dsom.py", "only_one_arg"]):
            with self.assertRaises(SystemExit) as ctx:
                self.mod.main()
            self.assertEqual(ctx.exception.code, 1)

    def test_missing_state_file_exits_with_status_1(self):
        self._write_diff("diff --git a/x.py b/x.py\n+++ b/x.py\n+added\n")
        # Do not create self.state_path.
        with mock.patch.object(sys, "argv", ["action_update_dsom.py", self.diff_path, self.state_path]):
            with mock.patch.dict(os.environ, {}, clear=True):
                with self.assertRaises(SystemExit) as ctx:
                    self.mod.main()
                self.assertEqual(ctx.exception.code, 1)

    def test_no_api_key_falls_back_to_local_compaction(self):
        self._write_diff("diff --git a/foo.py b/foo.py\n+++ b/foo.py\n+added line\n")
        self._write_state(
            "---\n"
            "okf_version: 0.1\n"
            "type: dsom_state\n"
            "title: DSOM Current State\n"
            "timestamp: \"2000-01-01T00:00:00Z\"\n"
            "topics: [\"state\", \"memory\"]\n"
            "---\n"
            "# DSOM Current State\n\n"
            "## Condensed History\n"
            "- Existing entry.\n"
        )

        with mock.patch.object(self.mod, "requests") as mock_requests:
            self._run_main(env={})
            mock_requests.post.assert_not_called()

        result = self._read_state()
        self.assertIn("[Auto-Sync] Modified files: foo.py (+1, -0).", result)
        self.assertIn("title: DSOM Current State", result)
        # Timestamp must have been refreshed away from the placeholder value.
        self.assertNotIn("2000-01-01T00:00:00Z", result)

    def test_bom_prefixed_input_state_file_is_cleaned_on_write(self):
        self._write_diff("diff --git a/foo.py b/foo.py\n+++ b/foo.py\n+added line\n")
        self._write_state(
            "---\n"
            "okf_version: 0.1\n"
            "type: dsom_state\n"
            "title: DSOM Current State\n"
            "timestamp: \"2000-01-01T00:00:00Z\"\n"
            "topics: [\"state\"]\n"
            "---\n"
            "# DSOM Current State\n\n"
            "## Condensed History\n"
            "- Existing entry.\n",
            encoding="utf-8-sig",
        )

        self._run_main(env={})

        with open(self.state_path, "rb") as f:
            raw = f.read()
        self.assertFalse(raw.startswith(b"\xef\xbb\xbf"))

    def test_successful_gemini_response_uses_ai_body_but_original_frontmatter_fields(self):
        self._write_diff("diff --git a/foo.py b/foo.py\n+++ b/foo.py\n+added line\n")
        self._write_state(
            "---\n"
            "okf_version: 0.1\n"
            "type: dsom_state\n"
            "title: Original Title\n"
            "timestamp: \"2000-01-01T00:00:00Z\"\n"
            "topics: [\"state\"]\n"
            "---\n"
            "# Original Title\n\n"
            "## Condensed History\n"
            "- Existing entry.\n"
        )

        ai_response_text = (
            "---\n"
            "title: AI-Suggested Title\n"
            "---\n"
            "# AI Body\n"
            "AI-generated condensed content.\n"
        )
        fake_response = mock.Mock()
        fake_response.raise_for_status = mock.Mock()
        fake_response.json.return_value = {
            "candidates": [{"content": {"parts": [{"text": ai_response_text}]}}]
        }

        with mock.patch.object(self.mod.requests, "post", return_value=fake_response) as mock_post:
            self._run_main(env={"GEMINI_API_KEY": "test-key"})
            mock_post.assert_called_once()

        result = self._read_state()
        # Body comes from the AI response...
        self.assertIn("# AI Body", result)
        self.assertIn("AI-generated condensed content.", result)
        # ...but frontmatter fields are re-derived from the ORIGINAL file's
        # existing frontmatter, not the AI's own (discarded) frontmatter.
        self.assertIn("title: Original Title", result)
        self.assertNotIn("AI-Suggested Title", result)

    def test_gemini_response_wrapped_in_markdown_fence_is_unwrapped(self):
        self._write_diff("diff --git a/foo.py b/foo.py\n+++ b/foo.py\n+added line\n")
        self._write_state(
            "---\n"
            "okf_version: 0.1\n"
            "type: dsom_state\n"
            "title: Original Title\n"
            "timestamp: \"2000-01-01T00:00:00Z\"\n"
            "topics: [\"state\"]\n"
            "---\n"
            "# Original Title\n\n"
            "## Condensed History\n"
            "- Existing entry.\n"
        )

        ai_response_text = "```\n---\ntitle: Ignored\n---\n# Fenced Body\nContent inside fences.\n```"
        fake_response = mock.Mock()
        fake_response.raise_for_status = mock.Mock()
        fake_response.json.return_value = {
            "candidates": [{"content": {"parts": [{"text": ai_response_text}]}}]
        }

        with mock.patch.object(self.mod.requests, "post", return_value=fake_response):
            self._run_main(env={"GOOGLE_API_KEY": "test-key"})

        result = self._read_state()
        self.assertIn("# Fenced Body", result)
        self.assertIn("Content inside fences.", result)
        self.assertNotIn("```", result)

    def test_gemini_api_failure_falls_back_to_local_compaction(self):
        self._write_diff("diff --git a/foo.py b/foo.py\n+++ b/foo.py\n+added line\n")
        self._write_state(
            "---\n"
            "okf_version: 0.1\n"
            "type: dsom_state\n"
            "title: Original Title\n"
            "timestamp: \"2000-01-01T00:00:00Z\"\n"
            "topics: [\"state\"]\n"
            "---\n"
            "# Original Title\n\n"
            "## Condensed History\n"
            "- Existing entry.\n"
        )

        with mock.patch.object(
            self.mod.requests, "post", side_effect=RuntimeError("network unreachable")
        ):
            self._run_main(env={"GEMINI_API_KEY": "test-key"})

        result = self._read_state()
        self.assertIn("[Auto-Sync] Modified files: foo.py (+1, -0).", result)

    def test_gemini_response_missing_expected_keys_falls_back_to_local_compaction(self):
        self._write_diff("diff --git a/foo.py b/foo.py\n+++ b/foo.py\n+added line\n")
        self._write_state(
            "---\n"
            "okf_version: 0.1\n"
            "type: dsom_state\n"
            "title: Original Title\n"
            "timestamp: \"2000-01-01T00:00:00Z\"\n"
            "topics: [\"state\"]\n"
            "---\n"
            "# Original Title\n\n"
            "## Condensed History\n"
            "- Existing entry.\n"
        )

        fake_response = mock.Mock()
        fake_response.raise_for_status = mock.Mock()
        fake_response.json.return_value = {"unexpected": "shape"}

        with mock.patch.object(self.mod.requests, "post", return_value=fake_response):
            self._run_main(env={"GEMINI_API_KEY": "test-key"})

        result = self._read_state()
        self.assertIn("[Auto-Sync] Modified files: foo.py (+1, -0).", result)

    def test_google_api_key_used_when_gemini_api_key_absent(self):
        self._write_diff("diff --git a/foo.py b/foo.py\n+++ b/foo.py\n+added\n")
        self._write_state(
            "---\n"
            "okf_version: 0.1\n"
            "type: dsom_state\n"
            "title: Original Title\n"
            "timestamp: \"2000-01-01T00:00:00Z\"\n"
            "topics: [\"state\"]\n"
            "---\n"
            "# Original Title\n\n"
            "## Condensed History\n"
            "- Existing entry.\n"
        )

        fake_response = mock.Mock()
        fake_response.raise_for_status = mock.Mock()
        fake_response.json.return_value = {
            "candidates": [{"content": {"parts": [{"text": "# Body\ntext\n"}]}}]
        }

        with mock.patch.object(self.mod.requests, "post", return_value=fake_response) as mock_post:
            self._run_main(env={"GOOGLE_API_KEY": "google-key"})
            mock_post.assert_called_once()
            called_url = mock_post.call_args[0][0]
            self.assertIn("key=google-key", called_url)

    def test_gemini_api_key_takes_precedence_over_google_api_key(self):
        self._write_diff("diff --git a/foo.py b/foo.py\n+++ b/foo.py\n+added\n")
        self._write_state(
            "---\n"
            "okf_version: 0.1\n"
            "type: dsom_state\n"
            "title: Original Title\n"
            "timestamp: \"2000-01-01T00:00:00Z\"\n"
            "topics: [\"state\"]\n"
            "---\n"
            "# Original Title\n\n"
            "## Condensed History\n"
            "- Existing entry.\n"
        )

        fake_response = mock.Mock()
        fake_response.raise_for_status = mock.Mock()
        fake_response.json.return_value = {
            "candidates": [{"content": {"parts": [{"text": "# Body\ntext\n"}]}}]
        }

        with mock.patch.object(self.mod.requests, "post", return_value=fake_response) as mock_post:
            self._run_main(env={"GEMINI_API_KEY": "gemini-key", "GOOGLE_API_KEY": "google-key"})
            called_url = mock_post.call_args[0][0]
            self.assertIn("key=gemini-key", called_url)
            self.assertNotIn("key=google-key", called_url)

    def test_default_active_agent_is_jules_persona(self):
        self._write_diff("diff --git a/foo.py b/foo.py\n+++ b/foo.py\n+added\n")
        self._write_state(
            "---\n"
            "okf_version: 0.1\n"
            "type: dsom_state\n"
            "title: Original Title\n"
            "timestamp: \"2000-01-01T00:00:00Z\"\n"
            "topics: [\"state\"]\n"
            "---\n"
            "# Original Title\n\n"
            "## Condensed History\n"
            "- Existing entry.\n"
        )

        fake_response = mock.Mock()
        fake_response.raise_for_status = mock.Mock()
        fake_response.json.return_value = {
            "candidates": [{"content": {"parts": [{"text": "# Body\ntext\n"}]}}]
        }

        with mock.patch.object(self.mod.requests, "post", return_value=fake_response) as mock_post:
            self._run_main(env={"GEMINI_API_KEY": "test-key"})
            payload = mock_post.call_args[1]["json"]
            sent_text = payload["contents"][0]["parts"][0]["text"]
            self.assertIn("Google Jules", sent_text)
            self.assertNotIn("Google Antigravity", sent_text)

    def test_antigravity_active_agent_selects_antigravity_persona(self):
        self._write_diff("diff --git a/foo.py b/foo.py\n+++ b/foo.py\n+added\n")
        self._write_state(
            "---\n"
            "okf_version: 0.1\n"
            "type: dsom_state\n"
            "title: Original Title\n"
            "timestamp: \"2000-01-01T00:00:00Z\"\n"
            "topics: [\"state\"]\n"
            "---\n"
            "# Original Title\n\n"
            "## Condensed History\n"
            "- Existing entry.\n"
        )

        fake_response = mock.Mock()
        fake_response.raise_for_status = mock.Mock()
        fake_response.json.return_value = {
            "candidates": [{"content": {"parts": [{"text": "# Body\ntext\n"}]}}]
        }

        with mock.patch.object(self.mod.requests, "post", return_value=fake_response) as mock_post:
            self._run_main(env={"GEMINI_API_KEY": "test-key", "ACTIVE_AGENT": "Antigravity"})
            payload = mock_post.call_args[1]["json"]
            sent_text = payload["contents"][0]["parts"][0]["text"]
            self.assertIn("Google Antigravity", sent_text)

    def test_active_agent_matching_is_case_insensitive(self):
        self._write_diff("diff --git a/foo.py b/foo.py\n+++ b/foo.py\n+added\n")
        self._write_state(
            "---\n"
            "okf_version: 0.1\n"
            "type: dsom_state\n"
            "title: Original Title\n"
            "timestamp: \"2000-01-01T00:00:00Z\"\n"
            "topics: [\"state\"]\n"
            "---\n"
            "# Original Title\n\n"
            "## Condensed History\n"
            "- Existing entry.\n"
        )

        fake_response = mock.Mock()
        fake_response.raise_for_status = mock.Mock()
        fake_response.json.return_value = {
            "candidates": [{"content": {"parts": [{"text": "# Body\ntext\n"}]}}]
        }

        with mock.patch.object(self.mod.requests, "post", return_value=fake_response) as mock_post:
            self._run_main(env={"GEMINI_API_KEY": "test-key", "ACTIVE_AGENT": "antIGRAVity"})
            payload = mock_post.call_args[1]["json"]
            sent_text = payload["contents"][0]["parts"][0]["text"]
            self.assertIn("Google Antigravity", sent_text)

    def test_output_frontmatter_block_is_valid_yaml_after_run(self):
        self._write_diff("diff --git a/foo.py b/foo.py\n+++ b/foo.py\n+added\n")
        self._write_state(
            "---\n"
            "okf_version: 0.1\n"
            "type: dsom_state\n"
            "title: Original Title\n"
            "timestamp: \"2000-01-01T00:00:00Z\"\n"
            "topics: [\"state\", \"memory\"]\n"
            "---\n"
            "# Original Title\n\n"
            "## Condensed History\n"
            "- Existing entry.\n"
        )

        self._run_main(env={})

        result = self._read_state()
        parts = result.split("---")
        self.assertEqual(len(parts), 3)
        parsed = yaml.safe_load(parts[1])
        self.assertEqual(parsed["okf_version"], 0.1)
        self.assertEqual(parsed["type"], "dsom_state")
        self.assertEqual(parsed["title"], "Original Title")
        self.assertEqual(parsed["topics"], ["state", "memory"])
        self.assertIsInstance(parsed["timestamp"], str)


if __name__ == "__main__":
    unittest.main()