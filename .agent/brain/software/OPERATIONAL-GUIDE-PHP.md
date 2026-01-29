# 🏥 OPERATIONAL-GUIDE-PHP.md (Master v1.4)
### 📜 .agent/brain/software/OPERATIONAL-GUIDE-PHP.md (Master v1.4)

## 1. 🏛️ Purpose & Service Scope
- **Purpose:** Definitive runbook and ITIL-aligned operational standards for PHP services.
- **Scope:** All PHP applications, `src/`, `tools/`, and Composer packages in this repository.
- **Audience:** Developers, SRE/Platform Engineers, Lead Architect, Security Team.
- **Service Relationship:** - **Service Provider:** AI Twin / PHP Development Team.
  - **Service Consumer:** Lead Architect (@lead-architect).
  - **Outcome:** Sovereign, maintainable, and High-Availability (HA) ready infrastructure.

## 2. 🔄 Service Value Chain (SVC) Mapping
Every task issued executes the following lifecycle:
- **Engage:** Intake via `task.md` with strict acceptance criteria and contract verification.
- **Plan:** Release planning in `implementation_plan.md` using ADRs and risk analysis.
- **Design:** Logical design in `walkthrough.md` and test spec definition *before* implementation.
- **Build:** Atomic Git Hygiene + PSR-12 + PHPStan/Psalm + Strict Typing.
- **Deliver:** CI/CD via GitHub Actions + `audit-pre-flight.sh` + `privacy-guardian.sh`.
- **Improve:** Sunday Human Audit + Infection Mutation testing + Retrospectives.

## 3. ⚖️ Standards & PHP Fig (PSR)
- **Strict Typing:** All files **MUST** begin with `declare(strict_types=1);`.
- **PSR Standards:** Mandatory PSR-12 (Style) and PSR-4 (Autoloading).
- **Interface Consistency:** Mandatory PSR-3 (Logging), PSR-7 (HTTP), and PSR-11 (Container).
- **Enforcement:** `vendor/bin/phpcs` gated in Gate 1 Pre-flight checks.

## 4. 🏗️ Environments & Configuration (SKMS)
- **Single Source of Truth (SSoT):** All configuration rooted in `.agent/brain/`.
- **Environment Files:** - `.env.example`: Canonical runtime variables.
  - `.env.local`: Developer local overrides (Strictly excluded from Git).
- **Secrets Management:** Vault or GitHub Secrets only. 
  - **Fail-Closed Rule:** Detected secrets in repo trigger an immediate revocation ritual.
- **Local Quickstart Ritual:**
  ```bash
  git clone <repo> && cd <repo>
  composer install --prefer-dist --no-interaction
  docker compose up --build
  vendor/bin/phpunit --colors=always
  vendor/bin/phpstan analyse
  vendor/bin/psalm

```

## 5. 🚦 Quality Gates & CI/CD (CAPM Integration)

### Gate 1 (PR - Automated):

* **Static Analysis:** PHPStan Level 8+ and Psalm (No warnings).
* **Testing:** Unit/Integration Tests (PHPUnit/Pest) > 80% coverage on logic-critical areas.
* **Security:** `composer audit` / Snyk must return 0 vulnerabilities.
* **Linting:** Zero PSR-12 violations.

### Gate 2 (Pre-release - Manual/Staging):

* Integration tests passing in Staging environment.
* Performance profiling check (Xdebug/Blackfire) against response time thresholds.
* **Metrics Tracking:** Record **CPI/SPI** in `metrics_report.md`.

## 6. 📈 Performance & Memory Governance

* **Memory Limits:** Strictly defined in `php.ini` per service (e.g., 128M/256M).
* **Optimization:** OpCache must be enabled in all Production Docker images.
* **Profiling:** XHProf or Blackfire usage mandatory for Sev2 performance incidents.

## 7. 🛡️ Sovereign Security & Vulnerability

* **Runtime Integrity:** Production containers **MUST** use **Read-Only** filesystems (except `/tmp` or specific paths).
* **Dependency Sovereignty:** - **Zero-Bloat Policy:** Avoid heavy dependencies for trivial tasks.
* **Audit Ritual:** Monthly review of `composer.json` to prune redundant packages.
* **Dependabot:** Weekly review of dependency PRs is mandatory.


* **Privacy Enforcement:** `privacy-guardian.sh` mandatory before every `git push`.

## 8. 🚨 Incident & SRE Protocols

* **Ownership:** Oncall rotation defined in `.agent/brain/php/ONCALL.md`.
* **Service Levels:**
* **Availability SLO:** 99.9% Monthly.
* **MTTR Target:** < 60 minutes for Sev1 incidents.
* **Error Rate SLI:** < 0.5% (5xx) over 10m window.


* **Alerting Thresholds:**
* **Sev1 (P0):** 5xx Errors > 5% for 10m -> PagerDuty + SMS + Slack.
* **Sev2 (P1):** Latency p95 > 1s for 5m -> Slack Alert + Pager.
* **Sev3 (P2):** Performance degradation below SLO -> Slack + Ticket.



## 9. 📝 Logging & Observability

* **Format:** Structured **JSON** (Required: `timestamp`, `level`, `service_id`, `trace_id`).
* **Stack:** Sentry (Exceptions), Prometheus/Grafana (Metrics), ELK/CloudWatch (Logs).
* **Debugging Commands:**
* `docker compose logs -f php`
* `kubectl -n <ns> logs -f deploy/<service-name>`
* `php -S localhost:8000 -t public`



## 10. 🔄 Recovery & "Game Day" Rituals

* **Backups:** Nightly snapshots with 30-day retention and point-in-time recovery.
* **Rollback:** Maintain previous Docker image digests. Rollback is the first-response action for Sev1.
* **Game Day Drill:** Bi-annual ritual to verify "Rollback" and "DB Restore" procedures within the 60-minute MTTR window.

---

*Verified by Harisfazillah Jamel | Lead Architect | 2026-01-30*

