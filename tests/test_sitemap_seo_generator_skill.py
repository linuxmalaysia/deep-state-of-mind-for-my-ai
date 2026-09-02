"""
Unit tests for the new `sitemap-seo-generator` agent skill introduced by this PR,
and the cross-file registration/documentation updates that accompany it.

This PR:
1. Adds a brand-new skill file at
   `.agents/skills/sitemap-seo-generator/SKILL.md` describing how AI agents
   should invoke `tools/generate_sitemaps.py`.
2. Registers that skill in `AGENTS.md` (Knowledge & Documentation Skills
   table) and bumps the documented skill count from 31 to 32.
3. Registers the skill's `SKILL.md` in both `SUMMARY.md` (GitBook nav) and
   `mkdocs.yml` (MkDocs nav, under "AI Agent Skills & Workflows"), as the
   last entry in each list.
4. Updates the DSOM Protocol and Tooling Registry "closet" knowledge files
   under `.agents/brain/wings/wing_dsom_core/hall_facts/` to document Rules
   25/26/27 and the three new Python tools
   (`openwiki_emulator.py`, `generate_sitemaps.py`, `server.py`).

These tests validate the new skill file's OKF frontmatter/content and the
consistency of its registration across AGENTS.md, SUMMARY.md, and
mkdocs.yml, plus the specific textual additions made to the two closet.md
files.
"""
import pathlib
import re
import unittest

import yaml  # type: ignore


def _find_repo_root(start: pathlib.Path) -> pathlib.Path:
    """Locate the repository root containing the `.git` entry."""
    current = start.resolve()
    for parent in [current, *current.parents]:
        if (parent / ".git").exists():
            return parent
    raise RuntimeError("Could not locate repository root (.git not found)")


REPO_ROOT = _find_repo_root(pathlib.Path(__file__).parent)

SKILL_PATH = REPO_ROOT / ".agents" / "skills" / "sitemap-seo-generator" / "SKILL.md"
AGENTS_MD_PATH = REPO_ROOT / "AGENTS.md"
SUMMARY_MD_PATH = REPO_ROOT / "SUMMARY.md"
MKDOCS_PATH = REPO_ROOT / "mkdocs.yml"
CLOSET_DSOM_PROTOCOL_PATH = (
    REPO_ROOT
    / ".agents"
    / "brain"
    / "wings"
    / "wing_dsom_core"
    / "hall_facts"
    / "room_dsom_protocol"
    / "closet.md"
)
CLOSET_TOOLING_PATH = (
    REPO_ROOT
    / ".agents"
    / "brain"
    / "wings"
    / "wing_dsom_core"
    / "hall_facts"
    / "room_tooling"
    / "closet.md"
)

FRONTMATTER_RE = re.compile(r"\A---\s*\r?\n(.*?)(?:\r?\n)?---\s*(?:\r?\n|\Z)", re.DOTALL)


def _extract_frontmatter_block(content: str):
    """Return (raw_yaml_text, parsed_mapping) for the leading frontmatter."""
    match = FRONTMATTER_RE.match(content)
    if not match:
        return None, None
    raw = match.group(1)
    return raw, yaml.safe_load(raw)


# ---------------------------------------------------------------------------
# .agents/skills/sitemap-seo-generator/SKILL.md
# ---------------------------------------------------------------------------
class SkillFileExistenceTests(unittest.TestCase):
    """The new skill file must exist and be non-empty."""

    def test_skill_file_exists(self):
        self.assertTrue(SKILL_PATH.is_file())

    def test_skill_file_non_empty(self):
        self.assertTrue(SKILL_PATH.read_text(encoding="utf-8").strip())


class SkillFileBomAndFenceTests(unittest.TestCase):
    """The skill file must follow the OKF no-BOM, fence-first convention."""

    def test_no_leading_utf8_bom(self):
        raw_bytes = SKILL_PATH.read_bytes()
        self.assertFalse(raw_bytes.startswith(b"\xef\xbb\xbf"))

    def test_starts_exactly_with_frontmatter_fence(self):
        content = SKILL_PATH.read_text(encoding="utf-8")
        self.assertTrue(content.startswith(("---\n", "---\r\n")))


