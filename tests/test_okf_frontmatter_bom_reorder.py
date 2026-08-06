"""
Unit tests for the OKF frontmatter BOM/reordering changes applied to a batch
of `.agents/` brain documents by this PR.

This PR makes two related changes across a large batch of Markdown files
under `.agents/`:

1. **UTF-8 BOM prefix.** Every listed file's leading `---` frontmatter
   fence now begins with a UTF-8 byte-order-mark (``\\xef\\xbb\\xbf`` /
   ``\\ufeff``), e.g. ``---`` becomes ``\ufeff---``. Some
   `palace_update_proposal_*.md` files already carried a leading BOM before
   a bare `# ...` heading (no frontmatter at all); for those files the BOM
   now instead prefixes a newly-added frontmatter block.
2. **Field reordering / addition.** For files that already had OKF
   frontmatter, the `timestamp` and `topics` fields were moved so that they
   appear immediately after `title` and *before* `description`/`resource`
   (previously `timestamp` was the last field, after `description` and
   `resource`). For files that had no frontmatter at all
   (`palace_update_proposal_2026-07-17_0713.md` and six siblings), a new,
   minimal frontmatter block (`okf_version`, `type`, `title`, `timestamp`,
   `topics`) was prepended, with no `description`/`resource` fields.

These tests validate, for every file this PR touched:
    * the file exists and is non-empty;
    * it begins with a UTF-8 BOM immediately followed by the frontmatter
      fence;
    * the frontmatter block parses as valid YAML and is a mapping;
    * the mandatory OKF fields (`okf_version`, `type`, `title`, `timestamp`,
      `topics`) are present with the expected values;
    * `timestamp` and `topics` precede `description`/`resource` wherever the
      latter are present (regression guard against reverting the reorder);
    * the seven previously-frontmatter-less proposal files now have a
      *minimal* frontmatter block (no `description`/`resource`) directly
      followed by their original `# ... Palace Update Proposal` heading and
      unchanged body content (e.g. the `**Generated:**` line).
"""
import pathlib
import re
import unittest

import yaml  # type: ignore


def _find_repo_root(start: pathlib.Path) -> pathlib.Path:
    """Locate the repository root from a starting path."""
    current = start.resolve()
    for parent in [current, *current.parents]:
        if (parent / ".git").exists():
            return parent
    raise RuntimeError("Could not locate repository root (.git not found)")


REPO_ROOT = _find_repo_root(pathlib.Path(__file__).parent)

BOM = "\ufeff"
FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)


def _read_text_stripping_bom(path: pathlib.Path) -> str:
    """Read a file as UTF-8 text, transparently stripping a leading BOM."""
    return path.read_text(encoding="utf-8-sig")


def _read_raw_text(path: pathlib.Path) -> str:
    """Read a file as UTF-8 text, preserving any leading BOM character."""
    return path.read_text(encoding="utf-8")


def _extract_frontmatter_block(content_without_bom: str):
    """Return (raw_yaml_text, parsed_mapping) for the leading frontmatter."""
    match = FRONTMATTER_RE.match(content_without_bom)
    if not match:
        return None, None
    raw = match.group(1)
    return raw, yaml.safe_load(raw)


# ---------------------------------------------------------------------------
# Files that already had OKF frontmatter, and which gained a leading BOM
# plus a `timestamp`/`topics` reorder ahead of `description`/`resource`.
# (relative path, type, title, timestamp, topics, has_description, has_resource)
# ---------------------------------------------------------------------------
REORDERED_FRONTMATTER_FILES = [
    (
        ".agents/AGENTS.md",
        "documentation",
        "The Core AI Rulebook (DSOM)",
        "2026-08-05T21:59:00Z",
        ["dsom", "documentation"],
        True,
        True,
    ),
    (
        ".agents/brain/DSOM_TEMPLATE.md",
        "architecture_concept",
        "🧠 DSOM Session Log: [Insert Date/Task Name]",
        "2026-07-04T09:40:04Z",
        ["dsom", "brain", "concept"],
        True,
        True,
    ),
    (
        ".agents/brain/active_context_manifest.md",
        "active_context_manifest",
        "Active Context Manifest — Template",
        "2026-07-19T03:12:00Z",
        ["dsom", "documentation"],
        True,
        False,
    ),
    (
        ".agents/brain/implementation_plan.md",
        "architecture_concept",
        "🗺️ DSOM Implementation Plan",
        "2026-07-04T09:40:04Z",
        ["dsom", "brain", "concept"],
        True,
        True,
    ),
    (
        ".agents/brain/member/haris/walkthrough.md",
        "architecture_concept",
        "walkthrough",
        "2026-07-04T09:40:04Z",
        ["dsom", "brain", "concept"],
        True,
        True,
    ),
    (
        ".agents/brain/palace_registry.md",
        "architecture_concept",
        "🏛️ Palace Registry: Sovereign Retrieval Map",
        "2026-07-04T09:40:04Z",
        ["dsom", "brain", "concept"],
        True,
        True,
    ),
]

