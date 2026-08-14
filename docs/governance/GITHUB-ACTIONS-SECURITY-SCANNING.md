---
okf_version: 0.1
type: documentation
title: "GitHub Actions Security Scanning — CRDA Deprecation & Snyk Migration"
timestamp: "2026-07-27T04:49:00Z"
topics: ["snyk", "github-actions", "security", "crda", "ci-cd", "sarif", "governance"]
description: "L2 analysis document capturing the CRDA deprecation, Snyk replacement pattern, and proven workflow template for DSOM GitHub repositories."
resource: "file:///docs/governance/GITHUB-ACTIONS-SECURITY-SCANNING.md"
---

# GitHub Actions Security Scanning — CRDA → Snyk Migration

> **Status:** Active Governance Document | DSOM Security Standard | 2026-07-27

## Summary

The **Red Hat CodeReady Dependency Analytics (CRDA)** action (`redhat-actions/crda@v1`) is permanently defunct. Its backend API (`gw.api.openshift.io`) was decommissioned by Red Hat with no announced replacement or migration path. Any DSOM repository using the GitHub-generated CRDA starter workflow will fail immediately with a DNS resolution error.

The DSOM-standard replacement is the **native Snyk GitHub Action** (`snyk/actions/python@master`), which integrates directly with Snyk's cloud backend and produces SARIF output compatible with GitHub Code Scanning.

---

## The Failure Signature

When CRDA fails, the GitHub Actions log shows:

```

crda exited with code 1
FIL Unable to reach the server.
error="Post \"https://gw.api.openshift.io/user?user_key=...\": dial tcp:
lookup gw.api.openshift.io on 127.0.0.53:53: no such host"

```

This is a permanent infrastructure failure — not a configuration error. No amount of reconfiguration will resolve it.

---

## Snyk Concepts — Key Distinctions

AI agents and human operators must distinguish between three Snyk identifiers:

| Identifier | Format | Purpose | Used In Workflow? |
|:---|:---|:---|:---|
| **SNYK_TOKEN** | `xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx` | API authentication (personal/service account) | ✅ Yes — as GitHub Secret |
| **Project ID** | `e2f22e91-d40e-4c94-a509-865c2903b6ac` | Identifies a specific project scan in Snyk UI | ❌ No — for API queries only |
| **Org ID** | UUID | Identifies the Snyk organisation | ❌ No — optional advanced config |

---

## Action Version Matrix (Validated 2026-07-27)

| Action | Status | Correct Pin |
|:---|:---|:---|
| `redhat-actions/crda@v1` | ❌ Dead — backend offline | Remove; use Snyk instead |
| `github/codeql-action/upload-sarif@v3` | ⚠️ Deprecated Dec 2025 | Use `@v4` |
| `snyk/actions/python@master` | ✅ Active | Current standard |
| `actions/checkout@v4` | ✅ Active | Current standard |
| `actions/setup-python@v5` | ✅ Active | Current standard |

---

## Proven Workflow Template

The following template was validated in production on 2026-07-27 (commit `841c612`). All steps passed with zero errors.

```yaml
name: Snyk Security Scan

on:
  push:
    branches: [ "main" ]
    paths:
      - "requirements.txt"
      - ".github/workflows/crda.yml"
  pull_request:
    branches: [ "main" ]
    paths:
      - "requirements.txt"
      - ".github/workflows/crda.yml"
  schedule:
    - cron: "0 0 * * 1"
  workflow_dispatch:

concurrency:
  group: snyk-scan-${{ github.ref }}
  cancel-in-progress: true

permissions:
  contents: read
  security-events: write

jobs:
  snyk-scan:
    name: Snyk — Python Dependency Vulnerability Scan
    runs-on: ubuntu-latest
    timeout-minutes: 15
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: "pip"
      - run: pip install -r requirements.txt
      - uses: snyk/actions/python@master
        continue-on-error: true
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
        with:
          args: --sarif-file-output=snyk.sarif --severity-threshold=low
      - uses: github/codeql-action/upload-sarif@v4
        with:
          sarif_file: snyk.sarif
          category: snyk-python-scan

```

---

## Setup Checklist

- [ ] `SNYK_TOKEN` added to GitHub → Settings → Secrets → Actions.
- [ ] `requirements.txt` present at repository root with all external Python dependencies.
- [ ] `github/codeql-action/upload-sarif@v4` (not `@v3`).
- [ ] `continue-on-error: true` on Snyk step — ensures SARIF uploads even when vulnerabilities are found.
- [ ] Results visible at: GitHub → Security → Code scanning.

---

## SOURCES

- [`snyk/actions`](https://github.com/snyk/actions) — Official Snyk GitHub Actions.
- [`github/codeql-action` changelog](https://github.blog/changelog/2025-10-28-upcoming-deprecation-of-codeql-action-v3/) — v3 deprecation notice.
- [`redhat-actions/crda`](https://github.com/redhat-actions/crda) — Archived; no longer maintained.
- [`.agents/skills/github-actions-snyk-scanner/SKILL.md`](https://github.com/linuxmalaysia/deep-state-of-mind-for-my-ai/blob/main/.agents/skills/github-actions-snyk-scanner/SKILL.md) — Executable SOP for this workflow.
- [`.github/workflows/crda.yml`](https://github.com/linuxmalaysia/deep-state-of-mind-for-my-ai/blob/main/.github/workflows/crda.yml) — Live workflow file in this repository.

---
*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-07-27*
*Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*