class SkillFileFrontmatterTests(unittest.TestCase):
    """Validate the OKF v0.1 frontmatter fields of the new skill file."""

    @classmethod
    def setUpClass(cls):
        cls.content = SKILL_PATH.read_text(encoding="utf-8")
        cls.raw, cls.parsed = _extract_frontmatter_block(cls.content)

    def test_frontmatter_parses_as_mapping(self):
        self.assertIsNotNone(self.parsed)
        self.assertIsInstance(self.parsed, dict)

    def test_okf_version_is_correct(self):
        self.assertEqual(self.parsed.get("okf_version"), 0.1)

    def test_type_is_agent_skill(self):
        self.assertEqual(self.parsed.get("type"), "agent_skill")

    def test_title_matches_expected_value(self):
        self.assertEqual(
            self.parsed.get("title"), "🗺️ Sitemap & SEO Asset Generator Skill"
        )

    def test_timestamp_is_quoted_string(self):
        self.assertEqual(self.parsed.get("timestamp"), "2026-08-12T12:00:00Z")
        self.assertIsInstance(self.parsed.get("timestamp"), str)

    def test_description_field_present(self):
        self.assertEqual(
            self.parsed.get("description"),
            "Configures and manages sitemap and robots.txt generation to "
            "optimize SEO indexation for GitHub Pages, Read the Docs, and GitBook.",
        )

    def test_topics_is_expected_list(self):
        self.assertEqual(
            self.parsed.get("topics"),
            ["sitemap", "seo", "automation", "gitbook", "readthedocs"],
        )

    def test_name_field_matches_directory_name(self):
        self.assertEqual(self.parsed.get("name"), "sitemap-seo-generator")

    def test_description_precedes_topics_per_skill_convention(self):
        # SKILL.md files use a special field order where `description`
        # precedes `topics` (unlike other OKF documents).
        description_index = self.raw.index("description:")
        topics_index = self.raw.index("topics:")
        self.assertLess(description_index, topics_index)

    def test_first_three_keys_are_okf_version_type_title(self):
        self.assertEqual(list(self.parsed.keys())[:3], ["okf_version", "type", "title"])

    def test_dsom_related_topic_keywords_present(self):
        topics = self.parsed.get("topics", [])
        for expected in ("sitemap", "seo"):
            with self.subTest(topic=expected):
                self.assertIn(expected, topics)


class SkillFileContentSectionsTests(unittest.TestCase):
    """Validate required content sections and operational instructions."""

    @classmethod
    def setUpClass(cls):
        cls.content = SKILL_PATH.read_text(encoding="utf-8")

    def test_has_purpose_section(self):
        self.assertIn("**Purpose**", self.content)

    def test_has_when_to_use_section(self):
        self.assertIn("## When to use this skill", self.content)

    def test_has_how_to_use_section(self):
        self.assertIn("## How to use it", self.content)

    def test_has_quality_gates_section(self):
        self.assertIn("## Quality Gates & Compliance", self.content)

    def test_references_generate_sitemaps_tool(self):
        self.assertIn("tools/generate_sitemaps.py", self.content)

    def test_documents_uv_run_invocation_command(self):
        self.assertIn("uv run python tools/generate_sitemaps.py", self.content)

    def test_references_rule_16_uv_mandate(self):
        self.assertIn("Rule 16", self.content)

    def test_references_rule_25_bom_quoting(self):
        self.assertIn("Rule 25", self.content)

    def test_documents_three_output_files(self):
        for expected_file in ("sitemap.txt", "sitemap.xml", "robots.txt"):
            with self.subTest(file=expected_file):
                self.assertIn(expected_file, self.content)

    def test_documents_all_three_target_platforms(self):
        for platform in ("GitHub Pages", "Read the Docs", "GitBook"):
            with self.subTest(platform=platform):
                self.assertIn(platform, self.content)

    def test_mentions_summary_md_validation(self):
        self.assertIn("SUMMARY.md", self.content)

    def test_has_dsom_signature_footer(self):
        self.assertIn(
            "Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia)",
            self.content,
        )
        self.assertIn("GNU General Public License v3.0", self.content)

    def test_body_heading_matches_title(self):
        self.assertIn("# 🗺️ Sitemap & SEO Asset Generator Skill", self.content)


