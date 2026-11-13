"""Skills added beside the upstream baseline keep the upstream shape."""
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("check_skill_shape", ROOT / "scripts" / "check_skill_shape.py")
shape = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = shape
SPEC.loader.exec_module(shape)

SKILL = """---
name: demo
description: "Do a demo thing"
metadata:
  hermes:
    config:
      - {key: delivery.code_host, description: "Where code lives.", default: "detect"}
---
# Demo

Use when a demo is needed.

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| nothing | - | - |

## Configuration
- `delivery.code_host` decides the CLI.

## Procedure
1. Do it.

## Decision rules
- Prefer the simple way.

## Quality gate
Done when it is done.
"""

WORKFLOW = """---
name: flow
description: "Run a demo flow"
---
# Flow

## Trigger
Something happens.

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| nothing | - | - |

## Steps
1. Do it with `demo`.

## Decision rules
- Stop when unsure.

## Done when
- It is done.
"""


class ShapeTests(unittest.TestCase):
    def repo(self, tmp: str, skill: str = SKILL, workflow: str = WORKFLOW) -> Path:
        root = Path(tmp)
        (root / "capabilities").mkdir()
        (root / "capabilities" / "baseline.json").write_text(json.dumps({"profile_source_files": {
            "hermes-demo/profiles/demo-a/skills/upstream/SKILL.md": "x"}}), encoding="utf-8")
        base = root / "hermes-demo" / "profiles" / "demo-a" / "skills"
        for rel, text in (("upstream", "no shape at all"), ("demo", skill), ("workflows/flow", workflow),
                          ("capabilities/generated", "generated"), ("workflows/rendered", "rendered")):
            (base / rel).mkdir(parents=True)
            (base / rel / "SKILL.md").write_text(text, encoding="utf-8")
        (base / "workflows" / "rendered" / "references").mkdir()
        (base / "workflows" / "rendered" / "references" / "workflow.yaml").write_text("name: rendered\n", encoding="utf-8")
        return root

    def problems(self, root: Path) -> list[str]:
        return [e for path in shape.added_skills(root) for e in shape.check(path, root, {"delivery.code_host"})]

    def test_only_added_hand_written_skills_are_checked(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = self.repo(tmp)
            names = sorted(p.parent.name for p in shape.added_skills(root))
            self.assertEqual(["demo", "flow"], names)   # not the baselined, generated or rendered ones
            self.assertEqual([], self.problems(root))

    def test_each_departure_from_the_shape_is_reported(self):
        cases = {
            "missing section": SKILL.replace("## Quality gate\nDone when it is done.\n", ""),
            "foreign section": SKILL + "\n## Traps\n- One.\n",
            "out of order": SKILL.replace("## Procedure\n1. Do it.\n\n## Decision rules\n- Prefer the simple way.\n",
                                          "## Decision rules\n- Prefer the simple way.\n\n## Procedure\n1. Do it.\n"),
            "no use-when line": SKILL.replace("Use when a demo is needed.", "A demo."),
            "long description": SKILL.replace('"Do a demo thing"', '"' + "x" * 61 + '"'),
            "unknown setting": SKILL.replace("delivery.code_host", "delivery.nope"),
            "setting never explained": SKILL.replace("- `delivery.code_host` decides the CLI.", "- It depends."),
            "too long": SKILL.replace("1. Do it.", "1. " + "word " * 700),
            "broken reference": SKILL.replace("1. Do it.", "1. Do it as in [the list](references/list.md)."),
            "an incident story": SKILL.replace("- Prefer the simple way.", "- A stale copy once produced a wrong answer."),
        }
        for label, text in cases.items():
            with self.subTest(label), tempfile.TemporaryDirectory() as tmp:
                self.assertTrue(self.problems(self.repo(tmp, skill=text)), label)
        with tempfile.TemporaryDirectory() as tmp:
            broken = WORKFLOW.replace("## Done when\n- It is done.\n", "")
            self.assertTrue(self.problems(self.repo(tmp, workflow=broken)))

    def test_the_repository_passes(self):
        self.assertEqual(0, shape.main([]))


if __name__ == "__main__":
    unittest.main()
