---
name: qmd-search
version: "1.0.0"
description: "SOP for setting up, managing collections, incremental indexing, and querying on-device documents using the QMD hybrid search engine."
topics: ["qmd", "search", "semantic", "vector", "bm25"]
author: "Harisfazillah Jamel (LinuxMalaysia)"
license: "GPL-3.0-or-later"
okf_version: 0.2
type: agent_skill
status: stable
stale_after: "2027-10-01"
title: "QMD On-Device Search & Multi-Project Management SOP"
timestamp: "2026-10-09T00:00:00Z"
resource: "/.agents/skills/qmd-search/SKILL.md"
sources: [{author: "Harisfazillah Jamel (LinuxMalaysia)", id: "dsom-core-spec", resource: "/docs/governance/DSOM-TRI-PHASIC-COGNITIVE-ARCHITECTURE.md", title: "Deep State of Mind (DSOM) Governance Architecture", type: "architecture_spec", url: "https://github.com/linuxmalaysia/deep-state-of-mind-for-my-ai/blob/main/docs/governance/DSOM-TRI-PHASIC-COGNITIVE-ARCHITECTURE.md"}]
generated: {by: "Google Jules & Antigravity", timestamp: "2026-10-09T00:00:00Z"}
spec_version: "0.2"
allowed_tools: ["file_system_write", "file_system_read", "bash"]
tags: ["qmd", "search", "semantic", "vector", "bm25"]
---
# QMD On-Device Search & Multi-Project Management SOP

## Overview & Scope
This skill governs setting up, managing document collections, executing incremental updates, and querying local markdown documents using the **QMD (Query Markup Documents)** search engine. QMD combines lexical BM25 search, semantic vector search, and LLM re-ranking completely on-device without cloud dependencies.

---

## 1. Multi-Project Collection Registration
Always register unique, project-scoped collection names to prevent collisions in `~/.cache/qmd/index.sqlite`:

```bash
# Register documentation and agent rules
qmd collection add /path/to/project/docs --name <proj>-docs
qmd collection add /path/to/project/.agents --name <proj>-agents

# Add human context summaries
qmd context add qmd://<proj>-docs "Technical documentation and architecture"
qmd context add qmd://<proj>-agents "AI constitution, palace brain, and skills"

# Generate embeddings
qmd embed
```

---

## 2. Targeted Querying (Avoiding Cross-Project Clutter)
Target queries using `-c <collection>` when working within a specific project:

```bash
# Lexical BM25 search
qmd search "keyword" -c <proj>-docs

# Semantic vector search
qmd vsearch "conceptual description" -c <proj>-docs
```

---

## 3. Incremental Indexing (Add, Modify, Delete Only)
QMD uses SHA-256 content hashes and mtime comparisons. It does NOT re-index or re-embed unchanged files:

```bash
# 1. Scan for new, modified, or deleted files across all collections (fast, ~1-2s):
qmd update

# 2. Embed only newly added/modified text chunks (skips all existing vectors):
qmd embed

# Optional: Clean up deleted file records & reclaim database space:
qmd cleanup
```

---

## 4. Hourly Cron Sync Setup
To keep on-device indices continuously updated across projects, configure a cron task running `qmd update` and `qmd embed`:

### Sync Script (`~/.local/bin/qmd-sync-hourly.sh`)
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

### Register Crontab Job
```bash
chmod +x ~/.local/bin/qmd-sync-hourly.sh
(crontab -l 2>/dev/null | grep -v "qmd-sync-hourly.sh" ; echo "0 * * * * /home/$USER/.local/bin/qmd-sync-hourly.sh") | crontab -
```

---

## 5. Model Context Protocol (MCP) Integration
Configure `~/.gemini/config/mcp_config.json` or project `mcp.json` using the executable path resolved during setup (e.g. `qmd` on `PATH` or `$HOME/.npm-global/bin/qmd`):

```json
{
  "mcpServers": {
    "qmd": {
      "command": "qmd",
      "args": ["mcp"]
    }
  }
}
```

---

## 6. Turnkey AI Master Prompt

For immediate turnkey integration into new projects with AI agents, copy the prompt below:

```markdown
# MASTER PROMPT: TURNKEY INTEGRATION OF QMD ON-DEVICE SEARCH

You are instructed to integrate the QMD (Query Markup Documents) local search engine into this project to enable AI agents and developers to execute fast local searches (BM25 + Semantic Vector Search + LLM Re-ranking) 100% on-device.

Please execute the following phases:

### PHASE 1: CHECK QMD AVAILABILITY
1. Check if the `qmd` binary exists:
   ```bash
   which qmd || which ~/.npm-global/bin/qmd
   ```
2. IF ALREADY INSTALLED:
   - Record the version (`qmd --version`).
   - Ensure symbolic link exists for Antigravity agent:
     ```bash
     mkdir -p ~/.gemini/antigravity/bin
     ln -sf $(which qmd || echo "$HOME/.npm-global/bin/qmd") ~/.gemini/antigravity/bin/qmd
     ```
   - Skip to PHASE 3.

### PHASE 2: CLEAN INSTALLATION (IF NOT INSTALLED)
1. IF NOT INSTALLED:
   - Verify Node.js version is v22+ (`node -v`).
   - Prepare root-conflict-free user directory:
     ```bash
     mkdir -p ~/.npm-global
     npm config set prefix '~/.npm-global'
     npm install -g @tobilu/qmd
     grep -q '~/.npm-global/bin' ~/.bashrc || echo 'export PATH="$HOME/.npm-global/bin:$PATH"' >> ~/.bashrc
     export PATH="$HOME/.npm-global/bin:$PATH"
     ```
   - Download local quantized GGUF models:
     ```bash
     qmd pull --progress
     ```
   - Create symbolic link for agent:
     ```bash
     mkdir -p ~/.gemini/antigravity/bin
     ln -sf ~/.npm-global/bin/qmd ~/.gemini/antigravity/bin/qmd
     ```

### PHASE 3: COLLECTION SETTING
1. Identify documentation and rule folders (`docs/`, `.agents/`, `notes/`).
2. Register collections:
   ```bash
   qmd collection add <ABSOLUTE_PATH> --name docs
   ```
3. Add human context summary:
   ```bash
   qmd context add qmd://docs "Technical documentation and architecture notes"
   ```
4. Generate embeddings:
   ```bash
   qmd embed
   ```

### PHASE 4: MCP PROTOCOL REGISTRATION
Add the `qmd` server to `~/.gemini/config/mcp_config.json` using the executable path resolved during setup (e.g. `qmd` or `$HOME/.npm-global/bin/qmd`):
```json
{
  "mcpServers": {
    "qmd": {
      "command": "qmd",
      "args": ["mcp"]
    }
  }
}
```

### PHASE 5: VERIFICATION QUERY
1. Test BM25 keyword query:
   ```bash
   qmd search "architecture" --json -n 2
   ```
2. Test semantic vector query:
   ```bash
   qmd vsearch "system overview" -n 2
   ```
```

---
*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-10-09*
*Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*
