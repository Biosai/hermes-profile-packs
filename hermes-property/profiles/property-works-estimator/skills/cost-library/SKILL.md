---
name: cost-library
description: "Keep the work-item cost library and its dated prices"
metadata:
  hermes:
    config:
      - key: property.cost_library
        description: "Path to the work-item cost library, or none"
        default: "none"
      - key: property.investor_file
        description: "Where the investor file lives: memory or a path"
        default: "memory"
      - key: property.jurisdictions
        description: "Regions in play, e.g. BE-WAL,BE-BRU,BE-VLA,FR; or detect"
        default: "detect"
---
# Cost library

## When to use

When an estimate item has no line; when a price is more than a few months
old; when the investor gives an actual job cost or a cost price; for a
periodic review, if a scheduled task carries it.

## Prerequisites

| Needs | Why | Check |
|---|---|---|
| A location for the library (required to keep it) | a line must outlive the session | `property.cost_library` names a readable, writable path |
| Captured, sourced and dated prices (required) | an undated line is not used | every price has its source |

If a required prerequisite is missing, stop before step 1. Say which one, what
it blocks, and the smallest access that would unblock it (read-only first). Do
the parts that do not need it only if they still make sense alone. Never
replace data you could not read with an estimate, and never report "nothing
found" when the lookup failed.

## Configuration

- `property.cost_library`: a path → the library to read and update; `none`
  (default) → there is none: offer to start one at a path he chooses; until
  then, lines stay in the answer, marked "not kept".
- `property.investor_file`: his hourly cost and cost prices, if he does the
  works.
- `property.jurisdictions`: the re-indexation index (in Belgium, the ABEX
  index; in France, the published building indices). `detect` (default):
  country of the jobs.

If a value is unset or `detect`, say what you used, and give the line that
sets it: `hermes config set skills.config.<key> <value>` (one profile:
`hermes -p <profile> config set …`).

## Steps

1. **One line per work item**, with a clear unit (m², linear meter, piece,
   lump sum): description, composition (materials and quantities per unit),
   labor time per unit, sources.
2. **Materials**: supplier price captured, with source and date; price
   excluding VAT; waste and offcuts as a separate percentage.
3. **Labor**: labor time × hourly cost. If his investor file gives his real
   hourly cost, that is his cost price; otherwise a contractor's hourly cost,
   marked as an estimate.
4. **Indexation**: every price carries its date; re-index it on a public
   construction cost index (in Belgium, the ABEX index), stating the index
   and the date used.
5. **Actual job**: when the investor gives an actual cost (invoice, final
   account), record it with its source; it overrides the line it covers and
   serves to recalibrate the line.
6. **Status of each line**: "actual job", "cost price from his file",
   "library, indicative".
7. **Check**: a line without a source or a date is not used for estimates
   until it is completed.

## Output

The complete work-item line (composition, time, dated price, index, status),
or the list of lines to refresh, with their age.

## Pitfalls

- Copying an average price found online: it is a seller's price, not a work
  item line.
- Mixing excluding-VAT and including-VAT prices in the same line.
- Letting a line age without re-indexing: a figure without a capture date is
  a potentially wrong figure.
- Asking the investor for his actual jobs: they improve the base, they do not
  condition it.
