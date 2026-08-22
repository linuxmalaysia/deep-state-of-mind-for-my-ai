#!/usr/bin/env python3
"""
Mintlify MDX Documentation Builder for DSOM.
Translates sovereign Markdown (.md) documents and OKF frontmatter in docs/ and .agents/
into clean Mintlify MDX (.mdx) pages and dynamically generates docs-source/docs.json.

Standard: OKF v0.2 -> Mintlify MDX Specification
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


def parse_okf_frontmatter(content: str):
    """Extract OKF frontmatter fields (title, description) and return body."""
    match = FRONTMATTER_RE.match(content)
    title = None
    description = None

    if match:
        fm_block = match.group(1)
        body = content[match.end():]
        for line in fm_block.splitlines():
            line = line.strip()
            if line.startswith("title:"):
                title = line.split("title:", 1)[1].strip().strip('"')
            elif line.startswith("description:"):
                description = line.split("description:", 1)[1].strip().strip('"')
    else:
        body = content

    # Fallback to first # Heading if title not in frontmatter
    if not title:
        for line in body.splitlines():
            line = line.strip()
            if line.startswith("# "):
                title = line[2:].strip().strip('"')
                break

    if not title:
        title = "Document"

    if not description:
        description = f"{title} — Deep State of Mind (DSOM) Documentation"

    return title, description, body


def convert_markdown_to_mdx(md_text: str) -> str:
    """Convert standard markdown text into Mintlify MDX compatible format."""
    title, description, body = parse_okf_frontmatter(md_text)

    # Clean body: strip leading redundant # Title if it matches frontmatter title
    body_lines = body.strip().splitlines()
    if body_lines and body_lines[0].strip() == f"# {title}":
        body_lines = body_lines[1:]
    clean_body = "\n".join(body_lines).strip()

    # Build Mintlify MDX frontmatter
    # Escape quotes inside strings
    esc_title = title.replace('"', '\\"')
    esc_desc = description.replace('"', '\\"')

    mdx_frontmatter = f'''---
title: "{esc_title}"
description: "{esc_desc}"
---

'''
    return mdx_frontmatter + clean_body + "\n"


def build_mintlify_tree(repo_root: Path, target_dir: Path):
    """Build MDX pages and docs.json navigation index."""
    print("=" * 60)
    print("🔨 [MINTLIFY BUILDER] Compiling Sovereign Markdown Palace to MDX...")

    docs_dir = repo_root / "docs"
    agents_dir = repo_root / ".agents"

    target_dir.mkdir(parents=True, exist_ok=True)

    # Map categories to list of (title, rel_mdx_path_no_ext, source_md)
    categories = {
        "Get Started": [],
        "Governance & Framework": [],
        "Daily Rituals": [],
        "Agent Skills & SOPs": [],
        "Tools & Automation": [],
        "Diataxis Tutorials": [],
        "Diataxis How-To": [],
        "Diataxis Reference": [],
        "Diataxis Explanation": []
    }

    def add_page(category, rel_path, source_file):
        md_text = source_file.read_text(encoding="utf-8", errors="replace")
        mdx_content = convert_markdown_to_mdx(md_text)
        title, _, _ = parse_okf_frontmatter(md_text)

        out_file = target_dir / f"{rel_path}.mdx"
        out_file.parent.mkdir(parents=True, exist_ok=True)
        out_file.write_text(mdx_content, encoding="utf-8")

        categories[category].append((title, rel_path.as_posix()))

    # 1. Get Started & Core Entry Points
    add_page("Get Started", Path("introduction"), docs_dir / "README.md")
    add_page("Get Started", Path("quickstart"), docs_dir / "START-HERE.md")
    add_page("Get Started", Path("security"), docs_dir / "SECURITY.md")
    add_page("Get Started", Path("legal-notice"), docs_dir / "LEGAL-NOTICE.md")

    # 2. Governance
    gov_dir = docs_dir / "governance"
    if gov_dir.exists():
        for md_file in sorted(gov_dir.glob("*.md")):
            slug = f"governance/{md_file.stem.lower()}"
            add_page("Governance & Framework", Path(slug), md_file)

    # 3. Daily Rituals
    add_page("Daily Rituals", Path("rituals/sod-ritual"), docs_dir / "SOD-RITUAL.md")
    add_page("Daily Rituals", Path("rituals/eod-ritual"), docs_dir / "EOD-RITUAL.md")
    add_page("Daily Rituals", Path("rituals/transition-ritual"), docs_dir / "RITUAL-OF-TRANSITION.md")
    add_page("Daily Rituals", Path("rituals/human-handover"), docs_dir / "HUMAN-HANDOVER-CONTEXT.md")

    # 4. Agent Skills
    skills_dir = agents_dir / "skills"
    if skills_dir.exists():
        for skill_folder in sorted(skills_dir.iterdir()):
            if skill_folder.is_dir():
                skill_md = skill_folder / "SKILL.md"
                if skill_md.exists():
                    slug = f"skills/{skill_folder.name}"
                    add_page("Agent Skills & SOPs", Path(slug), skill_md)

    # 5. Tools & Automation
    tools_dir = docs_dir / "tools"
    if tools_dir.exists():
        for md_file in sorted(tools_dir.glob("*.md")):
            slug = f"tools/{md_file.stem.lower()}"
            add_page("Tools & Automation", Path(slug), md_file)

    # 6. Diataxis Quadrants
    tutorials_dir = docs_dir / "tutorials"
    if tutorials_dir.exists():
        for md_file in sorted(tutorials_dir.glob("*.md")):
            slug = f"tutorials/{md_file.stem.lower()}"
            add_page("Diataxis Tutorials", Path(slug), md_file)

    howto_dir = docs_dir / "how-to"
    if howto_dir.exists():
        for md_file in sorted(howto_dir.glob("*.md")):
            slug = f"how-to/{md_file.stem.lower()}"
            add_page("Diataxis How-To", Path(slug), md_file)

    ref_dir = docs_dir / "reference"
    if ref_dir.exists():
        for md_file in sorted(ref_dir.glob("*.md")):
            slug = f"reference/{md_file.stem.lower()}"
            add_page("Diataxis Reference", Path(slug), md_file)

    expl_dir = docs_dir / "explanation"
    if expl_dir.exists():
        for md_file in sorted(expl_dir.glob("*.md")):
            slug = f"explanation/{md_file.stem.lower()}"
            add_page("Diataxis Explanation", Path(slug), md_file)

    # Create root index.mdx if missing
    index_mdx = target_dir / "index.mdx"
    if not index_mdx.exists():
        index_content = '''---
title: "DSOM Sovereign Knowledge Brain"
description: "Sovereign AI Metacognitive Protocol & Knowledge Base."
---

# Welcome to DSOM Knowledge Brain

The **Deep State of Mind (DSOM)** framework provides zero-global spatial memory, metacognitive governance, and deterministic execution for sovereign AI workflows.

<CardGroup cols={2}>
  <Card title="Quickstart" icon="bolt" href="/quickstart">
    Get up and running with DSOM in under 5 minutes.
  </Card>
  <Card title="Governance" icon="shield" href="/governance/ai-initialization-sequence">
    Explore the 31 Constitutional AI Rules and sovereign architecture.
  </Card>
  <Card title="Agent Skills" icon="toolbox" href="/skills/agent-plugin-packager">
    Discover OKF-compliant standard operating procedures.
  </Card>
  <Card title="Team Masterclass" icon="graduation-cap" href="/tutorials/team-dsom-masterclass">
    End-to-end team onboarding and pair programming workflows.
  </Card>
</CardGroup>
'''
        index_mdx.write_text(index_content, encoding="utf-8")

    # Build docs.json Navigation
    tabs_config = [
        {
            "tab": "Documentation",
            "groups": [
                {
                    "group": "Get Started",
                    "pages": [p[1] for p in categories["Get Started"]]
                },
                {
                    "group": "Governance & Protocols",
                    "pages": [p[1] for p in categories["Governance & Framework"]]
                },
                {
                    "group": "Daily Rituals",
                    "pages": [p[1] for p in categories["Daily Rituals"]]
                },
                {
                    "group": "AI Agent Skills",
                    "pages": [p[1] for p in categories["Agent Skills & SOPs"]]
                }
            ]
        },
        {
            "tab": "Tools & Diataxis",
            "groups": [
                {
                    "group": "Tools & Automation",
                    "pages": [p[1] for p in categories["Tools & Automation"]]
                },
                {
                    "group": "Tutorials",
                    "pages": [p[1] for p in categories["Diataxis Tutorials"]]
                },
                {
                    "group": "How-To Guides",
                    "pages": [p[1] for p in categories["Diataxis How-To"]]
                },
                {
                    "group": "Reference",
                    "pages": [p[1] for p in categories["Diataxis Reference"]]
                },
                {
                    "group": "Explanation",
                    "pages": [p[1] for p in categories["Diataxis Explanation"]]
                }
            ]
        }
    ]

    docs_json_data = {
        "$schema": "https://mintlify.com/docs.json",
        "name": "DSOM — Deep State of Mind",
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