# The twelve palace_update_proposal_2026-04-08_* files all share the same
# type/title/timestamp/topics and the description+resource pattern.
_PALACE_0408_SUFFIXES = [
    "1214",
    "2154",
    "2156",
    "2242",
    "2250",
    "2252",
    "2301",
    "2315",
    "2320",
    "2323",
    "2326",
    "2327",
]
for _suffix in _PALACE_0408_SUFFIXES:
    REORDERED_FRONTMATTER_FILES.append(
        (
            f".agents/brain/palace_update_proposal_2026-04-08_{_suffix}.md",
            "architecture_concept",
            "🏛️ Palace Update Proposal",
            "2026-07-04T09:40:04Z",
            ["dsom", "brain", "concept"],
            True,
            True,
        )
    )

# ---------------------------------------------------------------------------
# Files that previously had NO frontmatter at all (just a leading BOM +
# bare heading) and gained a brand-new, minimal frontmatter block.
# (relative path, timestamp)
# ---------------------------------------------------------------------------
NEW_MINIMAL_FRONTMATTER_FILES = [
    (".agents/brain/palace_update_proposal_2026-07-17_0713.md", "2026-08-05T22:23:51Z"),
    (".agents/brain/palace_update_proposal_2026-07-17_0747.md", "2026-08-05T22:23:51Z"),
    (".agents/brain/palace_update_proposal_2026-07-17_0752.md", "2026-08-05T22:23:51Z"),
    (".agents/brain/palace_update_proposal_2026-07-18_2259.md", "2026-08-05T22:23:51Z"),
    (".agents/brain/palace_update_proposal_2026-07-19_1349.md", "2026-08-05T22:23:51Z"),
    (".agents/brain/palace_update_proposal_2026-07-26_0745.md", "2026-08-05T22:23:51Z"),
    (".agents/brain/palace_update_proposal_2026-07-26_0755.md", "2026-08-05T22:23:51Z"),
]

ALL_FILES_RELATIVE = [entry[0] for entry in REORDERED_FRONTMATTER_FILES] + [
    entry[0] for entry in NEW_MINIMAL_FRONTMATTER_FILES
]


class FrontmatterFileExistenceTests(unittest.TestCase):
    """All 25 files touched by this PR must exist and be non-empty."""

    def test_all_files_exist(self):
        for relative in ALL_FILES_RELATIVE:
            with self.subTest(path=relative):
                self.assertTrue(
                    (REPO_ROOT / relative).is_file(),
                    f"Expected {relative} to exist",
                )

    def test_no_duplicate_paths_in_test_fixture(self):
        # Sanity check on the test fixture itself: guards against a copy-paste
        # duplicate silently reducing effective coverage.
        self.assertEqual(len(ALL_FILES_RELATIVE), len(set(ALL_FILES_RELATIVE)))

    def test_expected_total_file_count(self):
        # 6 individually-named + 12 palace_update_proposal_2026-04-08_* +
        # 7 newly-frontmatter'd files == 25, matching the PR's file list.
        self.assertEqual(len(ALL_FILES_RELATIVE), 25)

    def test_all_files_non_empty(self):
        for relative in ALL_FILES_RELATIVE:
            with self.subTest(path=relative):
                content = _read_text_stripping_bom(REPO_ROOT / relative)
                self.assertTrue(content.strip(), f"{relative} should not be empty")


