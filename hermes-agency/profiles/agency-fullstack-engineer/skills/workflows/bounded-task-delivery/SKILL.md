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
      - key: delivery.issue_tracker
        description: "Where work items go: github, gitlab, jira, linear, file, none, or detect"
        default: "detect"
      - key: delivery.issue_file
        description: "Markdown file for work items when the tracker is file"
        default: ""
      - key: delivery.merge_policy
        description: "Who merges: owner, reviewer, or auto-when-green"
        default: "owner"
    prerequisites:
      commands: ["git"]
---
# Bounded Task Delivery

## Trigger
One bounded change is chosen for you to implement: a work item the owner or the team picked, or a ranked finding. An audit is not this workflow.

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| Push access to a branch on the code host | publish the draft | `git push --dry-run` to a new branch |
| The project's toolchain | rebuild and test from clean | the documented test command runs |
| Read access to CI logs | confirm the new test ran | open the latest run |

If one is missing, stop before step 1: say which, what it blocks, and the smallest access that unblocks it. Without push access, a local branch and a patch for the owner are acceptable only if the owner agrees; never push through another account.

## Configuration
- `delivery.code_host`: the CLI and the words. github: `gh`, pull request; gitlab: `glab`, merge request; any other host: its own CLI or web UI, saying what was done by hand. Detect from `git remote get-url origin`. "The request" below is either.
- `delivery.default_branch`: the base. Detect with `git symbolic-ref --short refs/remotes/origin/HEAD`, and say what you found.
- `delivery.repo_layout`, `delivery.repos`: `monorepo`: limit the change, the tests and the CI filter to the affected packages. `multi-repo`: one request per repository of `delivery.repos` that the change touches, each linking the others.
- `delivery.issue_tracker`: where an unrelated finding is recorded. `file`: appended to `delivery.issue_file`. `none`: your report.
- `delivery.merge_policy`: `owner`: the owner merges. `reviewer`: the reviewer merges after approval. `auto-when-green`: keep the draft flag until the review is done, since automation merges on green. You never merge yourself.

## Steps
1. Run `issue-clarification` on the work item; start once no question is open.
2. Restate the task as one outcome with an executable done criterion.
3. Start from a freshly fetched default branch, in your own worktree, one branch per task.
4. Write or update the test first and watch it fail for the right reason.
5. Make the smallest change that makes it pass.
6. Prove it by execution: rebuild from clean, run the relevant suite, read the CI log to confirm the new test ran, exercise the real path once.
7. Open the request as a draft: what changed, why, how it was proven, what is not covered, how to roll back. `gated-delivery` holds the conditions for calling it done.
8. Ask for a review by someone other than the author: the code reviewer profile when it is installed, otherwise a person. Hand base, check and thread problems to the git steward profile when it is installed; otherwise resolve them yourself.
9. After the merge, run `merge-followups`, then probe the behavior again from a fresh clone of the default branch.
10. Report the outcome with the draft link, the proof (command, result, CI log link, number of tests that ran), the reviewer and the review state, and what is not covered.

## Decision rules
- Two outcomes are two tasks. Four fixes on one branch are four fixes none of which can be reverted alone.
- Never write to a protected branch directly, "just a typo" included.
- To fix a broken check, first run the repository's gate on the default branch: green there means an unmerged branch broke it, and the fix is a commit on that branch, not a new branch.
- An unrelated finding is recorded where `delivery.issue_tracker` says, never added as an extra commit.
- A green check on a job that skipped the new test proves nothing.
- Done is the merged code observed working, not the merge.
- Written code never stays only on a local disk: unfinished work is pushed as a draft marked "do not merge", as [references/unfinished-work.md](references/unfinished-work.md) describes.
- `git reset --hard`, `git clean -xdf` and a bare `git checkout .` destroy unpushed work: use `git restore --source=HEAD -- <path>`, `git switch`, or `git stash push -m <why> -- <path>`. An approval prompt on a destructive command is a signal to read the plan again.

## Done when
- One reviewable request exists for the one task, with the run that proves it and the evidence linked.
- Merging followed `delivery.merge_policy`; you did not merge it.
- After the merge, the behavior was observed working from a fresh clone.
