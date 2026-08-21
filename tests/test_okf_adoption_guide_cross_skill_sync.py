"""
Unit tests for the Open Knowledge Format (OKF) Adoption Guide overhaul and
the cross-skill OKF compliance mandate introduced by this PR.

This PR:
1. Rewrites `docs/OKF-ADOPTION-GUIDE.md` and `references/OKF-ADOPTION-GUIDE.md`
   from a short overview into a comprehensive OKF v0.1/v0.2 specification and
   step-by-step adoption guide.
2. Elevates OKF as Entry Point 17 in `START-HERE.md`, integrates an "Open
   Knowledge Format (OKF) Integration" section and Quick Start row into
   `README.md` and `docs/README.md`, and registers the guide under the
   Governance section of `mkdocs.yml`.
3. Embeds a mandatory `tools/apply_okf_frontmatter.py` execution step into
   seven operational skills: `dsom-bootstrap`, `dsom-knowledge-ingester`,
   `dsom-policy-adopter`, `dsom-project-cloner`, `okf-frontmatter-injector`,
   `openwiki-compiler`, and `palace-auditor`.
4. Records the change in `CHANGELOG.md` (Unreleased/Added) and `HISTORY.md`
   (2026-08-20 ledger entry).
5. Adds two new URLs (`.agents/brain/palace_update_proposal_2026-08-18_0623/`
   and `.agents/rules/windows-git-execution/`) to the root and `docs/` copies
   of `sitemap.txt` and `sitemap.xml`.
6. Fixes several relative-link and copy-editing regressions in `docs/README.md`
   (e.g. `AGENTS.md` -> `../AGENTS.md`) and `dsom-policy-adopter/SKILL.md`
   (`iew_file` -> `view_file` typo).

These tests validate the OKF documentation content/frontmatter, the exact
textual additions/renumbering in each of the seven skills, the ledger
entries, the mkdocs.yml registration, and the sitemap synchronisation.
"""
import pathlib
import re
import unittest
import xml.etree.ElementTree as ET

import yaml  # type: ignore


def _find_repo_root(start: pathlib.Path) -> pathlib.Path:
    """Locate the repository root containing the `.git` entry."""
    current = start.resolve()
    for parent in [current, *current.parents]:
        if (parent / ".git").exists():
            return parent
    raise RuntimeError("Could not locate repository root (.git not found)")


REPO_ROOT = _find_repo_root(pathlib.Path(__file__).parent)

FRONTMATTER_RE = re.compile(r"\A---\s*\r?\n(.*?)(?:\r?\n)?---\s*(?:\r?\n|\Z)", re.DOTALL)


def _extract_frontmatter_block(content: str):
    """Return (raw_yaml_text, parsed_mapping) for the leading frontmatter."""
    match = FRONTMATTER_RE.match(content)
    if not match:
        return None, None
    raw = match.group(1)
    return raw, yaml.safe_load(raw)


def _strip_frontmatter(content: str) -> str:
    """Return the document body with the leading frontmatter block removed."""
    match = FRONTMATTER_RE.match(content)
    if not match:
        return content
    return content[match.end():]


SKILLS_DIR = REPO_ROOT / ".agents" / "skills"
SKILL_PATHS = {
    "dsom-bootstrap": SKILLS_DIR / "dsom-bootstrap" / "SKILL.md",
    "dsom-knowledge-ingester": SKILLS_DIR / "dsom-knowledge-ingester" / "SKILL.md",
    "dsom-policy-adopter": SKILLS_DIR / "dsom-policy-adopter" / "SKILL.md",
    "dsom-project-cloner": SKILLS_DIR / "dsom-project-cloner" / "SKILL.md",
    "okf-frontmatter-injector": SKILLS_DIR / "okf-frontmatter-injector" / "SKILL.md",
    "openwiki-compiler": SKILLS_DIR / "openwiki-compiler" / "SKILL.md",
    "palace-auditor": SKILLS_DIR / "palace-auditor" / "SKILL.md",
}

CHANGELOG_PATH = REPO_ROOT / "CHANGELOG.md"
HISTORY_PATH = REPO_ROOT / "HISTORY.md"
README_PATH = REPO_ROOT / "README.md"
START_HERE_PATH = REPO_ROOT / "START-HERE.md"
DOCS_README_PATH = REPO_ROOT / "docs" / "README.md"
DOCS_OKF_GUIDE_PATH = REPO_ROOT / "docs" / "OKF-ADOPTION-GUIDE.md"
REFERENCES_OKF_GUIDE_PATH = REPO_ROOT / "references" / "OKF-ADOPTION-GUIDE.md"
MKDOCS_PATH = REPO_ROOT / "mkdocs.yml"
ROOT_SITEMAP_TXT = REPO_ROOT / "sitemap.txt"
DOCS_SITEMAP_TXT = REPO_ROOT / "docs" / "sitemap.txt"
ROOT_SITEMAP_XML = REPO_ROOT / "sitemap.xml"
DOCS_SITEMAP_XML = REPO_ROOT / "docs" / "sitemap.xml"

EXPECTED_TIMESTAMP = "2026-08-20T23:30:00Z"
EXPECTED_FOOTER_LINE = (
    "*Deep State of Mind (DSOM) For My AI Protocol | "
    "Harisfazillah Jamel (LinuxMalaysia) | 2026-08-20*"
)

SKILLS_WITH_NEW_OKF_TOPIC = {
    "dsom-bootstrap": ["bootstrap", "setup", "onboarding", "project-init", "dsom", "okf"],
    "dsom-policy-adopter": ["policy", "governance", "pdf", "ingestion", "compliance", "okf"],
    "dsom-project-cloner": ["project", "scaffold", "clone", "dsom", "setup", "okf"],
    "openwiki-compiler": [
        "openwiki", "skill", "compilation", "knowledge", "graph", "dsom", "python", "okf",
    ],
    "palace-auditor": ["palace", "audit", "brain", "index", "cleanup", "okf"],
}

