# HOWTO: build_sovereign_book — PDF Internal Repository Archiver

# docs/tools/HOWTO-BUILD-SOVEREIGN-BOOK.md

> **Standard: DSOM For My AI Protocol v6.1 | Archival Persistence**
> **Tool:** `build_sovereign_book.sh` | **Version:** v3.11 | **Platform:** Linux / WSL2 (T2)

---

## 1. Purpose

`build_sovereign_book` is the **High-Fidelity Archiver** for the DSOM ecosystem. It collapses the entire repository's Markdown documentation and brain artifacts into a single, professionally typeset PDF book using **Pandoc** and **LuaLaTeX**. 

**Use it to:**
- Generate an immutable off-site backup of the "Sovereign Brain".
- Audit the repository for "Untracked" artifacts missing from `SUMMARY.md`.
- Produce a readable, versioned PDF manual with a Table of Contents.
- Automatically commit and archive the build artifact into the Git ledger.

**Location:** 
- `tools/build_sovereign_book.sh`

---

## 2. Prerequisites

| Requirement | Minimum | Notes |
|:---|:---|:---|
| Pandoc | 2.19+ | Required for Markdown to LaTeX conversion. |
| LuaLaTeX | TeX Live | Required for complex emoji and font rendering. |
| Rootfs | Linux | Not natively supported on Windows; run from WSL2. |

### 2.1 Installing Dependencies

**Ubuntu/Debian:**
```bash
sudo apt-get update && sudo apt-get install -y pandoc librsvg2-bin fonts-noto-color-emoji texlive-luatex texlive-latex-extra texlive-fonts-recommended texlive-plain-generic
```

**AlmaLinux/RHEL:**
```bash
sudo dnf install -y pandoc librsvg2-tools google-noto-emoji-color-fonts texlive-scheme-medium
```

---

## 3. Usage

### 3.1 Standard Build

```bash
bash tools/build_sovereign_book.sh
```

---

## 4. Build Engine Logic (The 8 Pillars)

1. **High-Res Timestamps:** Embeds `YYYYMMDD_HHMM` into the filename.
2. **Fail-Safe Traps:** Uses Bash traps to ensure `build_tmp/` is purged even on failure.
3. **OS-Aware:** Automatically detects DNF vs APT environments.
4. **Table Flattening:** Normalizes complex Markdown tables for PDF display.
5. **Artifact Discovery:** Scans the folder and warns if files are missing from `SUMMARY.md`.
6. **LuaLaTeX Power:** Supports **Noto Color Emoji** internally for status indicators.
7. **Header Isolation:** Protects the build from LaTeX syntax errors in raw Markdown.
8. **Atomic Ritual:** Commits the PDF and updates `HISTORY.md` automatically.

---

## 5. Reading the Output & Status Codes

| Label | Meaning | Action Needed |
|:---|:---|:---|
| `🔍 Auditing Artifacts` | Scanning for untracked files. | Review `⚠️ UNTRACKED` reports. |
| `🏗️  Building Book` | Pandoc engine is running. | Wait for completion. |
| `⭐ Success` | PDF generated and archived. | Run `git push` to finalize history. |
| `❌ Build failed` | LaTeX or Font error. | Check logs and verify font installations. |

---

## 6. Security Advisory

> [!WARNING]  
> The generated PDF contains your **entire project brain**. 
> - If your project is Private, keep the PDF private. 
> - If you move the PDF outside the repository, treat it as a Sensitive document.

---

## 7. Related Documents

| Document | Purpose |
|:---|:---|
| [`SUMMARY.md`](../../SUMMARY.md) | The definitive index used to order the book. |
| [`HISTORY.md`](../../HISTORY.md) | Updated automatically after every build. |

---

*Standard: DSOM For My AI Protocol v6.1 | Harisfazillah Jamel | LinuxMalaysia*
*Document Version: v1.0 | Created: 2026-04-08*
