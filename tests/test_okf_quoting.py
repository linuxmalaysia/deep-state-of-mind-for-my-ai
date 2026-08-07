"""
Unit tests for the OKF frontmatter quoting changes introduced by this PR.

This PR updates `tools/apply_okf_frontmatter.py` (and its mirror in
`.agents/skills/okf-frontmatter-injector/scripts/apply_okf.py`) so that:

1. `needs_double_quotes()` flags any string containing non-ASCII characters
   (e.g. emoji) or "special" characters (colons, brackets, parentheses, etc.)
   as requiring double-quoting in the emitted YAML frontmatter.
2. `serialize_val()` renders list values as inline JSON-style arrays with
   every string element double-quoted (e.g. `["dsom", "documentation"]`),
   and renders scalar string values either bare or double-quoted depending
   on `needs_double_quotes()`.
3. `process_file()` now writes the updated file using plain `utf-8` encoding
   (rather than `utf-8-sig`), so no BOM is ever (re-)introduced on write,
   even if the original file had one.

These tests exercise the two new/rewritten helper functions directly and
also exercise `process_file()` end-to-end against temporary files to confirm
the on-disk output matches the new quoting/encoding behaviour.
"""
import json
import os
import sys
import tempfile
import unittest

import yaml

# Add repo root to PYTHONPATH so `tools` is importable, matching the
# convention used by the existing OKF regression tests.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from tools.apply_okf_frontmatter import needs_double_quotes, serialize_val, process_file


class NeedsDoubleQuotesTests(unittest.TestCase):
    def test_plain_alphanumeric_string_does_not_need_quotes(self):
        self.assertFalse(needs_double_quotes("documentation"))

    def test_string_with_spaces_underscores_and_hyphens_does_not_need_quotes(self):
        self.assertFalse(needs_double_quotes("Active Context Manifest_template-1"))

    def test_empty_string_does_not_need_quotes(self):
        self.assertFalse(needs_double_quotes(""))

    def test_string_with_emoji_needs_quotes(self):
        self.assertTrue(needs_double_quotes("🧠 Deep State of Mind (DSOM)"))

    def test_string_with_non_ascii_accented_character_needs_quotes(self):
        self.assertTrue(needs_double_quotes("Café"))

    def test_string_with_colon_needs_quotes(self):
        self.assertTrue(needs_double_quotes("Palace Registry: Sovereign Retrieval Map"))

    def test_string_with_square_brackets_needs_quotes(self):
        self.assertTrue(needs_double_quotes("[BUG] "))

    def test_string_with_parentheses_needs_quotes(self):
        self.assertTrue(needs_double_quotes("OPERATIONAL-GUIDE-PHP.md (Master v1.4)"))

    def test_string_with_em_dash_needs_quotes(self):
        self.assertTrue(needs_double_quotes("Active Context Manifest — Template"))

    def test_non_string_int_does_not_need_quotes(self):
        self.assertFalse(needs_double_quotes(42))

    def test_non_string_none_does_not_need_quotes(self):
        self.assertFalse(needs_double_quotes(None))

    def test_non_string_list_does_not_need_quotes(self):
        self.assertFalse(needs_double_quotes(["a", "b"]))

    def test_non_string_float_does_not_need_quotes(self):
        self.assertFalse(needs_double_quotes(0.1))


class SerializeValListTests(unittest.TestCase):
    def test_list_of_plain_strings_renders_as_inline_double_quoted_array(self):
        result = serialize_val(["dsom", "documentation"], "topics")
        self.assertEqual(result, '["dsom", "documentation"]')

    def test_empty_list_renders_as_empty_brackets(self):
        result = serialize_val([], "topics")
        self.assertEqual(result, "[]")

    def test_single_element_list(self):
        result = serialize_val(["dsom"], "topics")
        self.assertEqual(result, '["dsom"]')

    def test_list_with_special_characters_is_still_double_quoted(self):
        result = serialize_val(["git", "commit", "history"], "topics")
        self.assertEqual(result, '["git", "commit", "history"]')

    def test_list_result_is_valid_yaml_flow_sequence(self):
        result = serialize_val(["render", "deployment", "static-site"], "topics")
        parsed = yaml.safe_load(result)
        self.assertEqual(parsed, ["render", "deployment", "static-site"])

    def test_list_with_non_string_items_uses_str_conversion(self):
        result = serialize_val([1, 2, 3], "some_numeric_list")
        self.assertEqual(result, "[1, 2, 3]")

    def test_list_string_element_containing_double_quote_is_escaped(self):
        result = serialize_val(['say "hi"'], "topics")
        # json.dumps must escape the embedded double quote so the overall
        # YAML flow sequence remains parseable.
        parsed = yaml.safe_load(result)
        self.assertEqual(parsed, ['say "hi"'])


