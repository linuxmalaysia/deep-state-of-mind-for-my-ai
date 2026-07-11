---
okf_version: 0.1
type: documentation
title: "GitHub Copilot Instructions (DSOM Template)"
description: "OKF-compliant documentation for copilot_instructions_template.md."
resource: "file:///docs/agent-configs/copilot_instructions_template.md"
timestamp: 2026-07-04T09:40:04Z
---
# GitHub Copilot Instructions (DSOM Template)

# Copy this content to `.github/copilot-instructions.md`

## 🏗️ Architectural Standards (DSOM)

1. **Clean Architecture:** Respect the layers. `src/Domain` depends on NOTHING. `src/Application` depends on Domain. `Infrastructure` depends on Application.
2. **Zero-Global:** Never suggest code that uses `global $var` or mutable global state.
3. **Defense in Depth:** Validate all inputs at the Driver/Controller layer.

## 🧠 Personalization (The Architect's Voice)

- **Mantra:** "Complexity is the enemy of security."
- **Style:** Prefer readability over "clever one-liners."
- **Docs:** Add DocBlocks to every method explaining the *Business Logic* (Why), not just the mechanics.

## 🇲🇾 Language Context

- If writing comments in Malay, use **Bahasa Baku (DBP)**.
- Avoid dialect or Indonesian loan words (e.g., Use 'Muat turun' NOT 'Download/Unduh').


---
*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-07-04*
*Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*
