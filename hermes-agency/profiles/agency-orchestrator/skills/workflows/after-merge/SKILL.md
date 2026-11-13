---
name: after-merge
description: "Close the loop after a change merges"
metadata:
  hermes:
    tags: [workflow, multi-profile]
    config:
      - {key: delivery.board, description: "Where the team claims work.", default: "none"}
      - {key: delivery.handoff, description: "How a step reaches another profile when no board runs the workflow.", default: "profile-turn"}
      - {key: delivery.code_host, description: "Where code and reviews live.", default: "detect"}
      - {key: delivery.issue_tracker, description: "Where findings and work items go.", default: "detect"}
      - {key: owner.channel, description: "Where questions and owner actions reach the owner.", default: "this conversation"}
    prerequisites:
      commands: [hermes]
---
# Workflow: after-merge

Everything that must happen once a change has merged, done by the profile that owns each part: the implementation owner's clean-up and counterpart, the knowledge base and shared skills, and closing the work item against its acceptance criteria.

You coordinate this workflow. Each step belongs to one profile, which runs it with its own skills; never run another profile's step yourself. This file is generated from `workflows/after-merge.yaml` (the same definition is in `references/workflow.yaml`).

## Trigger
A pull or merge request that belongs to a work item has merged (for a multi-repo item: every request of it).

## Steps
| # | Step | Actor | Loads | After | Produces |
|---|---|---|---|---|---|
| 1 | `followups` | `agency-fullstack-engineer` | `merge-followups` | — | the follow-up report with counterpart and docs request links |
| 2 | `knowledge` | `agency-knowledge-manager` | `post-merge-kb-update` | — | knowledge and skills requests, or "nothing to update" with the reason |
| 3 | `close` | `agency-product-manager` | `acceptance-criteria` | `followups`, `knowledge` | the work item closed with every follow-up linked, or the criterion the merged change misses |

### 1. `followups` — `agency-fullstack-engineer`
Clean up, record the downstream counterpart, update the repository docs, release the work item.

### 2. `knowledge` — `agency-knowledge-manager`
Update the knowledge base and shared skills from the merged diff.

### 3. `close` — `agency-product-manager`
Check the merged change against the acceptance criteria, link the follow-ups, and move the item to done.
- On failure the work goes back to `followups` with the findings; every step that depends on it then runs again.

### When a step sends the work back
A verdict belongs to the head it was given on. After a fix, every step that depends on the fixed step runs again on the new head, including checks that had already passed: a pass on an older head is void. Count the rounds per target step. After 3 rounds on the same step, stop and report to whoever started the workflow, with the findings of every round, instead of starting another.

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| Profiles installed: `agency-fullstack-engineer`, `agency-knowledge-manager`, `agency-product-manager` | each step runs as its own profile | `hermes profile list` |
| A way to hand a step to another profile, when there is no board (`delivery.handoff`) | steps that are not yours | the profile answers a test brief |
| The `kanban` toolset, when `delivery.board` is `hermes-kanban` | one card per step | `kanban_list` answers |

If a required prerequisite is missing, stop before step 1. Say which one, what it blocks, and the smallest access that would unblock it. A step whose profile is not installed is never run under another profile: report the workflow as blocked at that step. Never report a step done that its profile did not complete.

## Configuration
- `delivery.board` decides how the workflow runs (below).
- `delivery.handoff` decides how a step reaches another profile when no board runs the workflow (below).
- `delivery.code_host`: Where code and reviews live. Decides the CLI (`gh`, `glab`, …) and the words (pull request vs merge request). Detect from `git remote get-url origin`.
- `delivery.issue_tracker`: Where findings and work items go. `file`: a Markdown file named in `delivery.issue_file`. `none`: findings go in the report, never into a tracker.
- `owner.channel`: Where questions and owner actions reach the owner.

Current values appear in the `[Skill config]` block when this skill loads; an unset key shows its declared default. Persist a value with `hermes config set skills.config.<key> <value>` (per profile: `hermes -p <profile> config set …`); `hermes config migrate` prompts for keys still unset.

## Run it
### On a Hermes Kanban board (`delivery.board: hermes-kanban`)
1. Create every card up front, in step order, with `kanban_create`: title `after-merge: <step> — <work item>`, `assignee` the step's profile, `skills` the step's skills (plus the ones every step loads, and any extra skill whose condition holds), `parents` the cards of its After steps, and a body with the step's instructions, what it must produce and a link to the work item. For a step with an "On failure" target, the body also says: on a problem, comment the findings and block the card instead of completing it. The dispatcher starts each card when its parents are done.
2. A human step is a card assigned to you. When it starts, ask through `owner.channel` and block it with `kanban_block(kind="needs_input")`. On a go, comment the answer verbatim and complete the card; a human action (such as a merge) is complete only once you have verified it happened. On a change request, comment it verbatim and follow the step's "On a change request" line. On a plain no, comment it, leave the card blocked, and report the workflow stopped at that step.
3. An optional step whose condition does not hold is completed with `skipped: <reason>`, so the steps after it proceed.
4. A step with an "On failure" target that finds a problem comments its findings and blocks its card. Create a fix card for the target step's profile with the findings, make it a parent of the checking card (`kanban_link(parent_id=<fix>, child_id=<check>)`), and unblock the checking card (`kanban_unblock`): it waits until the fix is done, then runs again. For every other step that depends on the fixed step and already completed, create a new card (same title plus `— round <n>`) with the fix card as parent, so it runs again on the new head.

### Without a board (`delivery.board: none` or `tracker`)
Run the steps in dependency order. A step that names your own profile is yours to do. Hand every other step to its profile the way `delivery.handoff` says:
- `profile-turn`: one non-interactive turn of that profile, for example `hermes -p <profile> chat -Q -s <skills> --query-file <brief file>`. Its final reply is the step's output. Never add a flag that skips approvals.
- `channel`: post the brief in that profile's channel and wait for its answer there.
- `owner-relay`: give the brief to the owner through `owner.channel` and ask them to pass it on.

The brief carries the step's instructions, its skills, the work item and the outputs of its After steps. Wait for the output and check it against "Produces"; an answer that does not produce it is not a completed step. On a failure or a change request, send the work back as the step says and rerun what depends on it. At a human step, ask through `owner.channel` and wait. With `tracker`, record each step's start, output and decision as comments on the work item.

## Done when
- The work item is done and links the merge, the counterpart and every knowledge update.
- Every step is done, or skipped with the reason its condition did not hold; every human decision is recorded verbatim.

## Report
Each update names the workflow, the current step and its actor, links the cards or the work item, and says what is needed from whom, if anything.
