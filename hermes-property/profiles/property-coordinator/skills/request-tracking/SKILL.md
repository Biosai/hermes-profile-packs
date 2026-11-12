---
name: request-tracking
description: "Track the investor's requests, read from the source"
metadata:
  hermes:
    config:
      - key: property.question_register
        description: "Where the question and request register lives: memory or a path"
        default: "memory"
      - key: owner.channel
        description: "Where questions reach the investor (free text)"
        default: "this conversation"
---
# Request tracking

## When to use

When the investor hands the team a task ("analyze this property", "draft the
letter to the co-ownership manager", "compare these three buildings"); when he
asks where something stands; for a periodic summary, if he asked for one.

## Prerequisites

| Needs | Why | Check |
|---|---|---|
| The register (required) | requests have their own section | the "requests" section can be read |
| Access to the deliverables (required to say "delivered") | a status needs proof | the deliverable cited opens |

If a required prerequisite is missing, stop before step 1. Say which one, what
it blocks, and the smallest access that would unblock it (read-only first). Do
the parts that do not need it only if they still make sense alone. Never
replace data you could not read with an estimate, and never report "nothing
found" when the lookup failed.

## Configuration

- `property.question_register`: requests have their own section in it.
  `memory` (default) → this profile's persistent memory; a path → that file.
- `owner.channel`: where a periodic summary goes, if he asked for one and a
  scheduled task carries it; otherwise the status is given here, when he asks.

If a value is unset or `detect`, say what you used, and give the line that
sets it: `hermes config set skills.config.<key> <value>` (one profile:
`hermes -p <profile> config set …`).

## Steps

1. **When he asks, log it** in the "requests" section of the register: his
   words, the date, what is expected (deliverable, format), the profile that
   owns it, and the done condition.
2. **Split if needed**: a request that involves several experts keeps a single
   line with you, with the sub-tasks and their owners.
3. **To give a status, re-read the source at the moment you write**: does the
   deliverable exist, was it reviewed, drafted, approved by him? Write "done"
   only on proof that it is done.
4. **Classify**: delivered, in progress (with the next action and its owner),
   blocked (with the missing data or document, and who holds it), dropped at
   his request.
5. **A request blocked by a settled question is not blocked**: the answer
   exists, apply it.
6. **Close** a request when he has received the reviewed deliverable; keep the
   trace.

## Output

A short status, one line per request: his request (his words), state, proof
(link, document, delivery date), next action and owner. At the top, what
awaits a decision from him — without a single question he has already
settled.

## Pitfalls

- Composing the status from recollection: you announce "in progress" what was
  delivered long ago, and "waiting on you" what he settled.
- Presenting an unreviewed draft as done, or a draft he has not sent himself
  as sent.
- Leaving a request without an owner: it dies quietly.
- Drowning the status in detail: he wants to know what moves, what is
  blocked, and what is expected of him.
