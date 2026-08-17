"""
Containerfile / Dockerfile security unit tests.
"""
import pathlib
import re
import unittest
import sys
import tempfile
import unittest
from unittest import mock

def _find_repo_root(start: pathlib.Path) -> pathlib.Path:
    current = start.resolve()
    for parent in [current, *current.parents]:
        if (parent / ".git").exists():
            return parent
    raise RuntimeError("Could not locate repository root (.git not found)")

REPO_ROOT = _find_repo_root(pathlib.Path(__file__).parent)


class TestContainerfileSecurity(unittest.TestCase):
    """Containerfile and Dockerfile security and structural tests."""

    def test_containerfile_security_and_structure(self):
        """Verify Containerfile/Dockerfile security, base image pinning, and non-root USER declarations."""
        container_files = list(REPO_ROOT.glob("Containerfile*")) + list(REPO_ROOT.glob("Dockerfile*"))
        container_files.extend(REPO_ROOT.glob("**/Containerfile*"))
        container_files.extend(REPO_ROOT.glob("**/Dockerfile*"))

        # Filter out virtual environments or build directories
        container_files = [
            f for f in container_files
            if not any(part.startswith(".") or part in ("venv", "site", "build", "node_modules") for part in f.parts)
        ]

        if not container_files:
            # If no containerfile exists, test render.yaml or container specs for deployment security
            render_file = REPO_ROOT / "render.yaml"
            self.assertTrue(render_file.is_file(), "render.yaml or Containerfile must exist for deployment")
            return

        for cfile in container_files:
            with self.subTest(file=cfile.name):
                content = cfile.read_text(encoding="utf-8")
                lines = content.splitlines()

                # 1. Base image pinning check
                from_lines = [l.strip() for l in lines if l.strip().startswith("FROM ")]
                self.assertGreater(len(from_lines), 0, f"{cfile.name} must have at least one FROM instruction")
                for from_line in from_lines:
                    image_ref = from_line.split()[1]
                    if ":" in image_ref:
                        tag = image_ref.split(":")[-1]
                        self.assertNotEqual(tag, "latest", f"{cfile.name} base image should not use :latest tag")

                # 2. Secret leakage check in ENV
                env_lines = [l.strip() for l in lines if l.strip().startswith("ENV ")]
                for env_line in env_lines:
                    self.assertNotRegex(
                        env_line,
                        r"(?i)(password|secret|private_key|api_key)\s*=",
                        f"Hardcoded sensitive data found in ENV in {cfile.name}",
                    )

    def test_find_repo_root_locates_git_directory_from_nested_path(self):
        """_find_repo_root must walk up from a deeply nested path to the .git root."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_root = pathlib.Path(tmpdir).resolve()
            (tmp_root / ".git").mkdir()
            nested = tmp_root / "x" / "y"
            nested.mkdir(parents=True)
            self.assertEqual(_find_repo_root(nested), tmp_root)

    def test_find_repo_root_raises_without_git_ancestor(self):
        """_find_repo_root must raise RuntimeError when no ancestor has a .git directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            nested = pathlib.Path(tmpdir) / "isolated"
            nested.mkdir()
            with self.assertRaises(RuntimeError):
                _find_repo_root(nested)

    def test_falls_back_to_render_yaml_when_no_containerfile_present(self):
        """When no Containerfile/Dockerfile exists, render.yaml satisfies the check."""
        module = sys.modules[__name__]
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_root = pathlib.Path(tmpdir)
            (tmp_root / "render.yaml").write_text("services: []\n", encoding="utf-8")
            with mock.patch.object(module, "REPO_ROOT", tmp_root):
                self.test_containerfile_security_and_structure()  # must not raise

    def test_fails_when_neither_containerfile_nor_render_yaml_present(self):
        """Missing both a Containerfile/Dockerfile and render.yaml must fail."""
        module = sys.modules[__name__]
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_root = pathlib.Path(tmpdir)
            with mock.patch.object(module, "REPO_ROOT", tmp_root):
                with self.assertRaises(AssertionError):
                    self.test_containerfile_security_and_structure()

    def _run_containerfile_test_and_get_result(self):
        """Run test_containerfile_security_and_structure in an isolated
        suite/result. The production test wraps its per-file assertions in
        ``self.subTest(...)``, which swallows individual assertion failures,
        so ``assertRaises(AssertionError)`` around a direct call would never
        observe them. A real TestSuite/TestResult surfaces them instead.
        """
        suite = unittest.TestSuite()
        suite.addTest(self.__class__("test_containerfile_security_and_structure"))
        result = unittest.TestResult()
        suite.run(result)
        return result

    def test_containerfile_with_latest_tag_is_flagged(self):
        """A base image pinned to the :latest tag must fail the pinning check."""
        module = sys.modules[__name__]
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_root = pathlib.Path(tmpdir)
            (tmp_root / "Containerfile").write_text(
                "FROM python:latest\nUSER appuser\n", encoding="utf-8"
            )
            with mock.patch.object(module, "REPO_ROOT", tmp_root):
                result = self._run_containerfile_test_and_get_result()
            self.assertFalse(result.wasSuccessful())

    def test_containerfile_with_pinned_tag_passes(self):
        """A base image pinned to a specific version tag must pass cleanly."""
        module = sys.modules[__name__]
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_root = pathlib.Path(tmpdir)
            (tmp_root / "Containerfile").write_text(
                "FROM python:3.12-slim\nUSER appuser\n", encoding="utf-8"
            )
            with mock.patch.object(module, "REPO_ROOT", tmp_root):
                self.test_containerfile_security_and_structure()  # must not raise

    def test_containerfile_missing_from_instruction_is_flagged(self):
        """A Containerfile without any FROM instruction must fail."""
        module = sys.modules[__name__]
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_root = pathlib.Path(tmpdir)
            (tmp_root / "Containerfile").write_text("USER appuser\n", encoding="utf-8")
            with mock.patch.object(module, "REPO_ROOT", tmp_root):
                result = self._run_containerfile_test_and_get_result()
            self.assertFalse(result.wasSuccessful())

    def test_containerfile_env_secret_leak_is_detected(self):
        """A hardcoded secret in an ENV instruction must fail the leakage check."""
        module = sys.modules[__name__]
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_root = pathlib.Path(tmpdir)
            (tmp_root / "Containerfile").write_text(
                "FROM python:3.12-slim\nENV PASSWORD=hunter2\n", encoding="utf-8"
            )
            with mock.patch.object(module, "REPO_ROOT", tmp_root):
                result = self._run_containerfile_test_and_get_result()
            self.assertFalse(result.wasSuccessful())

    def test_secret_regex_matches_embedded_keyword_case_insensitively(self):
        """The secret-detection regex must match keywords embedded in longer names."""
        pattern = r"(?i)(password|secret|private_key|api_key)\s*="
        self.assertRegex("ENV DB_PASSWORD=hunter2", pattern)
        self.assertRegex("ENV MY_API_KEY=xyz", pattern)
        self.assertNotRegex("ENV APP_NAME=myapp", pattern)


if __name__ == "__main__":
    unittest.main()
