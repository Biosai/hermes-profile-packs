---
name: vat-regimes
description: "Say which Belgian VAT regime applies to the deal"
metadata:
  hermes:
    config:
      - key: property.investor_file
        description: "Where the investor file lives: memory or a path"
        default: "memory"
---
# Property VAT regimes (Belgium)

Use when a works budget must be costed VAT included, a new building is sold or bought, a letting includes services, or the investor considers demolishing and rebuilding.

## Prerequisites

| Needs | Why | Check |
|---|---|---|
| The operation and the use after works (required) | the regime depends on them | described in writing |
| The building's age (required for a reduced rate) | condition of the reduced rate | a document dates the first occupation |
| Access to the VAT code and its decrees (required) | no rate from memory | the text opens with its date |

If a required prerequisite is missing, stop before step 1. Say which one, what
it blocks, and the smallest access that would unblock it (read-only first). Do
the parts that do not need it only if they still make sense alone. Never
replace data you could not read with an estimate, and never report "nothing
found" when the lookup failed.

## Configuration

- `property.investor_file`: whether the investor does the works through their
  own company, and their accountant's written answers, each limited to its
  case. In `memory` (default), ask `property-coordinator` for them.

If a value is unset or `detect`, say what you used, and give the line that
sets it: `hermes config set skills.config.<key> <value>` (one profile:
`hermes -p <profile> config set …`).

## Procedure

1. **Qualify the operation**: construction works (renovation, conversion,
   building), sale of a new building (in the VAT sense),
   demolition-reconstruction, letting (exempt in principle) or accommodation
   with services.
2. **Qualify the building and its use**: private dwelling or not, age of the
   building since first occupation, end user, use after works (residence,
   short-term letting, professional use).
3. **Read the VAT code and its royal decrees in force** (Federal Public
   Service Finance, SPF Finances), with the version date: standard rate,
   reduced rates and their cumulative conditions (age, use, the client's
   certificate, invoicing directly to the end user), temporary regimes and
   their end date.
4. **Check who invoices whom**: if the investor does the works through their
   own company, invoicing between their companies has its own rules; if a
   third-party contractor invoices, the client's certificate often conditions
   the reduced rate.
5. **For the sale of a new building**, say whether the sale is subject to VAT
   (and not to registration duties) and what that changes for the buyer.
6. **Cost** the effect on the budget from `property-works-estimator`: one
   scenario per possible rate while the conditions are not established.

## Decision rules

- Never apply a reduced rate to a use that excludes it: a change of use after
  the works can lose the rate.
- Never extend the accountant's written answer on one use to another use.
- A temporary regime has an end date: read it.
- VAT on the sale of a new building and registration duties are one or the
  other, depending on the qualification: establish it, do not confuse them.

## Quality gate

The work is done when the regime is established on the text in force, or left
as one scenario per possible rate. The deliverable contains the regime
retained or the scenarios, the text (article, version), the conditions and
evidence to gather (certificate, building age, use), the effect as a range on
the budget or price, and the question for the investor's accountant.
