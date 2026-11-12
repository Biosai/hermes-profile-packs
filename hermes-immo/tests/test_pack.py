import json
import subprocess
import sys
import unittest
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover - depends on the environment
    yaml = None

ROOT = Path(__file__).resolve().parents[1]
START = "<!-- shared-rules:start -->\n"
END = "<!-- shared-rules:end -->\n"
KNOWN_CONFIG = {
    "immo.fiche_investisseur": "memory",
    "immo.registre_questions": "memory",
    "immo.juridictions": "detect",
    "immo.bibliotheque_ouvrages": "none",
    "owner.channel": "this conversation",
}


def skill_files():
    return sorted(
        p for p in (ROOT / "profiles").glob("*/skills/*/SKILL.md") if p.parent.name != "capabilities"
    )


def split(path):
    _, front, body = path.read_text(encoding="utf-8").split("---\n", 2)
    return front, body


class ImmoPackTests(unittest.TestCase):
    def setUp(self):
        self.manifest = json.loads((ROOT / "immo.json").read_text(encoding="utf-8"))

    def test_namespace_and_count(self):
        profiles = self.manifest["profiles"]
        self.assertEqual(self.manifest["profile_count"], len(profiles))
        self.assertTrue(all(p["name"].startswith("immo-") for p in profiles))

    def test_every_job_has_skill(self):
        for profile in self.manifest["profiles"]:
            root = ROOT / "profiles" / profile["name"] / "skills"
            skills = {p.parent.name for p in root.glob("*/SKILL.md")} - {"capabilities"}
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

    def test_shared_rules_block_is_identical_in_every_soul(self):
        rules = (ROOT / "shared" / "RULES.md").read_text(encoding="utf-8")
        blocks = set()
        for profile in self.manifest["profiles"]:
            text = (ROOT / "profiles" / profile["name"] / "SOUL.md").read_text(encoding="utf-8")
            self.assertEqual(1, text.count(START), profile["name"])
            self.assertTrue(text.endswith(START + rules + END), profile["name"])
            blocks.add(text[text.index(START):])
        self.assertEqual(1, len(blocks))

    def test_sync_shared_reports_no_drift(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "sync_shared.py"), "--check"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_validator_passes(self):
        result = subprocess.run([sys.executable, str(ROOT / "validate.py")], capture_output=True, text=True)
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_every_skill_declares_prerequisites_and_configuration(self):
        for path in skill_files():
            _, body = split(path)
            lines = body.splitlines()
            self.assertIn("## Prérequis", lines, path)
            self.assertIn("## Configuration", lines, path)
            self.assertIn("| Besoin | Pourquoi | Vérification |", body, path)
            self.assertIn("arrête-toi avant l'étape 1", body.replace("\n", " "), path)

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
                self.assertIn(f"`{entry['key']}`", body.split("## Configuration", 1)[1], path)
                used.setdefault(entry["key"], 0)
                used[entry["key"]] += 1
        self.assertEqual(set(KNOWN_CONFIG), set(used))

    def test_no_stale_config_command(self):
        stale = "hermes skills " + "config"
        for path in ROOT.rglob("*"):
            if path.is_file() and path.suffix in {".md", ".json", ".yaml", ".py"}:
                self.assertNotIn(stale, path.read_text(encoding="utf-8"), path)

    def test_no_runtime_state_files(self):
        forbidden = {"auth.json", ".env", "state.db", "projects.db", "gateway.pid", ".no-bundled-skills"}
        found = {p.name for p in (ROOT / "profiles").rglob("*") if p.is_file() and p.name in forbidden}
        self.assertFalse(found, sorted(found))


if __name__ == "__main__":
    unittest.main()
