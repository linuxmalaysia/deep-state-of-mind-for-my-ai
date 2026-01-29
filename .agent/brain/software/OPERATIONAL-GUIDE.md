# 📖 Software Operational Guide (Master v1.5)

## 1. 🏛️ Purpose & Universal Scope
- **Purpose:** Definitive runbook and ITIL-aligned operational standards for all software services.
- **Scope:** Applies to all applications, tools, and libraries regardless of programming language.
- **Service Relationship:** - **Service Provider:** AI Twin / Development Team.
  - **Service Consumer:** Lead Architect (@lead-architect).
  - **Outcome:** Sovereign, maintainable, and HA-ready infrastructure.

## 2. 🔄 Service Value Chain (SVC) Mapping
Every task issued executes the following lifecycle:
- **Engage:** Intake via `task.md` with strict acceptance criteria and contract verification.
- **Plan:** Release planning in `implementation_plan.md` using ADRs and risk analysis.
- **Design:** Logical design in `walkthrough.md` and test spec definition *before* implementation.
- **Build:** Atomic Git Hygiene + Linting + Static Analysis + Language-specific standards.
- **Deliver:** CI/CD via GitHub Actions + `audit-pre-flight.sh` + `privacy-guardian.sh`.
- **Improve:** Sunday Human Audit + Mutation testing + Retrospectives.

## 3. ⚖️ Universal Standards & Tooling Requirements
Every project must provide "Adapters" for the following:
1. **Dependency Management:** (e.g., Composer, NPM, Cargo, Pip, Go Modules).
   - *Policy:* All lock-files must be committed.
2. **Static Analysis:** (e.g., PHPStan, ESLint, Pylint, ShellCheck).
   - *Policy:* Strict mode mandatory; zero-warning threshold.
3. **Test Suite:** (e.g., PHPUnit, Jest, PyTest, GoTest).
   - *Policy:* Unit and Integration tests required for all logic-critical areas.

## 4. 🚦 Pre-flight & Quality Gates
### Gate 1 (PR - Automated):
1. `audit-pre-flight.sh`: Verification of environment and Git state.
2. `privacy-guardian.sh`: Scan for PII and secrets.
3. **Lint:** Language-specific coding standard check (e.g., PSR-12, PEP8, StandardJS).
4. **Security Audit:** Vulnerability scanning (e.g., `audit` commands or Snyk).

### Gate 2 (Pre-release - Manual/Staging):
- Integration tests passing in Staging.
- Performance profiling check against response time thresholds.
- **Metrics Tracking:** Record **CPI/SPI** in `metrics_report.md`.

## 5. 🏗️ Environments & Configuration (SKMS)
- **Single Source of Truth (SSoT):** All configuration rooted in `.agent/brain/`.
- **Secrets Management:** Vault or GitHub Secrets only. 
  - **Fail-Closed Rule:** Detected secrets in repo trigger an immediate revocation ritual.
- **Local Overrides:** Use `.env.example` as a template; `.env.local` for local overrides (Git-ignored).

## 6. 🔄 Deployment & Portability Standards
All services must be **Sovereign-Portable**:
- **Standard:** Favor Linux-agnostic binaries or OCI-compliant Containers.
- **Isolation:** Avoid proprietary vendor-specific cloud features (No Lock-in).
- **Runtime Integrity:** In Production, containers **MUST** use **Read-Only** filesystems.

## 7. 📈 Performance & Resource Governance
- **Limits:** Strictly defined resource quotas (CPU/Memory) per service.
- **Profiling:** Language-specific profiling mandatory for Sev2 performance incidents.
- **Optimization:** Caching and OpCache equivalents must be enabled in production builds.

## 8. 🚨 Incident & SRE Protocols
- **Service Levels:**
  - **Availability SLO:** 99.9% Monthly.
  - **MTTR Target:** < 60 minutes for Sev1 incidents.
- **Alerting Thresholds:**
  - **Sev1 (P0):** Critical failure/Service Down -> PagerDuty + SMS + Lead Architect.
  - **Sev2 (P1):** Performance/Latency degradation -> Slack Alert + Pager.
- **Escalation:** Defined in project-specific `ONCALL.md`.

## 9. 📝 Logging & Observability
- **Format:** Structured **JSON** (Required: `timestamp`, `level`, `service_id`, `trace_id`).
- **Telemetry:** Exceptions (e.g., Sentry), Metrics (Prometheus), and Centralised Logs.

## 10. 🔄 Recovery & "Game Day" Rituals
- **Backups:** Nightly snapshots with 30-day retention and restoration verification.
- **Rollback:** Maintain previous build digests. Rollback is the first action for Sev1.
- **Game Day Drill:** Bi-annual ritual to verify "Rollback" and "Restore" procedures.

---
*Verified by Harisfazillah Jamel | Lead Architect | 2026-01-30*



# 📖 Software Operational Guide

## 🛠️ Universal Tooling Requirements
Every software project within this repository must provide adapters for:
1. **Dependency Management:** (e.g., Composer, NPM, Cargo, Pip).
2. **Static Analysis:** (e.g., PHPStan, ESLint, Pylint).
3. **Test Suite:** (e.g., PHPUnit, Jest, PyTest).

## 🚦 Pre-flight Rituals
Before any code is committed, the following must pass:
1. `audit-pre-flight.sh`: Verification of environment and Git state.
2. `privacy-guardian.sh`: Scan for PII and secrets.
3. `lint`: Language-specific coding standard check.

## 🔄 Deployment Standard
All software services must be **Sovereign-Portable**. 
- Favor Linux-agnostic binaries or containers.
- Avoid proprietary vendor-specific cloud features (No Lock-in).

