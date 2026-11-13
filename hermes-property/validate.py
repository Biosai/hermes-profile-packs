#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

try:  # PyYAML is optional: without it, nested frontmatter is only shallowly checked.
    import yaml
except ImportError:  # pragma: no cover - depends on the environment
    yaml = None

ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "property.json"
NAME_RE = re.compile(r"^property-[a-z0-9]+(?:-[a-z0-9]+)*$")
SKILL_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
PROFILE_REF_RE = re.compile(r"`(property-[a-z0-9]+(?:-[a-z0-9]+)*)`")
DISTRIBUTION_KEYS = ["name", "version", "description", "author", "license", "preload_skills"]
MIN_JOBS, MAX_JOBS = 3, 5
# Category containers that the repository capability tooling (capabilities.py --write)
# materializes supplemental skills into; they are not role-owned jobs. Same set as
# hermes-agency/validate.py.
GENERATED_SKILL_DIRS = {"capabilities", "software-development", "research", "productivity", "creative", "autonomous-ai-agents", "web", "workflows"}  # workflows: rendered by scripts/sync_workflows.py and validated there
# The panel's shared rules: one canonical skill in <repo>/shared-skills/panel-rules, copied
# byte-identical into every profile by scripts/sync_shared_skills.py and preloaded by each
# distribution.yaml. A shared skill is shipped by the profile but is not one of its jobs.
SHARED_SKILLS = ["panel-rules"]
SHARED_SOURCE = ROOT.parent / "shared-skills"
FRONTMATTER_KEYS = {"name", "description", "metadata", "required_environment_variables", "required_credential_files"}
MAX_DESCRIPTION = 60  # Hermes clips skill-index descriptions at 60 characters.
# Upstream SOUL shape: a title and exactly these six sections, in this order.
SOUL_SECTIONS = ["## Role", "## Responsibilities", "## Working standard", "## Collaboration", "## Communication", "## Definition of done"]
SOUL_MIN_WORDS, SOUL_MAX_WORDS = 250, 450
SOUL_PRINCIPLE = "do not replace"  # "you prepare the real professional's work; you do not replace them"
MIN_COLLABORATORS = 3
# Upstream skill shape, plus the two portability sections of docs/PORTABLE_SKILLS.md:
# "# Title", one line starting "Use when", then exactly these sections, in this order.
SKILL_SECTIONS = ["## Prerequisites", "## Configuration", "## Procedure", "## Decision rules", "## Quality gate"]
USE_WHEN = "Use when "
MAX_SKILL_WORDS = 650
PREREQ_TABLE = "| Needs | Why | Check |"
STOP_RULE = "stop before step 1"
REFERENCE_RE = re.compile(r"references/[A-Za-z0-9._-]+\.md")
STEP_RE = re.compile(r"^\d+\. ")
# Shared keys from docs/PORTABLE_SKILLS.md that this pack may declare, with their registry default.
KNOWN_CONFIG = {
    "property.investor_file": "memory",
    "property.question_register": "memory",
    "property.jurisdictions": "detect",
    "property.cost_library": "none",
    "owner.channel": "this conversation",
}
STALE_COMMAND = "hermes skills " + "config"  # only enables/disables skills; it sets no value
RETIRED_MARKER = "shared-rules:"  # the rules used to be inlined in every SOUL between two markers
FORBIDDEN = [
    re.compile(r"/home/[A-Za-z0-9._-]+/"),
    re.compile(r"BEGIN (?:RSA |OPENSSH |EC )?PRIVATE KEY"),
    re.compile(r"(?i)(?:api[_-]?key|access[_-]?token|refresh[_-]?token|password)\s*[:=]\s*[\"'][^\"']{8,}"),
    re.compile(r"-100[0-9]{6,}"),
    re.compile(r"§D[0-9]"),
]


def parse_distribution(path: Path) -> tuple[list[str], dict[str, str]]:
    keys: list[str] = []
    data: dict[str, str] = {}
    for raw in path.read_text(encoding="utf-8").splitlines():
        if ":" not in raw or raw.lstrip().startswith("#"):
            continue
        key, value = raw.split(":", 1)
        keys.append(key.strip())
        data[key.strip()] = value.strip().strip('"').strip("'")
    return keys, data


