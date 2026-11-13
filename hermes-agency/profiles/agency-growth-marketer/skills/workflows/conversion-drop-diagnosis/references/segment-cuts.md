# The segment cuts

The answer is almost always in a segment. An answer to "why zero signups?" that is not backed by a fresh, segmented pull is worth nothing.

## Reading the source
Read the analytics and payments sources as `revenue-state-audit` says, for whatever `growth.analytics_source` and `growth.payments_source` name. This workflow bundles no reader for them. Say in the report how each number was read.

## 1. Widen the window first
- `revenue-state-audit` over 10, 30 and 90 days.
- The daily series of the conversion event over about 180 days.

A "10-day problem" is usually permanent and only just noticed. That changes the plan from "what broke" to "this never worked": say so plainly.

## 2. Cut, each with its own rate
1. Channel, paid against unpaid.
2. Device.
3. Country.

- Where the source reports sessions and events separately, pull the sessions in a second report on the same dimensions and join the two in code.
- Pull session duration and pages per session per channel. A bucket at a few seconds and about one page never entered the funnel.
- Compute in code, not by eye: the share of sessions in countries with no payment option the product accepts, and the share of sessions under about 2 seconds.
- Cut by platform before blaming a native-app defect: it cannot be the constraint while nearly all sessions are on the web.

## 3. Metrics that cannot measure a fix
A metric whose definition depends on the broken thing cannot measure its repair. Session duration runs from the first event to the last: a page that fires a spurious early event shows longer sessions while it is broken. Check which events bound the metric, or measure server-side.

## 4. In-app browsers
Links from social apps open in an embedded browser. Sign-in through an identity provider is often refused there (an error such as `disallowed_useragent`, or blocked popups). If most paid traffic is in-app, social login is dead for it by construction. Look in the product for a webview detector and the event it emits, and count that event.

## 5. The page the visitor is served
```
python3 scripts/landing_payload.py <url> --ua <preset>
python3 scripts/landing_payload.py <url> --ua-string "<full user agent>"
```
`--ua` or `--ua-string` is required: use the user agent the paid traffic really arrives with. Presets exist for two social in-app browsers (`instagram`, `facebook`) and for `iphone`, `android` and `desktop` browsers; for any other app, copy its user agent from the analytics source or the server logs and pass it with `--ua-string`.

An empty mount element as the whole body means nothing paints until the script bundle has run. Compare the blocking download time with the median session of that traffic.
