import os
import re
import argparse
from datetime import datetime, timezone

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
    return os.path.splitext(filename)[0]

def apply_okf(root_dir):
    timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    modified_count = 0
    
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Exclude directories
        dirnames[:] = [d for d in dirnames if d not in ['.git', 'node_modules', 'scratch']]
        
        for filename in filenames:
            if not filename.endswith('.md'):
                continue
                
            filepath = os.path.join(dirpath, filename)
            rel_path = os.path.relpath(filepath, root_dir).replace('\\', '/')
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
            if content.startswith('---'):
                print(f"Skipping (already has frontmatter): {rel_path}")
                continue
                
            okf_type = get_okf_type(rel_path)
            title = extract_title(content, filename)
            
            frontmatter = f"""---
okf_version: 0.1
type: {okf_type}
title: "{title.replace('"', '')}"
description: "OKF-compliant documentation for {filename}."
resource: "file:///{rel_path}"
timestamp: {timestamp}
---
"""
            
            new_content = frontmatter + content
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
                
            print(f"Applied OKF to: {rel_path}")
            modified_count += 1
            
    print(f"\\nTotal files modified: {modified_count}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Inject OKF frontmatter into Markdown files.")
    parser.add_argument("directory", help="The root directory to scan.")
    args = parser.parse_args()
    apply_okf(args.directory)
