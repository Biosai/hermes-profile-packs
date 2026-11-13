---
name: ready-queue
description: "Groom the backlog into a ranked, question-free Ready list"
metadata:
  hermes:
    tags: [workflow]
    config:
      - {key: delivery.issue_tracker, description: "Where work items go: github, gitlab, jira, linear, file, none, or detect", default: "detect"}
      - {key: delivery.issue_file, description: "Markdown file for work items when the tracker is file", default: ""}
      - {key: delivery.board, description: "Where work is claimed: hermes-kanban, tracker, or none", default: "none"}
      - {key: delivery.handoff, description: "How a step reaches another profile without a board: profile-turn, channel, or owner-relay", default: "profile-turn"}
      - {key: owner.channel, description: "Where questions and owner actions reach the owner", default: "this conversation"}
    prerequisites:
      commands: [hermes, gh, glab]
---
# Ready Queue

Grooms an engineering backlog into a ranked Ready list in which every item can be started with zero questions.

## Trigger
The Ready list drops below the floor the team agreed, a planning cycle starts, or the owner asks what is next.

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| Write access to the issue tracker, or to `delivery.issue_file` | rank, fold answers in, promote | edit one item, or the file |
| The `hermes` CLI, when `delivery.board` is `hermes-kanban` | request reviews | `hermes kanban boards list` |

If one is missing, stop before step 1 and say which, what it blocks, and the smallest access that would unblock it (read-only first). Never report "nothing found" when the lookup failed. With `delivery.issue_tracker` set to `none` there is no backlog to groom: say so and stop.

## Configuration
- `delivery.issue_tracker` and `delivery.issue_file`: where Backlog and Ready live. A tracker: a status, column or label. `file`: two sections of the file, Ready ordered top first. `detect`: infer from where items live, and say so.
- `delivery.board`: how a review is requested. `hermes-kanban`: one card per review, assigned to the reviewing profile. `tracker`: a review sub-task or an assignment on the item. `none`: ask each reviewer as `delivery.handoff` says, and record the verdict on the item.
- `owner.channel`: where questions are asked.
- Persist a detected value with `hermes config set skills.config.<key> <value>`.

## Steps
1. Pick candidates: highest priority first, as `prioritization` ranks them, then small startable items that can slot ahead of blocked larger ones.
2. Bring each candidate to the standard of `issue-authoring-standard`, its criteria written with `acceptance-criteria`.
3. Request the readiness reviews, each answered in one comment:
   - buildable as written? From a developer profile when one is installed, otherwise a person who would build it.
   - does it fit, and where does it go? From the software architect profile when it is installed, otherwise the technical owner.
   - when regulated data is touched, a compliance review, from the compliance reviewer profile when it is installed, otherwise the person accountable for compliance.
4. Fold the reviews in: each question raised is answered in the body or becomes a pending question.
5. Check precedent before asking. If the owner already ruled on the same question and nothing superseded it, apply the ruling, cite it, and log it so that the owner keeps a veto.
6. Ask the pending questions where `owner.channel` says: one decision per question, one question at a time, the most blocking first, each with lettered options, their consequences and a recommended default. Keep the next questions written, so that each answer is followed by the next question in the same reply.
7. On each answer, record it on the item and fold it in before asking the next.
8. Promote an item only when its reviews read FITS, or FITS WITH CONDITIONS with the conditions folded in, no question is pending, and its data-change line is filled.
9. Rank Ready by priority, then size and dependencies. Re-rank on every change.
10. Report after each pass: the Ready count, the candidates under review, the pending question, the questions staged behind it, and the top three of Ready with links.

## Decision rules
- As many items as possible in Ready, the top one next to pick. The floor is the alarm level, never the target.
- Size ranks; it is never a status.
- Never apply precedent to data changes, merges, production, unprecedented money or permission rules, or product scope: ask.
- Product questions go to whoever leads the product, technical ones to the technical owner. Split a mixed question.
- One session owns asking the questions and applying the answers. Others write answers down for it and stop: two sessions applying the same answer diverge.
- NEEDS DECISION is not a soft yes: the item stays out of Ready, and so do epics and open decisions.
- An item promoted with a hidden question is the developer's first blocked turn.
- Never write a review in the reviewer's place. A review that failed to run, or has nobody to give it, is reported, never silently retried or skipped.

## Done when
- The Ready list holds at least the agreed floor of items, each ranked, with acceptance criteria and no open question.
- Every item that could not be made ready is listed with what blocks it and who can unblock it.