class LeadingBomTests(unittest.TestCase):
    """Every touched file must begin with a UTF-8 BOM immediately before ---."""

    def test_files_start_with_utf8_bom_bytes(self):
        for relative in ALL_FILES_RELATIVE:
            with self.subTest(path=relative):
                raw_bytes = (REPO_ROOT / relative).read_bytes()
                self.assertTrue(
                    raw_bytes.startswith(b"\xef\xbb\xbf"),
                    f"Expected {relative} to start with a UTF-8 BOM",
                )

    def test_files_start_with_bom_then_frontmatter_fence(self):
        for relative in ALL_FILES_RELATIVE:
            with self.subTest(path=relative):
                raw_text = _read_raw_text(REPO_ROOT / relative)
                self.assertTrue(
                    raw_text.startswith(BOM + "---\n"),
                    f"Expected {relative} to start with BOM + '---\\n'",
                )

    def test_bom_stripping_yields_bare_frontmatter_fence(self):
        for relative in ALL_FILES_RELATIVE:
            with self.subTest(path=relative):
                content = _read_text_stripping_bom(REPO_ROOT / relative)
                self.assertTrue(content.startswith("---\n"))
                self.assertFalse(content.startswith(BOM))

    def test_bom_appears_exactly_once_per_file(self):
        # Regression guard: the BOM must only be the encoding marker at the
        # very start of the file, not duplicated or reintroduced mid-file.
        for relative in ALL_FILES_RELATIVE:
            with self.subTest(path=relative):
                raw_text = _read_raw_text(REPO_ROOT / relative)
                self.assertEqual(raw_text.count(BOM), 1)


class FrontmatterParsesAsValidYamlTests(unittest.TestCase):
    """Every touched file's frontmatter block must parse as a YAML mapping."""

    def test_frontmatter_present_and_is_mapping(self):
        for relative in ALL_FILES_RELATIVE:
            with self.subTest(path=relative):
                content = _read_text_stripping_bom(REPO_ROOT / relative)
                _, parsed = _extract_frontmatter_block(content)
                self.assertIsNotNone(
                    parsed, f"Expected {relative} to have a parseable frontmatter block"
                )
                self.assertIsInstance(parsed, dict)


