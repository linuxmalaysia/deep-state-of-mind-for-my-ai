# /// script
# dependencies = [
#     "pyyaml>=6.0",
# ]
# ///
"""
Council of High Intelligence Emulator & Consensus Engine for DSOM Workspace
Protocol: Deep State of Mind (DSOM) For My AI Protocol
Author:   Harisfazillah Jamel (LinuxMalaysia)
License:  GNU General Public License v3.0

Description:
Executes multi-perspective AI deliberation across specialized domain personas:
1. Senior Systems Architect
2. Chief Security Officer (CSO)
3. Pragmatic Staff Engineer
4. Domain Specialist
5. Sovereign FOSS Systems Architect (Harisfazillah Jamel / LinuxMalaysia)
Synthesizes trade-offs, evidence tags, and produces a Council Decision Record (CDR)
markdown artifact with OKF v0.2 frontmatter. Zero-binary pure Python implementation (Rule 27).
"""

import argparse
import copy
import datetime
import functools
import pathlib
import re
import sys
from typing import Any, Dict, Optional, Tuple

import yaml

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
DECISIONS_DIR = REPO_ROOT / "docs" / "decisions"
VALID_MODES = {"quick", "full", "duo", "triad"}
MAX_CACHEABLE_CONTEXT_BYTES = 8000


def get_timestamp() -> str:
    """Returns ISO 8601 UTC timestamp string ending with Z."""
    return datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


