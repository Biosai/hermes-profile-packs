---
name: market-value-comparables
description: "Estimate market value from four named comparables"
metadata:
  hermes:
    config:
      - key: property.jurisdictions
        description: "Regions in play, e.g. BE-WAL,BE-BRU,BE-VLA,FR; or detect"
        default: "detect"
---
# Market value from comparables

Use when an exit price (resale), the value of a kept unit or a market rent is needed, or a value put forward by a seller or an agency must be checked.

## Prerequisites

| Needs | Why | Check |
|---|---|---|
| The property: type, sourced area, condition, neighborhood (required) | comparison criteria | every criterion has its source |
| Access to listings and published prices (required) | find the comparables | a search returns dated results |

If a required prerequisite is missing, stop before step 1. Say which one, what
it blocks, and the smallest access that would unblock it (read-only first). Do
the parts that do not need it only if they still make sense alone. Never
replace data you could not read with an estimate, and never report "nothing
found" when the lookup failed.

## Configuration

- `property.jurisdictions`: in France (FR), look first for published realized
  prices (DVF); in Belgium, check which source of realized prices exists,
  otherwise the comparables are asking prices. `detect` (default): country
  derived from the address.

If a value is unset or `detect`, say what you used, and give the line that
sets it: `hermes config set skills.config.<key> <value>` (one profile:
`hermes -p <profile> config set …`).

## Procedure

1. **Define the target property**: type, floor area (source), floor level,
   condition, outdoor space, parking, precise neighborhood. These are your
   comparison criteria.
2. **Search for comparables**: same type, similar area, same neighborhood,
   comparable condition seen in the photos. For each, note: source, address or
   location, area, price, capture date, and whether it is an **asking price**
   (listing) or a **realized price** (published transaction, completed public
   sale).
3. **In France**, transactions are published (the DVF land-value data): use
   realized prices first. **In Belgium**, check which public source of
   realized prices exists for the area; otherwise your comparables are asking
   prices, and you say so.
4. **Exclude, naming them**, the ones clearly out of line, above as well as
   below, with the reason (condition, area, view, listing error).
5. **Keep at least four comparables.** Fewer than four: still give the range,
   with the sample size and a note that the base is weak.
6. **Adjust** for differences in area and condition, saying by how much and
   why; an unjustified adjustment is not made.
7. **Give the range** (low, median, high) and the sample size.

## Decision rules

- A municipality's median €/m² sorts listings; it does not value a property,
  which neighborhood and condition distort.
- A listing is an asking price, not a realized price; one that stayed online
  for a long time is a price that did not happen.
- A comparable without a capture date is a potentially wrong comparable.
- Compare like with like: never a flat with houses, or a let property with
  vacant ones.
- Explain a discount: if the property is below market, say why. If it is
  because of works the investor does at cost price, that is the investor's
  ground; otherwise, look for what the market knows and you do not.

## Quality gate

The valuation is done when it rests on named, dated comparables and states how
many. The deliverable is a table of the comparables kept (source, location,
area, price, €/m², date, asking or realized, adjustment), the excluded ones
with their reason, and the range with its sample size.
