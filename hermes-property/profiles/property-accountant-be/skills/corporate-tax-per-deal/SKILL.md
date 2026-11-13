---
name: corporate-tax-per-deal
description: "Handle the corporate income tax of a deal"
metadata:
  hermes:
    config:
      - key: property.investor_file
        description: "Where the investor file lives: memory or a path"
        default: "memory"
---
# Corporate income tax of a deal

Use when the investor acts through a company and the investor or an expert asks for the after-tax result of a deal, compares resale with keeping the property, or asks about taking a property out of the company.

## Prerequisites

| Needs | Why | Check |
|---|---|---|
| The deal's figures (required) | basis of the result | margin, costs and works sourced |
| The presentation rule in the investor file | per deal or at year end | the file can be read; otherwise before tax, and said |

If a required prerequisite is missing, stop before step 1. Say which one, what
it blocks, and the smallest access that would unblock it (read-only first). Do
the parts that do not need it only if they still make sense alone. Never
replace data you could not read with an estimate, and never report "nothing
found" when the lookup failed.

## Configuration

- `property.investor_file`: how the investor wants tax shown, and what their
  accountant confirmed. In `memory` (default), ask `property-coordinator`;
  unreadable → cost before tax and say so.

If a value is unset or `detect`, say what you used, and give the line that
sets it: `hermes config set skills.config.<key> <value>` (one profile:
`hermes -p <profile> config set …`).

## Procedure

1. **Read the investor's rule in the investor file**: is a deal judged before
   tax, the tax being computed at year end on all the company's profits, or is
   an after-tax result wanted per deal? Apply it; without it, cost before tax
   and say so.
2. **Qualify the property**: inventory (bought to resell) or fixed asset
   (kept, let). The qualification changes the accounting treatment, the
   capital gain and depreciation; the investor's accountant confirms it.
3. **Read the income tax code in force** (Code des impôts sur les revenus
   1992): ordinary rate, reduced rate and its conditions (director's pay,
   shareholding structure, size), capital gains regimes, depreciation rules.
4. **Compute the deal's result**: margin, deductible costs, depreciation where
   relevant. Depreciation defers tax, it does not remove it: say so.
5. **Present the tax as a range**, one scenario per possible rate, until the
   investor's accountant has confirmed the company's situation.
6. **Flag the personal effects**: salary, dividend, rent the investor receives
   from the company, benefits in kind. That is often where the trade-off lies,
   and the investor's accountant decides it. Detail:
   [references/company-and-investor.md](references/company-and-investor.md).

## Decision rules

- A table that mixes depreciation alone with the overall result of a property
  compares two different things: say so, also when the spreadsheet is the
  investor's own.
- Never apply the reduced rate without checking all its conditions.
- Do not add a tax block that the investor's rule excludes from per-deal
  presentation.
- A company's tax depends on all its results, not on a single deal.
- Say "before tax" out loud: a cash flow or a profit without tax carries the
  label.

## Quality gate

The work is done when the result is labelled before or after tax as the
investor file asks, and the tax is a range per rate scenario. The deliverable
contains the qualification (inventory or fixed asset, to be confirmed), the
result before tax, the tax as a range per rate scenario, the text and version,
the personal effects flagged, and the question for the investor's accountant.
