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

A test that passes with and without the fix proves nothing. This workflow proves that a new test or guard bites: undo the fix in every way it can be undone, read the red, confirm it names the guard you meant, restore, and see green. Run it after writing a regression test and before calling a fix verified.

## Trigger
A regression test, assertion or guard was just added and is about to be called verified; a change adds to a mutation or sabotage suite; someone asks "does the test fail without the fix?".

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| A worktree you own, at the head under test | mutations are local edits, restored afterwards | `git status --porcelain` is empty before you start |
| The suite runs locally, with the git-ignored files it needs | read the red and the green yourself | the repository's own test entry point runs and its SKIP count matches the baseline |

If a required prerequisite is missing, stop before step 1. Say which one, what it blocks, and the smallest access that would unblock it. Never report a test as biting when you could not run it: "not checked" is the answer.

## Configuration
- `delivery.repo_layout`: `monorepo`: run the affected packages' suites and their dependents; `detect` from workspace files and say what you found.
- `delivery.default_branch`: the clean reference when a mutation result needs comparing; `detect` with `git symbolic-ref --short refs/remotes/origin/HEAD`.
- Nothing else is a setting: the method holds for any language and framework.
Set values with `hermes config set skills.config.<key> <value>`.

## Steps
1. **Reproduce the reported numbers before trusting the severity.** Run the scenario and print the intermediate values, the buggy and the correct branch side by side, so the delta is output, not inference. A filed "cosmetic" or "latent" is a claim from memory: a duplicate that "only" inflates a counter can land on a threshold and flip a classification. Report a corrected severity, upward or down.
2. **Assert the fact only your change moves.** Assert the intermediate value a threshold reads, not a verdict string that another threshold can also produce; the exact value, not its sign or truthiness (a "positive" check survives deleting the largest term); and feed inputs that leave only the asserted path able to produce the result.
3. **Belt every accessor that can raise**, in the check and in its setup: an index, key or first-element lookup, or a parse called bare makes the run crash under mutation instead of failing by name. Wrap it in a helper that returns a boolean, and let the check name what is missing.
4. **One mutation per way the fix can be undone**, not one per fix:

   | Mutation | Catches |
   |---|---|
   | remove the call from the real path | a correct helper nothing calls: needs a guard reading the module source for the call and its order |
   | neuter the helper to an identity | invoked, does nothing |
   | discard the data the helper preserves | works, silently lossy |
   | tighten it to drop valid input | works, over-strict |

5. **Make the harness strict.** Count applied mutations and exit non-zero when one did not apply: an absent search string changed nothing, and the green that follows is not evidence. Match whitespace loosely and normalise quotes (text from PDFs and rendered pages carries non-breaking spaces, curly apostrophes, soft hyphens), never digits, dates or identifiers. Import the subject's own matcher instead of recopying it, mutate through its widest matcher, and assert the mutation landed before running the check.
6. **Aim each mutation at the path the fixture walks.** A mutation that applies to a branch the scenario never enters stays green and reads as "guard not covered" while the guard is fine. A mutation staying green while its neighbours go red is the tell. Prefer mutating the producer of a fact over the consumer's unreached error branch.
7. **Read the red.** Your check failing by name, with a message naming what is missing: it bites. Your check absent from the failures, or the run aborting: it crashed, go to step 3. Your check failing under a mutation aimed at another guard: it is coupled, go to step 2. An exit status alone never proves a test bites.
8. **Restore, see green, quote this run's total.** Check the denominator: count candidates with a deliberately permissive matcher and the items the strict checker processed, print both, and fail on any gap; `68/68 passed` over 72 items certifies text nobody read. Cross-check against an independent count, and say which earlier claims rested on unverified items.
9. **Run the repository's other suites too**: checks that hold docs and code in agreement fail when a figure changes. When the fix changes published figures, re-run the real collection and republish them under today's date; never hand-edit superseded measurements.

## Collector and judge
When a checker is split into collecting facts and judging them, a judge suite fed hand-written facts leaves the collector untested, and a green badge then certifies a blind probe. Give the collector its own harness: run it whole against fake command shims placed first on `PATH`, over a fixture tree, and assert that every family of facts the judge reads is present, that the end-of-run sentinel is the last line (a truncated run cannot read as clean), and that no secret from the fixture leaks, with a positive control that the secret really is in the file read. Every section that iterates a collection fails by name when it is empty, and a fact without its corroborating detail is not accepted.

## Done when
- Every new test or guard was seen failing, by name, under each undo mutation, and every mutation applied.
- The suite was restored and seen green, with the total and the denominator quoted from that run.
- The reported scenario was reproduced and its severity confirmed or corrected with numbers.

## Output standard
```
Mutation proof — <test or guard> — head <sha>
M1 removed from the real path: RED — <check name>: <message>
M2 neutered to identity: RED — <check name>: <message>
Applied 4/4 — restored: GREEN <pass>/<total> (candidates <n>, processed <n>)
Severity: confirmed | corrected to <...> (<numbers>)
```

## Traps
- One mutation for a fix with four undo paths.
- Verifying a helper only through fixtures: a correct helper the real path never calls passes them all.
- A non-applying mutation printed as an informational line: it is a hole in the proof.
- Never seeing the suite green after the mutations: it may simply be broken.
