---
name: property-deal-review
description: "Review one property deal with the expert panel"
metadata:
  hermes:
    tags: [workflow, multi-profile]
    config:
      - {key: delivery.board, description: "Where the team claims work.", default: "none"}
      - {key: delivery.handoff, description: "How a step reaches another profile when no board runs the workflow.", default: "profile-turn"}
      - {key: property.investor_file, description: "Where the investor's profile and own rules live.", default: "memory"}
      - {key: property.jurisdictions, description: "Regions and countries in play.", default: "detect"}
      - {key: owner.channel, description: "Where questions and owner actions reach the owner.", default: "this conversation"}
    prerequisites:
      commands: [hermes]
---
# Workflow: property-deal-review

One property deal in Belgium or France reviewed by the panel, each expert on its own part: works costs, strategies and scenarios, tax, the deed, the dwellings that legally exist, and the law where a clause or a lease shapes the deal. The coordinator turns their outputs into one synthesis with its weak assumptions named; the investor decides.

You coordinate this workflow. Each step belongs to one profile, which runs it with its own skills; never run another profile's step yourself. This file is generated from `workflows/property-deal-review.yaml` (the same definition is in `references/workflow.yaml`).

## Trigger
The investor sends a property to assess: a listing, a public sale, an option, or a building to divide.

## Steps
| # | Step | Actor | Loads | After | Produces |
|---|---|---|---|---|---|
| 1 | `capture` | `property-coordinator` | `investor-data-capture`, `open-questions` | — | the deal file with region, documents, the investor's rules that apply, and open questions |
| 2 | `works` | `property-works-estimator` | `listing-photo-review`, `works-estimate` | `capture` | works cost lines as ranges, each with its basis and date |
| 3 | `dwellings` | `property-architect` | `recognized-dwellings` | `capture` | each unit marked recognized, not recognized or unknown, with its proof |
| 4 | `notary` | `property-notary` | `sale-agreement-and-option`, `documents-to-request` | `capture` | the risks in the deed, and the documents and questions for the real notary |
| 5 | `tax-be` | `property-accountant-be` | `registration-duties`, `deal-costs` | `capture` | duties and costs per possible regime, marked to confirm with the investor's accountant |
| 6 | `tax-fr` | `property-accountant-fr` | `belgian-company-in-france` | `capture` | French tax per scenario, and the exact question for a French accountant |
| 7 | `strategy` | `property-investment-partner` | `deal-strategies`, `three-scenarios`, `market-value-comparables` | `works`, `dwellings`, `notary`, `tax-be`, `tax-fr` | the strategies ranked, each with three scenarios and the comparables behind the value |
| 8 | `law` | `property-lawyer` | `clause-analysis`, `primary-law-sources` | `notary` | each legal question answered with its source, or marked TO VERIFY |
| 9 | `synthesis` | `property-coordinator` | `expert-debate`, `consult-expert` | `strategy`, `law` | one synthesis with ranges, sources, disagreements resolved or stated, and the weak assumptions |
| 10 | `decide` | the investor | — | `synthesis` | the investor's decision, recorded verbatim |

### 1. `capture` — `property-coordinator`
Record the deal and its documents with their sources, establish the region, and ask the investor the one question that blocks the most.

### 2. `works` — `property-works-estimator`
Turn the listing, photos and certificates into cost lines with ranges and their basis.

### 3. `dwellings` — `property-architect`
Establish, unit by unit, which dwellings are legally recognized and what proves it.
- Runs only when the deal counts on more dwellings than the documents prove, a division, or a change of use. Otherwise it is recorded as skipped, with that reason.

### 4. `notary` — `property-notary`
Say what the investor would sign, what he inherits, and what to ask before signing.
- Also loads `auction-conditions` when the property is sold at a public sale.
- Also loads `co-ownership-file` when the property is in a co-ownership.

### 5. `tax-be` — `property-accountant-be`
Set out the Belgian tax regimes and costs as scenarios, with their conditions.
- Runs only when the property is in Belgium or a Belgian company buys it. Otherwise it is recorded as skipped, with that reason.

### 6. `tax-fr` — `property-accountant-fr`
Set out the French tax treatment and flag the Belgian side to the Belgian accountant.
- Runs only when the property is in France. Otherwise it is recorded as skipped, with that reason.

### 7. `strategy` — `property-investment-partner`
Test every way to make the property pay, across optimistic, realistic and worst cases.

### 8. `law` — `property-lawyer`
Answer the legal questions the deal raises, on the primary text with its version date.
- Runs only when a clause, a lease or a dispute shapes the deal. Otherwise it is recorded as skipped, with that reason.

### 9. `synthesis` — `property-coordinator`
Run the expert debate where experts disagree, then write one synthesis that names its weak assumptions.

### 10. `decide` — the investor
The investor decides. Nothing is sent to an agency, notary, co-ownership manager or seller without his approval.
- Asks: make an offer, pass, or ask for more on a named point

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| Profiles installed: `property-accountant-be`, `property-accountant-fr`, `property-architect`, `property-coordinator`, `property-investment-partner`, `property-lawyer`, `property-notary`, `property-works-estimator` | each step runs as its own profile | `hermes profile list` |
| A way to hand a step to another profile, when there is no board (`delivery.handoff`) | steps that are not yours | the profile answers a test brief |
| The `kanban` toolset, when `delivery.board` is `hermes-kanban` | one card per step | `kanban_list` answers |
| A way to reach the owner (`owner.channel`) | human steps | the owner answers there |

If a required prerequisite is missing, stop before step 1. Say which one, what it blocks, and the smallest access that would unblock it. A step whose profile is not installed is never run under another profile: report the workflow as blocked at that step. Never report a step done that its profile did not complete.

## Configuration
- `delivery.board` decides how the workflow runs (below).
- `delivery.handoff` decides how a step reaches another profile when no board runs the workflow (below).
- `property.investor_file`: Where the investor's profile and own rules live.
- `property.jurisdictions`: Regions and countries in play. Detect from the property's address, then confirm.
- `owner.channel`: Where questions and owner actions reach the owner.

Current values appear in the `[Skill config]` block when this skill loads; an unset key shows its declared default. Persist a value with `hermes config set skills.config.<key> <value>` (per profile: `hermes -p <profile> config set …`); `hermes config migrate` prompts for keys still unset.

## Run it
### On a Hermes Kanban board (`delivery.board: hermes-kanban`)
1. Create every card up front, in step order, with `kanban_create`: title `property-deal-review: <step> — <work item>`, `assignee` the step's profile, `skills` the step's skills (plus the ones every step loads, and any extra skill whose condition holds), `parents` the cards of its After steps, and a body with the step's instructions, what it must produce and a link to the work item. For a step with an "On failure" target, the body also says: on a problem, comment the findings and block the card instead of completing it. The dispatcher starts each card when its parents are done.
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
- Every figure in the synthesis is a range with its basis and the date it was read.
- Missing data is named as missing, never estimated to move forward.
- Every step is done, or skipped with the reason its condition did not hold; every human decision is recorded verbatim.

## Report
Each update names the workflow, the current step and its actor, links the cards or the work item, and says what is needed from whom, if anything.
