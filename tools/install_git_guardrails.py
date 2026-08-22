#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""
DSOM Git Pre-Commit Guardrails Installer
Installs a lightweight pre-commit hook that validates Git commits using guardrails-ai-dsom.
"""

import os
import sys
from pathlib import Path

def install_hook():
    repo_root = Path(__file__).resolve().parent.parent
    hooks_dir = repo_root / ".git" / "hooks"
    if not hooks_dir.exists():
        print("[ERROR] .git/hooks directory not found. Is this a Git repository?")
        sys.exit(1)
    pre_commit_path = hooks_dir / "pre-commit"
    hook_script = r'''#!/usr/bin/env bash
# DSOM Sovereign Pre-Commit Guardrail Hook
set -e
REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null)"
GUARDRAILS_DIR="${REPO_ROOT}/tools/guardrails-ai-dsom"
if [ -d "$GUARDRAILS_DIR" ]; then
    echo "🛡️  Running DSOM Pre-Commit Guardrails..."
    if uv run --with pytest --with pyyaml --with tiktoken pytest "$GUARDRAILS_DIR/tests" -q; then
        echo "✅ [PASS] DSOM 10/10 Custom Guardrails Verified Clean."
    else
        echo "❌ [ERROR] DSOM Guardrail verification failed! Commit aborted."
        exit 1
    fi
fi
exit 0
'''
    pre_commit_path.write_text(hook_script.strip() + "\n", encoding="utf-8")
    if os.name != "nt":
        import stat
        pre_commit_path.chmod(pre_commit_path.stat().st_mode | stat.S_IEXEC)
    print(f"[PASS] Successfully installed DSOM Git Pre-Commit Guardrail Hook at: {pre_commit_path}")

if __name__ == "__main__":
    install_hook()
