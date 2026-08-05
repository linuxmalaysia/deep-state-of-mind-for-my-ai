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
    def setUpClass(cls):
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

    def test_version_is_2(self):
        self.assertEqual(self.config.get("version"), 2, "Expected version: 2 in .readthedocs.yaml")

    def test_build_os_and_tools(self):
        build = self.config.get("build", {})
        self.assertEqual(build.get("os"), "ubuntu-24.04", "Expected build.os to be ubuntu-24.04")
        tools = build.get("tools", {})
        self.assertEqual(tools.get("python"), "3.13", "Expected build.tools.python to be '3.13'")

    def test_mkdocs_configuration(self):
        mkdocs = self.config.get("mkdocs", {})
        self.assertEqual(
            mkdocs.get("configuration"),
            "mkdocs.yml",
            "Expected mkdocs.configuration to point to mkdocs.yml",
        )
