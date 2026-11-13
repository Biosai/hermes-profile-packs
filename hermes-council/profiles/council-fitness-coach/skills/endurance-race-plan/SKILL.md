---
name: endurance-race-plan
description: "Plan and adapt training back from an endurance event date"
metadata:
  hermes:
    config:
      - key: training.record
        description: "Where the training log lives: memory, a file path, or an app export"
        default: "memory"
---
# Endurance Race Plan

Use when the user is training for a dated endurance event (a running race, an open-water swim, a long ride) or reports a session toward one. Choosing, buying and caring for gear belongs to the `gear-shopping-list` workflow.

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| The training record, when `training.record` is a file or an export | baseline and log | the file opens; the export is recent |
| Web search, for event dates and local recommendations | facts the coach must not recall from memory | one search returns results |

If the record is set but cannot be read, say so, and what it blocks, before planning. Never invent past sessions to fill the gap. Without web search, say which dates and places are unconfirmed.

## Configuration
`training.record` says where the log lives: `memory` (the host's memory, when the user wants continuity), a file path (read before advising, updated only when the user agreed) or an app export (read-only: new sessions stay in the reply for the user to carry). [The training record](references/training-record.md) says what is logged and how a shared file is edited. Set it with `hermes config set skills.config.training.record <value>`.

## Procedure
1. Check today's date, then read the record. Without one, work from what the user shares.
2. Settle the units once. Read them from the user's data (a watch export, earlier sessions), or ask: kilometres or miles, pace or speed, Celsius or Fahrenheit. Note the answer in the record and use it everywhere.
3. Confirm the event date on the organiser's site or from two sources.
4. Establish the baseline from their data, then with the training record reference's baseline questions, a few at a time.
5. Turn results into paces or efforts. Give a realistic and a stretch target, each with the percentage it asks over the current result, and decide on the stretch at a mid-plan checkpoint.
6. Work back from the event date through base, build, peak and taper, as [the plan shape](references/plan-shape.md) says.
7. Deliver the target, a standard week, the phases as short bullets, then this week's sessions: what, how long or how far, at what effort, and why. The week-by-week table goes in the record.
8. When a session is reported, log it as the training record reference says, and confirm it was saved before saying so.
9. Adapt to what was actually done. Say plainly when the target no longer fits the date, with options.
10. Research local recommendations (routes, open-water spots, clubs) in the local language, and ground each in an official source.
11. Apply [the stop and safety rules](references/safety.md) to every plan and reply.

## Decision rules
- The user's units, everywhere: never assume kilometres, a pace format or Celsius.
- One missed day is noise: never "catch up" by doubling. After a missed week, never moralise: repeat the restart week lighter and ask what got in the way.
- Chest pain, fainting, unusual breathlessness, pain that changes the stride or lasts more than a few days, or anything getting worse: stop that training and see a doctor or physiotherapist.
- Nobody swims open water alone.
- Places are researched, never recalled. Risks are stated plainly, without false precision.
- The user stays in charge: plan changes and logging can just be done; registering, buying, booking and contacting a club are prepared for the user to do. Check-ins are scheduled only when the user asks.

## Quality gate
The reply matches what the user asked for: a direct answer, a reflection, a logged session, or a plan with the target, the standard week, the phases and this week's sessions, in the user's units. Assumptions are visible, unconfirmed dates and places are named, a handoff to a doctor or another specialist is described honestly, and files are created only when asked or agreed.
