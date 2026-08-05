# ==============================================================================
# Protocol    : Deep State of Mind (DSOM) For My AI
# Author      : Harisfazillah Jamel (LinuxMalaysia)
# Timestamp   : 2026-08-05
# License     : GNU General Public License v3.0
# Standard    : UK English | DBP-standard Bahasa Melayu Malaysia (Piawai)
# ==============================================================================
"""
Unit tests for the brain artefacts and ledgers updated alongside the Read the
Docs integration:

- `.agents/brain/task.md`: gained an OKF frontmatter block and four new
  checklist entries documenting the Read the Docs work.
- `.agents/brain/walkthrough.md`: gained an OKF frontmatter block and a new
  "🏁 Session Anchor: 2026-08-05 — Read the Docs Integration" section.
- `CHANGELOG.md`: gained a new "Read the Docs Integration" bullet under
  `## [Unreleased]` -> `### Added`.
- `HISTORY.md`: gained a new dated entry for 2026-08-05.
"""
import pathlib
import unittest

import yaml  # type: ignore


def _find_repo_root(start: pathlib.Path) -> pathlib.Path:
    """Locate the repository root from a starting path."""
    current = start.resolve()
    for parent in [current, *current.parents]:
        if (parent / ".git").exists():
            return parent
    raise RuntimeError("Could not locate repository root (.git not found)")


def _parse_frontmatter(content: str):
    """Parse a leading YAML frontmatter block (delimited by `---`) and return
    the parsed mapping plus the remaining body text."""
    if not content.startswith("---\n"):
        return None, content
    end_index = content.find("\n---\n", 4)
    if end_index == -1:
        return None, content
    frontmatter_text = content[4:end_index]
    body = content[end_index + len("\n---\n"):]
    return yaml.safe_load(frontmatter_text), body


REPO_ROOT = _find_repo_root(pathlib.Path(__file__).parent)
TASK_PATH = REPO_ROOT / ".agents" / "brain" / "task.md"
WALKTHROUGH_PATH = REPO_ROOT / ".agents" / "brain" / "walkthrough.md"
CHANGELOG_PATH = REPO_ROOT / "CHANGELOG.md"
HISTORY_PATH = REPO_ROOT / "HISTORY.md"


class TaskLedgerFrontmatterTests(unittest.TestCase):
    """Verify the new OKF frontmatter block in task.md."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.content = TASK_PATH.read_text(encoding="utf-8")
        cls.frontmatter, cls.body = _parse_frontmatter(cls.content)

    def test_task_md_exists(self):
        self.assertTrue(TASK_PATH.is_file())

    def test_frontmatter_is_parsed_as_mapping(self):
        self.assertIsInstance(self.frontmatter, dict)

    def test_frontmatter_declares_task_ledger_type(self):
        self.assertEqual(self.frontmatter.get("type"), "task_ledger")

    def test_frontmatter_declares_okf_version(self):
        self.assertEqual(self.frontmatter.get("okf_version"), 0.1)

    def test_frontmatter_declares_expected_topics(self):
        self.assertEqual(
            self.frontmatter.get("topics"),
            ["readthedocs", "configuration", "testing"],
        )

    def test_frontmatter_timestamp_matches_session_date(self):
        timestamp = self.frontmatter.get("timestamp")
        # PyYAML parses ISO-8601 datetimes into datetime objects.
        self.assertEqual(str(timestamp.date()), "2026-08-05")


class TaskLedgerChecklistTests(unittest.TestCase):
    """Verify the new checklist entries appended to task.md."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.content = TASK_PATH.read_text(encoding="utf-8")

    def test_readthedocs_yaml_checklist_item_present_and_checked(self):
        self.assertIn(
            "`[x]` Create and configure `.readthedocs.yaml` at the root for Read the Docs integration.",
            self.content,
        )

    def test_signature_injector_checklist_item_present_and_checked(self):
        self.assertIn(
            "`[x]` Run `dsom-signature-injector` to sign `.readthedocs.yaml`.",
            self.content,
        )

    def test_unit_tests_checklist_item_present_and_checked(self):
        self.assertIn(
            "`[x]` Add unit tests for Read the Docs configuration and verify them.",
            self.content,
        )

    def test_brain_and_ledger_sync_checklist_item_present_and_checked(self):
        self.assertIn(
            "`[x]` Update brain artefacts (`task.md`, `walkthrough.md`) and ledgers (`CHANGELOG.md`, `HISTORY.md`).",
            self.content,
        )

    def test_no_unchecked_readthedocs_items(self):
        """Boundary check: none of the new Read the Docs items were left unchecked."""
        self.assertNotIn("`[ ]` Create and configure `.readthedocs.yaml`", self.content)

    def test_dsom_footer_signature_still_present(self):
        self.assertIn(
            "Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-08-05",
            self.content,
        )


