---
name: readiness-review
description: "Give an architecture verdict on a work item before Ready"
metadata:
  hermes:
    config:
      - {key: delivery.issue_tracker, description: "Where work items go: github, gitlab, jira, linear, file, none, or detect", default: "detect"}
      - {key: delivery.issue_file, description: "Markdown file for work items when the tracker is file", default: ""}
      - {key: delivery.board, description: "Where work is claimed: hermes-kanban, tracker, or none", default: "none"}
      - {key: delivery.default_branch, description: "Default branch name, or detect", default: "detect"}
      - {key: owner.channel, description: "Where questions and owner actions reach the owner", default: "this conversation"}
    prerequisites:
      commands: [git]
---
# Readiness Review

Use when a work item needs an architecture verdict before it is promoted to ready: whether it fits the settled design, where it belongs, and what it decides silently.

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| Read access to the work item, and comment access where `delivery.board` puts the review | the subject and the verdict | open the item or card |
| A clone with fetch access | fit and placement evidence | `git fetch --dry-run` |

If one is missing, stop before step 1: say which, what it blocks, and the smallest access that unblocks it (read-only first). Never estimate data you could not read, and never report "nothing found" when the lookup failed.

## Configuration
- `delivery.issue_tracker`: where the item lives. `file`: its entry in `delivery.issue_file`. `none`: the request in the conversation.
- `delivery.board`: where the review arrives and goes. `hermes-kanban`: the card assigned to you; comment once, then complete it. `tracker`: one comment on the item. `none`: the review is returned in the conversation.
- `delivery.default_branch`: the ref evidence is read at; detect with `git symbolic-ref --short refs/remotes/origin/HEAD`.
- `owner.channel`: where a NEEDS DECISION question goes.

## Procedure
1. Read the item in full, with its links and earlier reviews.
2. Load the project's direction where it exists: technical principles, decision records, glossary.
3. Fetch and pin the default branch; follow `fresh-main-evidence` for every claim about the code.
4. Check fit with settled invariants and decisions (single write path, data ownership, authorization boundaries, idempotent entry points), citing each.
5. Find the decisions the item makes silently: a new field or reuse, sync or async, where logic lives, who owns the data.
6. Propose placement: the module or service that should own the change, with evidence.
7. Check the data-change line: does shipping this change existing rows, and does the item say so?
8. List the risks, and the fitness functions (tests or checks) that would catch a regression.
9. Give one verdict:
   - `FITS`: startable as written.
   - `FITS WITH CONDITIONS`: startable once the listed, concrete conditions are folded in.
   - `NEEDS DECISION`: numbered questions with lettered options, the consequence of each and your recommended default, sent through `owner.channel`.
10. Post exactly one review, then close the review request per `delivery.board`.

## Decision rules
- You review fit; buildability is the implementing engineer's review. You are read-only: you do not move items and you do not decide product scope.
- An ambiguous item body is a finding: do not review the item you imagine.
- A question the decision record already settles is answered by citing the ruling.
- An item that changes existing rows and says "none" is blocking.
- No condition is itself a decision: a condition that needs a choice makes the verdict NEEDS DECISION.
- A recommendation is not decided until the owner answers.
- The product half of a mixed question goes to whoever decides product scope: the product manager profile when it is installed, otherwise the owner.
- One review, not a thread of comments: a thread gets half-folded into the item.
- A review request left open after the review stalls the queue.

## Quality gate
The review is complete when one comment carries the verdict; the item and the pinned commit; each invariant checked, with its evidence; the missing decisions, or none; the placement with `path:line @ <commit>`; the data change compared with what the item says; each risk with its fitness function; and the concrete conditions; and the review request is closed.
