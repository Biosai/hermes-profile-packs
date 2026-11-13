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

A team with fewer profiles than a workflow has roles renders its own copy, with
several roles (or all of them) held by one profile:

    python scripts/sync_workflows.py --render issue-to-merge --solo
    python scripts/sync_workflows.py --render contract-change \
        --assign agency-onchain-engineer=self --assign agency-code-reviewer=reviewer \
        --assign agency-security-reviewer=reviewer

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
             "on_fail", "on_reject", "optional_when", "decided_by", "asks", "who"}
TOP_KEYS = {"name", "version", "description", "summary", "pack", "coordinator", "trigger",
            "uses_settings", "all_steps_load", "steps", "done_when", "then", "max_fix_rounds"}
# A human step is decided by the owner, or by whoever one of these settings names. Other
# settings say how something is done (how an approval is captured), not who decides.
DECIDER_SETTINGS = {"delivery.merge_policy", "delivery.apply_policy"}
DEFAULT_FIX_ROUNDS = 3
RUNNER = "self"            # in a role assignment: the profile that runs the workflow
BOARD = "delivery.board"
HANDOFF = "delivery.handoff"
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
    for key in (BOARD, HANDOFF):
        if key not in registry:
            raise WorkflowError(f"the settings registry lacks {key}, which every workflow rendering uses")
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


def load_orchestrators(root: Path) -> dict[str, str]:
    """pack key -> the profile its manifest names as `orchestrator` (the pack's coordinator of multi-role work)."""
    out = {}
    for pack in json.loads((root / "packs.json").read_text(encoding="utf-8"))["packs"]:
        manifest = json.loads((root / pack["manifest"]).read_text(encoding="utf-8"))
        if manifest.get("orchestrator"):
            out[pack["name"].removeprefix("hermes-")] = manifest["orchestrator"]
    return out


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

def validate(path: Path, wf: dict, profiles: dict, registry: dict, names: set[str],
             orchestrators: dict[str, str] | None = None) -> list[str]:
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
            if decided_by != "owner" and not (decided_by in DECIDER_SETTINGS and decided_by in registry):
                err(f"{where}: decided_by must be 'owner' or a setting that names who acts {sorted(DECIDER_SETTINGS)}")
            if not str(step.get("asks", "")).strip():
                err(f"{where}: a human step says what it asks")
            on_reject = step.get("on_reject")
            if on_reject is not None and (on_reject not in ancestors[sid] or on_reject in human_ids):
                err(f"{where}: on_reject must name an earlier profile step this one depends on")
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
        if not step.get("human") and step.get("on_reject") is not None:
            err(f"{where}: on_reject belongs to a human step; a profile step uses on_fail")
        seen.append(sid)
    if len(actors) < 2:
        err("a multi-profile workflow needs at least two actors (profiles or a human)")
    rounds = wf.get("max_fix_rounds", DEFAULT_FIX_ROUNDS)
    if not isinstance(rounds, int) or isinstance(rounds, bool) or not 1 <= rounds <= 9:
        err("max_fix_rounds must be a whole number from 1 to 9")
    # Who coordinates: the pack's orchestrator as soon as two profiles are involved (routing
    # between specialists is its job); a workflow of one profile and a human is its own.
    step_profiles = actors - {"human"}
    if coordinator in profiles and orchestrators is not None:
        if len(step_profiles) >= 2:
            wanted = orchestrators.get(pack)
            if wanted and coordinator != wanted:
                err(f"coordinator must be {wanted}, the pack's orchestrator, because {len(step_profiles)} profiles hold steps")
        elif step_profiles and coordinator not in step_profiles:
            err(f"coordinator must be {sorted(step_profiles)[0]}, the only profile that holds a step")
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
            needed = {s["profile"] for s in wf["steps"] if not s.get("human")}
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


def roles_of(wf: dict) -> list[str]:
    """The pack profiles a definition names: one per profile step, plus the coordinator."""
    return sorted({s["profile"] for s in wf["steps"] if not s.get("human")} | {wf["coordinator"]})


def assignment_from(wf: dict, pairs: list[str], solo: bool) -> dict[str, str]:
    """Role assignment from the command line: `--solo`, or one `--assign ROLE=WHO` per role."""
    roles = roles_of(wf)
    if solo:
        if pairs:
            raise WorkflowError("--solo and --assign are exclusive")
        return {role: RUNNER for role in roles}
    assignment = {}
    for pair in pairs:
        role, sep, who = pair.partition("=")
        if not sep or role not in roles or not ID_RE.fullmatch(who):
            raise WorkflowError(f"--assign {pair!r}: expected ROLE=WHO with ROLE one of {roles} and WHO a profile name or {RUNNER!r}")
        assignment[role] = who
    holders = {s["profile"] for s in wf["steps"] if not s.get("human")}
    if wf["coordinator"] not in holders:
        # Coordinating is what running the workflow means, unless said otherwise.
        assignment.setdefault(wf["coordinator"], RUNNER)
    missing = sorted(set(roles) - set(assignment))
    if missing:
        raise WorkflowError(f"{wf['name']}: no --assign for {missing} (or use --solo)")
    return assignment


