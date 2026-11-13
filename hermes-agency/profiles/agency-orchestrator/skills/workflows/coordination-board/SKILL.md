---
name: coordination-board
description: "Sweep the board for stale, duplicate or ownerless work"
metadata:
  hermes:
    tags: [workflow]
    config:
      - {key: delivery.board, description: "Where work is claimed: hermes-kanban, tracker, or none", default: "none"}
      - {key: delivery.code_host, description: "Where code is reviewed: github, gitlab, bitbucket, other, or detect", default: "detect"}
      - {key: delivery.issue_tracker, description: "Where work items go: github, gitlab, jira, linear, file, none, or detect", default: "detect"}
      - {key: owner.channel, description: "Where questions and owner actions reach the owner", default: "this conversation"}
    prerequisites:
      commands: [hermes, gh, glab]
---
# Coordination Board

## Trigger
Before you start or route a work item; when someone asks who is working on what; and on the schedule the owner set.

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| The `kanban` toolset, when `delivery.board` is `hermes-kanban` | list and read cards | `kanban_list` answers |
| Tracker read access, when `delivery.board` is `tracker` | assignments, states, comments | list the items in progress |
| Read access to the code host | the real state of linked pull or merge requests | open one request |

If one is missing, stop before step 1: say which, what it blocks, and the smallest access that unblocks it (read-only first). Never report "nothing found" when the lookup failed. With `delivery.board` set to `none` there is no board to sweep: say so and stop.

## Configuration
- `delivery.board`: what is swept. `hermes-kanban`: the cards of the workflows you coordinate, where the card assigned to a profile is its claim. `tracker`: the work items, where the claim is the assignment or a dated comment. `none`: nothing.
- `delivery.code_host`, `delivery.issue_tracker`: where you read the state of each linked request and work item (github: `gh`; gitlab: `glab`; any other host: its own CLI or web UI). Detect from the links on the cards.
- `owner.channel`: where questions and the report go.

## Steps
1. List the open cards or items with only the fields needed: id, title, assignee, status, last update.
2. For each, read the last activity and the state of the linked request and work item yourself.
3. Classify each from those facts:
   - **active**: running, with recent activity;
   - **stale**: running, silent for longer than that kind of work explains;
   - **blocked without a question**: nothing on it says what is awaited, or from whom;
   - **no owner**: no assignee, or an assignee that is not an installed profile;
   - **done but open**: the linked request is merged, or the work item closed;
   - **duplicate**: two cards or items for the same work.
4. Look for the duplicates titles hide: compare the files each open request changes with those of other open and recently merged requests.
5. Compare the board with the tracker: a work item accepted for delivery with no card and no assignee is work with no owner.
6. Act within your authority:
   - stale: ask the assignee for a status, in a comment on the card or item;
   - blocked without a question: on a step you coordinate, ask the missing question (`escalation-routing`) and write it on the card; otherwise ask the assignee to state it;
   - no owner: choose the profile with `profile-routing` and assign it;
   - done but open: complete a human step of yours once you have verified it happened; ask any other assignee to close its card with its proof;
   - duplicate: when one has not started and you created it, close it with a link to the other; otherwise the owner decides which stands.
7. Report through `owner.channel`, grouped by profile: each entry that is not active, with its link, what you did and what you need from whom; the count of active work; and whether the sweep was scheduled or run by hand.

## Decision rules
- The board has one use: the card assigned to a profile is its claim. Never create a card to mark, park or reserve work.
- Never run another profile's step, take a running card from its assignee, or complete a card on its behalf. A stalled card is reported, never taken away.
- State comes from facts (the linked request, its merge state, the item's state), never from a title.
- "Stale" is relative: a long test campaign may be silent for an hour. Read the last comment first.
- Cards do not expire. Automatic expiry silently overrides a working profile: it exists only if the owner chose it.
- A cleanup the owner asked to automate, or a change to the board's columns, follows [references/board-maintenance.md](references/board-maintenance.md).
- The board stops profiles colliding; it does not tell people what is being worked on. Planning updates stay with the working profile.

## Done when
- Every open card or item was classified from facts read in this run.
- Each one that is not active has an action within your authority, or is in the report with who must act.
- No card was created to mark a claim, and no running work was taken from its assignee.
