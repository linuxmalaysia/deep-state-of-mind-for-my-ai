"""
Unit tests for Attested Computations in Open Knowledge Format (OKF v0.2)
incorporation into the DSOM workspace.
"""
import pathlib
import unittest
import yaml


def _find_repo_root(start: pathlib.Path) -> pathlib.Path:
    current = start.resolve()
    for parent in [current, *current.parents]:
        if (parent / ".git").exists():
            return parent
    raise RuntimeError("Could not locate repository root (.git not found)")


REPO_ROOT = _find_repo_root(pathlib.Path(__file__).parent)
ATTESTED_COMP_GUIDE_PATH = REPO_ROOT / "docs" / "explanation" / "attested-computations-okf.md"
OKF_ADOPTION_DOCS_PATH = REPO_ROOT / "docs" / "OKF-ADOPTION-GUIDE.md"
OKF_ADOPTION_REF_PATH = REPO_ROOT / "references" / "OKF-ADOPTION-GUIDE.md"
MKDOCS_PATH = REPO_ROOT / "mkdocs.yml"
DOCS_SUMMARY_PATH = REPO_ROOT / "docs" / "SUMMARY.md"
ROOT_SUMMARY_PATH = REPO_ROOT / "SUMMARY.md"
LLMS_TXT_PATH = REPO_ROOT / "llms.txt"
EXPLANATION_INDEX_PATH = REPO_ROOT / "docs" / "explanation" / "index.md"
OKF_SKILL_PATH = REPO_ROOT / ".agents" / "skills" / "okf-v02-adoption-engineer" / "SKILL.md"


def _extract_frontmatter(content: str):
    if not content.startswith("---"):
        return None
    try:
        parts = content.split("---", 2)
        if len(parts) >= 3:
            return yaml.safe_load(parts[1])
    except Exception:
        pass
    return None


class AttestedComputationsOkfTests(unittest.TestCase):
    def test_explanation_guide_exists_and_is_valid_okf_v02(self):
        self.assertTrue(ATTESTED_COMP_GUIDE_PATH.is_file())
        content = ATTESTED_COMP_GUIDE_PATH.read_text(encoding="utf-8")
        frontmatter = _extract_frontmatter(content)
        self.assertIsInstance(frontmatter, dict)
        self.assertEqual(frontmatter.get("okf_version"), 0.2)
        self.assertEqual(frontmatter.get("spec_version"), "0.2")
        self.assertEqual(frontmatter.get("concept_id"), "attested_computations_okf")
        self.assertEqual(frontmatter.get("type"), "explanation")
        self.assertIn("attested-computation", frontmatter.get("topics", []))
        self.assertIn("Attested Computations in Open Knowledge Format", frontmatter.get("title", ""))

    def test_adoption_guides_contain_attested_computations_section(self):
        docs_content = OKF_ADOPTION_DOCS_PATH.read_text(encoding="utf-8")
        ref_content = OKF_ADOPTION_REF_PATH.read_text(encoding="utf-8")

        for content in (docs_content, ref_content):
            self.assertIn("### OKF v0.2 Attested Computations (Verifiable AI Knowledge)", content)
            self.assertIn("type: Attested Computation", content)
            self.assertIn("The 6-Step Mechanical Execution & Attestation Lifecycle", content)
            self.assertIn("Verification vs. Attestation", content)

    def test_navigation_and_indexing_registrations(self):
        mkdocs_content = MKDOCS_PATH.read_text(encoding="utf-8")
        self.assertIn("Attested Computations in OKF v0.2: explanation/attested-computations-okf.md", mkdocs_content)

        docs_summary_content = DOCS_SUMMARY_PATH.read_text(encoding="utf-8")
        self.assertIn("* [Attested Computations in OKF v0.2](explanation/attested-computations-okf.md)", docs_summary_content)

        root_summary_content = ROOT_SUMMARY_PATH.read_text(encoding="utf-8")
        self.assertIn("attested-computations-okf.md", root_summary_content)

        llms_txt_content = LLMS_TXT_PATH.read_text(encoding="utf-8")
        self.assertIn("[Attested Computations in OKF v0.2](docs/explanation/attested-computations-okf.md)", llms_txt_content)

        explanation_index_content = EXPLANATION_INDEX_PATH.read_text(encoding="utf-8")
        self.assertIn("[Attested Computations in OKF v0.2](attested-computations-okf.md)", explanation_index_content)

    def test_okf_v02_skill_references_attested_computation(self):
        skill_content = OKF_SKILL_PATH.read_text(encoding="utf-8")
        self.assertIn("Attested Computation", skill_content)


if __name__ == "__main__":
    unittest.main()
