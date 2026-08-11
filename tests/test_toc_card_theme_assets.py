"""
Unit tests for the "Dynamic Table of Contents (TOC) Card" front-end assets
added in this PR:

    - docs/stylesheets/extra.css  (new `.custom-toc-*` rule block)

These tests validate the *content* of the stylesheet using targeted
string/regex assertions, following the same convention used elsewhere in
this repository for verifying non-Python, declarative assets (see
tests/test_mkdocs_nav.py). The repository has no JavaScript/CSS test
runner, so behavioral coverage of the companion docs/javascripts/extra.js
logic lives in docs/javascripts/__tests__/extra.test.js (Jest + jsdom);
this file focuses solely on the static CSS contract that the JS code and
the rendered page depend on (selector names, key property values, and
overall rule-block integrity).
"""
import pathlib
import re
import unittest


def _find_repo_root(start: pathlib.Path) -> pathlib.Path:
    current = start.resolve()
    for parent in [current, *current.parents]:
        if (parent / ".git").exists():
            return parent
    raise RuntimeError("Could not locate repository root (.git not found)")


REPO_ROOT = _find_repo_root(pathlib.Path(__file__).parent)
CSS_PATH = REPO_ROOT / "docs" / "stylesheets" / "extra.css"


class TocCardStylesheetStructureTests(unittest.TestCase):
    """Basic file/section presence checks."""

    @classmethod
    def setUpClass(cls):
        cls.css_text = CSS_PATH.read_text(encoding="utf-8")

    def test_stylesheet_file_exists(self):
        self.assertTrue(CSS_PATH.is_file())

    def test_toc_design_system_section_header_present(self):
        self.assertIn(
            "Automated Dynamic Table of Contents (TOC) Card Design System",
            self.css_text,
        )

    def test_braces_are_balanced(self):
        # Regression guard: a malformed edit to the new rule block could
        # silently break every rule that follows it in the cascade.
        self.assertEqual(
            self.css_text.count("{"),
            self.css_text.count("}"),
            "Mismatched curly braces in extra.css",
        )

    def test_custom_toc_card_rule_defined_exactly_once(self):
        matches = re.findall(r"\.custom-toc-card\s*\{", self.css_text)
        self.assertEqual(
            len(matches),
            1,
            "Expected exactly one `.custom-toc-card { ... }` rule definition",
        )


class TocCardRuleBodyTests(unittest.TestCase):
    """Assertions about specific selectors and their declarations."""

    @classmethod
    def setUpClass(cls):
        cls.css_text = CSS_PATH.read_text(encoding="utf-8")

    def _rule_body(self, selector_pattern):
        """Return the declaration block text for the first rule whose
        selector matches `selector_pattern` (a regex, already escaped as
        needed by the caller), or fail the test if not found."""
        match = re.search(
            selector_pattern + r"\s*\{([^}]*)\}", self.css_text, re.DOTALL
        )
        self.assertIsNotNone(
            match, f"Could not find rule for selector pattern: {selector_pattern}"
        )
        return match.group(1)

    def test_toc_card_sticky_positioning_and_surface_styling(self):
        body = self._rule_body(r"\.custom-toc-card")
        self.assertIn("background: var(--lab-surface);", body)
        self.assertIn("border: 1px solid var(--lab-border);", body)
        self.assertIn("border-radius: var(--radius);", body)
        self.assertIn("position: sticky;", body)
        self.assertIn("top: var(--toc-sticky-top);", body)
        self.assertIn("max-height: calc(100vh - var(--toc-scroll-offset));", body)
        self.assertIn("overflow-y: auto;", body)
        self.assertIn("margin-bottom: 24px;", body)

    def test_toc_card_no_longer_hardcodes_sticky_offset_pixel_values(self):
        # Regression guard for the switch from hardcoded pixel values to the
        # centralised --toc-sticky-top / --toc-scroll-offset custom
        # properties: the raw magic numbers must not reappear in the rule.
        body = self._rule_body(r"\.custom-toc-card")
        self.assertNotIn("top: 90px;", body)
        self.assertNotIn("max-height: calc(100vh - 120px);", body)

    def test_toc_card_scrollbar_customizations(self):
        self.assertRegex(
            self.css_text,
            r"\.custom-toc-card::-webkit-scrollbar\s*\{\s*width:\s*4px;\s*\}",
        )
        thumb_body = self._rule_body(r"\.custom-toc-card::-webkit-scrollbar-thumb")
        self.assertIn("background: var(--lab-border);", thumb_body)
        self.assertIn("border-radius: 2px;", thumb_body)

    def test_toc_header_typography(self):
        body = self._rule_body(r"\.custom-toc-header")
        self.assertIn("text-transform: uppercase;", body)
        self.assertIn("font-weight: 700;", body)
        self.assertIn("border-bottom: 1px dashed var(--lab-border);", body)

    def test_toc_list_and_sublist_reset_default_list_styling(self):
        list_body = self._rule_body(r"\.custom-toc-list")
        self.assertIn("list-style: none !important;", list_body)
        self.assertIn("padding: 0 !important;", list_body)
        self.assertIn("margin: 0 !important;", list_body)

        sublist_body = self._rule_body(r"\.custom-toc-sublist")
        self.assertIn("list-style: none !important;", sublist_body)
        self.assertIn("padding-left: 14px !important;", sublist_body)
        self.assertIn("border-left: 1px solid var(--lab-border);", sublist_body)

    def test_toc_item_h3_variant_is_visually_smaller(self):
        item_body = self._rule_body(r"\.custom-toc-item(?!--)")
        self.assertIn("font-size: 0.85rem;", item_body)

        h3_body = self._rule_body(r"\.custom-toc-item--h3")
        self.assertIn("font-size: 0.8rem;", h3_body)

    def test_toc_link_base_styling(self):
        body = self._rule_body(r"\.custom-toc-link(?![:.\w-])")
        self.assertIn("color: var(--lab-muted) !important;", body)
        self.assertIn("text-decoration: none !important;", body)
        self.assertIn("cursor: pointer;", body)
        self.assertIn("display: block;", body)

    def test_toc_link_hover_state_uses_accent_purple(self):
        body = self._rule_body(r"\.custom-toc-link:hover")
        self.assertIn("color: var(--lab-purple) !important;", body)
        self.assertIn("padding-left: 4px;", body)

    def test_toc_link_active_state_is_visually_distinct(self):
        body = self._rule_body(r"\.custom-toc-link\.active")
        self.assertIn("color: var(--lab-purple) !important;", body)
        self.assertIn("font-weight: 700 !important;", body)
        self.assertIn("border-left: 2px solid var(--lab-purple);", body)
        self.assertIn("margin-left: -2px;", body)

    def test_default_mkdocs_secondary_nav_is_hidden(self):
        # The custom card replaces MkDocs' built-in secondary TOC nav, so
        # the stylesheet must forcibly hide it to avoid a duplicate TOC.
        self.assertRegex(
            self.css_text,
            r"\.md-sidebar--secondary\s+\.md-nav--secondary\s*\{\s*"
            r"display:\s*none\s*!important;\s*\}",
        )


