---
name: merge-followups
description: "Do the developer's follow-ups once your change merges"
metadata:
  hermes:
    config:
      - {key: delivery.code_host, description: "Where code is reviewed: github, gitlab, bitbucket, other, or detect", default: "detect"}
      - {key: delivery.repo_layout, description: "Repository layout: single, monorepo, multi-repo, or detect", default: "detect"}
      - {key: delivery.repos, description: "Working copies this profile may read or change (paths or URLs, comma-separated)", default: ""}
      - {key: delivery.issue_tracker, description: "Where work items go: github, gitlab, jira, linear, file, none, or detect", default: "detect"}
      - {key: delivery.issue_file, description: "Markdown file for work items when the tracker is file", default: ""}
      - {key: delivery.board, description: "Where work is claimed: hermes-kanban, tracker, or none", default: "none"}
    prerequisites:
      commands: [git, gh, glab]
---
# Merge Follow-ups

Use when a pull or merge request you own has merged and the developer's part remains: clean up, record the downstream counterpart, update the repository's docs, release the work item.

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| Read access to the code host | confirm the merge, read the merged diff | open the request |
| Push access to the repository | the docs request | `git push --dry-run` on a scratch branch |
| Tracker access, unless `delivery.issue_tracker` is `none` | the counterpart item | open any item |

If one is missing, stop before step 1: say which, what it blocks, and the smallest access that unblocks it (read-only first). Never estimate data you could not read, and never report "nothing found" when the lookup failed.

## Configuration
- `delivery.code_host`: how you confirm the merge. github: `gh pr view <n> --json state,mergeCommit`; gitlab: `glab mr view <n>`; any other host: its CLI or web UI, saying what was read by hand. Detect from `git remote get-url origin`.
- `delivery.repo_layout`, `delivery.repos`: `multi-repo`: run this once every request of the item has merged, across the repositories in `delivery.repos`; the counterpart may belong to another repository. `monorepo`: the counterpart and the docs may live in another package.
- `delivery.issue_tracker`: where the counterpart is recorded. `file`: appended to `delivery.issue_file`. `none`: its full text goes in your report.
- `delivery.board`: how the work item is released. `hermes-kanban`: complete the card assigned to you, with a summary. `tracker`: comment on the item and end your assignment. `none`: skip and say so.

## Procedure
1. Confirm the merge on the code host and note the merge commit.
2. Clean up: stop the item's test runs, take the local stack down, remove scratch files.
3. Record the downstream counterpart. When a consumer can observe the change (an endpoint, a contract, a field, a status code, user-visible behavior), write an item for that consumer with the shipped contract (paths, methods, payloads, status codes, error bodies, authentication, idempotency) and the product answers collected before the build, linked both ways.
4. Update the repository's own docs (flow index, API docs, decision records, migration notes) through a request written from the merged diff.
5. Update your profile memory with what you would need next time.
6. Release the work item once your follow-up requests are open.
7. Report each of steps 2 to 6 as done, or skipped with the reason.

## Decision rules
- A closed request is not a merged one: read the state and the merge commit.
- Do this on every merge you own, with or without the `after-merge` workflow. If a scheduled run may already have done it, check before repeating.
- Match the processes you stop by working directory, never by a command-line pattern that also matches other sessions.
- Start no local end-to-end run after the merge: CI and post-merge runs cover it.
- Docs describe what merged, not what the description intended.
- Nothing observable by a consumer: say "no counterpart, nothing filed". Silence must never mean either.
- When the team files work items through one person or profile, hand that owner the counterpart text.
- Do not wait for the follow-up requests to merge before releasing; an unmerged request of the item itself still holds it.
- The shared knowledge base and closing the work item are not this step: they belong to whoever owns them (the knowledge manager and product manager profiles when they are installed).

## Quality gate
The follow-ups are complete when the report names the merged request and its merge commit, and gives: cleanup (runs stopped, stack down, scratch removed); the counterpart (its link, its text when the tracker is `none`, or "no counterpart, nothing filed"); the docs request link; memory; the work item released; and which follow-up requests wait for review.
