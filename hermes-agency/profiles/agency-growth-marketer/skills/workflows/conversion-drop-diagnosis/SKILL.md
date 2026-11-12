---
name: conversion-drop-diagnosis
description: "Find where a zero or falling conversion is lost"
metadata:
  hermes:
    tags: [workflow]
    config:
      - key: growth.analytics_source
        description: "Traffic and funnel numbers: ga4, plausible, posthog, matomo, other, none"
        default: "none"
      - key: growth.payments_source
        description: "Revenue numbers: stripe, paddle, lemonsqueezy, other, none"
        default: "none"
      - key: delivery.issue_tracker
        description: "Issue tracker: github, gitlab, jira, linear, file, none, or detect"
        default: "detect"
    prerequisites:
      commands: ["python3", "curl"]
---
# Conversion Drop Diagnosis

An answer to "why zero signups?" that is not backed by a fresh, segmented pull is worthless.
The answer is almost always in a segment, and a real defect on the critical path is not
automatically THE constraint. Each step below can end the investigation.

## Trigger
"We have zero signups", "conversions dropped", "the ads bring traffic but nothing happens",
"still zero after the fix?", or "how do we grow X?" (then read `references/growth-asks.md`).

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| Analytics read access, when `growth.analytics_source` is not `none` | every cut below | a one-day report returns rows |
| Payments read access, when `growth.payments_source` is not `none` | whether anyone paid | listing the last payment succeeds |
| The public site and API reachable from here | render and production probes | `curl -sI <site>` answers |
| The owner's standing approval for production probes, before step 6 | the probe creates real rows | recorded in the brief or asked once |

If a required prerequisite is missing, stop before step 1. Say which one, what it blocks, and
the smallest access that would unblock it (read-only first). Without analytics, steps 3, 4
and 6 still make sense alone. Never model around a source you could not read.

## Configuration
- `growth.analytics_source` / `growth.payments_source`: as in `revenue-state-audit`; `none`
  means that half is "not measured". `other`: ask how to read it and say what you used.
- `delivery.issue_tracker`: where findings are filed in step 8, only when the owner agrees.
- Set values with `hermes config set skills.config.<key> <value>`.

## Steps
1. **Widen the window before believing the complaint.** Run `revenue-state-audit` over 10,
   30 and 90 days, and the event's daily series over about 180 days. A "10-day problem" is
   usually permanent and only just noticed: that changes the plan from "what broke" to
   "this never worked". Say so plainly.
2. **Cut by channel first (paid vs unpaid), then device, then country**, each with its own
   rate. Sessions are not per event: pull them in a second report on the same dimensions and
   join in code. Pull duration and pages per session per channel: a bucket at a few seconds
   and about one page never entered the funnel. Compute in code, not by eye, the share of
   sessions in countries with no payment option and the share under about 2 seconds.
3. **Check the visitor can see the page.** `python3 scripts/landing_payload.py <url> --ua
   instagram` (or the UA the paid traffic uses). An empty mount `<div>` body means nothing
   paints until the JavaScript runs; compare the blocking download time with the median
   session. A render defect *may* gate everything: rank it below a channel gap already
   found, fix it on its merits, and prove its effect in step 5.
4. **In-app browsers.** Social ads open links in an embedded webview where OAuth sign-in is
   often refused (`disallowed_useragent`, blocked popups). If most paid traffic is in-app,
   social login is dead for it by construction; look for a webview detector and its event.
5. **Did the last fix work?**
   a. Confirm it is live: re-run the probe on production with the paid UA, and fingerprint the
      live build from a change the fix introduced. Merged is not deployed. An issue closed by
      the merge is reopened with the probe output and a done-when naming the deploy.
   b. Size the test before reading the delta: `python3 scripts/effect_size.py --before S N
      --after S N --baseline R --target R --per-day D`. Push back on any verdict scheduled
      before that sample exists: it returns "flat" by construction. Report "shipped and
      verified" separately from "moved the funnel".
   c. Compare equal windows either side of the release, excluding the release day and days of
      your own testing; test with `scripts/fisher_exact.py`.

   | Result | Verdict |
   |---|---|
   | p >= 0.05, sample >= required | "no detectable effect: this was not the constraint" |
   | p >= 0.05, sample < required | "cannot conclude, need X more days" (give X) |

   Retiring a hypothesis after repeated underpowered nulls is a prioritisation decision, not
   a finding: label it so. When a scheduled verdict moves, write the power number and this
   table into the job's own prompt, then read the stored prompt back from the scheduler: an
   API success or a truncated preview does not prove the guardrails were saved.
6. **Prove the conversion step works before calling it broken**, against production, with
   cleanup: `references/production-probe.md`. Go on to the payment provider (a live checkout
   session that loads). Then measure pricing-page reach by channel: if no paid visitor reaches
   it, price and paywall copy are not the constraint. Test infrastructure changes that landed
   near the drop (CORS with the real origin, redirects, rate limits); a file untouched for
   months cannot explain last week's change.
7. **Name the data you could not get** (ad spend, search console, app store) in one line,
   with what it would change. Never infer paid efficiency from analytics alone.
8. **Report** (below), then offer one tracker item per cause with its numbers; do not file
   unasked.

## Done when
- Each cause is backed by a segmented, dated measurement or a production probe, or labelled
  a hypothesis.
- The fix list is ordered cheapest first, the gating item marked, and the dropped work named.

## Output standard
Measured table first; the awkward number bare ("0 signups on 3,200 mobile sessions in 90
days"); contradict the framing when the data does. "Still zero after the fix?" answers in
order: what is verified shipped; why the metric cannot answer yet (p, sessions per arm); when
the zero started; the constraint now binding; what is dropped.

## Traps
- A metric whose definition depends on the broken thing cannot measure the fix: duration
  spans the first and last event, so a page firing a spurious early event looked "longer"
  while broken. Check which events bound it, or measure server-side.
- A single native-app defect blamed while analytics shows nearly all sessions on the web.
- A 200 does not mean a page exists: single-page-app hosts answer 200 for every path. Use
  `scripts/crawl_probe.py`, which fetches an impossible path as a positive control.
