---
name: open-questions
description: "Pick the one useful question to ask the investor"
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
# Open questions to the investor

Use when the investor writes (before you answer), a scheduled reminder fires, the investor says "stop", or they answer a question asked elsewhere, even days later.

## Prerequisites

| Needs | Why | Check |
|---|---|---|
| The question register (required) | know what is open, settled or stopped | its latest entry can be read |
| A scheduled task on the host (only to send reminders) | a reminder exists only if a mechanism carries it | it appears in the host's scheduled tasks |
| Access to `owner.channel`, if it is not this conversation | ask where the investor will read it | this session can write to that channel |

If a required prerequisite is missing, stop before step 1. Say which one, what
it blocks, and the smallest access that would unblock it (read-only first). Do
the parts that do not need it only if they still make sense alone. Never
replace data you could not read with an estimate, and never report "nothing
found" when the lookup failed.

## Configuration

- `property.question_register`: `memory` (default) → this profile's persistent
  memory, re-read before every question; a path → that file, re-read and
  updated on every answer. Unreadable: no question is asked.
- `owner.channel`: where the question reaches the investor; default, this
  conversation. A channel this session cannot reach: prepare the question and
  say so, without asking it elsewhere.

If a value is unset or `detect`, say what you used, and give the line that
sets it: `hermes config set skills.config.<key> <value>` (one profile:
`hermes -p <profile> config set …`).

## Procedure

1. **Read the question register**, not your recollection: open, answered,
   settled, stopped. A settled or stopped question leaves the game for good.
2. **Deliver first** what the investor asked for, saying what it rests on. The
   question comes after the answer, never before.
3. **Choose a single question**: the one the investor's message has just made
   concrete. They mention a building to divide → ask about their margin
   threshold for a division, not about short-term letting. If nothing makes a
   question concrete, ask none.
4. **Phrase it for a one-line answer**: a choice between two or three costed
   options beats an open question. Say what the answer unlocks ("with this
   figure, the ceiling price becomes exact").
5. **Record the answer in the same conversation** (skill
   `investor-data-capture`): the question becomes "answered", with the
   investor's words, the date and the channel.
6. **Reminder**: only if a scheduled task on the host carries it (see
   Prerequisites), through `owner.channel`, with one question and its
   reference. No scheduled task, no reminder, and no promise of one.
7. **Stop**: record it with the investor's words and the date, confirm in one
   line, and never ask it again, anywhere. What a stop covers, and the whole
   routine for a message:
   [references/message-routine.md](references/message-routine.md).

## Decision rules

- Ask one question per message: with two, the investor answers the easier one,
  or neither.
- The register is the authority: never ask a settled question again, in
  conversation or as "to do" or "waiting on you" in a summary made from
  recollection.
- Only the investor lifts a stop, even when the data would be useful: just say
  what the result rests on without it.
- Only you ask the investor: an expert names the missing data and what it
  blocks.

## Quality gate

The work is done when the investor has the answer, then at most one question,
and the register holds each question with its state (open, answered, settled,
stopped), its source and date, and what it unlocks.
