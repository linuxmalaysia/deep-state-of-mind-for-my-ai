"""
Unit tests for the Read the Docs integration ledger/brain updates.

This PR:
1. Added OKF v0.1 YAML frontmatter to `.agents/brain/task.md` and
   `.agents/brain/walkthrough.md`, plus new checklist/session-anchor
   content describing the Read the Docs integration work.
2. Added a "Read the Docs Integration" entry to `CHANGELOG.md` under
   `## [Unreleased]` / `### Added`.
3. Added a dated `[2026-08-05]` entry to `HISTORY.md`.

These tests validate that the new content is present, well-formed
(valid YAML frontmatter), and correctly ordered relative to
pre-existing/neighbouring content.
"""
import pathlib
import re
import unittest

import yaml  # type: ignore


def _find_repo_root(start: pathlib.Path) -> pathlib.Path:
    current = start.resolve()
    for parent in [current, *current.parents]:
        if (parent / ".git").exists():
            return parent
    raise RuntimeError("Could not locate repository root (.git not found)")


REPO_ROOT = _find_repo_root(pathlib.Path(__file__).parent)
TASK_MD_PATH = REPO_ROOT / ".agents" / "brain" / "task.md"
WALKTHROUGH_MD_PATH = REPO_ROOT / ".agents" / "brain" / "walkthrough.md"
CHANGELOG_PATH = REPO_ROOT / "CHANGELOG.md"
HISTORY_PATH = REPO_ROOT / "HISTORY.md"

FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)


def _extract_frontmatter(content: str):
    """Parse the leading '---' YAML frontmatter block, if any."""
    match = FRONTMATTER_RE.match(content)
    if not match:
        return None
    return yaml.safe_load(match.group(1))


class TaskMdFrontmatterTests(unittest.TestCase):
    """Verify the new OKF frontmatter block in .agents/brain/task.md."""

    @classmethod
    def setUpClass(cls):
        cls.content = TASK_MD_PATH.read_text(encoding="utf-8-sig")
        cls.frontmatter = _extract_frontmatter(cls.content)

    def test_file_exists(self):
        self.assertTrue(TASK_MD_PATH.is_file())

    def test_frontmatter_present_and_parses(self):
        self.assertIsNotNone(self.frontmatter, "Expected a leading '---' YAML frontmatter block")
        self.assertIsInstance(self.frontmatter, dict)

    def test_frontmatter_fields(self):
        self.assertEqual(self.frontmatter.get("okf_version"), 0.1)
        self.assertEqual(self.frontmatter.get("type"), "task_ledger")
        self.assertEqual(self.frontmatter.get("title"), "🗺️ DSOM Task List")
        self.assertEqual(
            self.frontmatter.get("topics"),
            ["readthedocs", "configuration", "testing"],
        )

    def test_frontmatter_precedes_checklist_content(self):
        frontmatter_end = self.content.index("---\n", self.content.index("---\n") + 1) + len("---\n")
        checklist_index = self.content.index("- `[x]`")
        self.assertLessEqual(frontmatter_end, checklist_index)


class TaskMdChecklistContentTests(unittest.TestCase):
    """Verify the new Read the Docs checklist items in task.md."""

    @classmethod
    def setUpClass(cls):
        cls.content = TASK_MD_PATH.read_text(encoding="utf-8")

    def test_new_checklist_items_present(self):
        expected_items = [
            "- `[x]` Create and configure `.readthedocs.yaml` at the root for Read the Docs integration.",
            "- `[x]` Run `dsom-signature-injector` to sign `.readthedocs.yaml`.",
            "- `[x]` Add unit tests for Read the Docs configuration and verify them.",
            "- `[x]` Update brain artefacts (`task.md`, `walkthrough.md`) and ledgers (`CHANGELOG.md`, `HISTORY.md`).",
        ]
        for item in expected_items:
            with self.subTest(item=item):
                self.assertIn(item, self.content)

    def test_new_items_appear_after_prior_eod_item(self):
        eod_index = self.content.index(
            "- `[x]` Complete End-of-Day (EOD) context saving and synchronization."
        )
        readthedocs_index = self.content.index(
            "- `[x]` Create and configure `.readthedocs.yaml`"
        )
        self.assertLess(eod_index, readthedocs_index)

    def test_dsom_signature_footer_present(self):
        valid_dates = ["2026-08-05", "2026-08-20", "2026-08-21", "2026-08-22", "2026-08-23", "2026-08-24"]
        found = any(
            f"*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | {d}*"
            in self.content
            for d in valid_dates
        )
        self.assertTrue(
            found,
            "task.md should contain an up-to-date DSOM signature footer",
        )


class WalkthroughMdFrontmatterTests(unittest.TestCase):
    """Verify the new OKF frontmatter block in .agents/brain/walkthrough.md."""

    @classmethod
    def setUpClass(cls):
        cls.content = WALKTHROUGH_MD_PATH.read_text(encoding="utf-8-sig")
        cls.frontmatter = _extract_frontmatter(cls.content)

    def test_file_exists(self):
        self.assertTrue(WALKTHROUGH_MD_PATH.is_file())

    def test_frontmatter_present_and_parses(self):
        self.assertIsNotNone(self.frontmatter, "Expected a leading '---' YAML frontmatter block")
        self.assertIsInstance(self.frontmatter, dict)

    def test_frontmatter_fields(self):
        self.assertEqual(self.frontmatter.get("okf_version"), 0.1)
        self.assertEqual(self.frontmatter.get("type"), "walkthrough_ledger")
        self.assertEqual(self.frontmatter.get("title"), "🗺️ DSOM Session Walkthrough")
        self.assertEqual(
            self.frontmatter.get("topics"),
            ["readthedocs", "configuration", "testing"],
        )

    def test_frontmatter_precedes_heading_content(self):
        frontmatter_end = self.content.index("---\n", self.content.index("---\n") + 1) + len("---\n")
        heading_index = self.content.index("# DSOM Native MCP Architecture Complete")
        self.assertLessEqual(frontmatter_end, heading_index)


