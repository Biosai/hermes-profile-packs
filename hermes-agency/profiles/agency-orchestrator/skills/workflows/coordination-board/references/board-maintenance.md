# Board maintenance

Companion to the `coordination-board` workflow. The sweep reads and reports; these rules apply
when the owner asks for more.

## An automated cleanup
- It fixes only objectively wrong states: a closed work item in an active column, a card with no
  assignee. It never acts on age.
- It runs dry first: it prints what it would change, and the owner reads that before it changes
  anything.
- Prove it before trusting it: age a card far past any threshold, run the cleanup, and check that
  the card still belongs to its assignee; check that an untouched card stayed untouched.
- Cards do not expire. Automatic expiry silently overrides a profile that is still working, so it
  exists only if the owner chose it. If the owner decides that each profile answers for its own
  cards, remove any expiry mechanism entirely rather than leaving it dormant.

## Changing the board's structure
- On a tracker board, replacing a column or the option list of a field on a populated board can
  blank that field on every card. Place every card again afterwards, and check that none is left
  without a column.

## Report format
```
Board sweep — <UTC time> — N open — scheduled | run by hand
<profile>
  STALE: <id> <title> — idle <h>h — <link> — asked for a status
  BLOCKED WITHOUT A QUESTION / NO OWNER / DONE BUT OPEN / DUPLICATE: ...
Active: n, not listed.
Needed: <from whom, what> | nothing
```
A sweep that nobody scheduled does not run again by itself: say whether this one was scheduled.
