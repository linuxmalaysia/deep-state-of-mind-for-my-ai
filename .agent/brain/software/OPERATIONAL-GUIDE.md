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

