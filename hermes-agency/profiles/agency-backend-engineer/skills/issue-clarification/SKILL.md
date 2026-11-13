---
name: issue-clarification
description: "Ask what a work item leaves open; decide the rest"
metadata:
  hermes:
    config:
      - {key: delivery.issue_tracker, description: "Where work items go: github, gitlab, jira, linear, file, none, or detect", default: "detect"}
      - {key: delivery.issue_file, description: "Markdown file for work items when the tracker is file", default: ""}
      - {key: delivery.default_branch, description: "Default branch name, or detect", default: "detect"}
      - {key: owner.channel, description: "Where questions and owner actions reach the owner", default: "this conversation"}
    prerequisites:
      commands: [git]
---
# Issue Clarification

Use when you pick up a work item, before a branch exists, and again when a question appears during implementation.

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| Read access to the work item and its thread | the scope to clarify | open the item |
| A clone of the repository, with fetch access | answer what the code answers | `git fetch --dry-run` |

If one is missing, stop before step 1: say which, what it blocks, and the smallest access that unblocks it (read-only first). Never estimate data you could not read, and never report "nothing found" when the lookup failed.

## Configuration
- `delivery.issue_tracker`: where the item lives and where answers are recorded. `file`: its entry in `delivery.issue_file`. `none`: the request in the conversation; answers go in your report, then in the pull or merge request description. `detect`: the link you were given tells you; say what you used.
- `delivery.default_branch`: the ref you read code at; detect with `git symbolic-ref --short refs/remotes/origin/HEAD`.
- `owner.channel`: where questions go when the work item names nobody who decides them.

## Procedure
1. Read the item, its thread, linked items and requests, the acceptance criteria, the team's notes for the area, and the code it touches on a freshly fetched default branch.
2. List every ambiguity in writing.
3. Resolve what the work item, the code or a recorded decision answers; note each conclusion with its source.
4. Decide the reversible implementation choices yourself (naming, internal structure, which existing helper, test layout), and state each with its reason in the request description.
5. Keep as questions what changes what is built and nothing above settles:
   - behavior the item does not cover: empty, missing, expired, duplicate, concurrent, dependency down, unauthorized;
   - what a user or caller sees: wording, status codes, defaults, limits, units, time zones, rounding, an error or a silent no-op;
   - a choice that is costly to reverse: a new stored field or reuse of one, hard or soft delete, sync or async;
   - acceptance criteria, when there are none.
6. Ask them in one message through `owner.channel`, numbered, each with the options you see and a recommended default, so the answer can be "1A 2B 3 yes".
7. Stop until answered: no branch, no start on "the clear parts".
8. Record the answers where `delivery.issue_tracker` says and carry them into the request description. Flag an answer that contradicts the team's notes.
9. With nothing to ask, say so in one line (the scope as you read it, no open question) and start in the same turn.

## Decision rules
- Never guess on scope (client side, a migration, a new endpoint: in or out), existing data and compatibility (migrate, backfill or leave), security, money or an external contract: ask, even when you think you know.
- Do not send upward a choice your specialty can make and reverse: decide it, state it, move on.
- Never ask what the thread, the code or a recorded decision already answers.
- Silence is not a statement of clarity: always say that questions are open, or that none are.
- An unanswered question is never permission to proceed after a while.
- A question carries options and a default; "any thoughts?" is not one.
- More than about seven questions means the item needs rewriting: say so to whoever owns the backlog.
- Product questions go to whoever the work item names as deciding them, otherwise to the owner.

## Quality gate
Clarification is complete when either one numbered question block was sent and work waits on its answers, or one line states the scope and that no question is open; and every answer, like every choice you made yourself, is recorded on the work item or in the request description.