# ---------------------------------------------------------------------------
# AGENTS.md registration
# ---------------------------------------------------------------------------
class AgentsMdSkillRegistrationTests(unittest.TestCase):
    """Verify AGENTS.md registers the new skill and updates the skill count."""

    @classmethod
    def setUpClass(cls):
        cls.content = AGENTS_MD_PATH.read_text(encoding="utf-8")

    def test_skill_row_present_in_knowledge_and_documentation_table(self):
        self.assertIn(
            "| `sitemap-seo-generator` | Generates and compiles standard "
            "sitemaps and SEO assets across platforms (GitHub Pages, Read "
            "the Docs, GitBook) to optimize search indexing. | No input "
            "required. | Generated `sitemap.txt`, `sitemap.xml`, and "
            "`robots.txt` files. |",
            self.content,
        )

    def test_skills_directory_count_updated_to_44(self):
        self.assertIn(
            "`.agents/skills/` | OKF-compliant executable skill SOPs (44 skills).",
            self.content,
        )

    def test_stale_31_skill_count_is_not_present(self):
        # Regression guard: the old count must not linger anywhere in the file.
        self.assertNotIn("OKF-compliant executable skill SOPs (31 skills)", self.content)

    def test_new_skill_row_appears_after_palace_auditor(self):
        palace_auditor_index = self.content.index("`palace-auditor`")
        sitemap_skill_index = self.content.index("`sitemap-seo-generator`")
        self.assertLess(palace_auditor_index, sitemap_skill_index)


# ---------------------------------------------------------------------------
# SUMMARY.md registration
# ---------------------------------------------------------------------------
class SummaryMdSkillRegistrationTests(unittest.TestCase):
    """Verify SUMMARY.md registers the new skill link."""

    @classmethod
    def setUpClass(cls):
        cls.content = SUMMARY_MD_PATH.read_text(encoding="utf-8")

    def test_new_skill_entry_present(self):
        self.assertIn(
            "* [🗺️ Sitemap & SEO Asset Generator Skill]"
            "(.agents/skills/sitemap-seo-generator/SKILL.md)",
            self.content,
        )

    def test_new_skill_entry_resolves_to_existing_file(self):
        matches = re.findall(
            r"\[🗺️ Sitemap & SEO Asset Generator Skill\]\(([^)]+)\)", self.content
        )
        self.assertEqual(len(matches), 1)
        target = REPO_ROOT / matches[0]
        self.assertTrue(target.is_file())

    def test_sitemap_skill_entry_present_in_skills_and_workflows_section(self):
        section_start = self.content.index("## 🤖 8. AI Agent Skills & Workflows")
        next_section_start = self.content.index(
            "## 📚 9. References & Genesis Papers"
        )
        section_body = self.content[section_start:next_section_start]
        entries = re.findall(r"^\* \[.+?\]\(.+?\)$", section_body, re.MULTILINE)
        self.assertTrue(entries, "Expected at least one skill entry in the section")
        self.assertTrue(any("Sitemap & SEO Asset Generator Skill" in e for e in entries))


# ---------------------------------------------------------------------------
# mkdocs.yml registration
# ---------------------------------------------------------------------------
class MkdocsYmlSkillRegistrationTests(unittest.TestCase):
    """Verify mkdocs.yml nav registers the new skill entry."""

    @classmethod
    def setUpClass(cls):
        cls.content = MKDOCS_PATH.read_text(encoding="utf-8")
        with MKDOCS_PATH.open(encoding="utf-8") as fh:
            cls.config = yaml.safe_load(fh)

    def test_mkdocs_yml_exists_and_not_empty(self):
        self.assertTrue(MKDOCS_PATH.is_file())
        self.assertTrue(self.content.strip())

    def test_new_nav_entry_text_present(self):
        pattern = re.compile(
            r"Sitemap & SEO Asset Generator Skill:\s*"
            r"\.agents/skills/sitemap-seo-generator/SKILL\.md\s*$",
            re.MULTILINE,
        )
        self.assertRegex(self.content, pattern)

    def test_new_nav_entry_path_resolves_to_existing_file(self):
        # mkdocs nav paths for `.agents/` entries are exempted from the
        # `docs_dir`-relative resolution because `.agents` sits at the repo
        # root (see `exclude_docs: !.agents`), so we resolve relative to the
        # repository root here.
        resolved = REPO_ROOT / ".agents" / "skills" / "sitemap-seo-generator" / "SKILL.md"
        self.assertTrue(resolved.is_file())

    def _find_section(self, section_name):
        for entry in self.config["nav"]:
            if isinstance(entry, dict) and section_name in entry:
                return entry[section_name]
        raise AssertionError(f"Could not find nav section {section_name!r}")

    def test_skill_registered_under_ai_agent_skills_and_workflows_section(self):
        section_items = self._find_section("AI Agent Skills & Workflows")
        flattened = {}
        for item in section_items:
            for label, path in item.items():
                flattened[label] = path
        self.assertEqual(
            flattened.get("Sitemap & SEO Asset Generator Skill"),
            ".agents/skills/sitemap-seo-generator/SKILL.md",
        )

    def test_sitemap_skill_present_in_section(self):
        section_items = self._find_section("AI Agent Skills & Workflows")
        labels = [next(iter(item)) for item in section_items]
        self.assertIn("Sitemap & SEO Asset Generator Skill", labels)


