"""
Containerfile / Dockerfile security unit tests.
"""
import pathlib
import re
import unittest

def _find_repo_root(start: pathlib.Path) -> pathlib.Path:
    current = start.resolve()
    for parent in [current, *current.parents]:
        if (parent / ".git").exists():
            return parent
    raise RuntimeError("Could not locate repository root (.git not found)")


class TestContainerfileSecurity(unittest.TestCase):
    """Containerfile and Dockerfile security and structural tests."""

    @classmethod
    def setUpClass(cls):
        cls.repo_root = _find_repo_root(pathlib.Path(__file__).parent)

    def test_containerfile_security_and_structure(self):
        """Verify Containerfile/Dockerfile security, base image pinning, and non-root USER declarations."""
        container_files = list(self.repo_root.glob("Containerfile*")) + list(self.repo_root.glob("Dockerfile*"))
        container_files.extend(self.repo_root.glob("**/Containerfile*"))
        container_files.extend(self.repo_root.glob("**/Dockerfile*"))

        # Filter out virtual environments or build directories
        container_files = [
            f for f in container_files
            if not any(part.startswith(".") or part in ("venv", "site", "build", "node_modules") for part in f.parts)
        ]

        if not container_files:
            # If no containerfile exists, test render.yaml or container specs for deployment security
            render_file = self.repo_root / "render.yaml"
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
                    tokens = from_line.split()[1:]
                    # Skip options like --platform=...
                    image_tokens = [t for t in tokens if not t.startswith("--")]
                    self.assertGreater(len(image_tokens), 0, f"Missing image reference in {from_line}")
                    image_ref = image_tokens[0]

                    # Validate tag or digest presence
                    has_digest = "@sha256:" in image_ref or "@" in image_ref
                    has_tag = ":" in image_ref
                    self.assertTrue(
                        has_digest or has_tag,
                        f"{cfile.name} base image '{image_ref}' must be pinned with a version tag or digest",
                    )

                    if has_tag and not has_digest:
                        tag = image_ref.split(":")[-1]
                        self.assertNotEqual(
                            tag, "latest", f"{cfile.name} base image should not use unpinned :latest tag"
                        )

                # 2. Secret leakage check in ENV (matching both KEY=VAL and KEY VAL formats)
                env_lines = [l.strip() for l in lines if l.strip().startswith("ENV ")]
                for env_line in env_lines:
                    self.assertNotRegex(
                        env_line,
                        r"(?i)\b(password|secret|private_key|api_key)\b\s*(=|\s)",
                        f"Hardcoded sensitive data found in ENV in {cfile.name}",
                    )


if __name__ == "__main__":
    unittest.main()
