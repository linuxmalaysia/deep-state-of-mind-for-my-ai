"""
Ansible playbook compliance unit tests.
"""
import pathlib
import unittest
import sys
import tempfile
import unittest
from unittest import mock

import yaml

def _find_repo_root(start: pathlib.Path) -> pathlib.Path:
    current = start.resolve()
    for parent in [current, *current.parents]:
        if (parent / ".git").exists():
            return parent
    raise RuntimeError("Could not locate repository root (.git not found)")

REPO_ROOT = _find_repo_root(pathlib.Path(__file__).parent)


class TestAnsibleCompliance(unittest.TestCase):
    """Ansible playbook and configuration compliance tests."""

    def test_ansible_playbook_compliance(self):
        """Verify ansible.cfg configuration and playbooks structure."""
        ansible_cfg = REPO_ROOT / "ansible.cfg"
        self.assertTrue(ansible_cfg.is_file(), "ansible.cfg must exist at repository root")

        cfg_content = ansible_cfg.read_text(encoding="utf-8")
        self.assertIn("[defaults]", cfg_content, "ansible.cfg must contain [defaults] section")

        playbooks_dir = REPO_ROOT / "playbooks"
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

    def test_find_repo_root_locates_git_directory_from_nested_path(self):
        """_find_repo_root must walk up from a deeply nested path to the .git root."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_root = pathlib.Path(tmpdir).resolve()
            (tmp_root / ".git").mkdir()
            nested = tmp_root / "a" / "b" / "c"
            nested.mkdir(parents=True)
            self.assertEqual(_find_repo_root(nested), tmp_root)

    def test_find_repo_root_raises_without_git_ancestor(self):
        """_find_repo_root must raise RuntimeError when no ancestor has a .git directory."""
        with tempfile.TemporaryDirectory() as tmpdir:
            nested = pathlib.Path(tmpdir) / "isolated"
            nested.mkdir()
            with self.assertRaises(RuntimeError):
                _find_repo_root(nested)

    def test_repo_root_resolves_to_actual_git_directory(self):
        """The module-level REPO_ROOT constant must point at a real .git checkout."""
        self.assertTrue((REPO_ROOT / ".git").exists())

    def test_playbook_validation_rejects_missing_ansible_cfg(self):
        """Compliance check must fail loudly when ansible.cfg is absent."""
        module = sys.modules[__name__]
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_root = pathlib.Path(tmpdir)
            with mock.patch.object(module, "REPO_ROOT", tmp_root):
                with self.assertRaises(AssertionError):
                    self.test_ansible_playbook_compliance()

    def _run_compliance_test_and_get_result(self):
        """Run test_ansible_playbook_compliance in an isolated suite/result.

        The production test wraps its per-playbook assertions in
        ``self.subTest(...)``, which *deliberately* swallows individual
        assertion failures so that ``assertRaises(AssertionError)`` around a
        direct method call would never observe them. Running the method
        through a real TestSuite/TestResult surfaces those failures instead.
        """
        suite = unittest.TestSuite()
        suite.addTest(self.__class__("test_ansible_playbook_compliance"))
        result = unittest.TestResult()
        suite.run(result)
        return result

    def test_playbook_validation_rejects_play_missing_hosts(self):
        """A play lacking a 'hosts' key must fail the compliance assertion."""
        module = sys.modules[__name__]
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_root = pathlib.Path(tmpdir)
            (tmp_root / "ansible.cfg").write_text("[defaults]\n", encoding="utf-8")
            playbooks_dir = tmp_root / "playbooks"
            playbooks_dir.mkdir()
            (playbooks_dir / "bad.yml").write_text(
                "- tasks:\n    - name: noop\n      debug:\n        msg: hi\n",
                encoding="utf-8",
            )
            with mock.patch.object(module, "REPO_ROOT", tmp_root):
                result = self._run_compliance_test_and_get_result()
            self.assertFalse(result.wasSuccessful())

    def test_playbook_validation_rejects_play_without_tasks_or_roles(self):
        """A play with 'hosts' but no tasks/roles/import_tasks/include_tasks must fail."""
        module = sys.modules[__name__]
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_root = pathlib.Path(tmpdir)
            (tmp_root / "ansible.cfg").write_text("[defaults]\n", encoding="utf-8")
            playbooks_dir = tmp_root / "playbooks"
            playbooks_dir.mkdir()
            (playbooks_dir / "bad.yml").write_text("- hosts: all\n", encoding="utf-8")
            with mock.patch.object(module, "REPO_ROOT", tmp_root):
                result = self._run_compliance_test_and_get_result()
            self.assertFalse(result.wasSuccessful())

    def test_playbook_validation_accepts_roles_only_play(self):
        """A minimal, well-formed playbook using only 'roles' must pass cleanly."""
        module = sys.modules[__name__]
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_root = pathlib.Path(tmpdir)
            (tmp_root / "ansible.cfg").write_text("[defaults]\n", encoding="utf-8")
            playbooks_dir = tmp_root / "playbooks"
            playbooks_dir.mkdir()
            (playbooks_dir / "good.yml").write_text(
                "- hosts: all\n  roles:\n    - common\n",
                encoding="utf-8",
            )
            with mock.patch.object(module, "REPO_ROOT", tmp_root):
                self.test_ansible_playbook_compliance()  # must not raise

    def test_playbook_validation_rejects_non_list_yaml_document(self):
        """A playbook whose top-level YAML document is a mapping, not a list, must fail."""
        module = sys.modules[__name__]
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_root = pathlib.Path(tmpdir)
            (tmp_root / "ansible.cfg").write_text("[defaults]\n", encoding="utf-8")
            playbooks_dir = tmp_root / "playbooks"
            playbooks_dir.mkdir()
            (playbooks_dir / "bad.yml").write_text("hosts: all\ntasks: []\n", encoding="utf-8")
            with mock.patch.object(module, "REPO_ROOT", tmp_root):
                result = self._run_compliance_test_and_get_result()
            self.assertFalse(result.wasSuccessful())


if __name__ == "__main__":
    unittest.main()
