#!/usr/bin/env python3

# ==============================================================================
# Protocol    : Deep State of Mind (DSOM) For My AI
# Author      : Harisfazillah Jamel (LinuxMalaysia)
# Timestamp   : 2026-08-05
# License     : GNU General Public License v3.0
# Standard    : UK English | DBP-standard Bahasa Melayu Malaysia (Piawai)
# ==============================================================================
"""
OKF Frontmatter Compliance Script.
Scans a target directory and ensures all .md files use OKF v0.1 YAML frontmatter
with the required fields (okf_version, type, title, timestamp, topics).
"""
import os
import re
import argparse
import yaml
from datetime import datetime, timezone

FRONTMATTER_RE = re.compile(r'\A---\s*\n(.*?)\n---\s*(?:\r?\n|\Z)', re.DOTALL)

def get_okf_type(filepath):
    path_parts = filepath.replace('\\', '/').split('/')
    if 'docs' in path_parts and 'governance' in path_parts:
        return 'governance_protocol'
    elif '.agents' in path_parts and 'skills' in path_parts:
        return 'agent_skill'
    elif '.agents' in path_parts and 'brain' in path_parts:
        return 'architecture_concept'
    elif 'tools-and-automation' in path_parts or 'tools' in path_parts:
        return 'automation_tool'
    elif 'playbooks' in path_parts or 'roles' in path_parts:
        return 'infrastructure_playbook'
    return 'documentation'

def extract_title(content, filename):
    match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if match:
        return match.group(1).strip()
    # Format filename cleanly if H1 isn't found
    name_without_ext = os.path.splitext(filename)[0]
    return name_without_ext.replace('_', ' ').replace('-', ' ').title()

def get_default_topics(okf_type):
    mapping = {
        'governance_protocol': ['dsom', 'governance', 'protocol'],
        'agent_skill': ['dsom', 'skill', 'agent'],
        'architecture_concept': ['dsom', 'brain', 'concept'],
        'automation_tool': ['dsom', 'automation', 'tool'],
        'infrastructure_playbook': ['dsom', 'infrastructure', 'playbook'],
        'documentation': ['dsom', 'documentation']
    }
    return mapping.get(okf_type, ['dsom', 'documentation'])

def serialize_val(val, key):
    # PyYAML safe_dump formats lists as inline arrays with default_flow_style=True
    # and serializes strings, dates, and other scalars natively and safely.
    dumped = yaml.safe_dump(val, default_flow_style=True, allow_unicode=True).strip()
    if dumped.endswith('\n...'):
        dumped = dumped[:-4]
    elif dumped.endswith('...'):
        dumped = dumped[:-3]
    return dumped.strip()

def process_file(filepath, root_dir):
    rel_path = os.path.relpath(filepath, root_dir).replace('\\', '/')
    filename = os.path.basename(filepath)

    with open(filepath, 'r', encoding='utf-8-sig') as f:
        content = f.read()

    if not content.strip():
        return False

    existing_frontmatter = {}
    rest_of_content = content

    # Consume every consecutive leading frontmatter block
    while True:
        match = FRONTMATTER_RE.match(rest_of_content)
        if not match:
            break
        yaml_block = match.group(1)
        rest_of_content = rest_of_content[match.end():]
        try:
            parsed = yaml.safe_load(yaml_block)
            if isinstance(parsed, dict):
                existing_frontmatter.update(parsed)
        except Exception as e:
            print(f"Warning: Failed to parse existing frontmatter block in {rel_path}: {e}")

    # 1. okf_version
    okf_version = existing_frontmatter.get('okf_version')
    if okf_version is None or str(okf_version) != '0.1':
        okf_version = 0.1

    # 2. type
    okf_type = existing_frontmatter.get('type')
    if not okf_type:
        okf_type = get_okf_type(rel_path)

    # 3. title
    title = existing_frontmatter.get('title')
    if not title:
        title = extract_title(rest_of_content, filename)

    # 4. timestamp
    timestamp = existing_frontmatter.get('timestamp')
    if not timestamp:
        timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    else:
        # Convert parsed timestamp (string or datetime) to UTC
        if isinstance(timestamp, str):
            try:
                timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            except Exception:
                pass
        if isinstance(timestamp, datetime):
            if timestamp.tzinfo is None:
                timestamp = timestamp.replace(tzinfo=timezone.utc)
            timestamp = timestamp.astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
        else:
            timestamp = str(timestamp)

    # 5. topics
    topics = existing_frontmatter.get('topics')
    if not topics or not isinstance(topics, list):
        topics = get_default_topics(okf_type)

    # Build updated frontmatter dict
    updated_frontmatter = {
        'okf_version': okf_version,
        'type': okf_type,
        'title': title,
        'timestamp': timestamp,
        'topics': topics
    }

    # Preserve other metadata fields if present
    for k, v in existing_frontmatter.items():
        if k not in updated_frontmatter:
            if isinstance(v, datetime):
                if v.tzinfo is None:
                    v = v.replace(tzinfo=timezone.utc)
                v = v.astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
            updated_frontmatter[k] = v

    # Serialize cleanly keeping specific key order
    ordered_keys = ['okf_version', 'type', 'title', 'timestamp', 'topics']
    yaml_lines = []
    for k in ordered_keys:
        yaml_lines.append(f"{k}: {serialize_val(updated_frontmatter[k], k)}")

    for k, val in updated_frontmatter.items():
        if k not in ordered_keys:
            yaml_lines.append(f"{k}: {serialize_val(val, k)}")

    new_frontmatter_block = "---\n" + "\n".join(yaml_lines) + "\n---\n"
    new_content = new_frontmatter_block + rest_of_content

    if new_content != content:
        with open(filepath, 'w', encoding='utf-8-sig') as f:
            f.write(new_content)
        return True
    return False

def main():
    parser = argparse.ArgumentParser(description="Ensure OKF v0.1 compliance on all Markdown files.")
    parser.add_argument("directory", nargs="?", default=".", help="Root directory to scan (default: '.')")
    args = parser.parse_args()

    root_dir = os.path.abspath(args.directory)
    modified_count = 0
    total_count = 0

    # Exclude list for directories we should not modify/add frontmatter to
    exclude_dirs = {'.git', 'node_modules', '.pytest_cache'}
    
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Prune excluded directories in place
        dirnames[:] = [d for d in dirnames if d not in exclude_dirs]
        
        for filename in filenames:
            if not filename.endswith('.md'):
                continue

            filepath = os.path.join(dirpath, filename)

            # Reject symlinks
            if os.path.islink(filepath):
                continue
                
            # Verify resolved path remains within the resolved root_dir
            try:
                real_root = os.path.realpath(root_dir)
                real_filepath = os.path.realpath(filepath)
                if os.path.commonpath([real_root, real_filepath]) != real_root:
                    continue
            except Exception:
                continue

            total_count += 1
            if process_file(filepath, root_dir):
                rel = os.path.relpath(filepath, root_dir).replace('\\', '/')
                print(f"Standardised/Injected OKF: {rel}")
                modified_count += 1

    print(f"\nScan complete. Total markdown files checked: {total_count}")
    print(f"Total files modified to be OKF-compliant: {modified_count}")

if __name__ == "__main__":
    main()
