---
name: real-run-verification
description: "Verify a done claim with real runs and counted results"
metadata:
  hermes:
    config:
      - {key: delivery.code_host, description: "Where code is reviewed: github, gitlab, bitbucket, other, or detect", default: "detect"}
      - {key: delivery.repo_layout, description: "Repository layout: single, monorepo, multi-repo, or detect", default: "detect"}
      - {key: delivery.default_branch, description: "Default branch name, or detect", default: "detect"}
      - {key: delivery.board, description: "Where work is claimed: hermes-kanban, tracker, or none", default: "none"}
      - {key: delivery.issue_tracker, description: "Where work items go: github, gitlab, jira, linear, file, none, or detect", default: "detect"}
    prerequisites:
      commands: [git, gh, glab]
---
# Real-Run Verification

Use when a done claim must be verified, or a test campaign others will rely on must be run, with counts at the current head.

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| A clone with fetch access, and your own worktree | run at the exact head | `git fetch --dry-run` |
| The git-ignored files and services the suite needs | no silent skips | the suite's setup check |
| Read access to the code host | the request head, CI results | open the request |

If one is missing, stop before step 1: say which, what it blocks, and the smallest access that unblocks it (read-only first). Never estimate data you could not read, and never report "nothing found" when the lookup failed. A live-mode run needs the sandbox credentials of the real dependencies: without them it is "not run", never green.

## Configuration
- `delivery.code_host`: how you read the request's head and CI. github: `gh pr view <n> --json headRefOid`; gitlab: `glab mr view <n>`; any other host: its CLI or web UI.
- `delivery.repo_layout`: `monorepo`: run the affected packages' suites and their dependents, naming them. `multi-repo`: pin one commit per repository.
- `delivery.default_branch`: the clean ref for comparison runs.
- `delivery.board`: the claim: the card assigned to you (`hermes-kanban`), your assignment (`tracker`), or nothing (`none`).
- `delivery.issue_tracker`: where a regression found after the merge is recorded; `none`: your report.

## Procedure
1. Check the claim per `delivery.board`; if someone else holds this verification, stop and say who.
2. Pin the request's head commit and the freshly fetched default branch's commit.
3. In your own worktree at that head, copy in the git-ignored files with tight permissions, and use the repository's own test entry point on the toolchain versions CI pins.
4. Send output to a file and compute PASS / SKIP / FAIL from the log. Runner behaviors that fake a green, per stack: [references/stack-examples.md](references/stack-examples.md).
5. Read SKIP before PASS: compare with the baseline for this head and mode; list unexpected skips.
6. Check each acceptance criterion beyond the happy path: empty, missing, duplicate, concurrent, unauthorized, dependency failing.
7. Revert the change locally and confirm the new tests fail by name; for a fix with several ways to be undone, run the `mutation-proof` workflow.
8. Before calling a failure flaky or upstream, rerun it alone and on a clean default branch.
9. Record the baseline: head, mode (mocked or real sandboxes), counts, expected skips with reasons.
10. After the merge, when the release must be confirmed: run the live suite on the new default-branch head and compare what is served or published with a build of the merged tree (same reference).

## Decision rules
- Default to disbelief: a claim without a run you executed at the current head is unverified, and re-reading someone's numbers is not verification.
- A skip from a missing credential is a FAIL; more skips than the baseline means a broken environment.
- A baseline is measured at this head, never remembered.
- A background run you never read back did not happen.
- A CI fix is proven by an observed transition: a new run on the new head, failure then success. Re-running the old run proves nothing.
- A merged change is not a shipped one; a host's silence on default-branch merges proves nothing.
- A post-merge failure is recorded per `delivery.issue_tracker` with counts, failing tests and the owning developer. Fix forward; never revert automatically.

## Quality gate
Verification is complete when the report names the request and both pinned commits; scope, mode and environment files; the command with PASS / SKIP / FAIL against the baseline; each acceptance criterion as met, not met or not verifiable, with the observation; whether the new tests fail without the change; and one verdict with its reason: VERIFIED, NOT VERIFIED or BLOCKED.
