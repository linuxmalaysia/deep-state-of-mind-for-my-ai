import os
import sys
import glob
from datetime import datetime

def get_last_modified_date(filepath):
    timestamp = os.path.getmtime(filepath)
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d')

def inject_signature(target_path):
    files_to_process = []
    
    if os.path.isfile(target_path):
        files_to_process.append(target_path)
    elif os.path.isdir(target_path):
        for root, _, files in os.walk(target_path):
            if '.git' in root or '.agents\\brain' in root:
                continue
            for file in files:
                if file.endswith(('.md', '.sh', '.ps1', '.yml', '.yaml')):
                    files_to_process.append(os.path.join(root, file))
    
    for filepath in files_to_process:
        date_str = get_last_modified_date(filepath)
        
        md_footer = f"\n\n---\n*Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | {date_str}*\n*Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0*\n"
        code_header = f"# Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel (LinuxMalaysia) | {date_str}\n# Standard: UK English | DBP-standard Bahasa Melayu Malaysia (Piawai) | GNU General Public License v3.0\n\n"
        
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        if "Deep State of Mind (DSOM) For My AI Protocol | Harisfazillah Jamel" in content:
            print(f"Skipping {filepath} (Signature already exists)")
            continue
            
        try:
            if filepath.endswith('.md'):
                with open(filepath, 'a', encoding='utf-8') as f:
                    f.write(md_footer)
                print(f"Appended Markdown footer to {filepath}")
            elif filepath.endswith(('.sh', '.ps1', '.yml', '.yaml')):
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(code_header + content)
                print(f"Prepended code header to {filepath}")
        except Exception as e:
            print(f"Error processing {filepath}: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python inject.py <file_or_directory_path>")
        sys.exit(1)
    
    inject_signature(sys.argv[1])
