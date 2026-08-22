#!/usr/bin/env python3
"""
Mintlify MDX Documentation Builder for DSOM.
Translates sovereign Markdown (.md) documents and OKF frontmatter in docs/ and .agents/
into clean Mintlify MDX (.mdx) pages and dynamically generates docs-source/docs.json.

Standard: User Manual Site Style -> Mintlify MDX Specification
Author  : Harisfazillah Jamel (LinuxMalaysia)
License : GNU General Public License v3.0
"""

import json
import os
import re
import shutil
import sys
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

FRONTMATTER_RE = re.compile(r"\A---\s*\r?\n(.*?)(?:\r?\n)?---\s*\r?\n", re.DOTALL)


def to_title_case_sidebar(text: str) -> str:
    """Generate 1-3 word Title Case sidebarTitle from title or filename."""
    cleaned = re.sub(r"(?i)\b(dsom|the|for my ai|guide|specification|protocol|mandate|blueprint)\b", "", text)
    cleaned = re.sub(r"[^a-zA-Z0-9\s]", " ", cleaned).strip()
    words = cleaned.split()
    if not words:
        words = text.split()[:2]
    selected = words[:3]
    return " ".join(w.capitalize() for w in selected)


def parse_frontmatter_and_content(content: str):
    """Extract frontmatter and body, synthesizing required SEO title, sidebarTitle, and description."""
    match = FRONTMATTER_RE.match(content)
    title = None
    sidebar_title = None
    description = None

    if match:
        fm_block = match.group(1)
        body = content[match.end():]
        for line in fm_block.splitlines():
            line = line.strip()
            if line.startswith("title:"):
                title = line.split("title:", 1)[1].strip().strip('"').strip("'")
            elif line.startswith("sidebarTitle:"):
                sidebar_title = line.split("sidebarTitle:", 1)[1].strip().strip('"').strip("'")
            elif line.startswith("description:"):
                description = line.split("description:", 1)[1].strip().strip('"').strip("'")
    else:
        body = content

    if not title:
        for line in body.splitlines():
            line = line.strip()
            if line.startswith("# "):
                title = line[2:].strip().strip('"')
                break

    if not title:
        title = "DSOM Documentation"

    if not sidebar_title:
        sidebar_title = to_title_case_sidebar(title)

    if not description:
        for para in body.split("\n\n"):
            p = para.strip()
            if p and not p.startswith("#") and not p.startswith("---") and not p.startswith("```") and not p.startswith(">") and not p.startswith("["):
                clean_p = re.sub(r"[\[\]\*\_\`]", "", p).replace("\n", " ").strip()
                if len(clean_p) > 20:
                    description = clean_p[:150].strip()
                    break

    if not description:
        description = f"Official documentation and operational guidance for {title} within the DSOM protocol."

    if len(description) > 155:
        description = description[:152].rstrip() + "..."
    while len(description) < 130:
        description += " Deep State of Mind framework."
    if len(description) > 155:
        description = description[:152].rstrip() + "..."

    title = title.replace("—", "-").replace("–", "-")
    sidebar_title = sidebar_title.replace("—", "-").replace("–", "-")
    description = description.replace("—", "-").replace("–", "-")

    return title, sidebar_title, description, body


def convert_markdown_to_mdx(md_text: str) -> str:
    """Convert standard markdown text into Mintlify MDX compatible format following User Manual style."""
    title, sidebar_title, description, body = parse_frontmatter_and_content(md_text)

    body_lines = body.strip().splitlines()
    if body_lines and (body_lines[0].strip() == f"# {title}" or body_lines[0].strip().startswith("# ")):
        body_lines = body_lines[1:]
    clean_body = "\n".join(body_lines).strip()

    clean_body = re.sub(r"\[([^\]]+)\]\((?!http|mailto|#)([^\)]+?)\.md([#\)][^\)]*)?\)", r"[\1](\2\3)", clean_body)
    clean_body = re.sub(r"\]\((?:\.\./)*images/", "](/images/", clean_body)
    clean_body = re.sub(r"\]\(docs/images/", "](/images/", clean_body)
    clean_body = clean_body.replace(" — ", ", ").replace(" – ", ", ")

    esc_title = title.replace('"', '\"')
    esc_sidebar = sidebar_title.replace('"', '\"')
    esc_desc = description.replace('"', '\"')

    mdx_frontmatter = "---\n" + f'title: "{esc_title}"\n' + f'sidebarTitle: "{esc_sidebar}"\n' + f'description: "{esc_desc}"\n' + "---\n\n"
    return mdx_frontmatter + clean_body + "\n"


