---
name: owner-question-protocol
description: "Ask the owner one decision with options and a pick"
metadata:
  hermes:
    config:
      - key: owner.channel
        description: "Where questions and owner actions reach the owner"
        default: "this conversation"
      - key: venture.brief
        description: "Path or URL of the brief: customer, voice, constraints, autonomy"
        default: ""
---
# Owner Question Protocol

Use when the brief, the decision record and a command cannot settle a question and a wrong
guess would cost real work. The owner is the person who holds the decision: usually the
operator, sometimes a budget or account holder they named. Ask when unsure, always; never
guess past a decision that is not yours. For a full proposal with an implementation plan
use `one-three-one-rule`; to record the outcome durably use `decision-log`.

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| A way to reach the owner | the question must arrive where it is read | `owner.channel` names a place you can post to |
| Read access to the brief, when `venture.brief` is set | earlier decisions may already answer it | the file or page opens |

If a required prerequisite is missing, stop before step 1. Say which one, what it blocks, and
the smallest access that would unblock it. Never report "no earlier decision" when the
record could not be read.

## Configuration
- `owner.channel`: where the question is posted. Default "this conversation": ask here.
- `venture.brief`: read it in step 1. Unset: say there is no brief on record and check the
  decision log and the linked work item instead.
- Set values per profile with `hermes config set skills.config.<key> <value>`;
  `hermes config migrate` asks for unset ones.

## Procedure
1. Check the record first: the brief, the decision log, the linked work item, earlier
   answers. If the owner already decided, quote that decision with its date and continue.
2. Do not ask what you can find out: run the command, read the file, query the system.
3. Reduce the question to ONE decision. Several decisions become several questions, ordered
   by which one unblocks the most work.
4. Context in at most two lines: what is happening and why it needs a choice now.
5. Two to four options, each with what happens, what it costs (money, time, risk, what gets
   dropped) and whether it can be undone.
6. Recommend one option, with the reason in one sentence. "No preference" only when the
   options really are equivalent, and say so.
7. Say what continues while you wait and the safe default if no answer comes: nothing
   irreversible happens on silence.
8. Post it in `owner.channel`, linked to the work it blocks. One question per message; lead
   with it, never bury it in a status update.
9. When the answer arrives: record it verbatim where the question lives, record the decision
   where decisions live (the brief, `decision-log` or the work item) with its date, then act.

## Output standard
```
Decision needed: <one line>
Context: <two lines max>
A) <option>: <consequence, cost, reversible?>
B) <option>: <consequence, cost, reversible?>
Recommendation: <letter>, because <reason>.
Blocks: <link>. Meanwhile: <what continues>. Default on no answer: <safe default>.
```

## Traps
- "What do you think?" with no options: the owner does the work the question was for.
- Silence, a reaction or a relayed "they said ok" treated as approval.
- A later plan quietly re-proposing an option the owner already dropped. Quote the dated
  decision instead.

## Quality gate
The owner can answer in one reply without opening anything else, nothing irreversible
depends on an assumed answer, and the answer is recorded where the next person will look.