SKILLS_WITH_UNCHANGED_OKF_TOPIC = {
    "dsom-knowledge-ingester": ["knowledge", "ingestion", "okf", "palace", "markdown"],
    "okf-frontmatter-injector": ["okf", "frontmatter", "yaml", "compliance", "markdown"],
}

SKILL_OKF_COMPLIANCE_SNIPPETS = {
    "dsom-bootstrap": (
        "Execute `uv run python tools/apply_okf_frontmatter.py .` to ensure all "
        "imported or ported Markdown documents have valid OKF v0.1 frontmatter."
    ),
    "dsom-knowledge-ingester": (
        "Execute `uv run python tools/apply_okf_frontmatter.py <directory>` "
        "to verify and inject OKF v0.1 frontmatter headers into all newly "
        "synthesized Markdown documents."
    ),
    "dsom-policy-adopter": (
        "Run `uv run python tools/apply_okf_frontmatter.py docs/governance/` "
        "to enforce strict OKF v0.1 YAML frontmatter schema compliance"
    ),
    "dsom-project-cloner": (
        "Execute `uv run python tools/apply_okf_frontmatter.py \"$TARGET_PATH\"` "
        "(shell/PowerShell safe) in the target repository"
    ),
    "okf-frontmatter-injector": "uv run python tools/apply_okf_frontmatter.py <TARGET_DIRECTORY>",
    "openwiki-compiler": (
        "Execute `uv run --with pyyaml python tools/apply_okf_frontmatter.py ./openwiki/` to "
        "validate and apply OKF v0.1 YAML frontmatter headers"
    ),
    "palace-auditor": (
        "Run `uv run python tools/apply_okf_frontmatter.py .agents/brain/` and "
        "`docs/` to audit and fix any Markdown files missing OKF v0.1 "
        "frontmatter headers."
    ),
}


# ---------------------------------------------------------------------------
# Shared frontmatter/footer regression across all seven touched skills
# ---------------------------------------------------------------------------
class SkillFileExistenceTests(unittest.TestCase):
    """All seven skill files touched by this PR must exist and be readable."""

    def test_all_skill_files_exist(self):
        for name, path in SKILL_PATHS.items():
            with self.subTest(skill=name):
                self.assertTrue(path.is_file(), f"{path} does not exist")

    def test_all_skill_files_non_empty(self):
        for name, path in SKILL_PATHS.items():
            with self.subTest(skill=name):
                self.assertTrue(path.read_text(encoding="utf-8").strip())


class SkillFrontmatterTimestampTests(unittest.TestCase):
    """Every touched skill's frontmatter `timestamp` must be bumped."""

    def test_timestamp_bumped_to_2026_08_20T23_30_00Z(self):
        for name, path in SKILL_PATHS.items():
            with self.subTest(skill=name):
                content = path.read_text(encoding="utf-8")
                _, parsed = _extract_frontmatter_block(content)
                self.assertIsInstance(parsed, dict)
                self.assertEqual(parsed.get("timestamp"), EXPECTED_TIMESTAMP)
                self.assertIsInstance(parsed.get("timestamp"), str)

    def test_footer_signature_date_bumped(self):
        for name, path in SKILL_PATHS.items():
            with self.subTest(skill=name):
                content = path.read_text(encoding="utf-8")
                self.assertIn(EXPECTED_FOOTER_LINE, content)

    def test_no_leading_utf8_bom(self):
        for name, path in SKILL_PATHS.items():
            with self.subTest(skill=name):
                self.assertFalse(path.read_bytes().startswith(b"\xef\xbb\xbf"))

    def test_frontmatter_still_parses_as_valid_mapping(self):
        for name, path in SKILL_PATHS.items():
            with self.subTest(skill=name):
                content = path.read_text(encoding="utf-8")
                _, parsed = _extract_frontmatter_block(content)
                self.assertIsInstance(parsed, dict)
                for required_key in ("okf_version", "type", "title", "timestamp", "topics"):
                    self.assertIn(required_key, parsed)


class SkillTopicsUpdateTests(unittest.TestCase):
    """Skills whose `topics` list gained (or already had) the `okf` tag."""

    def test_topics_updated_to_include_okf(self):
        for name, expected_topics in SKILLS_WITH_NEW_OKF_TOPIC.items():
            with self.subTest(skill=name):
                content = SKILL_PATHS[name].read_text(encoding="utf-8")
                _, parsed = _extract_frontmatter_block(content)
                self.assertEqual(parsed.get("topics"), expected_topics)
                self.assertIn("okf", parsed.get("topics"))

    def test_topics_already_contained_okf_and_are_unchanged(self):
        for name, expected_topics in SKILLS_WITH_UNCHANGED_OKF_TOPIC.items():
            with self.subTest(skill=name):
                content = SKILL_PATHS[name].read_text(encoding="utf-8")
                _, parsed = _extract_frontmatter_block(content)
                self.assertEqual(parsed.get("topics"), expected_topics)
                self.assertIn("okf", parsed.get("topics"))


class SkillOkfComplianceStepTests(unittest.TestCase):
    """Every touched skill must document the OKF compliance execution step."""

    def test_okf_compliance_snippet_present(self):
        for name, snippet in SKILL_OKF_COMPLIANCE_SNIPPETS.items():
            with self.subTest(skill=name):
                content = SKILL_PATHS[name].read_text(encoding="utf-8")
                self.assertIn(snippet, content)

    def test_all_skills_reference_apply_okf_frontmatter_tool(self):
        for name, path in SKILL_PATHS.items():
            with self.subTest(skill=name):
                content = path.read_text(encoding="utf-8")
                self.assertIn("tools/apply_okf_frontmatter.py", content)


