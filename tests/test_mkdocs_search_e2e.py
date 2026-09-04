"""
E2E test using Playwright to check MkDocs site search indexing of newly adopted skills.
Serves compiled site/ output on a local HTTP port and performs real browser search interactions.
"""
import http.server
import pathlib
import socketserver
import tempfile
import threading
import unittest

try:
    from playwright.sync_api import sync_playwright
    _PLAYWRIGHT_AVAILABLE = True
except ImportError:
    _PLAYWRIGHT_AVAILABLE = False


def _find_repo_root(start: pathlib.Path) -> pathlib.Path:
    current = start.resolve()
    for parent in [current, *current.parents]:
        if (parent / ".git").exists():
            return parent
    raise RuntimeError(
        f"Could not locate repository root (.git not found) starting from path '{start}'. "
        "Please run tests inside a valid Git checkout repository."
    )


class ReusableTCPServer(socketserver.TCPServer):
    allow_reuse_address = True


class MkDocsSearchE2ETests(unittest.TestCase):
    """E2E Playwright test suite checking MkDocs search functionality."""

    @classmethod
    def setUpClass(cls):
        if not _PLAYWRIGHT_AVAILABLE:
            raise unittest.SkipTest("playwright is not installed in this environment")

        repo_root = _find_repo_root(pathlib.Path(__file__).parent)
        site_dir = repo_root / "site"

        if not site_dir.is_dir() or not (site_dir / "index.html").exists():
            raise unittest.SkipTest(
                f"Compiled MkDocs site directory not found at {site_dir}. Run 'mkdocs build' first."
            )

        # Start a quiet background HTTP server serving site_dir
        class QuietHandler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=str(site_dir), **kwargs)

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
        """Checks search modal correctly indexes newly added skills."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            screenshot_path = pathlib.Path(tmp_dir) / "mkdocs_search_e2e_check.png"

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

                # Wait for target result item
                target_result = page.locator("a.md-search-result__link", has_text="GitHub Actions Snyk")
                target_result.first.wait_for(state="visible", timeout=10000)

                title_text = target_result.first.text_content()
                self.assertIn(
                    "GitHub Actions Snyk",
                    title_text,
                    "Expected target search result title to contain 'GitHub Actions Snyk' for query 'github-actions-snyk-scanner'",
                )

                # Take screenshot of search modal with active results
                page.screenshot(path=str(screenshot_path))
                browser.close()

            self.assertTrue(
                screenshot_path.exists(),
                f"Expected screenshot at {screenshot_path}",
            )


if __name__ == "__main__":
    unittest.main()
