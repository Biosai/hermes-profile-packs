---
name: mutation-proof
description: "Prove a new test fails when its fix is undone"
metadata:
  hermes:
    tags: [workflow]
    config:
      - {key: delivery.repo_layout, description: "Repository layout: single, monorepo, multi-repo, or detect", default: "detect"}
      - {key: delivery.default_branch, description: "Default branch name, or detect", default: "detect"}
    prerequisites:
      commands: [git]
---
# Mutation Proof

## Trigger
A regression test, assertion or guard was just added and is about to be called verified; a change adds to a mutation suite; someone asks whether the test fails without the fix.

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| A worktree you own, at the head under test | mutations are local edits, restored afterwards | `git status --porcelain` is empty before you start |
| The suite runs locally, with the git-ignored files it needs | read the red and the green yourself | the repository's test entry point runs; its SKIP count matches the baseline |

If one is missing, stop before step 1: say which, what it blocks, and the smallest access that unblocks it. Never report a test as biting when you could not run it: the answer is "not checked".

## Configuration
- `delivery.repo_layout`: `monorepo`: run the suites of the affected packages and their dependents. `detect`: from workspace files; say what you found.
- `delivery.default_branch`: the clean reference when a mutation result needs comparing; detect with `git symbolic-ref --short refs/remotes/origin/HEAD`.

The method holds for any language and framework.

## Steps
1. Reproduce the reported scenario and print the intermediate values, the buggy and the correct branch side by side, so the severity is measured. Confirm it or correct it, upward or down.
2. Make the check assert the fact that only the change moves: the intermediate value a threshold reads, not a verdict another threshold can also produce; the exact value, not its sign or truthiness; with inputs that leave only the asserted path able to produce the result.
3. Guard every accessor that can raise, in the check and in its setup (an index, a key or first-element lookup, a parse): wrap it in a helper that returns a boolean, so the check fails by name and says what is missing.
4. List one mutation per way the fix can be undone. The four standard ones, and the rules for a strict harness: [references/mutations.md](references/mutations.md).
5. Apply each mutation and assert it landed before running the check. Count the mutations applied, and fail when one did not apply.
6. Read the red, for each mutation:
   - your check fails by name, with a message naming what is missing: it bites;
   - your check is absent from the failures, or the run aborts: it crashed, go back to step 3;
   - your check fails under a mutation aimed at another guard: it is coupled, go back to step 2.
7. Restore, run the suite, see it green. Quote this run's total and its denominator: the candidates counted with a deliberately permissive matcher, against the items the strict checker processed. Fail on any gap.
8. Run the repository's other suites too: checks that hold docs and code in agreement fail when a figure changes.
9. Report, in the format given in the same reference.

## Decision rules
- A test that passes with and without the fix proves nothing. An exit status alone never proves a test bites.
- One mutation per undo path, not one per fix.
- A mutation that did not apply is a hole in the proof, never an informational line: an absent search string changed nothing.
- A mutation that stays green while its neighbors go red is probably aimed at a branch the fixture never enters: aim at the producer of the fact before concluding the guard is missing.
- A helper verified only through fixtures may be correct and never called: one mutation removes the call from the real path.
- Never skip the final green: after the mutations the suite may simply be broken.
- A severity filed as "cosmetic" or "latent" is a claim until the numbers are printed.
- A pass rate without its denominator certifies items nobody read.
- When a checker is split into a collector and a judge, a judge suite fed hand-written facts leaves the collector untested: give the collector its own harness (same reference).
- When the fix changes published figures, rerun the real collection and publish them under the new date; never hand-edit superseded measurements.

## Done when
- Every new test or guard was seen failing by name under each undo mutation, and every mutation applied.
- The suite was restored and seen green, with the total and the denominator quoted from that run.
- The reported scenario was reproduced, and its severity confirmed or corrected with numbers.
