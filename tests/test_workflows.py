"""Multi-profile workflows: definitions are checked against real profiles and rendered exactly."""
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import textwrap
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("sync_workflows", ROOT / "scripts" / "sync_workflows.py")
sync_workflows = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = sync_workflows
SPEC.loader.exec_module(sync_workflows)

GOOD = """
name: demo
version: 0.1.0
description: "Demo workflow"
summary: A demo.
pack: demo
coordinator: demo-lead
trigger: Something happens.
uses_settings: [delivery.merge_policy, owner.channel]
steps:
  - {id: write, profile: demo-maker, skills: [make], does: Make it., output: a thing}
  - {id: check, profile: demo-lead, skills: [check], needs: [write], on_fail: write, does: Check it., output: a verdict}
  - {id: ship, human: true, decided_by: delivery.merge_policy, needs: [check], asks: ship it, does: Ship., output: shipped}
done_when: [It shipped.]
"""


class WorkflowRepoTests(unittest.TestCase):
    def test_repository_workflows_are_valid_and_rendered(self):
        self.assertEqual([], sync_workflows.drift(ROOT))

    def test_rendered_skills_are_hermes_workflow_skills(self):
        rendered = list(ROOT.glob("hermes-*/profiles/*/skills/workflows/*/references/workflow.yaml"))
        self.assertTrue(rendered)
        for ref in rendered:
            skill = ref.parent.parent / "SKILL.md"
            front = yaml.safe_load(skill.read_text(encoding="utf-8").split("---")[1])
            self.assertEqual(front["name"], skill.parent.name)
            self.assertLessEqual(len(front["description"]), 60)
            self.assertIn("workflow", front["metadata"]["hermes"]["tags"])
            keys = [c["key"] for c in front["metadata"]["hermes"]["config"]]
            self.assertIn("delivery.board", keys)

    def test_single_profile_workflows_have_trigger_steps_and_done(self):
        for skill in ROOT.glob("hermes-*/profiles/*/skills/workflows/*/SKILL.md"):
            if (skill.parent / "references" / "workflow.yaml").is_file():
                continue
            text = skill.read_text(encoding="utf-8")
            for heading in ("## Trigger", "## Steps", "## Done when", "## Prerequisites", "## Configuration"):
                self.assertIn(heading, text, f"{skill}: {heading}")


class WorkflowValidationTests(unittest.TestCase):
    def make_repo(self, root: Path, definition: str) -> None:
        (root / "docs").mkdir()
        (root / "docs" / "PORTABLE_SKILLS.md").write_text(
            "| Key | Values | Default | Meaning |\n|---|---|---|---|\n"
            "| `delivery.board` | hermes-kanban, none | none | Where the team claims work. |\n"
            "| `delivery.merge_policy` | owner, reviewer | owner | Who may merge. |\n"
            "| `owner.channel` | free text | this conversation | Where the owner is reached. |\n",
            encoding="utf-8",
        )
        (root / "packs.json").write_text(json.dumps({"packs": [
            {"name": "hermes-demo", "path": "hermes-demo", "namespace": "demo-*", "manifest": "hermes-demo/demo.json"}]}),
            encoding="utf-8")
        pack = root / "hermes-demo"
        pack.mkdir()
        (pack / "demo.json").write_text(json.dumps({"profiles": [{"name": "demo-lead"}, {"name": "demo-maker"}]}),
                                        encoding="utf-8")
        for profile, skills in (("demo-lead", ["check"]), ("demo-maker", ["make"])):
            for skill in skills:
                d = pack / "profiles" / profile / "skills" / skill
                d.mkdir(parents=True)
                (d / "SKILL.md").write_text(f"---\nname: {skill}\ndescription: d\n---\n", encoding="utf-8")
        (root / "recipes.json").write_text(json.dumps({"recipes": []}), encoding="utf-8")
        (root / "workflows").mkdir()
        (root / "workflows" / "demo.yaml").write_text(textwrap.dedent(definition), encoding="utf-8")

    def errors(self, definition: str) -> list[str]:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_repo(root, definition)
            return sync_workflows.build(root)[1]

    def test_good_definition_renders_into_the_coordinator(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_repo(root, GOOD)
            self.assertEqual(2, sync_workflows.sync(root))
            target = root / "hermes-demo/profiles/demo-lead/skills/workflows/demo"
            self.assertTrue((target / "SKILL.md").is_file())
            self.assertEqual((root / "workflows/demo.yaml").read_bytes(), (target / "references/workflow.yaml").read_bytes())
            self.assertEqual([], sync_workflows.drift(root))
            (target / "SKILL.md").write_text("hand edit\n", encoding="utf-8")
            self.assertEqual(1, len(sync_workflows.drift(root)))

    def test_each_broken_reference_is_reported(self):
        cases = {
            "unknown profile": GOOD.replace("profile: demo-maker", "profile: demo-ghost"),
            "no skill": GOOD.replace("skills: [make]", "skills: [missing]"),
            "later step": GOOD.replace("needs: [write]", "needs: [ship]"),
            "on_fail outside": GOOD.replace("on_fail: write", "on_fail: ship"),
            "human without decider": GOOD.replace("decided_by: delivery.merge_policy, ", ""),
            "unknown setting": GOOD.replace("[delivery.merge_policy, owner.channel]", "[delivery.nope, owner.channel]"),
            "human without owner channel": GOOD.replace("[delivery.merge_policy, owner.channel]", "[delivery.merge_policy]"),
            "long description": GOOD.replace('"Demo workflow"', '"' + "x" * 61 + '"'),
        }
        for label, definition in cases.items():
            with self.subTest(label):
                self.assertTrue(self.errors(definition), label)

    def test_a_single_actor_is_not_a_multi_profile_workflow(self):
        single = """
        name: demo
        version: 0.1.0
        description: "Demo"
        summary: A demo.
        pack: demo
        coordinator: demo-lead
        trigger: Something.
        steps:
          - {id: a, profile: demo-lead, skills: [check], does: A., output: a}
          - {id: b, profile: demo-lead, skills: [check], needs: [a], does: B., output: b}
        done_when: [Done.]
        """
        self.assertTrue(any("two actors" in e for e in self.errors(single)))


if __name__ == "__main__":
    unittest.main()
