"""Regression tests for OKF resource defaults and source migration."""

import copy
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

import yaml

# Match the import convention used by the existing OKF regression tests.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from tools.apply_okf_frontmatter import normalise_metadata, process_file


DEFAULT_SOURCES = [
    {
        "id": "dsom-core-spec",
        "title": "Deep State of Mind (DSOM) Governance Architecture",
        "resource": "/docs/governance/DSOM-TRI-PHASIC-COGNITIVE-ARCHITECTURE.md",
        "type": "architecture_spec",
        "author": "Harisfazillah Jamel (LinuxMalaysia)",
    },
    {
        "id": "google-okf-v02-spec",
        "title": "Google Cloud Open Knowledge Format (OKF) v0.2 Specification",
        "resource": "https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md",
        "type": "external_spec",
        "author": "Google Cloud Platform",
    },
]


class NormaliseProvenanceTests(unittest.TestCase):
    def normalise(self, metadata, rel_path="docs/guide.md"):
        return normalise_metadata(metadata, "# Guide\n", rel_path, rel_path.split("/")[-1])

    def test_missing_resource_uses_document_path_from_repository_root(self):
        for rel_path in ("README.md", "docs/nested/guide.md", ".agents/skills/audit/SKILL.md"):
            with self.subTest(path=rel_path):
                self.assertEqual(self.normalise({}, rel_path)["resource"], f"/{rel_path}")

    def test_empty_resource_gets_default(self):
        for resource in (None, ""):
            with self.subTest(resource=resource):
                result = self.normalise({"resource": resource})
                self.assertEqual(result["resource"], "/docs/guide.md")

    def test_existing_document_resource_is_preserved(self):
        for resource in (
            "/docs/canonical.md",
            "file:///docs/canonical.md",
            "https://example.org/guide?version=2#provenance",
        ):
            with self.subTest(resource=resource):
                self.assertEqual(self.normalise({"resource": resource})["resource"], resource)

    def test_missing_sources_get_canonical_provenance(self):
        self.assertEqual(self.normalise({})["sources"], DEFAULT_SOURCES)

    def test_empty_or_non_list_sources_get_canonical_provenance(self):
        for sources in (None, [], "", "https://example.org/spec", {}, {"id": "legacy"}, 1, False):
            with self.subTest(sources=sources):
                self.assertEqual(self.normalise({"sources": sources})["sources"], DEFAULT_SOURCES)

    def test_default_sources_are_independent_between_documents(self):
        first = self.normalise({})
        first["sources"][0]["resource"] = "/custom.md"
        first["sources"].append({"id": "extra"})
        self.assertEqual(self.normalise({}, "docs/other.md")["sources"], DEFAULT_SOURCES)

    def test_legacy_url_is_copied_to_resource_without_losing_source_metadata(self):
        source = {
            "id": "upstream-spec",
            "title": "Upstream: [v2]",
            "url": "https://example.org/spec?version=2#sources",
            "author": "Example Author",
            "type": "external_spec",
            "annotations": {"section": "provenance", "verified": True},
        }
        result = self.normalise({"sources": [source]})
        self.assertEqual(result["sources"], [{**source, "resource": source["url"]}])

    def test_source_resource_takes_precedence_over_legacy_url(self):
        source = {"id": "guide", "resource": "/docs/canonical.md", "url": "https://example.org/old"}
        self.assertEqual(self.normalise({"sources": [source]})["sources"], [source])

    def test_sources_without_url_are_preserved_without_inventing_resources(self):
        sources = [{"id": "partial", "title": "Unresolved reference"}, {"resource": "/docs/spec.md"}]
        self.assertEqual(self.normalise({"sources": sources})["sources"], sources)

    def test_mixed_legacy_sources_keep_order_and_duplicates(self):
        sources = [
            "https://example.org/legacy",
            {"url": "https://example.org/spec"},
            ".agents/AGENTS.md",
            "https://example.org/legacy",
        ]
        result = self.normalise({"sources": sources})
        self.assertEqual(result["sources"], [
            sources[0],
            {"url": "https://example.org/spec", "resource": "https://example.org/spec"},
            sources[2],
            sources[3],
        ])

    def test_source_migration_does_not_mutate_caller_metadata(self):
        metadata = {"sources": [{"url": "https://example.org/spec", "id": "spec"}]}
        original = copy.deepcopy(metadata)
        result = self.normalise(metadata)
        self.assertEqual(metadata, original)
        result["sources"][0]["id"] = "changed"
        result["sources"].append({"id": "extra"})
        self.assertEqual(metadata, original)

    def test_provenance_migration_preserves_existing_document_metadata(self):
        metadata = {
            "okf_version": 0.1,
            "type": "documentation",
            "title": "Original title",
            "timestamp": "2026-01-02T03:04:05Z",
            "topics": ["provenance"],
            "description": "An existing guide",
            "verified": {"by": "Reviewer", "notes": ["checked"]},
        }
        result = self.normalise(metadata)
        self.assertEqual(result, {
            **metadata,
            "okf_version": 0.2,
            "spec_version": "0.2",
            "resource": "/docs/guide.md",
            "sources": DEFAULT_SOURCES,
        })

    def test_normalising_provenance_twice_is_idempotent(self):
        for metadata in ({}, {"sources": [{"url": "https://example.org/spec"}]}):
            with self.subTest(metadata=metadata):
                first = self.normalise(metadata)
                self.assertEqual(self.normalise(first), first)


