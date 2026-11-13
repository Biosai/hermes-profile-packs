import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover - depends on the environment
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
CANONICAL_SHARED = ROOT.parent / "shared-skills"
SHARED_SKILLS = ["panel-rules"]
KNOWN_CONFIG = {
    "property.investor_file": "memory",
    "property.question_register": "memory",
    "property.jurisdictions": "detect",
    "property.cost_library": "none",
    "owner.channel": "this conversation",
}
SOUL_SECTIONS = [
    "## Role", "## Responsibilities", "## Working standard", "## Collaboration", "## Communication",
    "## Definition of done",
]
SKILL_SECTIONS = ["## Prerequisites", "## Configuration", "## Procedure", "## Decision rules", "## Quality gate"]
MAX_SKILL_WORDS = 650
GENDERED = re.compile(r"\b(?:he|him|his|himself)\b", re.IGNORECASE)


GENERATED_SKILL_DIRS = {
    "capabilities", "software-development", "research", "productivity", "creative", "autonomous-ai-agents", "web",
}


def skill_files(shared=True):
    """Role-owned SKILL.md files, plus the profile copies of the shared skills unless shared=False."""
    skip = GENERATED_SKILL_DIRS if shared else GENERATED_SKILL_DIRS | set(SHARED_SKILLS)
    return sorted(p for p in (ROOT / "profiles").glob("*/skills/*/SKILL.md") if p.parent.name not in skip)


def reference_files():
    return sorted(
        p for p in (ROOT / "profiles").glob("*/skills/*/references/*.md") if p.parents[1].name not in GENERATED_SKILL_DIRS
    )


def split(path):
    _, front, body = path.read_text(encoding="utf-8").split("---\n", 2)
    return front, body


def headings(text):
    return [line for line in text.splitlines() if line.startswith("## ")]


def section(text, heading):
    lines = text.splitlines()
    start = lines.index(heading) + 1
    end = next((i for i in range(start, len(lines)) if lines[i].startswith("## ")), len(lines))
    return "\n".join(lines[start:end])


def tree(path):
    return {str(p.relative_to(path)): p.read_bytes() for p in sorted(path.rglob("*")) if p.is_file()}


def preload_skills(path):
    values, active = [], False
    for raw in path.read_text(encoding="utf-8").splitlines():
        if raw == "preload_skills:":
            active = True
        elif active and raw and not raw[0].isspace():
            break
        elif active and raw.strip().startswith("- "):
            values.append(raw.strip()[2:])
    return values


