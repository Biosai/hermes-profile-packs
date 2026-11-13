---
name: materials-quantities-prices
description: "Turn takeoffs into materials, quantities and prices"
metadata:
  hermes:
    config:
      - key: property.cost_library
        description: "Path to the work-item cost library, or none"
        default: "none"
---
# Materials, quantities and prices

Use when a job is being prepared, a work-item line must be updated with current prices, or the investor asks for a shopping list or a supplier comparison.

## Prerequisites

| Needs | Why | Check |
|---|---|---|
| Sourced takeoffs (required) | quantities start there | every quantity names its source |
| Access to supplier prices (required) | captured, dated prices | a dated page or quote opens |

If a required prerequisite is missing, stop before step 1. Say which one, what
it blocks, and the smallest access that would unblock it (read-only first). Do
the parts that do not need it only if they still make sense alone. Never
replace data you could not read with an estimate, and never report "nothing
found" when the lookup failed.

## Configuration

- `property.cost_library`: a path → update the lines with the captured prices;
  `none` (default) → prices stay in the answer, dated.

If a value is unset or `detect`, say what you used, and give the line that
sets it: `hermes config set skills.config.<key> <value>` (one profile:
`hermes -p <profile> config set …`).

## Procedure

1. **Start from the takeoffs** (skill `plans-and-takeoffs` of
   `property-architect`, or a site survey): each quantity carries its source.
2. **Break each work item into materials**: main material, fixings,
   accessories, consumables. Use the supplier's sales unit (roll, pallet,
   pack), not only the work-item unit.
3. **Add waste and offcuts** per material type, as a separate line.
4. **Capture prices** from at least two suppliers where possible: product
   reference, price excluding VAT, unit, pack size, lead time, capture date,
   source (link or quote).
5. **Round up to the sales unit** and compute the real cost of the order.
6. **Compare**: gap between suppliers, equivalent products, lead times.
7. **Prepare the order as a draft**: supplier, references, quantities,
   captured price, delivery. It is never placed: the investor places it.
8. **Update the library**, if `property.cost_library` names one (skill
   `cost-library`), with the captured prices and their date.

## Decision rules

- A price without a date or a source is not used.
- Round up to the pack size: otherwise the order costs more than the takeoff.
- The order stays a draft, even after a "go ahead": the investor places it.
- Compare equivalent products only (thickness, class, certification).

## Quality gate

The list is done when every quantity names its source and every price its date
and supplier. The deliverable is a materials list (work item, article,
reference, net quantity, waste, ordered quantity, unit price, total, supplier,
capture date), the supplier comparison at the bottom, and the draft order if
requested.