class ProcessFileProvenanceTests(unittest.TestCase):
    def setUp(self):
        temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(temporary_directory.cleanup)
        self.root = Path(temporary_directory.name)
        self.path = self.root / "docs" / "Café guide.md"
        self.path.parent.mkdir()
        self.body = "# Café guide\n\n[Reference](https://example.org/spec)\n\n---\nBody remains intact.\n"

    def write_document(self, metadata):
        text = "---\n" + yaml.safe_dump(metadata, allow_unicode=True) + "---\n" + self.body
        self.path.write_text(text, encoding="utf-8")

    def read_document(self):
        opening, frontmatter, body = self.path.read_text(encoding="utf-8").split("---\n", 2)
        self.assertEqual(opening, "")
        self.assertEqual(body, self.body)
        return yaml.safe_load(frontmatter)

    def test_bare_document_gets_serialisable_defaults_and_is_stable_on_second_run(self):
        self.path.write_text(self.body, encoding="utf-8")
        self.assertTrue(process_file(str(self.path), str(self.root)))
        metadata = self.read_document()
        self.assertEqual(metadata["resource"], "/docs/Café guide.md")
        self.assertEqual(metadata["sources"], DEFAULT_SOURCES)
        self.assertEqual(metadata["okf_version"], 0.2)
        self.assertEqual(metadata["spec_version"], "0.2")
        first_bytes = self.path.read_bytes()
        with patch("tools.apply_okf_frontmatter.atomic_replace_file") as replace:
            self.assertFalse(process_file(str(self.path), str(self.root)))
        replace.assert_not_called()
        self.assertEqual(self.path.read_bytes(), first_bytes)

    def test_existing_provenance_round_trips_special_characters_and_mixed_sources(self):
        legacy_source = {
            "id": "spec",
            "title": 'Café: [v2] "quoted"',
            "author": "Example Author",
            "url": "https://example.org/spec?x=1&y=2#details",
        }
        canonical_source = {"resource": "/docs/spec.md", "url": "https://example.org/old"}
        self.write_document({
            "resource": "file:///docs/canonical.md",
            "sources": [legacy_source, canonical_source, ".agents/AGENTS.md"],
        })
        self.assertTrue(process_file(str(self.path), str(self.root)))
        result = self.read_document()
        self.assertEqual(result["resource"], "file:///docs/canonical.md")
        self.assertEqual(result["sources"], [
            {**legacy_source, "resource": legacy_source["url"]},
            canonical_source,
            ".agents/AGENTS.md",
        ])
        first_bytes = self.path.read_bytes()
        self.assertFalse(process_file(str(self.path), str(self.root)))
        self.assertEqual(self.path.read_bytes(), first_bytes)

    def test_dry_run_reports_provenance_changes_without_writing(self):
        self.write_document({"sources": [{"url": "https://example.org/spec"}]})
        original = self.path.read_bytes()
        with patch("tools.apply_okf_frontmatter.atomic_replace_file") as replace:
            self.assertTrue(process_file(str(self.path), str(self.root), dry_run=True))
        replace.assert_not_called()
        self.assertEqual(self.path.read_bytes(), original)
        self.assertTrue(process_file(str(self.path), str(self.root)))
        self.assertFalse(process_file(str(self.path), str(self.root), dry_run=True))

    def strict_metadata(self):
        return {
            "okf_version": 0.2,
            "spec_version": "0.2",
            "concept_id": "provenance_guide",
            "status": "stable",
            "stale_after": "2027-01-01",
            "generated": {"by": "test-agent", "timestamp": "2026-01-01T00:00:00Z"},
            "sources": [{
                "id": "spec",
                "title": "Specification",
                "author": "Example Author",
                "url": "https://example.org/spec",
            }],
        }

    def test_legacy_url_migration_remains_compatible_with_strict_validation(self):
        original = self.strict_metadata()
        self.write_document(original)
        self.assertTrue(process_file(str(self.path), str(self.root), require_okf_v02=True))
        result = self.read_document()
        self.assertEqual(result["sources"], [
            {**original["sources"][0], "resource": "https://example.org/spec"},
        ])
        self.assertFalse(process_file(str(self.path), str(self.root), require_okf_v02=True))

    def test_invalid_legacy_url_is_rejected_before_writing_in_strict_mode(self):
        for url in ("relative/spec.md", "https:///missing-host", "", None):
            with self.subTest(url=url):
                metadata = self.strict_metadata()
                metadata["sources"][0]["url"] = url
                self.write_document(metadata)
                original = self.path.read_bytes()
                with patch("tools.apply_okf_frontmatter.atomic_replace_file") as replace:
                    with self.assertRaisesRegex(ValueError, r"sources\[0\]\.url"):
                        process_file(str(self.path), str(self.root), require_okf_v02=True)
                replace.assert_not_called()
                self.assertEqual(self.path.read_bytes(), original)

    def test_legacy_string_source_is_rejected_before_writing_in_strict_mode(self):
        metadata = self.strict_metadata()
        metadata["sources"] = ["https://example.org/spec"]
        self.write_document(metadata)
        original = self.path.read_bytes()
        with self.assertRaisesRegex(ValueError, r"sources\[0\] must be a mapping"):
            process_file(str(self.path), str(self.root), require_okf_v02=True)
        self.assertEqual(self.path.read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