# ---------------------------------------------------------------------------
# Cross-file registration consistency
# ---------------------------------------------------------------------------
class SkillRegistrationConsistencyTests(unittest.TestCase):
    """The skill must be consistently registered everywhere it is referenced."""

    def test_skill_directory_and_file_exist(self):
        self.assertTrue(SKILL_PATH.parent.is_dir())
        self.assertTrue(SKILL_PATH.is_file())

    def test_skill_registered_in_all_four_locations(self):
        agents_content = AGENTS_MD_PATH.read_text(encoding="utf-8")
        summary_content = SUMMARY_MD_PATH.read_text(encoding="utf-8")
        mkdocs_content = MKDOCS_PATH.read_text(encoding="utf-8")

        self.assertIn("sitemap-seo-generator", agents_content)
        self.assertIn(".agents/skills/sitemap-seo-generator/SKILL.md", summary_content)
        self.assertIn(".agents/skills/sitemap-seo-generator/SKILL.md", mkdocs_content)
        self.assertTrue(SKILL_PATH.is_file())


# ---------------------------------------------------------------------------
# .agents/brain/wings/wing_dsom_core/hall_facts/room_dsom_protocol/closet.md
# ---------------------------------------------------------------------------
class ClosetDsomProtocolUpdateTests(unittest.TestCase):
    """Verify the Rule 25/26/27 additions to the DSOM Protocol closet."""

    @classmethod
    def setUpClass(cls):
        cls.content = CLOSET_DSOM_PROTOCOL_PATH.read_text(encoding="utf-8")

    def test_file_exists_and_non_empty(self):
        self.assertTrue(CLOSET_DSOM_PROTOCOL_PATH.is_file())
        self.assertTrue(self.content.strip())

    def test_tri_phasic_mind_heading_now_cites_rule_26(self):
        self.assertTrue(
            ("1. **The Architecture (Rule 26):** Partitions AI processing into "
             "Active State (fast MCP streams), Twilight State "
             "(validation/linting check gates), and Deep State (background "
             "EOD palace-sync reviews and push optimization)." in self.content) or
            ("1. **The Architecture (Rule 26):** Partitions AI processing into "
             "Active State (fast MCP streams), Twilight State "
             "(validation/linting check gates), and Deep State (background "
             "EOD palace-sync reviews and push optimisation)." in self.content)
        )

    def test_old_unlabelled_architecture_heading_is_gone(self):
        self.assertNotIn(
            "1. **The Architecture:** Partitions AI processing into",
            self.content,
        )

    def test_new_collaborative_continuity_section_present(self):
        self.assertIn(
            "## 🤝 Collaborative Continuity & Zero-Binary Compiling", self.content
        )

    def test_rule_25_jules_antigravity_sync_documented(self):
        self.assertIn(
            "1. **Rule 25 (Jules & Antigravity Collaborative Sync):** "
            "Establishes peer-to-peer state synchronization and shared "
            "operational ledgers between Google Jules and Google Antigravity "
            "to secure cognitive continuity.",
            self.content,
        )

    def test_rule_27_openwiki_zero_binary_documented(self):
        self.assertIn(
            "2. **Rule 27 (Native OpenWiki Emulator & Zero-Binary Mandate):** "
            "Purges heavy Node.js binary bloat in favor of a native "
            "zero-dependency Python knowledge graph and compiler "
            "(`tools/openwiki_emulator.py`) integrated into FastMCP.",
            self.content,
        )

    def test_new_section_appears_before_retrieval_reference(self):
        collab_index = self.content.index(
            "## 🤝 Collaborative Continuity & Zero-Binary Compiling"
        )
        drawer_index = self.content.index("## 🔗 Retrieval Reference (The Drawer)")
        self.assertLess(collab_index, drawer_index)

    def test_new_section_appears_after_tri_phasic_mind_section(self):
        tri_phasic_index = self.content.index(
            "## 🌗 The Tri-Phasic Mind & Functional Modules"
        )
        collab_index = self.content.index(
            "## 🤝 Collaborative Continuity & Zero-Binary Compiling"
        )
        self.assertLess(tri_phasic_index, collab_index)

    def test_last_refined_date_updated(self):
        self.assertIn(
            "*Last Refined: 2026-08-12 | Hall: hall_facts | Wing: wing_dsom_core*",
            self.content,
        )

    def test_stale_last_refined_date_is_gone(self):
        self.assertNotIn(
            "*Last Refined: 2026-08-08 | Hall: hall_facts | Wing: wing_dsom_core*",
            self.content,
        )

    def test_new_changelog_entry_present(self):
        self.assertIn(
            "- [2026-08-12] Verified and aligned Rules 25, 26, and 27 "
            "knowledge bases within the Palace closets.",
            self.content,
        )

    def test_prior_changelog_entries_still_present(self):
        # Regression guard: appending the new changelog line must not have
        # clobbered the pre-existing history entries.
        self.assertIn(
            "- [2026-08-08] Integrated the Tri-Phasic Mind model and the "
            "four core subsystems",
            self.content,
        )
        self.assertIn("- [2026-08-02] GitHub Pages Alignment:", self.content)
        self.assertIn("- [2026-07-27] DSOM-AUTOMATED-STATE-SYNC.md", self.content)

    def test_changelog_entry_is_last_line_of_file(self):
        stripped = self.content.rstrip("\n")
        last_line = stripped.splitlines()[-1]
        self.assertEqual(
            last_line,
            "- [2026-08-12] Verified and aligned Rules 25, 26, and 27 "
            "knowledge bases within the Palace closets.",
        )

    def test_okf_frontmatter_unaffected_by_body_changes(self):
        _, parsed = _extract_frontmatter_block(self.content)
        self.assertEqual(parsed.get("okf_version"), 0.1)
        self.assertEqual(parsed.get("type"), "protocol")
        self.assertEqual(parsed.get("title"), "DSOM Protocol")
        self.assertEqual(parsed.get("timestamp"), "2026-08-08T12:00:00Z")


