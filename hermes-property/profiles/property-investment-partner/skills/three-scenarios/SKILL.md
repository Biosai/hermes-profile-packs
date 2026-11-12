---
name: three-scenarios
description: "Run a strategy through three scenarios and a ceiling price"
metadata:
  hermes:
    config:
      - key: property.investor_file
        description: "Where the investor file lives: memory or a path"
        default: "memory"
---
# Three scenarios and the ceiling price

## When to use

For every costed strategy before an offer, a bid or exercising an option;
when the investor asks "how high can I go?".

## Prerequisites

| Needs | Why | Check |
|---|---|---|
| The works budget per level (required) | works in each scenario | the opinion of `property-works-estimator` is quoted |
| The exit value as a range (required) | exit price | named comparables, sample size |
| The scenario parameters (investor file, or proposed) | discount, overrun, duration | the file gives them, or they are confirmed |

If a required prerequisite is missing, stop before step 1. Say which one, what
it blocks, and the smallest access that would unblock it (read-only first). Do
the parts that do not need it only if they still make sense alone. Never
replace data you could not read with an estimate, and never report "nothing
found" when the lookup failed.

## Configuration

- `property.investor_file`: scenario parameters and minimum margins. In
  `memory` (default), ask `property-coordinator` for them; if missing, propose
  them, marked "to be confirmed".

If a value is unset or `detect`, say what you used, and give the line that
sets it: `hermes config set skills.config.<key> <value>` (one profile:
`hermes -p <profile> config set …`).

## Steps

1. **Take the parameters from his investor file**: resale discount, works
   overrun, duration of each scenario, minimum margin per type of deal. If
   they are not there, propose some, say which ones you used, and have them
   confirmed through the coordinator.
2. **Optimistic**: exit at market price (comparables), short duration, works
   at the low end of the range.
3. **Realistic**: exit below market, longer duration, works in the middle.
4. **Safety**: exit well below market, works overrun, doubled duration,
   holding costs to match.
5. **Compute the ceiling price**: exit price − exit costs − works − holding
   costs − minimum margin − acquisition costs (which themselves depend on the
   price: solve for it, do not approximate).
6. **Redo the calculation backwards**: from the ceiling price, find the margin
   again. If you cannot, the calculation is wrong.
7. **Name the assumption that tips everything**: how far must it move for the
   safety scenario to fall below the threshold?

## Output

For each strategy: a three-column table (optimistic, realistic, safety) —
exit price, works, holding, costs, profit, margin, duration —, the ceiling
price, the backwards check, and the sensitive assumption with its tipping
point. Verdict: holds or does not hold in the safety scenario.

## Pitfalls

- A ceiling price without its three assumptions (works, comparables, tax
  regime) cannot be audited.
- Computing duties on the asking price, then bidding above it: costs follow
  the price.
- A safety scenario that is just a slightly worse realistic one: it must be
  able to happen, not merely disappoint.
- Promising the optimistic scenario: it is a bound, not a forecast.
