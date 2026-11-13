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

Finds where a zero or falling conversion is lost, from fresh, segmented measurements. Each step can end the investigation.

## Trigger
"We have zero signups", "conversions dropped", "the ads bring traffic but nothing happens", "still zero after the fix?", or "how do we grow X?" (then read [growth asks](references/growth-asks.md) first).

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| Analytics read access, unless `growth.analytics_source` is `none` | every cut below | a one-day report returns rows |
| Payments read access, unless `growth.payments_source` is `none` | whether anyone paid | the last payment lists |
| The public site and API reachable, with `python3` and `curl` | render and production probes | `curl -sI <site>` answers |
| The owner's standing approval for production probes, before step 6 | the probe creates real rows | recorded, or asked once |

The bundled scripts read the public site only and work with any source. No reader is bundled for an analytics or payments source: read each as `revenue-state-audit` says.

If one is missing, stop before step 1 and say which, what it blocks, and the smallest read-only access that unblocks it. Without analytics, steps 3, 4 and 6 still make sense alone. Never model around a source you could not read.

## Configuration
- `growth.analytics_source` and `growth.payments_source`: `none` means that half is "not measured". Without analytics, no segment can be named as the place of the loss; without payments, nothing is known past the checkout page. `other`: ask how it is read, and say what was used.
- `delivery.issue_tracker`: where step 8 files findings, only when the owner agrees. `none`: they stay in the report.
- Set values with `hermes config set skills.config.<key> <value>`.

## Steps
1. Widen the window before believing the complaint. Run `revenue-state-audit` over 10, 30 and 90 days, and the event's daily series over about 180 days.
2. Cut by channel first (paid against unpaid), then device, then country, each with its own rate, as [the segment cuts](references/segment-cuts.md) say, platform and metric traps included. Compute in code, not by eye.
3. Check that the visitor can see the page: `python3 scripts/landing_payload.py <url> --ua <preset>`, with the user agent the paid traffic really uses, or `--ua-string` for one without a preset. Compare the blocking download time with the median session.
4. Check in-app browsers. Links from social apps open in an embedded browser where sign-in through an identity provider is often refused. If most paid traffic arrives that way, look for a webview detector and its event.
5. If a fix already shipped, follow [did the fix work](references/did-the-fix-work.md): confirm it is live, size the test with `scripts/effect_size.py` before reading the delta, then compare equal windows with `scripts/fisher_exact.py`.
6. Prove the conversion step works before calling it broken, against production, with cleanup: [the production probe](references/production-probe.md). Go on to the payment provider, then measure pricing-page reach by channel, and test the infrastructure changes that landed near the drop.
7. Name in one line the data you could not get (ad spend, search console, app store) and what it would change.
8. Report as [the report](references/report.md) says, then offer one tracker item per cause with its numbers. Never file unasked.

## Decision rules
- A "10-day problem" is usually permanent and only just noticed. Say plainly when the plan changes from "what broke" to "this never worked".
- A real defect on the critical path is not automatically the constraint. A render defect may gate everything: rank it below a channel gap already found, fix it on its merits, and prove its effect in step 5.
- Merged is not deployed, and "shipped and verified" is reported apart from "moved the funnel".
- A verdict scheduled before the required sample exists returns "flat" by construction: push back on it.
- If no paid visitor reaches the pricing page, price and paywall copy are not the constraint.
- A file untouched for months cannot explain a recent drop.
- Never infer paid efficiency from analytics alone.
- A 200 does not mean a page exists: `scripts/crawl_probe.py` fetches an impossible path as a control.

## Done when
- Each cause is backed by a segmented, dated measurement or a production probe, or is labelled a hypothesis.
- The fix list is ordered cheapest first, the gating item is marked, and the dropped work is named.
- The report leads with the measured table and the awkward number, and contradicts the framing when the data does.
