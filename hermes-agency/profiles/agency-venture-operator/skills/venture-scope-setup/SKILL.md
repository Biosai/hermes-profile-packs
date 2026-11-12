---
name: venture-scope-setup
description: "Get the venture's scope from the owner and record it"
metadata:
  hermes:
    config:
      - key: venture.brief
        description: "Path or URL of the brief: customer, voice, constraints, autonomy"
        default: ""
      - key: owner.channel
        description: "Where questions and owner actions reach the owner"
        default: "this conversation"
      - key: owner.action_tracker
        description: "Where a waiting owner action is recorded: issue-tracker, file, conversation"
        default: "conversation"
---
# Venture Scope Setup

Use on the first task of a new venture copy, when its Scope section still says "not written
yet", when a task depends on a fact that neither Scope nor the brief states, or when the
venture changed (a pivot, a dropped market, a new constraint) and Scope is stale.

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| The owner, reachable in `owner.channel` | only the owner can describe the venture | a message can be posted there |
| Write access to the brief, when `venture.brief` is set | the approved scope is recorded there | the file or page is writable |

If a required prerequisite is missing, stop before step 1. Say which one, what it blocks, and
the smallest access that would unblock it. Without the owner there is no scope: never fill it
from another venture or from the product category.

## Configuration
- `venture.brief`: read it in step 1 and write the approved scope to it in step 5. Unset:
  propose creating one and give the owner its path to set with
  `hermes config set skills.config.venture.brief <path or URL>`.
- `owner.channel`: where the questions go. `owner.action_tracker`: where the "paste this
  Scope" request is recorded (see `owner-action-handoff` for the meaning of each value).

## Procedure
1. Read Scope and the brief. List every field that is missing or contradicts the other.
2. Ask the owner, a few questions at a time, only for what is missing: what the venture is in
   one sentence and who pays for it; which repositories, work tracker, domains and channels
   belong to it; the binding constraint as the owner sees it; decisions already made, each
   with its date; your autonomy per function (what you do alone, what you prepare).
3. Never fill a gap with a fact from another venture, however similar it looks.
4. Draft Scope as five short bullets; the detail stays in the brief. Propose it as text, not
   as a memory you keep.
5. On approval, write it to the brief with the approval date. Then give the owner the exact
   text to paste into the Scope section of the distribution copy this profile was installed
   from (an update re-reads that copy), recorded per `owner.action_tracker`.
6. Suggest the delivery settings the answers imply (code host, repositories, tracker, merge
   policy) as `hermes config set skills.config.<key> <value>` lines for the owner to run.
7. Re-read the brief after writing and report the link.

## Output standard
```
Venture: <name>
What it is: <one sentence>
Owns: <repositories, work tracker, channels>
Binding constraint: <one sentence, with a primary source if regulatory>
Decisions (dated): <YYYY-MM-DD: decision>; ...
```

## Traps
- Keeping the scope in conversation memory: the next session starts blank again.
- Editing only the installed `SOUL.md`: `hermes profile update` overwrites it from the source
  it was installed from.
- Writing a dropped option back into a later plan. A dated decision is a fence.
