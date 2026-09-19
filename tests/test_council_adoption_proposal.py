"""Tests for the Council of High Intelligence adoption proposal."""

import pathlib
import re
import unittest

import yaml


def _find_repo_root(start: pathlib.Path) -> pathlib.Path:
    current = start.resolve()
    for parent in (current, *current.parents):
        if (parent / ".git").exists():
            return parent
    raise RuntimeError("Could not locate repository root (.git not found)")


def _extract_frontmatter(path: pathlib.Path) -> dict:
    content = path.read_text(encoding="utf-8")
    if not content.startswith("---\n"):
        raise AssertionError(f"{path} must start with an OKF frontmatter fence")

    _, raw_frontmatter, _ = content.split("---", 2)
    frontmatter = yaml.safe_load(raw_frontmatter)
    if not isinstance(frontmatter, dict):
        raise AssertionError(f"{path} frontmatter must parse as a mapping")
    return frontmatter


def _find_nav_section(nav: list, label: str) -> list:
    for item in nav:
        if isinstance(item, dict) and label in item:
            section = item[label]
            if isinstance(section, list):
                return section
    raise AssertionError(f"mkdocs.yml has no {label!r} navigation section")


REPO_ROOT = _find_repo_root(pathlib.Path(__file__).parent)
PROPOSAL_RELATIVE_PATH = pathlib.Path(
    "docs/governance/COUNCIL-OF-HIGH-INTELLIGENCE-DSOM-ADOPTION-PROPOSAL.md"
)
MKDOCS_RELATIVE_PATH = pathlib.Path(
    "governance/COUNCIL-OF-HIGH-INTELLIGENCE-DSOM-ADOPTION-PROPOSAL.md"
)
PROPOSAL_PATH = REPO_ROOT / PROPOSAL_RELATIVE_PATH

PERSONAS = {
    "Aristotle",
    "Socrates",
    "Sun Tzu",
    "Ada Lovelace",
    "Marcus Aurelius",
    "Machiavelli",
    "Lao Tzu",
    "Richard Feynman",
    "Linus Torvalds",
    "Miyamoto Musashi",
    "Alan Watts",
    "Andrej Karpathy",
    "Ilya Sutskever",
    "Daniel Kahneman",
    "Donella Meadows",
    "Charlie Munger",
    "Nassim Taleb",
    "Dieter Rams",
}

DOMAIN_TRIADS = {
    "architecture",
    "strategy",
    "ethics",
    "debugging",
    "risk",
    "shipping",
    "product",
    "founder",
    "ai",
    "ai-product",
    "ai-safety",
    "decision",
    "systems",
    "uncertainty",
    "design",
    "economics",
    "bias",
}


class CouncilProposalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.content = PROPOSAL_PATH.read_text(encoding="utf-8")
        cls.frontmatter = _extract_frontmatter(PROPOSAL_PATH)

    def test_proposal_has_expected_okf_identity(self):
        self.assertFalse(PROPOSAL_PATH.read_bytes().startswith(b"\xef\xbb\xbf"))
        self.assertEqual(self.frontmatter["okf_version"], 0.1)
        self.assertEqual(self.frontmatter["type"], "governance_proposal")
        self.assertEqual(
            self.frontmatter["title"],
            "Council of High Intelligence: DSOM Adoption Proposal & Architectural Design",
        )
        self.assertEqual(
            self.frontmatter["resource"],
            f"file:///{PROPOSAL_RELATIVE_PATH.as_posix()}",
        )
        self.assertTrue(
            {"dsom", "governance", "council-of-intelligence", "deliberation"}
            <= set(self.frontmatter["topics"])
        )

    def test_persona_table_defines_exactly_eighteen_unique_members(self):
        persona_section = self.content.split(
            "### 1.1 The 18 Analytical Persona Lenses", 1
        )[1].split("### 1.2 Deliberation Modes & Domain Triads", 1)[0]
        names = re.findall(r"^\| \*\*(.+?)\*\* \|", persona_section, re.MULTILINE)

        self.assertEqual(len(names), 18)
        self.assertEqual(len(names), len(set(names)))
        self.assertEqual(set(names), PERSONAS)

    def test_all_modes_and_domain_triads_are_documented(self):
        modes_section = self.content.split(
            "### 1.2 Deliberation Modes & Domain Triads", 1
        )[1].split("### 1.3 Protocol Protections & Output Standards", 1)[0]
        modes = set(re.findall(r"\*\*(Full|Quick|Duo|Triad) Mode", modes_section))
        domain_line = next(
            line for line in modes_section.splitlines() if line.startswith("   - `")
        )
        domains = set(re.findall(r"`([a-z]+(?:-[a-z]+)?)`", domain_line))

        self.assertEqual(modes, {"Full", "Quick", "Duo", "Triad"})
        self.assertEqual(domains, DOMAIN_TRIADS)

    def test_architecture_maps_every_dsom_state_and_deliberation_phase(self):
        for state in ("Active State", "Twilight State", "Deep State"):
            with self.subTest(state=state):
                self.assertIn(state, self.content)

        for phase in range(1, 5):
            with self.subTest(phase=phase):
                self.assertRegex(self.content, rf"Phase {phase}:")

        for proposed_path in (
            ".agents/skills/council-of-intelligence/SKILL.md",
            "tools/council_emulator.py",
            "tools/mcp/server.py",
            "tests/test_council_emulator.py",
        ):
            with self.subTest(path=proposed_path):
                self.assertIn(f"`{proposed_path}`", self.content)


