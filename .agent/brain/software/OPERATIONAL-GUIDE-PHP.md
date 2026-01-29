# 🏥 OPERATIONAL-GUIDE-PHP.md (v1.2)
### 📜 .agent/brain/software/OPERATIONAL-GUIDE-PHP.md (v1.2)

## 1. Purpose & Scope
- **Purpose:** Provide the runbook and operational standards for PHP services.
- **Scope:** Applies to all PHP applications, src/, tools/, and Composer packages.
- **Audience:** Developers, SREs, Lead Architect.

## 2. Ownership & Prerequisites
- **Service Owner:** @lead-architect
- **Oncall Rotation:** Defined in `.agent/brain/php/ONCALL.md`.
- **Local Tools:** Docker, PHP CLI (8.2+ recommended), Composer 2.x.
- **Observability:** Sentry, Prometheus/Grafana, ELK/CloudWatch.

## 3. Quickstart (Local Ritual)
```bash
git clone <repo> && cd <repo>
composer install --prefer-dist --no-interaction
docker compose up --build
vendor/bin/phpunit --colors=always
vendor/bin/phpstan analyse

```

## 4. ⚖️ Standards & PHP Fig (PSR)

All code must adhere to the following standards:

* **Strict Typing:** All new files **MUST** begin with `declare(strict_types=1);`.
* **PSR-12:** Extended Coding Style Guide (Mandatory).
* **PSR-4:** Autoloading Standard.
* **PSR-3/7/11:** Logging, HTTP Messages, and Container interfaces.
* **Enforcement:** Use `vendor/bin/phpcs` in pre-flight checks.

## 5. 🏗️ Environments & Configuration

* **.env.example:** Canonical runtime variables.
* **.env.local:** Developer overrides (Never committed).
* **Secrets:** Use GitHub Secrets or Vault. **Fail-Closed Rule:** Builds must fail if a secret is detected in the repository.

## 6. 🚦 Quality Gates & CI/CD

### Gate 1 (PR):

* PHPStan Level 8+ (No warnings).
* Unit Tests (PHPUnit/Pest) > 80% coverage (Logic-critical areas).
* `composer audit` must return 0 vulnerabilities.

### Gate 2 (Pre-release):

* Integration tests in Staging.
* Performance profiling check (Xdebug/Blackfire).

## 7. 📈 Memory & Performance Governance

* **Memory Limit:** Strictly defined in `php.ini` per service (e.g., 128M/256M).
* **Profiling:** Use XHProf or Blackfire for Sev2 performance incidents.
* **Optimization:** OpCache must be enabled in Production Docker images.

## 8. 🛡️ Sovereign Security & Vulnerability

* **Runtime Integrity:** In Production, the PHP container filesystem should be **Read-Only** except for `/tmp` and specific upload paths.
* **Zero-Bloat Policy:** Avoid adding heavy dependencies for trivial tasks.
* **Audit Ritual:** Monthly review of `composer.json`.
* **Dependabot:** Weekly review of PRs is mandatory.

## 9. 🚨 Incident & Alerting (SRE)

* **SLO:** 99.9% availability, MTTR < 60 mins for Sev1.
* **Sev1 (P0):** 5xx Errors > 5% for 10m -> PagerDuty + SMS.
* **Sev2 (P1):** Latency p95 > 1s for 5m -> Slack Alert.

## 10. 📝 Logging & Debugging

* **Structured Logs:** Always log in JSON format for ELK ingestion.
* **Trace IDs:** Ensure Trace IDs are passed across microservices for debugging.
* **Commands:**
* `docker compose logs -f php`
* `php -S localhost:8000 -t public`

## 11. 🔄 Backups & Recovery

* **Nightly Backups:** Automated DB snapshots with 30-day retention.
* **Rollback:** Maintain previous Docker image digests. Rollback is the first action for Sev1.
* **Game Day Drill:** Bi-annual ritual to verify "Rollback" and "DB Restore" procedures within the 60-minute MTTR window.

