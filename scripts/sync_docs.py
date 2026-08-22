#!/usr/bin/env python3
"""
One-way documentation sync pipeline between two GitHub repositories with strict safety guards.
Syncs docs-source/ into downstream Docs repo root for Mintlify auto-build.

Safety Guards:
  Guard A — Source exists & docs.json is valid
  Guard B — Minimum .mdx file count floor (MIN_MDX_FILES, default 5)
  Guard C — Navigation integrity (every navigation path in docs.json has matching .mdx)
  Guard D — Diff preview & max deletions cap (MAX_DELETIONS, default 10; ALLOW_LARGE_DELETIONS=true)
  Guard E — Dry-run mode (--dry-run or DRY_RUN=true)
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# Enforce UTF-8 standard output for cross-platform and Windows console safety
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def run_cmd(cmd, cwd=None, env=None, check=True):
    """Run a shell command and return stdout/stderr."""
    result = subprocess.run(
        cmd,
        cwd=cwd,
        env=env,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False
    )
    if check and result.returncode != 0:
        print(f"[ERROR] Command failed: {' '.join(cmd)}", file=sys.stderr)
        print(f"Stdout: {result.stdout}", file=sys.stderr)
        print(f"Stderr: {result.stderr}", file=sys.stderr)
        sys.exit(result.returncode)
    return result


def extract_pages_from_nav(nav_node):
    """Recursively extract page strings from navigation structure in docs.json."""
    pages = []
    if isinstance(nav_node, list):
        for item in nav_node:
            pages.extend(extract_pages_from_nav(item))
    elif isinstance(nav_node, dict):
        if "pages" in nav_node and isinstance(nav_node["pages"], list):
            for page in nav_node["pages"]:
                if isinstance(page, str):
                    pages.append(page)
                elif isinstance(page, dict):
                    pages.extend(extract_pages_from_nav(page))
        for key in ("tabs", "groups"):
            if key in nav_node and isinstance(nav_node[key], list):
                pages.extend(extract_pages_from_nav(nav_node[key]))
    return pages


def guard_a_source_exists(source_dir: Path):
    """Guard A: Fail if docs-source/ does not exist or docs.json missing/invalid."""
    print("=" * 60)
    print("[GUARD A] Checking source folder and docs.json...")
    if not source_dir.exists() or not source_dir.is_dir():
        print(f"[GUARD A FAILED] Source directory '{source_dir}' does not exist.", file=sys.stderr)
        sys.exit(1)

    docs_json_path = source_dir / "docs.json"
    if not docs_json_path.exists():
        print(f"[GUARD A FAILED] Missing '{docs_json_path}'.", file=sys.stderr)
        sys.exit(1)

    try:
        with open(docs_json_path, "r", encoding="utf-8") as f:
            docs_data = json.load(f)
    except Exception as e:
        print(f"[GUARD A FAILED] Invalid JSON in '{docs_json_path}': {e}", file=sys.stderr)
        sys.exit(1)

    print("[GUARD A PASSED] Source directory and valid docs.json found.")
    return docs_data


def guard_b_minimum_files(source_dir: Path, min_floor: int):
    """Guard B: Fail if .mdx file count is below threshold."""
    print("=" * 60)
    print(f"[GUARD B] Checking .mdx file count (Minimum Floor: {min_floor})...")
    mdx_files = list(source_dir.rglob("*.mdx"))
    count = len(mdx_files)
    print(f"Found {count} .mdx files in '{source_dir}'.")
    if count < min_floor:
        print(f"[GUARD B FAILED] Found only {count} .mdx files, which is below the floor of {min_floor}.", file=sys.stderr)
        sys.exit(1)
    print(f"[GUARD B PASSED] .mdx file count ({count}) meets or exceeds floor ({min_floor}).")
    return mdx_files


def guard_c_navigation_integrity(source_dir: Path, docs_data: dict, mdx_files: list):
    """Guard C: Assert every referenced page in docs.json exists as a .mdx file."""
    print("=" * 60)
    print("[GUARD C] Checking navigation integrity against .mdx files...")
    nav = docs_data.get("navigation", {})
    referenced_pages = extract_pages_from_nav(nav)
    print(f"Found {len(referenced_pages)} page entries referenced in docs.json.")

    missing_pages = []
    referenced_paths = set()
    for page in referenced_pages:
        page_path = source_dir / f"{page}.mdx"
        referenced_paths.add(page_path.resolve())
        if not page_path.exists():
            missing_pages.append(f"{page}.mdx (expected at {page_path})")

    if missing_pages:
        print(f"[GUARD C FAILED] Missing {len(missing_pages)} page(s) referenced in docs.json navigation:", file=sys.stderr)
        for missing in missing_pages:
            print(f"   - {missing}", file=sys.stderr)
        sys.exit(1)

    present_paths = {p.resolve() for p in mdx_files}
    orphans = [p.relative_to(source_dir.resolve()).as_posix() for p in (present_paths - referenced_paths)]
    if orphans:
        print(f"[GUARD C NOTICE] {len(orphans)} orphan .mdx file(s) present but not in docs.json navigation:")
        for orphan in sorted(orphans):
            print(f"   - {orphan}")

    print("[GUARD C PASSED] All navigation entries have corresponding .mdx files.")


def guard_d_compute_diff(source_dir: Path, target_dir: Path, max_deletions: int, allow_large_deletions: bool):
    """Guard D: Compute file diff between source and target working tree; enforce deletion cap."""
    print("=" * 60)
    print("[GUARD D] Computing file diff against downstream repository...")

    source_files = {}
    for p in source_dir.rglob("*"):
        if p.is_file():
            rel = p.relative_to(source_dir).as_posix()
            source_files[rel] = p

    target_files = {}
    for p in target_dir.rglob("*"):
        if p.is_file():
            if ".git" in p.parts:
                continue
            rel = p.relative_to(target_dir).as_posix()
            target_files[rel] = p

    files_added = []
    files_modified = []
    files_deleted = []

    for rel, src_path in source_files.items():
        if rel not in target_files:
            files_added.append(rel)
        else:
            tgt_path = target_files[rel]
            if src_path.read_bytes() != tgt_path.read_bytes():
                files_modified.append(rel)

    for rel in target_files:
        if rel not in source_files:
            files_deleted.append(rel)

    print("Diff Summary:")
    print(f"   - Files Added:    {len(files_added)}")
    for f in sorted(files_added):
        print(f"     + {f}")
    print(f"   - Files Modified: {len(files_modified)}")
    for f in sorted(files_modified):
        print(f"     ~ {f}")
    print(f"   - Files Deleted:  {len(files_deleted)}")
    for f in sorted(files_deleted):
        print(f"     - {f}")

    if len(files_deleted) > max_deletions and not allow_large_deletions:
        print(f"[GUARD D FAILED] Deletions ({len(files_deleted)}) exceed maximum allowed ({max_deletions}).", file=sys.stderr)
        print("   Set ALLOW_LARGE_DELETIONS=true to override if this is intended.", file=sys.stderr)
        sys.exit(1)

    print("[GUARD D PASSED] Diff computed and deletion cap validated.")
    return files_added, files_modified, files_deleted


def main():
    parser = argparse.ArgumentParser(description="One-way documentation sync to Mintlify docs repo.")
    parser.add_argument("--source-dir", default="docs-source", help="Source docs directory in app repo.")
    parser.add_argument("--docs-repo", default=os.getenv("DOCS_REPO", "linuxmalaysia/my-knowledge-brain"), help="Downstream GitHub repo (OWNER/REPO).")
    parser.add_argument("--branch", default="main", help="Target branch.")
    parser.add_argument("--dry-run", action="store_true", default=os.getenv("DRY_RUN", "false").lower() in ("true", "1", "yes"), help="Run all guards and preview diff without pushing.")
    parser.add_argument("--allow-large-deletions", action="store_true", default=os.getenv("ALLOW_LARGE_DELETIONS", "false").lower() in ("true", "1", "yes"), help="Allow deleting more than MAX_DELETIONS files.")
    parser.add_argument("--min-mdx-files", type=int, default=int(os.getenv("MIN_MDX_FILES", "5")), help="Minimum required .mdx files in source.")
    parser.add_argument("--max-deletions", type=int, default=int(os.getenv("MAX_DELETIONS", "10")), help="Maximum allowed file deletions.")
    args = parser.parse_args()

    app_root = Path.cwd()
    source_dir = (app_root / args.source_dir).resolve()

    print("\nStarting Mintlify Docs Sync Pipeline")
    print(f"   App Root:                 {app_root}")
    print(f"   Source Directory:         {source_dir}")
    print(f"   Downstream Docs Repo:     {args.docs_repo}")
    print(f"   Target Branch:            {args.branch}")
    print(f"   Dry Run Mode:             {args.dry_run}")
    print(f"   Allow Large Deletions:    {args.allow_large_deletions}")
    print(f"   Min MDX Files Floor:      {args.min_mdx_files}")
    print(f"   Max Deletions Cap:        {args.max_deletions}\n")

    docs_data = guard_a_source_exists(source_dir)
    mdx_files = guard_b_minimum_files(source_dir, args.min_mdx_files)
    guard_c_navigation_integrity(source_dir, docs_data, mdx_files)

    token = os.getenv("DOCS_REPO_TOKEN")
    temp_dir = tempfile.mkdtemp(prefix="docs_sync_")
    target_repo_dir = Path(temp_dir) / "docs_repo"

    try:
        print("=" * 60)
        print(f"Cloning target docs repository '{args.docs_repo}'...")
        if token:
            clone_url = f"https://x-access-token:{token}@github.com/{args.docs_repo}.git"
        else:
            print("Notice: DOCS_REPO_TOKEN not found in env, using public https clone (dry-run mode).")
            clone_url = f"https://github.com/{args.docs_repo}.git"

        run_cmd(["git", "clone", "--depth", "1", "--branch", args.branch, clone_url, str(target_repo_dir)])

        files_added, files_modified, files_deleted = guard_d_compute_diff(
            source_dir, target_repo_dir, args.max_deletions, args.allow_large_deletions
        )

        print("=" * 60)
        if args.dry_run:
            print("[GUARD E: DRY RUN ACTIVATED]")
            print(f"   Planned Additions: {len(files_added)}")
            print(f"   Planned Changes:   {len(files_modified)}")
            print(f"   Planned Deletions: {len(files_deleted)}")
            print("   Dry-run mode enabled: No commits or pushes performed.")
            print("[PASS] Dry-run completed successfully.")
            return

        if not token:
            print("[ERROR] Cannot push changes: DOCS_REPO_TOKEN environment variable is missing.", file=sys.stderr)
            sys.exit(1)

        sha_res = run_cmd(["git", "rev-parse", "--short", "HEAD"], cwd=app_root, check=False)
        app_sha = sha_res.stdout.strip() if sha_res.returncode == 0 else "unknown"

        print("=" * 60)
        print(f"Executing sync into downstream repository @ commit {app_sha}...")

        for item in target_repo_dir.iterdir():
            if item.name == ".git":
                continue
            if item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()

        for item in source_dir.iterdir():
            dest = target_repo_dir / item.name
            if item.is_dir():
                shutil.copytree(item, dest)
            else:
                shutil.copy2(item, dest)

        run_cmd(["git", "config", "user.name", "Docs Sync Bot"], cwd=target_repo_dir)
        run_cmd(["git", "config", "user.email", "bot@harisfazillah.mintlify.site"], cwd=target_repo_dir)

        run_cmd(["git", "add", "-A"], cwd=target_repo_dir)
        status_res = run_cmd(["git", "status", "--porcelain"], cwd=target_repo_dir)

        if not status_res.stdout.strip():
            print("[SYNC COMPLETED] No changes detected. Target docs repository is already identical.")
            return

        commit_msg = f"Sync docs from app repo @ {app_sha}"
        run_cmd(["git", "commit", "-m", commit_msg], cwd=target_repo_dir)
        print(f"Committed: '{commit_msg}'")

        print("Pushing to downstream repository main branch...")
        run_cmd(["git", "push", "origin", args.branch], cwd=target_repo_dir)

        total_copied = len(list(source_dir.rglob("*")))
        print("=" * 60)
        print("[SYNC SUCCESSFUL]")
        print(f"   Total source items copied: {total_copied}")
        print(f"   Files added:               {len(files_added)}")
        print(f"   Files modified:            {len(files_modified)}")
        print(f"   Files deleted:             {len(files_deleted)}")
        print(f"   Downstream target:         https://github.com/{args.docs_repo}")
        print(f"   Live Mintlify Portal:      https://harisfazillah.mintlify.site")

    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir, ignore_errors=True)


if __name__ == "__main__":
    main()
