"""
Unit tests for the mkdocs.yml nav path corrections.

mkdocs resolves nav entries relative to `docs_dir` (which defaults to the
`docs/` folder). Several nav entries used to be written as
`docs/governance/FOO.md`, `docs/RITUAL-OF-TRANSITION.md`, etc. -
i.e. they included the `docs/` prefix a second time. Since MkDocs already
resolves these paths relative to `docs/`, the effective (and incorrect)
lookup was `docs/docs/governance/FOO.md`, which does not exist and would
404 when the site was built.

This PR rewrites those nav entries to be relative to `docs/` (dropping the
redundant `docs/` prefix), e.g. `governance/FOO.md`, `RITUAL-OF-TRANSITION.md`.

These tests validate:
1. `mkdocs.yml` exists and is non-empty.
2. Every corrected nav entry now uses the new, doubly-prefix-free path.
3. None of the old, doubly-prefixed (`docs/...`) paths remain for the
   entries this PR touched (regression guard against reverting the fix).
4. Every corrected nav path actually resolves to a real file under
   `docs/` (the true test of whether MkDocs would 404).
5. Where PyYAML is available, the nav structure is also validated
   structurally (section membership, exact label -> path mapping) rather
   than just textually.
"""
import pathlib
import re
import unittest

try:
    import yaml  # type: ignore

    HAS_YAML = True
except ImportError:  # pragma: no cover - environment dependent
    HAS_YAML = False


def _find_repo_root(start: pathlib.Path) -> pathlib.Path:
    current = start.resolve()
    for parent in [current, *current.parents]:
        if (parent / ".git").exists():
            return parent
    raise RuntimeError("Could not locate repository root (.git not found)")


REPO_ROOT = _find_repo_root(pathlib.Path(__file__).parent)
MKDOCS_PATH = REPO_ROOT / "mkdocs.yml"
DOCS_DIR = REPO_ROOT / "docs"

# (nav label, corrected path relative to docs/, old doubly-prefixed path)
CORRECTED_GOVERNANCE_ENTRIES = [
    ("AI Initialization Sequence", "governance/AI-INITIALIZATION-SEQUENCE.md"),
    ("AI Master Protocol", "governance/AI-MASTER-PROTOCOL.md"),
    ("DSOM Automated State Sync", "governance/DSOM-AUTOMATED-STATE-SYNC.md"),
    ("Native MCP Architecture", "governance/DSOM-MCP-ARCHITECTURE.md"),
    (
        "GitOps · AIOps · Ansible Strategy",
        "governance/GITOPS-AIOPS-ANSIBLE-STRATEGY.md",
    ),
    ("Operational Guide", "governance/OPERATIONAL-GUIDE.md"),
    ("NOSS Integration Guide", "governance/NOSS-INTEGRATION-GUIDE.md"),
    ("Python UV Environment Guide", "governance/PYTHON-UV-ENVIRONMENT-GUIDE.md"),
    ("Automation Audit Ledger", "governance/AUTOMATION-AUDIT-LIST.md"),
    ("Token Efficiency Report", "governance/DSOM-TOKEN-EFFICIENCY-REPORT.md"),
    (
        "Byte-Capped Execution Framework",
        "governance/BYTE-CAPPED-EXECUTION-FRAMEWORK.md",
    ),
    (
        "Ingestion Latency Architecture",
        "governance/DSOM-INGESTION-LATENCY-ARCHITECTURE.md",
    ),
    ("Token Performance Playbook", "governance/DSOM-TOKEN-PERFORMANCE-PLAYBOOK.md"),
    ("Zero-Global Memory Architecture", "governance/ZERO-GLOBAL-MEMORY.md"),
    ("LLM WIKI Adoption Strategy", "governance/LLM-WIKI-ADOPTION.md"),
    ("DSOM Efficiency Protocols", "governance/DSOM-EFFICIENCY-PROTOCOLS.md"),
    ("Knowledge-First Discovery", "governance/SOP-KNOWLEDGE-FIRST-DISCOVERY.md"),
    (
        "GitHub Actions Security Scanning",
        "governance/GITHUB-ACTIONS-SECURITY-SCANNING.md",
    ),
    ("Ritual of Transition", "RITUAL-OF-TRANSITION.md"),
    ("Personalization", "PERSONALIZATION.md"),
]

CORRECTED_AI_SETUP_ENTRIES = [
    (
        "Cognitive Twin Protocol Template",
        "governance/AI-COGNITIVE-TWIN-PROTOCOL.md",
    ),
    ("Reanimation Template", "REANIMATION-PROMPT-TEMPLATE.md"),
    ("Episodic Record Template", "DSOM-EPISODIC-RECORD-TEMPLATE.md"),
    ("Agent Protocols", "governance/MULTI-AGENT-PROTOCOLS.md"),
    ("Gemini DSOM Gem", "HOWTO-CREATE-DSOM-GEMINI-GEM.md"),
    ("Claude", "CLAUDE-SETUP.md"),
    ("DSOM Claude Initialiser", "model-specifics/dsom-claude-initialiser.md"),
    ("Copilot", "COPILOT-SETUP.md"),
]

CORRECTED_ANSIBLE_ENTRIES = [
    ("HOWTO Setup Baseline", "HOWTO-SETUP-ANSIBLE-BASELINE.md"),
    ("HOWTO Setup AlmaLinux 10 WSL2", "HOWTO-SETUP-WSL-ALMALINUX10.md"),
]

ALL_CORRECTED_ENTRIES = (
    CORRECTED_GOVERNANCE_ENTRIES
    + CORRECTED_AI_SETUP_ENTRIES
    + CORRECTED_ANSIBLE_ENTRIES
)


