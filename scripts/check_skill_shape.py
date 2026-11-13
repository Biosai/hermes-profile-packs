#!/usr/bin/env python3
"""Hold every skill added on top of the upstream baseline to the upstream skill shape.

Upstream role skills are a title, a line starting "Use when", then `## Procedure`,
usually `## Decision rules`, and `## Quality gate`, in 150-600 words. Skills added
here keep that shape and add the portability sections of docs/PORTABLE_SKILLS.md:

    skill      # Title / Use when ... / ## Prerequisites / ## Configuration (when it
               reads settings) / ## Procedure / ## Decision rules / ## Quality gate
    workflow   # Title / ## Trigger / ## Prerequisites / ## Configuration (when it
               reads settings) / ## Steps / ## Decision rules / ## Done when

A hand-written workflow is a SKILL.md under skills/workflows/ without
references/workflow.yaml (those are rendered by sync_workflows.py and skipped here).
Detail that does not fit goes to references/ inside the skill folder.

    python scripts/check_skill_shape.py            # every added skill
    python scripts/check_skill_shape.py PATH ...   # only skills under these paths
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
GENERATED = {"capabilities", "software-development", "research", "productivity", "creative",
             "autonomous-ai-agents", "web", "academy-continuing-education"}
MAX_DESCRIPTION = 60          # Hermes clips longer descriptions in the skill index
MAX_WORDS = {"skill": 650, "workflow": 750}
SKILL_SECTIONS = ["## Prerequisites", "## Procedure", "## Decision rules", "## Quality gate"]
WORKFLOW_SECTIONS = ["## Trigger", "## Prerequisites", "## Steps", "## Decision rules", "## Done when"]
ALLOWED = {"skill": {*SKILL_SECTIONS, "## Configuration"}, "workflow": {*WORKFLOW_SECTIONS, "## Configuration"}}
# Words that mark one team's past incident rather than a rule anyone can use.
RESIDUE = re.compile(r"\b(?:once (?:produced|caused|cost|led|shipped|broke)|last (?:week|month|year)|"
                     r"in (?:19|20)\d\d\b|\(\d{1,2}/\d{1,2}/\d{2,4}\))", re.IGNORECASE)


def added_skills(root: Path) -> list[Path]:
    """SKILL.md files that are not upstream-baselined, not generated and not rendered."""
    baseline = json.loads((root / "capabilities" / "baseline.json").read_text(encoding="utf-8"))["profile_source_files"]
    out = []
    for path in sorted([*root.glob("hermes-*/profiles/*/skills/**/SKILL.md"), *root.glob("shared-skills/*/SKILL.md")]):
        rel = path.relative_to(root).as_posix()
        parts = path.relative_to(root).parts
        if rel in baseline:
            continue
        if parts[0] != "shared-skills":
            first = parts[4]                      # hermes-x/profiles/<p>/skills/<first>/...
            if first in GENERATED:
                continue
            if (path.parent / "references" / "workflow.yaml").is_file():
                continue                          # rendered multi-profile workflow
            copy_of = root / "shared-skills" / path.parent.name / "SKILL.md"
            if first != "workflows" and copy_of.is_file():
                continue                          # byte-identical copy; the source is checked
        out.append(path)
    return out


def kind_of(path: Path, root: Path) -> str:
    return "workflow" if "workflows" in path.relative_to(root).parts[:-2] else "skill"


def check(path: Path, root: Path, registry: set[str]) -> list[str]:
    rel = path.relative_to(root).as_posix()
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not match:
        return [f"{rel}: no YAML frontmatter"]
    errors = []
    try:
        front = yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError as exc:
        return [f"{rel}: frontmatter is not valid YAML ({exc})"]
    body = match.group(2)
    kind = kind_of(path, root)
    if front.get("name") != path.parent.name:
        errors.append(f"{rel}: name must equal the folder name")
    description = str(front.get("description") or "")
    if not description or len(description) > MAX_DESCRIPTION:
        errors.append(f"{rel}: description must be 1-{MAX_DESCRIPTION} characters (has {len(description)})")
    keys = [c.get("key") for c in (((front.get("metadata") or {}).get("hermes") or {}).get("config") or [])]
    for key in keys:
        if key not in registry:
            errors.append(f"{rel}: setting {key!r} is not in docs/PORTABLE_SKILLS.md")
        elif f"`{key}`" not in body:
            errors.append(f"{rel}: declares setting {key!r} but the body never says what it changes")
    headings = re.findall(r"^## .*$", body, re.M)
    wanted = WORKFLOW_SECTIONS if kind == "workflow" else SKILL_SECTIONS
    for heading in wanted:
        if heading not in headings:
            errors.append(f"{rel}: missing section {heading!r}")
    if keys and "## Configuration" not in headings:
        errors.append(f"{rel}: reads settings but has no '## Configuration' section")
    for heading in headings:
        if heading not in ALLOWED[kind]:
            errors.append(f"{rel}: section {heading!r} is not part of the {kind} shape (fold it in, or move it to references/)")
    order = [h for h in headings if h in ALLOWED[kind]]
    at = wanted.index("## Prerequisites") + 1          # Configuration comes right after Prerequisites
    expected = [h for h in (wanted[:at] + ["## Configuration"] + wanted[at:]) if h in order]
    if order != expected:
        errors.append(f"{rel}: sections are out of order (expected {', '.join(expected)})")
    if kind == "skill" and not re.search(r"^Use when ", body, re.M):
        errors.append(f"{rel}: no line starting 'Use when' under the title")
    words = len(body.split())
    if words > MAX_WORDS[kind]:
        errors.append(f"{rel}: {words} words (max {MAX_WORDS[kind]}); move detail to references/")
    for link in re.findall(r"\]\((references/[^)#]+)", body):
        if not (path.parent / link).is_file():
            errors.append(f"{rel}: links {link}, which does not exist")
    hit = RESIDUE.search(body)
    if hit:
        errors.append(f"{rel}: reads like one team's incident ({hit.group(0)!r}); keep the rule, drop the story")
    return errors


def main(argv: list[str]) -> int:
    registry = set(re.findall(r"^\| `([a-z_]+\.[a-z_]+)` \|", (ROOT / "docs" / "PORTABLE_SKILLS.md").read_text(encoding="utf-8"), re.M))
    scopes = [Path(a).resolve() for a in argv]
    skills = [p for p in added_skills(ROOT) if not scopes or any(s == p or s in p.parents for s in scopes)]
    errors = [e for path in skills for e in check(path, ROOT, registry)]
    for error in errors:
        print(error, file=sys.stderr)
    if errors:
        print(f"{len(errors)} problem(s) in {len(skills)} added skills", file=sys.stderr)
        return 1
    print(f"skill shape OK: {len(skills)} added skills and workflows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
