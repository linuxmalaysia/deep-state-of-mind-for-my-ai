#!/usr/bin/env python3
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

FRONTMATTER_RE = re.compile(r'\A---\s*\n(.*?)\n---\s*\n', re.DOTALL)

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
    if isinstance(val, list):
        items = []
        for x in val:
            x_str = str(x)
            # Quote if there is a space, dash, or colon
            if ' ' in x_str or '-' in x_str or ':' in x_str:
                items.append(f'"{x_str}"')
            else:
                items.append(x_str)
        return f"[{', '.join(items)}]"
    elif isinstance(val, str):
        # Quote string if it contains special characters
        if key in ['title', 'description', 'resource'] or any(c in val for c in ':"#\'\\'):
            escaped = val.replace('\\', '\\\\').replace('"', '\\"')
            return f'"{escaped}"'
        return val
    elif isinstance(val, (float, int)):
        return str(val)
    elif val is None:
        return 'null'
    return str(val)

def process_file(filepath, root_dir):
    rel_path = os.path.relpath(filepath, root_dir).replace('\\', '/')
    filename = os.path.basename(filepath)

    with open(filepath, 'r', encoding='utf-8-sig') as f:
        content = f.read()

    if not content.strip():
        return False

    existing_frontmatter = {}
    rest_of_content = content

    match = FRONTMATTER_RE.match(content)
    if match:
        yaml_block = match.group(1)
        rest_of_content = content[match.end():]
        try:
            parsed = yaml.safe_load(yaml_block)
            if isinstance(parsed, dict):
                existing_frontmatter = parsed
        except Exception as e:
            print(f"Warning: Failed to parse existing frontmatter in {rel_path}: {e}")

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
    elif isinstance(timestamp, datetime):
        timestamp = timestamp.strftime('%Y-%m-%dT%H:%M:%SZ')
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
                v = v.strftime('%Y-%m-%dT%H:%M:%SZ')
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
    new_content = new_frontmatter_block + rest_of_content.lstrip()

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
            total_count += 1
            if process_file(filepath, root_dir):
                rel = os.path.relpath(filepath, root_dir).replace('\\', '/')
                print(f"Standardised/Injected OKF: {rel}")
                modified_count += 1

    print(f"\nScan complete. Total markdown files checked: {total_count}")
    print(f"Total files modified to be OKF-compliant: {modified_count}")

if __name__ == "__main__":
    main()