class ReorderedFrontmatterFieldTests(unittest.TestCase):
    """Field-value checks for files that already had OKF frontmatter."""

    def test_mandatory_fields_have_expected_values(self):
        for (
            relative,
            expected_type,
            expected_title,
            expected_timestamp,
            expected_topics,
            _has_description,
            _has_resource,
        ) in REORDERED_FRONTMATTER_FILES:
            with self.subTest(path=relative):
                content = _read_text_stripping_bom(REPO_ROOT / relative)
                _, parsed = _extract_frontmatter_block(content)
                self.assertEqual(parsed.get("okf_version"), 0.1)
                self.assertEqual(parsed.get("type"), expected_type)
                self.assertEqual(parsed.get("title"), expected_title)
                self.assertEqual(parsed.get("timestamp"), expected_timestamp)
                self.assertEqual(parsed.get("topics"), expected_topics)

    def test_description_and_resource_presence_matches_expectation(self):
        for (
            relative,
            _expected_type,
            _expected_title,
            _expected_timestamp,
            _expected_topics,
            has_description,
            has_resource,
        ) in REORDERED_FRONTMATTER_FILES:
            with self.subTest(path=relative):
                content = _read_text_stripping_bom(REPO_ROOT / relative)
                _, parsed = _extract_frontmatter_block(content)
                self.assertEqual("description" in parsed, has_description)
                self.assertEqual("resource" in parsed, has_resource)

    def test_timestamp_and_topics_precede_description_and_resource(self):
        # This is the crux of the reordering fix: timestamp/topics must now
        # come *before* description/resource in the raw frontmatter text,
        # not after (which was the pre-PR ordering).
        for (
            relative,
            _expected_type,
            _expected_title,
            _expected_timestamp,
            _expected_topics,
            has_description,
            has_resource,
        ) in REORDERED_FRONTMATTER_FILES:
            with self.subTest(path=relative):
                content = _read_text_stripping_bom(REPO_ROOT / relative)
                raw, _ = _extract_frontmatter_block(content)
                timestamp_index = raw.index("timestamp:")
                topics_index = raw.index("topics:")
                self.assertLess(
                    timestamp_index,
                    topics_index,
                    f"Expected 'timestamp:' before 'topics:' in {relative}",
                )
                if has_description:
                    description_index = raw.index("description:")
                    self.assertLess(
                        topics_index,
                        description_index,
                        f"Expected 'topics:' before 'description:' in {relative}",
                    )
                if has_resource:
                    resource_index = raw.index("resource:")
                    self.assertLess(
                        topics_index,
                        resource_index,
                        f"Expected 'topics:' before 'resource:' in {relative}",
                    )

    def test_first_three_keys_are_okf_version_type_title(self):
        # okf_version/type/title were never reordered; this pins down that
        # the reorder only affected timestamp/topics relative to
        # description/resource, not the leading trio.
        for (
            relative,
            _expected_type,
            _expected_title,
            _expected_timestamp,
            _expected_topics,
            _has_description,
            _has_resource,
        ) in REORDERED_FRONTMATTER_FILES:
            with self.subTest(path=relative):
                content = _read_text_stripping_bom(REPO_ROOT / relative)
                _, parsed = _extract_frontmatter_block(content)
                self.assertEqual(
                    list(parsed.keys())[:3], ["okf_version", "type", "title"]
                )

    def test_timestamp_values_are_quoted_strings_not_bare_datetimes(self):
        # Quoting matters: an unquoted "2026-07-04T09:40:04Z" would be
        # auto-parsed by YAML into a datetime.datetime object instead of a
        # plain string, which downstream OKF tooling expects.
        for (
            relative,
            _expected_type,
            _expected_title,
            _expected_timestamp,
            _expected_topics,
            _has_description,
            _has_resource,
        ) in REORDERED_FRONTMATTER_FILES:
            with self.subTest(path=relative):
                content = _read_text_stripping_bom(REPO_ROOT / relative)
                _, parsed = _extract_frontmatter_block(content)
                self.assertIsInstance(parsed.get("timestamp"), str)


class NewMinimalFrontmatterFilesTests(unittest.TestCase):
    """Checks for the seven files that gained frontmatter for the first time."""

    def test_mandatory_fields_have_expected_values(self):
        for relative, expected_timestamp in NEW_MINIMAL_FRONTMATTER_FILES:
            with self.subTest(path=relative):
                content = _read_text_stripping_bom(REPO_ROOT / relative)
                _, parsed = _extract_frontmatter_block(content)
                self.assertEqual(parsed.get("okf_version"), 0.1)
                self.assertEqual(parsed.get("type"), "architecture_concept")
                self.assertEqual(parsed.get("title"), "🏛️ Palace Update Proposal")
                self.assertEqual(parsed.get("timestamp"), expected_timestamp)
                self.assertEqual(parsed.get("topics"), ["dsom", "brain", "concept"])

    def test_frontmatter_is_minimal_no_description_or_resource(self):
        for relative, _expected_timestamp in NEW_MINIMAL_FRONTMATTER_FILES:
            with self.subTest(path=relative):
                content = _read_text_stripping_bom(REPO_ROOT / relative)
                _, parsed = _extract_frontmatter_block(content)
                self.assertNotIn("description", parsed)
                self.assertNotIn("resource", parsed)
                self.assertEqual(
                    set(parsed.keys()),
                    {"okf_version", "type", "title", "timestamp", "topics"},
                )

    def test_frontmatter_immediately_followed_by_original_heading(self):
        for relative, _expected_timestamp in NEW_MINIMAL_FRONTMATTER_FILES:
            with self.subTest(path=relative):
                content = _read_text_stripping_bom(REPO_ROOT / relative)
                match = FRONTMATTER_RE.match(content)
                self.assertIsNotNone(match)
                remainder = content[match.end():]
                self.assertTrue(
                    remainder.startswith("# 🏛️ Palace Update Proposal"),
                    f"Expected {relative} body to start with the original heading "
                    f"immediately after frontmatter",
                )

    def test_generated_line_date_matches_filename_suffix(self):
        # Regression guard: adding frontmatter must not have disturbed the
        # existing body content, in particular the per-file "Generated:"
        # timestamp that is embedded in the filename itself.
        for relative, _expected_timestamp in NEW_MINIMAL_FRONTMATTER_FILES:
            with self.subTest(path=relative):
                filename = pathlib.Path(relative).stem
                # e.g. "palace_update_proposal_2026-07-17_0713" -> "2026-07-17_0713"
                suffix = filename.replace("palace_update_proposal_", "")
                content = _read_text_stripping_bom(REPO_ROOT / relative)
                self.assertIn(f"> **Generated:** {suffix}", content)

    def test_body_still_declares_eod_mode_and_pending_review_status(self):
        for relative, _expected_timestamp in NEW_MINIMAL_FRONTMATTER_FILES:
            with self.subTest(path=relative):
                content = _read_text_stripping_bom(REPO_ROOT / relative)
                self.assertIn("> **Mode:** EOD", content)
                self.assertIn(
                    "> **Status:** PENDING AI REVIEW — Do not commit until closets are updated.",
                    content,
                )


