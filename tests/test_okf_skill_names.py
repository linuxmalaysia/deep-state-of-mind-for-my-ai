# ==============================================================================
# Protocol    : Deep State of Mind (DSOM) For My AI
# Author      : Harisfazillah Jamel (LinuxMalaysia)
# Timestamp   : 2026-09-15
# License     : GNU General Public License v3.0
# Standard    : UK English | DBP-standard Bahasa Melayu Malaysia (Piawai)
# ==============================================================================
"""Tests for skill-name derivation in the OKF frontmatter tool."""

from pathlib import Path
import sys
import tempfile
import unittest

import yaml

sys.path.append(str(Path(__file__).resolve().parents[1]))

from tools.apply_okf_frontmatter import (
    normalise_metadata,
    parse_frontmatter,
    process_file,
    serialise_frontmatter,
)


def _metadata(**overrides):
    metadata = {
        "okf_version": 0.1,
        "type": "agent_skill",
        "title": "Example Skill",
        "timestamp": "2026-09-15T00:00:00Z",
        "description": "Exercises one repeatable workflow.",
        "topics": ["dsom", "skill", "agent"],
    }
    metadata.update(overrides)
    return metadata


class SkillNameMetadataTests(unittest.TestCase):
    def test_derives_name_from_relative_skill_directory(self):
        result = normalise_metadata(
            _metadata(),
            "# Example Skill\n",
            ".agents/skills/example-skill/SKILL.md",
            "SKILL.md",
        )

        self.assertEqual(result["name"], "example-skill")

    def test_filepath_parent_takes_precedence_over_relative_path(self):
        result = normalise_metadata(
            _metadata(),
            "# Example Skill\n",
            ".agents/skills/relative-name/SKILL.md",
            "SKILL.md",
            filepath="/tmp/.agents/skills/filepath-name/SKILL.md",
        )

        self.assertEqual(result["name"], "filepath-name")

    def test_replaces_stale_existing_name(self):
        result = normalise_metadata(
            _metadata(name="old-name", custom_field="preserved"),
            "# Example Skill\n",
            ".agents/skills/current-name/SKILL.md",
            "SKILL.md",
        )

        self.assertEqual(result["name"], "current-name")
        self.assertEqual(result["custom_field"], "preserved")

    def test_does_not_create_name_outside_skills_directory(self):
        result = normalise_metadata(
            _metadata(),
            "# Example Skill\n",
            "docs/examples/SKILL.md",
            "SKILL.md",
        )

        self.assertNotIn("name", result)

    def test_preserves_explicit_name_outside_skills_directory(self):
        result = normalise_metadata(
            _metadata(name="external-skill"),
            "# Example Skill\n",
            "docs/examples/SKILL.md",
            "SKILL.md",
        )

        self.assertEqual(result["name"], "external-skill")


class SkillNameSerialisationTests(unittest.TestCase):
    def test_places_name_immediately_after_topics_for_skill_files(self):
        frontmatter = serialise_frontmatter(
            _metadata(name="example-skill", custom_field="preserved"),
            ".agents/skills/example-skill/SKILL.md",
            "SKILL.md",
        )

        lines = frontmatter.splitlines()
        self.assertEqual(
            lines[1:8],
            [
                "okf_version: 0.1",
                "type: agent_skill",
                "title: Example Skill",
                'timestamp: "2026-09-15T00:00:00Z"',
                'description: "Exercises one repeatable workflow."',
                'topics: ["dsom", "skill", "agent"]',
                "name: example-skill",
            ],
        )
        self.assertLess(frontmatter.index("name:"), frontmatter.index("custom_field:"))

    def test_serialised_skill_name_round_trips_as_string(self):
        frontmatter = serialise_frontmatter(
            _metadata(name="skill-v2"),
            ".agents/skills/skill-v2/SKILL.md",
            "SKILL.md",
        )

        parsed = yaml.safe_load(frontmatter.split("---", 2)[1])
        self.assertEqual(parsed["name"], "skill-v2")


class SkillNameProcessFileTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def _create_markdown(self, relative_path, *, name=None):
        path = self.root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        metadata = _metadata()
        if name is not None:
            metadata["name"] = name
        content = serialise_frontmatter(metadata, relative_path, path.name)
        path.write_text(content + "# Example Skill\n", encoding="utf-8")
        return path

    def _read_metadata(self, path):
        content = path.read_text(encoding="utf-8")
        metadata, _ = parse_frontmatter(content, path.relative_to(self.root).as_posix())
        return metadata

    def test_injects_missing_name_when_root_is_skills_directory(self):
        path = self._create_markdown(
            ".agents/skills/missing-name/SKILL.md",
        )
        skills_root = self.root / ".agents" / "skills"

        modified = process_file(str(path), str(skills_root))

        self.assertTrue(modified)
        self.assertEqual(self._read_metadata(path)["name"], "missing-name")

    def test_corrects_stale_name_and_is_idempotent(self):
        path = self._create_markdown(
            ".agents/skills/current-name/SKILL.md",
            name="stale-name",
        )

        self.assertTrue(process_file(str(path), str(self.root)))
        content_after_first_run = path.read_text(encoding="utf-8")
        self.assertEqual(self._read_metadata(path)["name"], "current-name")

        self.assertFalse(process_file(str(path), str(self.root)))
        self.assertEqual(path.read_text(encoding="utf-8"), content_after_first_run)

    def test_dry_run_reports_change_without_writing(self):
        path = self._create_markdown(
            ".agents/skills/current-name/SKILL.md",
            name="stale-name",
        )
        original = path.read_text(encoding="utf-8")

        modified = process_file(str(path), str(self.root), dry_run=True)

        self.assertTrue(modified)
        self.assertEqual(path.read_text(encoding="utf-8"), original)

    def test_standalone_skill_file_outside_agents_skills_gets_no_name(self):
        path = self._create_markdown("examples/SKILL.md")

        modified = process_file(str(path), str(self.root))

        self.assertFalse(modified)
        self.assertNotIn("name", self._read_metadata(path))


if __name__ == "__main__":
    unittest.main()
