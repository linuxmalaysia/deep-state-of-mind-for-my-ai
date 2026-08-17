"""
Ansible playbook compliance unit tests.
"""
import pathlib
import unittest
import yaml

def _find_repo_root(start: pathlib.Path) -> pathlib.Path:
    current = start.resolve()
    for parent in [current, *current.parents]:
        if (parent / ".git").exists():
            return parent
    raise RuntimeError("Could not locate repository root (.git not found)")


class TestAnsibleCompliance(unittest.TestCase):
    """Ansible playbook and configuration compliance tests."""

    @classmethod
    def setUpClass(cls):
        cls.repo_root = _find_repo_root(pathlib.Path(__file__).parent)

    def test_ansible_playbook_compliance(self):
        """Verify ansible.cfg configuration and playbooks structure."""
        ansible_cfg = self.repo_root / "ansible.cfg"
        self.assertTrue(ansible_cfg.is_file(), "ansible.cfg must exist at repository root")

        cfg_content = ansible_cfg.read_text(encoding="utf-8")
        self.assertIn("[defaults]", cfg_content, "ansible.cfg must contain [defaults] section")

        playbooks_dir = self.repo_root / "playbooks"
        self.assertTrue(playbooks_dir.is_dir(), "playbooks directory must exist")

        playbook_files = list(playbooks_dir.glob("*.yml")) + list(playbooks_dir.glob("*.yaml"))
        self.assertGreater(len(playbook_files), 0, "playbooks directory must contain YAML files")

        for pb_file in playbook_files:
            with self.subTest(playbook=pb_file.name):
                content = pb_file.read_text(encoding="utf-8")
                parsed = yaml.safe_load(content)
                self.assertIsInstance(parsed, list, f"{pb_file.name} must be a YAML list of plays")
                for play in parsed:
                    self.assertIsInstance(play, dict, f"Each play in {pb_file.name} must be a dict")
                    self.assertIn("hosts", play, f"Play in {pb_file.name} must specify 'hosts'")
                    has_execution = any(k in play for k in ("tasks", "roles", "import_tasks", "include_tasks"))
                    self.assertTrue(
                        has_execution,
                        f"Play in {pb_file.name} must specify tasks or roles",
                    )


if __name__ == "__main__":
    unittest.main()
