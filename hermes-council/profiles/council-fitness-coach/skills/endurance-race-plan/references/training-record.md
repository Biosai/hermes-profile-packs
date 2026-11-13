# The training record

`training.record` says where it lives.

| Value | Reading | Writing |
|---|---|---|
| `memory` | the host's memory, when the user wants continuity | kept in memory |
| a file path | read before advising | updated only when the user agreed |
| an app export | read before advising | read-only: new sessions stay in the reply for the user to carry |

The record also holds the user's units (distance, pace or speed, temperature), settled once.

## Logging a reported session
1. Turn relative dates ("yesterday", "this morning") into real dates.
2. Log the date and weekday, the activity, the duration or distance broken down, how it felt and the effort (rate of perceived exertion).
3. A missing feeling or effort is logged as "to add", and asked for in the same reply. Do not hold the log back for it.
4. Note deviations from the plan, so that the next nudge is targeted.
5. Confirm the record was saved before saying so.
6. Reply: brief recognition, what was logged, then the rest of the week.

## A file in a shared, version-controlled repository
- Edit it on a fresh branch from the default branch, in your own working copy, never on a branch another agent has checked out.
- Before pushing to the branch of an earlier change, check that the change is still open.
- Re-read the change before saying the session is logged.

## Baseline questions
Ask a few at a time, and only what changes the plan: how the last event felt, weekly volume, the longest recent session, an easy pace or effort, injuries, available days, other sports and strength work, the watch and heart-rate data available.
