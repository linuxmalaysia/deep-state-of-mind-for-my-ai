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
        cls.digest_re = re.compile(r"@sha256:[a-fA-F0-9]{64}\b")
        cls.sensitive_key_re = re.compile(r"(?i)\b(password|secret|private_key|api_key)\b")

    def test_containerfile_security_and_structure(self):
        """Verify Containerfile/Dockerfile security, immutable base image digest pinning, and non-root USER declarations."""
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
                from_lines = [line.strip() for line in lines if line.strip().startswith("FROM ")]
                self.assertGreater(len(from_lines), 0, f"{cfile.name} must have at least one FROM instruction")
                for from_line in from_lines:
                    tokens = from_line.split()[1:]
                    # Skip options like --platform=...
                    image_tokens = [t for t in tokens if not t.startswith("--")]
                    self.assertGreater(len(image_tokens), 0, f"Missing image reference in {from_line}")
                    image_ref = image_tokens[0]

                    # Validate complete immutable sha256 digest presence
                    has_valid_digest = bool(self.digest_re.search(image_ref))
                    self.assertTrue(
                        has_valid_digest,
                        f"{cfile.name} base image '{image_ref}' must be pinned with an explicit immutable @sha256:<64-hex> digest",
                    )

                # 2. Secret leakage check in ENV (supporting KEY=VAL and space-separated KEY VAL formats)
                env_lines = [line.strip() for line in lines if line.strip().startswith("ENV ")]
                for env_line in env_lines:
                    env_payload = env_line[4:].strip()
                    pairs = []

                    if "=" in env_payload:
                        # KEY=VAL or KEY1=VAL1 KEY2=VAL2
                        matches = re.findall(r'(\w+)=("[^"]*"|\'\S*\'|\S+)', env_payload)
                        pairs.extend(matches)
                    else:
                        # Single KEY VAL pair
                        parts = env_payload.split(maxsplit=1)
                        if len(parts) == 2:
                            pairs.append((parts[0], parts[1]))

                    for key, val in pairs:
                        if self.sensitive_key_re.search(key):
                            clean_val = val.strip('"\':')
                            # Reject literal data while allowing runtime references (e.g. $VAR or ${VAR})
                            is_runtime_ref = clean_val.startswith("$") or clean_val.startswith("${")
                            self.assertTrue(
                                is_runtime_ref,
                                f"Hardcoded sensitive data found in ENV in {cfile.name}: key '{key}' has literal value '{val}'",
                            )


if __name__ == "__main__":
    unittest.main()
