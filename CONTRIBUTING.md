# 🤝 Contributing to Deep State of Mind (DSOM)

Thank you for your interest in contributing to the DSOM project. This project is governed by strict architectural laws to prevent context decay and maintain technical integrity.

By contributing to this repository, you agree to uphold the standards of the **Lead Architect (Harisfazillah Jamel)**.

## ⚖️ Our Standards

### 1. The DSOM Trinity
Every code change must be accompanied by updates to the "Brain" artifacts:
* **`task.md`**: Update the status of the current objective.
* **`walkthrough.md`**: Provide the "Why" and the "Logic" behind the change.
* **`implementation_plan.md`**: Ensure the change aligns with the long-term roadmap.

### 2. Atomic Commits
We follow a strict **One-Change, One-Commit** policy. Do not bundle multiple features or fixes into a single commit.
* **Format:** `type(scope): descriptive message`
* **Examples:** * `feat(tools): add new scanner to privacy-guardian`
    * `fix(brain): correct logic error in task tracker`
    * `docs(readme): update installation instructions`

### 3. Coding Philosophy
* **Zero-Global Pattern:** Avoid global variables and side effects.
* **HA-Ready:** Design for high-availability and zero-downtime environments.
* **Sovereign & Portable:** Use open-source standards (PHP 8.4+, Bash, Python 3.12+). Avoid proprietary vendor lock-in.

## 🚀 How to Contribute

1.  **Fork the Repository:** Create your own copy to work on.
2.  **Clone & Reanimate:** Run `./tools/audit-pre-flight.sh` to ensure your environment is clean.
3.  **Create a Branch:** `git checkout -b feat/your-feature-name`
4.  **Sync the Brain:** Update the `.agent/brain/` files before you start coding.
5.  **Commit Atomics:** Commit your changes one file at a time with detailed messages.
6.  **Pull Request:** Submit your PR with a link to your updated `walkthrough.md` logic.

## 📄 License
By contributing, you agree that your contributions will be licensed under the **GNU GPL v3.0**.

---
*Maintained by Harisfazillah Jamel (LinuxMalaysia)*
