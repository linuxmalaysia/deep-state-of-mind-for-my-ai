import os
import sys
import tempfile
import unittest
import yaml

# Add repo root to PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from tools.apply_okf_frontmatter import process_file

class TestOkfMultipleFrontmatterRegression(unittest.TestCase):
    def setUp(self):
        # Create a temporary file
        self.fd, self.path = tempfile.mkstemp(suffix=".md")
        os.close(self.fd)

    def tearDown(self):
        # Clean up the temporary file
        if os.path.exists(self.path):
            os.remove(self.path)

    def test_consecutive_frontmatter_blocks(self):
        # Write content with consecutive frontmatter blocks
        input_content = """---
okf_version: 0.1
type: documentation
title: "First Block"
---
---
okf_version: 0.1
type: documentation
title: "Second Block"
topics: [testing, regression]
---
# Document Title

This is the body content.
"""
        with open(self.path, "w", encoding="utf-8") as f:
            f.write(input_content)

        # Run process_file once (first run)
        temp_dir = os.path.dirname(self.path)
        modified1 = process_file(self.path, temp_dir)
        self.assertTrue(modified1)

        # Read back content after first run
        with open(self.path, "r", encoding="utf-8") as f:
            content1 = f.read()

        # Check that exactly one frontmatter block remains and parses correctly
        # Split by "---" should yield exactly 3 parts
        parts = content1.split("---")
        self.assertEqual(len(parts), 3, f"Expected exactly one frontmatter block, got: {content1}")

        frontmatter = yaml.safe_load(parts[1])
        self.assertEqual(frontmatter.get("okf_version"), 0.1)
        self.assertEqual(frontmatter.get("type"), "documentation")
        self.assertEqual(frontmatter.get("title"), "Second Block") # Second block takes precedence in updates
        self.assertEqual(frontmatter.get("topics"), ["testing", "regression"])

        # Run process_file a second time (second run)
        modified2 = process_file(self.path, temp_dir)
        self.assertFalse(modified2, "File should not be modified on a second run when it's already compliant")

        # Verify the content remains exactly unchanged
        with open(self.path, "r", encoding="utf-8") as f:
            content2 = f.read()
        self.assertEqual(content1, content2, "Content changed unexpectedly on second run")

if __name__ == "__main__":
    unittest.main()
