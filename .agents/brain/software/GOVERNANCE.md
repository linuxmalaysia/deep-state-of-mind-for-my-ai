---
okf_version: 0.1
type: architecture_concept
title: "🛡️ Software Governance & Risk Manifest"
description: "OKF-compliant documentation for GOVERNANCE.md."
resource: "file:///.agents/brain/software/GOVERNANCE.md"
timestamp: 2026-07-04T09:40:04Z
---
# 🛡️ Software Governance & Risk Manifest

## ⚖️ Architectural Laws
1. **Zero-Global Pattern:** No global state management regardless of language paradigms.
2. **Atomic Git Hygiene:** One logical change = One commit.
3. **Pedagogical Logic:** Every PR must explain the *Why* in the `walkthrough.md`.

## 🔒 Security Policy
- **Fail-Closed:** If any security audit (e.g., `composer audit`, `npm audit`) fails, the build is rejected.
- **Dependency Sovereignty:** Minimise external packages. If a package is > 1MB or has > 50 sub-dependencies, it requires a manual audit by the Lead Architect.

## 📋 Compliance
- Documentation follows **LDP Standards**.
- Versioning follows **Semantic Versioning 2.0.0**.

