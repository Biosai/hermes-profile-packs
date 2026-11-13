---
name: owner-question-protocol
description: "Ask the owner one decision with options and a pick"
metadata:
  hermes:
    config:
      - key: owner.channel
        description: "Where questions and owner actions reach the owner"
        default: "this conversation"
      - key: project.brief
        description: "Path or URL of the brief: customer, voice, constraints, autonomy"
        default: ""
---
# Owner Question Protocol

Use when the project brief, the decision record and a command cannot settle a question, and a wrong guess would cost real work. The owner is the person who holds the decision: usually the operator, sometimes a budget or account holder they named.

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| A way to reach the owner | the question must arrive where it is read | `owner.channel` names a place you can post to |
| Read access to the project brief, when `project.brief` is set | an earlier decision may already answer it | the brief opens |

If one is missing, stop before step 1 and say which, what it blocks, and the smallest access that would unblock it. Never report "no earlier decision" when the record could not be read.

## Configuration
- `owner.channel`: where the question is posted. Default: this conversation.
- `project.brief`: read in step 1. Unset: say there is no brief on record, and check the decision log and the linked work item instead.
- Set values with `hermes config set skills.config.<key> <value>`.

## Procedure
1. Check the record first: the brief and any list of resolved asks it keeps, the decision log, the linked work item and its comments, earlier answers. If the owner already decided, quote that decision with its date and continue.
2. Find out what you can before asking: run the command, read the file, query the system.
3. Reduce the question to one decision. With several open questions, ask them one at a time, the most blocking first, each after the previous answer.
4. Give the context in at most two lines: what is happening and why it needs a choice now, framed from the owner's objective, in their words.
5. Give two to four options, each with what happens, what it costs (money, time, risk, what gets dropped) and whether it can be undone.
6. Recommend one option, with the reason in one sentence. When data can inform the choice, the reason carries the metric, value, denominator, window and source; otherwise it says "no data: assumption".
7. Say what continues while you wait, and the safe default if no answer comes.
8. Post it where `owner.channel` says, in [the question format](references/question-format.md), linked to the work it blocks, never buried in a status update. A question about a draft carries the full text, not a link and a summary.
9. When the answer arrives, record it verbatim where the question lives and the dated decision where decisions live (the brief, `decision-log` or the work item), then act.
10. Before listing any ask again, in a reminder, a status or a waiting list, [re-check it today](references/re-check-an-ask.md).

## Decision rules
- Never guess past a decision that is not yours: a wrong guess costs more than a question, a silent stall more than both.
- One decision per question, and one question at a time.
- A deferral ("later", "not a blocker") is an answer: do not re-ask until the owner raises it.
- Nothing irreversible happens on silence. Never choose an option because no answer came: wait, and keep doing other work.
- Silence, a reaction or a relayed "they said ok" is not approval.
- Never "what do you think?" without options, and "no preference" only when the options really are equivalent.
- A dated decision is a fence: quote it instead of re-proposing an option the owner dropped.
- A full proposal with an implementation plan belongs to `one-three-one-rule`, and a step only the owner can perform to the `owner-action-handoff` workflow.

## Quality gate
The question is ready when the owner can answer in one reply without opening anything else and nothing irreversible depends on an assumed answer. The work is done when the answer is recorded where the next person will look.
