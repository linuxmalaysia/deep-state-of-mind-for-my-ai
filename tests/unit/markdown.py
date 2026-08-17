"""
Markdown OKF schema, DSOM governance footers, and UK English spelling unit tests.
"""
import os
import pathlib
import re
import unittest
import yaml

def _find_repo_root(start: pathlib.Path) -> pathlib.Path:
    current = start.resolve()
    for parent in [current, *current.parents]:
        if (parent / ".git").exists():
            return parent
    raise RuntimeError("Could not locate repository root (.git not found)")


class TestMarkdownCompliance(unittest.TestCase):
    """Markdown schema, governance footers, and spelling compliance tests."""

    @classmethod
    def setUpClass(cls):
        cls.repo_root = _find_repo_root(pathlib.Path(__file__).parent)

    def _discover_md_files(self) -> list[pathlib.Path]:
        exclude_files = {"CLAUDE.md", "CHANGELOG.md", "HISTORY.md"}
        exclude_dirs = {".git", "node_modules", ".pytest_cache", "venv", ".venv", "openwiki", "site", "references"}

        md_files = []
        for dirpath, dirnames, filenames in os.walk(self.repo_root):
            dirnames[:] = [d for d in dirnames if d not in exclude_dirs]
            for filename in filenames:
                if filename.endswith(".md") and filename not in exclude_files:
                    filepath = pathlib.Path(dirpath) / filename
                    if not filepath.is_symlink():
                        try:
                            content = filepath.read_text(encoding="utf-8").strip()
                            if content.startswith("../") and "\n" not in content and len(content) < 250:
                                continue
                        except (OSError, UnicodeDecodeError) as err:
                            self.fail(f"Failed to read markdown file {filepath.relative_to(self.repo_root)}: {err}")
                        md_files.append(filepath)
        return md_files

    def test_markdown_okf_compliance(self):
        """Verify Markdown files adhere to OKF v0.1 schema frontmatter rules."""
        FRONTMATTER_RE = re.compile(r"\A---\s*\r?\n(.*?)(?:\r?\n)?---\s*(?:\r?\n|\Z)", re.DOTALL)
        REQUIRED_FIELDS = {"okf_version", "type", "title", "timestamp", "topics"}

        md_files = self._discover_md_files()

        for md_file in md_files:
            with self.subTest(file=md_file.relative_to(self.repo_root).as_posix()):
                raw_bytes = md_file.read_bytes()
                self.assertFalse(raw_bytes.startswith(b"\xef\xbb\xbf"), f"{md_file.name} must not contain UTF-8 BOM")

                text = raw_bytes.decode("utf-8")
                self.assertTrue(text.startswith("---\n") or text.startswith("---\r\n"), f"{md_file.name} must begin with frontmatter fence ---")

                match = FRONTMATTER_RE.match(text)
                self.assertIsNotNone(match, f"{md_file.name} must contain valid frontmatter block")

                raw_fm = match.group(1)
                data = yaml.safe_load(raw_fm)
                self.assertIsInstance(data, dict, f"Frontmatter in {md_file.name} must parse to a mapping")

                for field in REQUIRED_FIELDS:
                    self.assertIn(field, data, f"Frontmatter in {md_file.name} missing required field '{field}'")

                # Verify okf_version equals 0.1
                self.assertEqual(data.get("okf_version"), 0.1, f"okf_version in {md_file.name} must equal 0.1")

                # Verify timestamp uses a double-quoted YAML scalar
                if "timestamp:" in raw_fm:
                    self.assertRegex(
                        raw_fm,
                        r'timestamp:\s*"[^"]+"',
                        f"Timestamp field in {md_file.name} must be a double-quoted YAML scalar",
                    )

    def test_markdown_governance_footers(self):
        """Verify presence of governance footers or copyright signatures in Markdown docs."""
        docs_dir = self.repo_root / "docs"
        doc_files = [p for p in docs_dir.glob("**/*.md") if p.is_file() and not p.is_symlink()]
        self.assertGreater(len(doc_files), 0, "docs directory must contain Markdown files")

        for doc_file in doc_files:
            with self.subTest(file=doc_file.relative_to(self.repo_root).as_posix()):
                text = doc_file.read_text(encoding="utf-8")
                has_license_ref = any(term in text for term in ("GPL", "License", "Copyright", "DSOM", "Deep State of Mind", "Governance"))
                self.assertTrue(has_license_ref, f"{doc_file.name} should reference license/DSOM governance")

    def test_uk_english_documentation_spellings(self):
        """Verify UK English spelling conventions across documentation corpus and reject unapproved US variants."""
        doc_files = self._discover_md_files()

        UK_TERMS = ["organisation", "optimisation", "behaviour", "standardised", "localised", "categorises"]
        US_UK_PAIRS = [
            (r"\borganization\b", "organisation"),
            (r"\boptimization\b", "optimisation"),
            (r"\bbehavior\b", "behaviour"),
            (r"\bstandardized\b", "standardised"),
            (r"\blocalized\b", "localised"),
            (r"\bcategorizes\b", "categorises"),
        ]

        combined_text = ""
        for doc in doc_files:
            if doc.exists():
                text = doc.read_text(encoding="utf-8")
                clean_lines = []
                for line in text.splitlines():
                    # Skip lines that are URLs, external citations, or specific legacy document titles/citations
                    if any(kw in line.lower() for kw in ("http://", "https://", "snyk organisation", "org id", "snyk organization", "optimization.md", "engine-optimization", "mind optimization", "engine optimization", "agentic optimization")):
                        continue
                    clean_lines.append(line)
                combined_text += "\n".join(clean_lines).lower() + "\n"

        # Assert UK English terms are present in corpus
        for uk_term in UK_TERMS:
            with self.subTest(uk_term=uk_term):
                self.assertIn(
                    uk_term,
                    combined_text,
                    f"Documentation corpus should incorporate standard UK English spelling '{uk_term}'",
                )

        # Reject prohibited US spellings
        for us_pattern, uk_replacement in US_UK_PAIRS:
            with self.subTest(us_pattern=us_pattern):
                matches = re.findall(us_pattern, combined_text)
                self.assertEqual(
                    len(matches),
                    0,
                    f"Found prohibited US spelling pattern '{us_pattern}' in documentation text. Expected UK variant '{uk_replacement}'.",
                )


if __name__ == "__main__":
    unittest.main()
