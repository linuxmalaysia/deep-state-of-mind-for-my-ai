#!/usr/bin/env python3
# ==============================================================================
# Protocol    : Deep State of Mind (DSOM) For My AI
# Workflow    : Semantic Compaction (DSOM State Sync)
# Author      : Harisfazillah Jamel (LinuxMalaysia)
# Timestamp   : 2026-08-11
# License     : GNU General Public License v3.0
# Standard    : UK English | DBP-standard Bahasa Melayu Malaysia (Piawai)
# Description : Uses Gemini (Antigravity/Jules) to read a PR diff, perform
#               Semantic Compaction, and update the current_state.dsom file.
#               If no APIs are available, falls back to a robust Python-based
#               local Semantic Compaction engine.
# ==============================================================================

import os
import sys
import datetime
import re
import requests
import json
import tempfile
import stat
import yaml
from datetime import timezone

FRONTMATTER_RE = re.compile(r'\A---\s*\r?\n(.*?)(?:\r?\n)?---\s*(?:\r?\n|\Z)', re.DOTALL)

class CustomLoader(yaml.SafeLoader):
    pass

CustomLoader.yaml_implicit_resolvers = {
    key: [r for r in resolvers if r[0] != 'tag:yaml.org,2002:timestamp']
    for key, resolvers in yaml.SafeLoader.yaml_implicit_resolvers.items()
}

def needs_double_quotes(s):
    if not isinstance(s, str):
        return False
    if s == "":
        return True
    if s != s.strip():
        return True
    if '\n' in s or '\r' in s or '\t' in s:
        return True
    if any(ord(c) > 127 for c in s):
        return True
    if re.search(r'[^a-zA-Z0-9_\-\s]', s):
        return True
    try:
        parsed = yaml.safe_load(s)
        if not isinstance(parsed, str) or parsed != s:
            return True
    except Exception:
        return True
    return False

def serialise_val(val, key):
    if isinstance(val, list):
        formatted_elements = []
        for item in val:
            if isinstance(item, str):
                formatted_elements.append(json.dumps(item, ensure_ascii=False))
            else:
                formatted_elements.append(serialise_val(item, key))
        return "[" + ", ".join(formatted_elements) + "]"

    if isinstance(val, str):
        if needs_double_quotes(val):
            return json.dumps(val, ensure_ascii=False)
        else:
            return val

    dumped = yaml.safe_dump(val, default_flow_style=True, allow_unicode=True).strip()
    if dumped.endswith('\n...'):
        dumped = dumped[:-4]
    elif dumped.endswith('...'):
        dumped = dumped[:-3]
    return dumped.strip()

def read_file_and_strip_bom(filepath):
    had_bom = False
    if os.path.exists(filepath):
        try:
            with open(filepath, 'rb') as bf:
                had_bom = bf.read(3) == b'\xef\xbb\xbf'
        except OSError as e:
            raise OSError(f"Failed to read binary prefix for {filepath}: {e}") from e

    with open(filepath, 'r', encoding='utf-8-sig') as f:
        raw_text = f.read()

    clean_content = raw_text.replace('\ufeff', '')
    return clean_content, had_bom

def parse_frontmatter(content, rel_path):
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

def normalise_metadata(existing_frontmatter, rel_path, filename):
    okf_version = existing_frontmatter.get('okf_version', 0.1)
    okf_type = existing_frontmatter.get('type', 'dsom_state')
    title = existing_frontmatter.get('title', "DSOM Current State")
    timestamp = datetime.datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    topics = existing_frontmatter.get('topics', ['state', 'memory', 'compaction'])

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
            updated_frontmatter[k] = v

    return updated_frontmatter

def serialise_frontmatter(updated_frontmatter, filename):
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

def local_compaction(diff_content, rest_of_content):
    """
    Parses the git diff content and updates rest_of_content (markdown body)
    locally, adding the summary to the Condensed History section.
    """
    file_changes = {}
    current_file = None

    for line in diff_content.splitlines():
        match = re.match(r'^diff --git a/(.*) b/(.*)$', line)
        if match:
            current_file = match.group(2)
            file_changes[current_file] = {"added": 0, "deleted": 0}
        elif current_file:
            if line.startswith("+") and not line.startswith("+++"):
                file_changes[current_file]["added"] += 1
            elif line.startswith("-") and not line.startswith("---"):
                file_changes[current_file]["deleted"] += 1

    if not file_changes:
        summary_text = "No code files modified in diff."
    else:
        summary_parts = []
        for f, stats in file_changes.items():
            summary_parts.append(f"{f} (+{stats['added']}, -{stats['deleted']})")
        summary_text = f"Modified files: {', '.join(summary_parts)}."

    # Insert into ## Condensed History or ## Active State
    target_heading = "## Condensed History"
    if target_heading in rest_of_content:
        parts = rest_of_content.split(target_heading, 1)
        lines = parts[1].splitlines()

        insert_idx = 0
        for idx, l in enumerate(lines):
            if l.strip().startswith("-") or l.strip() == "":
                insert_idx = idx
                if l.strip().startswith("-"):
                    break

        new_bullet = f"- [Auto-Sync] {summary_text}"
        lines.insert(insert_idx, new_bullet)

        updated_body = parts[0] + target_heading + "\n" + "\n".join(lines)
    else:
        # Fallback to appending at the end of the file
        updated_body = rest_of_content.strip() + f"\n\n## Condensed History\n- [Auto-Sync] {summary_text}\n"

    return updated_body

