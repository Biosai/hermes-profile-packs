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

Use when the investor gives a figure (a job's cost, a rent achieved, a price paid), answers a question, settles a trade-off or dictates a rule, at the first exchange to set up the investor file, or when they forward a written answer from their accountant, notary or lawyer.

## Prerequisites

| Needs | Why | Check |
|---|---|---|
| Write access to the investor file (required) | nothing is recorded otherwise | the line just written can be read back |
| The investor's words, or the document (required) | every line carries its source | the message or document can be quoted |

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

## Procedure

1. **Record it in the same conversation**, not "later", where
   `property.investor_file` puts it: what is not written down is lost, and the
   other profiles will never hear it. What the file must establish:
   [references/investor-file.md](references/investor-file.md).
2. **Every line carries its source**: who, when, which channel, the investor's
   words in quotation marks. A figure without a capture date is a potentially
   wrong figure.
3. **Mark the status**: recorded rule, measured figure (actual job, invoice),
   the investor's own estimate, passing remark. A passing remark becomes a
   rule only after the investor confirms it.
4. **If the data answers an open question**, mark the question "answered"
   (skill `open-questions`).
5. **Say what the data changes**: which calculation it makes exact, which
   option it settles. Tell the relevant expert at the next consultation.
6. **Confirm in one line** what was recorded; do not read back the file.

## Decision rules

- Keep a written answer to the case it covers: the accountant's answer on
  short-term letting does not apply to long-term letting.
- Never overwrite an old value without a trace: keep the old value and its
  date.
- Do not record as a rule something said once in passing: a threshold the
  investor mentioned is presented as such and confirmed before it becomes a
  rule.
- The investor's edge is established, not assumed: do not assume they do the
  works because they are in the trade; ask once, when a deal makes it
  concrete. Until the file says so, the works line is an estimate, and the
  experts say so.

## Quality gate

The capture is done when every figure, answer, decision or rule the investor
gave in this conversation is written where `property.investor_file` puts it,
the question it settles is marked answered, and the investor has a one-line
confirmation. The deliverable contains one file line per data point: value,
unit, status, quoted source, date, scope (which type of deal it covers).