class TocCardStickyOffsetVariableTests(unittest.TestCase):
    """Tests for the centralised `--toc-sticky-top` / `--toc-scroll-offset`
    custom properties that the `.custom-toc-card` rule now references
    instead of hardcoded pixel values."""

    @classmethod
    def setUpClass(cls):
        cls.css_text = CSS_PATH.read_text(encoding="utf-8")

    def _root_block(self):
        match = re.search(r":root\s*\{([^}]*)\}", self.css_text, re.DOTALL)
        self.assertIsNotNone(match, "Could not find the `:root { ... }` block")
        return match.group(1)

    def test_toc_sticky_top_defined_in_root_with_expected_default(self):
        root_body = self._root_block()
        self.assertRegex(root_body, r"--toc-sticky-top:\s*90px;")

    def test_toc_scroll_offset_defined_in_root_with_expected_default(self):
        root_body = self._root_block()
        self.assertRegex(root_body, r"--toc-scroll-offset:\s*120px;")

    def test_toc_sticky_top_defined_exactly_once(self):
        matches = re.findall(r"--toc-sticky-top\s*:", self.css_text)
        self.assertEqual(
            len(matches),
            1,
            "--toc-sticky-top should be defined exactly once (in :root)",
        )

    def test_toc_scroll_offset_defined_exactly_once(self):
        matches = re.findall(r"--toc-scroll-offset\s*:", self.css_text)
        self.assertEqual(
            len(matches),
            1,
            "--toc-scroll-offset should be defined exactly once (in :root)",
        )

    def test_toc_sticky_top_referenced_by_custom_toc_card_rule(self):
        match = re.search(
            r"\.custom-toc-card\s*\{([^}]*)\}", self.css_text, re.DOTALL
        )
        self.assertIsNotNone(match)
        self.assertIn("var(--toc-sticky-top)", match.group(1))

    def test_toc_scroll_offset_referenced_by_custom_toc_card_rule(self):
        match = re.search(
            r"\.custom-toc-card\s*\{([^}]*)\}", self.css_text, re.DOTALL
        )
        self.assertIsNotNone(match)
        self.assertIn("var(--toc-scroll-offset)", match.group(1))

    def test_sticky_offset_variables_not_overridden_in_dark_theme_block(self):
        # These are documented as "centralised" offsets, so the dark-theme
        # ([data-md-color-scheme="slate"]) override block should not
        # redefine them with different values.
        dark_match = re.search(
            r'\[data-md-color-scheme="slate"\]\s*\{([^}]*)\}',
            self.css_text,
            re.DOTALL,
        )
        self.assertIsNotNone(dark_match, "Could not find the dark theme override block")
        dark_body = dark_match.group(1)
        self.assertNotIn("--toc-sticky-top", dark_body)
        self.assertNotIn("--toc-scroll-offset", dark_body)


class TocCardStylesheetRegressionTests(unittest.TestCase):
    """Guards against regressions in pre-existing rules near the new block."""

    @classmethod
    def setUpClass(cls):
        cls.css_text = CSS_PATH.read_text(encoding="utf-8")

    def test_toc_card_block_appears_after_theme_mode_controller_block(self):
        theme_mode_idx = self.css_text.find(".theme-mode-btn.active")
        toc_idx = self.css_text.find(".custom-toc-card")
        self.assertNotEqual(theme_mode_idx, -1)
        self.assertNotEqual(toc_idx, -1)
        self.assertLess(
            theme_mode_idx,
            toc_idx,
            "Expected the new TOC card rules to be appended after the "
            "existing theme-mode controller rules",
        )

    def test_preexisting_scrollbar_rules_are_unaffected(self):
        # The new `.custom-toc-card::-webkit-scrollbar` rule is scoped and
        # must not replace the pre-existing global scrollbar rule.
        self.assertRegex(
            self.css_text,
            r"(?<!\.custom-toc-card)::-webkit-scrollbar\s*\{\s*width:\s*8px;",
        )


if __name__ == "__main__":
    unittest.main()