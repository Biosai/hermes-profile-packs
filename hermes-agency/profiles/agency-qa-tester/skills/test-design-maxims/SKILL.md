---
name: test-design-maxims
description: "Check tests against maxims that catch false greens"
metadata:
  hermes:
    prerequisites:
      commands: [git]
---
# Test Design Maxims

Use when writing or reviewing a test, to find the ways it can pass while the behavior is wrong.

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| Read access to the tests and the code under test | review against the maxims | open the files |
| A way to run the tests locally, only to prove a test fails without the change | step 4 | the suite's own setup check |

If one is missing, stop before step 1: say which, what it blocks, and the smallest access that unblocks it (read-only first). Never estimate data you could not read, and never report "nothing found" when the lookup failed.

## Procedure
1. For each new or changed test, name what it claims to prove and the defect that should make it fail.
2. Walk the maxims, family by family; each is stated in full in [references/maxims.md](references/maxims.md):
   - **Fixtures and state (1-4)**: a fixture comes from the product path; it seeds a reachable state; a restore undoes every side effect; a shared table has other writers.
   - **Concurrency (5-7)**: a race test manufactures its race; a parallel test's cleanups outlive it; closing a test server can reset process-wide state.
   - **Faults and fixes (8-9)**: a fault test faults inside the unit; deflaking must not assert less.
   - **What the code must be tested for (10-22)**: every door of an invariant; fields valid alone but nonsense together; served values round-trip; every enumeration of a vocabulary; a refusal names its real cause; a 4xx is not a refusal; a missing relation does not read as "no data"; recovery leaves a trace; a shared flight has no caller; per-call errors need a private collector; a loop needs an independent bound; a fixed budget is a data-size ceiling; a vendor assertion is a dated fact.
3. Where a maxim applies and the test does not satisfy it, fix the test before relying on its result; in a review, write the finding.
4. Prove that the test bites, that it fails when the change is undone, with the `mutation-proof` workflow. That workflow owns the proof and its rules: assert the value the change moves, fail by name, treat an empty collection as a finding, quote the denominator, test the collector apart from the judge.
5. Report.

## Decision rules
- A test that cannot fail is worse than no test: it buys confidence nobody earned.
- The maxims hold for any language, framework or repository layout. Where one needs a team-specific fact (a fixture helper, a cleanup hook), use the repository's convention and name it.
- Removing an assertion, widening a tolerance or retrying until green is not a fix. Find the cause, or quarantine the test visibly, with a recorded work item or a line in your report.
- A finding names the maxim, the test and the concrete way it passes falsely; "weak test" is not a finding.
- The list is not exhaustive: when a new false green teaches a maxim, propose it.

## Quality gate
The check is complete when every new or changed test was read against each family; each unmet maxim is fixed, or reported as `Maxim <n> — <test name> — <how it passes falsely>`; and your own work lists the maxims checked per test file.