class WalkthroughMdSessionAnchorContentTests(unittest.TestCase):
    """Verify the new Read the Docs Integration session anchor section."""

    @classmethod
    def setUpClass(cls):
        cls.content = WALKTHROUGH_MD_PATH.read_text(encoding="utf-8")

    def test_session_anchor_heading_present(self):
        self.assertIn(
            "## 🏁 Session Anchor: 2026-08-05 — Read the Docs Integration",
            self.content,
        )

    def test_achieved_milestones_present(self):
        expected_lines = [
            "- Created `.readthedocs.yaml` configuration file at the repository root "
            "to enable build integration on Read the Docs.",
            "- Processed `.readthedocs.yaml` using the `dsom-signature-injector` skill "
            "to prepend the standard DSOM licence and ownership signature.",
        ]
        for line in expected_lines:
            with self.subTest(line=line):
                self.assertIn(line, self.content)

    def test_mental_anchor_quote_present(self):
        self.assertIn(
            "> Added official Read the Docs configuration and ensured full compliance "
            "with DSOM's signature and testing standards.",
            self.content,
        )

    def test_new_anchor_appears_after_previous_github_pages_anchor(self):
        github_pages_anchor_index = self.content.index(
            "## 🏁 Session Anchor: 2026-08-02 — GitHub Pages Alignment"
        )
        readthedocs_anchor_index = self.content.index(
            "## 🏁 Session Anchor: 2026-08-05 — Read the Docs Integration"
        )
        self.assertLess(github_pages_anchor_index, readthedocs_anchor_index)

    def test_underlying_rationale_and_mental_anchor_sections_present(self):
        self.assertIn("### Underlying Rationale", self.content)
        self.assertIn("### Integration Mental Anchor", self.content)


class ChangelogReadthedocsEntryTests(unittest.TestCase):
    """Verify the new Read the Docs entry in CHANGELOG.md."""

    @classmethod
    def setUpClass(cls):
        cls.content = CHANGELOG_PATH.read_text(encoding="utf-8")

    def test_file_exists(self):
        self.assertTrue(CHANGELOG_PATH.is_file())

    def test_entry_text_present(self):
        self.assertIn(
            "- **Read the Docs Integration:** Configured `.readthedocs.yaml` at the "
            "repository root using Ubuntu 24.04, Python 3.13, and MkDocs integration "
            "to automatically build the project's documentation on Read the Docs. "
            "Added comprehensive unit tests in `tests/test_readthedocs_config.py` to "
            "verify configuration integrity.",
            self.content,
        )

    def test_entry_is_within_unreleased_added_section(self):
        unreleased_index = self.content.index("## [Unreleased]")
        added_index = self.content.index("### Added", unreleased_index)
        entry_index = self.content.index("**Read the Docs Integration:**")
        self.assertLess(unreleased_index, added_index)
        self.assertLess(added_index, entry_index)


class HistoryReadthedocsEntryTests(unittest.TestCase):
    """Verify the new dated entry in HISTORY.md."""

    @classmethod
    def setUpClass(cls):
        cls.content = HISTORY_PATH.read_text(encoding="utf-8")

    def test_file_exists(self):
        self.assertTrue(HISTORY_PATH.is_file())

    def test_entry_text_present(self):
        self.assertIn(
            "- [2026-08-05]: **Read the Docs Integration.** Configured `.readthedocs.yaml` "
            "at the repository root using Ubuntu 24.04, Python 3.13, and MkDocs to enable "
            "automated document compilation on Read the Docs. Appended standard DSOM "
            "licence/ownership headers, added a new unit testing layer in "
            "`tests/test_readthedocs_config.py`, and updated the project's brain artefacts.",
            self.content,
        )

    def test_entry_appears_after_previous_dated_entry(self):
        previous_entry_index = self.content.index(
            "- [2026-07-26]: **Local Knowledge-First Protocol & Temporal Verification.**"
        )
        new_entry_index = self.content.index(
            "- [2026-08-05]: **Read the Docs Integration.**"
        )
        self.assertLess(previous_entry_index, new_entry_index)

    def test_entry_appears_before_ledger_footer(self):
        # HISTORY.md contains multiple historical "End of Current Ledger"
        # boundary markers; only the final one closes the current ledger.
        new_entry_index = self.content.index(
            "- [2026-08-05]: **Read the Docs Integration.**"
        )
        footer_index = self.content.rindex("*End of Current Ledger")
        self.assertLess(new_entry_index, footer_index)

    def test_entries_are_in_chronological_order(self):
        # All top-level dated bullet entries should be non-decreasing by date.
        dates = re.findall(r"^- \[(\d{4}-\d{2}-\d{2})\]:", self.content, re.MULTILINE)
        self.assertEqual(dates, sorted(dates))
        self.assertIn("2026-08-05", dates)


if __name__ == "__main__":
    unittest.main()