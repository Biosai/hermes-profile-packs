---
name: accountant-question
description: "Draft the accountant question and record the answer"
metadata:
  hermes:
    config:
      - key: property.investor_file
        description: "Where the investor file lives: memory or a path"
        default: "memory"
---
# The question to the investor's accountant

Use when a tax figure stays in options for lack of confirmation, a deed is coming whose regime depends on a qualification, or the investor forwards an answer from their accountant.

## Prerequisites

| Needs | Why | Check |
|---|---|---|
| The decision to settle and its costed scenarios (required) | a closed question | the scenarios exist |
| Write access to the investor file (to record the answer) | the written answer becomes the rule | the line written can be read back |

If a required prerequisite is missing, stop before step 1. Say which one, what
it blocks, and the smallest access that would unblock it (read-only first). Do
the parts that do not need it only if they still make sense alone. Never
replace data you could not read with an estimate, and never report "nothing
found" when the lookup failed.

## Configuration

- `property.investor_file`: where to record the written answer. In `memory`
  (default), hand it to `property-coordinator`; a path → record it yourself if
  you can write there.

If a value is unset or `detect`, say what you used, and give the line that
sets it: `hermes config set skills.config.<key> <value>` (one profile:
`hermes -p <profile> config set …`).

## Procedure

1. **Isolate the decision**: which choice or qualification changes the figure
   (duty regime, inventory or fixed asset, VAT rate, tax rate, individual or
   company).
2. **Write one closed question per decision**: "For the purchase of property X
   by the company, can we meet the conditions of the regime … (text, article,
   version): declaration, guarantee, resale deadline?".
3. **Attach the minimal context**: facts of the deal, amounts as ranges, text
   and version, the costed scenarios the answer will decide between.
4. **Say what each answer changes** for the deal, in one line: the reader will
   know why the question matters.
5. **Hand the draft to the investor**, who sends it to the accountant of their
   choice.
6. **When the written answer arrives**: record it in the same conversation
   (or have `property-coordinator` record it), word for word, with its date,
   author and **scope** — the exact case it covers.
7. **Apply it**: the settled option becomes the rule, for that case only; the
   other cases stay as options.

## Decision rules

- Ask a closed question: an open one ("what do you advise?") gets a general
  answer that settles nothing.
- A written answer becomes the rule only for the case it covers: an answer for
  short-term letting does not apply to long-term letting.
- Do not put the question to the investor yourself: go through
  `property-coordinator`, which owns open questions.
- Do not wait for the written answer to deliver: deliver in options; the
  investor decides in their own time.

## Quality gate

The work is done when the draft question is in the investor's hands and, once
the written answer arrives, it is recorded with its scope. The deliverable is
a draft question, ready for the investor to send, and after the answer: the
investor-file line (written answer quoted, author, date, scope) and the
recalculated figure.
