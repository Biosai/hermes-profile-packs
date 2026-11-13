---
name: lease-and-tenant
description: "Handle a lease or tenant question"
metadata:
  hermes:
    config:
      - key: property.jurisdictions
        description: "Regions in play, e.g. BE-WAL,BE-BRU,BE-VLA,FR; or detect"
        default: "detect"
---
# Lease and tenant

Use when a tenant does not pay or disputes a date, an indexation, a deposit or a check-in report; the investor wants to give notice, index the rent or draft a lease; a purchased property is occupied; or a short-term, shared or furnished corporate let needs a framework.

## Prerequisites

| Needs | Why | Check |
|---|---|---|
| The lease itself (required) | dates, duration, clauses are quoted | the full lease opens, signatures included |
| The property's address (required) | the region designates the text | municipality known |
| The documents of the dispute: statement, letters, check-in report | dated facts | every document is dated |

If a required prerequisite is missing, stop before step 1. Say which one, what
it blocks, and the smallest access that would unblock it (read-only first). Do
the parts that do not need it only if they still make sense alone. Never
replace data you could not read with an estimate, and never report "nothing
found" when the lookup failed.

## Configuration

- `property.jurisdictions`: the applicable lease text (Walloon, Flemish,
  Brussels; French if FR). `detect` (default): derive the region from the
  property's address, state it, and have it confirmed.

If a value is unset or `detect`, say what you used, and give the line that
sets it: `hermes config set skills.config.<key> <value>` (one profile:
`hermes -p <profile> config set …`).

## Procedure

1. **The property's region**: it designates the text (Wallonia, Flanders and
   Brussels each have their own residential lease legislation; commercial
   leases follow a separate regime).
2. **Qualify the lease**: main residence or not, duration, shared housing,
   student, furnished, commercial or mixed. The qualification decides the
   regime.
3. **Read the lease**: date concluded, start date, duration, rent,
   indexation, deposit, notice clauses. Quote word for word, with the
   article.
4. **Read the regional text in force** at the lease date and at the date of
   the facts; read the transitional provision if the lease is old.
5. **For a notice**: ground, notice period, form, start of the notice
   period, any compensation and the exact condition that triggers it.
6. **For arrears**: dated statement, formal notice (draft), conciliation,
   justice of the peace (*juge de paix*), what happens to the deposit. Say
   what the investor can do alone and what needs a lawyer or a bailiff
   (*huissier de justice*).
7. **For an occupied purchased property**: what the buyer takes over
   (registered lease or not, certain date), and how the buyer can end it.
8. **Run the adversarial review** (skill `adversarial-review`).

## Decision rules

- Apply the rule of the property's region, in the version in force: never
  another region's, or the one from before the reform.
- Tell the rule from its exception: compensation may be due only if the ground
  for the notice is not carried out.
- No eviction and no keeping of the deposit without a court order: the judge
  authorizes it.
- The letter is a draft: the investor sends it.

## Quality gate

The answer is done when it has gone through the adversarial review. The
deliverable contains the dated facts (lease quoted), the rule (text, article,
version), the time limits computed, the investor's options with their cost and
risk, a draft letter if useful, and the question for the investor's lawyer.
