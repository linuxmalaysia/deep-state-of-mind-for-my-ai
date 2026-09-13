"""Tests for the DSOM adoption of OKF v0.2 Attested Computations."""

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


REPO_ROOT = _find_repo_root(pathlib.Path(__file__).parent)
ATTESTED_COMP_GUIDE_PATH = (
    REPO_ROOT / "docs" / "explanation" / "attested-computations-okf.md"
)
OKF_ADOPTION_DOCS_PATH = REPO_ROOT / "docs" / "OKF-ADOPTION-GUIDE.md"
OKF_ADOPTION_REF_PATH = REPO_ROOT / "references" / "OKF-ADOPTION-GUIDE.md"
MKDOCS_PATH = REPO_ROOT / "mkdocs.yml"
DOCS_SUMMARY_PATH = REPO_ROOT / "docs" / "SUMMARY.md"
ROOT_SUMMARY_PATH = REPO_ROOT / "SUMMARY.md"
LLMS_TXT_PATH = REPO_ROOT / "llms.txt"
START_HERE_PATH = REPO_ROOT / "START-HERE.md"
EXPLANATION_INDEX_PATH = REPO_ROOT / "docs" / "explanation" / "index.md"
OKF_SKILL_PATH = (
    REPO_ROOT / ".agents" / "skills" / "okf-v02-adoption-engineer" / "SKILL.md"
)

ATTESTED_HEADING = "### OKF v0.2 Attested Computations (Verifiable AI Knowledge)"
LIFECYCLE_STEPS = ["Discover", "Load", "Parameterize", "Execute", "Attest", "Gate"]


def _read(path: pathlib.Path) -> str:
    return path.read_text(encoding="utf-8")


def _extract_frontmatter(content: str):
    """Return strictly fenced YAML frontmatter, or ``None`` when invalid."""
    lines = content.splitlines()
    if not lines or lines[0] != "---":
        return None
    try:
        closing_fence = lines.index("---", 1)
        return yaml.safe_load("\n".join(lines[1:closing_fence]))
    except (ValueError, yaml.YAMLError):
        return None


def _extract_between(content: str, start_marker: str, end_marker: str) -> str:
    start = content.index(start_marker) + len(start_marker)
    end = content.index(end_marker, start)
    return content[start:end].strip()


def _lifecycle_steps(content: str) -> list[tuple[int, str]]:
    return [
        (int(number), name)
        for number, name in re.findall(
            r"^(\d+)\. \*\*([A-Za-z]+):\*\*", content, flags=re.MULTILINE
        )
    ]


def _mkdocs_targets(node, label: str) -> list[str]:
    targets = []
    if isinstance(node, list):
        for item in node:
            targets.extend(_mkdocs_targets(item, label))
    elif isinstance(node, dict):
        for key, value in node.items():
            if key == label and isinstance(value, str):
                targets.append(value)
            targets.extend(_mkdocs_targets(value, label))
    return targets


class AttestedComputationsOkfTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.guide = _read(ATTESTED_COMP_GUIDE_PATH)

    def test_explanation_guide_has_complete_okf_v02_frontmatter(self):
        self.assertTrue(ATTESTED_COMP_GUIDE_PATH.is_file())
        self.assertTrue(self.guide.startswith("---\n"), "frontmatter must start at byte 0")
        self.assertFalse(self.guide.startswith("\ufeff"), "frontmatter must not have a BOM")

        frontmatter = _extract_frontmatter(self.guide)
        self.assertIsInstance(frontmatter, dict)
        self.assertEqual(frontmatter["okf_version"], 0.2)
        self.assertEqual(frontmatter["spec_version"], "0.2")
        self.assertEqual(frontmatter["concept_id"], "attested_computations_okf")
        self.assertEqual(frontmatter["type"], "explanation")
        self.assertEqual(frontmatter["status"], "stable")
        self.assertRegex(frontmatter["stale_after"], r"^\d{4}-\d{2}-\d{2}$")
        self.assertIn("attested-computation", frontmatter["topics"])

        self.assertGreaterEqual(len(frontmatter["sources"]), 2)
        for source in frontmatter["sources"]:
            with self.subTest(source=source.get("id")):
                self.assertTrue({"id", "title", "author", "url"} <= source.keys())
                self.assertTrue(source["url"].startswith("https://"))
        for trust_signal in ("generated", "verified"):
            self.assertTrue({"by", "timestamp"} <= frontmatter[trust_signal].keys())

    def test_embedded_specimen_is_a_complete_attested_computation_contract(self):
        specimen = _extract_between(self.guide, "````yaml\n", "\n````")
        self.assertIn("\n```sql\n", specimen, "outer fence must contain the SQL fence")

        contract = _extract_frontmatter(specimen)
        self.assertIsInstance(contract, dict)
        self.assertEqual(contract["okf_version"], 0.2)
        self.assertEqual(contract["spec_version"], "0.2")
        self.assertEqual(contract["type"], "Attested Computation")
        self.assertEqual(contract["runtime"], "bigquery")
        self.assertEqual(
            contract["parameters"],
            [{"name": "year", "type": "integer", "required": True}],
        )
        self.assertEqual(
            contract["executor"],
            {
                "resource": "references/skills/run-on-bq.md",
                "receipt": ["job_id", "executed_sql", "result"],
            },
        )
        self.assertEqual(
            contract["attester"]["resource"],
            "references/attesters/sql-equality.py",
        )
        self.assertTrue({"generated", "verified", "sources"} <= contract.keys())

        self.assertIn("WHERE fiscal_year = @year", specimen)
        self.assertIn("binds only the declared `parameters`", specimen)

    def test_lifecycle_is_documented_once_in_the_required_order(self):
        lifecycle = _extract_between(
            self.guide,
            "## The 6-Step Mechanical Execution & Attestation Lifecycle",
            "## Verification vs. Attestation",
        )
        self.assertEqual(
            _lifecycle_steps(lifecycle),
            list(enumerate(LIFECYCLE_STEPS, start=1)),
        )
        for step in LIFECYCLE_STEPS:
            self.assertEqual(lifecycle.count(f"**{step}:**"), 1)

    def test_verification_and_attestation_remain_distinct(self):
        distinction = _extract_between(
            self.guide,
            "## Verification vs. Attestation",
            "## Conclusion & Impact on DSOM v0.2",
        )
        self.assertIn("Doc-Level Verification (`verified`)", distinction)
        self.assertIn("matches business policy", distinction)
        self.assertIn("Runtime Attestation (`attester`)", distinction)
        self.assertIn("specific runtime execution", distinction)
        self.assertIn("deterministic code", distinction)

    def test_adoption_guide_copies_have_identical_attestation_sections(self):
        sections = []
        for path in (OKF_ADOPTION_DOCS_PATH, OKF_ADOPTION_REF_PATH):
            content = _read(path)
            with self.subTest(path=path.relative_to(REPO_ROOT)):
                self.assertEqual(content.count(ATTESTED_HEADING), 1)
                section = _extract_between(content, ATTESTED_HEADING, "> [!TIP]")
                lifecycle = _extract_between(
                    section,
                    "#### The 6-Step Mechanical Execution & Attestation Lifecycle",
                    "#### Verification vs. Attestation",
                )
                self.assertEqual(
                    _lifecycle_steps(lifecycle),
                    list(enumerate(LIFECYCLE_STEPS, start=1)),
                )
                for concept in (
                    "type: Attested Computation",
                    "runtime",
                    "parameters",
                    "executor",
                    "attester",
                    "Doc-Level Verification",
                    "Runtime Attestation",
                ):
                    self.assertIn(concept, section)
                sections.append(section)

        self.assertEqual(sections[0], sections[1])

    def test_navigation_registrations_are_unique_and_resolve(self):
        expected_links = (
            (
                DOCS_SUMMARY_PATH,
                "* [Attested Computations in OKF v0.2](explanation/attested-computations-okf.md)",
                REPO_ROOT / "docs" / "explanation" / "attested-computations-okf.md",
            ),
            (
                ROOT_SUMMARY_PATH,
                "* [🔒 Attested Computations in OKF v0.2](docs/explanation/attested-computations-okf.md)",
                REPO_ROOT / "docs" / "explanation" / "attested-computations-okf.md",
            ),
            (
                LLMS_TXT_PATH,
                "[Attested Computations in OKF v0.2](docs/explanation/attested-computations-okf.md)",
                REPO_ROOT / "docs" / "explanation" / "attested-computations-okf.md",
            ),
            (
                EXPLANATION_INDEX_PATH,
                "[Attested Computations in OKF v0.2](attested-computations-okf.md)",
                REPO_ROOT / "docs" / "explanation" / "attested-computations-okf.md",
            ),
        )
        for index_path, link, target in expected_links:
            with self.subTest(index=index_path.relative_to(REPO_ROOT)):
                self.assertEqual(_read(index_path).count(link), 1)
                self.assertTrue(target.is_file())

        mkdocs = yaml.safe_load(_read(MKDOCS_PATH))
        targets = _mkdocs_targets(mkdocs["nav"], "Attested Computations in OKF v0.2")
        self.assertEqual(targets, ["explanation/attested-computations-okf.md"])
        self.assertTrue((REPO_ROOT / "docs" / targets[0]).is_file())

    def test_start_here_exposes_the_published_guide_once(self):
        link = (
            "[`https://linuxmalaysia.github.io/deep-state-of-mind-for-my-ai/"
            "explanation/attested-computations-okf/`]"
            "(https://linuxmalaysia.github.io/deep-state-of-mind-for-my-ai/"
            "explanation/attested-computations-okf/)"
        )
        self.assertEqual(_read(START_HERE_PATH).count(link), 1)

    def test_okf_v02_skill_declares_the_attestation_contract_fields(self):
        skill_content = _read(OKF_SKILL_PATH)
        frontmatter = _extract_frontmatter(skill_content)
        self.assertIsInstance(frontmatter, dict)
        document_type = frontmatter["inputs"]["document_type"]
        self.assertIn("Attested Computation", document_type["description"])
        self.assertEqual(document_type["type"], "string")

        directive = _extract_between(
            skill_content,
            "- **Attestation Registry**:",
            "3. **Content Alignment Rules**:",
        )
        self.assertIn("`type: Attested Computation`", directive)
        for field in ("runtime", "parameters", "executor", "attester"):
            self.assertIn(f"`{field}`", directive)
        self.assertIn("without embedding raw runtimes", directive)


if __name__ == "__main__":
    unittest.main()
