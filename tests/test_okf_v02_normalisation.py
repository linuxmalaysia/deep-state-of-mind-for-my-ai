# ==============================================================================
# Protocol    : Deep State of Mind (DSOM) For My AI
# Author      : Harisfazillah Jamel (LinuxMalaysia)
# Timestamp   : 2026-10-08
# License     : GNU General Public License v3.0
# Standard    : UK English | DBP-standard Bahasa Melayu Malaysia (Piawai)
# ==============================================================================
"""Regression tests for OKF v0.2 source and trust metadata migration."""

import copy
import tempfile
import unittest
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import yaml

from tools.apply_okf_frontmatter import (
    get_default_topics,
    get_okf_type,
    normalise_metadata,
    process_file,
    serialise_frontmatter,
    serialise_val,
    validate_okf_v02_metadata,
)

TIMESTAMP = "2026-10-04T12:00:00Z"
REPOSITORY_URL = (
    "https://github.com/linuxmalaysia/deep-state-of-mind-for-my-ai/blob/main/"
)
AUTHOR = "Harisfazillah Jamel (LinuxMalaysia)"


def trust_metadata():
    """Return independent, valid metadata for each test."""
    return {
        "okf_version": 0.2,
        "spec_version": "0.2",
        "timestamp": TIMESTAMP,
        "concept_id": "example_concept",
        "status": "stable",
        "stale_after": "2027-10-04",
        "sources": [{
            "id": "spec",
            "title": "Example specification",
            "author": "Example Author",
            "url": "https://example.org/spec",
        }],
        "generated": {"by": "test-agent", "timestamp": TIMESTAMP},
    }


def normalise(metadata, *, strict=False):
    return normalise_metadata(
        metadata, "# Example\n", "docs/example.md", "example.md",
        require_okf_v02=strict,
    )


class FlowMappingTests(unittest.TestCase):
    def test_nested_trust_metadata_round_trips_without_mutation(self):
        value = {
            "sources": [{
                "title": 'Guide: "Café" [draft]',
                "url": "https://example.org/spec?q=one&x=two",
                "notes": "first line\nsecond line\\path",
            }],
            "generated": {"by": "test-agent", "timestamp": TIMESTAMP},
            "values": [None, True, False, 0, 0.2, "false", "null", "0123"],
            "empty_mapping": {},
            "empty_list": [],
        }
        original = copy.deepcopy(value)
        rendered = serialise_val(value, "trust")

        self.assertTrue(rendered.startswith("{"))
        self.assertTrue(rendered.endswith("}"))
        self.assertNotIn("\n", rendered)
        self.assertEqual(yaml.safe_load(rendered), original)
        self.assertEqual(value, original)

    def test_empty_mapping_round_trips(self):
        self.assertEqual(serialise_val({}, "generated"), "{}")


