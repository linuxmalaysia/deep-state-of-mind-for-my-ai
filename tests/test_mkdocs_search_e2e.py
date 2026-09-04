"""
E2E test using Playwright to verify MkDocs site search indexing of newly adopted skills.
Serves compiled site/ output on a local HTTP port and performs real browser search interactions.
"""
import http.server
import pathlib
import socketserver
import threading
import time
import unittest

try:
    from playwright.sync_api import sync_playwright
    HAS_PLAYWRIGHT = True
except ImportError:
    HAS_PLAYWRIGHT = False


def _find_repo_root(start: pathlib.Path) -> pathlib.Path:
    current = start.resolve()
    for parent in [current, *current.parents]:
        if (parent / ".git").exists():
            return parent
    raise RuntimeError("Could not locate repository root (.git not found)")


REPO_ROOT = _find_repo_root(pathlib.Path(__file__).parent)
SITE_DIR = REPO_ROOT / "site"


class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True


@unittest.skipUnless(HAS_PLAYWRIGHT, "playwright is not installed in this environment")
class MkDocsSearchE2ETests(unittest.TestCase):
    """E2E Playwright test suite validating MkDocs search functionality."""

    @classmethod
    def setUpClass(cls):
        if not SITE_DIR.is_dir() or not (SITE_DIR / "index.html").exists():
            raise unittest.SkipTest(
                f"Compiled MkDocs site directory not found at {SITE_DIR}. Run 'mkdocs build' first."
            )

        # Start a quiet background HTTP server serving SITE_DIR
        class QuietHandler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=str(SITE_DIR), **kwargs)

            def log_message(self, format, *args):
                pass

        cls.server = ReusableTCPServer(("127.0.0.1", 0), QuietHandler)
        cls.port = cls.server.server_address[1]
        cls.server_thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.server_thread.start()
        cls.base_url = f"http://127.0.0.1:{cls.port}/"

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, "server"):
            cls.server.shutdown()
            cls.server.server_close()

    def test_search_indexes_newly_adopted_skills(self):
        """Verifies search modal correctly indexes newly added skills."""
        screenshot_dir = REPO_ROOT / ".logs"
        screenshot_dir.mkdir(exist_ok=True)
        screenshot_path = screenshot_dir / "mkdocs_search_e2e_verification.png"

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={"width": 1280, "height": 800})
            page.goto(self.base_url)

            # Wait for search input in MkDocs Material theme
            search_input = page.locator("input.md-search__input")
            search_input.wait_for(state="visible", timeout=10000)

            # Perform search query for newly adopted skill
            search_input.focus()
            search_input.fill("github-actions-snyk-scanner")

            # Wait for search result container and entries to render
            results_container = page.locator(".md-search-result__list")
            results_container.wait_for(state="visible", timeout=10000)

            # Wait briefly for indexing/rendering
            page.wait_for_timeout(1000)

            results_text = page.locator(".md-search-result").text_content()
            self.assertIn(
                "Snyk",
                results_text,
                "Expected search results to include 'Snyk' for query 'github-actions-snyk-scanner'",
            )

            # Take verification screenshot of search modal with active results
            page.screenshot(path=str(screenshot_path))
            browser.close()

        self.assertTrue(
            screenshot_path.exists(),
            f"Expected verification screenshot at {screenshot_path}",
        )


if __name__ == "__main__":
    unittest.main()
