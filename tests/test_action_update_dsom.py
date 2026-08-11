"""
Unit tests for `.github/scripts/action_update_dsom.py`.

This PR rewrites the DSOM Semantic Compaction script so that it:

1. No longer requires the OpenAI SDK/`OPENAI_API_KEY`. Instead it uses the
   Gemini REST API directly via `requests`, driven by `GEMINI_API_KEY` or
   `GOOGLE_API_KEY`, and selects a "Jules" or "Antigravity" persona system
   prompt based on the `ACTIVE_AGENT` environment variable.
2. Adds a zero-API, purely local Python fallback engine
   (`local_compaction()`) that summarises a PR diff's added/deleted line
   counts per file and inserts an "[Auto-Sync]" bullet into the
   `## Condensed History` section (or appends a new section if absent).
3. Adds a small OKF frontmatter toolkit: `needs_double_quotes()`,
   `serialise_val()`, `read_file_and_strip_bom()`, `parse_frontmatter()`
   (multi-block merge, using a `CustomLoader` that disables YAML's implicit
   timestamp resolution so date-like strings stay strings),
   `normalise_metadata()` (refreshes the timestamp, preserves other
   fields), `serialise_frontmatter()` (stable key ordering) and
   `atomic_replace_file()` (write-to-temp + `os.replace`, preserving the
   original file's permission bits).
4. Rewrites `main()` to always attempt the Gemini API first (if a key is
   configured) and gracefully fall back to `local_compaction()` on any
   failure, before reassembling and atomically writing the updated
   `current_state.dsom` file.

These tests exercise the module in isolation (loaded via
`importlib.util`, following the convention established in
`tests/test_dsom_signature_injector.py`, since `.github/scripts/` is not an
importable package) using temporary files/directories so the real
repository tree is never modified. Network calls are mocked; nothing in
this test file makes real HTTP requests.
"""
import datetime
import importlib.util
import os
import pathlib
import stat
import sys
import tempfile
import unittest
from unittest import mock

try:
    import yaml  # type: ignore
    HAS_YAML = True
except ImportError:  # pragma: no cover - environment dependent
    HAS_YAML = False

try:
    import requests  # type: ignore  # noqa: F401
    HAS_REQUESTS = True
except ImportError:  # pragma: no cover - environment dependent
    HAS_REQUESTS = False

HAS_DEPS = HAS_YAML and HAS_REQUESTS


def _find_repo_root(start: pathlib.Path) -> pathlib.Path:
    current = start.resolve()
    for parent in [current, *current.parents]:
        if (parent / ".git").exists():
            return parent
    raise RuntimeError("Could not locate repository root (.git not found)")


REPO_ROOT = _find_repo_root(pathlib.Path(__file__).parent)
SCRIPT_PATH = REPO_ROOT / ".github" / "scripts" / "action_update_dsom.py"