def distribution_list(path: Path, key: str) -> list[str]:
    """Items of a top-level YAML block list such as preload_skills."""
    values: list[str] = []
    active = False
    for raw in path.read_text(encoding="utf-8").splitlines():
        if raw == f"{key}:":
            active = True
        elif active and raw and not raw[0].isspace():
            break
        elif active and raw.strip().startswith("- "):
            values.append(raw.strip()[2:].strip().strip('"').strip("'"))
    return values


def split_skill(path: Path) -> tuple[str, str] | None:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return None
    parts = text.split("---\n", 2)
    if len(parts) < 3:
        return None
    return parts[1], parts[2]


def parse_frontmatter(raw: str) -> dict:
    """Parse with PyYAML when available; otherwise read top-level scalar keys only."""
    if yaml is not None:
        data = yaml.safe_load(raw)
        return data if isinstance(data, dict) else {}
    data: dict = {}
    for line in raw.splitlines():
        if not line or line[0].isspace() or ":" not in line:
            continue
        key, value = line.split(":", 1)
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        data[key.strip()] = value if value else {}
    return data


def section(body: str, heading: str) -> str:
    lines = body.splitlines()
    if heading not in lines:
        return ""
    start = lines.index(heading) + 1
    end = next((i for i in range(start, len(lines)) if lines[i].startswith("## ")), len(lines))
    return "\n".join(lines[start:end])


def headings(text: str) -> list[str]:
    return [line for line in text.splitlines() if line.startswith("## ")]


def paragraphs(text: str) -> list[str]:
    return [block for block in re.split(r"\n\s*\n", text.strip("\n")) if block.strip()]


def tree(path: Path) -> dict[str, bytes]:
    return {
        str(p.relative_to(path)): p.read_bytes()
        for p in sorted(path.rglob("*"))
        if p.is_file() and "__pycache__" not in p.parts and p.suffix != ".pyc"
    }


def check_template(label: str, text: str, body: str) -> list[str]:
    """The upstream skill shape: title, "Use when" line, then the five sections in order."""
    errors: list[str] = []
    content = [line for line in body.splitlines() if line.strip()]
    if not content or not content[0].startswith("# "):
        errors.append(f"{label}: the body must start with a '# Title' line")
    lead = paragraphs(body.split("\n## ", 1)[0])
    if len(lead) != 2 or "\n" in lead[1] or not lead[1].startswith(USE_WHEN) or not lead[1].endswith("."):
        errors.append(f"{label}: the title must be followed by exactly one line starting '{USE_WHEN.strip()}'")
    found = headings(body)
    if found != SKILL_SECTIONS:
        errors.append(f"{label}: sections must be exactly {[h[3:] for h in SKILL_SECTIONS]}, found {[h[3:] for h in found]}")
        return errors
    prerequisites = section(body, "## Prerequisites")
    if PREREQ_TABLE not in prerequisites:
        errors.append(f"{label}: ## Prerequisites needs the table {PREREQ_TABLE}")
    if STOP_RULE not in " ".join(prerequisites.split()):
        errors.append(f"{label}: ## Prerequisites needs the stop rule ('{STOP_RULE}')")
    steps = [line for line in section(body, "## Procedure").splitlines() if line.strip() and not line[0].isspace()]
    if not steps or not steps[0].startswith("1. ") or not all(STEP_RE.match(line) for line in steps):
        errors.append(f"{label}: ## Procedure must be a numbered list starting at 1")
    rules = [line for line in section(body, "## Decision rules").splitlines() if line.strip() and not line[0].isspace()]
    if not rules or not all(line.startswith("- ") for line in rules):
        errors.append(f"{label}: ## Decision rules must be a bullet list")
    gate = paragraphs(section(body, "## Quality gate"))
    if len(gate) != 1 or gate[0].lstrip().startswith(("- ", "|")) or STEP_RE.match(gate[0].lstrip()):
        errors.append(f"{label}: ## Quality gate must be one paragraph")
    words = len(text.split())
    if words > MAX_SKILL_WORDS:
        errors.append(f"{label}: SKILL.md has {words} words (max {MAX_SKILL_WORDS}); move detail to references/")
    return errors


