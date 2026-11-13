---
name: revenue-state-audit
description: "Audit measured revenue state and the binding constraint"
metadata:
  hermes:
    config:
      - key: growth.analytics_source
        description: "Traffic and funnel numbers: ga4, plausible, posthog, matomo, other, none"
        default: "none"
      - key: growth.payments_source
        description: "Revenue numbers: stripe, paddle, lemonsqueezy, other, none"
        default: "none"
required_environment_variables:
  - name: GOOGLE_APPLICATION_CREDENTIALS
    prompt: "Path to a Google service-account JSON with Viewer access to the GA4 property"
    help: "Only when growth.analytics_source is ga4 and no analytics connector is set up"
    required_for: "reading traffic and conversions from GA4"
    optional: true
  - name: STRIPE_API_KEY
    prompt: "Stripe restricted key with read-only access"
    help: "Only when growth.payments_source is stripe and no payments connector is set up"
    required_for: "reading payments and revenue from Stripe"
    optional: true
---
# Revenue State Audit

Use when a product has traffic or users but little or no revenue, when someone asks how the numbers are or proposes buying traffic or a feature, or before a business number is quoted. Zero or falling conversions continue with the `conversion-drop-diagnosis` workflow.

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| Analytics read access, unless `growth.analytics_source` is `none` | sessions, channels, funnel steps | a one-day report returns rows |
| Payments read access, unless `growth.payments_source` is `none` | payments and revenue | the last payment lists |
| The product's user store, read-only (optional) | signups and activation | one count query returns |

No reader is bundled. Hermes can prompt for `GOOGLE_APPLICATION_CREDENTIALS` (`ga4`) and `STRIPE_API_KEY` (`stripe`) when no connector is set up. Any other source is read through its own connector, API or export, by hand, as [reading each source](references/sources.md) says.

If one is missing, stop before step 1 and say which, what it blocks, and the smallest read-only access that unblocks it. Never estimate what you could not read, and never report "no revenue" when the lookup failed.

## Configuration
- `growth.analytics_source` and `growth.payments_source` name where the numbers come from. `other`: ask which tool, and how it is read.
- `none` for analytics leaves arrival, channels, paid share and where visitors stop unknown. `none` for payments leaves revenue and who paid unknown. Label that half "not measured" and say what cannot be concluded. With both `none`, stop and say which setting and access would allow an audit.
- Set values with `hermes config set skills.config.<key> <value>`.

## Procedure
1. Pull each number from its source, read-only, recording how it was read, the window and the time. End windows yesterday: analytics processing lags by hours.
2. Build the funnel with the stages of `acquisition-funnel`, counted as people, over the same windows every time: 7 and 28 days, the previous period, and 90 days or the longest the source holds.
3. Cut before concluding, in the order of [the cuts](references/funnel-cuts.md): channel (paid against unpaid), device, country. Then rank sources by conversions and state the paid share.
4. Before calling a change a regression or a win, check its mechanism: tracking, consent, bots, a deploy or a campaign that day.
5. Walk the pay path once in production, up to the payment record and the entitlement.
6. Apply [the measurement traps](references/measurement-traps.md) before quoting any count, the team's own test activity first.
7. Name the binding constraint: the step whose improvement most plausibly ends in payment.
8. Rank the backlog by closeness to revenue, cheapest first, marking the step that gates the others. Give each test a kill line: metric, threshold, read-out date.
9. Report in [the report format](references/report-format.md), or its quick pulse for a same-day question. Offer to file one item per cause; never file unasked.

## Decision rules
- A number from a deck, a conversation or an earlier audit is a dated claim: re-verify it before quoting. An absence is "none in <window>, measured <date>", never "never".
- Below a few dozen, give counts, not rates.
- No conclusion before the cuts: an aggregate never explains itself.
- A defect on the critical path is not automatically the constraint: prove it with a before and after on its metric, or retract it.
- A broken or unverified step to payment is fixed before anyone recommends more traffic.
- Contradict a stakeholder's framing when the evidence does.
- A reported event explains only the days after it: look for an earlier break in the daily series.

## Quality gate
Done when every number in the report was read today from its source, with its window and how it was read, each unmeasured half is named with what it leaves unknown, the binding constraint rests on a measurement, and the next test has a kill line and names what is dropped.
