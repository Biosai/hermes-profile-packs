---
name: infra-change
description: "Change infrastructure through review and a human apply"
metadata:
  hermes:
    tags: [workflow, multi-profile]
    config:
      - {key: delivery.board, description: "Where the team claims work.", default: "none"}
      - {key: delivery.handoff, description: "How a step reaches another profile when no board runs the workflow.", default: "profile-turn"}
      - {key: delivery.iac_tool, description: "Infrastructure-as-code tool, when there is one.", default: "detect"}
      - {key: delivery.merge_policy, description: "Who may merge.", default: "owner"}
      - {key: delivery.apply_policy, description: "Who applies infrastructure changes.", default: "human"}
      - {key: owner.channel, description: "Where questions and owner actions reach the owner.", default: "this conversation"}
    prerequisites:
      commands: [hermes]
---
# Workflow: infra-change

An infrastructure-as-code change from request to verified apply. The change is planned and reviewed in a PR; the merge and the apply stay with the humans the settings name.

You coordinate this workflow. Each step belongs to one profile, which runs it with its own skills; never run another profile's step yourself. This file is generated from `workflows/infra-change.yaml` (the same definition is in `references/workflow.yaml`).

## Trigger
An infrastructure change is requested: a work item, an incident follow-up, or drift found in a plan.

## Steps
| # | Step | Actor | Loads | After | Produces |
|---|---|---|---|---|---|
| 1 | `plan` | `agency-infrastructure-engineer` | `iac-change-safety` | — | a PR with plan evidence and exact apply inputs |
| 2 | `security` | `agency-infrastructure-engineer` | `infra-security-review` | `plan` | findings resolved, or the blocking ones |
| 3 | `gate` | `agency-product-manager` | `ready-to-merge-gate` | `security` | a gate report where every line holds, or the failing lines |
| 4 | `merge` | the human named by `delivery.merge_policy` | — | `gate` | the merge commit on the default branch |
| 5 | `apply` | the human named by `delivery.apply_policy` | — | `merge` | the apply output |
| 6 | `verify` | `agency-infrastructure-engineer` | `iac-change-safety` | `apply` | an empty fresh plan, or the failing resources with their errors |

Every profile step also loads `gated-delivery`.

### 1. `plan` — `agency-infrastructure-engineer`
Write the smallest change, read its plan for every environment, explain every replace and destroy, report drift.

### 2. `security` — `agency-infrastructure-engineer`
Review the change for privilege, exposure and secret handling.
- Runs only when the change touches identity, secrets, network exposure, WAF, CI or host bootstrap. Otherwise it is recorded as skipped, with that reason.
- On failure the work goes back to `plan` with the findings, then this step runs again.

### 3. `gate` — `agency-product-manager`
Check every line of the ready-to-merge gate on the current head.
- On failure the work goes back to `plan` with the findings, then this step runs again.

### 4. `merge` — the human named by `delivery.merge_policy`
The human or mechanism named by the merge policy merges the PR. You verify it is merged.
- Asks: merge the infrastructure PR, or say what blocks it
- Who acts follows `delivery.merge_policy`.

### 5. `apply` — the human named by `delivery.apply_policy`
The human or approved pipeline named by the apply policy applies. Nobody applies from a session.
- Asks: apply the merged change with the inputs in the PR, then share the apply output
- Who acts follows `delivery.apply_policy`.

### 6. `verify` — `agency-infrastructure-engineer`
Read the apply output and confirm that a fresh plan shows no changes.

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| Profiles installed: `agency-infrastructure-engineer`, `agency-product-manager` | each step runs as its own profile | `hermes profile list` |
| A way to hand a step to another profile, when there is no board (`delivery.handoff`) | steps that are not yours | the profile answers a test brief |
| The `kanban` toolset, when `delivery.board` is `hermes-kanban` | one card per step | `kanban_list` answers |
| A way to reach the owner (`owner.channel`) | human steps | the owner answers there |

If a required prerequisite is missing, stop before step 1. Say which one, what it blocks, and the smallest access that would unblock it. A step whose profile is not installed is never run under another profile: report the workflow as blocked at that step. Never report a step done that its profile did not complete.

## Configuration
- `delivery.board` decides how the workflow runs (below).
- `delivery.handoff` decides how a step reaches another profile when no board runs the workflow (below).
- `delivery.iac_tool`: Infrastructure-as-code tool, when there is one.
- `delivery.merge_policy`: Who may merge. A profile never merges under `owner`. Decides who acts at `merge`.
- `delivery.apply_policy`: Who applies infrastructure changes. A profile never applies under `human`. Decides who acts at `apply`.
- `owner.channel`: Where questions and owner actions reach the owner.

Current values appear in the `[Skill config]` block when this skill loads; an unset key shows its declared default. Persist a value with `hermes config set skills.config.<key> <value>` (per profile: `hermes -p <profile> config set …`); `hermes config migrate` prompts for keys still unset.

## Run it
### On a Hermes Kanban board (`delivery.board: hermes-kanban`)
1. Create every card up front, in step order, with `kanban_create`: title `infra-change: <step> — <work item>`, `assignee` the step's profile, `skills` the step's skills (plus the ones every step loads, and any extra skill whose condition holds), `parents` the cards of its After steps, and a body with the step's instructions, what it must produce and a link to the work item. For a step with an "On failure" target, the body also says: on a problem, comment the findings and block the card instead of completing it. The dispatcher starts each card when its parents are done.
2. A human step is a card assigned to you. When it starts, ask through `owner.channel` and block it with `kanban_block(kind="needs_input")`. On a go, comment the answer verbatim and complete the card; a human action (such as a merge) is complete only once you have verified it happened. On a no, comment it, leave the card blocked, and report the workflow stopped at that step.
3. An optional step whose condition does not hold is completed with `skipped: <reason>`, so the steps after it proceed.
4. A step with an "On failure" target that finds a problem comments its findings and blocks its card. Create a fix card for the target step's profile with the findings, make it a parent of the checking card (`kanban_link(parent_id=<fix>, child_id=<check>)`), and unblock the checking card (`kanban_unblock`): it waits until the fix is done, then runs again.

### Without a board (`delivery.board: none` or `tracker`)
Run the steps in dependency order. A step that names your own profile is yours to do. Hand every other step to its profile the way `delivery.handoff` says:
- `profile-turn`: one non-interactive turn of that profile, for example `hermes -p <profile> chat -Q -s <skills> --query-file <brief file>`. Its final reply is the step's output. Never add a flag that skips approvals.
- `channel`: post the brief in that profile's channel and wait for its answer there.
- `owner-relay`: give the brief to the owner through `owner.channel` and ask them to pass it on.

The brief carries the step's instructions, its skills, the work item and the outputs of its After steps. Wait for the output and check it against "Produces"; an answer that does not produce it is not a completed step. Loop back on failure as above. At a human step, ask through `owner.channel` and wait. With `tracker`, record each step's start, output and decision as comments on the work item.

## Done when
- A fresh plan after the apply shows no changes.
- Every step is done, or skipped with the reason its condition did not hold; every human decision is recorded verbatim.

## Report
Each update names the workflow, the current step and its actor, links the cards or the work item, and says what is needed from whom, if anything.
