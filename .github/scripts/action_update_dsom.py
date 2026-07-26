#!/usr/bin/env python3
# ==============================================================================
# Protocol    : Deep State of Mind (DSOM) For My AI
# Workflow    : Semantic Compaction (DSOM State Sync)
# Author      : Harisfazillah Jamel (LinuxMalaysia)
# Timestamp   : 2026-07-27
# Description : Uses OpenAI to read a PR diff, perform Semantic Compaction,
#               and update the current_state.dsom file.
# ==============================================================================

import os
import sys
import datetime
from openai import OpenAI

def main():
    if len(sys.argv) != 3:
        print("Usage: action_update_dsom.py <pr_diff_file> <dsom_state_file>")
        sys.exit(1)

    diff_file = sys.argv[1]
    state_file = sys.argv[2]

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable is not set.")
        sys.exit(1)

    with open(diff_file, "r", encoding="utf-8") as f:
        diff_content = f.read()

    if not os.path.exists(state_file):
        print(f"Error: DSOM state file {state_file} does not exist.")
        sys.exit(1)

    with open(state_file, "r", encoding="utf-8") as f:
        current_state = f.read()

    client = OpenAI(api_key=api_key)

    system_prompt = (
        "You are the DSOM Cognitive Engine. Your task is to perform Semantic Compaction.\n"
        "You will be given the current `current_state.dsom` file and a Pull Request diff.\n"
        "Analyze the diff and update the `current_state.dsom` file to reflect any new "
        "architectural decisions, major features, or state changes.\n"
        "- Keep the output strictly in the OKF v0.1 format.\n"
        "- Update the timestamp in the YAML frontmatter to the current date.\n"
        "- Do not add verbose conversational fluff. Only output the updated file content.\n"
        "- Do not wrap the output in markdown code blocks, just return the raw text."
    )

    user_prompt = f"Current DSOM State:\n{current_state}\n\nPull Request Diff:\n{diff_content}"

    print("Sending request to OpenAI for Semantic Compaction...")
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.2
    )

    new_state = response.choices[0].message.content.strip()

    # Sometimes the model still outputs markdown blocks, strip them if present.
    if new_state.startswith("```"):
        lines = new_state.splitlines()
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines[-1].startswith("```"):
            lines = lines[:-1]
        new_state = "\n".join(lines)

    # Make sure we update the timestamp in python to be safe
    now_str = datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")
    
    with open(state_file, "w", encoding="utf-8") as f:
        f.write(new_state)

    print(f"Successfully updated {state_file}")

if __name__ == "__main__":
    main()
