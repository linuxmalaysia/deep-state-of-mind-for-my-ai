#!/usr/bin/env python3

# ==============================================================================
# Protocol    : Deep State of Mind (DSOM) For My AI
# Author      : Harisfazillah Jamel (LinuxMalaysia)
# Timestamp   : 2026-09-06
# License     : GNU General Public License v3.0
# Standard    : UK English | DBP-standard Bahasa Melayu Malaysia (Piawai)
# ==============================================================================
"""
OKF Frontmatter Compliance Script.
Scans a target directory and ensures all .md files use OKF YAML frontmatter.
The strict mode rejects incomplete or malformed OKF v0.2 trust metadata.
"""
import argparse
import json
import os
import re
import stat
import sys
import tempfile
from datetime import datetime, timezone
from urllib.parse import urlparse

import yaml

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
        return 'skill'
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
        'skill': ['dsom', 'skill', 'agent'],
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
    """Return a YAML value, using flow syntax for lists and dictionaries.

    List strings are always double-quoted; other strings are quoted as needed
    to preserve their value. Dictionary keys are emitted verbatim and must
    already be safe as unquoted YAML keys. The key argument does not affect
    formatting. Cyclic lists and dictionaries are unsupported.

    Raises:
        yaml.representer.RepresenterError: If a fallback value cannot be
            represented by PyYAML's safe dumper.
        RecursionError: If nested lists or dictionaries exceed the recursion limit.
    """
    # Format lists as inline arrays with double-quoted strings and recursive non-string serialisation
    if isinstance(val, list):
        formatted_elements = []
        for item in val:
            if isinstance(item, str):
                formatted_elements.append(json.dumps(item, ensure_ascii=False))
            else:
                formatted_elements.append(serialise_val(item, key))
        return "[" + ", ".join(formatted_elements) + "]"

    # Format dicts as inline flow maps
    if isinstance(val, dict):
        pairs = [f"{k}: {serialise_val(v, k)}" for k, v in val.items()]
        return "{" + ", ".join(pairs) + "}"

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


