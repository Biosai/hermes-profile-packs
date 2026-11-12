# "How do we grow X?"

When the question shifts from "why is X zero?" to "how do we grow X?", do not jump to
tactics. These checks routinely kill the question as asked.

## A. Check X's denominator first

A downstream metric cannot be grown directly when the population it draws from does not
exist. Pull the 365-day count of the event and of distinct people, then the monthly new vs
returning series. Returning sessions flat at a few dozen a month while new sessions swing by
thousands means logins or retention are a symptom of the account count, not a lever. Say so,
decline the workstream (its effect could never be measured) and name the upstream metric.

## B. Prove the organic channel is reachable before proposing content

Single-digit organic sessions per quarter is rarely a ranking problem. Run
`python3 scripts/crawl_probe.py <site>`, then follow `organic-channel-audit.md`.

## C. Order the answer by cost; refuse the underpowered experiment

A store listing, profile page or directory entry that is written but not published is the
cheapest lever there is: rank it above any build, and verify it on the live public page, not
in the repository. An experiment on that surface needs the same power check as step 5 of the
workflow: publish first, baseline the conversion rate, then test a variant.

## D. Decline a recurring content generator; offer a reminder

When the plan lands on organic content, the next ask is often "shouldn't we schedule this?".
Give the reasons, not only the rule:
- If the search results are already held by direct competitors (one search round tells),
  the only edge is a person with a point of view; a weekly generated piece is the commodity
  they already outrank, under the brand's name.
- A job that writes public content is automated publishing; publishing needs approval.
- Cadence is not the constraint while indexation is unmeasured.

Offer a reminder to a person instead, and let the owner choose. Frame "write more?" as a
commitment with a number and a date, or an explicit decision to stop at one.

## E. "Is it our value proposition?"

Locate the loss before touching words: `value-proposition-diagnosis`.

## F. A native-app defect while the web carries the traffic

Cut by platform before blaming a missing in-app billing path: it cannot be the constraint
while nearly all sessions are on the web and the store shows almost no installs. Report it,
say why it is not the constraint, and name the install volume that would promote it.
