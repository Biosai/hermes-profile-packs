---
name: sale-agreement-and-option
description: "Read a sale agreement or option before signing"
metadata:
  hermes:
    config:
      - key: property.jurisdictions
        description: "Regions in play, e.g. BE-WAL,BE-BRU,BE-VLA,FR; or detect"
        default: "detect"
---
# Preliminary sale agreement, promise and purchase option

Use when a preliminary contract is about to be signed, a seller or an agency sends a draft, or an option approaches its expiry.

## Prerequisites

| Needs | Why | Check |
|---|---|---|
| The full draft preliminary contract (required) | every clause is quoted | every page and annex opens |
| The property's region (required) | conditions and statements depend on it | established from the address |

If a required prerequisite is missing, stop before step 1. Say which one, what
it blocks, and the smallest access that would unblock it (read-only first). Do
the parts that do not need it only if they still make sense alone. Never
replace data you could not read with an estimate, and never report "nothing
found" when the lookup failed.

## Configuration

- `property.jurisdictions`: regional rules (pre-emption, statements,
  documents); FR → French law, TO VERIFY without a text read. `detect`
  (default): derive the region from the property's address, state it, and have
  it confirmed.

If a value is unset or `detect`, say what you used, and give the line that
sets it: `hermes config set skills.config.<key> <value>` (one profile:
`hermes -p <profile> config set …`).

## Procedure

1. **Identify the document**: preliminary sale agreement (*compromis*, a sale
   complete subject to conditions), unilateral promise, purchase option,
   accepted offer. Its nature decides who is bound to what. What this profile
   reads, in Belgium and in France:
   [references/conveyancing-scope.md](references/conveyancing-scope.md).
2. **Pick out the essential terms**, quoted word for word: parties, property
   (description, land registry, units), price, down payment or deposit with a
   withdrawal right (*arrhes*), deed date, occupancy, charges.
3. **Conditions precedent** (*conditions suspensives*): financing, planning,
   soil, obtaining a permit, no pre-emption. For each: time limit, evidence to
   provide, who can waive it, what happens to the down payment.
4. **Exit clauses**: withdrawal, penalty, termination; amount, conditions.
5. **For an option**: on which units, at what price, duration, option fee
   (credited or not), form and deadline for exercise, whether the option can be
   assigned or exercised in favor of a third party, what happens at expiry.
   The duty regime of the structure is costed with `property-accountant-be`;
   what the deed must contain to open it is your part.
6. **What the deed will have to contain**: statements that condition a duty
   regime, the seller's declarations, annexed documents.
7. **What is missing**: list of documents (skill `documents-to-request`).
8. **The meaning and risk of a disputed clause** → `property-lawyer`.

## Decision rules

- Never let an agency's "standard" agreement be signed with no planning
  condition precedent when the strategy depends on a permit.
- A deposit with a withdrawal right (*arrhes*) is not a down payment (a firm
  sale): do not confuse them.
- Note the date and form of exercise of an option: without them, it expires.
- Never assume an option can be assigned: the clause says so, or it does not.
- That the deed carries the statement that opens a duty regime is your part: a
  missing statement is rarely fixed afterwards.

## Quality gate

The reading is done when every clause that binds or releases the investor is
quoted with its article and its date. The deliverable is a table of the
clauses that matter (quoted, with their article), what binds the investor,
what releases them and by which date, the changes to request (as a draft), and
the question for the notary handling the deed.
