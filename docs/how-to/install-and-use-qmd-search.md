---
okf_version: 0.2
type: documentation
title: "How to Install, Manage, and Query On-Device Documents with QMD Search"
timestamp: "2026-10-09T00:00:00Z"
topics: ["qmd", "search", "how-to", "mcp", "semantic-search"]
resource: "file:///docs/how-to/install-and-use-qmd-search.md"
sources: [{author: "Harisfazillah Jamel (LinuxMalaysia)", id: "dsom-core-spec", resource: "/docs/governance/DSOM-TRI-PHASIC-COGNITIVE-ARCHITECTURE.md", title: "Deep State of Mind (DSOM) Governance Architecture", type: "architecture_spec", url: "https://github.com/linuxmalaysia/deep-state-of-mind-for-my-ai/blob/main/docs/governance/DSOM-TRI-PHASIC-COGNITIVE-ARCHITECTURE.md"}]
spec_version: "0.2"
description: "Step-by-step Diátaxis how-to guide for installing QMD, managing multi-project collections, performing incremental updates, setting up cron background synchronization, and integrating with Model Context Protocol (MCP)."
---
# How to Install, Manage, and Query On-Device Documents with QMD Search

This guide details how to install, configure, and operate **QMD (Query Markup Documents)**—an on-device, hybrid search engine combining BM25 lexical search, semantic vector embeddings (via GGUF / `node-llama-cpp`), and LLM re-ranking without any cloud dependencies.

---

## Prerequisites

* Linux or WSL2 (Ubuntu / AlmaLinux) environment.
* Node.js v20+ and `npm`.
* `crontab` utility for automated background synchronization.

---

## 1. Clean Installation Without Root Conflicts

To prevent root permission issues during global NPM package installation, configure a user-scoped NPM directory (`~/.npm-global`).

```bash
# 1. Create global directory and configure npm prefix
mkdir -p ~/.npm-global
npm config set prefix '~/.npm-global'

# 2. Install QMD globally as user
npm install -g @tobilu/qmd

# 3. Add to user PATH in ~/.bashrc if not already present
grep -q '~/.npm-global/bin' ~/.bashrc || echo 'export PATH="$HOME/.npm-global/bin:$PATH"' >> ~/.bashrc
export PATH="$HOME/.npm-global/bin:$PATH"

# 4. Download local GGUF models (embedding and re-ranking)
qmd pull --progress
```

---

## 2. Multi-Project Collection Registration

Register unique collection names for each project workspace to prevent index collisions in `~/.cache/qmd/index.sqlite`.

```bash
# Register project documentation and AI agent skill directories
qmd collection add /home/user/workspace/my-project/docs --name myproj-docs
qmd collection add /home/user/workspace/my-project/.agents --name myproj-agents

# Add human context summaries to guide semantic search routing
qmd context add qmd://myproj-docs "Technical documentation, API specs, and architecture design notes"
qmd context add qmd://myproj-agents "AI agent constitution, brain memory files, and executable skills"

# Generate initial vector embeddings
qmd embed
```

---

## 3. Incremental Indexing Routines

QMD uses SHA-256 content hashes and file modification timestamps (`mtime`) to perform fast incremental scans. Unchanged files are skipped automatically during embedding calculations.

```bash
# 1. Scan collections for new, modified, or deleted Markdown files (~1-2 seconds)
qmd update

# 2. Embed vector representations strictly for new or modified text chunks
qmd embed

# 3. (Optional) Purge stale records of deleted files and reclaim database space
qmd cleanup
```

---

## 4. Automated Hourly Background Sync

To guarantee that on-device search indices remain updated without manual intervention, configure an automated hourly cron job.

### Create Sync Script (`~/.local/bin/qmd-sync-hourly.sh`)

```bash
#!/usr/bin/env bash
# ==============================================================================
# QMD Hourly Incremental Sync Script (WSL2 / Linux)
# Protocol: Deep State of Mind (DSOM) v0.2
# ==============================================================================

set -euo pipefail

export PATH="$HOME/.npm-global/bin:$HOME/.local/bin:/usr/local/bin:/usr/bin:/bin:$PATH"
LOG_FILE="$HOME/.local/var/log/qmd-sync.log"

mkdir -p "$HOME/.local/var/log"
echo "[$(date '+%Y-%m-%d %H:%M:%S')] === Starting QMD incremental update ===" >> "$LOG_FILE"

if command -v qmd >/dev/null 2>&1; then
    qmd update >> "$LOG_FILE" 2>&1 || echo "[$(date '+%Y-%m-%d %H:%M:%S')] Warning: qmd update exited with code $?" >> "$LOG_FILE"
    qmd embed >> "$LOG_FILE" 2>&1 || echo "[$(date '+%Y-%m-%d %H:%M:%S')] Warning: qmd embed exited with code $?" >> "$LOG_FILE"
else
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ERROR: qmd binary not found in PATH" >> "$LOG_FILE"
    exit 1
fi

echo "[$(date '+%Y-%m-%d %H:%M:%S')] === QMD incremental update completed ===" >> "$LOG_FILE"
```

### Install Crontab Job

```bash
chmod +x ~/.local/bin/qmd-sync-hourly.sh
(crontab -l 2>/dev/null | grep -v "qmd-sync-hourly.sh" ; echo "0 * * * * /home/$USER/.local/bin/qmd-sync-hourly.sh") | crontab -
```

---

## 5. Model Context Protocol (MCP) Server Setup

Register QMD as an MCP tool server for AI agents in `~/.gemini/config/mcp_config.json` or workspace `mcp.json`:

```json
{
  "mcpServers": {
    "qmd": {
      "command": "/home/user/.npm-global/bin/qmd",
      "args": ["mcp"]
    }
  }
}
```

Set secure file permissions:
```bash
chmod 600 ~/.gemini/config/mcp_config.json
```

---

## 6. Verification and Querying

Execute verification queries to confirm proper indexation:

```bash
# BM25 Lexical Keyword Search
qmd search "architecture" -c myproj-docs --json -n 2

# Semantic Vector Search
qmd vsearch "cognitive state preservation" -c myproj-docs -n 2

# Check index health and status
qmd status
```

---
*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-10-09*
*Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*
