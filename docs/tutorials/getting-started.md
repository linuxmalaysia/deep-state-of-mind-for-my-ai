---
okf_version: 0.1
type: documentation
title: "Tutorial: Getting Started with DSOM Tools"
timestamp: "2026-08-13T12:00:00Z"
topics: ["dsom", "tutorial", "getting-started", "tools"]
---
# Getting started with DSOM tools

A step-by-step tutorial guiding you through running, auditing, and integrating the DSOM workspace toolchain.

## Learning objectives

By completing this tutorial, you will:
- **Initialise** the local OpenWiki documentation hub.
- **Audit and repair** OKF v0.1 metadata frontmatter.
- **Spin up** and test the local Model Context Protocol (MCP) server.

---

## Lesson 1: Initialise your OpenWiki hub

Let's start by materialising the local OpenWiki workspace and knowledge graphs.

1. Open your terminal at the project root.
2. Run the initialisation command:

   ```bash
   uv run --with pyyaml python tools/openwiki_emulator.py --init
   ```

3. Open `./openwiki/graph.html` in your web browser. You should see an interactive visualiser map representing the active documentation.

---

## Lesson 2: Audit and repair frontmatter metadata

Now we will verify that all Markdown documentation satisfies the strict Open Knowledge Format (OKF v0.1).

1. Execute the compliance scanning command:

   ```bash
   uv run --with pyyaml python tools/apply_okf_frontmatter.py docs/
   ```

2. The script automatically scans all files. If any fields are missing, it adds them. If formatting is incorrect, it fixes it atomically.
3. Check one of your files to see the newly standardised headers:

   ```bash
   head -n 8 docs/tutorials/index.md
   ```


---

## Lesson 3: Start the FastMCP server

Let's publish our documentation Palace directly to AI clients.

1. Launch the server over `stdio`:

   ```bash
   uv run tools/mcp/server.py
   ```

2. The server sits waiting for JSON-RPC requests.
3. In a separate terminal, run the MCP verification tests to make sure everything communicates properly:

   ```bash
   uv run --with pyyaml --with pytest --with mcp==1.2.1 --with fastmcp pytest tests/test_mcp_server.py
   ```


**Congratulations!** You have completed the getting started tutorial for DSOM.


---
*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-08-14*
*Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*
