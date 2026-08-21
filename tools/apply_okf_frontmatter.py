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
import sys
import re
import argparse
import json
import tempfile
import stat
import yaml
from datetime import datetime, timezone

FRONTMATTER_RE = re.compile(r'\A---\s*\r?\n(.*?)(?:\r?\n)?---\s*(?:\r?\n|\Z)', re.DOTALL)

class CustomLoader(yaml.SafeLoader):
    pass

CustomLoader.yaml_implicit_resolvers = {
    key: [r for r in resolvers if r[0] != 'tag:yaml.org,2002:timestamp']
    for key, resolvers in yaml.SafeLoader.yaml_implicit_resolvers.items()
}

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

def needs_double_quotes(s):
    if not isinstance(s, str):
        return False
    # Check empty strings
    if s == "":
        return True
    # Check leading/trailing whitespace
    if s != s.strip():
        return True
    # Check for newline, carriage return, or tab characters
    if '\n' in s or '\r' in s or '\t' in s:
        return True
    # Check for emojis/non-ASCII
    if any(ord(c) > 127 for c in s):
        return True
    # Check for colons, brackets, parentheses, or other special characters
    if re.search(r'[^a-zA-Z0-9_\-\s]', s):
        return True
    # YAML-aware round-trip check to detect values parsed as non-strings
    try:
        parsed = yaml.safe_load(s)
        if not isinstance(parsed, str) or parsed != s:
            return True
    except Exception:
        return True
    return False

def serialise_val(val, key):
    # Format lists as inline arrays with double-quoted strings and recursive non-string serialisation
    if isinstance(val, list):
        formatted_elements = []
        for item in val:
            if isinstance(item, str):
                formatted_elements.append(json.dumps(item, ensure_ascii=False))
            else:
                formatted_elements.append(serialise_val(item, key))
        return "[" + ", ".join(formatted_elements) + "]"

    # Format strings, quoting if they contain emojis/special characters or are YAML-sensitive
    if isinstance(val, str):
        if needs_double_quotes(val):
            return json.dumps(val, ensure_ascii=False)
        else:
            return val

    # Fallback to safe_dump for other types (e.g. ints, floats, booleans)
    dumped = yaml.safe_dump(val, default_flow_style=True, allow_unicode=True).strip()
    if dumped.endswith('\n...'):
        dumped = dumped[:-4]
    elif dumped.endswith('...'):
        dumped = dumped[:-3]
    return dumped.strip()


# ==============================================================================
# Refactored focused helpers for process_file()
# ==============================================================================

def read_file_and_strip_bom(filepath):
    """
    Reads the file as raw bytes to detect if it starts with the UTF-8 BOM.
    Then reads/decodes and removes *all* occurrences of the \ufeff character.
    Returns (clean_content, had_bom).
    """
    had_bom = False
    if os.path.exists(filepath):
        try:
            with open(filepath, 'rb') as bf:
                had_bom = bf.read(3) == b'\xef\xbb\xbf'
        except OSError as e:
            raise OSError(f"Failed to read binary prefix for {filepath}: {e}") from e

    with open(filepath, 'r', encoding='utf-8-sig') as f:
        raw_text = f.read()

    # Strip ALL occurrences of the \ufeff character
    clean_content = raw_text.replace('\ufeff', '')
    return clean_content, had_bom


def parse_frontmatter(content, rel_path):
    """
    Parses consecutive leading frontmatter blocks.
    Raises ValueError on non-mapping blocks or parse failures.
    Returns (existing_frontmatter, rest_of_content).
    """
    existing_frontmatter = {}
    rest_of_content = content

    while True:
        match = FRONTMATTER_RE.match(rest_of_content)
        if not match:
            break
        yaml_block = match.group(1)
        try:
            parsed = yaml.load(yaml_block, Loader=CustomLoader)
            if parsed is None:
                parsed = {}
            if isinstance(parsed, dict):
                existing_frontmatter.update(parsed)
                rest_of_content = rest_of_content[match.end():]
            else:
                raise ValueError(f"Existing frontmatter block in {rel_path} is not a mapping dict.")
        except Exception as e:
            if isinstance(e, ValueError):
                raise e
            raise ValueError(f"Failed to parse existing frontmatter block in {rel_path}: {e}") from e

    return existing_frontmatter, rest_of_content


