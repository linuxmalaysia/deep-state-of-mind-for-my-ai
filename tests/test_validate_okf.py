"""Exercise the POSIX validator against isolated Markdown fixtures."""

import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

VALIDATOR = Path(__file__).resolve().parents[1] / "tools" / "validate-okf.sh"
FIELDS = {
    "okf_version": "0.2",
    "type": "documentation",
    "title": '"Example: Café"',
    "timestamp": '"2026-10-04T12:00:00Z"',
    "topics": '["okf", "documentation"]',
}


def document(fields=None, body="# Example\n"):
    if fields is None:
        fields = FIELDS
    return "---\n" + "\n".join(f"{key}: {value}" for key, value in fields.items()) + "\n---\n" + body


@unittest.skipUnless(os.name == "posix" and shutil.which("sh"), "POSIX shell required")
class ValidateOkfTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.scratch = self.root / "scratch"
        self.scratch.mkdir()

    def write_document(self, relative_path, content):
        path = self.root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content.encode("utf-8"))
        return path

    def run_validator(self, expected_status):
        result = subprocess.run(
            ["sh", str(VALIDATOR)],
            cwd=self.root,
            env={**os.environ, "TMPDIR": str(self.scratch)},
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
        self.assertEqual(result.returncode, expected_status, result.stdout + result.stderr)
        self.assertEqual(result.stderr, "")
        self.assertEqual(list(self.scratch.iterdir()), [], "Validator leaked its temporary file list")
        if expected_status == 0:
            self.assertIn("[SUCCESS]", result.stdout)
            self.assertNotIn("[ERROR]", result.stdout)
        else:
            self.assertIn("[FAIL]", result.stdout)
            self.assertNotIn("[SUCCESS]", result.stdout)
        return result.stdout

    def test_empty_directory_succeeds(self):
        self.run_validator(0)

    def test_valid_nested_documents_with_spaces_and_crlf_are_unchanged(self):
        paths = [
            self.write_document("guide.md", document()),
            self.write_document("nested directory/guide with spaces.md", document().replace("\n", "\r\n")),
        ]
        originals = {path: path.read_bytes() for path in paths}
        self.run_validator(0)
        for path, original in originals.items():
            self.assertEqual(path.read_bytes(), original)

    def test_missing_or_misplaced_opening_delimiter_is_rejected(self):
        for content in ("", "# No metadata\n", "\n" + document(), "\ufeff" + document(), " ---\n" + document()):
            with self.subTest(content=content[:20]):
                self.write_document("invalid.md", content)
                output = self.run_validator(1)
                self.assertIn("./invalid.md: Missing opening YAML frontmatter", output)
                self.assertIn("1 hard errors", output)

    def test_missing_closing_delimiter_is_rejected(self):
        self.write_document("invalid.md", "---\ntitle: Example\n--\n")
        output = self.run_validator(1)
        self.assertIn("./invalid.md: Missing closing YAML frontmatter", output)
        self.assertIn("1 hard errors", output)

    def test_each_required_field_must_be_present(self):
        for field in FIELDS:
            with self.subTest(field=field):
                fields = {key: value for key, value in FIELDS.items() if key != field}
                self.write_document("invalid.md", document(fields))
                output = self.run_validator(1)
                self.assertIn(f"Missing or empty '{field}'", output)
                self.assertIn("1 hard errors", output)

    def test_each_required_field_rejects_empty_values(self):
        for field in FIELDS:
            for value in ("", "   ", '""', "''", "[]"):
                with self.subTest(field=field, value=value):
                    self.write_document("invalid.md", document({**FIELDS, field: value}))
                    output = self.run_validator(1)
                    self.assertIn(f"'{field}'", output)
                    self.assertIn("1 hard errors", output)

    def test_body_fields_cannot_satisfy_missing_frontmatter_fields(self):
        self.write_document("invalid.md", "---\n---\n" + document())
        output = self.run_validator(1)
        self.assertIn("5 hard errors", output)

    def test_first_duplicate_field_cannot_be_rescued_by_later_value(self):
        self.write_document("invalid.md", document().replace("type: documentation", "type:\ntype: documentation"))
        output = self.run_validator(1)
        self.assertIn("Missing or empty 'type'", output)
        self.assertIn("1 hard errors", output)

    def test_reports_errors_across_files_and_fields(self):
        self.write_document("no-opening.md", "# Invalid\n")
        self.write_document("no-closing.md", "---\n")
        self.write_document("empty-fields.md", document({key: "" for key in FIELDS}))
        self.write_document("valid.md", document())
        output = self.run_validator(1)
        self.assertEqual(output.count("[ERROR]"), 7)
        self.assertIn("7 hard errors", output)
        for filename in ("no-opening.md", "no-closing.md", "empty-fields.md"):
            self.assertIn(filename, output)

    def test_reserved_files_dependencies_and_non_markdown_are_excluded(self):
        for relative in (
            "index.md", "log.md", "nested/index.md", "nested/log.md",
            ".git/invalid.md", ".venv/invalid.md", "node_modules/invalid.md",
            ".pytest_cache/invalid.md", "nested/node_modules/invalid.md", "notes.txt",
        ):
            self.write_document(relative, "No frontmatter\n")
        self.write_document("ordinary.md", document())
        self.run_validator(0)

    def test_similarly_named_directories_are_still_scanned(self):
        self.write_document("node_modules_backup/invalid.md", "No frontmatter\n")
        output = self.run_validator(1)
        self.assertIn("node_modules_backup/invalid.md", output)

    def test_legacy_citation_headers_warn_without_failing(self):
        for heading in ("# Citations", "# Sources"):
            with self.subTest(heading=heading):
                self.write_document("guide.md", document(body=heading + "\n\nLegacy source.\n"))
                output = self.run_validator(0)
                self.assertIn("[WARN]", output)
                self.assertIn("Migrate to frontmatter 'sources:'", output)


if __name__ == "__main__":
    unittest.main()
