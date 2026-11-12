---
name: documents-to-request
description: "List the documents to request before signing"
metadata:
  hermes:
    config:
      - key: property.jurisdictions
        description: "Regions in play, e.g. BE-WAL,BE-BRU,BE-VLA,FR; or detect"
        default: "detect"
---
# Documents to request

## When to use

As soon as a property becomes serious: before an offer, a preliminary sale
agreement, exercising an option, a bid.

## Prerequisites

| Needs | Why | Check |
|---|---|---|
| The region, the type of property and the type of sale (required) | the list depends on them | established in writing |
| Access to the obligations in force (required) | the list changes over time | the official source opens with its date |

If a required prerequisite is missing, stop before step 1. Say which one, what
it blocks, and the smallest access that would unblock it (read-only first). Do
the parts that do not need it only if they still make sense alone. Never
replace data you could not read with an estimate, and never report "nothing
found" when the lookup failed.

## Configuration

- `property.jurisdictions`: decides the list (certificates and reports by
  region; mandatory surveys in France). `detect` (default): derive the region
  from the property's address, state it, and have it confirmed.

If a value is unset or `detect`, say what you used, and give the line that
sets it: `hermes config set skills.config.<key> <value>` (one profile:
`hermes -p <profile> config set …`).

## Steps

1. **Establish the region, the type of property and the type of sale**
   (private sale, public sale, off-plan sale). The list depends on them, and
   it changes over time: check the obligations in force on the official
   source.
2. **Technical documents**: energy performance certificate (PEB in Wallonia
   and Brussels, EPC in Flanders), electrical installation inspection,
   asbestos certificate where the region requires it, soil information or
   certificate, post-construction file (*dossier d'intervention ultérieure*),
   heating-oil tank, fire brigade report if there are several dwellings.
3. **Planning documents**: planning information (*renseignements
   urbanistiques*), approved permits and plans, known breaches (with
   `property-architect`).
4. **Legal documents**: the seller's title deed, easements, mortgages and
   seizures, running leases and their registration, pre-emption rights.
5. **Co-ownership**: basic deed, regulations, the co-ownership manager's file
   (skill `co-ownership-file`).
6. **France**: the mandatory property surveys (*diagnostics*), the risk
   statement, co-ownership documents — **TO VERIFY** against the list in
   force.
7. **For each document**: who holds it (seller, notary, municipality,
   co-ownership manager, agency), how long it takes, and what it can change in
   the deal.

## Output

A table: document, mandatory or useful, who holds it, lead time, status
(received with date / requested / missing), what it can change. At the top,
the missing documents that can kill the deal.

## Pitfalls

- A list from memory, or another region's.
- A document "received" but out of date or about another unit.
- Waiting for the deed to read the planning information: it must be read
  before the offer when the strategy depends on it.
- Requesting from the seller yourself: the email is a draft for the investor.