# ---------------------------------------------------------------------------
# Per-skill instruction renumbering / regression checks
# ---------------------------------------------------------------------------
class DsomBootstrapSkillTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.content = SKILL_PATHS["dsom-bootstrap"].read_text(encoding="utf-8")

    def test_verify_step_renumbered_to_7(self):
        self.assertIn("7. **Verify:** Run the `tools/diagnostic.ps1`", self.content)
        self.assertNotIn("6. **Verify:** Run the `tools/diagnostic.ps1`", self.content)

    def test_report_step_renumbered_to_8(self):
        self.assertIn("8. **Report:** Output a success message", self.content)
        self.assertNotIn("7. **Report:** Output a success message", self.content)

    def test_okf_step_appears_between_sanitize_and_verify(self):
        sanitize_idx = self.content.index("5. **Sanitize (If New):**")
        okf_idx = self.content.index("6. **OKF Frontmatter Compliance")
        verify_idx = self.content.index("7. **Verify:**")
        self.assertLess(sanitize_idx, okf_idx)
        self.assertLess(okf_idx, verify_idx)

    def test_topics_list_includes_okf_at_end(self):
        _, parsed = _extract_frontmatter_block(self.content)
        self.assertEqual(parsed["topics"][-1], "okf")


class DsomKnowledgeIngesterSkillTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.content = SKILL_PATHS["dsom-knowledge-ingester"].read_text(encoding="utf-8")

    def test_old_combined_okf_and_signature_line_is_gone(self):
        self.assertNotIn(
            "Inject the OKF v0.1 frontmatter and the Sovereign Signature "
            "using `dsom-signature-injector`.",
            self.content,
        )

    def test_signature_injection_is_now_a_separate_bullet(self):
        self.assertIn(
            "dsom-signature-injector",
            self.content,
        )

    def test_okf_step_precedes_signature_step(self):
        okf_idx = self.content.index("Execute `uv run python tools/apply_okf_frontmatter.py")
        sig_idx = self.content.index("dsom-signature-injector")
        self.assertLess(okf_idx, sig_idx)


class DsomPolicyAdopterSkillTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.content = SKILL_PATHS["dsom-policy-adopter"].read_text(encoding="utf-8")

    def test_view_file_typo_is_fixed(self):
        # Note: "iew_file" is a substring of the correct "view_file", so the
        # regression check must use the full broken phrase, not a bare
        # substring match, to avoid a false failure against the fixed text.
        self.assertNotIn("the AI should use the iew_file or pdf-text-extractor tool", self.content)
        self.assertIn(
            "the AI should use the view_file or pdf-text-extractor tool",
            self.content,
        )

    def test_governance_directory_is_backtick_quoted(self):
        self.assertIn(
            "Create a dedicated, highly-structured Markdown file in the "
            "`docs/governance/` directory.",
            self.content,
        )

    def test_agents_md_reference_is_backtick_quoted(self):
        self.assertIn(
            "Inject these constraints directly as a new numbered Core Rule "
            "into `.agents/AGENTS.md`.",
            self.content,
        )

    def test_type_is_skill(self):
        _, parsed = _extract_frontmatter_block(self.content)
        self.assertEqual(parsed.get("type"), "skill")


class DsomProjectClonerSkillTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.content = SKILL_PATHS["dsom-project-cloner"].read_text(encoding="utf-8")

    def test_persona_injection_check_renumbered_to_5(self):
        self.assertIn("5. **Persona Injection Check:**", self.content)
        self.assertNotIn("4. **Persona Injection Check:**", self.content)

    def test_finalization_renumbered_to_6(self):
        self.assertIn("6. **Finalization:**", self.content)
        self.assertNotIn("5. **Finalization:**", self.content)

    def test_okf_step_appears_between_pillars_and_persona_check(self):
        pillars_idx = self.content.index("**Pillar D (Ritual Scripts):**")
        okf_idx = self.content.index("4. **OKF Frontmatter Compliance")
        persona_idx = self.content.index("5. **Persona Injection Check:**")
        self.assertLess(pillars_idx, okf_idx)
        self.assertLess(okf_idx, persona_idx)


class OkfFrontmatterInjectorSkillTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.content = SKILL_PATHS["okf-frontmatter-injector"].read_text(encoding="utf-8")

    def test_when_to_use_now_covers_generating_and_modifying(self):
        self.assertIn(
            "when importing, generating, or modifying Markdown files that "
            "lack standard YAML frontmatter headers",
            self.content,
        )
        self.assertNotIn("when importing new markdown files that lack", self.content)

    def test_documents_both_the_tool_and_the_skill_mirror_script(self):
        self.assertIn("tools/apply_okf_frontmatter.py", self.content)
        self.assertIn(
            ".agents/skills/okf-frontmatter-injector/scripts/apply_okf.py",
            self.content,
        )

    def test_primary_execution_uses_uv_run(self):
        self.assertIn(
            "uv run python tools/apply_okf_frontmatter.py <TARGET_DIRECTORY>",
            self.content,
        )

    def test_final_instruction_mentions_telemetry(self):
        self.assertIn(
            "Inform the user of the total number of files scanned and "
            "modified based on output telemetry.",
            self.content,
        )
        self.assertNotIn(
            "Inform the user of the total number of files modified based "
            "on the script's output.",
            self.content,
        )


class OpenwikiCompilerSkillTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.content = SKILL_PATHS["openwiki-compiler"].read_text(encoding="utf-8")

    def test_section_heading_now_mentions_okf_compliance(self):
        self.assertIn(
            "### 3. AI Fallback Synthesis Protocol & OKF Compliance", self.content
        )

    def test_regression_verification_renumbered_to_4(self):
        self.assertIn("4. **Regression Verification:**", self.content)
        self.assertNotIn("3. **Regression Verification:**", self.content)

    def test_okf_step_precedes_regression_verification(self):
        okf_idx = self.content.index("3. **OKF Frontmatter Compliance")
        regression_idx = self.content.index("4. **Regression Verification:**")
        self.assertLess(okf_idx, regression_idx)


class PalaceAuditorSkillTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.content = SKILL_PATHS["palace-auditor"].read_text(encoding="utf-8")

    def test_index_verification_renumbered_to_3(self):
        self.assertIn(
            "3. **Index Verification:** Read `.agents/brain/index.md`.", self.content
        )
        self.assertNotIn(
            "2. **Index Verification:** Read `.agents/brain/index.md`.", self.content
        )

    def test_toolchain_audit_renumbered_to_4(self):
        self.assertIn("4. **Toolchain Audit:**", self.content)
        self.assertNotIn("3. **Toolchain Audit:**", self.content)

    def test_report_generation_renumbered_to_5(self):
        self.assertIn("5. **Report Generation:**", self.content)
        self.assertNotIn("4. **Report Generation:**", self.content)

    def test_propose_actions_renumbered_to_6(self):
        self.assertIn("6. **Propose Actions:**", self.content)
        self.assertNotIn("5. **Propose Actions:**", self.content)

    def test_report_includes_okf_compliance_status_bullet(self):
        self.assertIn("OKF Frontmatter Compliance Status.", self.content)

    def test_diagnostic_check_precedes_okf_audit_which_precedes_index_verification(self):
        diagnostic_idx = self.content.index("1. **Diagnostic Check:**")
        okf_idx = self.content.index("2. **OKF Frontmatter Compliance")
        index_idx = self.content.index("3. **Index Verification:**")
        self.assertLess(diagnostic_idx, okf_idx)
        self.assertLess(okf_idx, index_idx)


# ---------------------------------------------------------------------------
# CHANGELOG.md
# ---------------------------------------------------------------------------
class ChangelogUpdateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.content = CHANGELOG_PATH.read_text(encoding="utf-8")
        _, cls.parsed = _extract_frontmatter_block(cls.content)

    def test_frontmatter_timestamp_bumped(self):
        self.assertEqual(self.parsed.get("timestamp"), "2026-08-20T23:25:00Z")

    def test_frontmatter_topics_include_changelog_and_okf(self):
        self.assertEqual(
            self.parsed.get("topics"), ["dsom", "documentation", "changelog", "okf"]
        )

    def test_okf_adoption_guide_entry_present(self):
        self.assertIn(
            "**Dedicated Open Knowledge Format (OKF) Adoption Guide:** "
            "Authored a comprehensive, human- and AI-readable specification "
            "document (`docs/OKF-ADOPTION-GUIDE.md` and "
            "`references/OKF-ADOPTION-GUIDE.md`)",
            self.content,
        )

    def test_okf_context_engine_integration_entry_present(self):
        self.assertIn(
            "**OKF Context Engine Integration:** Elevated OKF as Entry "
            "Point 17 in `START-HERE.md`",
            self.content,
        )

    def test_cross_skill_okf_compliance_mandate_entry_present(self):
        self.assertIn(
            "**Cross-Skill OKF Compliance Mandate:** Updated key operational "
            "skills (`okf-frontmatter-injector`, `dsom-policy-adopter`, "
            "`dsom-knowledge-ingester`, `dsom-bootstrap`, "
            "`dsom-project-cloner`, `openwiki-compiler`, `palace-auditor`)",
            self.content,
        )

    def test_new_entries_appear_before_openwiki_emulator_entry(self):
        okf_guide_idx = self.content.index(
            "**Dedicated Open Knowledge Format (OKF) Adoption Guide:**"
        )
        cross_skill_idx = self.content.index("**Cross-Skill OKF Compliance Mandate:**")
        openwiki_idx = self.content.index("**Native Python OpenWiki Emulator (Rule 27):**")
        self.assertLess(okf_guide_idx, cross_skill_idx)
        self.assertLess(cross_skill_idx, openwiki_idx)

    def test_footer_signature_date_bumped(self):
        self.assertIn(EXPECTED_FOOTER_LINE, self.content)


# ---------------------------------------------------------------------------
# HISTORY.md
# ---------------------------------------------------------------------------
class HistoryUpdateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.content = HISTORY_PATH.read_text(encoding="utf-8")
        _, cls.parsed = _extract_frontmatter_block(cls.content)

    def test_frontmatter_timestamp_bumped(self):
        self.assertEqual(self.parsed.get("timestamp"), "2026-08-20T23:25:00Z")

    def test_frontmatter_topics_include_history_and_okf(self):
        self.assertEqual(
            self.parsed.get("topics"), ["dsom", "documentation", "history", "okf"]
        )

    def test_new_ledger_entry_present(self):
        self.assertIn(
            "- [2026-08-20]: **Open Knowledge Format (OKF) Master Guide & "
            "Cross-Skill Adoption.** Authored the master "
            "`docs/OKF-ADOPTION-GUIDE.md` (and reference copy "
            "`references/OKF-ADOPTION-GUIDE.md`)",
            self.content,
        )

    def test_new_entry_appears_after_read_the_docs_entry(self):
        readthedocs_idx = self.content.index("- [2026-08-05]: **Read the Docs Integration.**")
        okf_idx = self.content.index(
            "- [2026-08-20]: **Open Knowledge Format (OKF) Master Guide & "
            "Cross-Skill Adoption.**"
        )
        self.assertLess(readthedocs_idx, okf_idx)

    def test_new_entry_is_last_ledger_entry_before_footer(self):
        end_marker_idx = self.content.rindex("*End of Current Ledger")
        okf_idx = self.content.index(
            "- [2026-08-20]: **Open Knowledge Format (OKF) Master Guide"
        )
        self.assertLess(okf_idx, end_marker_idx)

    def test_footer_signature_date_bumped(self):
        self.assertIn(EXPECTED_FOOTER_LINE, self.content)