class SerializeValStringTests(unittest.TestCase):
    def test_plain_string_returned_unquoted(self):
        result = serialize_val("documentation", "type")
        self.assertEqual(result, "documentation")

    def test_string_with_emoji_is_double_quoted(self):
        result = serialize_val("🧠 DSOM Session Log: [Insert Date/Task Name]", "title")
        self.assertEqual(result, json.dumps("🧠 DSOM Session Log: [Insert Date/Task Name]", ensure_ascii=False))
        self.assertTrue(result.startswith('"') and result.endswith('"'))

    def test_timestamp_string_is_double_quoted(self):
        # Timestamps contain colons, so they always require quoting to avoid
        # ambiguity with YAML's own colon-based key/value syntax.
        result = serialize_val("2026-08-05T21:59:00Z", "timestamp")
        self.assertEqual(result, '"2026-08-05T21:59:00Z"')

    def test_quoted_string_round_trips_through_yaml(self):
        original = "Release Notes: v10.3.1-skills"
        result = serialize_val(original, "title")
        self.assertEqual(yaml.safe_load(result), original)

    def test_plain_string_round_trips_through_yaml(self):
        original = "walkthrough"
        result = serialize_val(original, "title")
        self.assertEqual(result, original)
        self.assertEqual(yaml.safe_load(result), original)


class SerializeValFallbackTests(unittest.TestCase):
    def test_float_uses_yaml_safe_dump_fallback(self):
        result = serialize_val(0.1, "okf_version")
        self.assertEqual(result, "0.1")

    def test_int_uses_yaml_safe_dump_fallback(self):
        result = serialize_val(1, "some_int_field")
        self.assertEqual(result, "1")

    def test_none_uses_yaml_safe_dump_fallback(self):
        result = serialize_val(None, "assignees")
        # PyYAML serializes None as "null" in safe_dump flow style.
        self.assertEqual(result, "null")


class ProcessFileQuotingIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.fd, self.path = tempfile.mkstemp(suffix=".md")
        os.close(self.fd)

    def tearDown(self):
        if os.path.exists(self.path):
            os.remove(self.path)

    def _write(self, content, encoding="utf-8"):
        with open(self.path, "w", encoding=encoding) as f:
            f.write(content)

    def _read_raw_bytes(self):
        with open(self.path, "rb") as f:
            return f.read()

    def _read_text(self):
        with open(self.path, "r", encoding="utf-8") as f:
            return f.read()

    def test_title_with_emoji_is_double_quoted_in_output(self):
        input_content = (
            "---\n"
            "okf_version: 0.1\n"
            "type: documentation\n"
            "title: 🧠 Deep State of Mind (DSOM)\n"
            "timestamp: '2026-07-04T09:40:04Z'\n"
            "topics: [dsom, documentation]\n"
            "---\n"
            "# 🧠 Deep State of Mind (DSOM)\n"
        )
        self._write(input_content)
        temp_dir = os.path.dirname(self.path)

        modified = process_file(self.path, temp_dir)
        self.assertTrue(modified)

        new_content = self._read_text()
        self.assertIn('title: "🧠 Deep State of Mind (DSOM)"', new_content)

    def test_topics_list_is_rendered_as_inline_double_quoted_array(self):
        input_content = (
            "---\n"
            "okf_version: 0.1\n"
            "type: documentation\n"
            "title: Plain Title\n"
            "timestamp: '2026-07-04T09:40:04Z'\n"
            "topics: [dsom, documentation]\n"
            "---\n"
            "# Plain Title\n"
        )
        self._write(input_content)
        temp_dir = os.path.dirname(self.path)

        process_file(self.path, temp_dir)

        new_content = self._read_text()
        self.assertIn('topics: ["dsom", "documentation"]', new_content)

    def test_timestamp_is_rendered_as_double_quoted_string(self):
        input_content = (
            "---\n"
            "okf_version: 0.1\n"
            "type: documentation\n"
            "title: Plain Title\n"
            "timestamp: '2026-07-04T09:40:04Z'\n"
            "topics: [dsom, documentation]\n"
            "---\n"
            "# Plain Title\n"
        )
        self._write(input_content)
        temp_dir = os.path.dirname(self.path)

        process_file(self.path, temp_dir)

        new_content = self._read_text()
        self.assertIn('timestamp: "2026-07-04T09:40:04Z"', new_content)

    def test_plain_ascii_title_remains_unquoted(self):
        input_content = (
            "---\n"
            "okf_version: 0.1\n"
            "type: documentation\n"
            "title: walkthrough\n"
            "timestamp: '2026-07-04T09:40:04Z'\n"
            "topics: [dsom, brain, concept]\n"
            "---\n"
            "# walkthrough\n"
        )
        self._write(input_content)
        temp_dir = os.path.dirname(self.path)

        process_file(self.path, temp_dir)

        new_content = self._read_text()
        self.assertIn("title: walkthrough\n", new_content)
        self.assertNotIn('title: "walkthrough"', new_content)

    def test_output_never_written_with_utf8_bom_even_if_input_had_one(self):
        input_content = (
            "---\n"
            "okf_version: 0.1\n"
            "type: documentation\n"
            "title: BOM Source File\n"
            "timestamp: '2026-07-04T09:40:04Z'\n"
            "topics: [dsom, documentation]\n"
            "---\n"
            "# BOM Source File\n"
        )
        # Write the source file WITH a UTF-8 BOM, simulating a legacy file.
        self._write(input_content, encoding="utf-8-sig")

        raw_before = self._read_raw_bytes()
        self.assertTrue(raw_before.startswith(b"\xef\xbb\xbf"))

        temp_dir = os.path.dirname(self.path)
        modified = process_file(self.path, temp_dir)
        self.assertTrue(modified)

        raw_after = self._read_raw_bytes()
        self.assertFalse(
            raw_after.startswith(b"\xef\xbb\xbf"),
            "process_file must not re-introduce a UTF-8 BOM on write",
        )
        self.assertTrue(raw_after.startswith(b"---\n"))

    def test_idempotent_on_second_run_after_quoting(self):
        input_content = (
            "---\n"
            "okf_version: 0.1\n"
            "type: documentation\n"
            "title: 🚀 Release Notes\n"
            "timestamp: '2026-07-04T09:40:04Z'\n"
            "topics: [dsom, documentation]\n"
            "---\n"
            "# 🚀 Release Notes\n"
        )
        self._write(input_content)
        temp_dir = os.path.dirname(self.path)

        first_modified = process_file(self.path, temp_dir)
        self.assertTrue(first_modified)
        content_after_first_run = self._read_text()

        second_modified = process_file(self.path, temp_dir)
        self.assertFalse(
            second_modified,
            "Re-running process_file on an already-quoted, compliant file "
            "should not report any further modification",
        )
        self.assertEqual(self._read_text(), content_after_first_run)

    def test_output_frontmatter_block_is_valid_yaml_after_quoting(self):
        input_content = (
            "---\n"
            "okf_version: 0.1\n"
            "type: documentation\n"
            "title: 🛡️ DSOM Sovereign Coding Instructions\n"
            "timestamp: '2026-07-04T09:40:04Z'\n"
            "topics: [dsom, documentation]\n"
            "description: OKF-compliant documentation for copilot-instructions.md.\n"
            "---\n"
            "# 🛡️ DSOM Sovereign Coding Instructions\n"
        )
        self._write(input_content)
        temp_dir = os.path.dirname(self.path)

        process_file(self.path, temp_dir)

        new_content = self._read_text()
        # Extract the single frontmatter block and confirm it still parses.
        parts = new_content.split("---")
        self.assertEqual(len(parts), 3)
        parsed = yaml.safe_load(parts[1])
        self.assertEqual(parsed["title"], "🛡️ DSOM Sovereign Coding Instructions")
        self.assertEqual(parsed["topics"], ["dsom", "documentation"])
        self.assertEqual(
            parsed["description"], "OKF-compliant documentation for copilot-instructions.md."
        )


if __name__ == "__main__":
    unittest.main()