# 🛡️ Privacy Guardian (privacy-guardian.sh)

> **"Loose lips sink ships."** - Preventing Data Leaks to AI Models.

## 1. 🏛️ Purpose
**Version:** v1.0
**Description:** A pre-commit and pre-upload scanner that checks the generated `sod_manifest` for sensitive data (PII, API Keys, IPs) to ensure "Sovereign Privacy."

## 2. 🛡️ Safety Mechanisms
| Mechanism | Status | Description |
| :--- | :--- | :--- |
| **Zero-Global Pattern** | ✅ Enforced | Local variable scoping. |
| **Exit-on-Error** | ✅ Active | `set -e` injected. |
| **Heuristic Scan** | ✅ Active | Uses regex for IPv4, Google Keys, Slack Tokens, and Home Paths. |

## 3. ⚙️ Usage
```bash
./tools/privacy-guardian.sh
```

## 4. 🧠 Logic Flow
1.  **Target Verification:** Checks if a `sod_manifest_YYYY-MM-DD.txt` exists.
2.  **Regex Scanning:** Iterates through an array of dangerous patterns:
    *   IPv4 Addresses
    *   Google API Keys (`AIza...`)
    *   OpenAI Keys (`sk-...`)
    *   Slack Tokens (`xoxb...`)
    *   Local User Paths (`/home/user/`)
3.  **Reporting:** Exits with `1` if leaks are found, requiring manual remediation.

## 5. 📝 Extracted Comments
> "Scans the generated DSOM reanimation manifest for sensitive information before it is uploaded to an external AI model."
