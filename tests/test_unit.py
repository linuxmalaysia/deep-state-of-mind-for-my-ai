"""
Top-level unit test suite for DSOM framework components.

Imports and re-exports modular unit tests from tests.unit package.
"""
import unittest

import tests.unit as unit_package
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


class TestUnitSuiteExports(unittest.TestCase):
    """Verify tests/test_unit.py correctly aggregates tests.unit's test cases."""

    def test_all_matches_module_globals(self):
        current_module = globals()
        for name in __all__:
            self.assertIn(name, current_module, f"{name} listed in __all__ but not importable")

    def test_all_exported_names_are_testcase_subclasses(self):
        for name in __all__:
            obj = globals()[name]
            self.assertTrue(
                issubclass(obj, unittest.TestCase),
                f"{name} must be a unittest.TestCase subclass",
            )

    def test_reexports_are_identical_objects_from_unit_package(self):
        """tests/test_unit.py and tests/unit/__init__.py must expose the same
        class objects (not independent copies) for each name in __all__."""
        for name in __all__:
            with self.subTest(name=name):
                self.assertIs(globals()[name], getattr(unit_package, name))

    def test_unit_package_all_matches_test_unit_all(self):
        self.assertEqual(sorted(__all__), sorted(unit_package.__all__))

    def test_all_contains_no_duplicates(self):
        self.assertEqual(len(__all__), len(set(__all__)))


if __name__ == "__main__":
    unittest.main()