def _load_module():
    """Load action_update_dsom.py as a standalone module (hidden directory)."""
    spec = importlib.util.spec_from_file_location("action_update_dsom", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ScriptFileExistsTests(unittest.TestCase):
    def test_script_exists(self):
        self.assertTrue(SCRIPT_PATH.is_file(), f"Expected {SCRIPT_PATH} to exist")

    def test_no_longer_imports_openai(self):
        content = SCRIPT_PATH.read_text(encoding="utf-8")
        self.assertNotIn("from openai import OpenAI", content)
        self.assertNotIn("OPENAI_API_KEY", content)

    def test_imports_requests_and_yaml(self):
        content = SCRIPT_PATH.read_text(encoding="utf-8")
        self.assertIn("import requests", content)
        self.assertIn("import yaml", content)


@unittest.skipUnless(HAS_DEPS, "PyYAML and requests are required to load action_update_dsom.py")
class NeedsDoubleQuotesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod = _load_module()

    def test_plain_alphanumeric_string_does_not_need_quotes(self):
        self.assertFalse(self.mod.needs_double_quotes("dsom_state"))

    def test_string_with_spaces_hyphens_underscores_does_not_need_quotes(self):
        self.assertFalse(self.mod.needs_double_quotes("state_memory-compaction test"))

    def test_empty_string_needs_quotes(self):
        self.assertTrue(self.mod.needs_double_quotes(""))

    def test_leading_or_trailing_whitespace_needs_quotes(self):
        self.assertTrue(self.mod.needs_double_quotes(" DSOM Current State"))
        self.assertTrue(self.mod.needs_double_quotes("DSOM Current State "))

    def test_string_with_newline_needs_quotes(self):
        self.assertTrue(self.mod.needs_double_quotes("line1\nline2"))

    def test_string_with_tab_needs_quotes(self):
        self.assertTrue(self.mod.needs_double_quotes("a\tb"))

    def test_string_with_colon_needs_quotes(self):
        self.assertTrue(self.mod.needs_double_quotes("2026-08-11T13:40:00Z"))

    def test_string_with_non_ascii_needs_quotes(self):
        self.assertTrue(self.mod.needs_double_quotes("Café"))

    def test_string_that_yaml_parses_as_non_string_needs_quotes(self):
        # "123" parses as an int, "yes"/"null" as bool/None -- all need quoting
        # to be preserved as literal strings.
        self.assertTrue(self.mod.needs_double_quotes("123"))
        self.assertTrue(self.mod.needs_double_quotes("yes"))
        self.assertTrue(self.mod.needs_double_quotes("null"))

    def test_non_string_values_do_not_need_quotes(self):
        self.assertFalse(self.mod.needs_double_quotes(42))
        self.assertFalse(self.mod.needs_double_quotes(0.1))
        self.assertFalse(self.mod.needs_double_quotes(None))
        self.assertFalse(self.mod.needs_double_quotes(["a", "b"]))


@unittest.skipUnless(HAS_DEPS, "PyYAML and requests are required to load action_update_dsom.py")
class SerialiseValTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod = _load_module()

    def test_list_of_plain_strings_renders_as_inline_double_quoted_array(self):
        result = self.mod.serialise_val(["state", "memory", "compaction"], "topics")
        self.assertEqual(result, '["state", "memory", "compaction"]')

    def test_empty_list_renders_as_empty_brackets(self):
        self.assertEqual(self.mod.serialise_val([], "topics"), "[]")

    def test_list_with_non_string_items_uses_yaml_fallback(self):
        self.assertEqual(self.mod.serialise_val([1, 2, 3], "nums"), "[1, 2, 3]")

    def test_plain_string_returned_unquoted(self):
        self.assertEqual(self.mod.serialise_val("dsom_state", "type"), "dsom_state")

    def test_string_requiring_quotes_is_json_encoded(self):
        result = self.mod.serialise_val("2026-08-11T13:40:00Z", "timestamp")
        self.assertEqual(result, '"2026-08-11T13:40:00Z"')

    def test_string_with_embedded_quote_is_escaped_in_list(self):
        result = self.mod.serialise_val(['say "hi"'], "topics")
        parsed = yaml.safe_load(result)
        self.assertEqual(parsed, ['say "hi"'])

    def test_float_uses_yaml_fallback(self):
        self.assertEqual(self.mod.serialise_val(0.1, "okf_version"), "0.1")

    def test_none_uses_yaml_fallback(self):
        self.assertEqual(self.mod.serialise_val(None, "field"), "null")

    def test_bool_uses_yaml_fallback(self):
        self.assertEqual(self.mod.serialise_val(True, "flag"), "true")


@unittest.skipUnless(HAS_DEPS, "PyYAML and requests are required to load action_update_dsom.py")
class ReadFileAndStripBomTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod = _load_module()

    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.tmp_dir.cleanup()

    def _write(self, name, content, encoding="utf-8"):
        path = os.path.join(self.tmp_dir.name, name)
        with open(path, "w", encoding=encoding) as f:
            f.write(content)
        return path

    def test_file_without_bom(self):
        path = self._write("no_bom.dsom", "---\ntype: dsom_state\n---\nbody\n")
        content, had_bom = self.mod.read_file_and_strip_bom(path)
        self.assertFalse(had_bom)
        self.assertEqual(content, "---\ntype: dsom_state\n---\nbody\n")

    def test_file_with_bom_is_detected_and_stripped(self):
        path = self._write("bom.dsom", "---\ntype: dsom_state\n---\nbody\n", encoding="utf-8-sig")
        content, had_bom = self.mod.read_file_and_strip_bom(path)
        self.assertTrue(had_bom)
        self.assertNotIn("\ufeff", content)
        self.assertTrue(content.startswith("---\n"))

    def test_missing_file_raises(self):
        missing = os.path.join(self.tmp_dir.name, "does_not_exist.dsom")
        with self.assertRaises(FileNotFoundError):
            self.mod.read_file_and_strip_bom(missing)


@unittest.skipUnless(HAS_DEPS, "PyYAML and requests are required to load action_update_dsom.py")
class ParseFrontmatterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod = _load_module()

    def test_single_frontmatter_block(self):
        content = "---\nokf_version: 0.1\ntype: dsom_state\n---\n# Body\ntext\n"
        frontmatter, rest = self.mod.parse_frontmatter(content, "current_state.dsom")
        self.assertEqual(frontmatter, {"okf_version": 0.1, "type": "dsom_state"})
        self.assertEqual(rest, "# Body\ntext\n")

    def test_no_frontmatter_returns_empty_dict_and_full_content(self):
        content = "# Just a heading\nNo frontmatter here.\n"
        frontmatter, rest = self.mod.parse_frontmatter(content, "x.dsom")
        self.assertEqual(frontmatter, {})
        self.assertEqual(rest, content)

    def test_multiple_consecutive_blocks_merge_with_later_taking_precedence(self):
        content = (
            "---\ntitle: First\ntopics: [a]\n---\n"
            "---\ntitle: Second\n---\n"
            "# Body\n"
        )
        frontmatter, rest = self.mod.parse_frontmatter(content, "x.dsom")
        self.assertEqual(frontmatter, {"title": "Second", "topics": ["a"]})
        self.assertEqual(rest, "# Body\n")

    def test_empty_frontmatter_block_parses_as_empty_dict(self):
        content = "---\n---\nBody text\n"
        frontmatter, rest = self.mod.parse_frontmatter(content, "x.dsom")
        self.assertEqual(frontmatter, {})
        self.assertEqual(rest, "Body text\n")

    def test_crlf_frontmatter_is_supported(self):
        content = "---\r\ntitle: CRLF\r\n---\r\nBody\r\n"
        frontmatter, rest = self.mod.parse_frontmatter(content, "x.dsom")
        self.assertEqual(frontmatter.get("title"), "CRLF")

    def test_non_mapping_frontmatter_raises_value_error(self):
        content = "---\n- a\n- b\n---\nBody\n"
        with self.assertRaises(ValueError):
            self.mod.parse_frontmatter(content, "bad.dsom")

    def test_malformed_yaml_raises_value_error_with_context(self):
        content = "---\nkey: [unterminated\n---\nBody\n"
        with self.assertRaises(ValueError) as ctx:
            self.mod.parse_frontmatter(content, "bad.dsom")
        self.assertIn("bad.dsom", str(ctx.exception))

    def test_custom_loader_keeps_timestamp_like_strings_as_strings(self):
        # Regression guard: an *unquoted* ISO-8601-looking value must not be
        # auto-parsed into a datetime.date/datetime object by the loader
        # used here, otherwise downstream str-only logic would break.
        content = "---\ntimestamp: 2026-08-11T13:40:00Z\n---\nBody\n"
        frontmatter, _ = self.mod.parse_frontmatter(content, "x.dsom")
        self.assertIsInstance(frontmatter["timestamp"], str)
        self.assertEqual(frontmatter["timestamp"], "2026-08-11T13:40:00Z")


@unittest.skipUnless(HAS_DEPS, "PyYAML and requests are required to load action_update_dsom.py")
class NormaliseMetadataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod = _load_module()

    TIMESTAMP_RE_SOURCE = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$"

    def test_defaults_applied_when_frontmatter_empty(self):
        result = self.mod.normalise_metadata({}, "current_state.dsom", "current_state.dsom")
        self.assertEqual(result["okf_version"], 0.1)
        self.assertEqual(result["type"], "dsom_state")
        self.assertEqual(result["title"], "DSOM Current State")
        self.assertEqual(result["topics"], ["state", "memory", "compaction"])
        self.assertRegex(result["timestamp"], self.TIMESTAMP_RE_SOURCE)

    def test_existing_values_are_preserved(self):
        existing = {
            "okf_version": 0.2,
            "type": "custom_type",
            "title": "Custom Title",
            "topics": ["custom"],
        }
        result = self.mod.normalise_metadata(existing, "x.dsom", "x.dsom")
        self.assertEqual(result["okf_version"], 0.2)
        self.assertEqual(result["type"], "custom_type")
        self.assertEqual(result["title"], "Custom Title")
        self.assertEqual(result["topics"], ["custom"])

    def test_timestamp_is_always_refreshed_not_preserved(self):
        existing = {"timestamp": "2000-01-01T00:00:00Z"}
        result = self.mod.normalise_metadata(existing, "x.dsom", "x.dsom")
        self.assertNotEqual(result["timestamp"], "2000-01-01T00:00:00Z")
        self.assertRegex(result["timestamp"], self.TIMESTAMP_RE_SOURCE)

    def test_timestamp_is_close_to_current_utc_time(self):
        before = datetime.datetime.now(datetime.timezone.utc)
        result = self.mod.normalise_metadata({}, "x.dsom", "x.dsom")
        after = datetime.datetime.now(datetime.timezone.utc)
        parsed = datetime.datetime.strptime(
            result["timestamp"], "%Y-%m-%dT%H:%M:%SZ"
        ).replace(tzinfo=datetime.timezone.utc)
        self.assertGreaterEqual(parsed, before - datetime.timedelta(seconds=2))
        self.assertLessEqual(parsed, after + datetime.timedelta(seconds=2))

    def test_extra_fields_are_preserved(self):
        existing = {"description": "A description.", "custom_field": "value"}
        result = self.mod.normalise_metadata(existing, "x.dsom", "x.dsom")
        self.assertEqual(result["description"], "A description.")
        self.assertEqual(result["custom_field"], "value")

    def test_standard_keys_come_before_extra_fields_in_result_order(self):
        existing = {"description": "desc"}
        result = self.mod.normalise_metadata(existing, "x.dsom", "x.dsom")
        keys = list(result.keys())
        self.assertEqual(keys[:5], ["okf_version", "type", "title", "timestamp", "topics"])
        self.assertIn("description", keys[5:])


@unittest.skipUnless(HAS_DEPS, "PyYAML and requests are required to load action_update_dsom.py")
class SerialiseFrontmatterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod = _load_module()

    def test_output_wrapped_in_fence_lines(self):
        result = self.mod.serialise_frontmatter(
            {"okf_version": 0.1, "type": "dsom_state", "title": "T", "timestamp": "2026-08-11T13:40:00Z", "topics": ["a"]},
            "current_state.dsom",
        )
        self.assertTrue(result.startswith("---\n"))
        self.assertTrue(result.endswith("---\n"))

    def test_standard_keys_ordered_before_extra_keys(self):
        metadata = {
            "description": "desc",
            "okf_version": 0.1,
            "topics": ["a"],
            "type": "dsom_state",
            "title": "T",
            "timestamp": "2026-08-11T13:40:00Z",
        }
        result = self.mod.serialise_frontmatter(metadata, "x.dsom")
        lines = [line for line in result.splitlines() if line and line != "---"]
        keys_in_order = [line.split(":", 1)[0] for line in lines]
        self.assertEqual(
            keys_in_order,
            ["okf_version", "type", "title", "timestamp", "topics", "description"],
        )

    def test_values_are_serialised_via_serialise_val(self):
        metadata = {
            "okf_version": 0.1,
            "type": "dsom_state",
            "title": "DSOM Current State",
            "timestamp": "2026-08-11T13:40:00Z",
            "topics": ["state", "memory"],
        }
        result = self.mod.serialise_frontmatter(metadata, "x.dsom")
        self.assertIn('timestamp: "2026-08-11T13:40:00Z"', result)
        self.assertIn('topics: ["state", "memory"]', result)
        self.assertIn("type: dsom_state", result)

    def test_result_frontmatter_block_round_trips_through_yaml(self):
        metadata = {
            "okf_version": 0.1,
            "type": "dsom_state",
            "title": "DSOM Current State",
            "timestamp": "2026-08-11T13:40:00Z",
            "topics": ["state", "memory", "compaction"],
            "description": "A description with: a colon.",
        }
        result = self.mod.serialise_frontmatter(metadata, "x.dsom")
        inner = result[len("---\n"):-len("---\n")]
        parsed = yaml.safe_load(inner)
        self.assertEqual(parsed["topics"], ["state", "memory", "compaction"])
        self.assertEqual(parsed["timestamp"], "2026-08-11T13:40:00Z")
        self.assertEqual(parsed["description"], "A description with: a colon.")


@unittest.skipUnless(HAS_DEPS, "PyYAML and requests are required to load action_update_dsom.py")
class AtomicReplaceFileTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod = _load_module()

    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.tmp_dir.cleanup()

    def test_creates_new_file_with_content(self):
        path = os.path.join(self.tmp_dir.name, "new_state.dsom")
        self.mod.atomic_replace_file(path, "hello world\n", "new_state.dsom")
        with open(path, "r", encoding="utf-8") as f:
            self.assertEqual(f.read(), "hello world\n")

    def test_overwrites_existing_file_content(self):
        path = os.path.join(self.tmp_dir.name, "state.dsom")
        with open(path, "w", encoding="utf-8") as f:
            f.write("old content\n")
        self.mod.atomic_replace_file(path, "new content\n", "state.dsom")
        with open(path, "r", encoding="utf-8") as f:
            self.assertEqual(f.read(), "new content\n")

    def test_preserves_existing_permission_mode(self):
        path = os.path.join(self.tmp_dir.name, "state.dsom")
        with open(path, "w", encoding="utf-8") as f:
            f.write("old content\n")
        original_mode = os.stat(path).st_mode
        target_mode = original_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
        os.chmod(path, target_mode)

        self.mod.atomic_replace_file(path, "new content\n", "state.dsom")

        resulting_mode = os.stat(path).st_mode
        if os.name != "nt":
            self.assertEqual(stat.S_IMODE(resulting_mode), stat.S_IMODE(target_mode))

    def test_no_leftover_temp_files_after_success(self):
        path = os.path.join(self.tmp_dir.name, "state.dsom")
        self.mod.atomic_replace_file(path, "content\n", "state.dsom")
        remaining = os.listdir(self.tmp_dir.name)
        self.assertEqual(remaining, ["state.dsom"])

    def test_temp_file_cleaned_up_on_replace_failure(self):
        path = os.path.join(self.tmp_dir.name, "state.dsom")
        with open(path, "w", encoding="utf-8") as f:
            f.write("old content\n")

        with mock.patch.object(self.mod.os, "replace", side_effect=OSError("boom")):
            with self.assertRaises(OSError):
                self.mod.atomic_replace_file(path, "new content\n", "state.dsom")

        # Original file must remain untouched, and no stray temp files left.
        with open(path, "r", encoding="utf-8") as f:
            self.assertEqual(f.read(), "old content\n")
        remaining = os.listdir(self.tmp_dir.name)
        self.assertEqual(remaining, ["state.dsom"])


@unittest.skipUnless(HAS_DEPS, "PyYAML and requests are required to load action_update_dsom.py")
class LocalCompactionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod = _load_module()

    def test_no_files_changed_produces_placeholder_message(self):
        result = self.mod.local_compaction("", "## Condensed History\n- old bullet\n")
        self.assertIn("No code files modified in diff.", result)

    def test_added_and_deleted_line_counts_are_tallied_per_file(self):
        diff_content = (
            "diff --git a/foo.py b/foo.py\n"
            "index 111..222 100644\n"
            "--- a/foo.py\n"
            "+++ b/foo.py\n"
            "+added line 1\n"
            "+added line 2\n"
            "-removed line 1\n"
        )
        result = self.mod.local_compaction(diff_content, "## Condensed History\n")
        self.assertIn("foo.py (+2, -1)", result)

    def test_multiple_files_are_all_summarised(self):
        diff_content = (
            "diff --git a/a.py b/a.py\n+x\n"
            "diff --git a/b.py b/b.py\n-y\n-z\n"
        )
        result = self.mod.local_compaction(diff_content, "## Condensed History\n")
        self.assertIn("a.py (+1, -0)", result)
        self.assertIn("b.py (+0, -2)", result)

    def test_plus_plus_plus_and_minus_minus_minus_headers_not_counted(self):
        diff_content = (
            "diff --git a/foo.py b/foo.py\n"
            "--- a/foo.py\n"
            "+++ b/foo.py\n"
        )
        result = self.mod.local_compaction(diff_content, "## Condensed History\n")
        self.assertIn("foo.py (+0, -0)", result)

    def test_bullet_inserted_immediately_before_existing_bullets(self):
        rest_of_content = (
            "# DSOM Current State\n\n"
            "## Condensed History\n\n"
            "- Existing bullet one.\n"
            "- Existing bullet two.\n\n"
            "## Archival Pointers\n"
        )
        diff_content = "diff --git a/x.py b/x.py\n+line\n"
        result = self.mod.local_compaction(diff_content, rest_of_content)
        lines = result.splitlines()
        auto_sync_idx = next(i for i, l in enumerate(lines) if l.startswith("- [Auto-Sync]"))
        existing_idx = next(i for i, l in enumerate(lines) if l == "- Existing bullet one.")
        self.assertLess(auto_sync_idx, existing_idx)
        self.assertIn("x.py (+1, -0)", lines[auto_sync_idx])

    def test_appends_new_section_when_heading_absent(self):
        rest_of_content = "# DSOM Current State\n\n## Active State\n- Something.\n"
        diff_content = "diff --git a/x.py b/x.py\n+line\n"
        result = self.mod.local_compaction(diff_content, rest_of_content)
        self.assertIn("## Condensed History", result)
        self.assertIn("- [Auto-Sync] Modified files: x.py (+1, -0).", result)
        # Original content must be preserved.
        self.assertIn("## Active State\n- Something.", result)

    def test_summary_message_uses_auto_sync_prefix(self):
        result = self.mod.local_compaction(
            "diff --git a/x.py b/x.py\n+a\n", "## Condensed History\n"
        )
        self.assertIn("[Auto-Sync]", result)


@unittest.skipUnless(HAS_DEPS, "PyYAML and requests are required to load action_update_dsom.py")
class MainFunctionTests(unittest.TestCase):
    """Integration-style tests exercising main() end-to-end."""

    @classmethod
    def setUpClass(cls):
        cls.mod = _load_module()

    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.diff_path = os.path.join(self.tmp_dir.name, "pr.diff")
        self.state_path = os.path.join(self.tmp_dir.name, "current_state.dsom")

        with open(self.diff_path, "w", encoding="utf-8") as f:
            f.write("diff --git a/foo.py b/foo.py\n+added line\n-removed line\n")

        with open(self.state_path, "w", encoding="utf-8") as f:
            f.write(
                "---\n"
                "okf_version: 0.1\n"
                "type: dsom_state\n"
                'title: "DSOM Current State"\n'
                'timestamp: "2000-01-01T00:00:00Z"\n'
                'topics: ["state", "memory", "compaction"]\n'
                'description: "A test description."\n'
                "---\n"
                "# DSOM Current State\n\n"
                "## Active State\n"
                "- Existing state.\n\n"
                "## Condensed History\n\n"
                "- Existing history bullet.\n"
            )

    def tearDown(self):
        self.tmp_dir.cleanup()

    def _run_main(self, argv, env=None, clear_env=True):
        base_env = {} if clear_env else dict(os.environ)
        if env:
            base_env.update(env)
        with mock.patch.object(sys, "argv", argv), mock.patch.dict(
            self.mod.os.environ, base_env, clear=clear_env
        ):
            self.mod.main()

    def test_wrong_number_of_args_exits_with_error(self):
        with mock.patch.object(sys, "argv", ["action_update_dsom.py", "only_one_arg"]):
            with self.assertRaises(SystemExit) as ctx:
                self.mod.main()
        self.assertEqual(ctx.exception.code, 1)

    def test_missing_state_file_exits_with_error(self):
        missing_state = os.path.join(self.tmp_dir.name, "does_not_exist.dsom")
        with mock.patch.object(
            sys, "argv", ["action_update_dsom.py", self.diff_path, missing_state]
        ):
            with self.assertRaises(SystemExit) as ctx:
                self.mod.main()
        self.assertEqual(ctx.exception.code, 1)

    def test_falls_back_to_local_compaction_when_no_api_key(self):
        self._run_main(["action_update_dsom.py", self.diff_path, self.state_path])

        with open(self.state_path, "r", encoding="utf-8") as f:
            new_content = f.read()

        self.assertIn("[Auto-Sync] Modified files: foo.py (+1, -1).", new_content)
        self.assertIn("- Existing history bullet.", new_content)
        self.assertIn("- Existing state.", new_content)
        # Frontmatter fields preserved, but the timestamp must have been refreshed.
        self.assertIn('description: "A test description."', new_content)
        self.assertNotIn("2000-01-01T00:00:00Z", new_content)

    def test_output_has_no_bom_and_single_frontmatter_block(self):
        self._run_main(["action_update_dsom.py", self.diff_path, self.state_path])
        with open(self.state_path, "rb") as f:
            raw = f.read()
        self.assertFalse(raw.startswith(b"\xef\xbb\xbf"))
        text = raw.decode("utf-8")
        self.assertEqual(text.count("---\n"), 2)

    def test_uses_gemini_api_when_api_key_present(self):
        fake_response = mock.Mock()
        fake_response.raise_for_status = mock.Mock()
        fake_response.json.return_value = {
            "candidates": [
                {"content": {"parts": [{"text": "# DSOM Current State\n\nAI-GENERATED BODY\n"}]}}
            ]
        }

        with mock.patch.object(self.mod.requests, "post", return_value=fake_response) as mock_post:
            self._run_main(
                ["action_update_dsom.py", self.diff_path, self.state_path],
                env={"GEMINI_API_KEY": "fake-key"},
            )

        mock_post.assert_called_once()
        with open(self.state_path, "r", encoding="utf-8") as f:
            new_content = f.read()
        self.assertIn("AI-GENERATED BODY", new_content)
        self.assertNotIn("[Auto-Sync]", new_content)

    def test_api_key_url_and_payload_use_configured_key(self):
        fake_response = mock.Mock()
        fake_response.raise_for_status = mock.Mock()
        fake_response.json.return_value = {
            "candidates": [{"content": {"parts": [{"text": "Body\n"}]}}]
        }

        with mock.patch.object(self.mod.requests, "post", return_value=fake_response) as mock_post:
            self._run_main(
                ["action_update_dsom.py", self.diff_path, self.state_path],
                env={"GOOGLE_API_KEY": "another-fake-key"},
            )

        called_url = mock_post.call_args.args[0]
        self.assertIn("another-fake-key", called_url)
        self.assertIn("generativelanguage.googleapis.com", called_url)

    def test_default_active_agent_uses_jules_persona(self):
        fake_response = mock.Mock()
        fake_response.raise_for_status = mock.Mock()
        fake_response.json.return_value = {
            "candidates": [{"content": {"parts": [{"text": "Body\n"}]}}]
        }

        with mock.patch.object(self.mod.requests, "post", return_value=fake_response) as mock_post:
            self._run_main(
                ["action_update_dsom.py", self.diff_path, self.state_path],
                env={"GEMINI_API_KEY": "fake-key"},
            )

        payload = mock_post.call_args.kwargs["json"]
        prompt_text = payload["contents"][0]["parts"][0]["text"]
        self.assertIn("Google Jules", prompt_text)
        self.assertNotIn("Google Antigravity", prompt_text)

    def test_active_agent_antigravity_uses_antigravity_persona(self):
        fake_response = mock.Mock()
        fake_response.raise_for_status = mock.Mock()
        fake_response.json.return_value = {
            "candidates": [{"content": {"parts": [{"text": "Body\n"}]}}]
        }

        with mock.patch.object(self.mod.requests, "post", return_value=fake_response) as mock_post:
            self._run_main(
                ["action_update_dsom.py", self.diff_path, self.state_path],
                env={"GEMINI_API_KEY": "fake-key", "ACTIVE_AGENT": "Antigravity"},
            )

        payload = mock_post.call_args.kwargs["json"]
        prompt_text = payload["contents"][0]["parts"][0]["text"]
        self.assertIn("Google Antigravity", prompt_text)

    def test_ai_response_wrapped_in_markdown_fence_is_unwrapped(self):
        fake_response = mock.Mock()
        fake_response.raise_for_status = mock.Mock()
        fake_response.json.return_value = {
            "candidates": [
                {
                    "content": {
                        "parts": [
                            {"text": "```\n# DSOM Current State\n\nFenced Body\n```"}
                        ]
                    }
                }
            ]
        }

        with mock.patch.object(self.mod.requests, "post", return_value=fake_response):
            self._run_main(
                ["action_update_dsom.py", self.diff_path, self.state_path],
                env={"GEMINI_API_KEY": "fake-key"},
            )

        with open(self.state_path, "r", encoding="utf-8") as f:
            new_content = f.read()
        self.assertIn("Fenced Body", new_content)
        self.assertNotIn("```", new_content)

    def test_falls_back_to_local_compaction_on_api_exception(self):
        with mock.patch.object(
            self.mod.requests, "post", side_effect=Exception("network down")
        ):
            self._run_main(
                ["action_update_dsom.py", self.diff_path, self.state_path],
                env={"GEMINI_API_KEY": "fake-key"},
            )

        with open(self.state_path, "r", encoding="utf-8") as f:
            new_content = f.read()
        self.assertIn("[Auto-Sync] Modified files: foo.py (+1, -1).", new_content)

    def test_falls_back_to_local_compaction_when_api_response_malformed(self):
        fake_response = mock.Mock()
        fake_response.raise_for_status = mock.Mock()
        fake_response.json.return_value = {"unexpected": "shape"}

        with mock.patch.object(self.mod.requests, "post", return_value=fake_response):
            self._run_main(
                ["action_update_dsom.py", self.diff_path, self.state_path],
                env={"GEMINI_API_KEY": "fake-key"},
            )

        with open(self.state_path, "r", encoding="utf-8") as f:
            new_content = f.read()
        self.assertIn("[Auto-Sync]", new_content)

    def test_no_api_key_never_calls_requests_post(self):
        with mock.patch.object(self.mod.requests, "post") as mock_post:
            self._run_main(["action_update_dsom.py", self.diff_path, self.state_path])
        mock_post.assert_not_called()


if __name__ == "__main__":
    unittest.main()