def build_mintlify_tree(repo_root: Path, target_dir: Path):
    """Build MDX pages and docs.json navigation index following User Manual site rules."""
    print("=" * 60)
    print("🔨 [MINTLIFY BUILDER] Compiling Sovereign Markdown Palace to MDX...")

    docs_dir = repo_root / "docs"
    agents_dir = repo_root / ".agents"

    target_dir.mkdir(parents=True, exist_ok=True)

    categories = {
        "Get Started": [],
        "Tutorials": [],
        "How-To": [],
        "Rituals": [],
        "Skills": [],
        "Reference": [],
        "Explanation": [],
        "Governance": []
    }

    def add_page(category, rel_path, source_file):
        if not source_file.exists():
            return
        md_text = source_file.read_text(encoding="utf-8", errors="replace")
        mdx_content = convert_markdown_to_mdx(md_text)
        title, sidebar_title, _, _ = parse_frontmatter_and_content(md_text)

        out_file = target_dir / f"{rel_path}.mdx"
        out_file.parent.mkdir(parents=True, exist_ok=True)
        out_file.write_text(mdx_content, encoding="utf-8")

        categories[category].append((sidebar_title, rel_path.as_posix()))

    # 1. Get Started & Core Pages
    add_page("Get Started", Path("quickstart"), docs_dir / "START-HERE.md")
    add_page("Get Started", Path("core-concepts"), docs_dir / "README.md")
    add_page("Governance", Path("security"), docs_dir / "SECURITY.md")
    add_page("Governance", Path("legal-notice"), docs_dir / "LEGAL-NOTICE.md")
    add_page("Governance", Path("AGENTS"), repo_root / "AGENTS.md")

    # 2. Tutorials
    tutorials_dir = docs_dir / "tutorials"
    if tutorials_dir.exists():
        for md_file in sorted(tutorials_dir.glob("*.md")):
            slug = f"tutorials/{md_file.stem.lower()}"
            add_page("Tutorials", Path(slug), md_file)

    # 3. How-To
    howto_dir = docs_dir / "how-to"
    if howto_dir.exists():
        for md_file in sorted(howto_dir.glob("*.md")):
            slug = f"how-to/{md_file.stem.lower()}"
            add_page("How-To", Path(slug), md_file)

    # 4. Rituals
    add_page("Rituals", Path("rituals/start-of-day"), docs_dir / "SOD-RITUAL.md")
    add_page("Rituals", Path("rituals/end-of-day"), docs_dir / "EOD-RITUAL.md")
    add_page("Rituals", Path("rituals/transition-ritual"), docs_dir / "RITUAL-OF-TRANSITION.md")
    add_page("Rituals", Path("rituals/human-handover"), docs_dir / "HUMAN-HANDOVER-CONTEXT.md")

    # 5. Skills
    skills_dir = agents_dir / "skills"
    if skills_dir.exists():
        for skill_folder in sorted(skills_dir.iterdir()):
            if skill_folder.is_dir():
                skill_md = skill_folder / "SKILL.md"
                if skill_md.exists():
                    slug = f"skills/{skill_folder.name}"
                    add_page("Skills", Path(slug), skill_md)

    # 6. Reference
    ref_dir = docs_dir / "reference"
    if ref_dir.exists():
        for md_file in sorted(ref_dir.glob("*.md")):
            slug = f"reference/{md_file.stem.lower()}"
            add_page("Reference", Path(slug), md_file)

    tools_dir = docs_dir / "tools"
    if tools_dir.exists():
        for md_file in sorted(tools_dir.glob("*.md")):
            slug = f"tools/{md_file.stem.lower()}"
            add_page("Reference", Path(slug), md_file)

    # 7. Explanation
    expl_dir = docs_dir / "explanation"
    if expl_dir.exists():
        for md_file in sorted(expl_dir.glob("*.md")):
            slug = f"explanation/{md_file.stem.lower()}"
            add_page("Explanation", Path(slug), md_file)

    # 8. Governance
    gov_dir = docs_dir / "governance"
    if gov_dir.exists():
        for md_file in sorted(gov_dir.glob("*.md")):
            slug = f"governance/{md_file.stem.lower()}"
            add_page("Governance", Path(slug), md_file)

    # Landing page (index.mdx)
    index_mdx = target_dir / "index.mdx"
    index_content = r'''---
title: "DSOM - Deep State of Mind: AI Governance Framework"
sidebarTitle: "Home"
description: "Deep State of Mind (DSOM) eliminates AI context decay by persisting your project brain in Git, giving any AI model perfect memory across every session."
---

DSOM is a metacognitive governance framework that transforms any AI model into a disciplined Cognitive Digital Twin. By storing your project working context in Git, DSOM ensures your AI maintains memory across sessions and follows deterministic rules.

<CardGroup cols={2}>
  <Card title="Quickstart" icon="rocket" href="/quickstart">
    Set up DSOM in your project in six steps, clone, initialise, and configure your Identity Card.
  </Card>
  <Card title="Core Concepts" icon="brain" href="/core-concepts">
    Understand the Three-Pillar model, the AI brain artifacts, and sovereign spatial memory.
  </Card>
  <Card title="Daily Rituals" icon="sun" href="/rituals/start-of-day">
    Master the Start-of-Day and End-of-Day rituals keeping your AI synchronised with your project state.
  </Card>
  <Card title="Agent Skills" icon="toolbox" href="/skills/agent-plugin-packager">
    Discover OKF-compliant standard operating procedures and portable Agent Plugins.
  </Card>
</CardGroup>

## Onboarding Steps

<Steps>
  <Step title="Clone or Scaffold">
    Use `dsom-project-cloner` or clone the repository to establish the 6-pillar footprint.
  </Step>
  <Step title="Initialize Memory">
    Run `.\tools\init-brain.ps1` or `bash tools/init-brain.sh` to scaffold your active spatial memory.
  </Step>
  <Step title="Verify Guardrails">
    Install pre-commit hooks with `uv run python tools/install_git_guardrails.py` to enforce safety.
  </Step>
  <Step title="Execute SOD Ritual">
    Run `.\tools\reanimate.ps1` at the beginning of each session to load context.
  </Step>
</Steps>
'''
    index_mdx.write_text(index_content, encoding="utf-8")

    tabs_config = [
        {
            "tab": "Documentation",
            "groups": [
                {
                    "group": "Get Started",
                    "pages": ["index"] + [p[1] for p in categories["Get Started"]]
                },
                {
                    "group": "Tutorials",
                    "pages": [p[1] for p in categories["Tutorials"]]
                },
                {
                    "group": "How-To",
                    "pages": [p[1] for p in categories["How-To"]]
                },
                {
                    "group": "Rituals",
                    "pages": [p[1] for p in categories["Rituals"]]
                },
                {
                    "group": "Skills",
                    "pages": [p[1] for p in categories["Skills"]]
                }
            ]
        },
        {
            "tab": "Reference",
            "groups": [
                {
                    "group": "Reference",
                    "pages": [p[1] for p in categories["Reference"]]
                },
                {
                    "group": "Explanation",
                    "pages": [p[1] for p in categories["Explanation"]]
                },
                {
                    "group": "Governance",
                    "pages": [p[1] for p in categories["Governance"]]
                }
            ]
        }
    ]

    docs_json_data = {
        "$schema": "https://mintlify.com/docs.json",
        "name": "DSOM - Deep State of Mind",
        "theme": "maple",
        "colors": {
            "primary": "#6C3FC5",
            "light": "#EDE8FC",
            "dark": "#2D1A5E"
        },
        "favicon": "/favicon.svg",
        "navigation": {
            "tabs": tabs_config
        },
        "navbar": {
            "primary": {
                "type": "github",
                "href": "https://github.com/linuxmalaysia/deep-state-of-mind-for-my-ai"
            }
        }
    }

    docs_json_path = target_dir / "docs.json"
    with open(docs_json_path, "w", encoding="utf-8") as f:
        json.dump(docs_json_data, f, indent=2)

    total_mdx = len(list(target_dir.rglob("*.mdx")))
    print(f"✅ [MINTLIFY BUILDER COMPLETE] Generated {total_mdx} MDX files and docs.json navigation.")


if __name__ == "__main__":
    repo_root = Path.cwd()
    target_dir = repo_root / "docs-source"
    build_mintlify_tree(repo_root, target_dir)
