---
name: expert-debate
description: "Run an adversarial debate between experts"
metadata:
  hermes:
    config:
      - key: property.investor_file
        description: "Where the investor file lives: memory or a path"
        default: "memory"
      - key: owner.channel
        description: "Where questions reach the investor (free text)"
        default: "this conversation"
---
# Expert debate

## When to use

Before an offer or a bid; when two opinions diverge; when the investor asks
"what do they all think?"; for a periodic review of open deals, if a scheduled
task carries it.

## Prerequisites

| Needs | Why | Check |
|---|---|---|
| Delegation and at least two installed experts (required) | a debate needs voices | the target profiles are among the installed profiles |
| The file: property, region, price, documents (required) | everyone answers the same file | every data point has its source |

If a required prerequisite is missing, stop before step 1. Say which one, what
it blocks, and the smallest access that would unblock it (read-only first). Do
the parts that do not need it only if they still make sense alone. Never
replace data you could not read with an estimate, and never report "nothing
found" when the lookup failed.

## Configuration

- `property.investor_file`: where thresholds and parameters come from; in
  `memory` (default), copy them into the shared question.
- `owner.channel`: where the synthesis of a periodic review goes; default,
  this conversation. No scheduled task, no periodic review.

If a value is unset or `detect`, say what you used, and give the line that
sets it: `hermes config set skills.config.<key> <value>` (one profile:
`hermes -p <profile> config set …`).

## Steps

1. **State the file once, for everyone**: property, region, price, intended
   deal structure, useful investor-file data, available documents and their
   dates, what is missing.
2. **Choose the voices**: `property-investment-partner` for the trade-off, and
   every expert whose domain can kill the deal (recognized dwellings, an
   auction-conditions clause, the duty regime, the works budget, a running
   lease).
3. **First round**: each expert answers the same question, in its domain — its
   position, its figures as ranges, the weak assumption, what it did not
   verify.
4. **Second round, adversarial**: each position goes to the others ("what, in
   your domain, overturns this conclusion?"). `property-investment-partner`
   plays the skeptical partner.
5. **Recalculate** what must be recalculated: an expert who changes an
   assumption (budget, regime, number of units) changes the ceiling price;
   redo it backwards.
6. **Synthesize** without adding your own position.

## Output

- What the experts agree on, with figures as ranges.
- What diverges: both positions quoted, their reasons, and the data or
  document that would decide between them.
- What makes a strategy impossible (not merely risky), if anything.
- The weakest assumption of the deal.
- The next action, its owner, and at most one question for him.

## Pitfalls

- A debate where each expert answers a different question: ask the same one.
- A synthesis that averages the disagreement away: two opposite opinions do
  not make a lukewarm one.
- Deciding yourself: the trade-off is his.
- Reopening the debate on a trade-off he has already made: it applies.
