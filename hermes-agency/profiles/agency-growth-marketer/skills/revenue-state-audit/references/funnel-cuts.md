# The cuts

An aggregate never explains itself. Make these cuts, in this order, before naming a cause.

## The funnel
Sessions, the intent step, signup, activation, checkout start, payment. Count people, not events. Use the same windows every time: the last 7 and 28 days, the previous period of the same length, and 90 days or the longest the source holds. Below a few dozen, give counts instead of rates.

## 1. Channel, bucketed paid against unpaid
- Give the session-to-signup rate per bucket.
- When paid converts orders of magnitude worse than unpaid, the constraint is who arrives. Show both rates, and the expected conversions per month: the paid rate multiplied by the monthly paid sessions.

## 2. Device

## 3. Country
With session duration, and whether people there can pay at all (a payment method the product accepts).

## 4. Sources ranked by conversions, not sessions
Over the longest window: which source has ever converted, and at what rate? Test it against the paid bucket before quoting a multiple. A good source that went quiet usually lost a placement: find which.

## 5. The paid share
State it. Traffic that stops when spending stops is rented. The sessions left after paid traffic stops are the real unpaid demand.

## 6. The mechanism behind any change
Before calling a change a regression or a win, check: a tracking change, a consent change, a bot wave, a deploy or a campaign on that date. Check a reported event ("the ads were paused") in the daily series and look for an earlier break: the event explains only the days after it.

## 7. The pay path
Walk it once in production, up to the payment record and the entitlement the payment should grant. A broken or unverified step is fixed before anyone recommends more traffic: past paid sessions multiplied by their rate show what more traffic would buy. Free funnel checks come first, then one paid burst sized in advance.

## Ranking what to do
By closeness to revenue, cheapest first, marking the step that gates the others. A small budget buys an answer, not a business. Each test gets a kill line: metric, threshold, read-out date.
