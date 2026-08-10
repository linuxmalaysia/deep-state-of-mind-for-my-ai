---
okf_version: "0.1"
type: "documentation"
title: "Quality Verification Framework & Regression Test Suites"
timestamp: "2026-08-10T21:22:55Z"
topics: ["openwiki", "quality", "verification", "testing", "assertions"]
description: "Python test-suite map, OKF/BOM/quoting/symlink assertions."
---
# Quality Verification Framework & Regression Test Suites

DSOM maintains absolute architectural compliance through a rigorous, automated testing framework that executes local quality assertions across all system files.

## 🧪 Regression Test Suite Map

- `test_okf_frontmatter_bom_reorder.py` — Discovers all markdown files and validates that frontmatter starts exactly on line 1, column 1, uses valid OKF v0.1 fields, has no leading UTF-8 BOM characters, and defensively double-quotes special strings.
- `test_docs_symlinks.py` — Confirms that symbolic links pointing to root files (`README.md`, `SECURITY.md`, etc.) are resolved correctly on all deployment targets.
- `test_mcp_server.py` — Exercises the FastMCP server, confirming correct JSON-RPC output and resource discovery.
- `test_readthedocs_config.py` / `test_readthedocs_ledger_sync.py` — Ensures that Read the Docs and GitBook files are synchronised with `SUMMARY.md`.

## 🛠️ Cross-Platform Guardrails

To support cross-platform co-working across Linux, macOS, and Windows environments, tests implement:
- **Windows CRLF Handling:** Byte fence matchers handle both `\\n` and `\\r\\n` line endings natively.
- **POSIX Assertions Bypass:** Permissions/chmod assertions are conditionally evaluated only on POSIX systems (`if os.name != 'nt'`).
- **Git Pointer Detection:** On Windows environments lacking OS symlink support, tests detect text-pointer files and gracefully parse them without raising exceptions.