def check_references(label: str, folder: Path, text: str, procedure: str) -> list[str]:
    """A skill folder holds SKILL.md and, optionally, references/*.md linked from its Procedure."""
    errors: list[str] = []
    extra = sorted(p.name for p in folder.iterdir() if p.name not in {"SKILL.md", "references"})
    if extra:
        errors.append(f"{label}: only SKILL.md and references/ belong in a skill directory, found {extra}")
    linked = set(REFERENCE_RE.findall(procedure))
    references = folder / "references"
    present: set[str] = set()
    if references.exists():
        if not references.is_dir():
            return errors + [f"{label}: references must be a directory"]
        for item in sorted(references.iterdir()):
            if not item.is_file() or item.suffix != ".md":
                errors.append(f"{label}: references/ holds Markdown files only, found {item.name}")
                continue
            present.add(f"references/{item.name}")
        if not present:
            errors.append(f"{label}: empty references/ directory")
    for name in sorted(present - linked):
        errors.append(f"{label}: {name} is not linked from the ## Procedure of SKILL.md")
    for name in sorted(set(REFERENCE_RE.findall(text)) - present):
        errors.append(f"{label}: SKILL.md links {name}, which does not exist")
    return errors


def check_skill(label: str, skill_name: str, path: Path, defaults: dict[str, set[str]]) -> list[str]:
    errors: list[str] = []
    parts = split_skill(path)
    if parts is None:
        return [f"{label}: SKILL.md must start with YAML frontmatter"]
    raw, body = parts
    try:
        meta = parse_frontmatter(raw)
    except Exception as exc:  # yaml.YAMLError and friends
        return [f"{label}: frontmatter is not valid YAML: {exc}"]
    extra = sorted(set(meta) - FRONTMATTER_KEYS)
    if extra:
        errors.append(f"{label}: unexpected frontmatter keys {extra}")
    if meta.get("name") != skill_name:
        errors.append(f"{label}: frontmatter name must match the directory")
    description = meta.get("description")
    if not isinstance(description, str) or not description.strip():
        errors.append(f"{label}: frontmatter missing description")
    elif len(description) > MAX_DESCRIPTION:
        errors.append(f"{label}: description is {len(description)} characters (max {MAX_DESCRIPTION})")
    if yaml is not None:
        metadata = meta.get("metadata") or {}
        hermes = metadata.get("hermes") or {} if isinstance(metadata, dict) else None
        if not isinstance(hermes, dict):
            errors.append(f"{label}: metadata.hermes must be a mapping")
            hermes = {}
        config = hermes.get("config") or []
        if not isinstance(config, list):
            errors.append(f"{label}: metadata.hermes.config must be a list")
            config = []
        configuration = section(body, "## Configuration")
        for entry in config:
            if not isinstance(entry, dict) or set(entry) != {"key", "description", "default"}:
                errors.append(f"{label}: each config entry needs exactly key, description, default")
                continue
            key = entry["key"]
            if key not in KNOWN_CONFIG:
                errors.append(f"{label}: config key {key} is not in the pack's registry subset")
                continue
            if str(entry["default"]) != KNOWN_CONFIG[key]:
                errors.append(f"{label}: {key} default must be {KNOWN_CONFIG[key]!r}")
            defaults.setdefault(key, set()).add(str(entry["default"]))
            if f"`{key}`" not in configuration:
                errors.append(f"{label}: ## Configuration does not explain {key}")
        for field in ("required_environment_variables", "required_credential_files"):
            value = meta.get(field)
            if value is not None and not isinstance(value, list):
                errors.append(f"{label}: {field} must be a list")
    text = path.read_text(encoding="utf-8")
    errors.extend(check_template(label, text, body))
    errors.extend(check_references(label, path.parent, text, section(body, "## Procedure")))
    return errors