def main():
    if len(sys.argv) != 3:
        print("Usage: action_update_dsom.py <pr_diff_file> <dsom_state_file>")
        sys.exit(1)

    diff_file = sys.argv[1]
    state_file = sys.argv[2]

    # Read diff file
    with open(diff_file, "r", encoding="utf-8") as f:
        diff_content = f.read()

    # Read state file and strip BOM
    if not os.path.exists(state_file):
        print(f"Error: DSOM state file {state_file} does not exist.")
        sys.exit(1)

    clean_state, had_bom = read_file_and_strip_bom(state_file)
    existing_frontmatter, rest_of_content = parse_frontmatter(clean_state, os.path.basename(state_file))

    # Detect the agent persona to use
    active_agent = os.environ.get("ACTIVE_AGENT", "Jules")
    print(f"Active Agent context detected: {active_agent}")

    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    new_state_body = None

    if api_key:
        print(f"API key detected. Directing Semantic Compaction via {active_agent} AI API...")

        if active_agent.lower() == "antigravity":
            system_prompt = (
                "You are Google Antigravity, a Tier-1 Cognitive Digital Twin assisting LinuxMalaysia in the DSOM framework.\n"
                "Your task is to perform Semantic Compaction on a Pull Request diff.\n"
                "You will be given the current `current_state.dsom` file and a Pull Request diff.\n"
                "Analyze the diff and update the `current_state.dsom` file to reflect any new "
                "architectural decisions, major features, or state changes.\n"
                "- Keep the output strictly in the OKF v0.1 format.\n"
                "- Do not add verbose conversational fluff. Only output the updated file content.\n"
                "- Do not wrap the output in markdown code blocks, just return the raw text."
            )
        else:
            system_prompt = (
                "You are Google Jules, a Tier-1 Cognitive Digital Twin assisting LinuxMalaysia in the DSOM framework.\n"
                "Your task is to perform Semantic Compaction on a Pull Request diff.\n"
                "You will be given the current `current_state.dsom` file and a Pull Request diff.\n"
                "Analyze the diff and update the `current_state.dsom` file to reflect any new "
                "architectural decisions, major features, or state changes.\n"
                "- Keep the output strictly in the OKF v0.1 format.\n"
                "- Do not add verbose conversational fluff. Only output the updated file content.\n"
                "- Do not wrap the output in markdown code blocks, just return the raw text."
            )

        user_prompt = f"Current DSOM State:\n{clean_state}\n\nPull Request Diff:\n{diff_content}"

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        headers = {'Content-Type': 'application/json'}
        payload = {
            "contents": [{
                "role": "user",
                "parts": [
                    {"text": f"{system_prompt}\n\n{user_prompt}"}
                ]
            }],
            "generationConfig": {
                "temperature": 0.2
            }
        }

        try:
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            response.raise_for_status()
            res_json = response.json()

            ai_text = res_json['candidates'][0]['content']['parts'][0]['text'].strip()

            # Extract response text if wrapped in markdown blocks
            if ai_text.startswith("```"):
                lines = ai_text.splitlines()
                if lines[0].startswith("```"):
                    lines = lines[1:]
                if lines[-1].startswith("```"):
                    lines = lines[:-1]
                ai_text = "\n".join(lines).strip()

            # Parse response frontmatter and body
            _, new_state_body = parse_frontmatter(ai_text, os.path.basename(state_file))
            print("Successfully processed semantic compaction using AI API.")
        except Exception as e:
            print(f"Warning: Failed to call Gemini API ({e}). Falling back to local semantic compaction.")
            new_state_body = None

    if new_state_body is None:
        print("Using local command-line engine to perform automated Semantic Compaction...")
        new_state_body = local_compaction(diff_content, rest_of_content)

    # Normalise metadata and update timestamp
    updated_frontmatter = normalise_metadata(existing_frontmatter, os.path.basename(state_file), os.path.basename(state_file))
    
    # Reassemble OKF v0.1 compliant content
    new_frontmatter_block = serialise_frontmatter(updated_frontmatter, os.path.basename(state_file))
    final_content = new_frontmatter_block + new_state_body.strip() + "\n"

    # Save atomically
    atomic_replace_file(state_file, final_content, os.path.basename(state_file))
    print(f"Successfully updated {state_file}")

if __name__ == "__main__":
    main()
