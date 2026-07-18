#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ---
# okf_version: 0.1
# type: executable_script
# title: "Core Token Counter Runtime"
# license: "GNU General Public License v3.0"
# ---

import os
import sys
import tiktoken

def count_tokens_in_file(filepath: str, model: str = "gpt-4") -> int:
    """Reads file content and calculates exact token footprints via tiktoken."""
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
        encoding = tiktoken.encoding_for_model(model)
        return len(encoding.encode(text))
    except Exception as e:
        print(f"[ERROR] Failed to read target resource {filepath}: {e}")
        return 0

def scan_path(target_path: str):
    """Parses and computes tokens for explicit files or workspace directory trees."""
    if not os.path.exists(target_path):
        print(f"[ERROR] Target path '{target_path}' does not exist in active workspace.")
        sys.exit(1)

    total_tokens = 0
    if os.path.isfile(target_path):
        tokens = count_tokens_in_file(target_path)
        print(f"[FILE] {target_path}: {tokens} tokens")
        total_tokens = tokens
    elif os.path.isdir(target_path):
        print(f"[DIR] Initiating workspace sweep across target: {target_path}")
        for root, _, files in os.walk(target_path):
            for file in files:
                # Restrict scanning scope to plaintext assets to prevent binary processing overhead
                if not file.endswith((".py", ".md", ".txt", ".json", ".yml", ".yaml", ".sh", ".ps1", ".css", ".html", ".js")):
                    continue
                filepath = os.path.join(root, file)
                tokens = count_tokens_in_file(filepath)
                if tokens > 0:
                    print(f" [ASSET] {filepath}: {tokens} tokens")
                    total_tokens += tokens
    
    print("-" * 60)
    print(f"[SUMMARY] TOTAL COMPUTED WORKSPACE TOKENS: {total_tokens}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("[ERROR] Missing target parameter path.")
        print("Usage: uv run --with tiktoken calculate-tokens.py [TARGET_PATH]")
        sys.exit(1)
    
    scan_path(sys.argv[1])
