---
name: value-proposition-diagnosis
description: "Test from customer words whether the offer is wanted"
metadata:
  hermes:
    config:
      - key: project.brief
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

Use when the funnel works mechanically but people leave at the value page or pricing, when signups do not return or pay, or when someone blames the value proposition or proposes a new homepage, positioning, name or target customer.

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| A source of customer words, read-only: support inbox, reviews, community, interview notes, search queries, feedback replies | the diagnosis quotes customers | one recent message opens |
| The live value and pricing pages | the proposition as stated | the pages load |
| The product's user store or CRM, read-only (optional) | where each person stops | one count query returns |
| Analytics and payments read access, unless the source is `none` | traffic by source, who paid | as in `revenue-state-audit` |

If one is missing, stop before step 1 and say which, what it blocks, and the smallest read-only access that unblocks it. Without customer words there is only taste: deliver step 1 and the evidence plan of step 7. Never invent a quote.

## Configuration
- `project.brief`: the project brief gives the declared customer and promise, and receives the result. Unset: take the promise from the live page, say so, and give the owner the text for a brief.
- `growth.analytics_source` and `growth.payments_source`: read as `revenue-state-audit` says. `none`: steps 2 and 6 rely on behaviour observed directly (replies, price questions), labelled as such.
- Set values with `hermes config set skills.config.<key> <value>`.

## Procedure
1. Locate the loss per person before discussing words: signup, first core use, next-day return, allowance used, pricing page, payment. Count outside people only, server-side, and core uses per person.
2. Split traffic quality from promise quality: compare the signup rate by source on the same page.
3. Write the proposition in one sentence, as the page states it: for whom, the problem, the outcome, why this and not the alternative. Test it against "why this instead of the free substitute?".
4. Collect customers' own words and quote them unchanged.
5. Compare their words for the problem and the outcome with the page's; note what they use today and its cost to them.
6. Check willingness to pay with behaviour: payments, price questions, exits at pricing. Count the outside people who reached the pricing page before blaming the price.
7. Below about one signup a week, gather evidence instead of rewriting or A/B testing, with [the evidence plan](references/evidence-plan.md).
8. Name the single biggest mismatch: wrong customer, wrong problem, wrong words or wrong price.
9. Propose one test that isolates it, with a kill line (metric, threshold, read-out date) and an owner. Name what is dropped, and the defects found that do not block.
10. Report in [the report format](references/report-format.md) and record the result in the project brief. Offer the owner action; never file it unasked.

## Decision rules
- Every copy change traces back to a quoted customer word, never to taste or to the question asked.
- When one source converts and another does not on the same page, the promise works and the loss is the audience.
- Answer the framing, then correct it with the step: a proposition can be weak without being what blocks today.
- Below ten, give the count and the window, never a rate.
- Liking is not paying: the opinion of friends or the team proves nothing. An edge only the product claims is a hypothesis.
- Quotes, testimonials and logos are real and used with consent, or absent.
- One change per test: with three, whatever moves, nothing is learned.

## Quality gate
Done when the loss is a count of outside people at one step, the page's sentence sits beside the customers' quoted words, one mismatch is named, and one test or evidence plan carries a kill line, an owner and what is dropped.
