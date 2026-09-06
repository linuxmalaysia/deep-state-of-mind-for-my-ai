"""Tests for the Start AI Agents prompt and its documentation registrations."""

from datetime import datetime
from pathlib import Path
import re
import unittest

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
PROMPT_PATH = REPO_ROOT / "docs" / "START-AI-AGENTS-PROMPT.md"

FRONTMATTER_RE = re.compile(
    r"\A---\s*\r?\n(?P<yaml>.*?)(?:\r?\n)?---\s*(?:\r?\n|\Z)",
    re.DOTALL,
)
MARKDOWN_LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
PROMPT_BLOCK_RE = re.compile(r"```markdown\r?\n(?P<prompt>.*?)\r?\n```", re.DOTALL)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class StartAiAgentsPromptTests(unittest.TestCase):
    """Check the prompt document's metadata and executable content contract."""

    @classmethod
    def setUpClass(cls):
        cls.content = _read(PROMPT_PATH)
        frontmatter_match = FRONTMATTER_RE.match(cls.content)
        if frontmatter_match is None:
            raise AssertionError(f"{PROMPT_PATH} must start with YAML frontmatter")
        cls.frontmatter = yaml.safe_load(frontmatter_match.group("yaml"))
        cls.prompt_blocks = PROMPT_BLOCK_RE.findall(cls.content)

    def test_file_is_bom_free_and_starts_with_frontmatter(self):
        self.assertFalse(PROMPT_PATH.read_bytes().startswith(b"\xef\xbb\xbf"))
        self.assertTrue(self.content.startswith("---\n"))

    def test_okf_v02_frontmatter_has_authoritative_trust_signals(self):
        self.assertEqual(self.frontmatter["okf_version"], 0.2)
        self.assertEqual(self.frontmatter["type"], "onboarding")
        self.assertEqual(
            self.frontmatter["title"],
            "Start AI Agents Master Setup Prompt & Execution Protocol",
        )
        self.assertEqual(self.frontmatter["generated"], "human-and-ai")
        self.assertEqual(self.frontmatter["verified"], "verified")
        self.assertEqual(self.frontmatter["status"], "authoritative")
        self.assertEqual(
            self.frontmatter["topics"],
            ["onboarding", "dsom", "ai-agents", "setup"],
        )

    def test_frontmatter_sources_cover_all_onboarding_authorities(self):
        source_urls = {source["url"] for source in self.frontmatter["sources"]}
        self.assertEqual(
            source_urls,
            {
                "https://linuxmalaysia.github.io/deep-state-of-mind-for-my-ai/START-HERE/",
                "https://linuxmalaysia.github.io/deep-state-of-mind-for-my-ai/AGENTS/",
                "https://linuxmalaysia.github.io/deep-state-of-mind-for-my-ai/.agents/AGENTS/",
            },
        )

    def test_stale_after_is_later_than_timestamp(self):
        timestamp = datetime.fromisoformat(
            self.frontmatter["timestamp"].replace("Z", "+00:00")
        )
        stale_after = datetime.fromisoformat(
            self.frontmatter["stale_after"].replace("Z", "+00:00")
        )
        self.assertGreater(stale_after, timestamp)

    def test_contains_one_self_contained_copy_paste_prompt(self):
        self.assertEqual(len(self.prompt_blocks), 1)
        prompt = self.prompt_blocks[0]
        self.assertTrue(prompt.startswith("I need you to setup everything"))
        self.assertIn(
            "Sovereign State Synchronised — DSOM Protocol is fully operational and active.",
            prompt,
        )

    def test_prompt_sections_are_complete_and_ordered(self):
        prompt = self.prompt_blocks[0]
        section_headings = [
            "### 1. DUAL AGENTS.MD ARCHITECTURE SETUP",
            "### 2. SPATIAL MEMORY INITIALISATION (`.agents/brain/`)",
            "### 3. UNIVERSAL GATEWAY MATRIX & DOWNSTREAM FOOTPRINT",
            "### 4. OPEN KNOWLEDGE FORMAT (OKF) & DTS 0.1 COMPLIANCE",
            "### 5. COGNITIVE TWIN PROTOCOL & 4-TIER ENVIRONMENT MAP",
            "### 6. CONFIRMATION HANDSHAKE",
        ]
        positions = [prompt.index(heading) for heading in section_headings]
        self.assertEqual(positions, sorted(positions))

    def test_prompt_names_every_required_gateway_and_brain_file(self):
        prompt = self.prompt_blocks[0]
        required_paths = {
            "`AGENTS.md`",
            "`.agents/AGENTS.md`",
            "`.agents/brain/`",
            "`task.md`",
            "`walkthrough.md`",
            "`palace_registry.md`",
            "`active_context_manifest.md`",
            "`.cursorrules`",
            "`CLAUDE.md`",
            "`.github/copilot-instructions.md`",
            "`README.md`",
            "`CHANGELOG.md`",
            "`HISTORY.md`",
        }
        for path in required_paths:
            with self.subTest(path=path):
                self.assertIn(path, prompt)

    def test_prompt_names_every_environment_tier(self):
        prompt = self.prompt_blocks[0]
        for tier in ("**T1:**", "**T2:**", "**T3:**", "**T4:**"):
            with self.subTest(tier=tier):
                self.assertEqual(prompt.count(tier), 1)

    def test_prompt_preserves_existing_files_before_modification(self):
        prompt = self.prompt_blocks[0]
        safeguards = (
            "inspect proposed targets before modifying",
            "preserve existing project-specific policies and states",
            "create only missing governance or spatial files",
            "request explicit approval before replacing any pre-existing file",
        )
        for safeguard in safeguards:
            with self.subTest(safeguard=safeguard):
                self.assertIn(safeguard, prompt)

    def test_all_relative_markdown_links_resolve(self):
        links = MARKDOWN_LINK_RE.findall(self.content)
        relative_links = [
            link.split("#", 1)[0]
            for link in links
            if link and not re.match(r"^[a-z][a-z0-9+.-]*:", link)
        ]
        self.assertGreater(len(relative_links), 0)
        for link in relative_links:
            with self.subTest(link=link):
                resolved = (PROMPT_PATH.parent / link).resolve()
                self.assertTrue(resolved.exists(), f"Broken relative link: {link}")


