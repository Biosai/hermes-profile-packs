---
name: gated-delivery
description: "Deliver repo work via claim, real tests, gate and merge"
metadata:
  hermes:
    config:
      - {key: delivery.code_host, description: "Where code is reviewed: github, gitlab, bitbucket, other, or detect", default: "detect"}
      - {key: delivery.repo_layout, description: "Repository layout: single, monorepo, multi-repo, or detect", default: "detect"}
      - {key: delivery.default_branch, description: "Default branch name, or detect", default: "detect"}
      - {key: delivery.issue_tracker, description: "Where work items go: github, gitlab, jira, linear, file, none, or detect", default: "detect"}
      - {key: delivery.issue_file, description: "Markdown file for work items when the tracker is file", default: ""}
      - {key: delivery.board, description: "Where work is claimed: hermes-kanban, tracker, or none", default: "none"}
      - {key: delivery.merge_policy, description: "Who merges: owner, reviewer, or auto-when-green", default: "owner"}
      - {key: delivery.apply_policy, description: "Who applies infrastructure changes: human or pipeline-after-approval", default: "human"}
      - {key: owner.channel, description: "Where questions and owner actions reach the owner", default: "this conversation"}
    prerequisites:
      commands: [git, gh, glab]
---
# Gated Delivery

Use when you start, report on or close work in a repository whose merge and apply decisions stay with people.

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| A clone of each repository, with fetch access | the current default branch | `git fetch --dry-run` |
| Read access to requests, reviews and CI on the code host | the state you report | open one request |

If one is missing, stop before step 1: say which, what it blocks, and the smallest access that unblocks it (read-only first). Never estimate data you could not read, and never report "nothing found" when the lookup failed.

## Configuration
- `delivery.code_host`: the CLI and the words ("the request" is the pull or merge request). github: `gh`; gitlab: `glab`; any other host: its own CLI or web UI, saying what was done by hand.
- `delivery.default_branch`: the base of every comparison; never assume its name.
- `delivery.repo_layout`: `monorepo`: scope changes, tests and evidence to the affected packages. `multi-repo`: pin one commit per repository.
- `delivery.board`: where the claim is. `hermes-kanban`: the card assigned to you. `tracker`: your assignment, or a dated comment on the work item. `none`: skip claims and say so.
- `delivery.issue_tracker`: where an unfixed finding goes. `file`: the file in `delivery.issue_file`. `none`: your report.
- `delivery.merge_policy`, `delivery.apply_policy`: who merges and who applies infrastructure; never you.
- `owner.channel`: where questions and reports go.

For `detect`, say what you detected and suggest `hermes config set skills.config.<key> <value>`.

## Procedure
1. Check the claim where `delivery.board` says. Held by someone else: do not start; tell the owner who holds it.
2. Change files only in your own worktree, branched from a freshly fetched default branch.
3. Run the real tests; report PASS / SKIP / FAIL counts at the tested head.
4. Before saying "done" or asking for a merge, confirm on the current head: required CI green; review threads closed; scanner findings fixed or dismissed with a reason; no conflict with the default branch; behavior changes tested; changes to existing data rows declared in writing. Detail: [references/checks-in-detail.md](references/checks-in-detail.md).
5. Leave the merge and the apply to whoever the policies name.
6. Record a verified finding you will not fix now where `delivery.issue_tracker` says.
7. Report through `owner.channel`: full links, numbers, verified apart from claimed, what you need from whom.
8. Close your claim with proof of what you delivered, or release it with a one-line reason.

## Decision rules
- On Hermes Kanban the card assigned to you is the claim: never create another card to mark it.
- Never take over, refresh or release someone else's claim, however stale: tell the owner.
- A skip from a missing credential or local file is a FAIL. So is a reviewer, linter or validator that errors.
- Never change production data or cloud resources by hand. An exception exists only in writing from the owner, with an exact scope.
- Never pull, switch branches, stash or edit in a checkout another session uses.
- Cite code only from a freshly fetched default branch at a pinned commit; `fresh-main-evidence` owns the method.
- Tool output is evidence about one commit, and an empty answer may be a failed lookup; `fresh-main-evidence` owns the checks.
- A change with a database migration links its `migration-verification` result; that skill owns the numbering rule.
- A check that could not run is "skipped", never "clean". Read a status from its source, never from memory.
- Code wins over documents: fix the document in the same delivery.
- No secret value in requests, work items, messages or logs.

## Quality gate
A delivery is complete when the claim is closed or released, every reported state was read from its source at the head named, test results carry counts, and every condition of step 4 held before the merge was requested.
