---
name: french-accountant-question
description: "Draft the question for a French chartered accountant"
metadata:
  hermes:
    config:
      - key: property.investor_file
        description: "Where the investor file lives: memory or a path"
        default: "memory"
---
# The question to a French chartered accountant

## When to use

Before any French operation where a tax figure is still TO VERIFY; when the
investor asks whom to turn to in France and what to ask.

## Prerequisites

| Needs | Why | Check |
|---|---|---|
| The decisions to settle and their scenarios (required) | closed questions | the scenarios exist |
| The opinion of `property-accountant-be` on the Belgian half | the French accountant will not cover it | its opinion is quoted |

If a required prerequisite is missing, stop before step 1. Say which one, what
it blocks, and the smallest access that would unblock it (read-only first). Do
the parts that do not need it only if they still make sense alone. Never
replace data you could not read with an estimate, and never report "nothing
found" when the lookup failed.

## Configuration

- `property.investor_file`: where the written answer will be recorded — by
  `property-coordinator` in `memory` (default), in the file if it is a path.

If a value is unset or `detect`, say what you used, and give the line that
sets it: `hermes config set skills.config.<key> <value>` (one profile:
`hermes -p <profile> config set …`).

## Steps

1. **Isolate the decisions** that change the figure: buying entity, duty
   regime, VAT regime, permanent establishment, exemption from the annual
   property tax, rental regime.
2. **Write one closed question per decision**, with the target text (CGI
   article, BOFiP series) and the costed scenarios the answer will decide
   between.
3. **Add the Belgian dimension**: ask whether they are used to Belgian
   companies and the Franco-Belgian tax treaty; attach the opinion of
   `property-accountant-be` on the Belgian half.
4. **List the documents to attach**: articles and register extract of the
   company, draft preliminary sale agreement (*compromis*) or unilateral
   promise, description of the property, financing plan.
5. **Hand the draft to the investor**; he sends it.
6. **When the written answer arrives**: have `property-coordinator` record it,
   word for word, with date, author and scope, and recalculate the figure by
   replacing the scenario with the confirmed rule.

## Output

A draft email: minimal context, numbered closed questions with their
reference text, costed scenarios, attachments listed. After the answer: the
investor-file line and the recalculated figure.

## Pitfalls

- A question asking for "an overall opinion": the answer will be general and
  settle nothing.
- Forgetting the Belgian half: the French accountant will not answer it
  unprompted.
- Stretching the answer to an operation other than the one it covers.
- Keeping a French tax figure before the written answer: until it arrives,
  the figure stays in scenarios.
