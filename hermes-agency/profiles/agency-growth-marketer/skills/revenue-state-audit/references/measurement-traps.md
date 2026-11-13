# Measurement traps

Check each before quoting a count.

## The team's own activity
Remove it before counting a checkout or a conversion. Group by hashed address and by domain; never print an address. Internal: reserved test domains, the product's own domain, direct-traffic hits on a day someone worked on the funnel, bursts from one identity. Zero outside checkouts means the funnel breaks before payment.

## Revenue
- An active subscription is not revenue: read the amount paid on its latest invoice. A fully discounted plan stays active at zero.
- A success-page view is not a payment until it is matched to a payment record.
- Test-mode records are not revenue.

## Funnel counts
- Survivors of a step are not demand: cut the numerator as well as the denominator.
- A zero may be an event that was never instrumented, or one emitted under two names after a rename. Check when the event was first and last recorded.
- Two analytics properties tracking one site: use the one that carries the conversion events, say which, and never add them.
- A report capped at a row limit hides rare rows: filter for them.

## Engagement
- An engaged or bounce rate on sessions of a few seconds is not engagement. Prefer duration and pages per session.
- Never compare a duration across a change to the events that bound it: duration runs from the first event to the last.

## Framing
- More traffic while a step to payment is broken or unverified buys nothing.
- A stakeholder's framing is tested like any other claim: contradict it when the evidence does.
