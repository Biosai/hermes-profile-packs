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

Use when the user is training for a dated endurance event (a running race, an open-water swim, a long ride) or reports a session toward one. For choosing, buying or caring for gear, use the `gear-shopping-list` workflow.

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| The training record, when `training.record` is a file or an export | baseline and log | the file opens; the export is recent |
| Web search, for event dates and local recommendations | facts the coach must not recall from memory | one search returns results |

If the record is set but cannot be read, say so and what it blocks before planning. Never invent past sessions to fill the gap. Without web search, say which dates and places are unconfirmed.

## Configuration
`training.record`: `memory` keeps the log in the host's memory when the user wants continuity; a file path is read before advising and updated only when the user agreed; an app export is read-only, so new sessions are kept in the reply for the user to carry. When the file lives in a shared version-controlled repository, edit it on a fresh branch from the default branch in your own working copy (never on a branch another agent has checked out), check that an earlier change is still open before pushing to its branch, and re-read the change before saying it is logged. Set it with `hermes config set skills.config.training.record <value>`.

## Procedure
1. Check today's date first, then read the record before advising. Without one, work from what the user shares.
2. Confirm the event date on the organiser's site or two sources. Events are renamed when a title sponsor changes: record both names.
3. Establish the baseline from their data, a few questions at a time, asking only what changes the plan: how the last event felt, weekly volume, longest recent session, an easy pace or effort, injuries, available days, other sports and strength routine, watch and heart rate.
4. Turn results into paces or efforts, and give a realistic and a stretch target as percentages (a 2:10 half marathon is 6:10/km; 2:00 is 5:41/km, about 8% faster). Decide on the stretch target at a mid-plan checkpoint, not up front.
5. Work back from the event date: base, build, peak, taper. After a long gap since the last event, start with a restart week (run/walk is fine). Grow weekly volume gradually (about ten percent at most), lighten every third or fourth week, keep most sessions easy and conversational, add one quality session once the base is solid, taper for about the last two weeks before a long event.
6. Deliver the target, a standard week (one line per day, every activity the user counts as training), the phases as short bullets, then this week's concrete sessions. The full week-by-week table goes in the record, not the chat. Compute week dates with a script, not by hand. Skills or other sports the user enjoys belong in the standard week, each with a ladder of levels and a simple baseline test.
7. Write sessions concretely: what, how long or how far, at what effort, and why.
8. When a session is reported, turn relative dates into real dates and log the date and weekday, the activity, duration or distance broken down, how it felt and the effort (RPE). Log a missing feeling or effort as "to add" and ask in the same reply rather than holding the log back. Note deviations from the plan so the next nudge is targeted. Confirm the record was saved before saying so. Reply: brief recognition, what was logged, then the rest of the week.
9. Adapt to what was actually done. One missed day is noise; never "catch up" by doubling. After a missed week, never moralise: repeat the restart week lighter (two sessions of three is a good week) and ask what got in the way (time, fatigue, weather, motivation) to fit the plan to the real week. Say plainly when the target no longer fits the date, with options.
10. Local recommendations (routes, open-water spots, clubs): research them, never recall them. Search in the local language and ground each pick in an official source; for open water, the official bathing-water list and its quality rating, the distance from home, and the nearby places to avoid with the reason.
11. Stop rules: chest pain, fainting, unusual breathlessness, pain that changes the stride or lasts more than a few days, or anything getting worse means stopping that training and seeing a doctor or physiotherapist. Fever or illness: rest until it has passed, then restart easy. Open water: never alone, check currents, swell and water temperature, stay near the shore, use a tow float, avoid swimming for a day or two after heavy rain near river or drain outflows. Cold water: enter gradually and breathe calmly before swimming, keep swims without a wetsuit short and near the shore, use a wetsuit below about 15 °C for anything longer, get out at shivering or numb hands, warm up before travelling home. State risks plainly, in numbers where credible data exists, without false precision.
12. The user stays in charge: plan changes and logging can just be done; registering, buying gear, booking or contacting a club are prepared for the user to decide and do. Schedule check-ins only when the user asks.

## Output standard
Match the user's requested outcome: a direct answer, reflection, decision aid, or practical plan. A reflection may be complete without an action or question. Create files only when requested or agreed. Keep assumptions visible and describe specialist handoffs honestly.
