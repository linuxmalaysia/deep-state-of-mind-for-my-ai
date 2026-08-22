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
    parse_okf_frontmatter,
    build_mintlify_tree,
)


class TestMintlifyMdxBuilder(unittest.TestCase):
    def test_parse_okf_frontmatter(self):
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
        title, desc, body = parse_okf_frontmatter(doc)
        self.assertEqual(title, "Custom Protocol")
        self.assertEqual(desc, "A sovereign description.")
        self.assertIn("This is body content.", body)

    def test_convert_markdown_to_mdx(self):
        doc = """---
okf_version: "0.2"
title: "Sample Guide"
description: "Sample description."
---

# Sample Guide

Content paragraph.
"""
        mdx = convert_markdown_to_mdx(doc)
        self.assertIn('title: "Sample Guide"', mdx)
        self.assertIn('description: "Sample description."', mdx)
        self.assertIn("Content paragraph.", mdx)

    def test_build_mintlify_tree_end_to_end(self):
        temp_dir = tempfile.mkdtemp(prefix="test_mdx_tree_")
        try:
            repo_root = Path(temp_dir)
            docs_dir = repo_root / "docs"
            agents_dir = repo_root / ".agents" / "skills" / "demo-skill"
            target_dir = repo_root / "docs-source"

            docs_dir.mkdir(parents=True, exist_ok=True)
            agents_dir.mkdir(parents=True, exist_ok=True)

            (docs_dir / "README.md").write_text("---\ntitle: \"Readme\"\n---\n# Readme\n", encoding="utf-8")
            (docs_dir / "START-HERE.md").write_text("---\ntitle: \"Start\"\n---\n# Start\n", encoding="utf-8")
            (docs_dir / "SECURITY.md").write_text("---\ntitle: \"Security\"\n---\n# Security\n", encoding="utf-8")
            (docs_dir / "LEGAL-NOTICE.md").write_text("---\ntitle: \"Legal\"\n---\n# Legal\n", encoding="utf-8")
            (docs_dir / "SOD-RITUAL.md").write_text("---\ntitle: \"SOD\"\n---\n# SOD\n", encoding="utf-8")
            (docs_dir / "EOD-RITUAL.md").write_text("---\ntitle: \"EOD\"\n---\n# EOD\n", encoding="utf-8")
            (docs_dir / "RITUAL-OF-TRANSITION.md").write_text("---\ntitle: \"Transition\"\n---\n# Transition\n", encoding="utf-8")
            (docs_dir / "HUMAN-HANDOVER-CONTEXT.md").write_text("---\ntitle: \"Handover\"\n---\n# Handover\n", encoding="utf-8")
            (agents_dir / "SKILL.md").write_text("---\ntitle: \"Demo Skill\"\n---\n# Demo Skill\n", encoding="utf-8")

            build_mintlify_tree(repo_root, target_dir)

            docs_json = target_dir / "docs.json"
            self.assertTrue(docs_json.exists())
            with open(docs_json, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.assertEqual(data["name"], "DSOM — Deep State of Mind")
            self.assertTrue(len(data["navigation"]["tabs"]) > 0)
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
