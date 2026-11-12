---
name: plans-and-takeoffs
description: "Take areas and quantities off plans or surveys"
metadata:
  hermes:
    config:
      - key: property.jurisdictions
        description: "Regions in play, e.g. BE-WAL,BE-BRU,BE-VLA,FR; or detect"
        default: "detect"
---
# Plans, measurements and quantity takeoffs

## When to use

When a deal comes with plans (permit, basic deed, architect's drawings, agency
sketch); when `property-works-estimator` needs quantities; when the announced
floor area must be checked against a document.

## Prerequisites

| Needs | Why | Check |
|---|---|---|
| The plans or surveys (required) | every takeoff starts there | scale or dimensions are legible |
| The applicable area definition (for a sale or a lease) | legal areas differ by country | the text that defines it has been read |

If a required prerequisite is missing, stop before step 1. Say which one, what
it blocks, and the smallest access that would unblock it (read-only first). Do
the parts that do not need it only if they still make sense alone. Never
replace data you could not read with an estimate, and never report "nothing
found" when the lookup failed.

## Configuration

- `property.jurisdictions`: decides which legal area definition to read (in
  France, the private area of a co-ownership unit has its own). `detect`
  (default): country derived from the address.

If a value is unset or `detect`, say what you used, and give the line that
sets it: `hermes config set skills.config.<key> <value>` (one profile:
`hermes -p <profile> config set …`).

## Steps

1. **Identify each document**: type, author, date, scale, revision. A plan
   without a scale or dimensions is only a sketch.
2. **Tell the areas apart**: habitable, usable, gross, footprint, and the one
   the listing uses. Say which one you measure.
3. **Use written dimensions** rather than measuring a drawing; if you must
   measure to scale, say so and widen the range.
4. **Cross-check**: plan against deed, plan against listing, plan against
   photos. An area gap is a fact to pass to `property-investment-partner`: it
   is often the discount, or the trap.
5. **Do the takeoffs per work item**: walls (length × height, openings
   deducted), floors and ceilings, roof (pitch included), joinery (number and
   sizes), networks (estimated lengths).
6. **Add waste and offcuts** as a separate line, never buried in the
   quantity.
7. **Send the quantities** to `property-works-estimator` with their source and
   precision.

## Output

A table of areas (document, type of area, value, source, precision) and a
table of quantities (work item, unit, quantity, method, source). At the top:
the main gap between documents, if there is one.

## Pitfalls

- Taking the listing's area for granted: it is there to sell.
- Measuring a printed or scanned plan without checking the real scale.
- Forgetting heights: an area under a certain ceiling height does not always
  count as habitable.
- Mixing plans of different dates without saying so.
