---
name: works-estimate
description: "Estimate a property's works per level of intervention"
metadata:
  hermes:
    config:
      - key: property.cost_library
        description: "Path to the work-item cost library, or none"
        default: "none"
      - key: property.investor_file
        description: "Where the investor file lives: memory or a path"
        default: "memory"
---
# Works estimate

Use when `property-investment-partner` weighs a deal, a ceiling price is needed, resale must be compared with letting, or a budget that came from elsewhere must be checked.

## Prerequisites

| Needs | Why | Check |
|---|---|---|
| The property review: photos, listing, certificates (required) | visible items | the skill `listing-photo-review` has been run |
| A price base (required) | no market average | each item names its base: library, cost price or dated captured price |

If a required prerequisite is missing, stop before step 1. Say which one, what
it blocks, and the smallest access that would unblock it (read-only first). Do
the parts that do not need it only if they still make sense alone. Never
replace data you could not read with an estimate, and never report "nothing
found" when the lookup failed.

## Configuration

- `property.cost_library`: a path → the default base; `none` (default) → every
  item rests on a captured, dated price, status "captured price, indicative".
- `property.investor_file`: whether the investor does the works, which trades,
  at what cost price; unreadable → a contractor's estimate, stated.

If a value is unset or `detect`, say what you used, and give the line that
sets it: `hermes config set skills.config.<key> <value>` (one profile:
`hermes -p <profile> config set …`).

## Procedure

1. **Read the investor file**: does the investor do the works personally,
   which trades, at what cost price? The items the investor does are costed at
   their cost price; the others as a contractor's estimate.
2. **Start from the property review** (skill `listing-photo-review`) and the
   quantities (`property-architect` if plans exist).
3. **Define three levels**: as is (making safe only), refresh (finishes,
   sanitary fittings, paint), full renovation (services, envelope, energy-class
   jump if targeted).
4. **Per item and per level**: quantity × base price (library line, cost
   price, or a captured and dated price), as a low and high range. Each item
   names its base, in the order of
   [references/price-bases.md](references/price-bases.md).
5. **Contingency** as a separate line, wider when there has been no viewing.
6. **Obligations**: a renovation that targets an energy class or triggers an
   obligation follows the text in force (skill
   `renovation-obligations-and-aid`); no equipment that is being phased out is
   budgeted. Flag compulsory site insurance (ten-year liability, *décennale*,
   in Belgium and in France): its texts are **TO VERIFY** before a threshold
   is cited.
7. **Duration** of each level as a range: it is a holding assumption for
   `property-investment-partner`.
8. **Read it backwards**: is the total divided by the area plausible for that
   level? If not, find the faulty item.

## Decision rules

- Cost items, never an overall price per m²: nobody knows what an overall
  price counts.
- Cost at the investor's cost price only what the investor does personally.
- Count ancillary costs: waste removal, scaffolding, connections, protection,
  cleaning.
- A budget without "to check at the viewing" claims to know what it does not.
- Areas come from a document: an item per m² on a listing's area inherits the
  listing's error.

## Quality gate

The estimate is done when the backwards reading is plausible for each level
and every item names its base. The deliverable is a budget per level (items,
quantities, ranges, contingency, total, duration), what remains unknown
without a viewing, and the status line: "base: library, indicative", "base:
captured price, indicative", "base: cost price from the investor file" or
"base: the investor's actual job <reference>". Amounts exclude VAT; VAT is
`property-accountant-be`'s business.