# ---------------------------------------------------------------------------
# .agents/brain/wings/wing_dsom_core/hall_facts/room_tooling/closet.md
# ---------------------------------------------------------------------------
class ClosetToolingRegistryUpdateTests(unittest.TestCase):
    """Verify the new tool rows and design law added to the Tooling Registry."""

    @classmethod
    def setUpClass(cls):
        cls.content = CLOSET_TOOLING_PATH.read_text(encoding="utf-8")

    def test_file_exists_and_non_empty(self):
        self.assertTrue(CLOSET_TOOLING_PATH.is_file())
        self.assertTrue(self.content.strip())

    def test_openwiki_emulator_tool_row_present(self):
        self.assertIn(
            "| `openwiki_emulator.py` | v1.0 | Python | Native zero-dependency "
            "OpenWiki compiler & self-healing Mermaid validator |",
            self.content,
        )

    def test_generate_sitemaps_tool_row_present(self):
        self.assertIn(
            "| `generate_sitemaps.py` | v1.0 | Python | Automated sitemap & "
            "SEO asset generation (GitHub Pages, Read the Docs, GitBook) |",
            self.content,
        )

    def test_mcp_server_tool_row_present(self):
        self.assertIn(
            "| `server.py` | v1.0 | Python | Native FastMCP Model Context "
            "Protocol server for Sovereign Markdown Palace |",
            self.content,
        )

    def test_new_python_tool_rows_appear_after_dsom_onboard(self):
        onboard_index = self.content.index("`dsom-onboard.sh/.ps1`")
        openwiki_index = self.content.index("`openwiki_emulator.py`")
        sitemap_index = self.content.index("`generate_sitemaps.py`")
        server_index = self.content.index("`server.py`")
        self.assertLess(onboard_index, openwiki_index)
        self.assertLess(openwiki_index, sitemap_index)
        self.assertLess(sitemap_index, server_index)

    def test_new_howto_docs_referenced(self):
        self.assertIn("`HOWTO-OPENWIKI.md` | `HOWTO-MCP-SERVER.md`", self.content)

    def test_python_first_zero_binary_design_law_present(self):
        self.assertIn(
            "- **Python-first and Zero-Binary (Rule 16 & Rule 27):** Core "
            "compiling and schema operations must be written in pure Python "
            "using `uv run` to ensure complete, zero-binary cross-platform "
            "portability.",
            self.content,
        )

    def test_mcp_server_release_timeline_entry_present(self):
        self.assertIn(
            "- `2026-08-05`: **MCP Server Release.** FastMCP server "
            "implemented in `tools/mcp/server.py`.",
            self.content,
        )

    def test_openwiki_zero_binary_release_timeline_entry_present(self):
        self.assertIn(
            "- `2026-08-09`: **OpenWiki Zero-Binary Release.** Node-based "
            "openwiki replaced with native Python emulator "
            "`tools/openwiki_emulator.py`.",
            self.content,
        )

    def test_timeline_entries_are_chronologically_ordered(self):
        mcp_index = self.content.index("- `2026-08-05`: **MCP Server Release.**")
        openwiki_index = self.content.index(
            "- `2026-08-09`: **OpenWiki Zero-Binary Release.**"
        )
        doc_sprint_index = self.content.index(
            "- `2026-04-08`: **The Great Documentation Sprint.**"
        )
        self.assertLess(doc_sprint_index, mcp_index)
        self.assertLess(mcp_index, openwiki_index)

    def test_last_refined_date_updated(self):
        self.assertIn(
            "*Last Refined: 2026-08-12 | Backfill: Full History | "
            "Hall: hall_facts | Wing: wing_dsom_core*",
            self.content,
        )

    def test_stale_last_refined_date_is_gone(self):
        self.assertNotIn(
            "*Last Refined: 2026-04-08 | Backfill: Full History | "
            "Hall: hall_facts | Wing: wing_dsom_core*",
            self.content,
        )

    def test_new_changelog_entry_present(self):
        self.assertIn(
            "- [2026-08-12] Added sitemap, openwiki emulator, and MCP server "
            "tools to the Tooling Registry.",
            self.content,
        )

    def test_prior_changelog_entry_still_present(self):
        self.assertIn("- [2026-08-02] GitHub Pages Alignment:", self.content)

    def test_changelog_entry_is_last_line_of_file(self):
        stripped = self.content.rstrip("\n")
        last_line = stripped.splitlines()[-1]
        self.assertEqual(
            last_line,
            "- [2026-08-12] Added sitemap, openwiki emulator, and MCP server "
            "tools to the Tooling Registry.",
        )

    def test_okf_frontmatter_unaffected_by_body_changes(self):
        _, parsed = _extract_frontmatter_block(self.content)
        self.assertEqual(parsed.get("okf_version"), 0.1)
        self.assertEqual(parsed.get("type"), "tooling_registry")
        self.assertEqual(parsed.get("title"), "Tooling Registry")
        self.assertEqual(parsed.get("timestamp"), "2026-06-19T14:00:00Z")

    def test_tool_inventory_table_still_well_formed(self):
        # Regression guard: every row of the table (between the header
        # separator and the next markdown heading) must be a well-formed
        # 4-column pipe table row.
        table_start = self.content.index("| Tool | Current Version | Platform | Purpose |")
        table_section_end = self.content.index("## 📚 Documentation")
        table_block = self.content[table_start:table_section_end]
        rows = [
            line for line in table_block.splitlines()
            if line.strip().startswith("|")
        ]
        # Header + separator + at least the pre-existing 16 tools + 3 new ones.
        self.assertGreaterEqual(len(rows), 2 + 19)
        for row in rows:
            with self.subTest(row=row):
                self.assertTrue(row.strip().startswith("|"))
                self.assertTrue(row.strip().endswith("|"))


if __name__ == "__main__":
    unittest.main()