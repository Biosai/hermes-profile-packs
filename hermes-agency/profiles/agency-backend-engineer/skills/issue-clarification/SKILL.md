---
name: issue-clarification
description: "Ask every open question on a work item before coding"
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

Surfaces every product or technical question before a branch exists, and either asks them or states that none remain. Use it unprompted at the start of every work item, and again when a question appears mid-implementation. Nobody should have to ask "is it clear?". A plausible guess that ships is worse than a question that costs two minutes.

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| Read access to the work item: the tracker's CLI or API, the issue file, or the request in this conversation | the scope to clarify | open the item |
| A clone of the repository, with fetch access | answer what the code answers | `git fetch --dry-run` |

If a required prerequisite is missing, stop before step 1. Say which one, what it blocks, and the smallest access that would unblock it (read-only first). Do the parts that do not need it only if they still make sense alone. Never replace data you could not read with an estimate, and never report "nothing found" when the lookup failed.

## Configuration
- `delivery.issue_tracker`: where the item and its thread live, and where you record the answers. `file`: the entry in `delivery.issue_file`. `none`: the request in the conversation; record answers in your report and later in the PR description. `detect`: the URL you were given tells you; say what you used.
- `delivery.default_branch`: the ref you read code at (`origin/<default>`); detect with `git symbolic-ref --short refs/remotes/origin/HEAD`.
- `owner.channel`: where the questions go when no product lead is named.
Current values appear in the `[Skill config]` block when the skill loads; an unset key shows its declared default. Persist a detected value with `hermes config set skills.config.<key> <value>` (per profile: `hermes -p <profile> config set …`); `hermes config migrate` prompts for keys still unset.

## Procedure
1. **Do the homework.** Read the item, its thread, linked items and PRs, acceptance criteria, the team's notes for the area, and the code it touches at a freshly fetched `origin/<default>`. Never ask what these already answer.
2. **List every ambiguity**, in writing.
3. **Resolve what the repository resolves**, noting each conclusion and its source (`path:line @ <sha>`, a decision record).
4. **Keep the questions that need a decision.** Always ask, never guess:
   - behavior the item does not cover: empty, missing, expired, duplicate, concurrent, dependency down, unauthorized;
   - scope: is the client side, a migration, a new endpoint in or out?
   - which defensible design: new field or reuse, sync or async, hard or soft delete, error or silent no-op;
   - anything user-visible: wording, status codes, defaults, limits, units, time zones, rounding;
   - existing production data and compatibility: migrate, backfill, or leave? Breaking change acceptable?
   - acceptance criteria, if there are none;
   - anything touching money, authentication, permissions or a vendor contract, even if you think you know.
5. **Ask in one message** through `owner.channel` (product questions to the product lead when there is one), numbered, each with the options you see and a recommended default, so the answer can be "1A 2B 3 yes".
6. **More than about seven questions** means the item needs rewriting; say that to whoever owns the backlog.
7. **Stop.** "Blocked on N questions before I start." No branch, no "starting on the clear parts".
8. **When answered**, record the answers where `delivery.issue_tracker` says, and carry them into the PR description. Flag any answer that contradicts the team's notes.
9. **If nothing is ambiguous**, say so in one line (scope as you read it, "no open questions, starting now") and start in the same turn.

## Output standard
Either the numbered question block ending `WAITING ON YOU — answers to 1-N`, or the one-line scope statement followed by the first progress line.

## Traps
- Silence is not a statement of clarity. Always say one or the other.
- An unanswered question is never permission to proceed "after a while".
- A question already answered in the thread costs trust. Read the thread first.
- "Any thoughts?" is not a question. Options and a default are.
