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
MANIFEST = ROOT / "immo.json"
RULES = ROOT / "shared" / "RULES.md"
START = "<!-- shared-rules:start -->\n"
END = "<!-- shared-rules:end -->\n"
NAME_RE = re.compile(r"^immo-[a-z0-9]+(?:-[a-z0-9]+)*$")
SKILL_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
PROFILE_REF_RE = re.compile(r"`(immo-[a-z0-9]+(?:-[a-z0-9]+)*)`")
DISTRIBUTION_KEYS = ["name", "version", "description", "author", "license"]
MIN_JOBS, MAX_JOBS = 3, 5
# Category containers that the repository capability tooling (capabilities.py --write)
# materializes supplemental skills into; they are not role-owned jobs. Same set as
# hermes-agency/validate.py.
GENERATED_SKILL_DIRS = {"capabilities", "software-development", "research", "productivity", "creative", "autonomous-ai-agents", "web"}
FRONTMATTER_KEYS = {"name", "description", "metadata", "required_environment_variables", "required_credential_files"}
MAX_DESCRIPTION = 60  # Hermes clips skill-index descriptions at 60 characters.
REQUIRED_SECTIONS = ("## Prérequis", "## Configuration")
PREREQ_TABLE = "| Besoin | Pourquoi | Vérification |"
# Shared keys from docs/PORTABLE_SKILLS.md that this pack may declare, with their registry default.
KNOWN_CONFIG = {
    "immo.fiche_investisseur": "memory",
    "immo.registre_questions": "memory",
    "immo.juridictions": "detect",
    "immo.bibliotheque_ouvrages": "none",
    "owner.channel": "this conversation",
}
STALE_COMMAND = "hermes skills " + "config"  # only enables/disables skills; it sets no value
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
    lines = body.splitlines()
    for heading in REQUIRED_SECTIONS:
        if heading not in lines:
            errors.append(f"{label}: missing {heading} section")
    if PREREQ_TABLE not in section(body, "## Prérequis"):
        errors.append(f"{label}: ## Prérequis needs the table {PREREQ_TABLE}")
    return errors


def check_shared_block(name: str, soul: Path, rules: str) -> list[str]:
    text = soul.read_text(encoding="utf-8")
    if text.count(START) != 1 or text.count(END) != 1:
        return [f"{name}: SOUL.md must contain exactly one shared-rules block"]
    if not text.endswith(START + rules + END):
        return [f"{name}: shared-rules block differs from shared/RULES.md (run: python sync_shared.py)"]
    body = text[: text.index(START)]
    if not body.strip():
        return [f"{name}: SOUL.md has no role body before the shared-rules block"]
    return []


def main() -> int:
    errors: list[str] = []
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    entries = manifest.get("profiles", [])
    names = [item.get("name") for item in entries]

    if manifest.get("name") != "hermes-immo":
        errors.append("manifest name must be hermes-immo")
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

    if not RULES.is_file():
        errors.append("missing shared/RULES.md")
        rules = ""
    else:
        rules = RULES.read_text(encoding="utf-8")
        if START in rules or END in rules:
            errors.append("shared/RULES.md must not contain the block markers")

    config_defaults: dict[str, set[str]] = {}
    for item in entries:
        name = item["name"]
        if not NAME_RE.fullmatch(name):
            errors.append(f"invalid Immo profile name: {name}")
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
            if rules:
                errors.extend(check_shared_block(name, soul, rules))
            for ref in sorted(set(PROFILE_REF_RE.findall(soul.read_text(encoding="utf-8")))):
                if ref not in expected:
                    errors.append(f"{name}: SOUL.md names unknown profile {ref}")
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

        skill_root = root / "skills"
        skill_names: set[str] = set()
        if skill_root.is_dir():
            for child in sorted(skill_root.iterdir()):
                if child.name in GENERATED_SKILL_DIRS:
                    continue
                if not child.is_dir():
                    errors.append(f"{name}: unexpected file under skills/: {child.name}")
                    continue
                extra = sorted(p.name for p in child.iterdir() if p.name != "SKILL.md")
                if extra:
                    errors.append(f"{name}/{child.name}: only SKILL.md belongs in a job directory, found {extra}")
                if not (child / "SKILL.md").is_file():
                    errors.append(f"{name}/{child.name}: job directory without SKILL.md")
        for skill in sorted(skill_root.glob("*/SKILL.md")):
            skill_name = skill.parent.name
            if skill_name in GENERATED_SKILL_DIRS:
                continue
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
        if STALE_COMMAND in text:
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
        f"Hermes Immo validation passed: {len(entries)} profiles, {sum(len(p['jobs']) for p in entries)} skills, "
        f"shared rules identical in every SOUL, {len(config_defaults)} config keys, frontmatter checked with {parser}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
