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

Use when a product has traffic or users but little or no revenue, when someone proposes
buying traffic or building a feature to grow, or before any plan, post or message quotes a
number about the business. Measured state comes first; every plan is built on it.

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
- `growth.analytics_source` / `growth.payments_source` decide where steps 1 and 3 read from.
  `other`: ask which tool and how to read it, then say what you used. `none`: that half of
  the funnel is "not measured".
- Set values with `hermes config set skills.config.<key> <value>`; `hermes config migrate`
  asks for unset ones.

## Procedure
1. Pull each number from its source, read-only, and record the query, window and time run.
2. Re-verify before quoting: a number from a deck, a chat or an earlier audit is a dated
   claim, not the current state.
3. Build the funnel with the same windows every time (last 7 and 28 days, previous period):
   sessions, intent step, signup, activation, checkout start, payment, with each step's
   conversion and absolute loss. Below a few dozen events, give counts, not rates.
4. State the paid share of traffic. Traffic that stops when spending stops is rented.
5. Before calling a change a regression or a win, check the mechanism: tracking changes,
   filters, consent, bot waves, a deploy or campaign on that date.
6. Walk the pay path once in production up to the payment record and the entitlement. A
   broken or unverified step is fixed before anyone recommends more traffic.
7. Name the binding constraint: the step whose improvement most plausibly ends in a payment.
   A defect on the critical path is not automatically the constraint; prove it with a
   before/after on the metric it should move, or retract it.
8. Rank the backlog by revenue proximity and say what is dropped. A small budget buys an
   answer, not a business. Give each test a kill line (metric, threshold, read-out date).

## Output standard
```
Revenue state as of <date> (sources: <analytics>, <payments>; pulled <time>)
Awkward number first: <number and why it matters>
Funnel: sessions <n> (paid <x>%) -> intent <n> -> signup <n> -> activated <n> -> paid <n>
Revenue: <amount> | last completed payment: <date> | not measured: <...>
Binding constraint: <step> (<evidence>)
Next test: <change>. Kill line: <metric> >= <threshold> by <date>. Dropping: <...>
```

## Traps
- Quoting last month's number as current, or mixing two sources for one funnel step.
- Recommending paid acquisition while any step to payment is broken or unverified.
- Agreeing with a stakeholder's framing because it is theirs. Contradict it with evidence.
