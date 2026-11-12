---
name: adversarial-review
description: "Attack a legal answer before sending it"
metadata:
  hermes:
    config:
      - key: property.jurisdictions
        description: "Regions in play, e.g. BE-WAL,BE-BRU,BE-VLA,FR; or detect"
        default: "detect"
---
# Adversarial review

## When to use

Before every legal answer, without exception, including internal
consultations. Your first answer is a draft.

## Prerequisites

| Needs | Why | Check |
|---|---|---|
| The draft, and the texts and documents it cites (required) | reviewing means comparing again | every text and every document opens |
| Access to the official sources (required) | check versions and quotations | the text opens with its consolidation date |

If a required prerequisite is missing, stop before step 1. Say which one, what
it blocks, and the smallest access that would unblock it (read-only first). Do
the parts that do not need it only if they still make sense alone. Never
replace data you could not read with an estimate, and never report "nothing
found" when the lookup failed.

## Configuration

- `property.jurisdictions`: the region to check first. `detect` (default):
  derive the region from the property's address, state it, and have it
  confirmed. A property outside the list: point it out.

If a value is unset or `detect`, say what you used, and give the line that
sets it: `hermes config set skills.config.<key> <value>` (one profile:
`hermes -p <profile> config set …`).

## Steps

1. **Does the text exist, and is it the right one?** The region of the
   property; the date the lease or contract was concluded, which may place it
   under an earlier regime — read the transitional provision; the version date
   of the text you read. Regimes cited from memory have turned out not to
   exist.
2. **Did you read the whole article?** The next paragraph, the exception, the
   aside, the cross-reference. The sentence after a rule often says when it
   does not apply, or lets the parties derogate from it.
3. **Is the rule mandatory or default?** A rule can be mandatory on one point
   and default on another; a default rule gives way to the clause: read the
   document.
4. **What overturns your conclusion?** A derogating clause, an unmet formal
   condition (in writing, registered letter, time limit, mandatory mentions),
   a more recent text, the other party's position. Look for it, and say what
   you found.
5. **Recalculate every time limit**: starting point, method of notification,
   working or calendar days, deadline carried over. Show the calculation.
6. **Compare every quotation again** with the text you opened, word for word.
   A quotation that does not match is copied again, not rephrased.
7. **Re-read every document you cite**: date, amount, clause, page.
8. **What does not survive** is marked **TO VERIFY**, with what would need to
   be read to clear it.

## Output

The corrected answer, and at the bottom one line: what the review changed (or
"review without change"), and the list of points TO VERIFY.

## Pitfalls

- Reviewing to confirm rather than to refute: look for what proves you wrong.
- Treating an unofficial source (consolidation, summary) as authoritative on a
  point that decides a dispute: go back to the official publication.
- Letting a time limit computed in your head go through because "it's a
  month".
- Filling a gap with case law from memory.