def actor(step: dict, assignment: dict[str, str] | None = None) -> str:
    if step.get("human"):
        if step.get("who"):
            return step["who"]
        return "the owner" if step["decided_by"] == "owner" else f"the human named by `{step['decided_by']}`"
    who = step["profile"] if assignment is None else assignment[step["profile"]]
    return "you" if who == RUNNER else f"`{who}`"


def render_skill(wf: dict, registry: dict, coordinators: dict[str, str],
                 assignment: dict[str, str] | None = None) -> str:
    """Render one definition as a Hermes skill.

    `assignment` maps every pack profile the definition names to the profile that holds
    that role in the reader's team, or to RUNNER for the profile running the workflow.
    Without it each role is its own pack profile (the rendering shipped in this repo).
    `coordinators` gives, per follow-on workflow, who coordinates it (a profile or RUNNER).
    """
    name = wf["name"]
    steps = wf["steps"]
    holders = [s["profile"] if assignment is None else assignment[s["profile"]]
               for s in steps if not s.get("human")]
    solo = all(h == RUNNER for h in holders)        # one profile holds every role
    mixed = not solo and RUNNER in holders          # the runner holds some roles
    others = sorted({h for h in holders if h != RUNNER})
    settings = list(dict.fromkeys([BOARD, *([] if solo else [HANDOFF]), *(wf.get("uses_settings") or [])]))
    config = "\n".join(
        f"      - {{key: {key}, description: {json.dumps(first_sentence(registry[key]['meaning']), ensure_ascii=False)}, "
        f"default: {json.dumps(registry[key]['default'], ensure_ascii=False)}}}"
        for key in settings
    )
    always = wf.get("all_steps_load") or []
    has_human = any(s.get("human") for s in steps)
    rounds = wf.get("max_fix_rounds", DEFAULT_FIX_ROUNDS)
    has_loop = any(s.get("on_fail") or s.get("on_reject") for s in steps)
    stop_to = "ask the owner through `owner.channel`" if has_human else "report to whoever started the workflow"
    if solo:
        notice = ["> **One profile holds every role here.** The description below was written for a team of "
                  "profiles. In this setup you run every step yourself, and no second profile checks the work.",
                  ""]
        mode = ("You run every step of this workflow yourself, loading each step's skills as you reach it. "
                "Keep the steps separate and in order: each one still produces its own output. Never report a "
                "step as independently reviewed or verified. "
                + ("The human step is the only independent check, so give that person the evidence itself, "
                   "not your summary of it. " if has_human else
                   "Nobody else checks this work: say so in the report. "))
    elif mixed:
        notice = []
        mode = ("You coordinate this workflow and run the steps marked \"you\" yourself, loading each step's "
                "skills as you reach it. A step that names another profile belongs to that profile; never run "
                "it yourself. ")
    else:
        notice = []
        mode = ("You coordinate this workflow. Each step belongs to one profile, which runs it with its own "
                "skills; never run another profile's step yourself. ")

    lines = [
        "---",
        f"name: {name}",
        f"description: {json.dumps(wf['description'])}",
        "metadata:",
        "  hermes:",
        f"    tags: [workflow, {'single-profile' if solo else 'multi-profile'}]",
        "    config:",
        config,
        "    prerequisites:",
        "      commands: [hermes]",
        "---",
        f"# Workflow: {name}",
        "",
        *notice,
        wf["summary"].strip(),
        "",
        f"{mode}This file is generated from "
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
        lines.append(f"| {i} | `{s['id']}` | {actor(s, assignment)} | {loads} | {_code(s.get('needs') or [])} | {s['output'].strip()} |")
    if always:
        lines += ["", f"Every profile step also loads {_code(always)}."]
    for i, s in enumerate(steps, 1):
        lines += ["", f"### {i}. `{s['id']}` — {actor(s, assignment)}", s["does"].strip()]
        if s.get("human"):
            lines.append(f"- Asks: {s['asks'].strip()}")
            if s["decided_by"] != "owner":
                lines.append(f"- Who acts follows `{s['decided_by']}`.")
            if s.get("on_reject"):
                lines.append(f"- On a change request the work goes back to `{s['on_reject']}` with the answer verbatim; "
                             "the steps after it run again, then this question is asked again. A plain no stops the workflow.")
            else:
                lines.append("- A no stops the workflow at this step.")
        for extra in s.get("extra_skills", []) or []:
            lines.append(f"- Also loads `{extra['skill']}` when {extra['when'].strip()}.")
        if s.get("optional_when"):
            lines.append(f"- Runs only when {s['optional_when'].strip()}. Otherwise it is recorded as skipped, with that reason.")
        if s.get("on_fail"):
            lines.append(f"- On failure the work goes back to `{s['on_fail']}` with the findings; "
                         "every step that depends on it then runs again.")

    if has_loop:
        lines += [
            "",
            "### When a step sends the work back",
            "A verdict belongs to the head it was given on. After a fix, every step that depends on the "
            "fixed step runs again on the new head, including checks that had already passed: a pass on "
            "an older head is void. Count the rounds per target step. After "
            f"{rounds} round{'s' if rounds != 1 else ''} on the same step, stop and {stop_to}, with the "
            "findings of every round, instead of starting another.",
        ]
    lines += [
        "",
        "## Prerequisites",
        "| Needs | Why | Check |",
        "|---|---|---|",
    ]
    if others:
        lines.append(f"| Profiles installed: {_code(others)} | "
                     f"{'their steps run as those profiles' if mixed else 'each step runs as its own profile'} | "
                     "`hermes profile list` |")
        lines.append("| A way to hand a step to another profile, when there is no board (`delivery.handoff`) | "
                     "steps that are not yours | the profile answers a test brief |")
    lines.append("| The `kanban` toolset, when `delivery.board` is `hermes-kanban` | one card per step | `kanban_list` answers |")
    if has_human:
        lines.append("| A way to reach the owner (`owner.channel`) | human steps | the owner answers there |")
    lines += [
        "",
        "If a required prerequisite is missing, stop before step 1. Say which one, what it blocks, and the "
        "smallest access that would unblock it. "
        + ("Never report a step done that you did not complete." if solo else
           "A step whose profile is not installed is never run under another profile: report the workflow "
           "as blocked at that step. Never report a step done that its profile did not complete."),
        "",
        "## Configuration",
        "- `delivery.board` decides how the workflow runs (below).",
    ]
    if not solo:
        lines.append("- `delivery.handoff` decides how a step reaches another profile when no board runs the "
                     "workflow (below).")
    for key in [k for k in settings if k not in (BOARD, HANDOFF)]:
        deciders = [s["id"] for s in steps if s.get("decided_by") == key]
        note = f" Decides who acts at {_code(deciders)}." if deciders else ""
        lines.append(f"- `{key}`: {registry[key]['meaning']}{note}")
    assignee = ("your own profile" if solo else
                "the step's profile (your own for a step marked \"you\")" if mixed else "the step's profile")
    fixer = "the target step" if solo else "the target step's profile"
    tracker_note = ("With `tracker`, record each step's start, output and decision as comments on the "
                    "work item.")
    if solo:
        without_board = [
            "Work through the steps in dependency order, loading each step's skills as you reach it, and "
            "check each output against \"Produces\" before the next step. On a failed check or a change "
            "request, go back to the step named with the findings, then run again every step that depends "
            "on it. At a human step, "
            f"ask through `owner.channel` and wait. {tracker_note}",
        ]
    else:
        without_board = [
            "Run the steps in dependency order. "
            + ("Do the steps marked \"you\" yourself. " if mixed else
               "A step that names your own profile is yours to do. ")
            + "Hand every other step to its profile the way `delivery.handoff` says:",
            "- `profile-turn`: one non-interactive turn of that profile, for example "
            "`hermes -p <profile> chat -Q -s <skills> --query-file <brief file>`. Its final reply is the "
            "step's output. Never add a flag that skips approvals.",
            "- `channel`: post the brief in that profile's channel and wait for its answer there.",
            "- `owner-relay`: give the brief to the owner through `owner.channel` and ask them to pass it on.",
            "",
            "The brief carries the step's instructions, its skills, the work item and the outputs of its "
            "After steps. Wait for the output and check it against \"Produces\"; an answer that does not "
            "produce it is not a completed step. On a failure or a change request, send the work back as "
            "the step says and rerun what depends on it. At a human step, ask "
            f"through `owner.channel` and wait. {tracker_note}",
        ]
    lines += [
        "",
        "Current values appear in the `[Skill config]` block when this skill loads; an unset key shows its "
        "declared default. Persist a value with `hermes config set skills.config.<key> <value>` (per "
        "profile: `hermes -p <profile> config set …`); `hermes config migrate` prompts for keys still unset.",
        "",
        "## Run it",
        "### On a Hermes Kanban board (`delivery.board: hermes-kanban`)",
        f"1. Create every card up front, in step order, with `kanban_create`: title `{name}: <step> — <work item>`, "
        f"`assignee` {assignee}, `skills` the step's skills (plus the ones every step loads, and any "
        "extra skill whose condition holds), `parents` the cards of its After steps, and a body with the "
        "step's instructions, what it must produce and a link to the work item. For a step with an \"On "
        "failure\" target, the body also says: on a problem, comment the findings and block the card "
        "instead of completing it. The dispatcher starts each card when its parents are done.",
        "2. A human step is a card assigned to you. When it starts, ask through `owner.channel` and block it "
        "with `kanban_block(kind=\"needs_input\")`. On a go, comment the answer verbatim and complete the "
        "card; a human action (such as a merge) is complete only once you have verified it happened. On a "
        "change request, comment it verbatim and follow the step's \"On a change request\" line. On a "
        "plain no, comment it, leave the card blocked, and report the workflow stopped at that step.",
        "3. An optional step whose condition does not hold is completed with `skipped: <reason>`, so the "
        "steps after it proceed.",
        "4. A step with an \"On failure\" target that finds a problem comments its findings and blocks its "
        f"card. Create a fix card for {fixer} with the findings, make it a parent of the "
        "checking card (`kanban_link(parent_id=<fix>, child_id=<check>)`), and unblock the checking card "
        "(`kanban_unblock`): it waits until the fix is done, then runs again. For every other step that "
        "depends on the fixed step and already completed, create a new card (same title plus "
        "`— round <n>`) with the fix card as parent, so it runs again on the new head.",
        "",
        "### Without a board (`delivery.board: none` or `tracker`)",
        *without_board,
        "",
        "## Done when",
        *[f"- {item.strip()}" for item in wf["done_when"]],
        "- Every step is done, or skipped with the reason its condition did not hold; every human decision "
        "is recorded verbatim.",
    ]
    if wf.get("then"):
        lines += ["", "## Then"]
        for follow in wf["then"]:
            if coordinators[follow] == RUNNER:
                lines.append(f"- Start `{follow}` yourself.")
            else:
                lines.append(f"- Start `{follow}`, coordinated by `{coordinators[follow]}`.")
    lines += [
        "",
        "## Report",
        "Each update names the workflow, the current step and its actor, links the cards or the work "
        "item, and says what is needed from whom, if anything."
        + (" It also says that one profile ran every step." if solo else ""),
        "",
    ]
    if assignment is not None:
        lines += [
            "## Roles here",
            "| Role in the definition | Held by |",
            "|---|---|",
            *[f"| `{role}` | {'you' if who == RUNNER else f'`{who}`'} |" for role, who in sorted(assignment.items())],
            "",
            "The definition, with its original roles, is in `references/workflow.yaml`.",
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
    orchestrators = load_orchestrators(root)
    for path, wf in defs:
        errors += validate(path, wf, profiles, registry, names, orchestrators)
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


def render_for(root: Path, name: str, pairs: list[str], solo: bool) -> str:
    """One valid definition rendered for a team's own role assignment."""
    _, errors = build(root)
    if errors:
        raise WorkflowError("\n".join(errors))
    workflows = {wf["name"]: wf for _, wf in definitions(root)}
    if name not in workflows:
        raise WorkflowError(f"unknown workflow {name!r}; defined: {sorted(workflows)}")
    wf = workflows[name]
    assignment = assignment_from(wf, pairs, solo)
    # A follow-on workflow is coordinated by whoever holds its coordinator's role here;
    # a role this assignment does not cover keeps its pack profile.
    coordinators = {n: assignment.get(w["coordinator"], w["coordinator"]) for n, w in workflows.items()}
    return render_skill(wf, load_registry(root), coordinators, assignment)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true", help="validate and report drift without writing")
    parser.add_argument("--render", metavar="NAME", help="print one workflow rendered for a role assignment")
    parser.add_argument("--solo", action="store_true", help="with --render: one profile holds every role")
    parser.add_argument("--assign", action="append", default=[], metavar="ROLE=WHO",
                        help=f"with --render: who holds a role, a profile name or {RUNNER!r} (repeat per role)")
    args = parser.parse_args()
    try:
        if args.render:
            sys.stdout.write(render_for(ROOT, args.render, args.assign, args.solo))
            return 0
        if args.solo or args.assign:
            parser.error("--solo and --assign need --render NAME")
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