class StartAiAgentsRegistrationTests(unittest.TestCase):
    """Check each documentation layer registers Entry Point 23 once."""

    EXPECTED_REGISTRATIONS = {
        "README.md": "docs/START-AI-AGENTS-PROMPT.md",
        "docs/README.md": "docs/START-AI-AGENTS-PROMPT.md",
        "SUMMARY.md": "docs/START-AI-AGENTS-PROMPT.md",
        "docs/SUMMARY.md": "START-AI-AGENTS-PROMPT.md",
        "llms.txt": "docs/START-AI-AGENTS-PROMPT.md",
        "mkdocs.yml": "START-AI-AGENTS-PROMPT.md",
    }

    def test_navigation_layers_register_prompt_once(self):
        for relative_path, expected_target in self.EXPECTED_REGISTRATIONS.items():
            with self.subTest(path=relative_path):
                content = _read(REPO_ROOT / relative_path)
                if relative_path == "mkdocs.yml":
                    registrations = content.count(
                        f"Start AI Agents Setup Prompt: {expected_target}"
                    )
                else:
                    registrations = MARKDOWN_LINK_RE.findall(content).count(
                        expected_target
                    )
                self.assertEqual(
                    registrations,
                    1,
                    f"{relative_path} must register {expected_target} exactly once",
                )

    def test_root_and_docs_start_here_register_entry_point_23(self):
        expected_by_path = {
            "START-HERE.md": "docs/START-AI-AGENTS-PROMPT.md",
            "docs/START-HERE.md": "START-AI-AGENTS-PROMPT.md",
        }
        for relative_path, expected_target in expected_by_path.items():
            with self.subTest(path=relative_path):
                content = _read(REPO_ROOT / relative_path)
                self.assertIn(
                    "## 23. The Start AI Agents Prompt Entry Point",
                    content,
                )
                self.assertIn(expected_target, content)
                self.assertIn("Entry Point 23: Start AI Agents Setup Prompt", content)

    def test_readmes_advertise_23_entry_points(self):
        for relative_path in ("README.md", "docs/README.md"):
            with self.subTest(path=relative_path):
                self.assertIn(
                    "The 23 primary onboarding entry points.",
                    _read(REPO_ROOT / relative_path),
                )


if __name__ == "__main__":
    unittest.main()
