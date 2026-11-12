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

## When to use

When the investor or an expert asks for the after-tax result of a deal,
compares resale with keeping the property, or asks about taking a property out
of the company.

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

- `property.investor_file`: how he wants tax shown, and what his accountant
  confirmed. In `memory` (default), ask `property-coordinator`; unreadable →
  cost before tax and say so.

If a value is unset or `detect`, say what you used, and give the line that
sets it: `hermes config set skills.config.<key> <value>` (one profile:
`hermes -p <profile> config set …`).

## Steps

1. **Read his rule in the investor file**: does he judge a deal before tax,
   the tax being computed at year end on all the company's profits, or does he
   want an after-tax result per deal? Apply it; without it, cost before tax
   and say so.
2. **Qualify the property**: inventory (bought to resell) or fixed asset
   (kept, let). The qualification changes the accounting treatment, the
   capital gain and depreciation; his accountant confirms it.
3. **Read the income tax code in force** (Code des impôts sur les revenus
   1992): ordinary rate, reduced rate and its conditions (director's pay,
   shareholding structure, size), capital gains regimes, depreciation rules.
4. **Compute the deal's result**: margin, deductible costs, depreciation where
   relevant. Depreciation defers tax, it does not remove it: say so.
5. **Present the tax as a range**, one scenario per possible rate, until his
   accountant has confirmed the company's situation.
6. **Flag the personal effects**: salary, dividend, rent he receives from the
   company, benefits in kind. That is often where the trade-off lies, and his
   accountant decides it.

## Output

The qualification (inventory or fixed asset, to be confirmed), the result
before tax, the tax as a range per rate scenario, the text and version, the
personal effects flagged, and the question for his accountant.

## Pitfalls

- A table that mixes depreciation alone with the overall result of a property
  compares two different things.
- Applying the reduced rate without checking all its conditions.
- Adding a tax block that his rule excludes from per-deal presentation.
- Forgetting that a company's tax depends on all its results, not on a single
  deal.
