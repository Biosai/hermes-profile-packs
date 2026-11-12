---
name: auction-conditions
description: "Read the auction conditions of a public sale"
metadata:
  hermes:
    config:
      - key: property.jurisdictions
        description: "Regions in play, e.g. BE-WAL,BE-BRU,BE-VLA,FR; or detect"
        default: "detect"
---
# Auction conditions of a public sale

## When to use

Before any bid, on the notaries' public sale platform (Biddit in Belgium) or
in the room; as soon as the auction conditions (*cahier des charges*) are
available.

## Prerequisites

| Needs | Why | Check |
|---|---|---|
| The full auction conditions and their annexes (required) | the reading is line by line | the dated version from the notary's office opens |
| The property's region (required) | costs and documents depend on it | established from the address |

If a required prerequisite is missing, stop before step 1. Say which one, what
it blocks, and the smallest access that would unblock it (read-only first). Do
the parts that do not need it only if they still make sense alone. Never
replace data you could not read with an estimate, and never report "nothing
found" when the lookup failed.

## Configuration

- `property.jurisdictions`: regional rules and the sale platform. `detect`
  (default): derive the region from the property's address, state it, and have
  it confirmed.

If a value is unset or `detect`, say what you used, and give the line that
sets it: `hermes config set skills.config.<key> <value>` (one profile:
`hermes -p <profile> config set …`).

## Steps

1. **Get the full auction conditions** and their annexes (planning
   information, certificates, co-ownership file, leases). Note their date and
   the notary's office that drew them up.
2. **Auction fees**: scale or percentage set by the conditions, calculation
   base, who pays what. They come on top of the price and follow the bid.
3. **Payment deadlines**: price, costs, late interest, penalties (resale at
   the defaulting buyer's risk, *folle enchère*, or equivalent). Compare them
   with the financing.
4. **Occupancy**: vacant or occupied, enforceable leases, date of possession,
   occupancy compensation. Read a running lease with `property-lawyer`.
5. **Condition of the property and excluded warranties**: hidden defects,
   area, number of dwellings, planning compliance, soil. What is excluded, the
   buyer bears.
6. **Co-ownership**: the clause on works and calls for funds voted before the
   sale. The legal rule is a default rule; the clause in the conditions
   prevails. Read it, do not presume it (skill `co-ownership-file`).
7. **Overbid (*surenchère*), bidding conditions, guarantees to provide**.
8. **Cost** everything the conditions put on the winning bidder and pass it to
   `property-investment-partner` for the ceiling price.

## Output

The clauses that matter, quoted with their article; a table of the costs borne
by the winning bidder (item, base, range); occupancy and its consequences;
missing documents; the question for the notary's office before the sale.

## Pitfalls

- Bidding on a ceiling price computed without the auction fees, which rise
  with the bid.
- Presuming the legal rule on co-ownership charges: the clause in the
  conditions can set it aside.
- Ignoring the payment deadline: late financing costs interest, or the sale.
- Believing a public-sale clause can be negotiated: it is costed.
