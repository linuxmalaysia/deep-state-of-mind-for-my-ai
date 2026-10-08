# ==============================================================================
# Protocol    : Deep State of Mind (DSOM) For My AI
# Author      : Harisfazillah Jamel (LinuxMalaysia)
# Timestamp   : 2026-10-08
# License     : GNU General Public License v3.0
# Standard    : UK English | DBP-standard Bahasa Melayu Malaysia (Piawai)
# ==============================================================================
"""Check install playbook expressions without invoking Lola or changing the host.

Jinja2 is supplied by the ansible-core dependency used in documentation CI.
"""

import unittest
from pathlib import Path

import yaml
from jinja2 import Environment, StrictUndefined


class LolaPlaybookTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = Path(__file__).resolve().parents[1] / "playbooks" / "install.yml"
        cls.play = yaml.safe_load(path.read_text(encoding="utf-8"))[0]
        cls.tasks = cls.play["tasks"]
        cls.probe = next(task for task in cls.tasks if task.get("register") == "lola_check")
        cls.sync = next(task for task in cls.tasks if task.get("register") == "lola_sync_output")
        cls.report = next(task for task in cls.tasks if "ansible.builtin.debug" in task)
        cls.environment = Environment(undefined=StrictUndefined)

    def test_install_runs_locally_without_fact_gathering(self):
        self.assertEqual(self.play["hosts"], "localhost")
        self.assertEqual(self.play["connection"], "local")
        self.assertIs(self.play["gather_facts"], False)

    def test_missing_cli_probe_is_nonfatal_and_never_reports_changes(self):
        self.assertEqual(self.probe["ansible.builtin.command"], "which lola")
        self.assertIs(self.probe["changed_when"], False)
        self.assertIs(self.probe["failed_when"], False)
        self.assertLess(self.tasks.index(self.probe), self.tasks.index(self.sync))

    def test_sync_runs_only_when_cli_probe_succeeds(self):
        expression = self.environment.compile_expression(self.sync["when"])
        for rc, expected in ((0, True), (1, False), (127, False)):
            with self.subTest(rc=rc):
                self.assertIs(expression(lola_check={"rc": rc}), expected)

    def test_sync_uses_repository_manifest_from_playbook_parent(self):
        self.assertEqual(self.sync["ansible.builtin.command"], "lola sync")
        template = self.environment.from_string(self.sync["args"]["chdir"])
        root = Path(__file__).resolve().parents[1]
        directory = Path(template.render(playbook_dir=str(root / "playbooks"))).resolve()
        self.assertEqual(directory, root)
        self.assertTrue((directory / ".lola-req").is_file())
        self.assertIs(self.sync["failed_when"], False)

    def test_sync_reports_changes_only_for_successful_install_or_sync(self):
        expression = self.environment.compile_expression(self.sync["changed_when"])
        cases = (
            (0, "Synchronized 46 packages", True),
            (0, "Installed example", True),
            (0, "Already up to date", False),
            (0, "", False),
            (1, "Installed example before an error", False),
            (127, "Synchronized", False),
        )
        for rc, stdout, expected in cases:
            with self.subTest(rc=rc, stdout=stdout):
                self.assertIs(expression(lola_sync_output={"rc": rc, "stdout": stdout}), expected)

    def render_status(self, **context):
        return self.environment.from_string(self.report["ansible.builtin.debug"]["msg"]).render(**context)

    def test_successful_sync_reports_success(self):
        message = self.render_status(lola_check={"rc": 0}, lola_sync_output={"rc": 0})
        self.assertIn("successfully", message)
        self.assertNotIn("Falling back", message)

    def test_sync_error_reports_exit_code_and_local_fallback(self):
        for rc in (1, 127):
            with self.subTest(rc=rc):
                message = self.render_status(lola_check={"rc": 0}, lola_sync_output={"rc": rc})
                self.assertIn(f"exit code {rc}", message)
                self.assertIn("Falling back to local vendored skills in .agents/skills/", message)
                self.assertNotIn("successfully", message)

    def test_missing_cli_handles_undefined_and_skipped_sync_results(self):
        for result in ({}, {"lola_sync_output": {"skipped": True}}):
            with self.subTest(result=result):
                message = self.render_status(lola_check={"rc": 1}, **result)
                self.assertIn("Using local vendored skills in .agents/skills/", message)
                self.assertNotIn("successfully", message)

    def test_available_cli_with_no_sync_result_uses_local_fallback(self):
        message = self.render_status(lola_check={"rc": 0})
        self.assertIn("Using local vendored skills in .agents/skills/", message)


if __name__ == "__main__":
    unittest.main()