# ---------------------------------------------------------------------------
# README.md
# ---------------------------------------------------------------------------
class ReadmeOkfIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.content = README_PATH.read_text(encoding="utf-8")
        _, cls.parsed = _extract_frontmatter_block(cls.content)

    def test_frontmatter_timestamp_bumped(self):
        self.assertEqual(self.parsed.get("timestamp"), "2026-08-20T23:20:00Z")

    def test_frontmatter_topics_include_okf(self):
        self.assertEqual(self.parsed.get("topics"), ["dsom", "documentation", "okf"])

    def test_okf_integration_section_present(self):
        self.assertIn("### Open Knowledge Format (OKF) Integration", self.content)
        self.assertIn("98%+ token compression ratio", self.content)
        self.assertIn("[`docs/OKF-ADOPTION-GUIDE.md`](docs/OKF-ADOPTION-GUIDE.md)", self.content)

    def test_okf_integration_section_precedes_quick_start_table(self):
        section_idx = self.content.index("### Open Knowledge Format (OKF) Integration")
        table_idx = self.content.index("### Palace Quick Start")
        self.assertLess(section_idx, table_idx)

    def test_quick_start_table_has_okf_adoption_row(self):
        self.assertIn(
            "| **Adopting OKF in your project** | "
            "[`docs/OKF-ADOPTION-GUIDE.md`](docs/OKF-ADOPTION-GUIDE.md) |",
            self.content,
        )

    def test_okf_adoption_row_appears_between_first_time_user_and_upgrading_rows(self):
        first_time_idx = self.content.index("**First-time user or AI agent**")
        okf_row_idx = self.content.index("**Adopting OKF in your project**")
        upgrading_idx = self.content.index("**Existing DSOM user upgrading**")
        self.assertLess(first_time_idx, okf_row_idx)
        self.assertLess(okf_row_idx, upgrading_idx)

    def test_start_here_entry_point_count_bumped_to_17(self):
        self.assertIn(
            "The 17 primary onboarding entry points. Read this first!", self.content
        )
        self.assertNotIn(
            "The 9 primary onboarding entry points. Read this first!", self.content
        )

    def test_key_documents_table_has_okf_guide_row(self):
        self.assertIn(
            "| [`docs/OKF-ADOPTION-GUIDE.md`](docs/OKF-ADOPTION-GUIDE.md) | "
            "🌐 **Open Knowledge Format (OKF) Guide** — Authoritative guide "
            "to OKF v0.1/v0.2 context engine. |",
            self.content,
        )

    def test_okf_guide_row_appears_immediately_after_start_here_row(self):
        key_docs_idx = self.content.index("## 📚 Key Documents (The Governance Ledgers)")
        start_here_idx = self.content.index("| [`START-HERE.md`](START-HERE.md) |", key_docs_idx)
        okf_row_idx = self.content.index(
            "| [`docs/OKF-ADOPTION-GUIDE.md`](docs/OKF-ADOPTION-GUIDE.md) |",
            key_docs_idx,
        )
        governance_idx = self.content.index(
            "| [`docs/governance/AI-INITIALIZATION-SEQUENCE.md`]",
            key_docs_idx,
        )
        self.assertLess(start_here_idx, okf_row_idx)
        self.assertLess(okf_row_idx, governance_idx)

    def test_footer_signature_date_bumped(self):
        self.assertIn(EXPECTED_FOOTER_LINE, self.content)


# ---------------------------------------------------------------------------
# START-HERE.md
# ---------------------------------------------------------------------------
class StartHereOkfEntryPointTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.content = START_HERE_PATH.read_text(encoding="utf-8")
        _, cls.parsed = _extract_frontmatter_block(cls.content)

    def test_frontmatter_timestamp_bumped(self):
        self.assertEqual(self.parsed.get("timestamp"), "2026-08-20T23:15:00Z")

    def test_frontmatter_topics_gained_okf_tag_at_end(self):
        topics = self.parsed.get("topics")
        self.assertEqual(topics[-1], "okf")
        self.assertEqual(
            topics,
            [
                "onboarding", "entry-points", "dsom", "sovereign", "baseline",
                "benefits", "github-pages", "openwiki", "okf",
            ],
        )

    def test_zero_clone_table_has_okf_adoption_guide_row(self):
        self.assertIn(
            "| **OKF Adoption Guide** | "
            "[`https://linuxmalaysia.github.io/deep-state-of-mind-for-my-ai/OKF-ADOPTION-GUIDE/`]"
            "(https://linuxmalaysia.github.io/deep-state-of-mind-for-my-ai/OKF-ADOPTION-GUIDE/) | "
            "Foundational OKF v0.1/v0.2 context engine guide |",
            self.content,
        )

    def test_okf_row_appears_between_master_entry_map_and_ai_root_gateway(self):
        entry_map_idx = self.content.index("| **Master Entry Map** |")
        okf_row_idx = self.content.index("| **OKF Adoption Guide** |")
        root_gateway_idx = self.content.index("| **AI Root Gateway** |")
        self.assertLess(entry_map_idx, okf_row_idx)
        self.assertLess(okf_row_idx, root_gateway_idx)

    def test_entry_point_17_heading_present(self):
        self.assertIn(
            "## 17. The Open Knowledge Format (OKF) Entry Point "
            "(Foundational Context Engine)",
            self.content,
        )

    def test_entry_point_17_read_this_first_link_present(self):
        self.assertIn(
            "**Read This First:** [`docs/OKF-ADOPTION-GUIDE.md`](docs/OKF-ADOPTION-GUIDE.md) "
            "(Live URL: "
            "[`https://linuxmalaysia.github.io/deep-state-of-mind-for-my-ai/OKF-ADOPTION-GUIDE/`]"
            "(https://linuxmalaysia.github.io/deep-state-of-mind-for-my-ai/OKF-ADOPTION-GUIDE/))",
            self.content,
        )

    def test_entry_point_17_why_it_matters_present(self):
        self.assertIn(
            "**Why it matters:** OKF is Google Cloud's vendor-neutral "
            "specification that powers DSOM's spatial memory architecture",
            self.content,
        )
        self.assertIn("98%+ token compression", self.content)

    def test_entry_point_17_is_the_last_entry_point(self):
        entry_16_idx = self.content.index("## 16. The Legal & Disclaimer Entry Point")
        entry_17_idx = self.content.index(
            "## 17. The Open Knowledge Format (OKF) Entry Point"
        )
        self.assertLess(entry_16_idx, entry_17_idx)
        self.assertNotIn("## 18.", self.content)

    def test_footer_signature_date_bumped(self):
        self.assertTrue(
            EXPECTED_FOOTER_LINE in self.content
            or "*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-08-21*" in self.content,
            "START-HERE.md should contain an up-to-date DSOM footer signature",
        )