@functools.lru_cache(maxsize=256)
def _slugify(text: str) -> str:
    """Converts a topic string into a clean filename slug."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    return text[:50].strip("-") or "decision"


@functools.lru_cache(maxsize=256)
def _dump_yaml_frontmatter_cached(
    okf_version: str,
    doc_type: str,
    title: str,
    timestamp: str,
    topics: Tuple[str, ...],
    spec_version: str,
    description: str,
) -> str:
    """
    Serializes frontmatter mapping into YAML string with LRU caching.
    Prevents repeated AST serialization and PyYAML dumping overhead.
    """
    meta = {
        "okf_version": okf_version,
        "type": doc_type,
        "title": title,
        "timestamp": timestamp,
        "topics": list(topics),
        "spec_version": spec_version,
        "description": description,
    }
    return yaml.safe_dump(meta, sort_keys=False, allow_unicode=True)


def _build_evaluation(topic: str, context: str, mode: str, triad: str) -> dict:
    """Core evaluation logic for council personas and consensus verdict."""
    triad = (triad or "").lower()

    # Determine domain specialist title based on explicit triad, falling back to topic keywords
    domain_title = "Domain Specialist"
    if triad == "security":
        domain_title = "Cybersecurity Specialist"
    elif triad in {"architecture", "enterprise-infrastructure"}:
        domain_title = "Data Infrastructure Engineer"
    elif triad == "shipping":
        domain_title = "DevOps & Release Engineer"
    elif triad in {"risk", "public-sector-tech"}:
        domain_title = "Risk & Compliance Officer"
    elif triad == "sovereignty":
        domain_title = "Digital Sovereignty Auditor"
    elif "security" in topic.lower() or "auth" in topic.lower():
        domain_title = "Cybersecurity Specialist"
    elif "microservice" in topic.lower() or "database" in topic.lower():
        domain_title = "Data Infrastructure Engineer"
    elif "ci" in topic.lower() or "deploy" in topic.lower():
        domain_title = "DevOps & Release Engineer"
    elif "compliance" in topic.lower():
        domain_title = "Risk & Compliance Officer"

    # Define council personas
    all_personas = {
        "Systems Architect": {
            "title": "Senior Systems Architect",
            "stance": "Architectural purity, high availability, zero-global state, and long-term scalability.",
            "recommendation": f"Enforce modular decoupled design and stateless execution for '{topic}'.",
            "risk": "High operational overhead if abstracted prematurely without strict boundary definitions.",
        },
        "Chief Security Officer": {
            "title": "Chief Security Officer (CSO)",
            "stance": "Zero-trust boundaries, fine-grained access control (FGAC), credential isolation, and auditability.",
            "recommendation": f"Mandate least-privilege access, secret sanitisation, and cryptographic verification for '{topic}'.",
            "risk": "Potential friction in developer workflow or deployment velocity if security gates stall pipelines.",
        },
        "Pragmatic Engineer": {
            "title": "Pragmatic Staff Engineer",
            "stance": "Implementation velocity, minimal dependencies, operational simplicity, and developer experience.",
            "recommendation": f"Prioritise zero-binary, lightweight native Python utilities for '{topic}' to minimise maintenance toil.",
            "risk": "Risk of technical debt accumulation if short-term expediency compromises long-term HA requirements.",
        },
        "Domain Specialist": {
            "title": domain_title,
            "stance": "Domain-specific excellence, data integrity, performance tuning, and practical robustness.",
            "recommendation": f"Apply proven industry design patterns and strict schema validation tailored to '{topic}'.",
            "risk": "Domain-specific edge cases failing during unexpected traffic spikes or boundary transitions.",
        },
        "Sovereign FOSS Architect": {
            "title": "Sovereign FOSS Systems Architect (Harisfazillah Jamel / LinuxMalaysia)",
            "stance": "Digital sovereignty over proprietary lock-in, open standards (POSIX), enterprise Linux HA, and COO realism.",
            "recommendation": f"Ensure full compute and data ownership for '{topic}' using battle-tested open-source components and calibrated 5-year TCO.",
            "risk": "Potential velocity dampening during initial prototype exploration if bare-metal or self-hosting constraints are over-indexed.",
        },
    }

    # Select active personas based on mode and triad
    if mode == "duo":
        active_keys = ["Systems Architect", "Chief Security Officer"]
    elif mode == "triad":
        if triad == "sovereignty":
            active_keys = ["Sovereign FOSS Architect", "Pragmatic Engineer", "Chief Security Officer"]
        elif triad == "enterprise-infrastructure":
            active_keys = ["Sovereign FOSS Architect", "Systems Architect", "Pragmatic Engineer"]
        elif triad == "public-sector-tech":
            active_keys = ["Sovereign FOSS Architect", "Chief Security Officer", "Domain Specialist"]
        elif triad == "architecture":
            active_keys = ["Sovereign FOSS Architect", "Systems Architect", "Domain Specialist"]
        elif triad == "security":
            active_keys = ["Systems Architect", "Chief Security Officer", "Sovereign FOSS Architect"]
        else:
            # Default triad (e.g. shipping, risk)
            active_keys = ["Systems Architect", "Chief Security Officer", "Domain Specialist"]
    elif mode == "full":
        active_keys = list(all_personas.keys())
    else:  # quick mode defaults to the four classic council pillars
        active_keys = ["Systems Architect", "Chief Security Officer", "Pragmatic Engineer", "Domain Specialist"]

    perspectives = {k: all_personas[k] for k in active_keys}

    # Build trade-off debate points with evidence tags
    debate_points = [
        {
            "category": "Security vs. Velocity",
            "tag": "[ASSUMPTION]",
            "detail": f"Zero external binary dependencies reduce operational attack surface for '{topic}'.",
            "resolution": "Adopt automated pre-commit guardrail checks to balance speed with security gate enforcing.",
        },
        {
            "category": "Sovereignty vs. Cloud Lock-in",
            "tag": "[ASSUMPTION]",
            "detail": f"Reliance on open standards and self-hostable runtimes preserves strategic exit capability for '{topic}'.",
            "resolution": "Enforce POSIX standards, open database formats, and zero-binary pure Python execution in alignment with Rule 27.",
        },
        {
            "category": "Architecture vs. Complexity",
            "tag": "[INFERENCE]",
            "detail": "Modular Python execution allows seamless FastMCP tool exposure while preserving decoupled spatial memory.",
            "resolution": "Maintain pure Python zero-binary CLI implementation to satisfy Rule 27 without adding Node.js runtime bloat.",
        },
        {
            "category": "Operational Feasibility",
            "tag": "[ASSUMPTION]",
            "detail": f"Local environment under `uv` provides sufficient execution isolation for '{topic}'.",
            "resolution": "Enforce explicit requirement checks and fallback handling across Linux, macOS, and Windows environments.",
        },
    ]

    if context:
        debate_points.append({
            "category": "Contextual Constraints",
            "tag": "[FACT]",
            "detail": f"Provided context: '{context}'.",
            "resolution": "Align execution parameters directly with supplied operational constraints.",
        })

    # Final verdict synthesis
    verdict = {
        "summary": f"Simulated multi-perspective persona deliberation for '{topic}' under mode '{mode}'. Note that no empirical assessment or live human review was performed, and this output represents an exploratory discussion. The listed action items and kill criteria are simulated templates and have not been evaluated against the specific operational topic or context.",
        "action_plan": [
            "1. Implement core logic using zero-dependency pure Python scripts in alignment with Rule 27.",
            "2. Verify digital sovereignty and zero proprietary lock-in under Harisfazillah Jamel heuristics.",
            "3. Integrate FastMCP tool contract in `tools/mcp/server.py` for direct AI client invocation.",
            "4. Add comprehensive regression tests under `tests/test_council_emulator.py`.",
            "5. Emit OKF v0.2 compliant Council Decision Record (CDR) artifact for spatial memory tracking.",
        ],
        "kill_criteria": [
            "Requirement for third-party Node.js global binaries or elevated UAC privileges (unevaluated template).",
            "Uncalibrated recurring cloud licensing taxes or closed proprietary API capture (unevaluated template).",
            "Failure to pass OKF v0.2 frontmatter validation or UTF-8 encoding checks (unevaluated template).",
        ],
    }

    return {
        "topic": topic,
        "context": context,
        "mode": mode,
        "triad": triad,
        "perspectives": perspectives,
        "debate_points": debate_points,
        "verdict": verdict,
    }


@functools.lru_cache(maxsize=128)
def _evaluate_topic_cached(topic: str, context: str, mode: str, triad: str) -> dict:
    """Internal memoized evaluation builder."""
    return _build_evaluation(topic=topic, context=context, mode=mode, triad=triad)


def evaluate_topic(topic: str, context: str = "", mode: str = "quick", triad: str = None) -> dict:
    """
    Simulates multi-perspective assessment across council personas and modes.

    Args:
        topic: The decision topic or architectural trade-off to evaluate.
        context: Optional operational context or constraints.
        mode: Deliberation mode ('quick', 'full', 'duo', 'triad').
        triad: Optional domain triad selector ('architecture', 'security', 'shipping', 'risk',
               'sovereignty', 'enterprise-infrastructure', 'public-sector-tech').

    Returns:
        Structured evaluation dict with persona perspectives, trade-off debate, and consensus verdict.
    """
    mode_clean = (mode or "quick").lower()
    if mode_clean not in VALID_MODES:
        raise ValueError(f"Invalid mode '{mode}'. Supported modes are: {', '.join(sorted(VALID_MODES))}")
    mode_norm = mode_clean
    triad_norm = (triad or "").lower()
    context_str = context or ""

    # Check byte size of context to avoid caching huge payloads in LRU memory
    context_bytes = len(context_str.encode("utf-8"))
    if context_bytes > MAX_CACHEABLE_CONTEXT_BYTES:
        return _build_evaluation(topic=topic, context=context_str, mode=mode_norm, triad=triad_norm)

    result = _evaluate_topic_cached(topic=topic, context=context_str, mode=mode_norm, triad=triad_norm)
    return copy.deepcopy(result)


def clear_cache() -> None:
    """Clears all internal caches in council_emulator."""
    _evaluate_topic_cached.cache_clear()
    _dump_yaml_frontmatter_cached.cache_clear()
    _slugify.cache_clear()


def get_cache_info() -> Dict[str, Any]:
    """Returns cache diagnostic statistics for test inspection and profiling."""
    return {
        "evaluate_topic": _evaluate_topic_cached.cache_info()._asdict(),
        "yaml_frontmatter": _dump_yaml_frontmatter_cached.cache_info()._asdict(),
        "slugify": _slugify.cache_info()._asdict(),
    }


def generate_cdr(topic: str, evaluation: dict, timestamp: str = None) -> str:
    """
    Formats the evaluation into an OKF v0.2 Council Decision Record (CDR) markdown document.

    Args:
        topic: The deliberation topic string.
        evaluation: The structured assessment output from evaluate_topic().
        timestamp: Optional ISO 8601 timestamp string.

    Returns:
        Formatted markdown document string with OKF v0.2 frontmatter starting on line 1.
    """
    if timestamp is None:
        timestamp = get_timestamp()

    perspectives = evaluation.get("perspectives", {})
    debate_points = evaluation.get("debate_points", [])
    verdict = evaluation.get("verdict", {})

    matrix_rows = []
    for key, info in perspectives.items():
        title = info.get("title", key)
        stance = info.get("stance", "")
        recommendation = info.get("recommendation", "")
        risk = info.get("risk", "")
        matrix_rows.append(f"| **{title}** | {stance} | {recommendation} | {risk} |")

    matrix_table = "\n".join(matrix_rows)

    debate_rows = []
    for dp in debate_points:
        category = dp.get("category", "Debate")
        tag = dp.get("tag", "[FACT]")
        detail = dp.get("detail", "")
        resolution = dp.get("resolution", "")
        debate_rows.append(f"- **{category}** `{tag}`: {detail}\n  *Resolution:* {resolution}")

    debate_block = "\n".join(debate_rows)

    action_plan_rows = "\n".join(verdict.get("action_plan", []))
    kill_criteria_rows = "\n".join(f"- {item}" for item in verdict.get("kill_criteria", []))

    yaml_frontmatter = _dump_yaml_frontmatter_cached(
        okf_version="0.2",
        doc_type="documentation",
        title=f"Council Decision Record: {topic}",
        timestamp=timestamp,
        topics=("council", "decision", "architecture"),
        spec_version="0.2",
        description=f"Council Decision Record (CDR) produced by Council of High Intelligence multi-agent deliberation engine for {topic}.",
    )

    body_markdown = f"""# Council Decision Record (CDR): {topic}

