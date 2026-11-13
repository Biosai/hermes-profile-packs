---
name: deal-costs
description: "List and cost every cost of a deal"
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
# Costs of a deal

Use when a ceiling price, a margin or a yield must be calculated, or a yield spreadsheet that came from elsewhere must be checked.

## Prerequisites

| Needs | Why | Check |
|---|---|---|
| The address, price and type of sale (required) | the costs depend on them | region established, price sourced |
| The auction conditions (required for a public sale) | auction fees | the full conditions open |

If a required prerequisite is missing, stop before step 1. Say which one, what
it blocks, and the smallest access that would unblock it (read-only first). Do
the parts that do not need it only if they still make sense alone. Never
replace data you could not read with an estimate, and never report "nothing
found" when the lookup failed.

## Configuration

- `property.jurisdictions`: duties, local taxes and scales of the region.
  `detect` (default): derive the region from the property's address, state it,
  and have it confirmed.
- `property.investor_file`: whether tax is part of the exit costs, per the
  investor's presentation rule.

If a value is unset or `detect`, say what you used, and give the line that
sets it: `hermes config set skills.config.<key> <value>` (one profile:
`hermes -p <profile> config set …`).

## Procedure

1. **Entry costs**: registration duties or VAT (dedicated skills), deed costs
   and the notary's fees (statutory scale to read, disbursements), public-sale
   costs set by the auction conditions (*cahier des charges*), mortgage and
   loan arrangement costs, any search or commission fees.
2. **Holding costs**: interest, property withholding tax (*précompte
   immobilier*) or French property tax, insurance, co-ownership charges,
   energy and upkeep of an empty building, municipal taxes on vacant
   buildings, duration taken from the scenario.
3. **Exit costs**: agency commission or public-sale costs, certificates and
   reports required for the sale, mortgage release, division costs (basic deed
   (*acte de base*), surveyor), tax according to the rule in the investor
   file.
4. **Source every cost**: scale read (with its date), quote, auction
   conditions quoted, or an assumption marked as such.
5. **Treat costs that depend on the price** as functions of the price, not
   fixed amounts: they move with the bid.
6. **Mixed structure**: acquisition costs apply to what is bought, not to the
   full price of a deal where part stays under option.

## Decision rules

- Never use a flat percentage for "notary costs": it hides items that do not
  follow the same base.
- Count the holding costs of an empty building during a permit or works.
- Public-sale costs differ from private-sale costs: read the auction
  conditions.
- Count each item once: never both in costs and in works.

## Quality gate

The work is done when every cost is sourced or marked as an assumption, and
every cost that depends on the price is a function of it. The deliverable is a
table in three blocks (entry, holding, exit): item, calculation base, amount
as a range, source and date; plus the total as a percentage of the price, as a
check, never as a calculation rule.
