"""
Unit tests for Lola AI Package Manager (lola-ai) integration,
dual-compliant SKILL.md frontmatters, PEP 723 inline script metadata,
and air-gapped Ansible automation in Deep State of Mind (DSOM).
"""

import os
import pathlib
import re
import unittest
import yaml  # type: ignore


def _find_repo_root(start: pathlib.Path) -> pathlib.Path:
    current = start.resolve()
    for parent in [current, *current.parents]:
        if (parent / ".git").exists():
            return parent
    raise RuntimeError("Could not locate repository root (.git not found)")


REPO_ROOT = _find_repo_root(pathlib.Path(__file__).parent)
FRONTMATTER_RE = re.compile(r"\A---\s*\r?\n(.*?)(?:\r?\n)?---\s*(?:\r?\n|\Z)", re.DOTALL)


def _extract_frontmatter_block(content: str):
    match = FRONTMATTER_RE.match(content)
    if not match:
        return None, None
    raw = match.group(1)
    return raw, yaml.safe_load(raw)


class LolaRequirementsManifestTests(unittest.TestCase):
    """Validate root .lola-req declarative manifest."""

    LOLA_REQ_PATH = REPO_ROOT / ".lola-req"

    def test_lola_req_exists_and_non_empty(self):
        self.assertTrue(self.LOLA_REQ_PATH.is_file())
        self.assertTrue(self.LOLA_REQ_PATH.read_text(encoding="utf-8").strip())

    def test_lola_req_contains_pinned_version_comment(self):
        content = self.LOLA_REQ_PATH.read_text(encoding="utf-8")
        self.assertIn("lola-ai>=0.1.0", content)

    def test_lola_req_contains_all_46_skills(self):
        content = self.LOLA_REQ_PATH.read_text(encoding="utf-8")
        lines = [
            line.strip()
            for line in content.splitlines()
            if line.strip() and not line.strip().startswith("#")
        ]
        self.assertEqual(len(lines), 46)

        skills_dir = REPO_ROOT / ".agents" / "skills"
        expected_skills = set(
            f".agents/skills/{d.name}"
            for d in skills_dir.iterdir()
            if d.is_dir()
        )

        declared_paths = set(lines)
        self.assertEqual(declared_paths, expected_skills)

        for rel_path in lines:
            target_dir = REPO_ROOT / rel_path
            self.assertTrue(
                target_dir.is_dir(),
                f"Declared path {rel_path} does not exist as a skill directory.",
            )


class LolaSkillPackageDualFrontmatterTests(unittest.TestCase):
    """Validate dual Lola + OKF v0.2 frontmatter compliance across all 46 skills."""

    def test_all_46_skills_have_dual_compliant_frontmatter(self):
        skills_dir = REPO_ROOT / ".agents" / "skills"
        skill_dirs = sorted([d for d in skills_dir.iterdir() if d.is_dir()])
        self.assertEqual(len(skill_dirs), 46)

        required_keys = [
            "name",
            "version",
            "description",
            "author",
            "license",
            "okf_version",
            "type",
            "topics",
            "status",
            "stale_after",
        ]

        for s_dir in skill_dirs:
            skill_md = s_dir / "SKILL.md"
            self.assertTrue(
                skill_md.is_file(), f"Missing SKILL.md in {s_dir.name}"
            )
            content = skill_md.read_text(encoding="utf-8")
            raw, parsed = _extract_frontmatter_block(content)

            self.assertIsNotNone(
                parsed, f"Failed to parse frontmatter in {skill_md}"
            )
            self.assertIsInstance(
                parsed, dict, f"Frontmatter in {skill_md} must be a mapping"
            )

            for key in required_keys:
                self.assertIn(
                    key,
                    parsed,
                    f"Skill {s_dir.name} SKILL.md missing required key: {key}",
                )

            self.assertEqual(parsed["name"], s_dir.name)
            self.assertEqual(str(parsed["okf_version"]), "0.2")
            self.assertEqual(parsed["status"], "stable")


class Pep723InlineScriptMetadataTests(unittest.TestCase):
    """Validate PEP 723 inline script metadata on Python helper scripts inside skills."""

    def test_python_helper_scripts_contain_pep723_metadata(self):
        skills_dir = REPO_ROOT / ".agents" / "skills"
        py_scripts = list(skills_dir.rglob("scripts/*.py"))
        self.assertGreater(len(py_scripts), 0)

        for py_path in py_scripts:
            content = py_path.read_text(encoding="utf-8")
            self.assertIn(
                "# /// script",
                content,
                f"PEP 723 header '# /// script' missing in {py_path}",
            )
            self.assertIn(
                "# requires-python =",
                content,
                f"PEP 723 'requires-python' missing in {py_path}",
            )
            self.assertIn(
                "# ///",
                content,
                f"PEP 723 closing '# ///' missing in {py_path}",
            )


class RelativePathDecouplingTests(unittest.TestCase):
    """Verify zero absolute workstation path leaks in skills."""

    def test_no_absolute_workstation_paths_in_skills(self):
        skills_dir = REPO_ROOT / ".agents" / "skills"
        forbidden_regexes = [
            re.compile(r"file:///[a-zA-Z0-9_./-]+"),
            re.compile(r"[C-Z]:/[a-zA-Z0-9_./-]+"),
        ]

        for file_path in skills_dir.rglob("*"):
            if file_path.is_file() and not file_path.name.endswith(".pyc"):
                try:
                    content = file_path.read_text(
                        encoding="utf-8", errors="ignore"
                    )
                except (OSError, UnicodeDecodeError):
                    continue
                for reg in forbidden_regexes:
                    matches = reg.findall(content)
                    self.assertEqual(
                        len(matches),
                        0,
                        f"Absolute path or URI leak matches {matches} found in {file_path}",
                    )


class LolaAnsiblePlaybookTests(unittest.TestCase):
    """Validate playbooks/install.yml for air-gapped Lola sync automation."""

    PLAYBOOK_PATH = REPO_ROOT / "playbooks" / "install.yml"

    def test_playbook_exists_and_parses_as_valid_yaml(self):
        self.assertTrue(self.PLAYBOOK_PATH.is_file())
        content = self.PLAYBOOK_PATH.read_text(encoding="utf-8")
        parsed = yaml.safe_load(content)
        self.assertIsInstance(parsed, list)
        self.assertEqual(len(parsed), 1)

    def test_playbook_contains_airgap_lola_check(self):
        content = self.PLAYBOOK_PATH.read_text(encoding="utf-8")
        self.assertIn("which lola", content)
        self.assertIn("lola sync", content)
        self.assertIn("air-gapped environment", content)


class LolaDocumentationTests(unittest.TestCase):
    """Validate 4W1H documentation for Lola AI integration."""

    DOC_PATH = (
        REPO_ROOT
        / "docs"
        / "explanation"
        / "lola-ai-integration-dsom.md"
    )

    def test_doc_exists_and_contains_4w1h_sections(self):
        self.assertTrue(self.DOC_PATH.is_file())
        content = self.DOC_PATH.read_text(encoding="utf-8")

        for term in ("WHAT", "WHY", "WHO", "WHERE", "HOW"):
            self.assertIn(term, content)

    def test_doc_contains_summary_matrix_table(self):
        content = self.DOC_PATH.read_text(encoding="utf-8")
        self.assertIn(
            "| Skill Name | Version | Local Path | Status | Operational Capability |",
            content,
        )


if __name__ == "__main__":
    unittest.main()
