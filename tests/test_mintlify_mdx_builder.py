"""
Unit tests for tools/build_mintlify_mdx.py (Mintlify MDX Tree Builder).
"""

import json
import os
import shutil
import tempfile
import unittest
from pathlib import Path

from tools.build_mintlify_mdx import (
    convert_markdown_to_mdx,
    parse_frontmatter_and_content,
    to_title_case_sidebar,
    build_mintlify_tree,
)


class TestMintlifyMdxBuilder(unittest.TestCase):
    def test_parse_frontmatter_and_content(self):
        doc = """---
okf_version: "0.2"
type: "guide"
title: "Custom Protocol"
description: "A sovereign description."
topics: ["ai", "governance"]
---

# Custom Protocol

This is body content.
"""
        title, sidebar, desc, body = parse_frontmatter_and_content(doc)
        self.assertEqual(title, "Custom Protocol")
        self.assertEqual(sidebar, "Custom")
        self.assertTrue(130 <= len(desc) <= 155)
        self.assertIn("This is body content.", body)

    def test_to_title_case_sidebar(self):
        self.assertEqual(to_title_case_sidebar("The DSOM Architecture Protocol Guide"), "Architecture")
        self.assertEqual(to_title_case_sidebar("SOP Knowledge First Discovery"), "Sop Knowledge First")

    def test_convert_markdown_to_mdx(self):
        doc = """---
okf_version: "0.2"
title: "Sample Guide"
description: "Sample description for testing MDX conversion."
---

# Sample Guide

Content paragraph with a [link](docs/guide.md) and an image [pic](../images/icon.png).
"""
        mdx = convert_markdown_to_mdx(doc)
        self.assertIn('title: "Sample Guide"', mdx)
        self.assertIn('sidebarTitle: "Sample"', mdx)
        self.assertIn('[link](docs/guide)', mdx)
        self.assertIn('[pic](/images/icon.png)', mdx)

    def test_build_mintlify_tree_and_idempotency(self):
        temp_dir = tempfile.mkdtemp(prefix="test_mdx_tree_")
        try:
            repo_root = Path(temp_dir)
            docs_dir = repo_root / "docs"
            agents_dir = repo_root / ".agents" / "skills" / "demo-skill"
            target_dir = repo_root / "docs-source"

            docs_dir.mkdir(parents=True, exist_ok=True)
            agents_dir.mkdir(parents=True, exist_ok=True)

            (docs_dir / "README.md").write_text('---\ntitle: "Readme"\n---\n# Readme\n', encoding="utf-8")
            (docs_dir / "START-HERE.md").write_text('---\ntitle: "Start"\n---\n# Start\n', encoding="utf-8")
            (docs_dir / "SECURITY.md").write_text('---\ntitle: "Security"\n---\n# Security\n', encoding="utf-8")
            (docs_dir / "LEGAL-NOTICE.md").write_text('---\ntitle: "Legal"\n---\n# Legal\n', encoding="utf-8")
            (docs_dir / "SOD-RITUAL.md").write_text('---\ntitle: "SOD"\n---\n# SOD\n', encoding="utf-8")
            (docs_dir / "EOD-RITUAL.md").write_text('---\ntitle: "EOD"\n---\n# EOD\n', encoding="utf-8")
            (docs_dir / "RITUAL-OF-TRANSITION.md").write_text('---\ntitle: "Transition"\n---\n# Transition\n', encoding="utf-8")
            (docs_dir / "HUMAN-HANDOVER-CONTEXT.md").write_text('---\ntitle: "Handover"\n---\n# Handover\n', encoding="utf-8")
            (agents_dir / "SKILL.md").write_text('---\ntitle: "Demo Skill"\n---\n# Demo Skill\n', encoding="utf-8")

            # Run 1
            build_mintlify_tree(repo_root, target_dir)
            docs_json = target_dir / "docs.json"
            self.assertTrue(docs_json.exists())
            with open(docs_json, "r", encoding="utf-8") as f:
                data1 = json.load(f)
            self.assertIn("tabs", data1["navigation"])

            # Verify navigation integrity in generated docs.json
            for tab in data1["navigation"]["tabs"]:
                for grp in tab["groups"]:
                    for page in grp["pages"]:
                        page_file = target_dir / f"{page}.mdx"
                        self.assertTrue(page_file.exists(), f"Missing referenced page: {page_file}")

            # Run 2 (Idempotency)
            build_mintlify_tree(repo_root, target_dir)
            with open(docs_json, "r", encoding="utf-8") as f:
                data2 = json.load(f)
            self.assertEqual(data1, data2)
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
