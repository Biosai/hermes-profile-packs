---
name: issue-to-merge
description: "Take a work item from shaping to a verified merge"
metadata:
  hermes:
    tags: [workflow, multi-profile]
    config:
      - {key: delivery.board, description: "Where the team claims work.", default: "none"}
      - {key: delivery.handoff, description: "How a step reaches another profile when no board runs the workflow.", default: "profile-turn"}
      - {key: delivery.code_host, description: "Where code and reviews live.", default: "detect"}
      - {key: delivery.repo_layout, description: "How the code is split across repositories.", default: "detect"}
      - {key: delivery.issue_tracker, description: "Where findings and work items go.", default: "detect"}
      - {key: delivery.merge_policy, description: "Who may merge.", default: "owner"}
      - {key: owner.channel, description: "Where questions and owner actions reach the owner.", default: "this conversation"}
    prerequisites:
      commands: [hermes]
---
# Workflow: issue-to-merge

One work item, from a shaped request to a merged change that a separate profile has verified with real runs. Shaping, building, verifying and gating are done by different profiles, and the merge stays with whoever delivery.merge_policy names.

You coordinate this workflow. Each step belongs to one profile, which runs it with its own skills; never run another profile's step yourself. This file is generated from `workflows/issue-to-merge.yaml` (the same definition is in `references/workflow.yaml`).

## Trigger
A work item is accepted for delivery: it is at the top of the ready queue, or the owner asks for it.

## Steps
| # | Step | Actor | Loads | After | Produces |
|---|---|---|---|---|---|
| 1 | `shape` | `agency-product-manager` | `issue-authoring-standard` | — | a work item with problem, scope, acceptance criteria and links |
| 2 | `clarify` | `agency-backend-engineer` | `issue-clarification` | `shape` | questions answered on the item, or an explicit "no open question" |
| 3 | `build` | `agency-backend-engineer` | `backend-service-implementation`, `backend-testing` | `clarify` | a draft PR with tests and the run that proves them |
| 4 | `verify` | `agency-qa-tester` | `real-run-verification` | `build` | PASS/SKIP/FAIL counts against the baseline, with the commands and the head SHA |
| 5 | `readiness` | `agency-software-architect` | `readiness-review`, `fresh-main-evidence` | `build` | a readiness verdict with path:line@sha evidence |
| 6 | `gate` | `agency-product-manager` | `ready-to-merge-gate` | `verify`, `readiness` | a gate report where every line holds, or the failing lines |
| 7 | `merge` | the human named by `delivery.merge_policy` | — | `gate` | the merge commit on the default branch |

Every profile step also loads `gated-delivery`.

### 1. `shape` — `agency-product-manager`
Write or refine the work item so a developer can build it without guessing.

### 2. `clarify` — `agency-backend-engineer`
Ask every open question before any code, and record the answers on the work item.

### 3. `build` — `agency-backend-engineer`
Implement the change with its tests in your own worktree and open a draft pull or merge request.
- Also loads `go-backend-craft` when the affected code is Go.

### 4. `verify` — `agency-qa-tester`
Verify the change with runs you executed yourself, against a baseline at the head under test.
- On failure the work goes back to `build` with the findings, then this step runs again.

### 5. `readiness` — `agency-software-architect`
Review whether the change fits the architecture, with evidence from the freshly fetched default branch.
- Runs only when the change moves a module boundary, a public contract or a data model. Otherwise it is recorded as skipped, with that reason.
- On failure the work goes back to `build` with the findings, then this step runs again.

### 6. `gate` — `agency-product-manager`
Check every line of the ready-to-merge gate on the current head.
- On failure the work goes back to `build` with the findings, then this step runs again.

### 7. `merge` — the human named by `delivery.merge_policy`
The human or mechanism named by the merge policy merges the PR. You verify it is merged.
- Asks: merge the PR named in the gate report, or say what blocks it
- Who acts follows `delivery.merge_policy`.

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| Profiles installed: `agency-backend-engineer`, `agency-product-manager`, `agency-qa-tester`, `agency-software-architect` | each step runs as its own profile | `hermes profile list` |
| A way to hand a step to another profile, when there is no board (`delivery.handoff`) | steps that are not yours | the profile answers a test brief |
| The `kanban` toolset, when `delivery.board` is `hermes-kanban` | one card per step | `kanban_list` answers |
| A way to reach the owner (`owner.channel`) | human steps | the owner answers there |

If a required prerequisite is missing, stop before step 1. Say which one, what it blocks, and the smallest access that would unblock it. A step whose profile is not installed is never run under another profile: report the workflow as blocked at that step. Never report a step done that its profile did not complete.

## Configuration
- `delivery.board` decides how the workflow runs (below).
- `delivery.handoff` decides how a step reaches another profile when no board runs the workflow (below).
- `delivery.code_host`: Where code and reviews live. Decides the CLI (`gh`, `glab`, …) and the words (pull request vs merge request). Detect from `git remote get-url origin`.
- `delivery.repo_layout`: How the code is split across repositories. Monorepo: scope every change, test run and CI filter to the affected packages. Multi-repo: a change may span repos; link them.
- `delivery.issue_tracker`: Where findings and work items go. `file`: a Markdown file named in `delivery.issue_file`. `none`: findings go in the report, never into a tracker.
- `delivery.merge_policy`: Who may merge. A profile never merges under `owner`. Decides who acts at `merge`.
- `owner.channel`: Where questions and owner actions reach the owner.

Current values appear in the `[Skill config]` block when this skill loads; an unset key shows its declared default. Persist a value with `hermes config set skills.config.<key> <value>` (per profile: `hermes -p <profile> config set …`); `hermes config migrate` prompts for keys still unset.

## Run it
### On a Hermes Kanban board (`delivery.board: hermes-kanban`)
1. Create every card up front, in step order, with `kanban_create`: title `issue-to-merge: <step> — <work item>`, `assignee` the step's profile, `skills` the step's skills (plus the ones every step loads, and any extra skill whose condition holds), `parents` the cards of its After steps, and a body with the step's instructions, what it must produce and a link to the work item. For a step with an "On failure" target, the body also says: on a problem, comment the findings and block the card instead of completing it. The dispatcher starts each card when its parents are done.
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
- The merged change meets the work item's acceptance criteria.
- The verification counts and the gate report are linked from the work item.
- Every step is done, or skipped with the reason its condition did not hold; every human decision is recorded verbatim.

## Then
- Start `after-merge`, coordinated by `agency-product-manager`.

## Report
Each update names the workflow, the current step and its actor, links the cards or the work item, and says what is needed from whom, if anything.
