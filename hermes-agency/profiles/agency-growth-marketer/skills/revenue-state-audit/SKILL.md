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

Use when a product has traffic or users but little or no revenue, when someone asks "how are
the numbers?" or proposes buying traffic or a feature to grow, or before any message quotes a
business number. Measured state comes first. Zero or falling conversions: then run the
`conversion-drop-diagnosis` workflow.

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| Read access to the analytics source, when `growth.analytics_source` is not `none` (e.g. GA4 Viewer) | sessions, channels, funnel steps | a one-day report returns rows |
| Read access to the payments source, when `growth.payments_source` is not `none` (e.g. a read-only Stripe key) | payments and revenue | listing the last payment succeeds |
| Read-only access to the product's user store (optional) | signups and activation | one count query returns |

If a required prerequisite is missing, stop before step 1. Say which one, what it blocks, and
the smallest access that would unblock it (read-only first). With both sources `none`, there
is nothing to measure: stop and say which setting and access would make the audit possible.
With one source, audit that part only and label the other "not measured". Never replace data
you could not read with an estimate, and never report "no revenue" when the lookup failed.

## Configuration
- `growth.analytics_source` / `growth.payments_source` decide where the numbers come from.
  `other`: ask which tool and how to read it, then say what you used. `none`: that half of
  the funnel is "not measured".
- Set values with `hermes config set skills.config.<key> <value>`; `hermes config migrate`
  asks for unset ones.

## Procedure
1. Pull each number from its source, read-only, and record the query, window and time run.
   Analytics processing lags hours: end windows yesterday; today's row is context only.
2. Re-verify before quoting: a number from a deck, a chat or an earlier audit is a dated
   claim. State absences as "none in <window>, measured <date>", never "never".
3. Build the funnel with the same windows every time (last 7 and 28 days, previous period,
   and 90 days or the longest the source holds): sessions, intent step, signup, activation,
   checkout start, payment, counted as people, not events. Below a few dozen, give counts.
4. Cut before concluding: an aggregate never explains itself. Channel first, bucketed paid
   vs unpaid, with session-to-signup per bucket; then device; then country with session
   duration and whether people there can pay. When paid converts orders of magnitude worse
   than unpaid, the constraint is who arrives: show both rates and paid rate x monthly paid
   sessions = expected conversions per month.
5. Rank sources by conversions, not sessions, over the longest window: which source has ever
   converted, at what rate? Test it against the paid bucket before quoting a multiple. A good
   source that went quiet usually lost a placement.
6. State the paid share. Traffic that stops when spending stops is rented; the sessions left
   after paid traffic stops are the real unpaid demand.
7. Before calling a change a regression or a win, check the mechanism: tracking changes,
   consent, bot waves, a deploy or campaign on that date. Check a reported event ("we paused
   the ads") in the daily series and look for an earlier break: it explains only later days.
8. Walk the pay path once in production up to the payment record and the entitlement. A
   broken or unverified step is fixed before anyone recommends more traffic.
9. Name the binding constraint: the step whose improvement most plausibly ends in a payment.
   A defect on the critical path is not automatically the constraint; prove it with a
   before/after on the metric it should move, or retract it.
10. Rank the backlog by revenue proximity, cheapest first, marking the step that gates the
   others, and say what is dropped. A small budget buys an answer, not a business. Give each
   test a kill line (metric, threshold, read-out date). Offer to file one item per cause
   with its numbers; do not file unasked.

## Quick pulse ("how are we doing today?")
One read, a short answer in this order: revenue with the date of the last real payment;
last 7 vs previous 7 days (sessions, paid share, funnel steps as people); 90-day funnel in
counts; the last step an outside person reached; what changed the series and what it does
not explain; one next step as a question, and what is dropped.

## Output standard
```
Revenue state as of <date> (sources: <analytics>, <payments>; pulled <time>)
Awkward number first: <number and why it matters>
Funnel: sessions <n> (paid <x>%) -> intent <n> -> signup <n> -> activated <n> -> paid <n>
By channel: paid <rate> vs unpaid <rate>; best source ever: <source, rate, window>
Revenue: <amount> | last completed payment: <date> | not measured: <...>
Binding constraint: <step> (<evidence>)
Next test: <change>. Kill line: <metric> >= <threshold> by <date>. Dropping: <...>
```

## Traps
- An active subscription is not revenue: read its latest invoice's amount paid; fully
  discounted plans stay active at zero. A success-page view is not a payment until matched
  to a payment record.
- Checkout sessions or one conversion counted before removing the team's own tests: group by
  hashed address and domain (never print addresses); reserved test domains, the product's
  own domain, direct-traffic hits on a day someone worked on the funnel and bursts from one
  identity are internal. Zero outside checkouts means the funnel breaks before payment.
- Survivors of a step mistaken for demand (cut the numerator too), or a zero on an event
  that was never instrumented or is emitted under two names after a rename.
- Two analytics properties tracking one site: use the one carrying the conversion events,
  say which, never add them. A report capped at a row limit hides rare rows: filter for them.
- Engaged or bounce rate on few-second sessions read as engagement; prefer duration and pages
  per session, and never compare a duration across a change to the events that bound it.
- More traffic while a step to payment is broken or unverified: past paid sessions x their
  rate shows what more buys. Free funnel checks first, then one pre-sized paid burst.
- Agreeing with a stakeholder's framing because it is theirs. Contradict it with evidence.
