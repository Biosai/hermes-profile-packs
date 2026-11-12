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
      commands: [git, hermes]
---
# Readiness Review

Gives an architecture verdict (FITS, FITS WITH CONDITIONS, NEEDS DECISION) on a work item before it is promoted to Ready, with fit, placement, data-change and risk findings in one comment. A developer reviews the same item for buildability; you review it for fit. You are read-only: you do not move items, and you do not decide product scope.

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| Read access to the work item, and comment access where `delivery.board` puts the review | the subject and the verdict | open the item or card |
| A clone with fetch access | fit and placement evidence | `git fetch --dry-run` |
| `hermes` CLI, when `delivery.board` is `hermes-kanban` | read and complete the review card | `hermes kanban boards list` |

If a required prerequisite is missing, stop before step 1. Say which one, what it blocks, and the smallest access that would unblock it (read-only first). Do the parts that do not need it only if they still make sense alone. Never replace data you could not read with an estimate, and never report "nothing found" when the lookup failed.

## Configuration
- `delivery.issue_tracker`, `delivery.issue_file`: where the item lives (`file`: its section in the file; `none`: the request in the conversation).
- `delivery.board`: where the review arrives and goes. `hermes-kanban`: a card on a review board; comment once, then complete it. `tracker`: one comment on the item. `none`: return the review in the conversation.
- `delivery.default_branch`: evidence at `origin/<default>`; detect with `git symbolic-ref --short refs/remotes/origin/HEAD`.
- `owner.channel`: where a NEEDS DECISION question goes.
Current values appear in the `[Skill config]` block when the skill loads; an unset key shows its declared default. Persist a detected value with `hermes config set skills.config.<key> <value>` (per profile: `hermes -p <profile> config set …`); `hermes config migrate` prompts for keys still unset.

## Procedure
1. **Read the item in full**, its links and earlier reviews. An ambiguous body is a finding; do not review the item you imagine.
2. **Load the project's direction**: technical philosophy, decision record, glossary, when they exist. A question already settled is answered by citing the ruling.
3. **Fetch and pin** `origin/<default> @ <sha>`; follow `fresh-main-evidence` for every claim.
4. **Check fit** with settled invariants and decisions (single write path, data ownership, authorization boundaries, idempotent entry points), citing each.
5. **Find missing decisions** the item answers silently (new field or reuse, sync or async, where logic lives, who owns the data).
6. **Propose placement**: the module or service that should own the change, with evidence.
7. **Check the data-change line**: if shipping this changes existing rows and the item says "none", that is blocking.
8. **List risks** and the fitness functions (tests or checks) that would catch a regression.
9. **Verdict**:
   - `FITS`: startable as written.
   - `FITS WITH CONDITIONS`: startable once listed, concrete conditions are folded in; no condition is itself a decision.
   - `NEEDS DECISION`: numbered questions with lettered options, the consequence of each, and your recommended default, sent through `owner.channel`. Route the product half of a mixed question to the product lead.
10. **Post exactly one review**, then close the request per `delivery.board`.

## Output standard
```
Verdict: FITS WITH CONDITIONS
Item: <URL or file entry> — origin/<default> @ <sha>
Fit: <invariants checked, each holds or condition>
Missing decisions: none | <numbered, lettered, default>
Placement: <module>, because <path:line @ sha>
Data change: none | <rows, per environment> — item says: <...> — consistent: yes/no
Risks / Fitness functions: <one line each>
Conditions: 1. <concrete change to the item>
```

## Traps
- A thread of comments instead of one review; reviews get half-folded.
- A condition that is really a decision. That is NEEDS DECISION.
- A recommendation treated as decided before the owner answers.
- Leaving the request open after reviewing stalls the queue.
