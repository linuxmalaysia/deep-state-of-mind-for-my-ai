---
okf_version: "0.1"
type: "documentation"
title: "FastMCP Server Integration & Continuous Integration Workflows"
timestamp: "2026-09-05T11:43:26Z"
topics: ["openwiki", "integrations", "mcp", "ci-cd", "workflows"]
description: "FastMCP server contract, Context7 RAG endpoints, GitHub Actions workflows."
---
# FastMCP Server Integration & Continuous Integration Workflows

DSOM integrates with modern AI IDE interfaces and automated GitHub Actions to maintain live knowledge compilation and workflow verification.

## 🔌 FastMCP Server Architecture

The native DSOM Model Context Protocol (MCP) server resides in `tools/mcp/server.py` and uses **FastMCP**:

- **Sovereign Markdown Palace Exposure:** Exposes the entire compiled documentation structure directly to AI editors (Cursor, Claude Desktop).
- **Zero-Binary Search Tool:** Integrates sub-millisecond, local OKF-compliant search across all Palace rooms and brain manifests.

## 🤖 Continuous Integration Workflow Catalogue

All workspace modifications are compiled, linted, and verified via automated pipelines:

1. **`gh-pages.yml`:** Installs `uv`, compiles the static MkDocs documentation site with custom hooks, and deploys it to the `gh-pages` branch.
2. **`openwiki-update.yml`:** A scheduled daily cron workflow that runs the native Python OpenWiki emulator and automatically submits a pull request with updated knowledge graphs.
3. **`snyk-scanning.yml`:** Deploys Snyk container and dependency scanning to verify the security integrity of the Python/Node dependencies.

## 🛠️ Troubleshooting CI Permissions

### Pull Request Creation Failures

If the **`openwiki-update.yml`** workflow fails at the pull request creation step with the following error:

```text
GitHub Actions is not permitted to create or approve pull requests. - https://docs.github.com/rest/pulls/pulls#create-a-pull-request
```

This indicates that your repository or organisation permissions are restricting GitHub Actions from opening pull requests. To resolve this:

1. Navigate to your repository's main page on GitHub.
2. Click on **Settings** (the gear icon) at the top.
3. In the left sidebar, click on **Actions** -> **General**.
4. Scroll down to the **Workflow permissions** section.
5. Check the box for **"Allow GitHub Actions to create and approve pull requests"**.
6. Click **Save**.
7. Re-run the failed workflow.
