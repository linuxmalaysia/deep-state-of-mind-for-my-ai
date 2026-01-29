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

