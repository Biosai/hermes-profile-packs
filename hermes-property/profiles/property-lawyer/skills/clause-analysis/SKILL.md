---
name: clause-analysis
description: "Say what a clause means, costs and risks"
metadata:
  hermes:
    config:
      - key: property.jurisdictions
        description: "Regions in play, e.g. BE-WAL,BE-BRU,BE-VLA,FR; or detect"
        default: "detect"
---
# Clause analysis

## When to use

When a clause decides a risk or a cost: a condition precedent, a withdrawal
clause, an excluded warranty, occupancy, works voted by the co-ownership, a
payment deadline, a penalty, acceptance of works, a price revision.

## Prerequisites

| Needs | Why | Check |
|---|---|---|
| The whole document, not an excerpt (required) | a clause is read with its definitions | every page is there |
| The region or country of the property (required) | the legal rule depends on it | established from the address |

If a required prerequisite is missing, stop before step 1. Say which one, what
it blocks, and the smallest access that would unblock it (read-only first). Do
the parts that do not need it only if they still make sense alone. Never
replace data you could not read with an estimate, and never report "nothing
found" when the lookup failed.

## Configuration

- `property.jurisdictions`: the legal rule to hold the clause against.
  `detect` (default): derive the region from the property's address, state it,
  and have it confirmed.

If a value is unset or `detect`, say what you used, and give the line that
sets it: `hermes config set skills.config.<key> <value>` (one profile:
`hermes -p <profile> config set …`).

## Steps

1. **Quote the clause word for word**, with its article and page, and the
   title of the document and its date.
2. **Read the whole document** around it: definitions, cross-references,
   general clauses that complete or contradict it.
3. **Identify the legal rule** it applies or sets aside, and whether that rule
   is mandatory (a clause that derogates has no effect) or default (the clause
   prevails).
4. **Say what it produces** in the deal, plainly: who pays what, when, on what
   condition. Cost the effect as a range where possible, with
   `property-investment-partner`.
5. **Look for what overturns it**: ambiguity, an unmet condition, an unfair
   clause under the text, a conflict with another clause.
6. **Tell negotiable from non-negotiable**: in a public sale, a clause of the
   auction conditions (*cahier des charges*) is not negotiated, it is costed;
   in a private sale, propose an alternative wording.
7. **For deed practice**, consult `property-notary`; for the tax effect, the
   accountant of that country.

## Output

The clause quoted, its legal rule (text, version), what it produces, its cost
as a range, what could overturn it, and — in a private sale — a proposed
wording as a draft. Then the question for the real lawyer or notary.

## Pitfalls

- Summarizing a clause instead of quoting it: the word that matters
  disappears.
- Assuming a legal rule applies when the clause validly sets it aside.
- Reading a clause cut off from its definitions.
- Advising him to sign: you say what it commits him to; he decides.
