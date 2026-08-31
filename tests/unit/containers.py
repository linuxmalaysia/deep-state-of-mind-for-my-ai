"""
Containerfile / Dockerfile security unit tests.
"""
import pathlib
import re
import unittest
import yaml

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

                # 2. Secret leakage check in ENV (matching both KEY=VAL and KEY VAL formats)
                env_lines = [line.strip() for line in lines if line.strip().startswith("ENV ")]
                for env_line in env_lines:
                    self.assertNotRegex(
                        env_line,
                        r"(?i)\b(password|secret|private_key|api_key)\b\s*(=|\s)",
                        f"Hardcoded sensitive data found in ENV in {cfile.name}",
                    )


class TestQuadletManifestSchema(unittest.TestCase):
    """Podman 5+ Quadlet .kube and .yaml manifest schema validation tests."""

    @classmethod
    def setUpClass(cls):
        cls.repo_root = _find_repo_root(pathlib.Path(__file__).parent)
        cls.digest_re = re.compile(r"@sha256:[a-fA-F0-9]{64}\b")

    def test_quadlet_kube_unit_files(self):
        """Validate Quadlet .kube and .kube.j2 files against Podman 5+ unit specification."""
        kube_files = list(self.repo_root.glob("**/*.kube")) + list(self.repo_root.glob("**/*.kube.j2"))
        kube_files = [
            f for f in kube_files
            if not any(part.startswith(".") or part in ("venv", "site", "build", "node_modules") for part in f.parts)
        ]
        self.assertGreater(len(kube_files), 0, "At least one Quadlet .kube or .kube.j2 unit file must exist")

        for kfile in kube_files:
            with self.subTest(file=kfile.name):
                content = kfile.read_text(encoding="utf-8")
                self.assertIn("[Unit]", content, f"{kfile.name} missing [Unit] section header")
                self.assertIn("[Kube]", content, f"{kfile.name} missing [Kube] section header")
                self.assertIn("[Install]", content, f"{kfile.name} missing [Install] section header")
                self.assertIn("Yaml=", content, f"{kfile.name} must specify 'Yaml=' parameter under [Kube]")
                self.assertIn("WantedBy=", content, f"{kfile.name} must specify 'WantedBy=' parameter under [Install]")

    def test_quadlet_yaml_manifest_schema_and_performance_tuning(self):
        """Validate Quadlet Kubernetes .yaml Pod manifests and PostgreSQL tuning parameters."""
        yaml_files = list(self.repo_root.glob("**/gitea-stack.yaml")) + list(self.repo_root.glob("**/gitea-stack.yaml.j2"))
        yaml_files = [
            f for f in yaml_files
            if not any(part.startswith(".") or part in ("venv", "site", "build", "node_modules") for part in f.parts)
        ]
        self.assertGreater(len(yaml_files), 0, "At least one Quadlet .yaml Pod manifest must exist")

        for yfile in yaml_files:
            with self.subTest(file=yfile.name):
                raw_content = yfile.read_text(encoding="utf-8")
                clean_content = re.sub(r"\{\{.*?\}\}", "placeholder", raw_content)
                doc = yaml.safe_load(clean_content)

                self.assertEqual(doc.get("apiVersion"), "v1", f"{yfile.name} apiVersion must be v1")
                self.assertEqual(doc.get("kind"), "Pod", f"{yfile.name} kind must be Pod")
                self.assertIn("metadata", doc, f"{yfile.name} missing metadata section")
                self.assertIn("name", doc["metadata"], f"{yfile.name} missing metadata.name")

                spec = doc.get("spec", {})
                self.assertIn("containers", spec, f"{yfile.name} missing spec.containers")
                containers = spec["containers"]
                self.assertGreater(len(containers), 0, f"{yfile.name} containers list cannot be empty")

                # Verify container base image sha256 pinning
                for container in containers:
                    cname = container.get("name", "unnamed")
                    image = container.get("image", "")
                    self.assertTrue(
                        self.digest_re.search(image),
                        f"Container '{cname}' image '{image}' in {yfile.name} must be pinned with @sha256 digest",
                    )

                # Check PostgreSQL performance tuning parameters for large GitOps repos
                pg_container = next((c for c in containers if "db" in c.get("name", "") or "postgres" in c.get("image", "")), None)
                self.assertIsNotNone(pg_container, f"PostgreSQL container must be defined in {yfile.name}")

                # Reject PostgreSQL command override
                self.assertNotIn(
                    "command",
                    pg_container,
                    f"PostgreSQL container in {yfile.name} must not override 'command', use 'args' instead so entrypoint initialises properly",
                )

                pg_args = pg_container.get("args", [])
                pg_args_str = " ".join(pg_args)
                env_vars = {e.get("name"): str(e.get("value")) for e in pg_container.get("env", []) if isinstance(e, dict)}

                has_conn_tuning = bool(re.search(r"\bmax_connections\b", pg_args_str)) or "POSTGRES_MAX_CONNECTIONS" in env_vars
                has_buf_tuning = bool(re.search(r"\bshared_buffers\b", pg_args_str)) or "POSTGRES_SHARED_BUFFERS" in env_vars
                has_cache_tuning = bool(re.search(r"\beffective_cache_size\b", pg_args_str)) or "POSTGRES_EFFECTIVE_CACHE_SIZE" in env_vars
                has_maint_tuning = bool(re.search(r"\bmaintenance_work_mem\b", pg_args_str)) or "POSTGRES_MAINTENANCE_WORK_MEM" in env_vars
                has_work_tuning = bool(re.search(r"(?<!maintenance_)work_mem\b", pg_args_str)) or ("POSTGRES_WORK_MEM" in env_vars and "POSTGRES_MAINTENANCE_WORK_MEM" not in env_vars)

                self.assertTrue(has_conn_tuning, f"PostgreSQL max_connections tuning parameter missing in {yfile.name}")
                self.assertTrue(has_buf_tuning, f"PostgreSQL shared_buffers tuning parameter missing in {yfile.name}")
                self.assertTrue(has_cache_tuning, f"PostgreSQL effective_cache_size tuning parameter missing in {yfile.name}")
                self.assertTrue(has_maint_tuning, f"PostgreSQL maintenance_work_mem tuning parameter missing in {yfile.name}")
                self.assertTrue(has_work_tuning, f"PostgreSQL work_mem tuning parameter missing in {yfile.name}")


if __name__ == "__main__":
    unittest.main()
