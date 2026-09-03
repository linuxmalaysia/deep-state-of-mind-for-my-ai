---
okf_version: 0.1
type: agent_skill
title: "📜 Changelog Automation Skill"
timestamp: "2026-09-02T12:00:00Z"
description: "Automates changelog generation from commits, pull requests, and release notes following Keep a Changelog standards and Conventional Commits."
topics: ["changelog", "automation", "keep-a-changelog", "conventional-commits", "dsom"]
name: changelog-automation
---
# 📜 Changelog Automation Skill (`changelog-automation`)

## Purpose

The `changelog-automation` skill automates the generation and maintenance of project changelogs from Git commit histories, pull requests, and release tags. Adhering to the [Keep a Changelog](https://keepachangelog.com/) standard and Conventional Commits specifications, it ensures change logs communicate user impact and breaking changes rather than dumping raw commit messages.

---

## Core Philosophy: Focus on User & Developer Impact

A changelog is a communication document, not a raw `git log` dump.
- **Group Changes by Audience Impact**:
  - **Added**: New features or capabilities.
  - **Changed**: Modifications in existing functionality.
  - **Deprecated**: Soon-to-be removed features.
  - **Removed**: Now-removed features.
  - **Fixed**: Bug fixes.
  - **Security**: Vulnerability resolutions.
- **Highlight Breaking Changes**: Explicitly state migration steps required for developers or users when breaking changes occur.

---

## Tooling & Setup Integration

Integrate standard semantic versioning and commitlint tooling:
- **Conventional Commits**: Enforce commit message formatting (`feat:`, `fix:`, `docs:`, `refactor:`, `perf:`).
- **Automation Tools**: Use tools such as `@commitlint`, `standard-version`, `release-it`, or `semantic-release`.

---

## Keep a Changelog Template Format

```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Feature description detailing user benefit ([#123](https://github.com/org/repo/issues/123)).

### Fixed
- Resolved edge case causing transient timeouts during high load.

## [1.0.0] - 2026-09-02

### Added
- Initial stable release of the component.
```

---
*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | 2026-09-02*
*Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*
