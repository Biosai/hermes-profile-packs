---
name: recognized-dwellings
description: "Establish, unit by unit, if a dwelling is legally recognized"
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
# Recognized dwellings

Use when a purchase option, a division, a unit-by-unit resale or a per-unit rental is calculated, or a listing, auction conditions or a seller announce a number of dwellings.

## Prerequisites

| Needs | Why | Check |
|---|---|---|
| The address or land registry reference (required) | region, municipality, documents to look for | the plot can be found on the land registry portal |
| Permit, planning information (required to conclude) | only these documents prove it | the document opens and is dated; without it, the unit is "unknown" |
| An account on a land registry or planning portal (optional) | some data requires a login | the login works; otherwise ask for the document |

If a required prerequisite is missing, stop before step 1. Say which one, what
it blocks, and the smallest access that would unblock it (read-only first). Do
the parts that do not need it only if they still make sense alone. Never
replace data you could not read with an estimate, and never report "nothing
found" when the lookup failed.

## Configuration

- `property.jurisdictions`: the region designates the code and the documents
  that prove recognition. `detect` (default): derive the region from the
  property's address, state it, and have it confirmed. Outside the configured
  list: flag it before going on.
- `property.investor_file`: which strategies require recognized dwellings;
  unreadable → give the units' status without concluding on the strategy.

If a value is unset or `detect`, say what you used, and give the line that
sets it: `hermes config set skills.config.<key> <value>` (one profile:
`hermes -p <profile> config set …`).

## Procedure

1. **Establish the region and the municipality**: the rule and the documents
   that prove it depend on them.
2. **List the announced units** and where that claim comes from (listing,
   auction conditions (*cahier des charges*), lease, seller). It is a claim,
   not proof.
3. **Look for the documents, by strength of proof**: the **permit** that
   authorizes that number of dwellings, the municipality's **planning
   information** (*renseignements urbanistiques*), the **land registry** entry
   as separate dwellings. Detail:
   [references/proof-of-recognition.md](references/proof-of-recognition.md).
4. **Read each document word for word**: a permit for "two dwellings" does not
   cover a third one fitted in the attic; a renovation permit does not
   necessarily cover a change in the number of units.
5. **Check the date**: a division older than certain dates may benefit from a
   presumption or a limitation period under regional law. That is a legal
   question: consult `property-lawyer`, with the text in force.
6. **Classify each unit**: recognized (document quoted), not recognized
   (document that says so, or a permit covering fewer units), unknown (no
   document).
7. **State the consequence** for the strategies in the investor file, and flag
   it to `property-investment-partner`.

## Decision rules

- Separate meters, doorbells, letterboxes and running leases prove what the
  seller lets, not what the municipality authorized.
- The notary generally does not guarantee the number of dwellings: a "no
  guarantee" clause says so in plain words.
- "Unknown" is an answer: never round it up to "recognized" because the
  building "has always been let that way".
- An up-to-date land registry is not a permit: it records, it does not
  authorize.
- An unrecognized unit makes a strategy that requires recognized dwellings
  impossible, not merely risky.

## Quality gate

The work is done when every announced unit has a status backed by a quoted,
dated document, or is marked unknown. The deliverable is a table (unit,
status, document and date, useful quotation, consequence), then the most
useful missing document and who holds it.