class PropertyPackTests(unittest.TestCase):
    def setUp(self):
        self.manifest = json.loads((ROOT / "property.json").read_text(encoding="utf-8"))

    def test_namespace_and_count(self):
        profiles = self.manifest["profiles"]
        self.assertEqual(self.manifest["profile_count"], len(profiles))
        self.assertTrue(all(p["name"].startswith("property-") for p in profiles))

    def test_every_job_has_skill(self):
        for profile in self.manifest["profiles"]:
            root = ROOT / "profiles" / profile["name"] / "skills"
            skills = {p.parent.name for p in root.glob("*/SKILL.md")} - GENERATED_SKILL_DIRS - set(SHARED_SKILLS)
            self.assertEqual(set(profile["jobs"]), skills, profile["name"])

    def test_three_to_five_jobs_per_profile(self):
        for profile in self.manifest["profiles"]:
            self.assertGreaterEqual(len(profile["jobs"]), 3, profile["name"])
            self.assertLessEqual(len(profile["jobs"]), 5, profile["name"])

    def test_orchestrator_is_backbone(self):
        names = {p["name"] for p in self.manifest["profiles"]}
        self.assertIn(self.manifest["orchestrator"], names)
        self.assertIn(self.manifest["orchestrator"], self.manifest["backbone_profiles"])
        self.assertLessEqual(set(self.manifest["backbone_profiles"]), names)

    def test_every_profile_preloads_panel_rules_and_ships_it(self):
        copies = set()
        for profile in self.manifest["profiles"]:
            root = ROOT / "profiles" / profile["name"]
            with self.subTest(profile=profile["name"]):
                self.assertEqual(SHARED_SKILLS, preload_skills(root / "distribution.yaml"))
                for skill in SHARED_SKILLS:
                    copy = root / "skills" / skill
                    self.assertTrue((copy / "SKILL.md").is_file())
                    self.assertNotIn(skill, profile["jobs"])
                    copies.add(repr(sorted(tree(copy).items())))
                    if (CANONICAL_SHARED / skill).is_dir():  # absent when the pack is copied on its own
                        self.assertEqual(tree(CANONICAL_SHARED / skill), tree(copy))
        self.assertEqual(1, len(copies), "the shared skill must be byte-identical in every profile")

    def test_shared_rules_are_no_longer_inlined(self):
        self.assertFalse((ROOT / "shared").exists())
        self.assertFalse((ROOT / "sync_shared.py").exists())
        for soul in ROOT.glob("profiles/*/SOUL.md"):
            self.assertNotIn("shared-rules:", soul.read_text(encoding="utf-8"), soul)

    def test_every_soul_has_the_six_upstream_sections(self):
        names = {p["name"] for p in self.manifest["profiles"]}
        for profile in self.manifest["profiles"]:
            text = (ROOT / "profiles" / profile["name"] / "SOUL.md").read_text(encoding="utf-8")
            with self.subTest(profile=profile["name"]):
                self.assertEqual(f"# {profile['display_name']}", text.splitlines()[0])
                self.assertEqual(SOUL_SECTIONS, headings(text))
                words = len(text.split())
                self.assertGreaterEqual(words, 250)
                self.assertLessEqual(words, 450)
                # The principle every profile keeps: prepare the real professional's work, never replace them.
                role = " ".join(section(text, "## Role").split())
                self.assertIn("do not replace", role)
                self.assertIn("exact question", role)
                self.assertIn("`panel-rules`", section(text, "## Working standard"))
                collaborators = set(re.findall(r"`(property-[a-z-]+)`", section(text, "## Collaboration")))
                self.assertLessEqual(collaborators, names)
                self.assertGreaterEqual(len(collaborators - {profile["name"]}), 3)

    def test_validator_passes(self):
        result = subprocess.run([sys.executable, str(ROOT / "validate.py")], capture_output=True, text=True)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_every_skill_follows_the_upstream_template(self):
        self.assertEqual(38, len(skill_files(shared=False)))
        for path in skill_files():
            text = path.read_text(encoding="utf-8")
            _, body = split(path)
            with self.subTest(skill=str(path.relative_to(ROOT))):
                lead = [block for block in body.split("\n## ", 1)[0].strip().split("\n\n") if block.strip()]
                self.assertEqual(2, len(lead))
                self.assertTrue(lead[0].startswith("# "))
                self.assertTrue(lead[1].startswith("Use when ") and "\n" not in lead[1] and lead[1].endswith("."))
                self.assertEqual(SKILL_SECTIONS, headings(body))
                self.assertIn("| Needs | Why | Check |", section(body, "## Prerequisites"))
                self.assertIn("stop before step 1", " ".join(section(body, "## Prerequisites").split()))
                self.assertRegex(section(body, "## Procedure").strip(), r"^1\. ")
                self.assertTrue(section(body, "## Decision rules").strip().startswith("- "))
                gate = section(body, "## Quality gate").strip()
                self.assertNotIn("\n\n", gate)
                self.assertFalse(gate.startswith(("- ", "1. ")))
                self.assertLessEqual(len(text.split()), MAX_SKILL_WORDS)

    def test_references_are_linked_from_the_procedure_of_their_skill(self):
        self.assertTrue(reference_files())
        for path in reference_files():
            _, body = split(path.parents[1] / "SKILL.md")
            self.assertIn(f"references/{path.name}", section(body, "## Procedure"), path)
        for path in skill_files():
            for link in set(re.findall(r"references/[A-Za-z0-9._-]+\.md", path.read_text(encoding="utf-8"))):
                self.assertTrue((path.parent / link).is_file(), f"{path}: {link}")

    def test_wording_is_neutral(self):
        own = [ROOT / "README.md", ROOT / "property.json", *ROOT.glob("profiles/*/SOUL.md"),
               *ROOT.glob("profiles/*/distribution.yaml"), *skill_files(), *reference_files()]
        for path in own:
            text = path.read_text(encoding="utf-8")
            self.assertIsNone(GENDERED.search(text), f"{path}: the investor is 'the investor' and 'they'")
            self.assertNotIn("Voice reply", text, path)

    @unittest.skipUnless(yaml, "PyYAML not installed")
    def test_frontmatter_is_portable(self):
        allowed = {"name", "description", "metadata", "required_environment_variables", "required_credential_files"}
        used = {}
        for path in skill_files():
            front, body = split(path)
            meta = yaml.safe_load(front)
            self.assertLessEqual(set(meta), allowed, path)
            self.assertEqual(path.parent.name, meta["name"])
            self.assertTrue(meta["description"].strip(), path)
            self.assertLessEqual(len(meta["description"]), 60, path)
            for entry in (meta.get("metadata") or {}).get("hermes", {}).get("config", []):
                self.assertIn(entry["key"], KNOWN_CONFIG, path)
                self.assertEqual(KNOWN_CONFIG[entry["key"]], entry["default"], path)
                self.assertIn(f"`{entry['key']}`", section(body, "## Configuration"), path)
                used.setdefault(entry["key"], 0)
                used[entry["key"]] += 1
        self.assertEqual(set(KNOWN_CONFIG), set(used))

    def test_no_stale_config_command(self):
        stale = "hermes skills " + "config"
        own = [ROOT / "README.md", *ROOT.glob("profiles/*/SOUL.md"), *skill_files(), *reference_files()]
        for path in own:
            self.assertNotIn(stale, path.read_text(encoding="utf-8"), path)

    def test_no_runtime_state_files(self):
        forbidden = {"auth.json", ".env", "state.db", "projects.db", "gateway.pid", ".no-bundled-skills"}
        found = {p.name for p in (ROOT / "profiles").rglob("*") if p.is_file() and p.name in forbidden}
        self.assertFalse(found, sorted(found))


if __name__ == "__main__":
    unittest.main()
