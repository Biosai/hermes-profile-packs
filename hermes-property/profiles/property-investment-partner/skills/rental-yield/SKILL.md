---
name: rental-yield
description: "Compute a rental's cash flow and yield, before tax"
metadata:
  hermes:
    config:
      - key: property.jurisdictions
        description: "Regions in play, e.g. BE-WAL,BE-BRU,BE-VLA,FR; or detect"
        default: "detect"
      - key: property.investor_file
        description: "Where the investor file lives: memory or a path"
        default: "memory"
---
# Rental yield

Use when a property or a unit is meant to be let or kept after a division, or when resale and letting must be compared.

## Prerequisites

| Needs | Why | Check |
|---|---|---|
| The address and type of letting (required) | regime, authorizations, rents | region and type are established |
| The official rent grid, if the region publishes one | rent is read, not estimated | the grid opens with its date |
| The investor file (for the yield threshold) | compare with the threshold | the file can be read; otherwise no threshold verdict |

If a required prerequisite is missing, stop before step 1. Say which one, what
it blocks, and the smallest access that would unblock it (read-only first). Do
the parts that do not need it only if they still make sense alone. Never
replace data you could not read with an estimate, and never report "nothing
found" when the lookup failed.

## Configuration

- `property.jurisdictions`: decides the rent grid, the short-term letting
  rules and the lease regime. `detect` (default): derive the region from the
  property's address, state it, and have it confirmed.
- `property.investor_file`: the yield threshold for a kept unit; in `memory`
  (default), ask `property-coordinator` for it.

If a value is unset or `detect`, say what you used, and give the line that
sets it: `hermes config set skills.config.<key> <value>` (one profile:
`hermes -p <profile> config set …`).

## Procedure

1. **Qualify the type of letting**: long-term, shared housing, short-term
   (furnished tourist let), furnished corporate lets (stays of a few months).
   Each type has its legal regime (`property-lawyer`), its tax regime (the
   accountants) and its authorizations (`property-architect`: change of use,
   registration).
2. **Check that it is allowed**: short-term letting that is prohibited or
   needs an authorization not yet obtained comes out "impossible".
3. **Source the rents**:
   - if the region publishes an **indicative rent grid**, read it on the
     official site, with its date; do not estimate it;
   - otherwise, at least four named comparable listings;
   - short-term: a nightly price and an occupancy rate usually have no
     reliable public source; present them as **scenarios**, never as a
     measurement;
   - shared housing: only where demand is shown (listings, platforms, nearby
     institutions).
4. **List the costs**: property tax, insurance, maintenance, management,
   vacancy, non-recoverable charges, cleaning and linen for short-term
   letting, furniture and its replacement for furnished lets.
5. **Compute** as ranges: annual rent, costs, cash flow before tax, gross and
   net yield on the total cost price.
6. **Compare** with the threshold in the investor file for a kept unit.

## Decision rules

- The rent quoted by the seller, or the running lease, is a data point, not a
  comparable: never take it as a market rent.
- An "average" short-term occupancy rate found online is at best a scenario.
- Without the accountant's opinion on the investor's taxation, the figure
  stays before tax, and says so.
- Never dress a rental deal up as a resale ceiling price.

## Quality gate

The work is done when every rent has a dated source and every assumption
without one is marked as a scenario. The deliverable gives, per type of
letting: rent (source, date), costs, cash flow **before tax** (the label is
mandatory), gross and net yields, as ranges, with the vacancy and occupancy
assumptions marked as scenarios.
