---
name: contract-change
description: "Change a smart contract through review and testnet"
metadata:
  hermes:
    tags: [workflow, multi-profile]
    config:
      - {key: delivery.board, description: "Where the team claims work.", default: "none"}
      - {key: delivery.handoff, description: "How a step reaches another profile when no board runs the workflow.", default: "profile-turn"}
      - {key: delivery.code_host, description: "Where code and reviews live.", default: "detect"}
      - {key: delivery.merge_policy, description: "Who may merge.", default: "owner"}
      - {key: owner.channel, description: "Where questions and owner actions reach the owner.", default: "this conversation"}
      - {key: owner.action_tracker, description: "Where an owner action is recorded while it waits.", default: "conversation"}
    prerequisites:
      commands: [hermes]
---
# Workflow: contract-change

A smart-contract change goes from failing-first tests to an owner-approved mainnet action, with review by profiles that did not write it and a testnet deployment in between.

You coordinate this workflow. Each step belongs to one profile, which runs it with its own skills; never run another profile's step yourself. This file is generated from `workflows/contract-change.yaml` (the same definition is in `references/workflow.yaml`).

## Trigger
Any change to contract source, deployment or upgrade scripts, access control, fees, supply, allowances, or configuration a deployed contract reads.

## Steps
| # | Step | Actor | Loads | After | Produces |
|---|---|---|---|---|---|
| 1 | `change` | `agency-onchain-engineer` | `contract-change-authoring` | — | a draft request with intent, invariants and test evidence |
| 2 | `review` | `agency-code-reviewer` | `code-review`, `test-adequacy-review` | `change` | findings resolved, or the blocking ones |
| 3 | `security` | `agency-security-reviewer` | `security-review`, `authorization-review` | `change` | findings resolved, or the blocking ones |
| 4 | `testnet` | `agency-onchain-engineer` | `testnet-deployment` | `review`, `security` | testnet addresses, transactions and verification |
| 5 | `mainnet` | the owner | — | `testnet` | the owner's decision and, if approved, the mainnet transaction |

### 1. `change` — `agency-onchain-engineer`
Write the intent and invariants, the failing-first tests, then the change, in a draft request.

### 2. `review` — `agency-code-reviewer`
Review the change and whether its tests would catch a broken invariant.
- On failure the work goes back to `change` with the findings, then this step runs again.

### 3. `security` — `agency-security-reviewer`
Review the change for loss of funds, privilege and upgrade risks.
- Runs only when the change touches funds, access control, upgradeability or external calls. Otherwise it is recorded as skipped, with that reason.
- On failure the work goes back to `change` with the findings, then this step runs again.

### 4. `testnet` — `agency-onchain-engineer`
Deploy to a testnet and verify the behaviour on-chain.

### 5. `mainnet` — the owner
The owner decides on mainnet and signs. Each mainnet action is an owner action.
- Asks: approve and sign the prepared mainnet action, or say what blocks it

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| Profiles installed: `agency-code-reviewer`, `agency-onchain-engineer`, `agency-security-reviewer` | each step runs as its own profile | `hermes profile list` |
| A way to hand a step to another profile, when there is no board (`delivery.handoff`) | steps that are not yours | the profile answers a test brief |
| The `kanban` toolset, when `delivery.board` is `hermes-kanban` | one card per step | `kanban_list` answers |
| A way to reach the owner (`owner.channel`) | human steps | the owner answers there |

If a required prerequisite is missing, stop before step 1. Say which one, what it blocks, and the smallest access that would unblock it. A step whose profile is not installed is never run under another profile: report the workflow as blocked at that step. Never report a step done that its profile did not complete.

## Configuration
- `delivery.board` decides how the workflow runs (below).
- `delivery.handoff` decides how a step reaches another profile when no board runs the workflow (below).
- `delivery.code_host`: Where code and reviews live. Decides the CLI (`gh`, `glab`, …) and the words (pull request vs merge request). Detect from `git remote get-url origin`.
- `delivery.merge_policy`: Who may merge. A profile never merges under `owner`.
- `owner.channel`: Where questions and owner actions reach the owner.
- `owner.action_tracker`: Where an owner action is recorded while it waits.

Current values appear in the `[Skill config]` block when this skill loads; an unset key shows its declared default. Persist a value with `hermes config set skills.config.<key> <value>` (per profile: `hermes -p <profile> config set …`); `hermes config migrate` prompts for keys still unset.

## Run it
### On a Hermes Kanban board (`delivery.board: hermes-kanban`)
1. Create every card up front, in step order, with `kanban_create`: title `contract-change: <step> — <work item>`, `assignee` the step's profile, `skills` the step's skills (plus the ones every step loads, and any extra skill whose condition holds), `parents` the cards of its After steps, and a body with the step's instructions, what it must produce and a link to the work item. For a step with an "On failure" target, the body also says: on a problem, comment the findings and block the card instead of completing it. The dispatcher starts each card when its parents are done.
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
- Mainnet changes only through an action the owner approved and signed.
- Every step is done, or skipped with the reason its condition did not hold; every human decision is recorded verbatim.

## Report
Each update names the workflow, the current step and its actor, links the cards or the work item, and says what is needed from whom, if anything.
