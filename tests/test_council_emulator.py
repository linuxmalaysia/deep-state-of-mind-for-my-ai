"""
Unit tests for the Native Python Council Emulator (tools/council_emulator.py).

Verifies that:
1. `get_timestamp()` produces valid ISO 8601 UTC timestamp strings.
2. `evaluate_topic()` produces structured persona evaluations across all modes ('quick', 'full', 'duo', 'triad') and raises ValueError for invalid mode.
3. `generate_cdr()` formats valid OKF v0.2 frontmatter YAML and Markdown sections.
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

import council_emulator  # type: ignore


class CouncilEmulatorCachingTests(unittest.TestCase):
    """Test caching behaviour for evaluate_topic, generate_cdr, and slugify."""

    def setUp(self):
        council_emulator.clear_cache()

    def tearDown(self):
        council_emulator.clear_cache()

    def test_evaluate_topic_caching_returns_consistent_results(self):
        topic = "Zero Trust Token Revocation Architecture"
        res1 = council_emulator.evaluate_topic(topic, mode="quick")
        res2 = council_emulator.evaluate_topic(topic, mode="quick")

        self.assertEqual(res1, res2)
        info = council_emulator.get_cache_info()["evaluate_topic"]
        self.assertEqual(info["hits"], 1)
        self.assertEqual(info["misses"], 1)

    def test_evaluate_topic_defensive_copy_protects_cache(self):
        topic = "Defensive Mutation Isolation Test"
        res1 = council_emulator.evaluate_topic(topic, mode="duo")
        # Mutate the returned dictionary in-place
        res1["perspectives"]["Systems Architect"]["title"] = "Corrupted Architect Title"
        res1["verdict"]["action_plan"].append("Corrupted Step 99")

        # Second call should return pristine cached structure without caller mutation
        res2 = council_emulator.evaluate_topic(topic, mode="duo")
        self.assertNotEqual(
            res2["perspectives"]["Systems Architect"]["title"],
            "Corrupted Architect Title",
        )
        self.assertEqual(
            res2["perspectives"]["Systems Architect"]["title"],
            "Senior Systems Architect",
        )
        self.assertNotIn("Corrupted Step 99", res2["verdict"]["action_plan"])

    def test_clear_cache_resets_cache_statistics(self):
        council_emulator.evaluate_topic("Patroni High Availability", mode="full")
        council_emulator.evaluate_topic("Patroni High Availability", mode="full")
        info_before = council_emulator.get_cache_info()["evaluate_topic"]
        self.assertGreater(info_before["hits"], 0)

        council_emulator.clear_cache()
        info_after = council_emulator.get_cache_info()["evaluate_topic"]
        self.assertEqual(info_after["hits"], 0)
        self.assertEqual(info_after["misses"], 0)
        self.assertEqual(info_after["currsize"], 0)

    def test_generate_cdr_caches_yaml_frontmatter(self):
        topic = "Frontmatter YAML Serialization Caching Test"
        eval_dict = council_emulator.evaluate_topic(topic)
        ts = "2026-09-19T10:00:00Z"

        cdr1 = council_emulator.generate_cdr(topic, eval_dict, timestamp=ts)
        cdr2 = council_emulator.generate_cdr(topic, eval_dict, timestamp=ts)

        self.assertEqual(cdr1, cdr2)
        yaml_info = council_emulator.get_cache_info()["yaml_frontmatter"]
        self.assertEqual(yaml_info["hits"], 1)
        self.assertEqual(yaml_info["misses"], 1)

    def test_slugify_caching(self):
        text = "Batch Evaluation Performance Testing!"
        slug1 = council_emulator._slugify(text)
        slug2 = council_emulator._slugify(text)
        self.assertEqual(slug1, slug2)
        slug_info = council_emulator.get_cache_info()["slugify"]
        self.assertEqual(slug_info["hits"], 1)


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
        self.assertIn("Systems Architect", res["perspectives"])
        self.assertIn("Chief Security Officer", res["perspectives"])
        self.assertIn("Sovereign FOSS Architect", res["perspectives"])

    def test_evaluate_topic_custom_public_sector_tech_triad_without_keyword(self):
        res = council_emulator.evaluate_topic("Digital Services Portal", mode="triad", triad="public-sector-tech")
        self.assertEqual(res["triad"], "public-sector-tech")
        self.assertEqual(len(res["perspectives"]), 3)
        self.assertIn("Domain Specialist", res["perspectives"])
        self.assertEqual(res["perspectives"]["Domain Specialist"]["title"], "Risk & Compliance Officer")

    def test_evaluate_topic_triad_precedence_over_conflicting_topic_keyword(self):
        # Explicit triad 'public-sector-tech' must take precedence over 'authentication' keyword in topic
        res = council_emulator.evaluate_topic("Statutory User Authentication Subsystem", mode="triad", triad="public-sector-tech")
        self.assertEqual(res["triad"], "public-sector-tech")
        self.assertEqual(len(res["perspectives"]), 3)
        self.assertIn("Domain Specialist", res["perspectives"])
        self.assertEqual(res["perspectives"]["Domain Specialist"]["title"], "Risk & Compliance Officer")

    def test_evaluate_topic_custom_sovereignty_triad(self):
        res = council_emulator.evaluate_topic("On-Prem Self-Hosted LLM", mode="triad", triad="sovereignty")
        self.assertEqual(res["mode"], "triad")
        self.assertEqual(res["triad"], "sovereignty")
        self.assertEqual(len(res["perspectives"]), 3)
        self.assertIn("Sovereign FOSS Architect", res["perspectives"])
        self.assertIn("Harisfazillah Jamel", res["perspectives"]["Sovereign FOSS Architect"]["title"])

    def test_evaluate_topic_custom_enterprise_infrastructure_triad(self):
        res = council_emulator.evaluate_topic("PostgreSQL Patroni Cluster", mode="triad", triad="enterprise-infrastructure")
        self.assertEqual(res["triad"], "enterprise-infrastructure")
        self.assertEqual(len(res["perspectives"]), 3)
        self.assertIn("Sovereign FOSS Architect", res["perspectives"])
        self.assertIn("Systems Architect", res["perspectives"])
        self.assertIn("Pragmatic Engineer", res["perspectives"])

    def test_evaluate_topic_custom_public_sector_tech_triad(self):
        res = council_emulator.evaluate_topic("Statutory Compliance Platform", mode="triad", triad="public-sector-tech")
        self.assertEqual(res["triad"], "public-sector-tech")
        self.assertEqual(len(res["perspectives"]), 3)
        self.assertIn("Sovereign FOSS Architect", res["perspectives"])
        self.assertIn("Chief Security Officer", res["perspectives"])
        self.assertIn("Domain Specialist", res["perspectives"])

    def test_evaluate_topic_full_mode_includes_harisfazillah(self):
        res = council_emulator.evaluate_topic("Cloud Exit & Data Sovereignty Strategy", mode="full")
        self.assertEqual(res["mode"], "full")
        self.assertEqual(len(res["perspectives"]), 5)
        self.assertIn("Sovereign FOSS Architect", res["perspectives"])

    def test_evaluate_topic_invalid_mode_raises_value_error(self):
        with self.assertRaises(ValueError) as cm:
            council_emulator.evaluate_topic("Invalid Mode Test", mode="unsupported_mode")
        self.assertIn("Invalid mode 'unsupported_mode'", str(cm.exception))

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
        parts = cdr_md.split("---", 2)
        self.assertEqual(len(parts), 3)

        meta = yaml.safe_load(parts[1])
        self.assertEqual(meta["okf_version"], "0.2")
        self.assertEqual(meta["type"], "documentation")
        self.assertEqual(meta["title"], f"Council Decision Record: {topic}")
        self.assertEqual(meta["timestamp"], "2026-09-19T12:00:00Z")
        self.assertEqual(meta["spec_version"], "0.2")

        body = parts[2]
        self.assertIn("# Council Decision Record (CDR): Adopting FastMCP Server", body)
        self.assertIn("## 1. Executive Summary", body)
        self.assertIn("## 2. Persona Perspectives Matrix", body)
        self.assertIn("## 3. Deliberation & Trade-off Debate", body)
        self.assertIn("## 4. Final Council Verdict & Action Plan", body)

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

    def test_cli_output_flag_empty_value_generates_slug_path(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            fake_dest = pathlib.Path(tmpdir) / "docs" / "decisions" / "cdr-ci-workflow-hardening.md"
            with mock.patch.object(council_emulator, "REPO_ROOT", pathlib.Path(tmpdir)):
                with mock.patch.object(council_emulator, "DECISIONS_DIR", pathlib.Path(tmpdir) / "docs" / "decisions"):
                    with mock.patch("sys.argv", ["council_emulator.py", "--topic", "CI Workflow Hardening", "-o"]):
                        with contextlib.redirect_stdout(io.StringIO()):
                            council_emulator.main()
            self.assertTrue(fake_dest.is_file())

    def test_cli_search_argument(self):
        with mock.patch("sys.argv", ["council_emulator.py", "--search", "nonexistent_query_xyz"]):
            with contextlib.redirect_stderr(io.StringIO()) as stderr:
                council_emulator.main()
            output = stderr.getvalue()
            self.assertIn("No Council Decision Records matched query", output)


if __name__ == "__main__":
    unittest.main()