class ActiveContextManifestRegressionTests(unittest.TestCase):
    """Specific regression checks for active_context_manifest.md.

    Alongside the BOM/reorder, this file also lost the blank line that
    previously separated the closing frontmatter fence from the
    `# Active Context Manifest` heading.
    """

    PATH = REPO_ROOT / ".agents" / "brain" / "active_context_manifest.md"

    def test_no_blank_line_between_frontmatter_and_heading(self):
        content = _read_text_stripping_bom(self.PATH)
        match = FRONTMATTER_RE.match(content)
        self.assertIsNotNone(match)
        remainder = content[match.end():]
        self.assertTrue(
            remainder.startswith("# Active Context Manifest"),
            "Expected the heading to directly follow the frontmatter fence "
            "with no intervening blank line",
        )

    def test_usage_note_still_present_after_heading(self):
        content = _read_text_stripping_bom(self.PATH)
        self.assertIn(
            "> **Usage:** Update this file at the start of each session (SOD ritual).",
            content,
        )

    def test_timestamp_no_longer_has_utc_offset_suffix(self):
        # Pre-PR the timestamp carried a "+08:00" offset; the PR normalises
        # it to a bare "Z"-suffixed UTC timestamp string.
        content = _read_text_stripping_bom(self.PATH)
        _, parsed = _extract_frontmatter_block(content)
        self.assertEqual(parsed.get("timestamp"), "2026-07-19T03:12:00Z")
        self.assertNotIn("+08:00", content)


class WalkthroughMemberRegressionTests(unittest.TestCase):
    """Specific regression checks for .agents/brain/member/haris/walkthrough.md."""

    PATH = REPO_ROOT / ".agents" / "brain" / "member" / "haris" / "walkthrough.md"

    def test_body_content_unaffected_by_frontmatter_reorder(self):
        content = _read_text_stripping_bom(self.PATH)
        self.assertIn("## [2026-01-27] | Engine Telemetry", content)
        self.assertIn("- Model: Gemini 1.5 Flash (Free Tier).", content)

    def test_title_field_is_plain_lowercase_walkthrough(self):
        content = _read_text_stripping_bom(self.PATH)
        _, parsed = _extract_frontmatter_block(content)
        self.assertEqual(parsed.get("title"), "walkthrough")


class TopicsFieldShapeTests(unittest.TestCase):
    """Structural sanity checks on the `topics` field across all files."""

    def test_topics_is_always_a_non_empty_list_of_strings(self):
        for relative in ALL_FILES_RELATIVE:
            with self.subTest(path=relative):
                content = _read_text_stripping_bom(REPO_ROOT / relative)
                _, parsed = _extract_frontmatter_block(content)
                topics = parsed.get("topics")
                self.assertIsInstance(topics, list)
                self.assertTrue(topics)
                for topic in topics:
                    self.assertIsInstance(topic, str)

    def test_dsom_topic_present_in_every_file(self):
        for relative in ALL_FILES_RELATIVE:
            with self.subTest(path=relative):
                content = _read_text_stripping_bom(REPO_ROOT / relative)
                _, parsed = _extract_frontmatter_block(content)
                self.assertIn("dsom", parsed.get("topics", []))


if __name__ == "__main__":
    unittest.main()