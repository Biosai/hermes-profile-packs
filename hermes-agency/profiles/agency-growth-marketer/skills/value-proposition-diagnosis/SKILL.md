---
name: value-proposition-diagnosis
description: "Test from customer words whether the offer is wanted"
metadata:
  hermes:
    config:
      - key: venture.brief
        description: "Path or URL of the brief: customer, voice, constraints, autonomy"
        default: ""
      - key: growth.analytics_source
        description: "Traffic and funnel numbers: ga4, plausible, posthog, matomo, other, none"
        default: "none"
      - key: growth.payments_source
        description: "Revenue numbers: stripe, paddle, lemonsqueezy, other, none"
        default: "none"
---
# Value Proposition Diagnosis

Use when the funnel works mechanically but people leave at the value page or pricing, when
signups do not come back or pay, or when someone proposes repositioning, renaming or a new
target customer.

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| Read access to at least one source of customer words (support inbox, reviews, community, interview notes, search queries) | the diagnosis quotes customers | one recent message or review can be read |
| The live value and pricing pages | the proposition as stated | the pages load |
| Analytics read access, when `growth.analytics_source` is not `none` | where people leave | a one-day report returns rows |
| Payments read access, when `growth.payments_source` is not `none` | whether anyone paid | listing the last payment succeeds |

If a required prerequisite is missing, stop before step 1. Say which one, what it blocks, and
the smallest access that would unblock it (read-only first). Without any customer words there
is no diagnosis, only taste: stop. Never invent a quote to fill the gap.

## Configuration
- `venture.brief`: read the declared customer and promise from it, and record the result in
  it at the end. Unset: say so, take the promise from the live page, and give the owner the
  text to add to a brief.
- `growth.analytics_source` / `growth.payments_source`: `none` means step 4 relies on
  behaviour you can observe directly (replies, price questions), labelled as such.
- Set values with `hermes config set skills.config.<key> <value>`.

## Procedure
1. Write the current proposition in one sentence exactly as the page states it: for whom,
   the problem, the outcome, why this and not the alternative. If it cannot be summed up in
   one sentence, that is the first finding.
2. Collect customers' own words, read-only, and quote them; do not paraphrase them into the
   team's vocabulary.
3. Compare: do their words for the problem match the page's words? Is the outcome they want
   the one promised? What do they use today instead, and what does it cost them?
4. Check willingness to pay with behaviour, not opinion: payments, price questions, exits at
   pricing. A proposition nobody has paid for is a hypothesis, however warm the feedback.
5. Name the single biggest mismatch: wrong customer, wrong problem, wrong words, wrong price.
6. Propose one test that isolates it, with a kill line (metric, threshold, read-out date) and
   an owner, and record the result in the brief.

## Output standard
```
Page says: <one sentence>
Customers say: "<quote>" (<source>), "<quote>" (<source>)
Mismatch: <customer | problem | words | price>: <one line>
Test: <one change>. Kill line: <metric, threshold, date>. Owner: <...>
```

## Traps
- Rewriting copy from taste. Every change traces back to a quoted customer word.
- Asking friends or the team whether they like it. Liking is not paying.
- Inventing quotes, testimonials or logos. Real and attributed with consent, or none.
- Testing three changes at once: whatever moves, nothing is learned.
