# 🤝 Contributing to Deep State of Mind (DSOM)

Thank you for your interest in the **Deep State of Mind (DSOM) For My AI Protocol**. This project is a metacognitive governance system. Contributing here requires more than just code; it requires **Cognitive Alignment** with the Lead Architect's vision.

By contributing, you agree to uphold the **Sovereign Laws** enforced by Harisfazillah Jamel.

---

## 🏛️ 1. Architectural Mandates

### Clean Architecture (C-DSOM)
We follow a strict concentric layering system. All contributions must respect the **Inward Dependency Rule**:
* **Entities:** Pure logic. No external dependencies.
* **Use Cases:** Orchestration logic only.
* **Adapters/Drivers:** Where frameworks and external tools (Podman, RHEL) reside.
* *Violation:* Injecting framework-specific code into an Entity will result in an immediate PR rejection.

### The CRISP Strategy
Every interaction with this repository must pass the **CRISP** filter:
* **C**ontext: Always sync with `.agent/brain/` before making changes.
* **R**eview & Record: Document the "Why" in `walkthrough.md` *before* the code is committed.
* **I**teration: Use **Atomic Git Hygiene**. One file, one commit.
* **S**ingle-purpose: PRs must address one specific sub-task. No "monolithic" updates.
* **P**artnership: Maintain the persona of a **Senior Systems Architect**.

---

## ⚖️ 2. Technical Standards

### Linguistic Sovereignty
* **English:** Strictly **UK English** (e.g., 'initialise', 'standardise', 'centre').
* **Malay:** Strictly **DBP-standard Bahasa Melayu Malaysia (Piawai)**. Avoid Indonesian sentence structures or vocabulary (e.g., use 'Tugasan' instead of 'Tugas', 'Piawai' instead of 'Standar').

### Coding Laws
* **Zero-Global Pattern:** No global variables. Use strict state management.
* **HA-Ready:** All scripts and tools must be designed for High-Availability clusters.
* **Sovereign Portability:** Code must be Linux-agnostic and avoid proprietary vendor lock-in.

---

## 🚀 3. The Contribution Workflow

1.  **Phase 1: Reanimation:** Fork and clone. Run `./tools/audit-pre-flight.sh`.
2.  **Phase 2: Brain Sync:** Before coding, update `.agent/brain/task.md` to define your objective and `implementation_plan.md` to verify alignment.
3.  **Phase 3: Logic Record:** Write your architectural intent in `walkthrough.md`.
4.  **Phase 4: Atomic Execution:**
    * Commit changes one file at a time.
    * Format: `type(scope): message` (e.g., `feat(domain): initialise crawler entity`).
5.  **Phase 5: Hibernation Briefing:** In your Pull Request, provide a **Metacognitive Briefing**—a summary of the technical hurdles you faced.

---

## 📄 4. License
All contributions are licensed under the **GNU GPL v3.0**. 

---
*Upholding Open Source Sovereignty | Harisfazillah Jamel (LinuxMalaysia)*

Last Human Audit: 2026-01-12