class SourceNormalisationTests(unittest.TestCase):
    def test_default_sources_have_valid_absolute_urls(self):
        for sources in (None, [], "invalid", {}):
            with self.subTest(sources=sources):
                metadata = trust_metadata()
                metadata["sources"] = sources
                result = normalise(metadata, strict=True)
                validate_okf_v02_metadata(result, "docs/example.md")
                self.assertEqual(len(result["sources"]), 2)
                for source in result["sources"]:
                    self.assertTrue(source["url"].startswith("https://"))

    def test_source_strings_distinguish_local_and_external_references(self):
        references = [
            ("/docs/source.md", REPOSITORY_URL + "docs/source.md", False),
            ("docs/source.md", REPOSITORY_URL + "docs/source.md", False),
            ("https://example.org/spec", "https://example.org/spec", True),
            ("http://example.org/spec", "http://example.org/spec", True),
        ]
        for resource, url, external in references:
            with self.subTest(resource=resource):
                source = normalise({"sources": [resource]})["sources"][0]
                expected = {
                    "id": "source-1", "title": resource, "resource": resource,
                    "url": url,
                    "type": "external_spec" if external else "repository_file",
                }
                if not external:
                    expected["author"] = AUTHOR
                self.assertEqual(source, expected)

    def test_mapping_reference_aliases_gain_resource_and_url(self):
        for field, reference in (
            ("path", "/docs/source.md"),
            ("resource", "/docs/source.md"),
            ("resource", "https://example.org/spec"),
            ("url", "https://example.org/spec"),
        ):
            with self.subTest(field=field, reference=reference):
                metadata = {"sources": [{field: reference}]}
                original = copy.deepcopy(metadata)
                result = normalise(metadata)["sources"][0]
                self.assertEqual(result["resource"], reference)
                self.assertEqual(result["title"], reference)
                self.assertEqual(result["id"], "source-1")
                self.assertEqual(
                    result["url"], reference if reference.startswith("https://")
                    else REPOSITORY_URL + "docs/source.md",
                )
                self.assertEqual(metadata, original)

    def test_explicit_source_fields_and_extensions_survive(self):
        source = {
            "id": "custom-id", "title": "Custom title", "author": "Editor",
            "resource": "/docs/canonical.md", "path": "/docs/alias.md",
            "url": "https://example.org/published", "type": "manual",
            "section": "Background",
        }
        self.assertEqual(normalise({"sources": [source]})["sources"], [source])

    def test_invalid_entries_are_dropped_without_losing_valid_sources(self):
        result = normalise({"sources": [None, 42, [], "/docs/source.md"]})
        self.assertEqual(len(result["sources"]), 1)
        self.assertEqual(result["sources"][0]["resource"], "/docs/source.md")

    def test_strict_validation_rejects_sources_with_no_valid_entries(self):
        metadata = trust_metadata()
        metadata["sources"] = [None, 42, []]
        result = normalise(metadata, strict=True)
        with self.assertRaisesRegex(ValueError, "sources must be a non-empty list"):
            validate_okf_v02_metadata(result, "docs/example.md")

    def test_external_source_requires_author_in_strict_mode(self):
        metadata = trust_metadata()
        metadata["sources"] = ["https://example.org/spec"]
        result = normalise(metadata, strict=True)
        self.assertNotIn("author", result["sources"][0])
        with self.assertRaisesRegex(ValueError, r"sources\[0\]\.author"):
            validate_okf_v02_metadata(result, "docs/example.md")


class TrustNormalisationTests(unittest.TestCase):
    def test_valid_statuses_are_preserved_in_both_modes(self):
        for status in ("draft", "stable", "deprecated"):
            for strict in (False, True):
                with self.subTest(status=status, strict=strict):
                    self.assertEqual(normalise({"status": status}, strict=strict)["status"], status)

    def test_invalid_status_defaults_only_in_permissive_mode(self):
        for status in (None, "", "Stable", " stable ", "approved", 0, [], {}):
            with self.subTest(status=status):
                self.assertEqual(normalise({"status": status})["status"], "stable")
                with self.assertRaisesRegex(ValueError, r"docs/example\.md: status must"):
                    normalise({"status": status}, strict=True)

    def test_optional_trust_fields_are_not_invented(self):
        result = normalise({})
        for field in ("status", "generated", "stale_after"):
            self.assertNotIn(field, result)

    def test_generated_scalars_and_missing_authors_receive_defaults(self):
        cases = [
            ("custom-agent", "custom-agent"),
            (None, "agent/dsom-subagent-01"),
            (42, "42"),
            ({}, "agent/dsom-subagent-01"),
            ({"by": "  "}, "agent/dsom-subagent-01"),
            ({"by": 42}, "agent/dsom-subagent-01"),
        ]
        for generated, expected_by in cases:
            with self.subTest(generated=generated):
                result = normalise({"timestamp": TIMESTAMP, "generated": generated})
                self.assertEqual(result["generated"], {"by": expected_by, "timestamp": TIMESTAMP})

    def test_generated_timestamp_alias_priority_and_fallback(self):
        other = "2026-10-05T09:00:00Z"
        cases = [
            ({"at": other}, other),
            ({"timestamp": TIMESTAMP, "at": other}, TIMESTAMP),
            ({"timestamp": "", "at": other}, other),
            ({"timestamp": None, "at": other}, other),
            ({"timestamp": 42}, TIMESTAMP),
        ]
        for fields, expected in cases:
            with self.subTest(fields=fields):
                metadata = {"timestamp": TIMESTAMP, "generated": {"by": "agent", **fields}}
                original = copy.deepcopy(metadata)
                self.assertEqual(normalise(metadata)["generated"], {"by": "agent", "timestamp": expected})
                self.assertEqual(metadata, original)

    def test_generated_datetimes_convert_to_utc_across_date_boundary(self):
        cases = [
            (datetime(2026, 10, 4, 12), TIMESTAMP),
            (datetime(2026, 10, 4, 1, tzinfo=timezone(timedelta(hours=8))), "2026-10-03T17:00:00Z"),
        ]
        for timestamp, expected in cases:
            with self.subTest(timestamp=timestamp):
                result = normalise({"generated": {"by": "agent", "at": timestamp}})
                self.assertEqual(result["generated"]["timestamp"], expected)

    def test_stale_after_normalises_date_representations(self):
        for value in (
            "2028-02-29", " 2028-02-29 ", "2028-02-29T23:00:00Z",
            date(2028, 2, 29), datetime(2028, 2, 29, 23),
        ):
            with self.subTest(value=value):
                self.assertEqual(normalise({"stale_after": value})["stale_after"], "2028-02-29")

    def test_normalising_does_not_hide_invalid_stale_after_dates(self):
        metadata = trust_metadata()
        metadata["stale_after"] = "2027-02-29T12:00:00Z"
        with self.assertRaisesRegex(ValueError, "stale_after"):
            validate_okf_v02_metadata(normalise(metadata), "docs/example.md")