def check_soul(name: str, display_name: str, soul: Path, roster: set[str]) -> list[str]:
    """The upstream SOUL shape: a title, six sections, and no inlined shared rules."""
    errors: list[str] = []
    text = soul.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0] != f"# {display_name}":
        errors.append(f"{name}: SOUL.md must start with '# {display_name}'")
    found = headings(text)
    if found != SOUL_SECTIONS:
        errors.append(f"{name}: SOUL.md sections must be exactly {[h[3:] for h in SOUL_SECTIONS]}, found {[h[3:] for h in found]}")
    words = len(text.split())
    if not SOUL_MIN_WORDS <= words <= SOUL_MAX_WORDS:
        errors.append(f"{name}: SOUL.md has {words} words (expected {SOUL_MIN_WORDS}-{SOUL_MAX_WORDS}); move role detail to a skill or its references/")
    if RETIRED_MARKER in text:
        errors.append(f"{name}: SOUL.md still inlines the shared rules; they live in the preloaded skill {SHARED_SKILLS[0]}")
    if SOUL_PRINCIPLE not in " ".join(section(text, "## Role").split()):
        errors.append(f"{name}: ## Role must say that the profile prepares the real professional's work and does not replace them")
    for skill in SHARED_SKILLS:
        if f"`{skill}`" not in section(text, "## Working standard"):
            errors.append(f"{name}: ## Working standard must point to the preloaded skill {skill}")
    for ref in sorted(set(PROFILE_REF_RE.findall(text))):
        if ref not in roster:
            errors.append(f"{name}: SOUL.md names unknown profile {ref}")
    collaborators = set(PROFILE_REF_RE.findall(section(text, "## Collaboration"))) & roster - {name}
    if len(collaborators) < MIN_COLLABORATORS:
        errors.append(f"{name}: ## Collaboration must name at least {MIN_COLLABORATORS} other property profiles")
    return errors


def check_shared_skills(name: str, root: Path, canonical: dict[str, dict[str, bytes]]) -> list[str]:
    """Every profile preloads the shared skills and ships a byte-identical copy of each."""
    errors: list[str] = []
    preload = distribution_list(root / "distribution.yaml", "preload_skills")
    if preload != SHARED_SKILLS:
        errors.append(f"{name}: distribution preload_skills must be {SHARED_SKILLS}, got {preload}")
    for skill in SHARED_SKILLS:
        copy = root / "skills" / skill
        if not (copy / "SKILL.md").is_file():
            errors.append(f"{name}: preloads {skill} but does not ship skills/{skill}/SKILL.md")
            continue
        wanted = canonical.setdefault(skill, tree(copy))
        if tree(copy) != wanted:
            errors.append(f"{name}: skills/{skill} differs from the canonical shared skill (run: python scripts/sync_shared_skills.py)")
    return errors