---

*Verified by Harisfazillah Jamel | Lead Architect | 2026-01-30*

---

# 🏥 OPERATIONAL-GUIDE-PHP.md (v1.3)
### 📜 .agent/brain/software/OPERATIONAL-GUIDE-PHP.md (v1.3)

## 1. 🏛️ Purpose & Service Scope
- **Purpose:** Definitive runbook and ITIL-aligned operational standards for PHP services.
- **Scope:** All PHP applications, `src/`, `tools/`, and Composer packages.
- **Service Relationship:** - **Provider:** AI Twin / PHP Team.
  - **Consumer:** Lead Architect (@lead-architect).
  - **Outcome:** Sovereign, maintainable, and HA-ready infrastructure.

## 2. 🔄 Service Value Chain (SVC) Mapping
- **Engage:** Intake via `task.md` with strict acceptance criteria.
- **Plan:** Release planning in `implementation_plan.md` using ADRs.
- **Design:** Logical design in `walkthrough.md` *before* implementation.
- **Build:** Atomic Git Hygiene + PSR-12 + PHPStan/Psalm.
- **Deliver:** CI/CD via GitHub Actions + `audit-pre-flight.sh`.
- **Improve:** Sunday Human Audit + Infection Mutation testing.

## 3. ⚖️ Standards & PHP Fig (PSR)
- **Strict Typing:** All files **MUST** begin with `declare(strict_types=1);`.
- **PSR Standards:** Mandatory PSR-12 (Style) and PSR-4 (Autoloading).
- **Interface Consistency:** Mandatory PSR-3 (Logging) and PSR-7 (HTTP).
- **Enforcement:** `vendor/bin/phpcs` gated in Gate 1.

## 4. 🏗️ Environments & Configuration (SKMS)
- **SSoT:** All config rooted in `.agent/brain/` (The SKMS).
- **Secrets:** Vault or GitHub Secrets only. **Fail-Closed Rule:** Detected secrets in repo trigger an immediate revocation ritual.
- **Local Ritual:**
  ```bash
  composer install --prefer-dist --no-interaction
  docker compose up --build
  vendor/bin/phpunit && vendor/bin/phpstan analyse

```

## 5. 🚦 Quality Gates (CAPM Integration)

* **Gate 1 (PR):** PHPStan Level 8, 80% Coverage, 0 Composer Vulnerabilities.
* **Gate 2 (Pre-release):** Staging integration tests + Performance smoke tests.
* **Metrics:** Track **CPI/SPI** in `metrics_report.md`.

## 6. 📈 Performance & Memory Governance

* **Limits:** Hard-coded in `php.ini` (128M/256M).
* **OpCache:** Mandatory in Production Docker images.
* **Profiling:** XHProf/Blackfire usage mandatory for Sev2 latency spikes.

## 7. 🛡️ Sovereign Security

* **Runtime Integrity:** Production containers use **Read-Only** filesystems.
* **Dependency Sovereignty:** Monthly audit of `composer.json` to prune bloat.
* **Privacy:** `privacy-guardian.sh` mandatory before every `git push`.

## 8. 🚨 Incident & SRE Protocols

* **SLO:** 99.9% Availability | **MTTR:** < 60 mins.
* **Sev1 (P0):** 5xx > 5% for 10m -> PagerDuty + SMS.
* **Escalation:** Defined in `.agent/brain/php/ONCALL.md`.

## 9. 📝 Logging & Observability

* **Format:** Structured **JSON** (timestamp, level, service_id, trace_id).
* **Stack:** Sentry (Errors), Prometheus (Metrics), ELK (Logs).

## 10. 🔄 Recovery & "Game Day" Rituals

* **Backups:** Nightly snapshots, 30-day retention.
* **Rollback:** First-response action for Sev1 deploy incidents.
* **Game Day:** Bi-annual restore test to staging to verify MTTR.

---

*Verified by Harisfazillah Jamel | Lead Architect | 2026-01-30*

