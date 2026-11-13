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
            # each role is its own profile here, so every rendering says how a step is handed over
            self.assertIn("delivery.handoff", keys)
            self.assertIn("multi-profile", front["metadata"]["hermes"]["tags"])

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
            "| `delivery.handoff` | profile-turn, channel | profile-turn | How a step reaches another profile. |\n"
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

    def test_two_profiles_are_coordinated_by_the_pack_orchestrator(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_repo(root, GOOD)
            manifest = root / "hermes-demo" / "demo.json"
            data = json.loads(manifest.read_text(encoding="utf-8"))
            data["profiles"].append({"name": "demo-router"})
            data["orchestrator"] = "demo-router"
            manifest.write_text(json.dumps(data), encoding="utf-8")
            (root / "hermes-demo/profiles/demo-router/skills/route").mkdir(parents=True)
            (root / "hermes-demo/profiles/demo-router/skills/route/SKILL.md").write_text("---\nname: route\ndescription: d\n---\n", encoding="utf-8")
            errors = sync_workflows.build(root)[1]
            self.assertTrue(any("coordinator must be demo-router" in e for e in errors), errors)
            definition = root / "workflows" / "demo.yaml"
            definition.write_text(definition.read_text(encoding="utf-8").replace("coordinator: demo-lead", "coordinator: demo-router"), encoding="utf-8")
            self.assertEqual([], sync_workflows.build(root)[1])
            self.assertEqual(2, sync_workflows.sync(root))
            self.assertTrue((root / "hermes-demo/profiles/demo-router/skills/workflows/demo/SKILL.md").is_file())

    def test_a_human_can_send_the_work_back_and_loops_are_bounded(self):
        looped = GOOD.replace("needs: [check], asks: ship it", "needs: [check], on_reject: write, asks: ship it").replace(
            "trigger: Something happens.", "trigger: Something happens.\nmax_fix_rounds: 2")
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_repo(root, looped)
            self.assertEqual([], sync_workflows.build(root)[1])
            sync_workflows.sync(root)
            text = (root / "hermes-demo/profiles/demo-lead/skills/workflows/demo/SKILL.md").read_text(encoding="utf-8")
            self.assertIn("On a change request the work goes back to `write`", text)
            self.assertIn("every step that depends on it then runs again", text)
            self.assertIn("After 2 rounds on the same step, stop", text)
            self.assertIn("a pass on an older head is void", text)
        for label, bad in {
            "on_reject on a profile step": GOOD.replace("needs: [write], on_fail: write", "needs: [write], on_fail: write, on_reject: write"),
            "on_reject to a later step": GOOD.replace("needs: [check], asks: ship it", "needs: [check], on_reject: ship, asks: ship it"),
            "rounds not a number": GOOD.replace("trigger: Something happens.", "trigger: Something happens.\nmax_fix_rounds: many"),
            "decided by a setting that names no one": GOOD.replace("decided_by: delivery.merge_policy", "decided_by: owner.channel"),
        }.items():
            with self.subTest(label):
                self.assertTrue(self.errors(bad), label)

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


class RoleAssignmentTests(unittest.TestCase):
    """A team with fewer profiles than roles renders its own copy; the text must stay true."""

    def front(self, text: str) -> dict:
        return yaml.safe_load(text.split("---")[1])

    def test_one_profile_holding_every_role_is_told_so(self):
        text = sync_workflows.render_for(ROOT, "issue-to-merge", [], solo=True)
        front = self.front(text)
        self.assertEqual(["workflow", "single-profile"], front["metadata"]["hermes"]["tags"])
        self.assertNotIn("delivery.handoff", [c["key"] for c in front["metadata"]["hermes"]["config"]])
        self.assertIn("One profile holds every role here", text)
        self.assertIn("Never report a step as independently reviewed or verified", text)
        self.assertIn("Start `after-merge` yourself.", text)
        # nothing may tell a lone profile to hand work to someone, or to stay out of its own steps
        for false_claim in ("never run another profile's step yourself", "Profiles installed",
                            "delivery.handoff", "profile-turn"):
            self.assertNotIn(false_claim, text, false_claim)
        steps = [line for line in text.splitlines() if line.startswith("| ") and "| you |" in line]
        self.assertEqual(15, len(steps))   # 7 profile steps in the table + 8 roles held (coordinator included)
        self.assertIn("After 3 rounds on the same step, stop and ask the owner", text)
        self.assertIn("the human named by `delivery.merge_policy`", text)

    def test_a_runner_with_a_separate_reviewer_hands_over_only_the_review(self):
        text = sync_workflows.render_for(
            ROOT, "contract-change",
            ["agency-onchain-engineer=self", "agency-code-reviewer=reviewer", "agency-security-reviewer=reviewer"],
            solo=False)
        front = self.front(text)
        self.assertEqual(["workflow", "multi-profile"], front["metadata"]["hermes"]["tags"])
        self.assertIn("delivery.handoff", [c["key"] for c in front["metadata"]["hermes"]["config"]])
        self.assertIn("| 1 | `change` | you |", text)
        self.assertIn("| 2 | `review` | `reviewer` |", text)
        self.assertIn("Profiles installed: `reviewer`", text)
        self.assertIn("| `agency-orchestrator` | you |", text)   # coordinating defaults to the runner
        self.assertIn("Do the steps marked \"you\" yourself. Hand every other step", text)
        self.assertIn("hermes -p <profile> chat -Q -s <skills> --query-file <brief file>", text)
        self.assertIn("Never add a flag that skips approvals", text)
        self.assertNotIn("One profile holds every role here", text)

    def test_every_role_must_be_assigned(self):
        with self.assertRaises(sync_workflows.WorkflowError) as missing:
            sync_workflows.render_for(ROOT, "contract-change", ["agency-onchain-engineer=self"], solo=False)
        self.assertIn("agency-code-reviewer", str(missing.exception))
        for bad in (["agency-nobody=self"], ["agency-onchain-engineer"], ["agency-onchain-engineer=Not A Name"]):
            with self.subTest(bad), self.assertRaises(sync_workflows.WorkflowError):
                sync_workflows.render_for(ROOT, "contract-change", bad, solo=False)
        with self.assertRaises(sync_workflows.WorkflowError):
            sync_workflows.render_for(ROOT, "contract-change", ["agency-onchain-engineer=self"], solo=True)
        with self.assertRaises(sync_workflows.WorkflowError):
            sync_workflows.render_for(ROOT, "no-such-workflow", [], solo=True)

    def test_every_shipped_workflow_renders_solo_without_a_false_claim(self):
        for path, wf in sync_workflows.definitions(ROOT):
            with self.subTest(path.name):
                text = sync_workflows.render_for(ROOT, wf["name"], [], solo=True)
                self.assertNotIn("never run another profile's step", text)
                self.assertNotIn("coordinated by `self`", text)
                self.assertIn("## Roles here", text)

    def test_a_registry_without_the_handoff_setting_is_refused(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs").mkdir()
            (root / "docs" / "PORTABLE_SKILLS.md").write_text(
                "| `delivery.board` | hermes-kanban, none | none | Where the team claims work. |\n", encoding="utf-8")
            with self.assertRaises(sync_workflows.WorkflowError):
                sync_workflows.load_registry(root)


if __name__ == "__main__":
    unittest.main()
