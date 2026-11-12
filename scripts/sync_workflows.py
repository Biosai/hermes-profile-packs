#!/usr/bin/env python3
"""Validate multi-profile workflows and render them into their coordinating profile.

A multi-profile workflow is written once, as workflows/<name>.yaml: who does each
step, with which skills, after which steps, and where a human decides. Profiles
install only their own directory, so the definition is rendered into the
coordinating profile as a Hermes skill in the `workflows` category:

    <pack>/profiles/<coordinator>/skills/workflows/<name>/SKILL.md
    <pack>/profiles/<coordinator>/skills/workflows/<name>/references/workflow.yaml

    python scripts/sync_workflows.py           # validate, then write every rendering
    python scripts/sync_workflows.py --check   # validate and report drift, write nothing

See docs/WORKFLOWS.md for the format and how a coordinator runs a workflow.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
ID_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MAX_DESCRIPTION = 60
STEP_KEYS = {"id", "profile", "human", "skills", "extra_skills", "does", "output", "needs",
             "on_fail", "optional_when", "decided_by", "asks", "who"}
TOP_KEYS = {"name", "version", "description", "summary", "pack", "coordinator", "trigger",
            "uses_settings", "all_steps_load", "steps", "done_when", "then"}
REGISTRY_ROW = re.compile(r"^\|\s*`([a-z_]+\.[a-z_]+)`\s*\|([^|]*)\|([^|]*)\|([^|]*)\|\s*$")


class WorkflowError(ValueError):
    pass


# ---------------------------------------------------------------- inputs

def load_registry(root: Path) -> dict[str, dict[str, str]]:
    """Settings registry from the table in docs/PORTABLE_SKILLS.md (single source of truth)."""
    registry = {}
    for line in (root / "docs" / "PORTABLE_SKILLS.md").read_text(encoding="utf-8").splitlines():
        m = REGISTRY_ROW.match(line)
        if m:
            key, values, default, meaning = (part.strip() for part in m.groups())
            default = default.strip("`")
            if default.startswith("("):
                default = ""
            registry[key] = {"values": values.replace("`", ""), "default": default, "meaning": meaning}
    if not registry:
        raise WorkflowError("no settings registry found in docs/PORTABLE_SKILLS.md")
    return registry


def load_profiles(root: Path) -> dict[str, tuple[str, Path]]:
    """profile name -> (pack key, profile directory), from packs.json and each manifest."""
    profiles = {}
    for pack in json.loads((root / "packs.json").read_text(encoding="utf-8"))["packs"]:
        key = pack["name"].removeprefix("hermes-")
        manifest = json.loads((root / pack["manifest"]).read_text(encoding="utf-8"))
        for row in manifest.get("profiles", []):
            profiles[row["name"]] = (key, root / pack["path"] / "profiles" / row["name"])
    return profiles


def installed_skills(profile_dir: Path) -> set[str]:
    """Every skill a profile ships, at any depth (role-owned, workflows, supplemental)."""
    return {p.parent.name for p in (profile_dir / "skills").rglob("SKILL.md")}


def definitions(root: Path) -> list[tuple[Path, dict]]:
    folder = root / "workflows"
    if not folder.is_dir():
        return []
    out = []
    for path in sorted(folder.glob("*.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            raise WorkflowError(f"{path.name}: not a mapping")
        out.append((path, data))
    return out


# ---------------------------------------------------------------- validation

def validate(path: Path, wf: dict, profiles: dict, registry: dict, names: set[str]) -> list[str]:
    errors: list[str] = []
    label = path.name

    def err(message: str) -> None:
        errors.append(f"{label}: {message}")

    unknown = set(wf) - TOP_KEYS
    if unknown:
        err(f"unknown keys {sorted(unknown)}")
    name = wf.get("name", "")
    if name != path.stem or not ID_RE.fullmatch(str(name)):
        err("name must be kebab-case and equal the file name")
    description = str(wf.get("description", ""))
    if not description or len(description) > MAX_DESCRIPTION:
        err(f"description must be 1-{MAX_DESCRIPTION} characters")
    for field in ("version", "summary", "trigger"):
        if not str(wf.get(field, "")).strip():
            err(f"missing {field}")
    pack = wf.get("pack")
    coordinator = wf.get("coordinator")
    if coordinator not in profiles:
        err(f"unknown coordinator {coordinator!r}")
    elif profiles[coordinator][0] != pack:
        err(f"coordinator {coordinator} is not in pack {pack!r}")
    for key in wf.get("uses_settings", []) or []:
        if key not in registry:
            err(f"setting {key!r} is not in the registry (docs/PORTABLE_SKILLS.md)")
    done_when = wf.get("done_when")
    if not isinstance(done_when, list) or not done_when:
        err("done_when must be a non-empty list")
    for follow in wf.get("then", []) or []:
        if follow not in names:
            err(f"then: unknown workflow {follow!r}")

    steps = wf.get("steps")
    if not isinstance(steps, list) or len(steps) < 2:
        err("steps must list at least two steps")
        return errors
    seen: list[str] = []
    ancestors: dict[str, set[str]] = {}
    actors = set()
    human_ids = set()
    for index, step in enumerate(steps, 1):
        sid = str(step.get("id", ""))
        where = f"step {index} ({sid or '?'})"
        if set(step) - STEP_KEYS:
            err(f"{where}: unknown keys {sorted(set(step) - STEP_KEYS)}")
        if not ID_RE.fullmatch(sid) or sid in seen:
            err(f"{where}: id must be kebab-case and unique")
        for field in ("does", "output"):
            if not str(step.get(field, "")).strip():
                err(f"{where}: missing {field}")
        needs = step.get("needs", []) or []
        for need in needs:
            if need not in seen:
                err(f"{where}: needs {need!r}, which is not an earlier step")
        ancestors[sid] = set(needs).union(*(ancestors.get(n, set()) for n in needs))
        if step.get("human"):
            human_ids.add(sid)
            actors.add("human")
            if "profile" in step or step.get("skills") or step.get("extra_skills"):
                err(f"{where}: a human step has no profile or skills")
            decided_by = step.get("decided_by")
            if decided_by != "owner" and decided_by not in registry:
                err(f"{where}: decided_by must be 'owner' or a registry setting")
            if not str(step.get("asks", "")).strip():
                err(f"{where}: a human step says what it asks")
        else:
            profile = step.get("profile")
            if profile not in profiles:
                err(f"{where}: unknown profile {profile!r}")
                seen.append(sid)
                continue
            if profiles[profile][0] != pack:
                err(f"{where}: {profile} is outside pack {pack!r}")
            actors.add(profile)
            have = installed_skills(profiles[profile][1])
            skills = step.get("skills") or []
            if not skills:
                err(f"{where}: a profile step loads at least one skill")
            for skill in skills:
                if skill not in have:
                    err(f"{where}: {profile} has no skill {skill!r}")
            for extra in step.get("extra_skills", []) or []:
                if extra.get("skill") not in have or not str(extra.get("when", "")).strip():
                    err(f"{where}: extra skill {extra!r} must exist in {profile} and say when")
            for skill in wf.get("all_steps_load", []) or []:
                if skill not in have:
                    err(f"{where}: {profile} lacks {skill!r}, which every step loads")
        on_fail = step.get("on_fail")
        if on_fail is not None and (on_fail not in ancestors[sid] or on_fail in human_ids):
            err(f"{where}: on_fail must name an earlier profile step this one depends on")
        seen.append(sid)
    if len(actors) < 2:
        err("a multi-profile workflow needs at least two actors (profiles or a human)")
    if human_ids and "owner.channel" not in (wf.get("uses_settings") or []):
        err("a workflow with human steps must use owner.channel")
    return errors


def validate_recipes(root: Path, workflows: dict[str, dict], profiles: dict) -> list[str]:
    errors = []
    for recipe in json.loads((root / "recipes.json").read_text(encoding="utf-8"))["recipes"]:
        expanded = set(recipe["tiers"]["expanded"])
        for name in recipe.get("workflows", []):
            wf = workflows.get(name)
            if wf is None:
                errors.append(f"recipe {recipe['id']}: unknown workflow {name!r}")
                continue
            if wf["pack"] != recipe["pack"]:
                errors.append(f"recipe {recipe['id']}: workflow {name} belongs to pack {wf['pack']}")
            needed = {s["profile"] for s in wf["steps"] if not s.get("human")} | {wf["coordinator"]}
            missing = sorted(needed - expanded)
            if missing:
                errors.append(f"recipe {recipe['id']}: workflow {name} needs {missing}, absent from the expanded tier")
    return errors


# ---------------------------------------------------------------- rendering

def _code(items) -> str:
    return ", ".join(f"`{i}`" for i in items) or "—"


def first_sentence(text: str) -> str:
    head = re.split(r"(?<=[.!?])\s", text.strip(), maxsplit=1)[0]
    return head if head.endswith((".", "!", "?")) else head + "."


def actor(step: dict) -> str:
    if step.get("human"):
        if step.get("who"):
            return step["who"]
        return "the owner" if step["decided_by"] == "owner" else f"the human named by `{step['decided_by']}`"
    return f"`{step['profile']}`"


def render_skill(wf: dict, registry: dict, coordinators: dict[str, str]) -> str:
    name = wf["name"]
    steps = wf["steps"]
    settings = list(dict.fromkeys(["delivery.board", *(wf.get("uses_settings") or [])]))
    config = "\n".join(
        f"      - {{key: {key}, description: {json.dumps(first_sentence(registry[key]['meaning']), ensure_ascii=False)}, "
        f"default: {json.dumps(registry[key]['default'], ensure_ascii=False)}}}"
        for key in settings
    )
    profiles = sorted({s["profile"] for s in steps if not s.get("human")})
    always = wf.get("all_steps_load") or []
    has_human = any(s.get("human") for s in steps)

    lines = [
        "---",
        f"name: {name}",
        f"description: {json.dumps(wf['description'])}",
        "metadata:",
        "  hermes:",
        "    tags: [workflow, multi-profile]",
        "    config:",
        config,
        "    prerequisites:",
        "      commands: [hermes]",
        "---",
        f"# Workflow: {name}",
        "",
        wf["summary"].strip(),
        "",
        "You coordinate this workflow. Each step belongs to one profile, which runs it with its own "
        "skills; never run another profile's step yourself. This file is generated from "
        f"`workflows/{name}.yaml` (the same definition is in `references/workflow.yaml`).",
        "",
        "## Trigger",
        wf["trigger"].strip(),
        "",
        "## Steps",
        "| # | Step | Actor | Loads | After | Produces |",
        "|---|---|---|---|---|---|",
    ]
    for i, s in enumerate(steps, 1):
        loads = _code((s.get("skills") or []))
        lines.append(f"| {i} | `{s['id']}` | {actor(s)} | {loads} | {_code(s.get('needs') or [])} | {s['output'].strip()} |")
    if always:
        lines += ["", f"Every profile step also loads {_code(always)}."]
    for i, s in enumerate(steps, 1):
        lines += ["", f"### {i}. `{s['id']}` — {actor(s)}", s["does"].strip()]
        if s.get("human"):
            lines.append(f"- Asks: {s['asks'].strip()}")
            if s["decided_by"] != "owner":
                lines.append(f"- Who acts follows `{s['decided_by']}`.")
        for extra in s.get("extra_skills", []) or []:
            lines.append(f"- Also loads `{extra['skill']}` when {extra['when'].strip()}.")
        if s.get("optional_when"):
            lines.append(f"- Runs only when {s['optional_when'].strip()}. Otherwise it is recorded as skipped, with that reason.")
        if s.get("on_fail"):
            lines.append(f"- On failure the work goes back to `{s['on_fail']}` with the findings, then this step runs again.")

    lines += [
        "",
        "## Prerequisites",
        "| Needs | Why | Check |",
        "|---|---|---|",
        f"| Profiles installed: {_code(profiles)} | each step runs as its own profile | `hermes profile list` |",
        "| The `kanban` toolset, when `delivery.board` is `hermes-kanban` | one card per step | `kanban_list` answers |",
    ]
    if has_human:
        lines.append("| A way to reach the owner (`owner.channel`) | human steps | the owner answers there |")
    lines += [
        "",
        "If a required prerequisite is missing, stop before step 1. Say which one, what it blocks, and the "
        "smallest access that would unblock it. A step whose profile is not installed is never run under "
        "another profile: report the workflow as blocked at that step. Never report a step done that its "
        "profile did not complete.",
        "",
        "## Configuration",
        "- `delivery.board` decides how the workflow runs (below).",
    ]
    for key in settings[1:]:
        deciders = [s["id"] for s in steps if s.get("decided_by") == key]
        note = f" Decides who acts at {_code(deciders)}." if deciders else ""
        lines.append(f"- `{key}`: {registry[key]['meaning']}{note}")
    lines += [
        "",
        "Current values appear in the `[Skill config]` block when this skill loads; an unset key shows its "
        "declared default. Persist a value with `hermes config set skills.config.<key> <value>` (per "
        "profile: `hermes -p <profile> config set …`); `hermes config migrate` prompts for keys still unset.",
        "",
        "## Run it",
        "### On a Hermes Kanban board (`delivery.board: hermes-kanban`)",
        f"1. Create every card up front, in step order, with `kanban_create`: title `{name}: <step> — <work item>`, "
        "`assignee` the step's profile, `skills` the step's skills (plus the ones every step loads, and any "
        "extra skill whose condition holds), `parents` the cards of its After steps, and a body with the "
        "step's instructions, what it must produce and a link to the work item. For a step with an \"On "
        "failure\" target, the body also says: on a problem, comment the findings and block the card "
        "instead of completing it. The dispatcher starts each card when its parents are done.",
        "2. A human step is a card assigned to you. When it starts, ask through `owner.channel` and block it "
        "with `kanban_block(kind=\"needs_input\")`. On a go, comment the answer verbatim and complete the "
        "card; a human action (such as a merge) is complete only once you have verified it happened. On a "
        "no, comment it, leave the card blocked, and report the workflow stopped at that step.",
        "3. An optional step whose condition does not hold is completed with `skipped: <reason>`, so the "
        "steps after it proceed.",
        "4. A step with an \"On failure\" target that finds a problem comments its findings and blocks its "
        "card. Create a fix card for the target step's profile with the findings, make it a parent of the "
        "checking card (`kanban_link(parent_id=<fix>, child_id=<check>)`), and unblock the checking card "
        "(`kanban_unblock`): it waits until the fix is done, then runs again.",
        "",
        "### Without a board (`delivery.board: none` or `tracker`)",
        "Run the steps in dependency order. Hand each step to its profile, through the host's profile "
        "delegation or that profile's channel, with its skills, the work item and the outputs of its After "
        "steps; wait for the output and check it against \"Produces\". Loop back on failure as above. At a "
        "human step, ask through `owner.channel` and wait. With `tracker`, record each step's start, output "
        "and decision as comments on the work item.",
        "",
        "## Done when",
        *[f"- {item.strip()}" for item in wf["done_when"]],
        "- Every step is done, or skipped with the reason its condition did not hold; every human decision "
        "is recorded verbatim.",
    ]
    if wf.get("then"):
        lines += ["", "## Then"]
        for follow in wf["then"]:
            lines.append(f"- Start `{follow}`, coordinated by `{coordinators[follow]}`.")
    lines += [
        "",
        "## Report",
        "Each update names the workflow, the current step and its actor, links the cards or the work "
        "item, and says what is needed from whom, if anything.",
        "",
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------- sync

def build(root: Path = ROOT) -> tuple[dict[Path, bytes], list[str]]:
    registry = load_registry(root)
    profiles = load_profiles(root)
    defs = definitions(root)
    names = {path.stem for path, _ in defs}
    errors: list[str] = []
    for path, wf in defs:
        errors += validate(path, wf, profiles, registry, names)
    if errors:
        return {}, errors
    workflows = {wf["name"]: wf for _, wf in defs}
    errors += validate_recipes(root, workflows, profiles)
    coordinators = {n: wf["coordinator"] for n, wf in workflows.items()}
    outputs: dict[Path, bytes] = {}
    for path, wf in defs:
        target = profiles[wf["coordinator"]][1] / "skills" / "workflows" / wf["name"]
        outputs[target / "SKILL.md"] = render_skill(wf, registry, coordinators).encode()
        outputs[target / "references" / "workflow.yaml"] = path.read_bytes()
    return outputs, errors


def managed_dirs(root: Path) -> set[Path]:
    """Rendered workflow dirs on disk: the ones carrying references/workflow.yaml."""
    return {p.parent.parent for p in root.glob("hermes-*/profiles/*/skills/workflows/*/references/workflow.yaml")}


def drift(root: Path = ROOT) -> list[str]:
    outputs, errors = build(root)
    if errors:
        return errors
    problems = []
    for path, data in outputs.items():
        if not path.is_file() or path.read_bytes() != data:
            problems.append(f"stale or missing: {path.relative_to(root)}")
    wanted = {p.parent if p.name == "SKILL.md" else p.parent.parent for p in outputs}
    for orphan in sorted(managed_dirs(root) - wanted):
        problems.append(f"rendered workflow without a definition: {orphan.relative_to(root)}")
    for folder in wanted:
        extra = {p for p in folder.rglob("*") if p.is_file()} - set(outputs)
        problems += [f"unexpected file in a rendered workflow: {p.relative_to(root)}" for p in sorted(extra)]
    return problems


def sync(root: Path = ROOT) -> int:
    outputs, errors = build(root)
    if errors:
        raise WorkflowError("\n".join(errors))
    wanted = {p.parent if p.name == "SKILL.md" else p.parent.parent for p in outputs}
    for orphan in managed_dirs(root) - wanted:
        for f in sorted(orphan.rglob("*"), reverse=True):
            f.unlink() if f.is_file() else f.rmdir()
        orphan.rmdir()
    written = 0
    for path, data in outputs.items():
        if path.is_file() and path.read_bytes() == data:
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        written += 1
    return written


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true", help="validate and report drift without writing")
    args = parser.parse_args()
    try:
        if args.check:
            problems = drift()
            for problem in problems:
                print(problem, file=sys.stderr)
            if problems:
                print("Fix the definition, or run: python scripts/sync_workflows.py", file=sys.stderr)
                return 1
            print(f"workflows valid and in sync: {len(definitions(ROOT))} definitions")
            return 0
        print(f"wrote {sync()} files")
        return 0
    except (OSError, KeyError, WorkflowError, yaml.YAMLError, json.JSONDecodeError) as exc:
        print(f"workflow sync failed: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