class GeneratedAtValidationTests(unittest.TestCase):
    def test_accepts_at_alias_when_timestamp_is_absent_or_falsey(self):
        for timestamp in (None, "", False, 0):
            with self.subTest(timestamp=timestamp):
                metadata = trust_metadata()
                metadata["generated"] = {"by": "agent", "at": TIMESTAMP}
                validate_okf_v02_metadata(metadata, "docs/example.md")
                metadata["generated"]["timestamp"] = timestamp
                original = copy.deepcopy(metadata)
                validate_okf_v02_metadata(metadata, "docs/example.md")
                self.assertEqual(metadata, original)

    def test_rejects_invalid_alias_timestamps(self):
        for timestamp in (None, 42, "invalid", "2026-10-04", "2026-10-04T12:00:00", "2026-10-04T12:00:00+08:00"):
            with self.subTest(timestamp=timestamp):
                metadata = trust_metadata()
                metadata["generated"] = {"by": "agent", "at": timestamp}
                with self.assertRaisesRegex(ValueError, "generated.timestamp"):
                    validate_okf_v02_metadata(metadata, "docs/example.md")

    def test_valid_alias_does_not_mask_invalid_explicit_timestamp(self):
        metadata = trust_metadata()
        metadata["generated"] = {"by": "agent", "timestamp": "invalid", "at": TIMESTAMP}
        with self.assertRaisesRegex(ValueError, "generated.timestamp"):
            validate_okf_v02_metadata(metadata, "docs/example.md")

    def test_valid_explicit_timestamp_takes_precedence_over_invalid_alias(self):
        metadata = trust_metadata()
        metadata["generated"]["at"] = "invalid"
        validate_okf_v02_metadata(metadata, "docs/example.md")


