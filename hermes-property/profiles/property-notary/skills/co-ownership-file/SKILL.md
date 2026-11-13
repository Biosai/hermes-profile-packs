---
name: co-ownership-file
description: "Read the co-ownership manager's file and basic deed"
metadata:
  hermes:
    config:
      - key: property.jurisdictions
        description: "Regions in play, e.g. BE-WAL,BE-BRU,BE-VLA,FR; or detect"
        default: "detect"
---
# Co-ownership file

Use when a flat or a unit in a co-ownership is considered, the investor wants to resell a building unit by unit, or a bid on a unit is being prepared.

## Prerequisites

| Needs | Why | Check |
|---|---|---|
| The co-ownership manager's file (required for a ceiling price) | without it, no ceiling price | minutes, funds, works and charges open |
| The basic deed and regulations (required for a sale by units) | sellable units, shares | the deed opens |
| The auction conditions or the sale agreement | the cost-splitting clause | the clause can be quoted |

If a required prerequisite is missing, stop before step 1. Say which one, what
it blocks, and the smallest access that would unblock it (read-only first). Do
the parts that do not need it only if they still make sense alone. Never
replace data you could not read with an estimate, and never report "nothing
found" when the lookup failed.

## Configuration

- `property.jurisdictions`: which splitting rule to read (Belgian Code civil;
  in France, the co-ownership regime, TO VERIFY without a text read). `detect`
  (default): derive the region from the property's address, state it, and have
  it confirmed.

If a value is unset or `detect`, say what you used, and give the line that
sets it: `hermes config set skills.config.<key> <value>` (one profile:
`hermes -p <profile> config set …`).

## Procedure

1. **Is there a basic deed and a co-ownership manager?** The basic deed (*acte
   de base*, the master deed of the co-ownership) and the manager (*syndic*)
   are the first question, before any calculation. Without a basic deed, no
   unit can be sold separately.
2. **Ask for the manager's file**: minutes of the latest general meetings,
   state of the working capital and reserve fund, works voted or planned,
   current calls for funds, ordinary charges of recent years, pending
   disputes, debts of the co-ownership.
3. **Read the general meetings**: works voted (amount, schedule, the unit's
   share), works discussed but not voted, proceedings.
4. **Who pays what after the sale**: in Belgium, the law splits between seller
   and buyer the expenses voted before the sale (Code civil, art. 3.94, § 2 —
   read the version in force), but it is a **default** rule: in a private sale
   it is negotiated; in a public sale the clause in the auction conditions
   prevails. Read the clause.
5. **Basic deed and regulations**: private and common parts, shares, use of
   the units, restrictions on use (short-term letting, professional
   activity).
6. **For a sale by units**: does a basic deed have to be drawn up or amended,
   at what cost (surveyor, notary) and with what timeline?
7. **Cost** the unit's share of the voted works, the annual charges and the
   reserve fund, and pass them to `property-investment-partner`.

## Decision rules

- No ceiling price on a flat without the manager's file: it comes out without
  one, and the reason is stated.
- A flat is not costed like a house: charges, common works and regulations
  change everything.
- Never ignore a use restriction that rules out the intended rental strategy.
- Never presume the legal split when a clause sets it aside.

## Quality gate

The reading is done when the manager's file and the basic deed were read, or
their absence is stated with what it blocks. The deliverable says whether a
basic deed and a manager exist, and contains a table of the unit's commitments
(works voted, calls for funds, charges, reserve fund) with their source; the
clause that splits expenses between seller and buyer, quoted; the use
restrictions; and the missing documents.
