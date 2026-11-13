#!/usr/bin/env python3
"""Copy each canonical skill in shared-skills/ into every profile that carries it.

A skill used by several profiles is written once, under shared-skills/<name>/, and
listed in shared-skills/targets.json with the profile directories that ship it.
Profiles must carry byte-identical copies: edit the canonical file, then run this.

    python scripts/sync_shared_skills.py           # rewrite every copy
    python scripts/sync_shared_skills.py --check   # report drift, write nothing
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHARED = ROOT / "shared-skills"


def tree(path: Path) -> dict[str, bytes]:
    return {
        str(p.relative_to(path)): p.read_bytes()
        for p in sorted(path.rglob("*"))
        if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc"
    }


def plan(root: Path = ROOT) -> list[tuple[str, Path, Path]]:
    """(skill, canonical dir, copy dir) for every declared copy."""
    shared = root / "shared-skills"
    targets = json.loads((shared / "targets.json").read_text(encoding="utf-8"))["skills"]
    rows = []
    for skill, profiles in sorted(targets.items()):
        source = shared / skill
        if not (source / "SKILL.md").is_file():
            raise ValueError(f"missing canonical skill: shared-skills/{skill}/SKILL.md")
        for profile in profiles:
            profile_dir = root / profile
            if not (profile_dir / "distribution.yaml").is_file():
                raise ValueError(f"{skill}: target is not a profile distribution: {profile}")
            rows.append((skill, source, profile_dir / "skills" / skill))
    return rows


def drift(root: Path = ROOT) -> list[str]:
    problems = []
    shared = root / "shared-skills"
    declared = set(json.loads((shared / "targets.json").read_text(encoding="utf-8"))["skills"])
    on_disk = {p.name for p in shared.iterdir() if p.is_dir()}
    problems += [f"shared-skills/{name} is not declared in targets.json" for name in sorted(on_disk - declared)]
    for skill, source, copy in plan(root):
        if tree(copy) != tree(source):
            problems.append(f"{copy.relative_to(root)} differs from shared-skills/{skill}")
    return problems


def sync(root: Path = ROOT) -> int:
    written = 0
    for _skill, source, copy in plan(root):
        wanted = tree(source)
        if tree(copy) == wanted:
            continue
        if copy.exists():
            for stale in sorted(copy.rglob("*"), reverse=True):
                if stale.is_file():
                    stale.unlink()
                elif stale.is_dir():
                    stale.rmdir()
        for rel, data in wanted.items():
            target = copy / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
        written += 1
    return written


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true", help="report drift without writing")
    args = parser.parse_args()
    try:
        if args.check:
            problems = drift()
            for problem in problems:
                print(problem, file=sys.stderr)
            if problems:
                print("Run: python scripts/sync_shared_skills.py", file=sys.stderr)
                return 1
            print(f"shared skills in sync: {len(plan())} copies")
            return 0
        print(f"rewrote {sync()} copies")
        return 0
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"shared skill sync failed: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
