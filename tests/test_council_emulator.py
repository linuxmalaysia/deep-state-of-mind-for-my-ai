"""
Unit tests for the Native Python Council Emulator (tools/council_emulator.py).

Verifies that:
1. `get_timestamp()` produces valid ISO 8601 UTC timestamp strings.
2. `evaluate_topic()` produces structured persona evaluations across all modes ('quick', 'full', 'duo', 'triad').
3. `generate_cdr()` formats valid OKF v0.2 frontmatter and Markdown sections.
4. `run_council()` executes deliberation and optionally writes CDR artifacts to disk.
5. `cmd_search()` queries Council Decision Record documents.
6. CLI `main()` parses arguments cleanly via argparse.
"""

import contextlib
import io
import pathlib
import sys
import tempfile
import unittest
from unittest import mock

import yaml

# Ensure tools/ is on Python path
REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "tools"))

import council_emulator  # type: ignore # noqa: E402


class CouncilEmulatorTimestampTests(unittest.TestCase):
    """Test timestamp utility formatting."""

    def test_get_timestamp_format(self):
        ts = council_emulator.get_timestamp()
        self.assertTrue(ts.endswith("Z"))
        self.assertIn("T", ts)


class EvaluateTopicTests(unittest.TestCase):
    """Test multi-perspective evaluation logic across modes."""

    def test_evaluate_topic_quick_mode(self):
        res = council_emulator.evaluate_topic("Database Migration to PostgreSQL", mode="quick")
        self.assertEqual(res["topic"], "Database Migration to PostgreSQL")
        self.assertEqual(res["mode"], "quick")
        self.assertEqual(len(res["perspectives"]), 4)
        self.assertIn("Systems Architect", res["perspectives"])
        self.assertIn("Chief Security Officer", res["perspectives"])
        self.assertIn("Pragmatic Engineer", res["perspectives"])
        self.assertIn("Domain Specialist", res["perspectives"])

    def test_evaluate_topic_duo_mode(self):
        res = council_emulator.evaluate_topic("Microservices vs Monolith", mode="duo")
        self.assertEqual(res["mode"], "duo")
        self.assertEqual(len(res["perspectives"]), 2)
        self.assertIn("Systems Architect", res["perspectives"])
        self.assertIn("Chief Security Officer", res["perspectives"])

    def test_evaluate_topic_triad_mode(self):
        res = council_emulator.evaluate_topic("Zero Trust Auth Pipeline", mode="triad", triad="security")
        self.assertEqual(res["mode"], "triad")
        self.assertEqual(res["triad"], "security")
        self.assertEqual(len(res["perspectives"]), 3)
        self.assertEqual(res["perspectives"]["Domain Specialist"]["title"], "Cybersecurity Specialist")

    def test_evaluate_topic_includes_debate_and_verdict(self):
        res = council_emulator.evaluate_topic("FastMCP Tool Exposure", context="Production SLA required")
        self.assertTrue(len(res["debate_points"]) >= 3)
        self.assertTrue(any("[FACT]" in dp["tag"] for dp in res["debate_points"]))
        self.assertIn("summary", res["verdict"])
        self.assertIn("action_plan", res["verdict"])
        self.assertIn("kill_criteria", res["verdict"])


class GenerateCdrTests(unittest.TestCase):
    """Test OKF v0.2 CDR document generation."""

    def test_generate_cdr_frontmatter_and_sections(self):
        topic = "Adopting FastMCP Server"
        evaluation = council_emulator.evaluate_topic(topic)
        cdr_md = council_emulator.generate_cdr(topic, evaluation, timestamp="2026-09-19T12:00:00Z")

        self.assertTrue(cdr_md.startswith("---"))
        self.assertIn('okf_version: "0.2"', cdr_md)
        self.assertIn('type: "documentation"', cdr_md)
        self.assertIn(f'title: "Council Decision Record: {topic}"', cdr_md)
        self.assertIn("# Council Decision Record (CDR): Adopting FastMCP Server", cdr_md)
        self.assertIn("## 1. Executive Summary", cdr_md)
        self.assertIn("## 2. Persona Perspectives Matrix", cdr_md)
        self.assertIn("## 3. Deliberation & Trade-off Debate", cdr_md)
        self.assertIn("## 4. Final Council Verdict & Action Plan", cdr_md)

    def test_generate_cdr_frontmatter_valid_yaml(self):
        topic = "Quadlet Container Deployment"
        evaluation = council_emulator.evaluate_topic(topic)
        cdr_md = council_emulator.generate_cdr(topic, evaluation)

        parts = cdr_md.split("---", 2)
        self.assertEqual(len(parts), 3)
        meta = yaml.safe_load(parts[1])

        self.assertEqual(meta["okf_version"], "0.2")
        self.assertEqual(meta["type"], "documentation")
        self.assertEqual(meta["spec_version"], "0.2")
        self.assertIn("council", meta["topics"])


class RunCouncilTests(unittest.TestCase):
    """Test high-level run_council execution and file output."""

    def test_run_council_returns_string(self):
        cdr_md = council_emulator.run_council("Audit Logging Subsystem")
        self.assertIsInstance(cdr_md, str)
        self.assertIn("Council Decision Record", cdr_md)

    def test_run_council_writes_file_when_output_path_given(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            out_file = pathlib.Path(tmpdir) / "decisions" / "test_cdr.md"
            cdr_md = council_emulator.run_council("Ansible Automation Baseline", output_path=str(out_file))
            self.assertTrue(out_file.is_file())
            content = out_file.read_text(encoding="utf-8")
            self.assertEqual(content, cdr_md)


class CmdSearchTests(unittest.TestCase):
    """Test searching Council Decision Record files."""

    def test_cmd_search_finds_matching_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            search_dir = pathlib.Path(tmpdir)
            sample_cdr = """---
okf_version: "0.2"
title: "Council Decision Record: Patroni Cluster Setup"
description: "High availability PostgreSQL cluster deliberation"
---
# Patroni Cluster Setup
"""
            (search_dir / "cdr-patroni.md").write_text(sample_cdr, encoding="utf-8")

            results = council_emulator.cmd_search("patroni", search_dir=search_dir)
            self.assertEqual(len(results), 1)
            file_path, title, desc = results[0]
            self.assertEqual(title, "Council Decision Record: Patroni Cluster Setup")
            self.assertIn("High availability", desc)


class MainCliTests(unittest.TestCase):
    """Test CLI argument parsing and execution."""

    def test_cli_topic_argument(self):
        with mock.patch("sys.argv", ["council_emulator.py", "--topic", "CI Workflow Hardening"]):
            with contextlib.redirect_stdout(io.StringIO()) as stdout:
                council_emulator.main()
            output = stdout.getvalue()
            self.assertIn("Council Decision Record", output)
            self.assertIn("CI Workflow Hardening", output)

    def test_cli_search_argument(self):
        with mock.patch("sys.argv", ["council_emulator.py", "--search", "nonexistent_query_xyz"]):
            with contextlib.redirect_stdout(io.StringIO()) as stdout:
                council_emulator.main()
            output = stdout.getvalue()
            self.assertIn("No Council Decision Records matched query", output)


if __name__ == "__main__":
    unittest.main()
