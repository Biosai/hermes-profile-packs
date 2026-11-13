---
name: ready-to-merge-gate
description: "Decide if a change is ready to merge, with evidence"
metadata:
  hermes:
    config:
      - {key: delivery.code_host, description: "Where code is reviewed: github, gitlab, bitbucket, other, or detect", default: "detect"}
      - {key: delivery.repo_layout, description: "Repository layout: single, monorepo, multi-repo, or detect", default: "detect"}
      - {key: delivery.default_branch, description: "Default branch name, or detect", default: "detect"}
      - {key: delivery.merge_policy, description: "Who merges: owner, reviewer, or auto-when-green", default: "owner"}
    prerequisites:
      commands: [git, gh, glab]
---
# Ready-to-Merge Gate

Use when a pull or merge request is about to be presented as finished, or someone is about to ask for its merge.

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| Read access to the request, its reviews and CI on the code host | threads, findings, checks | open the request |
| A clone with fetch access | conflicts, base | `git fetch --dry-run` |
| Read access to the security-scanning dashboard, when the team uses one | the scanners line | open the project's findings |

If one is missing, stop before step 1: say which, what it blocks, and the smallest access that unblocks it (read-only first). Never estimate data you could not read, and never report "nothing found" when the lookup failed.

## Configuration
- `delivery.code_host`: how CI is read for one exact commit; commands and blind spots per host, and the report format, in [references/reading-ci.md](references/reading-ci.md). Detect from `git remote get-url origin`.
- `delivery.repo_layout`: `monorepo`: required checks and the impacted tests cover every affected package and its dependents. `multi-repo`: an item with several requests is ready only when all are.
- `delivery.default_branch`: `<default>`; detect with `git symbolic-ref --short refs/remotes/origin/HEAD`.
- `delivery.merge_policy`: who receives READY. `owner`: the owner, asked for an explicit go. `reviewer`: the approving reviewer, who merges. `auto-when-green`: auto-merge is turned on only after every line holds.

## Procedure
1. Run `pr-ready` first: it brings the request to merge-ready. The gate then proves each line below on the current head, with its evidence.
2. Fetch; record the request's head commit and that of `origin/<default>`.
3. **Scanners**: findings on changed files are fixed or dismissed with a written reason, on the dashboard and in the request's comments.
4. **Threads**: no review thread is open, bot and outdated threads included.
5. **Tests**: the author's impacted selection ran with PASS / SKIP / FAIL counts at this head, and required CI is green at this head. Name what each job that ran executes.
6. **Verification**: an independent VERIFIED verdict against the acceptance criteria (the QA tester profile when it is installed, otherwise a person other than the author), at this head or with a later diff that cannot change the result.
7. **Conflicts**: `git merge-tree --write-tree origin/<default> <branch>` prints no CONFLICT.
8. **Coverage**: tests that exercise the new behavior raise it.
9. **Data change**: declared as "none", or as the rows per environment.
10. **Migration**: a change that adds one links its `migration-verification` result for this head.
11. **Base**: `git rev-list --count <head>..origin/<default>` is zero when you report.
12. Send READY TO MERGE to whoever `delivery.merge_policy` names, or NOT READY with the failing lines back to the author.

## Decision rules
- One failing line means the work is in progress. A line you could not check is NOT CHECKED, and the verdict is NOT READY.
- A skip from a missing credential is a FAIL. No conclusion yet is pending. Zero CI runs at this head is "nothing ran", not green.
- Never accept a hard-coded PASS total: demand counts measured at this head.
- A conflicting branch whose commits are already on the default branch under other hashes (a rebase skips every commit; the diff is nearly all deletions) is a stale snapshot: recommend closing, never "rebase and merge".
- A data change is declared before merge and restated after it as an actionable note. Counts scope it; only the owner authorizes applying it.
- After a rebase, any CI gate, template or definition of done that came with the new base must be met.
- Across many open requests, run `open-pr-readiness-sweep` instead.

## Quality gate
The gate is done when the report names the request, both commits and the time, gives each line as PASS, FAIL or NOT CHECKED with its evidence, ends with one verdict, and has reached whoever must act on it.