class WalkthroughLedgerFrontmatterTests(unittest.TestCase):
    """Verify the new OKF frontmatter block in walkthrough.md."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.content = WALKTHROUGH_PATH.read_text(encoding="utf-8")
        cls.frontmatter, cls.body = _parse_frontmatter(cls.content)

    def test_walkthrough_md_exists(self):
        self.assertTrue(WALKTHROUGH_PATH.is_file())

    def test_frontmatter_is_parsed_as_mapping(self):
        self.assertIsInstance(self.frontmatter, dict)

    def test_frontmatter_declares_walkthrough_ledger_type(self):
        self.assertEqual(self.frontmatter.get("type"), "walkthrough_ledger")

    def test_frontmatter_declares_expected_topics(self):
        self.assertEqual(
            self.frontmatter.get("topics"),
            ["readthedocs", "configuration", "testing"],
        )

    def test_body_still_starts_with_original_heading(self):
        # Regression guard: the pre-existing body content must be preserved
        # unchanged directly after the newly inserted frontmatter block.
        self.assertTrue(
            self.body.startswith("# DSOM Native MCP Architecture Complete"),
            "Expected the original walkthrough heading to immediately follow the frontmatter",
        )


class WalkthroughSessionAnchorTests(unittest.TestCase):
    """Verify the new 2026-08-05 Read the Docs session anchor section."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.content = WALKTHROUGH_PATH.read_text(encoding="utf-8")

    def test_session_anchor_heading_present(self):
        self.assertIn(
            "## 🏁 Session Anchor: 2026-08-05 — Read the Docs Integration",
            self.content,
        )

    def test_achieved_milestones_subsection_present(self):
        self.assertIn("### Achieved Integration Milestones", self.content)
        self.assertIn(
            "Created `.readthedocs.yaml` configuration file at the repository root",
            self.content,
        )
        self.assertIn(
            "Processed `.readthedocs.yaml` using the `dsom-signature-injector` skill",
            self.content,
        )
        self.assertIn(
            "Added comprehensive unit tests in `tests/test_readthedocs_config.py`",
            self.content,
        )

    def test_rationale_subsection_present(self):
        self.assertIn("### Underlying Rationale", self.content)

    def test_mental_anchor_subsection_present(self):
        self.assertIn("### Integration Mental Anchor", self.content)
        self.assertIn(
            "> Added official Read the Docs configuration and ensured full compliance",
            self.content,
        )

    def test_new_section_appears_after_previous_session_anchor(self):
        github_pages_anchor_index = self.content.index(
            "## 🏁 Session Anchor: 2026-08-02 — GitHub Pages Alignment"
        )
        readthedocs_anchor_index = self.content.index(
            "## 🏁 Session Anchor: 2026-08-05 — Read the Docs Integration"
        )
        self.assertLess(github_pages_anchor_index, readthedocs_anchor_index)

    def test_new_section_is_last_in_file(self):
        # Regression guard: no further content should trail the new anchor,
        # ensuring the append happened at the end of the file as expected.
        readthedocs_anchor_index = self.content.index(
            "## 🏁 Session Anchor: 2026-08-05 — Read the Docs Integration"
        )
        remaining = self.content[readthedocs_anchor_index:]
        self.assertNotIn("## 🏁 Session Anchor:", remaining[len("## 🏁 Session Anchor: 2026-08-05"):])


class ChangelogReadthedocsEntryTests(unittest.TestCase):
    """Verify the new CHANGELOG.md entry for the Read the Docs integration."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.content = CHANGELOG_PATH.read_text(encoding="utf-8")

    def test_changelog_exists(self):
        self.assertTrue(CHANGELOG_PATH.is_file())

    def test_readthedocs_entry_present_under_unreleased_added(self):
        self.assertIn(
            "- **Read the Docs Integration:** Configured `.readthedocs.yaml` at the "
            "repository root using Ubuntu 24.04, Python 3.13, and MkDocs integration "
            "to automatically build the project's documentation on Read the Docs. "
            "Added comprehensive unit tests in `tests/test_readthedocs_config.py` "
            "to verify configuration integrity.",
            self.content,
        )

    def test_readthedocs_entry_is_first_item_under_unreleased_added(self):
        unreleased_index = self.content.index("## [Unreleased]")
        added_index = self.content.index("### Added", unreleased_index)
        readthedocs_index = self.content.index(
            "**Read the Docs Integration:**", added_index
        )
        next_bullet_index = self.content.index(
            "**Executor Modularity", added_index
        )
        self.assertLess(added_index, readthedocs_index)
        self.assertLess(readthedocs_index, next_bullet_index)


class HistoryReadthedocsEntryTests(unittest.TestCase):
    """Verify the new HISTORY.md dated entry for the Read the Docs integration."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.content = HISTORY_PATH.read_text(encoding="utf-8")

    def test_history_exists(self):
        self.assertTrue(HISTORY_PATH.is_file())

    def test_dated_entry_present(self):
        self.assertIn(
            "- [2026-08-05]: **Read the Docs Integration.** Configured "
            "`.readthedocs.yaml` at the repository root using Ubuntu 24.04, "
            "Python 3.13, and MkDocs to enable automated document compilation "
            "on Read the Docs.",
            self.content,
        )

    def test_dated_entry_appears_after_previous_entry(self):
        knowledge_first_index = self.content.index(
            "- [2026-07-26]: **Local Knowledge-First Protocol"
        )
        readthedocs_index = self.content.index(
            "- [2026-08-05]: **Read the Docs Integration.**"
        )
        self.assertLess(knowledge_first_index, readthedocs_index)

    def test_dated_entry_precedes_ledger_footer(self):
        readthedocs_index = self.content.index(
            "- [2026-08-05]: **Read the Docs Integration.**"
        )
        footer_index = self.content.index(
            "*End of Current Ledger | Standard: DSOM Protocol v10.4.0-governance | "
            "Harisfazillah Jamel*"
        )
        self.assertLess(readthedocs_index, footer_index)


if __name__ == "__main__":
    unittest.main()