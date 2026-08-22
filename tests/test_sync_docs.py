"""
Unit and integration tests for scripts/sync_docs.py (Mintlify Safety Guards A-E).
"""

import json
import os
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts.sync_docs import (
    extract_pages_from_nav,
    guard_a_source_exists,
    guard_b_minimum_files,
    guard_c_navigation_integrity,
    guard_d_compute_diff,
)


class TestMintlifyDocsSync(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp(prefix="test_sync_")
        self.source_dir = Path(self.temp_dir) / "docs-source"
        self.target_dir = Path(self.temp_dir) / "docs_target"
        self.source_dir.mkdir(parents=True, exist_ok=True)
        self.target_dir.mkdir(parents=True, exist_ok=True)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_extract_pages_from_nav(self):
        nav = {
            "tabs": [
                {
                    "tab": "Doc",
                    "groups": [
                        {"group": "G1", "pages": ["intro", "quickstart"]},
                        {"group": "G2", "pages": ["tools/overview", {"group": "Nested", "pages": ["nested/page"]}]}
                    ]
                }
            ]
        }
        pages = extract_pages_from_nav(nav)
        self.assertEqual(pages, ["intro", "quickstart", "tools/overview", "nested/page"])

    def test_guard_a_source_exists(self):
        docs_json = self.source_dir / "docs.json"
        with open(docs_json, "w", encoding="utf-8") as f:
            json.dump({"name": "Test Docs", "navigation": {}}, f)

        data = guard_a_source_exists(self.source_dir)
        self.assertEqual(data["name"], "Test Docs")

    def test_guard_b_minimum_files(self):
        for i in range(6):
            (self.source_dir / f"page_{i}.mdx").write_text(f"# Page {i}", encoding="utf-8")

        mdx_files = guard_b_minimum_files(self.source_dir, min_floor=5)
        self.assertEqual(len(mdx_files), 6)

    def test_guard_c_navigation_integrity(self):
        nav_data = {
            "navigation": {
                "groups": [
                    {"group": "Main", "pages": ["intro", "guide"]}
                ]
            }
        }
        (self.source_dir / "intro.mdx").write_text("# Intro", encoding="utf-8")
        (self.source_dir / "guide.mdx").write_text("# Guide", encoding="utf-8")
        (self.source_dir / "orphan.mdx").write_text("# Orphan", encoding="utf-8")

        mdx_files = list(self.source_dir.glob("*.mdx"))
        # Should pass without exception even with orphan present
        guard_c_navigation_integrity(self.source_dir, nav_data, mdx_files)

    def test_guard_d_diff_and_deletion_cap(self):
        (self.source_dir / "file1.mdx").write_text("v1", encoding="utf-8")
        (self.source_dir / "file2.mdx").write_text("v1", encoding="utf-8")

        (self.target_dir / "file1.mdx").write_text("v0", encoding="utf-8")
        (self.target_dir / "file_old.mdx").write_text("old", encoding="utf-8")

        added, modified, deleted = guard_d_compute_diff(
            self.source_dir, self.target_dir, max_deletions=5, allow_large_deletions=False
        )

        self.assertIn("file2.mdx", added)
        self.assertIn("file1.mdx", modified)
        self.assertIn("file_old.mdx", deleted)


if __name__ == "__main__":
    unittest.main()
