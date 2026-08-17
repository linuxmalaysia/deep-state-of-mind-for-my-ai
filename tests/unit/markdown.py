"""
Markdown OKF schema, DSOM governance footers, and UK English spelling unit tests.
"""
import os
import pathlib
import re
import unittest
import yaml

def _find_repo_root(start: pathlib.Path) -> pathlib.Path:
    """
    Locate the repository root containing a `.git` entry.
    
    Parameters:
    	start (pathlib.Path): Path from which to search the directory hierarchy.
    
    Returns:
    	pathlib.Path: The nearest ancestor containing a `.git` entry.
    
    Raises:
    	RuntimeError: If no repository root is found.
    """
    current = start.resolve()
    for parent in [current, *current.parents]:
        if (parent / ".git").exists():
            return parent
    raise RuntimeError("Could not locate repository root (.git not found)")

REPO_ROOT = _find_repo_root(pathlib.Path(__file__).parent)
FRONTMATTER_RE = re.compile(r"\A---\s*\r?\n(.*?)(?:\r?\n)?---\s*(?:\r?\n|\Z)", re.DOTALL)


class TestMarkdownCompliance(unittest.TestCase):
    """Markdown schema, governance footers, and spelling compliance tests."""

    def test_markdown_okf_compliance(self):
        """Verify that repository Markdown files use valid UTF-8 and required OKF v0.1 frontmatter fields."""
        exclude_files = {"CLAUDE.md"}
        exclude_dirs = {".git", "node_modules", ".pytest_cache", "venv", ".venv", "openwiki", "site"}

        md_files = []
        for dirpath, dirnames, filenames in os.walk(REPO_ROOT):
            dirnames[:] = [d for d in dirnames if d not in exclude_dirs]
            for filename in filenames:
                if filename.endswith(".md") and filename not in exclude_files:
                    filepath = pathlib.Path(dirpath) / filename
                    if not filepath.is_symlink():
                        # Handle Windows git text symlinks
                        try:
                            content = filepath.read_text(encoding="utf-8").strip()
                            if content.startswith("../") and "\n" not in content and len(content) < 250:
                                continue
                        except Exception:
                            pass
                        md_files.append(filepath)

        REQUIRED_FIELDS = {"okf_version", "type", "title", "timestamp", "topics"}

        for md_file in md_files:
            with self.subTest(file=md_file.relative_to(REPO_ROOT).as_posix()):
                raw_bytes = md_file.read_bytes()
                self.assertFalse(raw_bytes.startswith(b"\xef\xbb\xbf"), f"{md_file.name} must not contain UTF-8 BOM")

                text = raw_bytes.decode("utf-8")
                self.assertTrue(text.startswith("---\n") or text.startswith("---\r\n"), f"{md_file.name} must begin with frontmatter fence ---")

                match = FRONTMATTER_RE.match(text)
                self.assertIsNotNone(match, f"{md_file.name} must contain valid frontmatter block")

                data = yaml.safe_load(match.group(1))
                self.assertIsInstance(data, dict, f"Frontmatter in {md_file.name} must parse to a mapping")

                for field in REQUIRED_FIELDS:
                    self.assertIn(field, data, f"Frontmatter in {md_file.name} missing required field '{field}'")

    def test_markdown_governance_footers(self):
        """Verify presence of governance footers or copyright signatures in Markdown docs."""
        docs_dir = REPO_ROOT / "docs"
        doc_files = [p for p in docs_dir.glob("**/*.md") if p.is_file() and not p.is_symlink()]
        self.assertGreater(len(doc_files), 0, "docs directory must contain Markdown files")

        for doc_file in doc_files:
            with self.subTest(file=doc_file.relative_to(REPO_ROOT).as_posix()):
                text = doc_file.read_text(encoding="utf-8")
                has_license_ref = any(term in text for term in ("GPL", "License", "Copyright", "DSOM", "Deep State of Mind", "Governance"))
                self.assertTrue(has_license_ref, f"{doc_file.name} should reference license/DSOM governance")

    def test_uk_english_documentation_spellings(self):
        """Verify UK English spelling conventions across documentation corpus."""
        doc_files = [REPO_ROOT / "README.md"] + [p for p in (REPO_ROOT / "docs").glob("**/*.md") if p.is_file() and not p.is_symlink()]
        UK_TERMS = ["organisation", "optimisation", "behaviour", "standardised", "localised", "categorises"]

        combined_text = ""
        for doc in doc_files:
            if doc.exists():
                combined_text += doc.read_text(encoding="utf-8").lower() + "\n"

        for uk_term in UK_TERMS:
            with self.subTest(term=uk_term):
                self.assertIn(
                    uk_term,
                    combined_text,
                    f"Documentation corpus should incorporate standard UK English spelling '{uk_term}'"
                )


if __name__ == "__main__":
    unittest.main()
