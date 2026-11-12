---
name: planning-office-question
description: "Draft the exact question for the planning office"
metadata:
  hermes:
    config:
      - key: property.jurisdictions
        description: "Regions in play, e.g. BE-WAL,BE-BRU,BE-VLA,FR; or detect"
        default: "detect"
---
# The question to the planning office

## When to use

When a unit stays "unknown", a municipal rule cannot be found or is unclear,
or a division or change of use must be confirmed before an offer.

## Prerequisites

| Needs | Why | Check |
|---|---|---|
| The address and land registry reference (required) | identify the property without ambiguity | the plot can be found on the land registry portal |
| What is already known, documents attached (required) | the question starts from there | permits and regulation cited with their date |

If a required prerequisite is missing, stop before step 1. Say which one, what
it blocks, and the smallest access that would unblock it (read-only first). Do
the parts that do not need it only if they still make sense alone. Never
replace data you could not read with an estimate, and never report "nothing
found" when the lookup failed.

## Configuration

- `property.jurisdictions`: decides the language of the email (Dutch in
  Flanders, working translation attached) and the competent office. `detect`
  (default): derive the region from the property's address, state it, and have
  it confirmed.

If a value is unset or `detect`, say what you used, and give the line that
sets it: `hermes config set skills.config.<key> <value>` (one profile:
`hermes -p <profile> config set …`).

## Steps

1. **Gather the property's identification**: address, land registry
   references, current owner if known, intended operation.
2. **State what is already known**, documents attached: known permits
   (reference, date, scope), planning information (*renseignements
   urbanistiques*) received, regulation read (date).
3. **Ask a closed question, or two at most**, that the municipality can answer
   with yes, no or a reference: "How many dwellings does the permit of …
   authorize?", "Does the municipal division regulation of … apply to a plot
   of …?".
4. **Ask for the document, not an opinion**: a copy of the permit, the
   register extract, the council decision in force.
5. **State the useful deadline** (auction date, end of the option), without
   threat or pressure.
6. **Draft it** in the municipality's language (Dutch in Flanders; working
   translation attached for the investor).
7. **Hand it to the investor**: he, or his architect, sends it. Log the
   question in the file so that the answer can be attached to it.

## Output

A draft email: clear subject, property identification, what is known, the
closed question, the document requested, the useful deadline. Then one line:
what each possible answer changes for the deal.

## Pitfalls

- An open question ("what can be done with this property?") gets a general
  answer that settles nothing.
- Revealing the strategy or the target price: the municipality does not need
  them.
- Sending it yourself: the email is a draft, always.
- Taking an oral answer or an informal opinion for an authorization.
