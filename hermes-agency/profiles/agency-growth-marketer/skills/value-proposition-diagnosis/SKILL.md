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
signups do not come back or pay, when someone asks "what are we missing to convert?" or "is
it our value proposition?", or proposes rewriting the homepage, repositioning, renaming or a
new target customer.

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| Read access to at least one source of customer words (support inbox, reviews, community, interview notes, search queries, replies to feedback emails) | the diagnosis quotes customers | one recent message or review can be read |
| The live value and pricing pages | the proposition as stated | the pages load |
| Read-only access to the product's own events (user store or CRM), optional | where each person stops | one count query returns |
| Analytics read access, when `growth.analytics_source` is not `none` | traffic by source | a one-day report returns rows |
| Payments read access, when `growth.payments_source` is not `none` | whether anyone paid | listing the last payment succeeds |

If a required prerequisite is missing, stop before step 1. Say which one, what it blocks, and
the smallest access that would unblock it (read-only first). Without any customer words there
is no diagnosis, only taste: deliver only where people stop (step 1) and the plan to collect
their words (step 7). Never invent a quote to fill the gap.

## Configuration
- `venture.brief`: read the declared customer and promise from it, and record the result in
  it at the end. Unset: say so, take the promise from the live page, and give the owner the
  text to add to a brief.
- `growth.analytics_source` / `growth.payments_source`: `none` means steps 2 and 6 rely on
  behaviour you can observe directly (replies, price questions), labelled as such.
- Set values with `hermes config set skills.config.<key> <value>`.

## Procedure
1. Locate the loss per person before discussing words: signup, first core use, next-day
   return, allowance used, pricing page, payment; outside people only, counted server-side,
   not in web analytics. Go one level finer than "returned or not": count core uses per
   person. "Four of five used it exactly once" points at the first experience, a different
   fix from "used it for a week and left".
2. Split traffic quality from promise quality: compare signup rate by source on the same page.
   When one source converts and another does not, the promise works and the loss is the
   audience. Answer the framing directly, then correct it with the step: "yes, the proposition
   is weak; no, it is not what blocks today" when the loss sits before the price.
3. Write the current proposition in one sentence exactly as the page states it: for whom,
   the problem, the outcome, why this and not the alternative. Test it against "why this
   instead of the free substitute?" (often a general-purpose tool the customer already has);
   a list of use cases does not answer it. What only the product can claim stays a hypothesis
   until customers say it.
4. Collect customers' own words, read-only, and quote them; do not paraphrase them into the
   team's vocabulary. Zero replies to a feedback email means no written evidence of why
   people left, not that nothing is wrong.
5. Compare: do their words for the problem match the page's words? Is the outcome they want
   the one promised? What do they use today instead, and what does it cost them?
6. Check willingness to pay with behaviour, not opinion: payments, price questions, exits at
   pricing. State the pricing page's reach by outside people before blaming the price.
7. Below about one signup a week, gather evidence instead of rewriting or A/B testing: a copy
   change at that volume cannot be measured for months.
   - Loss after the first use: a free self-test first. With the owner's standing approval for
     probes on internal test accounts, sign up as a stranger, bring the three situations real
     people arrive with, in the main languages, grade the first answer (did it solve it,
     length, what it asked next) and hand over transcripts and a verdict. A weak first answer
     is a content or prompt fix, not a feature.
   - Then about five real people try it on a situation of their own, and three questions:
     better than the free substitute? would you come back tomorrow, and for what? what would
     make you pay the price? Rewrite the proposition in their words, then the site, store and
     directory copy.
8. Name the single biggest mismatch: wrong customer, wrong problem, wrong words, wrong price.
9. Propose one test that isolates it, with a kill line (metric, threshold, read-out date) and
   an owner, and record the result in the brief. List the real defects found on the way with
   their tracking status, say they are not the blocker, and name what is dropped (new
   features, page A/B tests, more ad budget). Offer the owner action; do not file it unasked.

## Output standard
```
Loss: <step> loses <n of N> outside people (<window>, server-side)
Page says: <one sentence>   Substitute: <what they use instead>
Customers say: "<quote>" (<source>), "<quote>" (<source>)
Mismatch: <customer | problem | words | price>: <one line>
Test: <one change or the evidence plan>. Kill line: <metric, threshold, date>. Owner: <...>
Dropped: <...>
```

## Traps
- Rewriting copy because someone asked about the proposition, or from taste. Every change
  traces back to a quoted customer word.
- "0 of 7 returned" reported as a rate. Below ten, give the count and the window.
- A moat claimed on what the substitute can copy in an afternoon. Name it as a hypothesis
  built on what the substitute lacks (memory of each case, reaching out first), sequenced
  after the return loop: memory only pays once someone comes back.
- Asking friends or the team whether they like it. Liking is not paying.
- Inventing quotes, testimonials or logos. Real and attributed with consent, or none.
- Testing three changes at once: whatever moves, nothing is learned.
- Pushing the evidence plan again when the conversation turned into stopping a channel:
  answer that decision, in the language the owner switched to.
