# Workflows

A **skill** is know-how a role brings to any task: how to write Go services, how to read an infrastructure plan, how to check a sale agreement. A **workflow** is an ordered process with a trigger: when a work item is accepted, when a change merges, when a deal comes in. Workflows are where "who does what, in which order, and who decides" lives; skills are where "how to do it well" lives.

Hermes has no workflow primitive of its own. A profile loads skills, and Hermes Kanban runs work across profiles: each card has one assignee profile, the skills its worker loads, and parent cards it waits for. This repository represents workflows with those two pieces.

## Two kinds

| Kind | When | Where it lives |
| --- | --- | --- |
| **Single-profile workflow** | one profile runs the whole process, possibly ending with a question to the owner | a skill under `skills/workflows/<name>/` in that profile, with `## Trigger`, `## Steps` and `## Done when` sections and the `workflow` tag |
| **Multi-profile workflow** | steps are handed between profiles, or to a human who decides | a definition in `workflows/<name>.yaml`, rendered into the coordinating profile as `skills/workflows/<name>/` |

Skills under `skills/workflows/` are in the `workflows` category in Hermes (the category is the folder), so an agent can list workflows apart from skills.

## Multi-profile workflow definitions

```yaml
name: issue-to-merge                 # = file name
version: 0.1.0
description: "Take a work item from shaping to a verified merge"   # at most 60 characters
summary: One paragraph on what the workflow achieves.
pack: agency                         # every profile step belongs to this pack
coordinator: agency-product-manager  # receives the rendered workflow skill
trigger: When the workflow starts.
uses_settings: [delivery.merge_policy, owner.channel]   # keys from docs/PORTABLE_SKILLS.md
all_steps_load: [gated-delivery]     # optional: loaded by every profile step
steps:
  - id: build
    profile: agency-backend-engineer
    skills: [backend-service-implementation, backend-testing]   # must exist in that profile
    extra_skills:
      - {skill: go-backend-craft, when: "the affected code is Go"}
    needs: [clarify]                 # earlier steps only
    does: What the step does.
    output: What it produces.
  - id: verify
    profile: agency-qa-tester
    skills: [real-run-verification]
    needs: [build]
    on_fail: build                   # an earlier step this one depends on
    optional_when: a condition       # otherwise the step is recorded as skipped
    does: ...
    output: ...
  - id: merge
    human: true
    decided_by: delivery.merge_policy   # a setting, or "owner"
    who: the owner                      # optional label
    asks: What the human is asked.
    needs: [verify]
    does: ...
    output: ...
done_when: [Observable conditions.]
then: [after-merge]                  # optional follow-on workflows
```

`python scripts/sync_workflows.py` validates every definition and writes the rendering; `--check` fails on any error or drift and runs in `python validate.py`. It checks that:

- every step names a profile of the pack and skills that profile ships (including `all_steps_load` and `extra_skills`);
- `needs` only point to earlier steps, so steps form no cycle, and `on_fail` points to a profile step the failing step depends on;
- every human step names who decides, and a workflow with human steps uses `owner.channel`;
- every setting is in the registry, and a workflow has at least two actors;
- every recipe that lists a workflow has all of its profiles in its `expanded` tier.

Edit the definition, never the rendered `SKILL.md`: the check fails on a hand edit.

## How a coordinator runs one

The rendered skill tells the coordinator, per `delivery.board`:

- **`hermes-kanban`**: create one card per step with `kanban_create` (assignee = the step's profile, `skills` = its skills, `parents` = the cards of its `needs`). The dispatcher starts each card when its parents are done. A human step is a card assigned to the coordinator, blocked with `kanban_block(kind="needs_input")` until the human answers. A failed check blocks its card; the coordinator creates a fix card for the `on_fail` profile, links it as the check card's parent, and unblocks the check card, which reruns once the fix is done.
- **`none` or `tracker`**: run the steps in dependency order, handing each to its profile through the host's delegation or the profile's channel, and stop at human steps.

A step whose profile is not installed is never run by another profile: the workflow is reported blocked at that step.

## Shipped workflows

| Workflow | Kind | Coordinator | Steps |
| --- | --- | --- | --- |
| `issue-to-merge` | multi-profile | `agency-product-manager` | shape → clarify → build → verify, readiness (optional) → gate → merge (human, `delivery.merge_policy`) |
| `after-merge` | multi-profile | `agency-product-manager` | developer follow-ups, knowledge update → close the item |
| `infra-change` | multi-profile | `agency-infrastructure-engineer` | plan → security review (optional) → gate → merge (human) → apply (human, `delivery.apply_policy`) → verify |
| `publish-with-approval` | multi-profile | `agency-social-media-manager` | draft → fact-check (optional) → approve (human) → publish → engage |
| `email-send-with-approval` | multi-profile | `agency-email-marketer` | draft → deliverability → approve (human) → send |
| `contract-change` | multi-profile | `agency-onchain-engineer` | change → code review, security review (optional) → testnet → mainnet (owner) |
| `property-deal-review` | multi-profile | `property-coordinator` | capture → works, dwellings, deed, tax BE/FR → strategy, law → synthesis → the investor decides |
| `ready-queue` | single-profile | `agency-product-manager` | refill the ready queue |
| `coordination-board` | single-profile | `agency-orchestrator` | sweep claims before routing |
| `repo-audit-to-issues` | single-profile | `agency-venture-operator` | audit a repository into findings |
| `bounded-task-delivery` | single-profile | `agency-venture-operator` | deliver one bounded change |
| `owner-action-handoff` | single-profile | `agency-chief-of-staff` | hand the owner a prepared action |

Recipes list the workflows their team can run in a `workflows` field.