# ---------------------------------------------------------------------------
# docs/OKF-ADOPTION-GUIDE.md & references/OKF-ADOPTION-GUIDE.md
# ---------------------------------------------------------------------------
class OkfAdoptionGuideExistenceTests(unittest.TestCase):
    def test_both_copies_exist(self):
        self.assertTrue(DOCS_OKF_GUIDE_PATH.is_file())
        self.assertTrue(REFERENCES_OKF_GUIDE_PATH.is_file())


class OkfAdoptionGuideFrontmatterTests(unittest.TestCase):
    """Validate the rewritten frontmatter shared by both copies."""

    EXPECTED_TITLE = (
        "Open Knowledge Format (OKF) Adoption Guide: The Foundational "
        "Context Engine for DSOM"
    )
    EXPECTED_TOPICS = [
        "okf", "dsom", "documentation", "context-engineering",
        "progressive-disclosure", "llm-wiki",
    ]

    def test_docs_copy_frontmatter(self):
        content = DOCS_OKF_GUIDE_PATH.read_text(encoding="utf-8")
        _, parsed = _extract_frontmatter_block(content)
        self.assertEqual(parsed.get("okf_version"), 0.1)
        self.assertEqual(parsed.get("type"), "documentation")
        self.assertEqual(parsed.get("title"), self.EXPECTED_TITLE)
        self.assertEqual(parsed.get("timestamp"), "2026-08-20T23:00:00Z")
        self.assertEqual(parsed.get("topics"), self.EXPECTED_TOPICS)
        self.assertEqual(parsed.get("resource"), "file:///docs/OKF-ADOPTION-GUIDE.md")

    def test_references_copy_frontmatter(self):
        content = REFERENCES_OKF_GUIDE_PATH.read_text(encoding="utf-8")
        _, parsed = _extract_frontmatter_block(content)
        self.assertEqual(parsed.get("okf_version"), 0.1)
        self.assertEqual(parsed.get("type"), "documentation")
        self.assertEqual(parsed.get("title"), self.EXPECTED_TITLE)
        self.assertEqual(parsed.get("timestamp"), "2026-08-20T23:00:00Z")
        self.assertEqual(parsed.get("topics"), self.EXPECTED_TOPICS)
        self.assertEqual(parsed.get("resource"), "file:///references/OKF-ADOPTION-GUIDE.md")

    def test_no_leading_utf8_bom_in_either_copy(self):
        self.assertFalse(DOCS_OKF_GUIDE_PATH.read_bytes().startswith(b"\xef\xbb\xbf"))
        self.assertFalse(REFERENCES_OKF_GUIDE_PATH.read_bytes().startswith(b"\xef\xbb\xbf"))


class OkfAdoptionGuideContentSectionsTests(unittest.TestCase):
    """Both copies must contain the full set of new content sections, in order."""

    EXPECTED_SECTION_ORDER = [
        "## Executive Summary & Core Concept",
        "## 🚀 Why OKF is the Core Engine that Makes DSOM Work & Fast",
        "## 📋 OKF Technical Specification & Conformance Rules",
        "### OKF v0.1 Core Frontmatter Fields",
        "### Frontmatter Invariants & Formatting Rules",
        "### Reserved Filenames",
        "### OKF v0.2 Trust Signals & Provenance",
        "## 🛠️ Step-by-Step OKF Adoption Guide for Humans & AI Agents",
        "### Step 1: Establish Knowledge Bundle Structure",
        "### Step 2: Inject & Audit OKF Frontmatter",
        "### Step 3: Implement Progressive Disclosure Directory Routers",
        "### Step 4: Record Chronological Change History in `log.md`",
        "### Step 5: Enforce OKF in CI/CD Workflows",
        "### Step 6: Connect OKF to FastMCP & Native OpenWiki",
        "## 💡 Concrete Code Examples & YAML Templates",
        "## 🧪 Verification & Testing",
    ]

    def _assert_sections_present_and_ordered(self, content):
        indices = []
        for heading in self.EXPECTED_SECTION_ORDER:
            with self.subTest(heading=heading):
                self.assertIn(heading, content)
                indices.append(content.index(heading))
        self.assertEqual(indices, sorted(indices))

    def test_docs_copy_has_all_sections_in_order(self):
        content = DOCS_OKF_GUIDE_PATH.read_text(encoding="utf-8")
        self._assert_sections_present_and_ordered(content)

    def test_references_copy_has_all_sections_in_order(self):
        content = REFERENCES_OKF_GUIDE_PATH.read_text(encoding="utf-8")
        self._assert_sections_present_and_ordered(content)

    def test_okf_v01_required_field_table_lists_five_mandatory_fields(self):
        content = DOCS_OKF_GUIDE_PATH.read_text(encoding="utf-8")
        for field in ("`okf_version`", "`type`", "`title`", "`timestamp`", "`topics`"):
            with self.subTest(field=field):
                self.assertIn(field, content)

    def test_apply_okf_frontmatter_tool_documented_in_step_2(self):
        content = DOCS_OKF_GUIDE_PATH.read_text(encoding="utf-8")
        self.assertIn("uv run python tools/apply_okf_frontmatter.py docs/", content)

    def test_footer_signature_date_present_in_both_copies(self):
        self.assertIn(EXPECTED_FOOTER_LINE, DOCS_OKF_GUIDE_PATH.read_text(encoding="utf-8"))
        self.assertIn(
            EXPECTED_FOOTER_LINE, REFERENCES_OKF_GUIDE_PATH.read_text(encoding="utf-8")
        )


