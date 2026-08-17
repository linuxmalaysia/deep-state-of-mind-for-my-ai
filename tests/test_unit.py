"""
Top-level unit test suite for DSOM framework components.

Imports and re-exports modular unit tests from tests.unit package.
"""
import unittest

from tests.unit.ansible import TestAnsibleCompliance
from tests.unit.containers import TestContainerfileSecurity
from tests.unit.llms import TestLlmsTxtParser
from tests.unit.markdown import TestMarkdownCompliance
from tests.unit.sitemaps import TestSitemapsAndContext7

__all__ = [
    "TestAnsibleCompliance",
    "TestContainerfileSecurity",
    "TestLlmsTxtParser",
    "TestMarkdownCompliance",
    "TestSitemapsAndContext7",
]

if __name__ == "__main__":
    unittest.main()
