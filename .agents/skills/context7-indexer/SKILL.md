---
okf_version: 0.1
type: skill
title: "Context7 Semantic Indexer"
description: "Governs the use of Context7 for indexing the Sovereign Markdown Palace and retrieving semantic context via MCP."
topics: [context7, semantic, index, mcp, rag]
timestamp: 2026-07-31T00:00:00Z
---
# Context7 Semantic Indexer

## Purpose
This skill governs the integration of [Context7](https://context7.com) within the DSOM architecture. Context7 acts as the external semantic retrieval engine (RAG) for the Sovereign Markdown Palace (`docs/`). It parses markdown documentation, chunks it, and generates searchable code/info snippets using an LLM (e.g., `gemini-3.1-flash-lite`).

## Integration Guidelines

### 1. The Indexing Process
Based on our project structure, Context7 specifically targets the `docs/` folder (such as `docs/governance/OPERATIONAL-SOVEREIGNTY.md` and `docs/governance/ZERO-GLOBAL-MEMORY.md`).
- Context7 clones the `main` branch.
- It bypasses non-RST and non-code configurations to focus directly on our Open Knowledge Format (OKF) markdown documentation.

### 2. Utilizing Context7 via MCP
For AI agents (Cursor, Google Jules, Claude) to query this semantic index:
1. Ensure the agent's MCP (Model Context Protocol) is configured to connect to `https://mcp.context7.com/mcp`.
2. The agent must inject the `CONTEXT7_API_KEY` directly into the MCP client configuration via environment variables.

### 3. Triggering Re-indexing
Currently, Context7 automatically syncs with the configured repository branch. If a massive structural change occurs in the Palace (e.g., via `dsom-state-sync`), ensure the changes are fully committed and pushed to `main` so Context7's webhook or polling mechanism can detect the diff and initiate the Parser step.

## Security (Rule 24 Mandate)
- **NEVER** write the `CONTEXT7_API_KEY` (e.g., `ctx7sk-...`) to a local `.env` file, `.git/config`, or any file tracked by Git.
- **GitLab CI/CD:** If Context7 requires integration via GitLab CI, the API key MUST be stored in GitLab CI/CD Settings as a masked and protected variable.