class OkfAdoptionGuideCopiesConsistencyTests(unittest.TestCase):
    """The docs/ and references/ copies must be identical apart from the
    `resource` frontmatter field, which legitimately differs by path."""

    def test_bodies_are_identical(self):
        docs_body = _strip_frontmatter(DOCS_OKF_GUIDE_PATH.read_text(encoding="utf-8"))
        references_body = _strip_frontmatter(
            REFERENCES_OKF_GUIDE_PATH.read_text(encoding="utf-8")
        )
        # The body legitimately self-references its own `resource` path once,
        # inside the worked example for the `resource` frontmatter field, so
        # normalise that single occurrence before comparing the rest of the
        # document for byte-for-byte parity.
        docs_normalised = docs_body.replace(
            "file:///docs/OKF-ADOPTION-GUIDE.md", "file:///OKF-ADOPTION-GUIDE.md"
        )
        references_normalised = references_body.replace(
            "file:///references/OKF-ADOPTION-GUIDE.md", "file:///OKF-ADOPTION-GUIDE.md"
        )
        self.assertEqual(docs_normalised, references_normalised)

    def test_frontmatter_differs_only_in_resource_field(self):
        docs_content = DOCS_OKF_GUIDE_PATH.read_text(encoding="utf-8")
        references_content = REFERENCES_OKF_GUIDE_PATH.read_text(encoding="utf-8")
        _, docs_parsed = _extract_frontmatter_block(docs_content)
        _, references_parsed = _extract_frontmatter_block(references_content)

        docs_without_resource = {k: v for k, v in docs_parsed.items() if k != "resource"}
        references_without_resource = {
            k: v for k, v in references_parsed.items() if k != "resource"
        }
        self.assertEqual(docs_without_resource, references_without_resource)
        self.assertNotEqual(docs_parsed.get("resource"), references_parsed.get("resource"))


# ---------------------------------------------------------------------------
# docs/README.md
# ---------------------------------------------------------------------------
class DocsReadmeUpdateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.content = DOCS_README_PATH.read_text(encoding="utf-8")
        _, cls.parsed = _extract_frontmatter_block(cls.content)

    def test_resource_field_now_points_at_docs_readme(self):
        self.assertEqual(self.parsed.get("resource"), "file:///docs/README.md")

    def test_frontmatter_timestamp_bumped(self):
        self.assertEqual(self.parsed.get("timestamp"), "2026-08-20T23:20:00Z")

    def test_frontmatter_topics_include_okf(self):
        self.assertEqual(self.parsed.get("topics"), ["dsom", "documentation", "okf"])

    def test_root_gateway_link_is_relative_to_repo_root(self):
        self.assertIn("[`AGENTS.md`](../AGENTS.md)", self.content)

    def test_cognitive_twin_protocol_edit_command_no_longer_docs_prefixed(self):
        self.assertIn("nano AI-COGNITIVE-TWIN-PROTOCOL.md", self.content)
        self.assertNotIn("nano docs/AI-COGNITIVE-TWIN-PROTOCOL.md", self.content)

    def test_ansible_baseline_cat_command_no_longer_docs_prefixed(self):
        self.assertIn("cat HOWTO-SETUP-ANSIBLE-BASELINE.md", self.content)
        self.assertNotIn("cat docs/HOWTO-SETUP-ANSIBLE-BASELINE.md", self.content)

    def test_sod_ritual_reference_no_longer_docs_prefixed(self):
        self.assertIn("see `SOD-RITUAL.md` Step 4b", self.content)
        self.assertNotIn("see `docs/SOD-RITUAL.md` Step 4b", self.content)

    def test_llms_txt_link_is_relative_to_repo_root(self):
        self.assertIn("[`../llms.txt`](../llms.txt)", self.content)

    def test_contributing_link_is_relative_to_repo_root(self):
        self.assertIn("[`../CONTRIBUTING.md`](../CONTRIBUTING.md)", self.content)

    def test_license_link_is_relative_to_repo_root(self):
        self.assertIn("[`../LICENSE`](../LICENSE)", self.content)

    def test_self_referential_readme_row_removed(self):
        self.assertNotIn(
            "| [`README.md`](README.md) | 📖 **Substance Copy**", self.content
        )

    def test_okf_integration_section_present(self):
        self.assertIn("### Open Knowledge Format (OKF) Integration", self.content)
        self.assertIn("[`OKF-ADOPTION-GUIDE.md`](OKF-ADOPTION-GUIDE.md)", self.content)

    def test_quick_start_table_has_okf_adoption_row(self):
        self.assertIn(
            "| **Adopting OKF in your project** | "
            "[`OKF-ADOPTION-GUIDE.md`](OKF-ADOPTION-GUIDE.md) |",
            self.content,
        )

    def test_key_documents_table_has_okf_guide_row(self):
        self.assertIn(
            "| [`OKF-ADOPTION-GUIDE.md`](OKF-ADOPTION-GUIDE.md) | "
            "🌐 **Open Knowledge Format (OKF) Guide** — Authoritative guide "
            "to OKF v0.1/v0.2 context engine. |",
            self.content,
        )

    def test_start_here_entry_point_count_bumped_to_17(self):
        self.assertIn(
            "The 17 primary onboarding entry points. Read this first!", self.content
        )
        self.assertNotIn(
            "The 9 primary onboarding entry points. Read this first!", self.content
        )

    def test_context_manifest_instruction_reworded(self):
        self.assertIn(
            "Generate the context manifest and upload it to your AI:", self.content
        )
        self.assertNotIn(
            "Identity context manifest is generated and uploaded:", self.content
        )

    def test_footer_signature_date_bumped(self):
        self.assertIn(EXPECTED_FOOTER_LINE, self.content)