class CouncilProposalNavigationTests(unittest.TestCase):
    def test_proposal_is_registered_in_every_changed_navigation_manifest(self):
        expected_entries = {
            REPO_ROOT / "SUMMARY.md": (
                "[🏛️ Council of High Intelligence DSOM Adoption Proposal]"
                f"({PROPOSAL_RELATIVE_PATH.as_posix()})"
            ),
            REPO_ROOT / "docs" / "SUMMARY.md": (
                "[Council of High Intelligence Proposal]"
                f"({MKDOCS_RELATIVE_PATH.as_posix()})"
            ),
            REPO_ROOT / "llms.txt": (
                "[Council of High Intelligence DSOM Adoption Proposal]"
                f"({PROPOSAL_RELATIVE_PATH.as_posix()})"
            ),
        }

        for path, entry in expected_entries.items():
            with self.subTest(path=path.relative_to(REPO_ROOT)):
                content = path.read_text(encoding="utf-8")
                self.assertEqual(content.count(entry), 1)

    def test_mkdocs_registers_resolvable_path_once_under_governance(self):
        config = yaml.safe_load((REPO_ROOT / "mkdocs.yml").read_text(encoding="utf-8"))
        governance = _find_nav_section(config["nav"], "Governance")
        expected = {
            "Council of High Intelligence Proposal": MKDOCS_RELATIVE_PATH.as_posix()
        }

        self.assertEqual(governance.count(expected), 1)
        self.assertTrue((REPO_ROOT / "docs" / expected[next(iter(expected))]).is_file())

    def test_docs_relative_manifests_reject_root_relative_proposal_path(self):
        stale_entry = PROPOSAL_RELATIVE_PATH.as_posix()
        for path in (REPO_ROOT / "mkdocs.yml", REPO_ROOT / "docs" / "SUMMARY.md"):
            with self.subTest(path=path.relative_to(REPO_ROOT)):
                self.assertNotIn(stale_entry, path.read_text(encoding="utf-8"))

    def test_start_here_exposes_entry_point_and_public_url(self):
        content = (REPO_ROOT / "START-HERE.md").read_text(encoding="utf-8")
        public_url = (
            "https://linuxmalaysia.github.io/deep-state-of-mind-for-my-ai/"
            "governance/COUNCIL-OF-HIGH-INTELLIGENCE-DSOM-ADOPTION-PROPOSAL/"
        )

        self.assertEqual(
            content.count(
                "## 24. The Council of High Intelligence Deliberation Entry Point"
            ),
            1,
        )
        self.assertIn(f"]({PROPOSAL_RELATIVE_PATH.as_posix()})", content)
        self.assertIn(f"]({public_url})", content)

    def test_palace_registry_routes_proposal_to_dsom_protocol_room(self):
        content = (REPO_ROOT / ".agents/brain/palace_registry.md").read_text(
            encoding="utf-8"
        )
        room = content.split("- **Room: `room_dsom_protocol`**", 1)[1].split(
            "- **Room:", 1
        )[0]

        self.assertIn("Council of High Intelligence proposal", room)


class WalkthroughFrontmatterTests(unittest.TestCase):
    def test_compacted_okf_v02_metadata_preserves_nested_provenance(self):
        frontmatter = _extract_frontmatter(
            REPO_ROOT / ".agents/brain/walkthrough.md"
        )

        self.assertEqual(frontmatter["okf_version"], 0.2)
        self.assertEqual(frontmatter["spec_version"], "0.2")
        self.assertEqual(frontmatter["concept_id"], "dsom_session_walkthrough")
        self.assertEqual(frontmatter["status"], "stable")
        self.assertEqual(frontmatter["sources"][0]["id"], "dsom_task_ledger")
        self.assertEqual(
            frontmatter["sources"][0]["url"], "file:///.agents/brain/task.md"
        )
        self.assertEqual(frontmatter["generated"]["by"], "DSOM Session Workflow")


if __name__ == "__main__":
    unittest.main()
