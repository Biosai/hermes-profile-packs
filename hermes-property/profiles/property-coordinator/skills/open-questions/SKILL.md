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

## When to use

On every message from the investor, before you answer; on every scheduled
reminder; when he says "stop"; when he answers a question asked elsewhere,
even days later.

## Prerequisites

| Needs | Why | Check |
|---|---|---|
| The question register (required) | know what is open, settled or stopped | its latest entry can be read |
| A scheduled task on the host (only to send reminders) | a reminder exists only if a mechanism carries it | it appears in the host's scheduled tasks |
| Access to `owner.channel`, if it is not this conversation | ask where he will read it | this session can write to that channel |

If a required prerequisite is missing, stop before step 1. Say which one, what
it blocks, and the smallest access that would unblock it (read-only first). Do
the parts that do not need it only if they still make sense alone. Never
replace data you could not read with an estimate, and never report "nothing
found" when the lookup failed.

## Configuration

- `property.question_register`: `memory` (default) → this profile's persistent
  memory, re-read before every question; a path → that file, re-read and
  updated on every answer. Unreadable: no question is asked.
- `owner.channel`: where the question reaches him; default, this conversation.
  A channel this session cannot reach: prepare the question and say so,
  without asking it elsewhere.

If a value is unset or `detect`, say what you used, and give the line that
sets it: `hermes config set skills.config.<key> <value>` (one profile:
`hermes -p <profile> config set …`).

## Steps

1. **Read the question register**, not your recollection: open, answered,
   settled, stopped. A settled or stopped question leaves the game for good.
2. **Deliver first** what he asked for, saying what it rests on. The question
   comes after the answer, never before.
3. **Choose a single question**: the one his message has just made concrete.
   He mentions a building to divide → ask about his margin threshold for a
   division, not about short-term letting. If nothing makes a question
   concrete, ask none.
4. **Phrase it so he can answer in one line**: a choice between two or three
   costed options beats an open question. Say what his answer unlocks ("with
   this figure, the ceiling price becomes exact").
5. **Record his answer in the same conversation** (skill
   `investor-data-capture`): the question becomes "answered", with his words,
   the date and the channel.
6. **Reminder**: only if a scheduled task on the host carries it (see
   Prerequisites), through `owner.channel`. A reminder carries one question and
   its reference, so that his answer attaches without ambiguity. No scheduled
   task, no reminder, and no promise of one.
7. **Stop**: "stop on this point" stops that question; "stop reminders" stops
   them all. Record the stop with his words and the date, confirm in one line,
   and never ask it again, anywhere.

## Output

- In the conversation: the answer, then at most one question.
- In the register: each question with its state (open, answered, settled,
  stopped), its source and date, and what it unlocks.

## Pitfalls

- Two questions in one message: he answers the easier one, or neither.
- Asking a settled question again because it "looks open" in a summary made
  from recollection. The register is the authority.
- Lifting a stop yourself because the data would be useful: only the investor
  lifts a stop. Without the data, just say what the result rests on.
- Turning a question into "to do" or "waiting on you" in a summary: that is
  asking it again.
- Letting an expert ask the question: the expert names the missing data; only
  you ask for it.
