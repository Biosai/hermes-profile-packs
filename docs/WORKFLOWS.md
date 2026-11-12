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
- **`none` or `tracker`**: run the steps in dependency order and stop at human steps. A step reaches its profile the way `delivery.handoff` says: `profile-turn` (one non-interactive turn of that profile, `hermes -p <profile> chat -Q -s <skills> --query-file <brief file>`, whose reply is the step's output), `channel` (a message in that profile's channel) or `owner-relay` (the owner passes the brief on).

A step whose profile is not installed is never run by another profile: the workflow is reported blocked at that step.

## Fewer profiles than roles

A definition names one pack profile per role, and the rendering shipped here assumes each is installed. A smaller team renders its own copy with a **role assignment**: every role is given to one of the team's profiles, or to `self`, the profile that runs the workflow.

```bash
# one profile holds every role
python scripts/sync_workflows.py --render issue-to-merge --solo > SKILL.md
# the runner writes, a second profile reviews
python scripts/sync_workflows.py --render contract-change \
  --assign agency-onchain-engineer=self \
  --assign agency-code-reviewer=reviewer --assign agency-security-reviewer=reviewer > SKILL.md
```

Put the result in the running profile's `skills/workflows/<name>/SKILL.md`, with the skills its steps load. The rendering changes with the assignment, and says what the team gives up:

- **One profile holds every role.** The steps keep their order and each still produces its own output, but the skill states that no second profile checks the work, forbids reporting a step as independently reviewed, and makes the human step the only independent check. There is nothing to hand over, so `delivery.handoff` is not used.
- **The runner holds some roles.** It runs the steps marked "you" and hands the others to the profiles named, on the board or through `delivery.handoff`.

A `## Roles here` table at the end of the rendering records who holds each role. Give independent review to a profile that did not do the work whenever one exists: a workflow whose value is a second pair of eyes (`contract-change`, the `verify` step of `issue-to-merge`) loses that value when one profile holds every role, and the rendering says so rather than hiding it.

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
| `remaining-work-to-issues` | single-profile | `agency-venture-operator` | file the work left between the plan and the tracker |
| `bounded-task-delivery` | single-profile | `agency-venture-operator` | deliver one bounded change |
| `open-pr-readiness-sweep` | single-profile | `agency-product-manager` | read-only merge verdict for every open PR in scope |
| `mutation-proof` | single-profile | `agency-qa-tester` | prove a new test fails when its fix is undone |
| `owner-action-handoff` | single-profile | `agency-chief-of-staff` | hand the owner a prepared action |
| `product-direction-review` | single-profile | `agency-product-manager` | decide what to build next, document the vision |
| `conversion-drop-diagnosis` | single-profile | `agency-growth-marketer` | find where a zero or falling conversion is lost |
| `one-to-one-email-send` | single-profile | `agency-email-marketer` | send approved personal emails from the owner's mailbox |
| `gear-shopping-list` | single-profile | `council-fitness-coach` | choose, price and check sport gear the user buys |

Recipes list the workflows their team can run in a `workflows` field.
