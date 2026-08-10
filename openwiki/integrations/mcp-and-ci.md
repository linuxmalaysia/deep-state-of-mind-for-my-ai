---
okf_version: 0.1
type: "documentation"
title: "FastMCP Server Integration & Continuous Integration Workflows"
timestamp: "2026-08-10T12:30:20Z"
topics: ["openwiki", "integrations", "mcp", "ci-cd", "workflows"]
description: "FastMCP server contract, Context7 RAG endpoints, GitHub Actions workflows."
---
# FastMCP Server Integration & Continuous Integration Workflows

DSOM integrates with modern AI IDE interfaces and automated GitHub Actions to maintain live knowledge compilation and workflow verification.

## 🔌 FastMCP Server Architecture

The native DSOM Model Context Protocol (MCP) server resides in `tools/mcp/server.py` and uses **FastMCP**:

- **Sovereign Markdown Palace Exposure:** Exposes the entire compiled documentation structure directly to AI editors (Cursor, Claude Desktop).
- **Zero-Binary Search Tool:** Integrates sub-millisecond, local OKF-compliant search across all Palace rooms and brain manifests.

## 🤖 Continuous Integration Workflow Catalog

All workspace modifications are compiled, linted, and verified via automated pipelines:

1. **`gh-pages.yml`:** Installs `uv`, compiles the static MkDocs documentation site with custom hooks, and deploys it to the `gh-pages` branch.
2. **`openwiki-update.yml`:** A scheduled daily cron workflow that runs the native Python OpenWiki emulator and automatically submits a pull request with updated knowledge graphs.
3. **`snyk-scanning.yml`:** Deploys Snyk container and dependency scanning to verify the security integrity of the Python/Node dependencies.
