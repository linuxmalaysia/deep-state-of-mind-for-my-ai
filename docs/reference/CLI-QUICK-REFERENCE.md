---
okf_version: 0.2
type: reference
title: "CLI & Terminal Commands Quick Reference"
timestamp: "2026-08-23T07:43:00Z"
sources:
  - file:///references/llms-from-context7.txt
  - file:///tools/mcp/server.py
generated: "hybrid"
verified: "verified"
status: "authoritative"
stale_after: "2027-08-23T07:43:00Z"
topics: ["cli", "reference", "commands", "cheatsheet", "context7", "ansible", "uv", "mcp"]
description: "Categorized quick reference and cheatsheet of essential CLI commands, setup instructions, and code snippets extracted from project artifacts."
---

# CLI & Terminal Commands Quick Reference

This reference aggregates verified command snippets, setup sequences, and tool executions across the DSOM framework.

## 1. Environment & Package Management (`uv`)

### Install `uv` Dependency Manager
```bash
# Official installer (recommended)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Verify installation
uv --version
```

```powershell
# Windows PowerShell installer
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# Verify installation
uv --version
```

### Install DSOM Guardrails
```bash
# Standard installation
uv add guardrails-ai-dsom

# With optional Guardrails AI and Token dependencies
uv add "guardrails-ai-dsom[all]"
```

---

## 2. FastMCP Server & Knowledge Retrieval

### Launch FastMCP Server
```bash
# Run server over stdio
uv run tools/mcp/server.py
```

### Search Code Snippets via FastMCP
Use the `search_code_snippets` tool inside Cursor, Claude Desktop, or your MCP client:
```json
{
  "query": "ansible",
  "limit": 3
}
```

---

## 3. Git Rituals & Guardrails Installation

### Initialize Git and Install Guardrails Hook
```bash
git init
git branch -M main

# Install unbypassable pre-commit guardrail hook
uv run python tools/install_git_guardrails.py
```

### Safe Multi-Remote Git Ritual
```powershell
# Non-interactive multi-remote push
$env:GIT_TERMINAL_PROMPT="0"
$env:GCM_INTERACTIVE="never"
git push origin main
git push gitlab main
```

---

## 4. Documentation Compilation & Sync

### Local Mintlify Preview
```bash
cd docs-source
npm i -g mint
mint dev
```

### Compile Markdown to MDX
```powershell
python tools/build_mintlify_mdx.py
```

### Run Dry-Run Sync Validation
```powershell
python scripts/sync_docs.py --dry-run
```

---

## 5. Control Node & System Automation

### Setup WSL AlmaLinux 10 Control Node
```powershell
# Run automated setup from repository root
.\tools\setup-wsl-almalinux10.ps1
```

### Hardening & Control Node Provisioning
```bash
# Inside WSL / Linux instance with root privileges
bash tools/setup-dsom-control-node.sh
```

### Verify Ansible Baseline Connectivity
```bash
ansible --version
ansible localhost -m ping
ansible all -m ping -i inventory/hosts.yml
```

---
*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-08-23*
*Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*
