"""Skills shared by several profiles are written once and copied byte-for-byte."""
import importlib.util
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("sync_shared_skills", ROOT / "scripts" / "sync_shared_skills.py")
sync_shared_skills = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = sync_shared_skills
SPEC.loader.exec_module(sync_shared_skills)


class SharedSkillTests(unittest.TestCase):
    def test_every_copy_matches_its_canonical_source(self):
        self.assertEqual([], sync_shared_skills.drift(ROOT))

    def test_every_shared_skill_ships_in_at_least_two_profiles(self):
        targets = json.loads((ROOT / "shared-skills" / "targets.json").read_text(encoding="utf-8"))["skills"]
        for skill, profiles in targets.items():
            self.assertGreaterEqual(len(profiles), 2, skill)
            self.assertEqual(len(profiles), len(set(profiles)), skill)

    def test_check_detects_and_sync_repairs_a_hand_edited_copy(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name in ("one", "two"):
                profile = root / "pack" / "profiles" / name
                (profile / "skills").mkdir(parents=True)
                (profile / "distribution.yaml").write_text(f"name: {name}\n", encoding="utf-8")
            canonical = root / "shared-skills" / "demo"
            canonical.mkdir(parents=True)
            (canonical / "SKILL.md").write_text("---\nname: demo\ndescription: d\n---\nbody\n", encoding="utf-8")
            (root / "shared-skills" / "targets.json").write_text(
                json.dumps({"skills": {"demo": ["pack/profiles/one", "pack/profiles/two"]}}), encoding="utf-8"
            )
            self.assertEqual(2, len(sync_shared_skills.drift(root)))
            self.assertEqual(2, sync_shared_skills.sync(root))
            self.assertEqual([], sync_shared_skills.drift(root))
            edited = root / "pack" / "profiles" / "two" / "skills" / "demo" / "SKILL.md"
            edited.write_text("hand edit\n", encoding="utf-8")
            self.assertEqual(1, len(sync_shared_skills.drift(root)))
            sync_shared_skills.sync(root)
            self.assertEqual((canonical / "SKILL.md").read_bytes(), edited.read_bytes())
            shutil.rmtree(canonical)
            with self.assertRaises(ValueError):
                sync_shared_skills.plan(root)


if __name__ == "__main__":
    unittest.main()
