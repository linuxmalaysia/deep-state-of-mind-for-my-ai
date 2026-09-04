"""
Unit test for auditing the token footprint of all .agents/skills/*/SKILL.md files.

Enforces Rule 10 / Byte-Capped Execution Framework circuit breaker:
No individual SKILL.md file may breach the 4,000-token threshold.
"""
import pathlib
import unittest

try:
    import tiktoken
    HAS_TIKTOKEN = True
except ImportError:
    HAS_TIKTOKEN = False

GATE_THRESHOLD = 4000


def _find_repo_root(start: pathlib.Path) -> pathlib.Path:
    current = start.resolve()
    for parent in [current, *current.parents]:
        if (parent / ".git").exists():
            return parent
    raise RuntimeError("Could not locate repository root (.git not found)")


REPO_ROOT = _find_repo_root(pathlib.Path(__file__).parent)
SKILLS_DIR = REPO_ROOT / ".agents" / "skills"


@unittest.skipUnless(HAS_TIKTOKEN, "tiktoken is not installed in this environment")
class SkillTokenFootprintTests(unittest.TestCase):
    """Audits token counts across all SKILL.md files in .agents/skills/."""

    @classmethod
    def setUpClass(cls):
        try:
            cls.enc = tiktoken.encoding_for_model("gpt-4")
        except Exception:
            cls.enc = tiktoken.get_encoding("cl100k_base")

    def test_skills_directory_exists(self):
        self.assertTrue(SKILLS_DIR.is_dir(), f"Skills directory not found at {SKILLS_DIR}")

    def test_no_skill_md_breaches_token_gate(self):
        skill_files = list(SKILLS_DIR.glob("*/SKILL.md"))
        self.assertGreater(len(skill_files), 0, "Expected at least one SKILL.md file")

        breaches = []
        for skill_path in sorted(skill_files):
            rel_path = skill_path.relative_to(REPO_ROOT)
            content = skill_path.read_text(encoding="utf-8", errors="ignore")
            token_count = len(self.enc.encode(content))
            if token_count >= GATE_THRESHOLD:
                breaches.append((str(rel_path), token_count))

        self.assertEqual(
            len(breaches),
            0,
            f"The following SKILL.md files breached the {GATE_THRESHOLD:,}-token gate: {breaches}",
        )


if __name__ == "__main__":
    unittest.main()
