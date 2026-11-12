---
name: coordination-board
description: "Sweep the claim board for stale or duplicate work"
metadata:
  hermes:
    config:
      - {key: delivery.board, description: "Where work is claimed: hermes-kanban, tracker, or none", default: "none"}
      - {key: delivery.code_host, description: "Where code is reviewed: github, gitlab, bitbucket, other, or detect", default: "detect"}
      - {key: delivery.issue_tracker, description: "Where work items go: github, gitlab, jira, linear, file, none, or detect", default: "detect"}
      - {key: owner.channel, description: "Where questions and owner actions reach the owner", default: "this conversation"}
    prerequisites:
      commands: [hermes, gh, glab]
---
# Coordination Board

Reads and sweeps the team's claim board, the ledger that stops two sessions doing the same work, and reports stale, malformed, duplicate or finished-but-open claims. Use it before routing substantial work, when someone asks "who is on X?", and on a schedule (twice a day suits an active team). You read and report; you never release, reassign or redo another session's claim.

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| `hermes` CLI, when `delivery.board` is `hermes-kanban` | list and read claims | `hermes kanban boards list` |
| Tracker read access, when `delivery.board` is `tracker` | read assignments and states | list in-progress items |
| Code-host CLI with read access: `gh` (github), `glab` (gitlab) | the real state of linked PRs | `gh auth status` / `glab auth status` |

If a required prerequisite is missing, stop before step 1. Say which one, what it blocks, and the smallest access that would unblock it (read-only first). Do the parts that do not need it only if they still make sense alone. Never replace data you could not read with an estimate, and never report "nothing found" when the lookup failed. With `delivery.board` set to `none` there is no ledger: say so, and suggest a board to the owner if collisions have happened.

## Configuration
- `delivery.board`: `hermes-kanban`: a dedicated board (named `coordination` by convention); claims are cards. `tracker`: a claim is an assignment plus an in-progress state and a comment naming the session. `none`: skip and say so.
- `delivery.code_host`, `delivery.issue_tracker`: where you read the linked PR and item state; detect from the links on the claims.
- `owner.channel`: where the sweep report goes.
Current values appear in the `[Skill config]` block when the skill loads; an unset key shows its declared default. Persist a detected value with `hermes config set skills.config.<key> <value>` (per profile: `hermes -p <profile> config set …`); `hermes config migrate` prompts for keys still unset.

## The ledger's contract
- One claim per work item; title `<repository> <item>`; body starts `session: <session name> — started <UTC time>`.
- On Hermes Kanban the card is parked as blocked from creation (`create ... --initial-status blocked`, or `block <id>` right after). A claim left ready is dispatched to a worker and the work runs twice.
- Progress is a comment; done is completion with the PR and item links; abandoned is a release with a one-line reason.

## Procedure: before routing
1. Search the board for the item (title, item link, PR link, branch).
2. Claimed with recent activity: route nothing; tell the requester which session holds it.
3. Claimed but stale: route nothing; report it to the owner with the claiming session.
4. Unclaimed: route it, and tell the receiving profile to claim it first.

## Procedure: sweep
1. List open claims with only the fields you need: id, title, assignee, last update.
2. Read each claim's last activity, and the linked PR and item state yourself; never trust a title for state.
3. Classify: **Active** (activity within the cadence of that work: leave it), **Stale** (idle for hours, not completed), **Malformed** (no session name: treat as stale), **Done but open** (linked PR merged or item closed), **Duplicate** (two claims for one item: the owner decides which stands).
4. Post one report through `owner.channel` and stop.

## Output standard
```
Coordination sweep — <UTC time> — N open claims
STALE (n): <id> <title> — session <name> — idle <h>h — <link>
MALFORMED (n) / DONE BUT OPEN (n) / DUPLICATE (n): ...
Active: n, not listed.
```
End with `WAITING ON YOU — release or nudge: <list>`, or `NOTHING NEEDED FROM YOU`.

## Traps
- Releasing a stale claim yourself destroys the owning session's context and invites a collision when it wakes.
- "Idle" is relative: a long test campaign may be silent for an hour. Read the last comment first.
- The claim board stops agents colliding; it does not tell humans what is being worked. Planning updates are the working profile's job.
