# Mutation proof: mutations, harness and collector

Companion to the `mutation-proof` workflow.

## What the check asserts (steps 1 to 3)
- Print the intermediate values of the reported scenario, the buggy and the correct branch side by
  side, so the delta is output and not inference. A defect that looks harmless alone (a duplicate
  that inflates a counter) can cross a threshold and change a classification: measure before
  accepting a filed severity.
- Assert the intermediate value a threshold reads, not a verdict string that another threshold can
  also produce.
- Assert the exact value, not its sign or truthiness: a "positive" check survives the deletion of
  the largest term.
- An index, a key lookup, a first-element lookup or a parse called bare makes the run crash under
  mutation instead of failing by name. Wrap it in a helper that returns a boolean, and let the
  check name what is missing.

## One mutation per way the fix can be undone (step 4)
| Mutation | Catches |
|---|---|
| Remove the call from the real path | a correct helper that nothing calls: needs a guard that reads the module source for the call and its order |
| Neuter the helper to an identity | invoked, does nothing |
| Discard the data the helper preserves | works, silently lossy |
| Tighten it to drop valid input | works, over-strict |

## A strict harness (step 5)
- Count the applied mutations and exit non-zero when one did not apply.
- When a mutation is a text substitution, match whitespace loosely and normalize quotes: text
  extracted from documents or rendered pages can carry non-breaking spaces, curly apostrophes and
  soft hyphens. Never loosen digits, dates or identifiers.
- Import the subject's own matcher instead of copying it, mutate through its widest matcher, and
  assert the mutation landed before running the check.

## Aim each mutation at the path the fixture walks
A mutation applied to a branch the scenario never enters stays green and reads as "guard not
covered" while the guard is fine. A mutation that stays green while its neighbors go red is the
sign. Prefer mutating the producer of a fact over the consumer's unreached error branch.

## The denominator (step 7)
Count the candidates with a deliberately permissive matcher and the items the strict checker
processed, print both, and fail on any gap: a checker whose pattern skipped some items still
prints a full pass rate. Cross-check against an independent count, and say which earlier claims
rested on items that were never verified.

## Collector and judge
When a checker is split into collecting facts and judging them, a judge suite fed hand-written
facts leaves the collector untested. Give the collector its own harness:
- run it whole, against fake command shims placed first on `PATH`, over a fixture tree;
- assert that every family of facts the judge reads is present;
- assert that the end-of-run sentinel is the last line, so a truncated run cannot read as clean;
- assert that no secret from the fixture leaks, with a positive control that the secret really is
  in the file read;
- make every section that iterates a collection fail by name when the collection is empty;
- do not accept a fact without its corroborating detail.

## Report format
```
Mutation proof — <test or guard> — head <commit>
M1 removed from the real path: RED — <check name>: <message>
M2 neutered to identity: RED — <check name>: <message>
Applied 4/4 — restored: GREEN <pass>/<total> (candidates <n>, processed <n>)
Severity: confirmed | corrected to <...> (<numbers>)
```