def normalise_metadata(existing_frontmatter, rest_of_content, rel_path, filename):
    """
    Normalises the mandatory OKF metadata fields and returns updated_frontmatter.
    """
    # 1. okf_version
    okf_version = existing_frontmatter.get('okf_version')
    if okf_version is None or str(okf_version) not in ('0.1', '0.2'):
        okf_version = 0.1
    else:
        try:
            okf_version = float(okf_version)
        except (ValueError, TypeError):
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
        if isinstance(timestamp, str):
            pass
        elif isinstance(timestamp, datetime):
            if timestamp.tzinfo is None:
                timestamp = timestamp.replace(tzinfo=timezone.utc)
            timestamp = timestamp.astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
        else:
            timestamp = str(timestamp)

    # 5. topics
    topics = existing_frontmatter.get('topics')
    if not topics or not isinstance(topics, list):
        topics = get_default_topics(okf_type)

    updated_frontmatter = {
        'okf_version': okf_version,
        'type': okf_type,
        'title': title,
        'timestamp': timestamp,
        'topics': topics
    }

    # Preserve other fields
    for k, v in existing_frontmatter.items():
        if k not in updated_frontmatter:
            if isinstance(v, datetime):
                if v.tzinfo is None:
                    v = v.replace(tzinfo=timezone.utc)
                v = v.astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
            updated_frontmatter[k] = v

    return updated_frontmatter


def serialise_frontmatter(updated_frontmatter, rel_path, filename):
    """
    Serialises the frontmatter keeping the specific order of keys.
    """
    special_reorder = filename == "SKILL.md"
    if special_reorder:
        ordered_keys = ['okf_version', 'type', 'title', 'timestamp', 'description', 'topics']
    else:
        ordered_keys = ['okf_version', 'type', 'title', 'timestamp', 'topics']

    yaml_lines = []
    for k in ordered_keys:
        if k in updated_frontmatter:
            yaml_lines.append(f"{k}: {serialise_val(updated_frontmatter[k], k)}")

    for k, val in updated_frontmatter.items():
        if k not in ordered_keys:
            yaml_lines.append(f"{k}: {serialise_val(val, k)}")

    return "---\n" + "\n".join(yaml_lines) + "\n---\n"


def atomic_replace_file(filepath, new_content, filename):
    """
    Atomically writes new_content to a temporary file, preserves original
    permission mode, and replaces filepath.
    """
    file_dir = os.path.dirname(filepath)
    temp_file = None
    temp_filepath = None
    try:
        temp_file = tempfile.NamedTemporaryFile(
            dir=file_dir, prefix=".temp_", suffix=f"_{filename}",
            mode='w', encoding='utf-8', delete=False
        )
        temp_filepath = temp_file.name
        temp_file.write(new_content)
        temp_file.close()

        # Copy original file permission mode onto temp file
        if os.path.exists(filepath):
            os.chmod(temp_filepath, stat.S_IMODE(os.stat(filepath).st_mode))

        os.replace(temp_filepath, filepath)
    except Exception as e:
        if temp_file is not None:
            try:
                temp_file.close()
            except Exception:
                pass
        if temp_filepath is not None and os.path.exists(temp_filepath):
            try:
                os.remove(temp_filepath)
            except Exception:
                pass
        raise e


# Main process_file implementation
def process_file(filepath, root_dir, *, dry_run=False):
    """
    Orchestrates the compliance flow for a single Markdown file.
    Note: dry_run is keyword-only.
    """
    rel_path = os.path.relpath(filepath, root_dir).replace('\\', '/')
    filename = os.path.basename(filepath)

    # 1. Read file and handle/strip BOM
    clean_content, had_bom = read_file_and_strip_bom(filepath)

    # 2. Parse existing frontmatter blocks
    existing_frontmatter, rest_of_content = parse_frontmatter(clean_content, rel_path)

    # 3. Normalise OKF metadata fields
    updated_frontmatter = normalise_metadata(existing_frontmatter, rest_of_content, rel_path, filename)

    # 4. Serialise frontmatter
    new_frontmatter_block = serialise_frontmatter(updated_frontmatter, rel_path, filename)
    new_content = new_frontmatter_block + rest_of_content

    # 5. Atomic replacement if changed or had BOM
    if new_content != clean_content or had_bom:
        if dry_run:
            return True
        atomic_replace_file(filepath, new_content, filename)
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
    exclude_dirs = {'.git', 'node_modules', '.pytest_cache', '.venv'}

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
            try:
                if process_file(filepath, root_dir):
                    rel = os.path.relpath(filepath, root_dir).replace('\\', '/')
                    print(f"Standardised/Injected OKF: {rel}")
                    modified_count += 1
            except Exception as e:
                print(f"Error processing {filepath}: {e}", file=sys.stderr)
                sys.exit(1)

    print(f"\nScan complete. Total markdown files checked: {total_count}")
    print(f"Total files modified to be OKF-compliant: {modified_count}")

if __name__ == "__main__":
    main()
