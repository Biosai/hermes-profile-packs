---
name: deal-strategies
description: "Test every strategy on a property before ruling one out"
metadata:
  hermes:
    config:
      - key: property.investor_file
        description: "Where the investor file lives: memory or a path"
        default: "memory"
      - key: property.jurisdictions
        description: "Regions in play, e.g. BE-WAL,BE-BRU,BE-VLA,FR; or detect"
        default: "detect"
---
# Every strategy on a property

## When to use

As soon as a concrete property arrives (listing, public sale, seller's offer,
a building he already owns) and someone has to decide what to do with it.

## Prerequisites

| Needs | Why | Check |
|---|---|---|
| The facts of the property: address, price, area, with sources (required) | nothing can be costed without them | every fact has its source |
| The investor file (required to rule out on a threshold) | accepted strategies, thresholds, areas | the file can be read; otherwise nothing is ruled out on a threshold, and you say so |
| The opinions of the architect, works estimator and accountant | recognized units, budget, costs | their answers are quoted |

If a required prerequisite is missing, stop before step 1. Say which one, what
it blocks, and the smallest access that would unblock it (read-only first). Do
the parts that do not need it only if they still make sense alone. Never
replace data you could not read with an estimate, and never report "nothing
found" when the lookup failed.

## Configuration

- `property.investor_file`: in `memory` (default), ask `property-coordinator`
  for thresholds, areas and accepted strategies; a path → read them.
- `property.jurisdictions`: a strategy that needs a region outside the list is
  flagged. `detect` (default): derive the region from the property's address,
  state it, and have it confirmed.

If a value is unset or `detect`, say what you used, and give the line that
sets it: `hermes config set skills.config.<key> <value>` (one profile:
`hermes -p <profile> config set …`).

## Steps

1. **Read his investor file**: accepted or refused strategies, by area;
   thresholds; scenario parameters; whether he does the works.
2. **Establish the facts of the property**: region, type, floor area
   (source), announced and recognized units (`property-architect`), condition
   (`property-works-estimator`), occupancy, co-ownership (`property-notary`).
   Name what is missing.
3. **List every plausible strategy** before ruling one out:
   - option on all units; option on some units + purchase of the rest;
   - purchase, division, full resale, or partial resale keeping some units;
   - resale as is, refreshed, fully renovated;
   - long-term letting, shared housing, short-term letting, furnished
     corporate lets;
   - splitting off land, garages, volumes; combinations.
4. **Rule out with a written reason**: outside his areas per his file,
   impossible (unrecognized unit, short-term letting prohibited), or margin
   below his threshold after calculation. "It does not look interesting" is
   not a reason.
5. **Cost each remaining strategy** as a range: entry price, acquisition costs
   (scenarios from `property-accountant-be`), works per level
   (`property-works-estimator`), holding costs, exit price or rents
   (comparables), exit costs.
6. **Run them through the three scenarios** (skill `three-scenarios`).
7. **Rank**: the best first, the one that holds in the safety scenario
   marked.

## Output

A table of strategies: profit (range), margin on purchase price, equity tied
up, return on equity, duration, holds in safety (yes/no), and the strategies
ruled out with their reason. Footer: works cost, comparables base, acquisition
tax regime.

## Pitfalls

- Ruling out a building on a whole-building resale alone, without testing
  division or partial resale.
- Mixing regimes: a rental is judged on cash flow and yield, not on a resale
  ceiling price.
- Applying acquisition costs to the full price of a deal where part of the
  property stays under option.
- Proposing a strategy that his file reserves for another area: flag it.
