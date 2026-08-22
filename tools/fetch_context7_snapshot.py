#!/usr/bin/env python3
"""
Fetch Context7 LLM RAG Snapshot for DSOM.
Retrieves the compiled text stream from Context7 API and saves it safely to references/llms-from-context7.txt.

Standard: Rule 24 Defensive Credential Handling | Rule 20 Local Knowledge First
Author  : Harisfazillah Jamel (LinuxMalaysia)
License : GNU General Public License v3.0
"""

import argparse
import os
import sys
import urllib.request
import urllib.error
from pathlib import Path

# Enforce UTF-8 output encoding
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def fetch_snapshot(tokens: int = 250000, target_path: Path = None, api_key: str = None) -> bool:
    repo_root = Path(__file__).resolve().parent.parent
    if target_path is None:
        target_path = repo_root / "references" / "llms-from-context7.txt"

    url = f"https://context7.com/gitlab_linuxmalaysia/deep-state-of-mind-for-my-ai/llms.txt?tokens={tokens}"
    print("=" * 60)
    print(f"📡 [CONTEXT7 FETCHER] Connecting to {url}...")

    headers = {
        "User-Agent": "DSOM-Context7-Fetcher/1.0",
        "Accept": "text/plain, text/markdown, */*"
    }

    key = api_key or os.getenv("CONTEXT7_API_KEY")
    if key:
        headers["Authorization"] = f"Bearer {key}"
        print("🔑 [AUTH] Using Context7 Bearer Token from environment.")
    else:
        print("ℹ️  [AUTH] No CONTEXT7_API_KEY found, attempting unauthenticated request.")

    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            if response.status != 200:
                print(f"❌ [ERROR] HTTP {response.status}: Failed to fetch snapshot.")
                return False
            data = response.read().decode("utf-8", errors="replace")

        if not data or len(data) < 100:
            print("❌ [ERROR] Received empty or invalid snapshot content.")
            return False

        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_text(data, encoding="utf-8")
        line_count = len(data.splitlines())
        size_kb = len(data.encode("utf-8")) / 1024
        print(f"✅ [SUCCESS] Saved {line_count:,} lines ({size_kb:.1f} KB) to {target_path}")
        return True
    except urllib.error.HTTPError as e:
        print(f"❌ [HTTP ERROR] {e.code}: {e.reason}")
        return False
    except Exception as e:
        print(f"❌ [ERROR] {str(e)}")
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch Context7 LLM Snapshot for DSOM.")
    parser.add_argument("--tokens", type=int, default=250000, help="Token budget (default: 250000)")
    parser.add_argument("--out", type=str, default=None, help="Custom output path")
    args = parser.parse_args()

    out_p = Path(args.out) if args.out else None
    success = fetch_snapshot(tokens=args.tokens, target_path=out_p)
    sys.exit(0 if success else 1)
