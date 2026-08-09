"""
Unit tests for the Native Python OpenWiki Emulator (tools/openwiki_emulator.py).

Verifies that:
1. `get_timestamp()` produces valid ISO format timestamp strings.
2. `generate_skeleton()` returns valid OKF YAML frontmatter documentation.
3. `generate_last_update_json()` outputs valid JSON metrics.
"""
import json
import pathlib
import sys
import unittest

# Ensure tools/ is on Python path
REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "tools"))

import openwiki_emulator  # type: ignore # noqa: E402


class OpenWikiEmulatorTests(unittest.TestCase):
    """Test OpenWiki emulator generator functions."""

    def test_get_timestamp_format(self):
        ts = openwiki_emulator.get_timestamp()
        self.assertTrue(ts.endswith("Z"))
        self.assertIn("T", ts)

    def test_generate_skeleton_contains_okf_frontmatter(self):
        skeleton = openwiki_emulator.generate_skeleton()
        self.assertTrue(skeleton.startswith("---"))
        self.assertIn("title: \"OpenWiki Documentation Skeleton & Subsystem Index\"", skeleton)

    def test_generate_last_update_json_parses(self):
        json_str = openwiki_emulator.generate_last_update_json()
        data = json.loads(json_str)
        self.assertEqual(data["status"], "success")
        self.assertIn("updatedAt", data)


if __name__ == "__main__":
    unittest.main()
