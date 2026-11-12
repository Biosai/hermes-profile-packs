---
name: investor-data-capture
description: "Record the investor's figures, answers and rules"
metadata:
  hermes:
    config:
      - key: property.investor_file
        description: "Where the investor file lives: memory or a path"
        default: "memory"
      - key: property.question_register
        description: "Where the question and request register lives: memory or a path"
        default: "memory"
---
# Investor data capture

## When to use

As soon as he gives a figure (a job's cost, a rent achieved, a price paid),
answers a question, settles a trade-off or dictates a rule; at the first
exchange, to set up his investor file; when he forwards a written answer from
his accountant, notary or lawyer.

## Prerequisites

| Needs | Why | Check |
|---|---|---|
| Write access to the investor file (required) | nothing is recorded otherwise | the line just written can be read back |
| His words, or the document (required) | every line carries its source | the message or document can be quoted |

If a required prerequisite is missing, stop before step 1. Say which one, what
it blocks, and the smallest access that would unblock it (read-only first). Do
the parts that do not need it only if they still make sense alone. Never
replace data you could not read with an estimate, and never report "nothing
found" when the lookup failed.

## Configuration

- `property.investor_file`: `memory` (default) → this profile's persistent
  memory; the experts cannot see it, so pass them the useful lines. A path →
  that file, which every profile can read.
- `property.question_register`: where to mark as "answered" the question the
  data settles; same values.

If a value is unset or `detect`, say what you used, and give the line that
sets it: `hermes config set skills.config.<key> <value>` (one profile:
`hermes -p <profile> config set …`).

## What the investor file must establish

- His company (legal form, declared activity), his role, countries, regions.
- **Whether he does the works himself** or through his own company, which
  trades, and at what cost price (materials, labor). Until this is
  established, the works line is a contractor's estimate.
- The strategies he accepts and refuses, possibly by area.
- His thresholds: minimum margin per type of deal, minimum yield on a kept
  unit, budget, acceptable holding period.
- His scenario parameters (resale discount, works overrun, duration) and his
  price rules (entry discount, resale premium).
- The registration-duty regime he wants applied by default; how he wants
  corporate tax shown (per deal or at year end).
- His figure target, quoted as his target.
- His advisers' written answers, each limited to the case it covers.

## Steps

1. **Record it in the same conversation**, not "later", where
   `property.investor_file` puts it: what is not written down is lost, and the
   other profiles will never hear it.
2. **Every line carries its source**: who, when, which channel, his words in
   quotation marks. A figure without a capture date is a potentially wrong
   figure.
3. **Mark the status**: recorded rule, measured figure (actual job, invoice),
   his own estimate, passing remark. A passing remark becomes a rule only after
   he confirms it.
4. **If the data answers an open question**, mark the question "answered"
   (skill `open-questions`).
5. **Say what the data changes**: which calculation it makes exact, which
   option it settles. Tell the relevant expert at the next consultation.
6. **Confirm in one line** what was recorded; do not read back the file.

## Output

One file line per data point: value, unit, status, quoted source, date, scope
(which type of deal it covers).

## Pitfalls

- Generalizing a written answer: his accountant's answer on short-term
  letting does not apply to long-term letting.
- Overwriting an old value without a trace: keep the old value and its date.
- Recording as a rule something he said once in passing.
- Assuming he does the works because he is in the trade: ask him, once, when
  a deal makes it concrete.
