---
name: email-send-with-approval
description: "Draft, check, approve and send an email campaign"
metadata:
  hermes:
    tags: [workflow, multi-profile]
    config:
      - {key: delivery.board, description: "Where the team claims work.", default: "none"}
      - {key: delivery.handoff, description: "How a step reaches another profile when no board runs the workflow.", default: "profile-turn"}
      - {key: venture.brief, description: "The venture's brief: customer, voice, constraints, autonomy.", default: ""}
      - {key: publishing.approval, description: "How the owner's approval of an outward action is captured.", default: "explicit-message"}
      - {key: owner.channel, description: "Where questions and owner actions reach the owner.", default: "this conversation"}
    prerequisites:
      commands: [hermes]
---
# Workflow: email-send-with-approval

An email campaign is sent only after deliverability is checked and the owner approved the exact campaign and audience. Drafts are free; the send is gated.

You coordinate this workflow. Each step belongs to one profile, which runs it with its own skills; never run another profile's step yourself. This file is generated from `workflows/email-send-with-approval.yaml` (the same definition is in `references/workflow.yaml`).

## Trigger
A campaign is needed: a launch, a newsletter slot, or a lifecycle message.

## Steps
| # | Step | Actor | Loads | After | Produces |
|---|---|---|---|---|---|
| 1 | `draft` | `agency-email-marketer` | `email-campaign`, `approval-gated-publishing` | — | subject, body, audience, consent basis and send time, as a draft in the email platform |
| 2 | `deliverability` | `agency-email-marketer` | `deliverability-review` | `draft` | a deliverability check that passes, or what to fix |
| 3 | `approve` | the human named by `publishing.approval` | — | `deliverability` | the owner's approval, recorded verbatim |
| 4 | `send` | `agency-email-marketer` | `approval-gated-publishing` | `approve` | the sent or scheduled campaign, linked, with its read-back send time |

### 1. `draft` — `agency-email-marketer`
Draft the campaign and pick the audience from the venture's brief, with each recipient's consent basis. An imported "subscribed" status needs the owner's dated opt-in statement.
- Also loads `segmentation` when the audience is a segment, not the whole list.

### 2. `deliverability` — `agency-email-marketer`
Check authentication, links, list hygiene and spam risk before anyone approves.
- On failure the work goes back to `draft` with the findings, then this step runs again.

### 3. `approve` — the human named by `publishing.approval`
The owner approves the exact campaign and audience.
- Asks: approve this exact campaign, audience and send time, or say what to change
- Who acts follows `publishing.approval`.

### 4. `send` — `agency-email-marketer`
Schedule or send exactly the approved campaign to the approved audience, then read each message back and compare its status and send time with the approved ones. An unexpected error on a send call goes to the owner, not to a retry on another endpoint.

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| Profiles installed: `agency-email-marketer` | each step runs as its own profile | `hermes profile list` |
| A way to hand a step to another profile, when there is no board (`delivery.handoff`) | steps that are not yours | the profile answers a test brief |
| The `kanban` toolset, when `delivery.board` is `hermes-kanban` | one card per step | `kanban_list` answers |
| A way to reach the owner (`owner.channel`) | human steps | the owner answers there |

If a required prerequisite is missing, stop before step 1. Say which one, what it blocks, and the smallest access that would unblock it. A step whose profile is not installed is never run under another profile: report the workflow as blocked at that step. Never report a step done that its profile did not complete.

## Configuration
- `delivery.board` decides how the workflow runs (below).
- `delivery.handoff` decides how a step reaches another profile when no board runs the workflow (below).
- `venture.brief`: The venture's brief: customer, voice, constraints, autonomy.
- `publishing.approval`: How the owner's approval of an outward action is captured. Decides who acts at `approve`.
- `owner.channel`: Where questions and owner actions reach the owner.

Current values appear in the `[Skill config]` block when this skill loads; an unset key shows its declared default. Persist a value with `hermes config set skills.config.<key> <value>` (per profile: `hermes -p <profile> config set …`); `hermes config migrate` prompts for keys still unset.

## Run it
### On a Hermes Kanban board (`delivery.board: hermes-kanban`)
1. Create every card up front, in step order, with `kanban_create`: title `email-send-with-approval: <step> — <work item>`, `assignee` the step's profile, `skills` the step's skills (plus the ones every step loads, and any extra skill whose condition holds), `parents` the cards of its After steps, and a body with the step's instructions, what it must produce and a link to the work item. For a step with an "On failure" target, the body also says: on a problem, comment the findings and block the card instead of completing it. The dispatcher starts each card when its parents are done.
2. A human step is a card assigned to you. When it starts, ask through `owner.channel` and block it with `kanban_block(kind="needs_input")`. On a go, comment the answer verbatim and complete the card; a human action (such as a merge) is complete only once you have verified it happened. On a no, comment it, leave the card blocked, and report the workflow stopped at that step.
3. An optional step whose condition does not hold is completed with `skipped: <reason>`, so the steps after it proceed.
4. A step with an "On failure" target that finds a problem comments its findings and blocks its card. Create a fix card for the target step's profile with the findings, make it a parent of the checking card (`kanban_link(parent_id=<fix>, child_id=<check>)`), and unblock the checking card (`kanban_unblock`): it waits until the fix is done, then runs again.

### Without a board (`delivery.board: none` or `tracker`)
Run the steps in dependency order. Hand each step to its profile the way `delivery.handoff` says:
- `profile-turn`: one non-interactive turn of that profile, for example `hermes -p <profile> chat -Q -s <skills> --query-file <brief file>`. Its final reply is the step's output. Never add a flag that skips approvals.
- `channel`: post the brief in that profile's channel and wait for its answer there.
- `owner-relay`: give the brief to the owner through `owner.channel` and ask them to pass it on.

The brief carries the step's instructions, its skills, the work item and the outputs of its After steps. Wait for the output and check it against "Produces"; an answer that does not produce it is not a completed step. Loop back on failure as above. At a human step, ask through `owner.channel` and wait. With `tracker`, record each step's start, output and decision as comments on the work item.

## Done when
- The sent campaign and audience match the approved ones exactly.
- Every step is done, or skipped with the reason its condition did not hold; every human decision is recorded verbatim.

## Report
Each update names the workflow, the current step and its actor, links the cards or the work item, and says what is needed from whom, if anything.
