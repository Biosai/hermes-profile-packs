# The report

- The measured table first: one row per segment, with sessions, conversions as people, the rate, the window and the date measured.
- The awkward number bare, in one sentence: the count, the segment and the window.
- Contradict the framing when the data does.
- Each cause is backed by a segmented, dated measurement or a production probe. Anything else is labelled a hypothesis.
- The fixes ordered cheapest first, the gating one marked, and the work that is dropped.
- One line for the data you could not get (ad spend, search console, app store) and what it would change. Never infer paid efficiency from analytics alone.
- With `growth.analytics_source` or `growth.payments_source` set to `none`, name that half as "not measured" and say what cannot be concluded without it.
- How each number was read: connector, API or export.

Then offer one tracker item per cause, with its numbers, filed where `delivery.issue_tracker` says. Do not file unasked.

For "still zero after the fix?", answer in the order given in the reference on whether the fix worked.

## Infrastructure changes near the drop
Test the changes that landed near the drop (allowed origins with the real origin, redirects, rate limits) as the production probe reference shows. A file untouched for months cannot explain a recent drop.

## Pricing-page reach
Measure how many visitors of each channel reach the pricing page. If no paid visitor reaches it, the price and the paywall copy are not the constraint.
