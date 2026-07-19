---
okf_version: 0.1
type: procedural_skill
title: "Procedural Specification: DSOM Token Calculator"
description: "Calculates token counts via tiktoken in isolated uv Python runspaces."
topics: [tokens, tiktoken, performance, byte-cap, context]
resource: "file:///.agents/skills/dsom-token-calculator/SKILL.md"
timestamp: 2026-07-18T14:52:39Z
---

# Operational Enforcements:
- Trigger this skill dynamically before any output loop that handles extensive datasets or raw configurations.
- If payload calculations return totals greater than **4000 tokens**, the system must block raw screen serialization and switch to targeted `view_file` calls or chunked reading.
