---
name: registration-duties
description: "Cost registration duties, region by region"
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
# Registration duties (Belgium)

Use when an acquisition must be costed (private sale, public sale, exercise of an option, purchase of units, contribution in kind) or a ceiling price depends on entry costs.

## Prerequisites

| Needs | Why | Check |
|---|---|---|
| The property's address (required) | the region designates the code | municipality known |
| The buyer's status (required) | several regimes depend on it | the investor file or the articles of association say it |
| Access to the regional code in force (required) | no rate from memory | the text opens with its version date |

If a required prerequisite is missing, stop before step 1. Say which one, what
it blocks, and the smallest access that would unblock it (read-only first). Do
the parts that do not need it only if they still make sense alone. Never
replace data you could not read with an estimate, and never report "nothing
found" when the lookup failed.

## Configuration

- `property.jurisdictions`: which regional code to read (BE-WAL, BE-VLA,
  BE-BRU); FR → `property-accountant-fr`. `detect` (default): derive the
  region from the property's address, state it, and have it confirmed.
- `property.investor_file`: the default regime and the accountant's written
  answers; unreadable → every regime comes out as a scenario.

If a value is unset or `detect`, say what you used, and give the line that
sets it: `hermes config set skills.config.<key> <value>` (one profile:
`hermes -p <profile> config set …`).

## Procedure

1. **Establish the property's region**: Wallonia, Flanders and Brussels each
   have their own code of registration duties (*droits d'enregistrement*),
   their rates, regimes and time limits. Nothing carries over from one region
   to another.
2. **Establish the buyer**: company or individual, VAT-registered or not,
   declared activity. Several reduced regimes are reserved for individuals;
   another one for buy-to-resell professionals.
3. **Read the regional code in force**, with its version date: the rate of the
   ordinary regime, of the property dealer regime (*marchand de biens*), of
   any allowance, and their conditions. Note the article and version for each.
   Regimes:
   [references/belgian-tax-scope.md](references/belgian-tax-scope.md).
4. **List the conditions of the reduced regime** as the text writes them:
   status of the buyer, declaration or statement in the deed, guarantee,
   resale deadline, number of transactions, penalty if not resold.
5. **Read the investor file**: which regime the investor wants applied by
   default, and what their accountant's written answer confirmed.
6. **Cost one scenario per possible regime**: duties, base (price, or market
   value if higher), and effect on the ceiling price.
7. **Refund**: say whether the text provides a refund on a quick resale, under
   which conditions and within which time limit.
8. **Structures** (option, sale by units, split purchase, contribution in
   kind): the regime depends on the drafting; consult `property-notary` and
   present scenarios.

## Decision rules

- No rate from memory, and none from another region: scales change, and not
  all at the same time.
- A formal condition missing from the deed loses the reduced regime, often
  without a refund: the difference can be worth the whole margin.
- Costs follow the price: never compute duties on the asking price, then bid
  above it.
- Never apply an allowance reserved for individuals to a company.

## Quality gate

The costing is done when every rate was read in the regional code in force.
The deliverable is a table: regime, text (article, region, version), rate
read, base, duties as a range, conditions, who checks them (deed →
`property-notary`); the default regime from the investor file first, the other
as a scenario, noted "to be confirmed by the investor's accountant" until a
written answer has done so.
