---
name: bounded-task-delivery
description: "Deliver one bounded change as a draft, proven by a run"
metadata:
  hermes:
    tags: [workflow]
    config:
      - key: delivery.code_host
        description: "Where code is reviewed: github, gitlab, bitbucket, other, or detect"
        default: "detect"
      - key: delivery.repo_layout
        description: "Repository layout: single, monorepo, multi-repo, or detect"
        default: "detect"
      - key: delivery.repos
        description: "Working copies this profile may read or change, comma-separated"
        default: ""
      - key: delivery.default_branch
        description: "Default branch name, or detect"
        default: "detect"
      - key: delivery.merge_policy
        description: "Who merges: owner, reviewer, or auto-when-green"
        default: "owner"
    prerequisites:
      commands: ["git"]
---
# Bounded Task Delivery

Use when the owner or the team chose a work item to implement in the venture's code. Not for
audits: those use `repo-audit-to-issues`.

## Trigger
One bounded change is picked for the venture: a ranked finding, or a task the owner asked for.

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| Push access to a branch on the code host | publish the draft | `git push --dry-run` to a new branch |
| The project's toolchain | rebuild and test from clean | the documented test command runs |
| CI log read access | confirm the new test ran | e.g. `gh auth status`, `glab auth status` |

If a required prerequisite is missing, stop before step 1. Say which one, what it blocks, and
the smallest access that would unblock it. Without push access, a local branch and a patch
for the owner are acceptable only if the owner agrees; never push through another account.

## Configuration
- `delivery.code_host`: decides the CLI (for example `gh` or `glab`) and the words (pull
  request or merge request); `detect` from `git remote get-url origin`.
- `delivery.default_branch`: the base; `detect` with
  `git symbolic-ref --short refs/remotes/origin/HEAD`, and say what you found.
- `delivery.repo_layout`: `monorepo` limits the change, the tests and the CI filter to the
  affected packages; `multi-repo` links the related changes in each description.
- `delivery.merge_policy`: `owner` (default): you never merge; `reviewer`: the reviewer
  merges after approval; `auto-when-green`: keep the draft flag until review is done, since
  automation merges on green. In every case you do not press merge yourself.
- Set values with `hermes config set skills.config.<key> <value>`.

## Steps
1. Restate the task as one outcome with an executable done criterion. Two outcomes are two
   tasks.
2. Start from a fresh fetch of the default branch in an isolated worktree, one branch per
   task. Never write to a protected branch directly, "just a typo" included. To fix a broken
   check, first run the repository's gate on the default branch: green there means an
   unmerged branch broke it, and the fix is a commit on that branch, not a new branch.
3. Write or update the test first and watch it fail for the right reason.
4. Make the smallest change that makes it pass. Unrelated findings go to
   `repo-audit-to-issues`, not into extra commits.
5. Prove it by execution: rebuild from clean, run the relevant suite, read the CI log to
   confirm the new test ran, exercise the real path once.
6. Open the request as a draft: what changed, why, how it was proven, what is not covered,
   how to roll back.
7. Ask a reviewer other than the author (`agency-code-reviewer` or a person). Hand base,
   check and thread problems to `agency-git-steward`.
8. After the merge, re-probe from a fresh clone of the default branch before calling it done.

## Unfinished work
Written code never stays only on a local disk. Commit it and push it as a draft whose
description opens with what fails (the failing suites and why, the passing count), says "do not
merge", names the item that finishes it, lists what is deliberately absent and the decisions
worth challenging now; post the measured CI conclusion as a comment. Split a finished fix from
unfinished work into two requests (check the finished paths out onto the right base). Pushed
branches ahead of the default branch with no request are a missing request or dead weight:
raise them. When your own sequencing was wrong, say so in the reply.

## Done when
- One reviewable change exists for that one task, with the run that proves it and the evidence linked.
- Merging follows `delivery.merge_policy`; you did not merge it.

## Output standard
```
Task: <outcome> - draft <link>
Proof: <command> -> <result>; CI log: <link, number of tests that ran>
Review: <reviewer> - <status>   Not covered: <...>
```

## Traps
- A green check on a job that skipped the new test.
- Scope creep: four fixes on one branch, none revertible alone.
- Calling it done at merge. Done is the merged code observed working.
- `git reset --hard`, `git clean -xdf` and a bare `git checkout .` destroy unpushed work. Use
  `git restore --source=HEAD -- <path>`, `git switch`, or `git stash push -m <why> -- <path>`;
  an approval prompt on a destructive command is a signal to re-read the plan.