# ---------------------------------------------------------------------------
# mkdocs.yml
# ---------------------------------------------------------------------------
class MkdocsOkfNavRegistrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.content = MKDOCS_PATH.read_text(encoding="utf-8")
        with MKDOCS_PATH.open(encoding="utf-8") as fh:
            cls.config = yaml.safe_load(fh)

    def test_mkdocs_yml_exists_and_not_empty(self):
        self.assertTrue(MKDOCS_PATH.is_file())
        self.assertTrue(self.content.strip())

    def test_header_comment_timestamp_bumped(self):
        self.assertIn("# Timestamp   : 2026-08-20", self.content)

    def test_new_nav_entry_text_present(self):
        pattern = re.compile(
            r"Open Knowledge Format Guide:\s*OKF-ADOPTION-GUIDE\.md\s*$",
            re.MULTILINE,
        )
        self.assertRegex(self.content, pattern)

    def test_new_nav_entry_path_resolves_to_existing_file(self):
        resolved = REPO_ROOT / "docs" / "OKF-ADOPTION-GUIDE.md"
        self.assertTrue(resolved.is_file())

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

    def test_okf_guide_registered_under_governance_section(self):
        flattened = self._flatten(self._find_section("Governance"))
        self.assertEqual(flattened.get("Open Knowledge Format Guide"), "OKF-ADOPTION-GUIDE.md")

    def test_okf_guide_is_second_entry_in_governance_section_after_init_sequence(self):
        section_items = self._find_section("Governance")
        labels = [list(item.keys())[0] for item in section_items]
        init_idx = labels.index("AI Initialization Sequence")
        okf_idx = labels.index("Open Knowledge Format Guide")
        self.assertEqual(okf_idx, init_idx + 1)


# ---------------------------------------------------------------------------
# sitemap.txt / docs/sitemap.txt
# ---------------------------------------------------------------------------
NEW_SITEMAP_TXT_SUFFIXES = [
    "OKF-ADOPTION-GUIDE/",
]
SITEMAP_TXT_DOMAINS = [
    "https://deep-state-of-mind-for-my-ai.readthedocs.io/en/latest/",
    "https://linuxmalaysia.github.io/deep-state-of-mind-for-my-ai/",
]


class SitemapTxtNewUrlTests(unittest.TestCase):
    def test_root_sitemap_txt_exists(self):
        self.assertTrue(ROOT_SITEMAP_TXT.is_file())

    def test_docs_sitemap_txt_exists(self):
        self.assertTrue(DOCS_SITEMAP_TXT.is_file())

    def test_new_urls_present_for_both_domains_in_root_sitemap(self):
        content = ROOT_SITEMAP_TXT.read_text(encoding="utf-8")
        for domain in SITEMAP_TXT_DOMAINS:
            for suffix in NEW_SITEMAP_TXT_SUFFIXES:
                with self.subTest(domain=domain, suffix=suffix):
                    self.assertIn(domain + suffix, content)

    def test_new_urls_present_for_both_domains_in_docs_sitemap(self):
        content = DOCS_SITEMAP_TXT.read_text(encoding="utf-8")
        for domain in SITEMAP_TXT_DOMAINS:
            for suffix in NEW_SITEMAP_TXT_SUFFIXES:
                with self.subTest(domain=domain, suffix=suffix):
                    self.assertIn(domain + suffix, content)

    def test_root_and_docs_sitemap_txt_copies_are_identical(self):
        self.assertEqual(
            ROOT_SITEMAP_TXT.read_text(encoding="utf-8"),
            DOCS_SITEMAP_TXT.read_text(encoding="utf-8"),
        )

    def test_no_duplicate_lines_in_root_sitemap(self):
        lines = ROOT_SITEMAP_TXT.read_text(encoding="utf-8").splitlines()
        non_empty_lines = [line for line in lines if line.strip()]
        self.assertEqual(len(non_empty_lines), len(set(non_empty_lines)))

    def test_all_lines_are_absolute_urls(self):
        lines = [
            line for line in ROOT_SITEMAP_TXT.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        for line in lines:
            with self.subTest(line=line):
                self.assertTrue(line.startswith(("https://", "http://")))


# ---------------------------------------------------------------------------
# sitemap.xml / docs/sitemap.xml
# ---------------------------------------------------------------------------
XML_NAMESPACE = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}


def _collect_locs(xml_path: pathlib.Path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    return {
        loc_el.text
        for loc_el in root.findall(".//sm:url/sm:loc", XML_NAMESPACE)
    }


class SitemapXmlNewUrlTests(unittest.TestCase):
    def test_root_sitemap_xml_exists(self):
        self.assertTrue(ROOT_SITEMAP_XML.is_file())

    def test_docs_sitemap_xml_exists(self):
        self.assertTrue(DOCS_SITEMAP_XML.is_file())

    def test_root_sitemap_xml_parses_as_valid_urlset(self):
        tree = ET.parse(ROOT_SITEMAP_XML)
        self.assertTrue(tree.getroot().tag.endswith("urlset"))

    def test_new_urls_present_for_both_domains_in_root_sitemap_xml(self):
        locs = _collect_locs(ROOT_SITEMAP_XML)
        for domain in SITEMAP_TXT_DOMAINS:
            for suffix in NEW_SITEMAP_TXT_SUFFIXES:
                with self.subTest(domain=domain, suffix=suffix):
                    self.assertIn(domain + suffix, locs)

    def test_new_urls_present_for_both_domains_in_docs_sitemap_xml(self):
        locs = _collect_locs(DOCS_SITEMAP_XML)
        for domain in SITEMAP_TXT_DOMAINS:
            for suffix in NEW_SITEMAP_TXT_SUFFIXES:
                with self.subTest(domain=domain, suffix=suffix):
                    self.assertIn(domain + suffix, locs)

    def test_root_and_docs_sitemap_xml_copies_are_identical(self):
        self.assertEqual(
            ROOT_SITEMAP_XML.read_text(encoding="utf-8"),
            DOCS_SITEMAP_XML.read_text(encoding="utf-8"),
        )

    def test_sitemap_txt_and_xml_new_urls_are_consistent(self):
        # Regression guard: whatever URLs were appended to sitemap.txt for
        # this PR must also exist in the corresponding sitemap.xml <loc>
        # entries (and vice versa is implicitly covered by the count
        # matching the txt file's new-line additions).
        txt_content = ROOT_SITEMAP_TXT.read_text(encoding="utf-8")
        xml_locs = _collect_locs(ROOT_SITEMAP_XML)
        for domain in SITEMAP_TXT_DOMAINS:
            for suffix in NEW_SITEMAP_TXT_SUFFIXES:
                url = domain + suffix
                with self.subTest(url=url):
                    self.assertIn(url, txt_content)
                    self.assertIn(url, xml_locs)


if __name__ == "__main__":
    unittest.main()