# ==============================================================================
# Protocol    : Deep State of Mind (DSOM) For My AI
# Author      : Harisfazillah Jamel (LinuxMalaysia)
# Timestamp   : 2026-08-05
# License     : GNU General Public License v3.0
# Standard    : UK English | DBP-standard Bahasa Melayu Malaysia (Piawai)
# ==============================================================================
"""
Unit tests for the Read the Docs configuration file (.readthedocs.yaml).

This verifies that:
1. The .readthedocs.yaml file exists at the root of the repository.
2. The file is a valid YAML document.
3. The configuration declared complies with the required parameters (version 2, MkDocs, etc.).
4. The DSOM Sovereign Signature/header is present.
"""
import pathlib
import unittest
import yaml  # type: ignore


def _find_repo_root(start: pathlib.Path) -> pathlib.Path:
    """Locate the repository root from a starting path."""
    current = start.resolve()
    for parent in [current, *current.parents]:
        if (parent / ".git").exists():
            return parent
    raise RuntimeError("Could not locate repository root (.git not found)")


REPO_ROOT = _find_repo_root(pathlib.Path(__file__).parent)
READTHEDOCS_PATH = REPO_ROOT / ".readthedocs.yaml"


class ReadthedocsConfigTests(unittest.TestCase):
    """Verify existence, structure, and values in .readthedocs.yaml."""

    @classmethod
    def setUpClass(cls) -> None:
        """
        Load the Read the Docs configuration file and store its text and parsed YAML content for the test class.
        """
        cls.content = ""
        cls.config = None
        if READTHEDOCS_PATH.is_file():
            cls.content = READTHEDOCS_PATH.read_text(encoding="utf-8")
            with READTHEDOCS_PATH.open(encoding="utf-8") as fh:
                cls.config = yaml.safe_load(fh)

    def test_readthedocs_yaml_exists(self):
        self.assertTrue(READTHEDOCS_PATH.is_file(), "Expected .readthedocs.yaml to exist")

    def test_dsom_signature_present(self):
        """Verify that the DSOM Sovereign Signature/header is present in the file."""
        self.assertIn(
            "Protocol    : Deep State of Mind (DSOM) For My AI",
            self.content,
            "Expected the DSOM Sovereign Signature header to be present",
        )
        self.assertIn(
            "Author      : Harisfazillah Jamel (LinuxMalaysia)",
            self.content,
            "Expected Harisfazillah Jamel to be declared as Author",
        )
        self.assertIn(
            "Timestamp   : 2026-08-05",
            self.content,
            "Expected correct Timestamp in DSOM header",
        )
        self.assertIn(
            "License     : GNU General Public License v3.0",
            self.content,
            "Expected correct License in DSOM header",
        )
        self.assertIn(
            "Standard    : UK English | DBP-standard Bahasa Melayu Malaysia (Piawai)",
            self.content,
            "Expected correct Standard in DSOM header",
        )

    def test_version_is_2(self):
        self.assertIsInstance(self.config, dict, "Expected configuration to be a dictionary")
        self.assertEqual(self.config.get("version"), 2, "Expected version: 2 in .readthedocs.yaml")

    def test_build_os_and_tools(self):
        self.assertIsInstance(self.config, dict, "Expected configuration to be a dictionary")
        build = self.config.get("build", {})
        self.assertIsInstance(build, dict, "Expected build configuration to be a dictionary")
        self.assertEqual(build.get("os"), "ubuntu-24.04", "Expected build.os to be ubuntu-24.04")
        tools = build.get("tools", {})
        self.assertIsInstance(tools, dict, "Expected build tools configuration to be a dictionary")
        self.assertEqual(tools.get("python"), "3.13", "Expected build.tools.python to be '3.13'")

    def test_mkdocs_configuration(self):
        self.assertIsInstance(self.config, dict, "Expected configuration to be a dictionary")
        mkdocs = self.config.get("mkdocs", {})
        self.assertIsInstance(mkdocs, dict, "Expected mkdocs configuration to be a dictionary")
        self.assertEqual(
            mkdocs.get("configuration"),
            "mkdocs.yml",
            "Expected mkdocs.configuration to point to mkdocs.yml",
        )
        mkdocs_file = REPO_ROOT / "mkdocs.yml"
        self.assertTrue(
            mkdocs_file.is_file(),
            f"Expected {mkdocs_file} to be an existing file",
        )

    def test_python_install_requirements(self):
        """Verify the python.install section points at docs/requirements.txt."""
        self.assertIsInstance(self.config, dict, "Expected configuration to be a dictionary")
        python_section = self.config.get("python", {})
        self.assertIsInstance(python_section, dict, "Expected python configuration to be a dictionary")
        install = python_section.get("install")
        self.assertIsInstance(install, list, "Expected python.install to be a list")
        self.assertEqual(len(install), 1, "Expected exactly one python.install entry")
        self.assertEqual(
            install[0],
            {"requirements": "docs/requirements.txt"},
            "Expected python.install to declare docs/requirements.txt",
        )
        requirements_file = REPO_ROOT / "docs" / "requirements.txt"
        self.assertTrue(
            requirements_file.is_file(),
            f"Expected {requirements_file} to be an existing file",
        )

    def test_top_level_keys_are_exactly_expected(self):
        """Regression guard: no stray or missing top-level keys."""
        self.assertIsInstance(self.config, dict, "Expected configuration to be a dictionary")
        self.assertEqual(
            set(self.config.keys()),
            {"version", "build", "mkdocs", "python"},
            "Expected exactly version, build, mkdocs, and python top-level keys",
        )

    def test_version_is_integer_type(self):
        # Read the Docs requires an unquoted integer 2, not the string "2".
        self.assertIsInstance(self.config, dict, "Expected configuration to be a dictionary")
        self.assertIsInstance(
            self.config.get("version"),
            int,
            "Expected version to parse as an integer, not a string",
        )

    def test_build_tools_python_version_is_string_type(self):
        # Quoted "3.13" must remain a string; unquoted 3.13 would be parsed
        # as a float by YAML and silently drop the trailing zero semantics.
        self.assertIsInstance(self.config, dict, "Expected configuration to be a dictionary")
        tools = self.config.get("build", {}).get("tools", {})
        self.assertIsInstance(
            tools.get("python"),
            str,
            "Expected build.tools.python to be a quoted string",
        )

    def test_file_is_not_empty(self):
        self.assertTrue(self.content.strip(), ".readthedocs.yaml should not be empty")

    def test_no_tab_characters(self):
        # YAML is whitespace-sensitive; tabs are a common source of subtle bugs.
        self.assertNotIn("\t", self.content, ".readthedocs.yaml should not contain tab characters")


class DocsRequirementsFileTests(unittest.TestCase):
    """Verify docs/requirements.txt referenced by .readthedocs.yaml."""

    REQUIREMENTS_PATH = REPO_ROOT / "docs" / "requirements.txt"

    @classmethod
    def setUpClass(cls):
        cls.content = ""
        if cls.REQUIREMENTS_PATH.is_file():
            cls.content = cls.REQUIREMENTS_PATH.read_text(encoding="utf-8")

    def test_requirements_file_exists(self):
        self.assertTrue(
            self.REQUIREMENTS_PATH.is_file(),
            f"Expected {self.REQUIREMENTS_PATH} to exist",
        )

    def test_requirements_file_not_empty(self):
        self.assertTrue(self.content.strip(), "docs/requirements.txt should not be empty")

    def test_declares_mkdocs_material_dependency(self):
        self.assertIn(
            "mkdocs-material",
            self.content,
            "Expected docs/requirements.txt to declare mkdocs-material",
        )


if __name__ == "__main__":
    unittest.main()