def normalise_metadata(
    existing_frontmatter,
    rest_of_content,
    rel_path,
    filename,
    *,
    require_okf_v02=False,
    filepath=None,
):
    """Return normalized OKF metadata without modifying the input mapping.

    Missing core fields receive defaults, including the current UTC timestamp.
    Source strings become mappings, source mappings receive missing reference
    fields, and other source entries are dropped. Local source references receive
    URLs under this repository's main branch. When present, generated metadata
    is reduced to by and timestamp fields, accepting at as a timestamp fallback.
    stale_after values are reduced to date text without checking date validity.
    Other fields are preserved, with datetime values converted to UTC text.

    Args:
        existing_frontmatter: Parsed metadata to normalize.
        rest_of_content: Markdown body used to derive a missing title.
        rel_path: Relative document path used for defaults and error messages.
        filename: Filename used when the body has no title heading.
        require_okf_v02: Reject conflicting versions and invalid status values.
            Full trust validation requires validate_okf_v02_metadata afterward.
            Otherwise, an invalid status is replaced with stable.
        filepath: Optional file path used to identify skills and derive their
            name from the parent directory, even when rel_path omits .agents/skills.

    Raises:
        ValueError: In strict mode, an existing non-null version differs from
            0.2, or a supplied status is not draft, stable, or deprecated.
    """
    # 1. okf_version
    okf_version = existing_frontmatter.get('okf_version')
    if require_okf_v02 and okf_version is not None and str(okf_version) != '0.2':
        raise ValueError(f"OKF v0.2 validation failed for {rel_path}: okf_version must be 0.2.")
    if require_okf_v02 or okf_version is None or str(okf_version) in ('0.1', '0.2'):
        okf_version = 0.2
    else:
        try:
            okf_version = float(okf_version)
        except (ValueError, TypeError):
            okf_version = 0.2

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

    # 6. resource
    resource = existing_frontmatter.get('resource')
    if not resource:
        resource = f"/{rel_path}"

    # 7. sources
    sources = existing_frontmatter.get('sources')
    if not sources or not isinstance(sources, list):
        sources = [
            {
                'id': 'dsom-core-spec',
                'title': 'Deep State of Mind (DSOM) Governance Architecture',
                'resource': '/docs/governance/DSOM-TRI-PHASIC-COGNITIVE-ARCHITECTURE.md',
                'url': 'https://github.com/linuxmalaysia/deep-state-of-mind-for-my-ai/blob/main/docs/governance/DSOM-TRI-PHASIC-COGNITIVE-ARCHITECTURE.md',
                'type': 'architecture_spec',
                'author': 'Harisfazillah Jamel (LinuxMalaysia)'
            },
            {
                'id': 'google-okf-v02-spec',
                'title': 'Google Cloud Open Knowledge Format (OKF) v0.2 Specification',
                'resource': 'https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md',
                'url': 'https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md',
                'type': 'external_spec',
                'author': 'Google Cloud Platform'
            }
        ]
    else:
        normalized_sources = []
        for idx, src in enumerate(sources):
            if isinstance(src, dict):
                src_copy = dict(src)
                if 'resource' not in src_copy and 'path' in src_copy:
                    src_copy['resource'] = src_copy['path']
                if 'resource' not in src_copy and 'url' in src_copy:
                    src_copy['resource'] = src_copy['url']
                if 'url' not in src_copy and 'resource' in src_copy:
                    res = str(src_copy['resource'])
                    if res.startswith('http://') or res.startswith('https://'):
                        src_copy['url'] = res
                    else:
                        src_copy['url'] = f"https://github.com/linuxmalaysia/deep-state-of-mind-for-my-ai/blob/main/{res.lstrip('/')}"
                if 'author' not in src_copy:
                    res = str(src_copy.get('resource', ''))
                    if not (res.startswith('http://') or res.startswith('https://')):
                        src_copy['author'] = 'Harisfazillah Jamel (LinuxMalaysia)'
                if 'id' not in src_copy:
                    src_copy['id'] = f"source-{idx+1}"
                if 'title' not in src_copy:
                    src_copy['title'] = str(src_copy.get('resource', 'Source Reference'))
                normalized_sources.append(src_copy)
            elif isinstance(src, str):
                res = src
                is_ext = res.startswith('http://') or res.startswith('https://')
                url_val = res if is_ext else f"https://github.com/linuxmalaysia/deep-state-of-mind-for-my-ai/blob/main/{res.lstrip('/')}"
                src_dict = {
                    'id': f"source-{idx+1}",
                    'title': res,
                    'resource': res,
                    'url': url_val,
                    'type': 'external_spec' if is_ext else 'repository_file',
                }
                if not is_ext:
                    src_dict['author'] = 'Harisfazillah Jamel (LinuxMalaysia)'
                normalized_sources.append(src_dict)
        sources = normalized_sources

    updated_frontmatter = {
        'okf_version': okf_version,
        'type': okf_type,
        'title': title,
        'timestamp': timestamp,
        'topics': topics,
        'resource': resource,
        'sources': sources,
    }

    # 8. status (if present, normalise or validate)
    if 'status' in existing_frontmatter:
        status = existing_frontmatter['status']
        if not isinstance(status, str) or status not in {'draft', 'stable', 'deprecated'}:
            if require_okf_v02:
                raise ValueError(
                    f"OKF v0.2 validation failed for {rel_path}: "
                    f"status must be draft, stable, or deprecated (got: {status})."
                )
            status = 'stable'
        updated_frontmatter['status'] = status

    # 9. generated (if present, normalise)
    if 'generated' in existing_frontmatter:
        generated = existing_frontmatter['generated']
        if not isinstance(generated, dict):
            by_val = str(generated) if generated is not None else 'agent/dsom-subagent-01'
            generated = {
                'by': by_val,
                'timestamp': timestamp
            }
        else:
            gen_by = generated.get('by')
            if not isinstance(gen_by, str) or not gen_by.strip():
                gen_by = 'agent/dsom-subagent-01'
            gen_ts = generated.get('timestamp') or generated.get('at') or timestamp
            if isinstance(gen_ts, datetime):
                if gen_ts.tzinfo is None:
                    gen_ts = gen_ts.replace(tzinfo=timezone.utc)
                gen_ts = gen_ts.astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
            elif not isinstance(gen_ts, str):
                gen_ts = timestamp
            generated = {
                'by': gen_by,
                'timestamp': gen_ts
            }
        updated_frontmatter['generated'] = generated

    # 10. stale_after (if present, normalise)
    if 'stale_after' in existing_frontmatter:
        stale_after = existing_frontmatter['stale_after']
        if isinstance(stale_after, datetime):
            stale_after = stale_after.strftime('%Y-%m-%d')
        else:
            stale_after_str = str(stale_after).strip()
            if 'T' in stale_after_str:
                stale_after_str = stale_after_str.split('T')[0]
            stale_after = stale_after_str
        updated_frontmatter['stale_after'] = stale_after

    if 'spec_version' in existing_frontmatter:
        updated_frontmatter['spec_version'] = str(existing_frontmatter['spec_version'])
    else:
        updated_frontmatter['spec_version'] = '0.2'

    # Always derive 'name' and Lola packaging fields for skill files under .agents/skills or SKILL.md
    if filename == "SKILL.md" or ".agents/skills/" in rel_path or (filepath and ".agents/skills" in filepath.replace('\\', '/')):
        if filepath:
            name = os.path.basename(os.path.dirname(os.path.abspath(filepath)))
        else:
            parts = rel_path.split('/')
            if len(parts) >= 2:
                name = parts[-2]
            else:
                name = os.path.basename(os.path.dirname(os.path.abspath(rel_path)))
        if name:
            updated_frontmatter['name'] = name

        if 'version' not in existing_frontmatter:
            updated_frontmatter['version'] = '1.0.0'
        else:
            updated_frontmatter['version'] = str(existing_frontmatter['version'])

        if 'author' not in existing_frontmatter:
            updated_frontmatter['author'] = 'Harisfazillah Jamel (LinuxMalaysia)'

        if 'license' not in existing_frontmatter:
            updated_frontmatter['license'] = 'GPL-3.0-or-later'

        if 'status' not in updated_frontmatter:
            updated_frontmatter['status'] = 'stable'

        if 'stale_after' not in updated_frontmatter:
            updated_frontmatter['stale_after'] = '2027-10-01'

    # Preserve other fields
    for k, v in existing_frontmatter.items():
        if k not in updated_frontmatter:
            if isinstance(v, datetime):
                if v.tzinfo is None:
                    v = v.replace(tzinfo=timezone.utc)
                v = v.astimezone(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
            updated_frontmatter[k] = v

    if require_okf_v02:
        spec_version = existing_frontmatter.get('spec_version')
        if spec_version is not None and str(spec_version) != '0.2':
            raise ValueError(f"OKF v0.2 validation failed for {rel_path}: spec_version must be 0.2.")
        updated_frontmatter['spec_version'] = '0.2'

    return updated_frontmatter


def validate_okf_v02_metadata(metadata, rel_path):
    """Reject incomplete or malformed OKF v0.2 trust metadata.

    Check version fields, a snake_case concept_id, status, a YYYY-MM-DD
    stale_after date, nonempty sources, and generated metadata. Source mappings
    require nonempty id, title, author, and absolute URL strings. generated.by
    must be nonempty, and its timestamp must parse with a zero UTC offset.
    generated.at is accepted when generated.timestamp is absent or falsey.
    Dates are checked for format and validity, not freshness.

    Return None on success without modifying metadata. rel_path identifies
    the document in error messages.

    Raises:
        ValueError: A required trust field is missing or invalid, including
            source URLs rejected by the URL parser.
    """
    required_fields = (
        'okf_version',
        'spec_version',
        'concept_id',
        'status',
        'stale_after',
        'sources',
        'generated',
    )
    missing = [field for field in required_fields if field not in metadata]
    if missing:
        fields = ', '.join(missing)
        raise ValueError(f"OKF v0.2 validation failed for {rel_path}: missing fields: {fields}.")

    if str(metadata['okf_version']) != '0.2':
        raise ValueError(f"OKF v0.2 validation failed for {rel_path}: okf_version must be 0.2.")
    if str(metadata['spec_version']) != '0.2':
        raise ValueError(f"OKF v0.2 validation failed for {rel_path}: spec_version must be 0.2.")

    concept_id = metadata['concept_id']
    if not isinstance(concept_id, str) or not re.fullmatch(r'[a-z][a-z0-9]*(?:_[a-z0-9]+)*', concept_id):
        raise ValueError(
            f"OKF v0.2 validation failed for {rel_path}: concept_id must use snake_case."
        )

    status = metadata['status']
    if not isinstance(status, str) or status not in {'draft', 'stable', 'deprecated'}:
        raise ValueError(
            f"OKF v0.2 validation failed for {rel_path}: status must be draft, stable, or deprecated."
        )

    stale_after = metadata['stale_after']
    try:
        parsed_stale_after = datetime.strptime(stale_after, '%Y-%m-%d')
    except (TypeError, ValueError) as exc:
        raise ValueError(
            f"OKF v0.2 validation failed for {rel_path}: stale_after must use YYYY-MM-DD."
        ) from exc
    if parsed_stale_after.strftime('%Y-%m-%d') != stale_after:
        raise ValueError(
            f"OKF v0.2 validation failed for {rel_path}: stale_after must use YYYY-MM-DD."
        )

    sources = metadata['sources']
    if not isinstance(sources, list) or not sources:
        raise ValueError(
            f"OKF v0.2 validation failed for {rel_path}: sources must be a non-empty list."
        )
    for index, source in enumerate(sources):
        if not isinstance(source, dict):
            raise ValueError(
                f"OKF v0.2 validation failed for {rel_path}: sources[{index}] must be a mapping."
            )
        for field in ('id', 'title', 'author', 'url'):
            value = source.get(field)
            if not isinstance(value, str) or not value.strip():
                raise ValueError(
                    f"OKF v0.2 validation failed for {rel_path}: "
                    f"sources[{index}].{field} must be a non-empty string."
                )
        source_url = urlparse(source['url'])
        if not source_url.scheme or (
            source_url.scheme in {'http', 'https'} and not source_url.netloc
        ):
            raise ValueError(
                f"OKF v0.2 validation failed for {rel_path}: "
                f"sources[{index}].url must be an absolute URL."
            )

    generated = metadata['generated']
    if not isinstance(generated, dict):
        raise ValueError(
            f"OKF v0.2 validation failed for {rel_path}: generated must be a mapping."
        )
    generated_by = generated.get('by')
    if not isinstance(generated_by, str) or not generated_by.strip():
        raise ValueError(
            f"OKF v0.2 validation failed for {rel_path}: generated.by must be a non-empty string."
        )
    generated_timestamp = metadata['generated'].get('timestamp') or metadata['generated'].get('at')
    if not isinstance(generated_timestamp, str):
        raise ValueError(
            f"OKF v0.2 validation failed for {rel_path}: generated.timestamp must be an ISO 8601 UTC string."
        )
    try:
        parsed_timestamp = datetime.fromisoformat(generated_timestamp.replace('Z', '+00:00'))
    except ValueError as exc:
        raise ValueError(
            f"OKF v0.2 validation failed for {rel_path}: generated.timestamp must be an ISO 8601 UTC string."
        ) from exc
    utc_offset = parsed_timestamp.utcoffset()
    if parsed_timestamp.tzinfo is None or utc_offset is None or utc_offset.total_seconds() != 0:
        raise ValueError(
            f"OKF v0.2 validation failed for {rel_path}: generated.timestamp must be an ISO 8601 UTC string."
        )


def serialise_frontmatter(updated_frontmatter, rel_path, filename):
    """
    Serialises the frontmatter keeping the specific order of keys.
    """
    special_reorder = filename == "SKILL.md"
    if special_reorder:
        ordered_keys = [
            'name',
            'version',
            'description',
            'author',
            'license',
            'okf_version',
            'type',
            'topics',
            'status',
            'stale_after',
            'title',
            'timestamp',
        ]
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
def process_file(filepath, root_dir, *, dry_run=False, require_okf_v02=False):
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
    updated_frontmatter = normalise_metadata(
        existing_frontmatter,
        rest_of_content,
        rel_path,
        filename,
        require_okf_v02=require_okf_v02,
        filepath=filepath,
    )
    if require_okf_v02:
        validate_okf_v02_metadata(updated_frontmatter, rel_path)

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
    parser = argparse.ArgumentParser(description="Ensure OKF compliance on all Markdown files.")
    parser.add_argument("directory", nargs="?", default=".", help="Root directory to scan (default: '.')")
    parser.add_argument(
        "--require-okf-v02",
        action="store_true",
        help="Reject Markdown files without complete, valid OKF v0.2 trust metadata.",
    )
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
                if process_file(filepath, root_dir, require_okf_v02=args.require_okf_v02):
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
