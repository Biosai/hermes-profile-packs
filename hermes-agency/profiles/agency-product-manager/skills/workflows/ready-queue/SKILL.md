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
      - {key: owner.channel, description: "Where questions and owner actions reach the owner", default: "this conversation"}
    prerequisites:
      commands: [hermes, gh, glab]
---
# Ready Queue

Grooms an engineering backlog into a ranked Ready list where every item is startable with zero questions, and runs the stream of question sets that unblocks candidates. As many items as possible in Ready, top one next to pick. A floor (for example five) is the alarm level, never the target.

## Trigger
The ready queue drops below the floor the team agreed, a planning cycle starts, or the owner asks what is next.

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| Write access to the tracker, or to `delivery.issue_file` | rank, fold answers, promote | edit one item or the file |
| A way to request reviews: `hermes` CLI when `delivery.board` is `hermes-kanban` | readiness reviews | `hermes kanban boards list` |

If a required prerequisite is missing, stop before step 1. Say which one, what it blocks, and the smallest access that would unblock it (read-only first). Do the parts that do not need it only if they still make sense alone. Never replace data you could not read with an estimate, and never report "nothing found" when the lookup failed. With `delivery.issue_tracker` set to `none` there is no backlog to groom: say so and stop.

## Configuration
- `delivery.issue_tracker`, `delivery.issue_file`: where Backlog and Ready live. Tracker: a status, column or label. `file`: two sections of the file, Ready ordered top first. `detect`: infer from where items live and say so.
- `delivery.board`: how reviews are requested. `hermes-kanban`: one card per reviewer on a review board (for example `ready-review`). `tracker`: a review sub-task or assignment on the item. `none`: ask the reviewers in the conversation and record their verdicts on the item.
- `owner.channel`: where question sets go.
Current values appear in the `[Skill config]` block when the skill loads; an unset key shows its declared default. Persist a detected value with `hermes config set skills.config.<key> <value>` (per profile: `hermes -p <profile> config set …`); `hermes config migrate` prompts for keys still unset.

## Steps
1. **Pick candidates**: highest priority first, then small startable items that can slot ahead of blocked larger ones. Size ranks; it is never a status.
2. **Request readiness reviews**: a developer (buildable as written?) and the architect (fits, where it goes?), plus compliance when regulated data is touched. Each review is one comment.
3. **Fold reviews in**: each raised question is answered in the body or becomes a pending question.
4. **Check precedent before asking.** If the owner already ruled on the same question and nothing superseded it, apply the ruling, cite it, and log it so the owner keeps a veto. Never from precedent: data changes, merges, production, unprecedented money or permission rules, product scope.
5. **Run the question stream** through `owner.channel`:
   - exactly one set pending at a time, product questions to the product lead and technical ones to the owner; split mixed questions;
   - at most five per set, numbered, lettered options with consequences, a recommended default;
   - a few sets staged and written, so each answer is followed by the next set in the same reply;
   - on each answer: record it on the item, fold it in, post the next set;
   - one session owns posting sets and applying answers; others write answers down for it and stop.
6. **Promote** only when reviews are FITS or FITS WITH CONDITIONS (conditions folded in), no question is pending, and the data-change line is filled.
7. **Rank Ready** by priority, then size and dependencies; re-rank on every change.
8. **Keep epics and open decisions out of Ready.**

## Done when
- The Ready list holds at least the agreed floor of items, each ranked, with acceptance criteria and no open question.
- Every item that could not be made ready is listed with what blocks it and who can unblock it.

## Output standard
After each pass: Ready count, candidates under review, the pending set, staged sets, and the top three of Ready with links. A crashing review worker is reported, never silently retried.

## Traps
- Questions dripped one at a time cost a context switch each. Batch them.
- NEEDS DECISION is not a soft yes; the item stays out of Ready.
- An item promoted with a hidden question is the developer's first blocked turn.
- Two sessions applying the same answer diverge.
