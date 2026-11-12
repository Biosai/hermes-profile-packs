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
guess past a decision that is not yours. A wrong guess costs more than a question, and a
silent stall costs more than both. For a full proposal with an implementation plan use
`one-three-one-rule`; to record the outcome durably use `decision-log`; for a step only the
owner can perform use the `owner-action-handoff` workflow.

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
1. Check the record first: the brief (including any list of resolved asks it keeps), the
   decision log, the linked work item and its comments, earlier answers. If the owner already
   decided, quote that decision with its date and continue. A deferral ("later", "not a
   blocker") is an answer too: do not re-ask until the owner raises it.
2. Do not ask what you can find out: run the command, read the file, query the system.
3. Reduce the question to ONE decision. Several decisions become several questions, ordered
   by which one unblocks the most work.
4. Context in at most two lines: what is happening and why it needs a choice now. Frame it
   from the owner's objective, in their words, not from the mechanism's internals.
5. Two to four options, each with what happens, what it costs (money, time, risk, what gets
   dropped) and whether it can be undone.
6. Recommend one option, with the reason in one sentence. When data can inform the choice,
   the reason carries the metric, value, denominator, window and source; otherwise it says
   "no data: assumption". "No preference" only when the options really are equivalent.
7. Say what continues while you wait and the safe default if no answer comes: nothing
   irreversible happens on silence.
8. Post it in `owner.channel`, linked to the work it blocks. One question per message; lead
   with it, never bury it in a status update. When the question is about a draft, paste the
   full text inline, not a link and a summary.
9. When the answer arrives: record it verbatim where the question lives, record the decision
   where decisions live (the brief, `decision-log` or the work item) with its date, then act.

## Before listing any ask again
A reminder, a block reason, a card result or a "waiting on you" list repeats asks that may
already be done. Re-asking something the owner already did is the most expensive mistake here.
Before each item, today:
1. Re-fetch its record. A closed owner-action record is done; drop it.
2. Probe the capability instead of quoting a note: call the API with the key, load the page,
   search for the receipt. "Access X is still missing" in a note is a snapshot, not a fact.
3. Compare with what happened in this conversation since the note or card was written:
   sends, posts, payments, merges. Work items copy asks from notes that predate the chat.
4. Fix the stale note in the same pass.

The first time an ask appears in a conversation, send the whole question (the problem in
measured numbers, each option with its effect and cost, the recommendation and its
conditions). After that, a one-line reminder with the record's link is enough. Each item in
a waiting list is already its own recorded owner action, one action per record.

## Output standard
```
Decision needed: <one line>
Context: <two lines max>
A) <option>: <consequence, cost, reversible?>
B) <option>: <consequence, cost, reversible?>
Recommendation: <letter>, because <reason, with the number and its source>.
Blocks: <link>. Meanwhile: <what continues>. Default on no answer: <safe default>.
```

## Traps
- "What do you think?" with no options: the owner does the work the question was for.
- A reminder naming options ("answer A/B/C, I recommend C") the owner never saw in full.
- Silence, a reaction or a relayed "they said ok" treated as approval.
- A later plan quietly re-proposing an option the owner already dropped. Quote the dated
  decision instead.
- Choosing an option because no answer came. Wait, and keep doing other work.

## Quality gate
The owner can answer in one reply without opening anything else, nothing irreversible
depends on an assumed answer, every listed ask was re-checked today, and the answer is
recorded where the next person will look.