class MkdocsFileTests(unittest.TestCase):
    def test_mkdocs_yml_exists(self):
        self.assertTrue(MKDOCS_PATH.is_file())

    def test_mkdocs_yml_not_empty(self):
        self.assertTrue(MKDOCS_PATH.read_text(encoding="utf-8").strip())


class MkdocsNavCorrectedPathTextTests(unittest.TestCase):
    """Regex/substring based checks that don't require a YAML parser."""

    @classmethod
    def setUpClass(cls):
        cls.content = MKDOCS_PATH.read_text(encoding="utf-8")

    def test_corrected_entries_present_with_docs_relative_paths(self):
        for label, corrected_path in ALL_CORRECTED_ENTRIES:
            with self.subTest(label=label):
                pattern = re.compile(
                    rf"{re.escape(label)}:\s*{re.escape(corrected_path)}\s*$",
                    re.MULTILINE,
                )
                self.assertRegex(
                    self.content,
                    pattern,
                    f"Expected nav entry {label!r} to map to {corrected_path!r}",
                )

    def test_old_doubly_prefixed_docs_paths_are_gone(self):
        # Regression guard: none of the corrected entries should still be
        # reachable via the old "docs/<path>" form anywhere in the file.
        for _, corrected_path in ALL_CORRECTED_ENTRIES:
            old_path = f"docs/{corrected_path}"
            with self.subTest(old_path=old_path):
                self.assertNotIn(
                    old_path,
                    self.content,
                    f"Found stale doubly-prefixed nav path {old_path!r} in mkdocs.yml",
                )

    def test_unrelated_nav_entries_are_unaffected(self):
        # Entries this PR did not touch should be untouched: they were
        # already relative to docs_dir before this PR (e.g. Home, AI Brain,
        # Playbooks, Tools sections) and must not have gained a redundant
        # "docs/" prefix as a side effect of this change.
        for nav_value in (
            "README.md",
            "START-HERE.md",
            "SECURITY.md",
            ".agents/brain/task.md",
            "playbooks/dsom/site.yml",
            "tools-and-automation/audit-pre-flight.md",
        ):
            with self.subTest(nav_value=nav_value):
                self.assertNotIn(f"docs/{nav_value}", self.content)


class MkdocsNavCorrectedPathResolutionTests(unittest.TestCase):
    """Verify every corrected nav path resolves to a real file under docs/.

    This is the behavioural crux of the fix: MkDocs resolves nav values
    relative to docs_dir, so `path.exists()` here mirrors what MkDocs
    itself would do when building the site.
    """

    def test_corrected_paths_resolve_to_existing_files(self):
        for label, corrected_path in ALL_CORRECTED_ENTRIES:
            with self.subTest(label=label, path=corrected_path):
                resolved = DOCS_DIR / corrected_path
                self.assertTrue(
                    resolved.is_file(),
                    f"Nav entry {label!r} -> {corrected_path!r} does not "
                    f"resolve to a file at {resolved}",
                )

    def test_old_doubly_prefixed_paths_do_not_exist(self):
        # Negative case: confirm the old paths genuinely would have 404'd
        # (i.e. docs/docs/... does not exist), proving this was a real bug.
        for _, corrected_path in ALL_CORRECTED_ENTRIES:
            old_relative = f"docs/{corrected_path}"
            with self.subTest(path=old_relative):
                self.assertFalse((DOCS_DIR / old_relative).exists())


@unittest.skipUnless(HAS_YAML, "PyYAML not installed")
class MkdocsNavYamlStructureTests(unittest.TestCase):
    """Structural validation of the nav tree (skipped if PyYAML is absent)."""

    @classmethod
    def setUpClass(cls):
        with MKDOCS_PATH.open(encoding="utf-8") as fh:
            cls.config = yaml.safe_load(fh)

    def _find_section(self, section_name):
        for entry in self.config["nav"]:
            if isinstance(entry, dict) and section_name in entry:
                return entry[section_name]
        raise AssertionError(f"Could not find nav section {section_name!r}")

    @staticmethod
    def _flatten(section_items):
        flattened = {}
        for item in section_items:
            for label, path in item.items():
                flattened[label] = path
        return flattened

    def test_governance_section_matches_expected_mapping(self):
        flattened = self._flatten(self._find_section("Governance"))
        for label, corrected_path in CORRECTED_GOVERNANCE_ENTRIES:
            with self.subTest(label=label):
                self.assertEqual(flattened.get(label), corrected_path)

    def test_ai_setup_section_matches_expected_mapping(self):
        flattened = self._flatten(self._find_section("AI Setup"))
        for label, corrected_path in CORRECTED_AI_SETUP_ENTRIES:
            with self.subTest(label=label):
                self.assertEqual(flattened.get(label), corrected_path)

    def test_ansible_section_matches_expected_mapping(self):
        flattened = self._flatten(self._find_section("Ansible"))
        for label, corrected_path in CORRECTED_ANSIBLE_ENTRIES:
            with self.subTest(label=label):
                self.assertEqual(flattened.get(label), corrected_path)

    def test_no_nav_value_anywhere_starts_with_docs_prefix(self):
        # Broad structural regression guard: walk the whole nav tree and
        # make sure no leaf value re-introduces a "docs/" prefix, which
        # would cause MkDocs to look for a nonexistent docs/docs/... path.
        def walk(node):
            if isinstance(node, list):
                for item in node:
                    yield from walk(item)
            elif isinstance(node, dict):
                for value in node.values():
                    yield from walk(value)
            elif isinstance(node, str):
                yield node

        for value in walk(self.config["nav"]):
            with self.subTest(value=value):
                self.assertFalse(
                    value.startswith("docs/"),
                    f"Nav value {value!r} incorrectly starts with 'docs/'",
                )


if __name__ == "__main__":
    unittest.main()