## 1. Executive Summary
{verdict.get('summary', '')}

## 2. Persona Perspectives Matrix

| Persona | Primary Stance | Key Recommendation | Critical Risk Flagged |
| :--- | :--- | :--- | :--- |
{matrix_table}

## 3. Deliberation & Trade-off Debate
{debate_block}

## 4. Final Council Verdict & Action Plan

### Priority Action Items
{action_plan_rows}

### Mandatory Kill Criteria
{kill_criteria_rows}

---
*Generated by DSOM Council of High Intelligence Emulator (Rule 27) | Timestamp: {timestamp}*
"""
    return f"---\n{yaml_frontmatter}---\n{body_markdown.strip()}\n"


def run_council(topic: str, context: str = "", output_path: str = "", mode: str = "quick", triad: str = "") -> str:
    """
    Main programmatic entrypoint to execute Council deliberation.

    Args:
        topic: The decision topic or architectural question.
        context: Optional extra operational context.
        output_path: Optional output file path. If provided, writes the CDR markdown artifact.
        mode: Deliberation mode ('quick', 'full', 'duo', 'triad').
        triad: Domain triad selector ('architecture', 'security', 'shipping', 'risk',
               'sovereignty', 'enterprise-infrastructure', 'public-sector-tech').

    Returns:
        The generated OKF v0.2 CDR markdown string.
    """
    ts = get_timestamp()
    evaluation = evaluate_topic(topic=topic, context=context, mode=mode, triad=triad)
    cdr_md = generate_cdr(topic=topic, evaluation=evaluation, timestamp=ts)

    if output_path:
        dest_file = REPO_ROOT / output_path if not pathlib.Path(output_path).is_absolute() else pathlib.Path(output_path)
        dest_file.parent.mkdir(parents=True, exist_ok=True)
        dest_file.write_text(cdr_md, encoding="utf-8")
        print(f"[Council Emulator] Council Decision Record saved to: {dest_file}", file=sys.stderr)

    return cdr_md


def cmd_search(query: str, search_dir: pathlib.Path = None) -> list:
    """
    Searches saved Council Decision Records for query string in OKF frontmatter or body.

    Args:
        query: Search term string.
        search_dir: Directory to search (defaults to docs/decisions/).

    Returns:
        List of matching (path, title, description) tuples.
    """
    target_dir = search_dir or DECISIONS_DIR
    if not target_dir.exists():
        print(f"[Council Search] Search directory {target_dir} does not exist.", file=sys.stderr)
        return []

    results = []
    for md_file in target_dir.rglob("*.md"):
        try:
            content = md_file.read_text(encoding="utf-8")
            if query.lower() in content.lower():
                title = md_file.stem
                desc = "Council Decision Record"
                if content.startswith("---"):
                    parts = content.split("---", 2)
                    if len(parts) >= 3:
                        meta = yaml.safe_load(parts[1])
                        if meta and isinstance(meta, dict):
                            title = meta.get("title", title)
                            desc = meta.get("description", desc)
                results.append((md_file, title, desc))
        except Exception:
            pass

    return results


def main():
    parser = argparse.ArgumentParser(description="DSOM Council of High Intelligence Zero-Binary CLI Emulator (Rule 27)")
    parser.add_argument("topic_pos", nargs="?", type=str, help="Topic for Council deliberation")
    parser.add_argument("--topic", "-t", type=str, help="Topic for Council deliberation")
    parser.add_argument("--context", "-c", type=str, default="", help="Optional operational context")
    parser.add_argument("--output", "-o", nargs="?", const="", default=None, help="Output markdown path for CDR artifact")
    parser.add_argument("--mode", "-m", type=str, default="quick", choices=sorted(VALID_MODES), help="Deliberation mode")
    parser.add_argument("--triad", type=str, default="", help="Domain triad selector for triad mode")
    parser.add_argument("--search", "-s", type=str, help="Search query for existing Council Decision Records")

    args = parser.parse_args()

    if args.search:
        print(f"[Council Search] Querying Council Decision Records for: '{args.search}'...", file=sys.stderr)
        matches = cmd_search(args.search)
        if matches:
            print(f"\nFound {len(matches)} matching Council Decision Record(s):", file=sys.stderr)
            for file_path, title, desc in matches:
                print(f" - [{file_path}] {title}\n   {desc}\n", file=sys.stderr)
        else:
            print(f"No Council Decision Records matched query '{args.search}'.", file=sys.stderr)
        return

    topic = args.topic or args.topic_pos
    if not topic:
        parser.print_help()
        sys.exit(1)

    if args.output is not None:
        if args.output == "":
            slug = _slugify(topic)
            output_path = f"docs/decisions/cdr-{slug}.md"
        else:
            output_path = args.output
    else:
        output_path = ""

    cdr_output = run_council(
        topic=topic,
        context=args.context,
        output_path=output_path,
        mode=args.mode,
        triad=args.triad
    )

    print("\n" + cdr_output)


if __name__ == "__main__":
    main()
