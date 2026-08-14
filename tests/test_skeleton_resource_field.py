"""
Unit tests for the `resource:` frontmatter field of `openwiki/_skeleton.md`.

This PR updates the `resource:` URI in the committed `openwiki/_skeleton.md`
file from a stale, container-specific path (`file:///app/openwiki/_skeleton.md`)
to the actual absolute checkout path used to regenerate the file
(`file:///home/runner/work/deep-state-of-mind-for-my-ai/deep-state-of-mind-for-my-ai/openwiki/_skeleton.md`).

These tests validate that:
1. `openwiki/_skeleton.md` exists, is non-empty, and starts with a clean
   (BOM-free) OKF frontmatter fence.
2. The frontmatter block parses as valid YAML and contains every mandatory
   OKF field, including the new `resource` value.
3. The `resource` field is a well-formed, absolute `file://` URI that
   resolves to `openwiki/_skeleton.md`.
4. The `resource` field no longer references the stale `/app/` container
   path (regression guard against reverting this PR's change).
5. The other frontmatter fields (title, timestamp, topics, description,
   type, okf_version) and the document body were left untouched by this
   PR's single-line edit.
"""
import pathlib
import re
import unittest
from urllib.parse import urlparse

import yaml

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
SKELETON_PATH = REPO_ROOT / "openwiki" / "_skeleton.md"

FRONTMATTER_RE = re.compile(r"\A---\s*\r?\n(.*?)(?:\r?\n)?---\s*(?:\r?\n|\Z)", re.DOTALL)

OLD_STALE_RESOURCE_URI = "file:///app/openwiki/_skeleton.md"
EXPECTED_RESOURCE_URI = (
    "file:///home/runner/work/deep-state-of-mind-for-my-ai/"
    "deep-state-of-mind-for-my-ai/openwiki/_skeleton.md"
)


def _read_skeleton_text() -> str:
    return SKELETON_PATH.read_text(encoding="utf-8")


def _extract_frontmatter(content: str):
    """Return (raw_yaml_text, parsed_mapping) for the leading frontmatter block."""
    match = FRONTMATTER_RE.match(content)
    if not match:
        return None, None
    raw = match.group(1)
    return raw, yaml.safe_load(raw)


class SkeletonFileExistenceTests(unittest.TestCase):
    """Basic sanity checks on the file touched by this PR."""

    def test_skeleton_file_exists(self):
        self.assertTrue(SKELETON_PATH.is_file())

    def test_skeleton_file_is_non_empty(self):
        content = _read_skeleton_text()
        self.assertTrue(content.strip())

    def test_skeleton_has_no_leading_bom(self):
        raw_bytes = SKELETON_PATH.read_bytes()
        self.assertFalse(raw_bytes.startswith(b"\xef\xbb\xbf"))

    def test_skeleton_starts_with_frontmatter_fence(self):
        content = _read_skeleton_text()
        self.assertTrue(content.startswith("---\n"))


class SkeletonFrontmatterParsingTests(unittest.TestCase):
    """Frontmatter must remain valid OKF YAML after this PR's edit."""

    def test_frontmatter_block_is_present(self):
        content = _read_skeleton_text()
        raw, parsed = _extract_frontmatter(content)
        self.assertIsNotNone(raw)
        self.assertIsInstance(parsed, dict)

    def test_frontmatter_contains_all_mandatory_okf_fields(self):
        content = _read_skeleton_text()
        _, parsed = _extract_frontmatter(content)
        for field in (
            "okf_version",
            "type",
            "title",
            "timestamp",
            "topics",
            "description",
            "resource",
        ):
            with self.subTest(field=field):
                self.assertIn(field, parsed)

    def test_untouched_fields_retain_expected_values(self):
        # Only `resource:` changed in this PR; every other field must be
        # exactly as it was before.
        content = _read_skeleton_text()
        _, parsed = _extract_frontmatter(content)
        self.assertEqual(parsed["okf_version"], "0.1")
        self.assertEqual(parsed["type"], "documentation")
        self.assertEqual(
            parsed["title"], "OpenWiki Documentation Skeleton & Subsystem Index"
        )
        self.assertEqual(parsed["topics"], ["openwiki", "skeleton", "dsom", "inventory"])
        self.assertEqual(
            parsed["description"],
            "Authoritative inventory ranking, planned page tree, and evidence "
            "briefs for the DSOM codebase.",
        )

    def test_timestamp_is_a_quoted_iso_string(self):
        content = _read_skeleton_text()
        _, parsed = _extract_frontmatter(content)
        self.assertIsInstance(parsed["timestamp"], str)
        self.assertTrue(parsed["timestamp"].endswith("Z"))
        self.assertIn("T", parsed["timestamp"])


class SkeletonResourceFieldTests(unittest.TestCase):
    """Targeted tests for the `resource:` value changed by this PR."""

    def test_resource_field_matches_committed_pr_value(self):
        # Regression/snapshot check pinned directly to this PR's diff.
        content = _read_skeleton_text()
        _, parsed = _extract_frontmatter(content)
        self.assertEqual(parsed["resource"], EXPECTED_RESOURCE_URI)

    def test_resource_field_is_not_the_stale_app_path(self):
        # Guards against reverting to the old, container-specific path.
        content = _read_skeleton_text()
        _, parsed = _extract_frontmatter(content)
        self.assertNotEqual(parsed["resource"], OLD_STALE_RESOURCE_URI)
        self.assertNotIn("file:///app/", content)

    def test_resource_field_is_a_valid_absolute_file_uri(self):
        content = _read_skeleton_text()
        _, parsed = _extract_frontmatter(content)
        resource = parsed["resource"]
        parsed_uri = urlparse(resource)
        self.assertEqual(parsed_uri.scheme, "file")
        self.assertTrue(parsed_uri.path.startswith("/"))

    def test_resource_field_resolves_to_skeleton_md_under_openwiki_dir(self):
        content = _read_skeleton_text()
        _, parsed = _extract_frontmatter(content)
        resource_path = pathlib.PurePosixPath(urlparse(parsed["resource"]).path)
        self.assertEqual(resource_path.name, "_skeleton.md")
        self.assertEqual(resource_path.parent.name, "openwiki")

    def test_resource_field_ends_with_expected_relative_suffix(self):
        content = _read_skeleton_text()
        _, parsed = _extract_frontmatter(content)
        self.assertTrue(parsed["resource"].endswith("openwiki/_skeleton.md"))

    def test_resource_field_is_double_quoted_in_raw_yaml(self):
        # Confirms the value is emitted the same way generate_skeleton()
        # in tools/openwiki_emulator.py formats it (a quoted YAML string).
        content = _read_skeleton_text()
        raw, _ = _extract_frontmatter(content)
        self.assertIn(f'resource: "{EXPECTED_RESOURCE_URI}"', raw)


class SkeletonBodyUnaffectedTests(unittest.TestCase):
    """The PR only touched frontmatter; the Markdown body must be intact."""

    def test_body_heading_immediately_follows_frontmatter(self):
        content = _read_skeleton_text()
        match = FRONTMATTER_RE.match(content)
        self.assertIsNotNone(match)
        remainder = content[match.end():]
        self.assertTrue(remainder.startswith("# OpenWiki documentation skeleton"))

    def test_body_still_contains_expected_sections(self):
        content = _read_skeleton_text()
        for heading in (
            "## Inventory and ranking",
            "## Planned tree",
            "## Evidence briefs completed before drafting",
            "## Critic TODO ledger",
        ):
            with self.subTest(heading=heading):
                self.assertIn(heading, content)


if __name__ == "__main__":
    unittest.main()