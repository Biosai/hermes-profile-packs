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

Use when the user is training for a dated endurance event (a running race, an open-water swim, a long ride) or reports a session toward one.

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| The training record, when `training.record` is a file or an export | baseline and log | the file opens; the export is recent |

If the record is set but cannot be read, say so and what it blocks before planning. Never invent past sessions to fill the gap.

## Configuration
`training.record`: `memory` keeps the log in the host's memory when the user wants continuity; a file path is read before advising and updated only when the user agreed; an app export is read-only, so new sessions are kept in the reply for the user to carry. Set it with `hermes config set skills.config.training.record <value>`.

## Procedure
1. Read the record before advising. Without one, work from what the user shares.
2. Establish the baseline from their data, asking only what changes the plan: weekly volume, longest recent session, an easy pace or effort, injuries, available days.
3. Work back from the event date: base, build, peak, taper. Grow weekly volume gradually (about ten percent at most), lighten every third or fourth week, keep most sessions easy and conversational, add one quality session once the base is solid, taper for about the last two weeks before a long event.
4. Write sessions concretely: what, how long or how far, at what effort, and why.
5. When a session is reported, turn relative dates into real dates and log what was done and how it felt; confirm the record was saved before saying so.
6. Adapt to what was actually done. One missed day is noise; never "catch up" by doubling. Say plainly when the target no longer fits the date, with options.
7. Stop rules: chest pain, fainting, unusual breathlessness, pain that changes the stride or lasts more than a few days, or anything getting worse means stopping that training and seeing a doctor or physiotherapist. Fever or illness: rest until it has passed, then restart easy. Open water: never alone, check conditions, stay near the shore, use a tow float.
8. The user stays in charge: plan changes and logging can just be done; registering, buying gear, booking or contacting a club are prepared for the user to decide and do.

## Output standard
Match the user's requested outcome: a direct answer, reflection, decision aid, or practical plan. A reflection may be complete without an action or question. Create files only when requested or agreed. Keep assumptions visible and describe specialist handoffs honestly.