def main() -> int:
    errors: list[str] = []
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    entries = manifest.get("profiles", [])
    names = [item.get("name") for item in entries]

    if manifest.get("name") != "hermes-property":
        errors.append("manifest name must be hermes-property")
    if manifest.get("profile_count") != len(entries):
        errors.append("manifest profile_count does not match profiles list")
    duplicates = [name for name, count in Counter(names).items() if count > 1]
    if duplicates:
        errors.append(f"duplicate manifest profiles: {duplicates}")
    orchestrator = manifest.get("orchestrator")
    if orchestrator not in names:
        errors.append("manifest orchestrator is not installed in roster")
    backbone = manifest.get("backbone_profiles", [])
    if orchestrator not in backbone:
        errors.append("manifest orchestrator is not in backbone_profiles")
    unknown_backbone = sorted(set(backbone) - set(names))
    if unknown_backbone:
        errors.append(f"backbone_profiles not in roster: {unknown_backbone}")
    categories = Counter(item.get("category") for item in entries)
    if dict(categories) != manifest.get("categories"):
        errors.append(f"manifest categories do not match roster: {dict(categories)}")

    expected = set(names)
    actual = {p.name for p in (ROOT / "profiles").iterdir() if p.is_dir()}
    if expected != actual:
        errors.append(f"profile directory mismatch: missing={sorted(expected-actual)} extra={sorted(actual-expected)}")

    for retired in ("shared", "sync_shared.py"):
        if (ROOT / retired).exists():
            errors.append(f"{retired} is retired: the shared rules are the skill {SHARED_SKILLS[0]} in the repository's shared-skills/")

    # Inside the repository the canonical source is shared-skills/<skill>; a pack copied on its
    # own still requires the copies to be identical across its profiles.
    canonical: dict[str, dict[str, bytes]] = {}
    for skill in SHARED_SKILLS:
        if (SHARED_SOURCE / skill / "SKILL.md").is_file():
            canonical[skill] = tree(SHARED_SOURCE / skill)

    config_defaults: dict[str, set[str]] = {}
    for item in entries:
        name = item["name"]
        if not NAME_RE.fullmatch(name):
            errors.append(f"invalid Hermes Property profile name: {name}")
            continue
        for field in ("display_name", "category", "description", "role"):
            if not str(item.get(field, "")).strip():
                errors.append(f"{name}: manifest entry missing {field}")
        root = ROOT / "profiles" / name
        dist = root / "distribution.yaml"
        soul = root / "SOUL.md"
        if not dist.is_file():
            errors.append(f"{name}: missing distribution.yaml")
            continue
        if not soul.is_file():
            errors.append(f"{name}: missing SOUL.md")
        else:
            errors.extend(check_soul(name, str(item.get("display_name", "")), soul, expected))
        if (root / ".no-bundled-skills").exists():
            errors.append(f"{name}: unexpected .no-bundled-skills file")
        keys, meta = parse_distribution(dist)
        if keys != DISTRIBUTION_KEYS:
            errors.append(f"{name}: distribution keys must be exactly {DISTRIBUTION_KEYS}, got {keys}")
        if meta.get("name") != name:
            errors.append(f"{name}: distribution name mismatch")
        if meta.get("version") != manifest.get("version"):
            errors.append(f"{name}: distribution version does not match pack version")
        for field in ("version", "description", "author", "license"):
            if not meta.get(field):
                errors.append(f"{name}: distribution missing {field}")
        errors.extend(check_shared_skills(name, root, canonical))

        skill_root = root / "skills"
        skill_names: set[str] = set()
        if skill_root.is_dir():
            for child in sorted(skill_root.iterdir()):
                if child.name in GENERATED_SKILL_DIRS:
                    continue
                if not child.is_dir():
                    errors.append(f"{name}: unexpected file under skills/: {child.name}")
                    continue
                if not (child / "SKILL.md").is_file():
                    errors.append(f"{name}/{child.name}: skill directory without SKILL.md")
        for skill in sorted(skill_root.glob("*/SKILL.md")):
            skill_name = skill.parent.name
            if skill_name in GENERATED_SKILL_DIRS:
                continue
            if skill_name not in SHARED_SKILLS:
                skill_names.add(skill_name)
            if not SKILL_RE.fullmatch(skill_name):
                errors.append(f"{name}: invalid skill name {skill_name}")
            errors.extend(check_skill(f"{name}/{skill_name}", skill_name, skill, config_defaults))
        if not skill_names:
            errors.append(f"{name}: no profile-specific skills")
        jobs = item.get("jobs", [])
        if not MIN_JOBS <= len(jobs) <= MAX_JOBS:
            errors.append(f"{name}: expected {MIN_JOBS}-{MAX_JOBS} jobs, found {len(jobs)}")
        if set(jobs) != skill_names:
            errors.append(f"{name}: jobs do not match skills: jobs={sorted(jobs)} skills={sorted(skill_names)}")

    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts or "__pycache__" in path.parts or path.suffix == ".pyc":
            continue
        if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".gif", ".webp"}:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        generated = len(path.parts) > len(ROOT.parts) + 4 and path.relative_to(ROOT).parts[3] in GENERATED_SKILL_DIRS
        if STALE_COMMAND in text and not generated:
            errors.append(f"{path.relative_to(ROOT)}: use hermes config set skills.config.<key>, not {STALE_COMMAND}")
        for pattern in FORBIDDEN:
            if pattern.search(text):
                errors.append(f"forbidden portable-content pattern in {path.relative_to(ROOT)}: {pattern.pattern}")

    for key, values in sorted(config_defaults.items()):
        if len(values) > 1:
            errors.append(f"config key {key} has inconsistent defaults across skills: {sorted(values)}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    parser = "PyYAML" if yaml is not None else "shallow parser (PyYAML not installed)"
    print(
        f"Hermes Property validation passed: {len(entries)} profiles with six-section SOULs, "
        f"{sum(len(p['jobs']) for p in entries)} role skills in the upstream template, "
        f"{', '.join(SHARED_SKILLS)} preloaded and shipped in every profile, "
        f"{len(config_defaults)} config keys, frontmatter checked with {parser}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
