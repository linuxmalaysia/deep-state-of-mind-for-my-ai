# HOWTO: Upgrade and Audit DSOM (Scenario 2)

**Author:** Harisfazillah Jamel  
**Version:** 1.0 (DSOM v5.2)  
**License:** GPLv3  

> **Scenario 2:** You have a project already running an older version of DSOM (e.g., v4.0). You want to upgrade to the latest v5.x features (ITIL Alignment, Privacy Hardening).

---

## 1. Introduction
This guide explains the safe procedure to upgrade the DSOM Protocol in a live project without losing your "Mental Anchor" or breaking existing context.

**Target Audience:** Digital Stewards, Maintainers.

## 2. Prerequisites
*   **Existing DSOM Install:** A project with an `.agent/brain/` directory.
*   **Clean Git State:** Commit all pending changes before starting.

## 3. The Procedure

### Step 1: Backup (Sovereign Safety)
Before overwriting tools, ensure your Brain artifacts are safe.

```bash
cp -r .agent/brain .agent/brain_backup_$(date +%F)
```

### Step 2: Update Tooling and Docs
You need to overwrite the `tools/` and `docs/` directories with the latest version from the master DSOM repository.

**If using Submodules:**
```bash
git submodule update --remote
cp -r .dsom-core/tools .
cp -r .dsom-core/docs .
```

**If Manual Copy:**
1.  Download the latest release zip from GitHub.
2.  Extract and overwrite the `tools/` and `docs/` folders in your project root.
3.  **Critical:** Do NOT verify/overwrite `.agent/brain/` yet.

### Step 3: Protocol Injection (The Constitution)
The upgrade often involves new "Laws" in `AI-MASTER-PROTOCOL.md` (e.g., ITIL Service Alignment).

1.  **Check `docs/AI-MASTER-PROTOCOL.md`:** Ensure the new file completely replaces the old one.
2.  **Verify `SUMMARY.md`:** Ensure new documents (like `ITIL-ALIGNMENT.md`) are listed.

### Step 4: The Audit (Re-Calibration)
New versions might require new file structures or configs.

1.  **Run the Initializer again:**
    ```bash
    bash tools/init-brain.sh
    ```
    *Why?* Newer versions of this script might check for new required files (like `DSOM_TEMPLATE.md`). It will skip existing files, so your `task.md` is safe.

2.  **Run the Privacy Guardian:**
    ```bash
    bash tools/privacy-guardian.sh
    ```
    *Why?* New patterns (like AWS Keys) might be detected in your old manifests. Clean them up.

### Step 5: Context Re-Sync
Your AI agent might be confused by the sudden change in Protocol.

1.  **Generate a fresh Manifest:**
    ```bash
    bash tools/reanimate.sh
    ```
2.  **Upload to AI:**
    > *"I have upgraded the DSOM Protocol to v5.2. Please analyze the attached manifest. Note the new Section 11 in the Master Protocol regarding ITIL Service Alignment. Confirm you understand our new Service Relationship."*

---

## 4. Troubleshooting

**Q: My `walkthrough.md` was overwritten!**  
A: `init-brain.sh` checks if files exist before writing. If it was overwritten, you might have used a `cp` command that targeted the brain directory. Restore from `brain_backup`.

**Q: The AI refuses to acknowledge the new laws.**  
A: The context window might be stale. Start a **New Chat Session** and perform the full Reanimation Ritual.

## 5. References
*   [Changelog](../CHANGELOG.md)
*   [Ritual of Transition](RITUAL-OF-TRANSITION.md)
