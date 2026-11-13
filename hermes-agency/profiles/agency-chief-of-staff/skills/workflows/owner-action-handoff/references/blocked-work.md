# Work blocked on the owner

How the work that waits for the owner is marked, and how it resumes. `delivery.board` says where.

## When work you own finishes or blocks
Send one short message where `owner.channel` says. Automatic notifications are often truncated.
- Finished: the outcome and its links.
- Blocked on a decision: the whole question (`owner-question-protocol`).
- Blocked on an owner action: the action and the link to its record.

## When the owner answers
1. Record the answer verbatim on the blocked work.
2. Record the decision where decisions live (`decision-log`, the project brief or the work item).
3. Complete the work with the outcome and the decision.

Complete it; never unblock or restart work that already produced a pull or merge request: restarting duplicates the work. If the answer still needs something only the owner can give, keep the work blocked on that owner action.

## Per `delivery.board`
| Value | Marking it blocked | Completing it after the answer |
|---|---|---|
| `hermes-kanban` | the card assigned to you is blocked, with the question or the owner action as its reason | `hermes kanban comment <id> "<answer>"`, then `hermes kanban complete <id> --result "<outcome: decision>"` |
| `tracker` | the tracker's own blocked or waiting status, with a dated comment | a comment with the answer, then the tracker's done status |
| `none` | nothing to mark: say so, and keep the block in your status | say what was completed, with the answer |

With `hermes-kanban`, a card that is unblocked while its comments link a pull or merge request can stay `ready` without ever being picked up: this is one more reason to complete an answered card instead of unblocking it.

## Reminders
A reminder of a pending owner action goes where the owner expects owner actions, as `owner.channel` says. It never opens a conversation about something else.