class LolaMetadataTests(unittest.TestCase):
    """Check Lola packaging defaults and preservation during OKF migration."""

    def normalise_skill(self, metadata, **kwargs):
        return normalise_metadata(
            metadata, "# Example skill\n", ".agents/skills/example/SKILL.md",
            "SKILL.md", **kwargs,
        )

    def test_skill_type_accepts_both_path_separators(self):
        for path in (
            ".agents/skills/example/SKILL.md",
            r"C:\workspace\.agents\skills\example\SKILL.md",
        ):
            with self.subTest(path=path):
                self.assertEqual(get_okf_type(path), "skill")

    def test_skill_type_uses_components_and_preserves_governance_precedence(self):
        for path, expected in (
            ("docs/skills/example.md", "documentation"),
            (".agents/skills-extra/example.md", "documentation"),
            (".agents/skills/example/docs/governance/policy.md", "governance_protocol"),
        ):
            with self.subTest(path=path):
                self.assertEqual(get_okf_type(path), expected)

    def test_new_and_legacy_skill_types_share_default_topics(self):
        for skill_type in ("skill", "agent_skill"):
            with self.subTest(skill_type=skill_type):
                self.assertEqual(get_default_topics(skill_type), ["dsom", "skill", "agent"])

    def test_missing_packaging_fields_receive_lola_defaults(self):
        result = self.normalise_skill({})
        expected = {
            "name": "example", "version": "1.0.0", "author": AUTHOR,
            "license": "GPL-3.0-or-later", "type": "skill",
            "status": "stable", "stale_after": "2027-10-01",
            "topics": ["dsom", "skill", "agent"],
        }
        for field, value in expected.items():
            with self.subTest(field=field):
                self.assertEqual(result[field], value)

    def test_standalone_skill_gets_packaging_fields_from_parent_directory(self):
        result = normalise_metadata({}, "# Portable\n", "portable/SKILL.md", "SKILL.md")
        self.assertEqual(result["name"], "portable")
        self.assertEqual(result["version"], "1.0.0")
        self.assertEqual(result["license"], "GPL-3.0-or-later")

    def test_existing_skill_types_survive_packaging_migration(self):
        for skill_type in ("agent_skill", "skill_sop"):
            with self.subTest(skill_type=skill_type):
                result = self.normalise_skill({"type": skill_type})
                self.assertEqual(result["type"], skill_type)
                self.assertEqual(result["version"], "1.0.0")

    def test_absolute_filepath_takes_precedence_over_relative_name(self):
        filepath = str(Path(tempfile.gettempdir()) / "actual-package" / "SKILL.md")
        result = self.normalise_skill({"name": "obsolete-name"}, filepath=filepath)
        self.assertEqual(result["name"], "actual-package")

    def test_skill_directory_is_recognised_when_scan_root_omits_it(self):
        filepath = str(Path(tempfile.gettempdir()) / ".agents" / "skills" / "example" / "guide.md")
        result = normalise_metadata({}, "# Guide\n", "guide.md", "guide.md", filepath=filepath)
        self.assertEqual(result["name"], "example")
        self.assertEqual(result["version"], "1.0.0")

    def test_explicit_packaging_and_extension_fields_survive_without_mutation(self):
        metadata = {
            "name": "old-name", "version": "2.4.0-rc.1", "author": "Package Maintainer",
            "license": "MIT", "status": "deprecated", "stale_after": "2028-02-29",
            "description": "A custom package", "topics": ["custom", "package", "test"],
            "extensions": {"targets": ["local"]},
        }
        original = copy.deepcopy(metadata)
        result = self.normalise_skill(metadata)
        for key, value in original.items():
            with self.subTest(key=key):
                self.assertEqual(result[key], "example" if key == "name" else value)
        self.assertEqual(metadata, original)

    def test_versions_are_strings_and_round_trip_through_yaml(self):
        for version, expected in ((0, "0"), (1.5, "1.5"), ("1.0", "1.0"), ("2.0.0+build.7", "2.0.0+build.7")):
            with self.subTest(version=version):
                metadata = self.normalise_skill({"version": version})
                rendered = serialise_frontmatter(metadata, ".agents/skills/example/SKILL.md", "SKILL.md")
                parsed = yaml.safe_load(rendered.split("---\n", 2)[1])
                self.assertEqual(metadata["version"], expected)
                self.assertEqual(parsed["version"], expected)

    def test_ordinary_documents_do_not_receive_lola_defaults(self):
        result = normalise_metadata({}, "# Guide\n", "docs/example.md", "example.md")
        for field in ("name", "version", "author", "license", "status", "stale_after"):
            with self.subTest(field=field):
                self.assertNotIn(field, result)

    def test_skill_serialisation_orders_packaging_keys_without_losing_values(self):
        metadata = self.normalise_skill({"description": 'Guide: "Café" [draft]', "custom": {"enabled": True}})
        original = copy.deepcopy(metadata)
        rendered = serialise_frontmatter(metadata, ".agents/skills/example/SKILL.md", "SKILL.md")
        parsed = yaml.safe_load(rendered.split("---\n", 2)[1])
        self.assertEqual(list(parsed)[:12], [
            "name", "version", "description", "topics", "author", "license",
            "okf_version", "type", "status", "stale_after", "title", "timestamp",
        ])
        self.assertEqual(parsed, original)
        self.assertEqual(metadata, original)

    def test_non_skill_serialisation_keeps_okf_keys_first(self):
        metadata = normalise({"name": "example", "version": "2.0"})
        rendered = serialise_frontmatter(metadata, "docs/example.md", "example.md")
        parsed = yaml.safe_load(rendered.split("---\n", 2)[1])
        self.assertEqual(list(parsed)[:5], ["okf_version", "type", "title", "timestamp", "topics"])
        self.assertEqual(parsed, metadata)

    def test_packaging_defaults_do_not_bypass_strict_status_validation(self):
        with self.assertRaisesRegex(ValueError, "status must"):
            self.normalise_skill({"status": "published"}, require_okf_v02=True)


class LolaSkillMigrationTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        self.path = self.root / ".agents" / "skills" / "example" / "SKILL.md"
        self.path.parent.mkdir(parents=True)
        self.body = "# Example\n\nCafé\n\n---\n\nKeep this body.\n"
        metadata = trust_metadata()
        metadata.update({"name": "old-name", "description": "Example skill", "version": 1.5})
        metadata.pop("status")
        metadata.pop("stale_after")
        self.path.write_text("---\n" + yaml.safe_dump(metadata) + "---\n" + self.body, encoding="utf-8")

    def test_strict_migration_adds_defaults_preserves_body_and_is_idempotent(self):
        self.assertTrue(process_file(str(self.path), str(self.root), require_okf_v02=True))
        first = self.path.read_bytes()
        _, raw, body = first.decode("utf-8").split("---\n", 2)
        metadata = yaml.safe_load(raw)
        self.assertEqual(metadata["name"], "example")
        self.assertEqual(metadata["version"], "1.5")
        self.assertEqual(metadata["type"], "skill")
        self.assertEqual(metadata["status"], "stable")
        self.assertEqual(metadata["stale_after"], "2027-10-01")
        self.assertEqual(body, self.body)
        validate_okf_v02_metadata(metadata, ".agents/skills/example/SKILL.md")
        self.assertFalse(process_file(str(self.path), str(self.root), require_okf_v02=True))
        self.assertEqual(self.path.read_bytes(), first)
        self.assertEqual(list(self.path.parent.iterdir()), [self.path])

    def test_dry_run_reports_missing_packaging_without_writing(self):
        original = self.path.read_bytes()
        self.assertTrue(process_file(str(self.path), str(self.root), dry_run=True, require_okf_v02=True))
        self.assertEqual(self.path.read_bytes(), original)
        self.assertEqual(list(self.path.parent.iterdir()), [self.path])


class MigratedFileTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.path = Path(self.directory.name) / "example.md"
        metadata = trust_metadata()
        metadata["sources"] = [{"path": "/docs/source.md"}]
        metadata["generated"] = {"by": "agent", "at": TIMESTAMP}
        metadata["stale_after"] = "2028-02-29T12:00:00Z"
        self.body = "# Example\n\nUnicode: Café\n\n---\n\nBody text.\n"
        self.path.write_text("---\n" + yaml.safe_dump(metadata) + "---\n" + self.body, encoding="utf-8")

    def test_strict_migration_preserves_body_and_is_idempotent(self):
        self.assertTrue(process_file(str(self.path), self.directory.name, require_okf_v02=True))
        first = self.path.read_bytes()
        _, frontmatter, body = first.decode("utf-8").split("---\n", 2)
        parsed = yaml.safe_load(frontmatter)
        validate_okf_v02_metadata(parsed, "example.md")
        self.assertEqual(body, self.body)
        self.assertEqual(parsed["generated"], {"by": "agent", "timestamp": TIMESTAMP})
        self.assertEqual(parsed["stale_after"], "2028-02-29")
        self.assertEqual(parsed["sources"][0]["url"], REPOSITORY_URL + "docs/source.md")
        self.assertFalse(process_file(str(self.path), self.directory.name, require_okf_v02=True))
        self.assertEqual(self.path.read_bytes(), first)

    def test_dry_run_reports_migration_without_writing(self):
        original = self.path.read_bytes()
        self.assertTrue(process_file(str(self.path), self.directory.name, dry_run=True, require_okf_v02=True))
        self.assertEqual(self.path.read_bytes(), original)
        self.assertEqual(list(Path(self.directory.name).iterdir()), [self.path])

    def test_invalid_status_is_rejected_before_file_replacement(self):
        content = self.path.read_text(encoding="utf-8").replace("status: stable", "status: approved")
        self.path.write_text(content, encoding="utf-8")
        original = self.path.read_bytes()
        with self.assertRaisesRegex(ValueError, "status must"):
            process_file(str(self.path), self.directory.name, require_okf_v02=True)
        self.assertEqual(self.path.read_bytes(), original)
        self.assertEqual(list(Path(self.directory.name).iterdir()), [self.path])


if __name__ == "__main__":
    unittest.main()
