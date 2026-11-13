---
name: external-analysis-challenge
description: "Redo an external analysis and say what holds"
---
# Challenge an external analysis

Use when the investor forwards a study, a yield spreadsheet, a seller's file, an agency valuation or an answer from a general-purpose assistant, and asks "is this right?".

## Prerequisites

| Needs | Why | Check |
|---|---|---|
| The full analysis, with its figures (required) | you redo what you have read | every page and every sheet opens |
| The opinions of the experts it touches | works, costs and comparables redone | their answers are quoted |

If a required prerequisite is missing, stop before step 1. Say which one, what
it blocks, and the smallest access that would unblock it (read-only first). Do
the parts that do not need it only if they still make sense alone. Never
replace data you could not read with an estimate, and never report "nothing
found" when the lookup failed.

## Configuration

No setting of its own: the settings of the skills it draws on (comparables,
works estimate, duties) apply to their parts.

## Procedure

1. **Identify the author and their interest**: a seller, an agency, a broker
   get paid if the deal happens. That is not a flaw; it is a reading
   assumption.
2. **Extract the numeric assumptions**, one per line: price, area, rents,
   occupancy, works, costs, taxation, duration, exit value.
3. **Source each one**: where does the figure come from, as of when? Without a
   source it is marked "unsourced"; if it comes from a general-purpose
   assistant, discard it and redo it.
4. **Redo the calculation** with your own bases: named comparables, the budget
   from `property-works-estimator`, the regimes from `property-accountant-be`.
   Do not patch their spreadsheet: rebuild yours and compare.
5. **Look for what is missing**: exit costs, vacancy, contingency,
   co-ownership, tax, unrecognized units, permit timeline.
6. **Test the safety scenario** on their own figures.
7. **Give a verdict per assumption**: holds, optimistic, wrong, unverifiable.

## Decision rules

- Rebuild, do not patch, a spreadsheet whose structure is wrong.
- Never reuse one of their assumptions for convenience without saying so.
- Objectivity is not hostility: what holds is said too.
- On a document meant for third parties, never align figures with the
  investor's target: objectivity comes first, and the target is quoted as the
  investor's.

## Quality gate

The challenge is done when every numeric assumption has a verdict and the
result was rebuilt on your own bases. The deliverable is a table: assumption,
their value, your value (range, source), verdict; then the result redone in
three scenarios, and the main gap in one sentence. Legal points you spot go to
`property-lawyer`.
