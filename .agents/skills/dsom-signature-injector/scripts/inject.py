#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
import os
import sys
from datetime import datetime


def get_last_modified_date(filepath: str) -> str:
    """Retrieves formatted last modified date for a file.

    Args:
        filepath: Path to the target file.

    Returns:
        Modification date in the local time zone, in YYYY-MM-DD format.

    Raises:
        OSError: If the file's modification time cannot be read.
        OverflowError: If the timestamp is outside the platform's date range.
    """
    timestamp = os.path.getmtime(filepath)
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')


def get_sh_yml_header(date_str: str) -> str:
    """Generates standard DSOM header for Shell, YAML, and Python scripts.

    Args:
        date_str: ISO date string for header timestamp.

    Returns:
        Formatted multi-line comment header string.
    """
    return f"""# ==============================================================================
# Protocol    : Deep State of Mind (DSOM) For My AI
# Author      : Harisfazillah Jamel (LinuxMalaysia)
# Timestamp   : {date_str}
# License     : GNU General Public License v3.0
# Standard    : UK English | DBP-standard Bahasa Melayu Malaysia (Piawai)
# ==============================================================================
"""


def get_ps1_header(date_str: str) -> str:
    """Generates standard DSOM comment block header for PowerShell scripts.

    Args:
        date_str: ISO date string for header timestamp.

    Returns:
        Formatted multi-line PowerShell block comment header string.
    """
    return f"""<#
.SYNOPSIS
    Deep State of Mind (DSOM) For My AI Protocol
.NOTES
    Author    : Harisfazillah Jamel (LinuxMalaysia)
    Timestamp : {date_str}
    License   : GNU General Public License v3.0
    Standard  : UK English | DBP-standard Bahasa Melayu Malaysia (Piawai)
#>
"""


def inject_signature(target_path: str) -> None:
    """Injects DSOM copyright signature headers/footers into target files or directory trees.

    Modifies Markdown, shell, YAML, Python, and PowerShell files using their
    local modification dates. Files containing the full protocol marker are
    skipped. Missing paths and unsupported extensions are left unchanged.
    Write errors are caught and processing continues with the next file.

    Args:
        target_path: Path to target file or directory.

    Raises:
        OSError: If reading a file or its modification time fails.
        OverflowError: If a modification timestamp cannot be converted to a date.
    """
    files_to_process = []
    
    if os.path.isfile(target_path):
        files_to_process.append(target_path)
    elif os.path.isdir(target_path):
        for root, _, files in os.walk(target_path):
            if '.git' in root or '.agents\\brain' in root:
                continue
            for file in files:
                if file.endswith(('.md', '.sh', '.ps1', '.yml', '.yaml', '.py')):
                    files_to_process.append(os.path.join(root, file))
    
    for filepath in files_to_process:
        date_str = get_last_modified_date(filepath)
        
        md_footer = f"\n\n---\n*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | {date_str}*\n*Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*\n"
        
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            
        content = "".join(lines)
        if "Deep State of Mind (DSOM) For My AI Protocol" in content:
            print(f"Skipping {filepath} (Signature already exists)")
            continue
            
        try:
            if filepath.endswith('.md'):
                with open(filepath, 'a', encoding='utf-8') as f:
                    f.write(md_footer)
                print(f"Appended Markdown footer to {filepath}")
            elif filepath.endswith(('.sh', '.yml', '.yaml', '.py')):
                header = get_sh_yml_header(date_str)
                if len(lines) > 0 and (lines[0].startswith("#!") or lines[0].startswith("---")):
                    # Shebang or YAML doc start present, insert after it
                    first_line = lines[0]
                    rest = "".join(lines[1:])
                    new_content = first_line + "\n" + header + rest
                else:
                    new_content = header + content
                    
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Prepended SH/YML header to {filepath}")
            elif filepath.endswith('.ps1'):
                header = get_ps1_header(date_str)
                new_content = header + content
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Prepended PS1 header to {filepath}")
        except Exception as e:
            print(f"Error processing {filepath}: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python inject.py <file_or_directory_path>")
        sys.exit(1)
    
    inject_signature(sys.argv[1])
