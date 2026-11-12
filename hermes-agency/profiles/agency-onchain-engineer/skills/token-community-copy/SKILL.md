---
name: token-community-copy
description: "Draft token community posts that pass the hard rules"
metadata:
  hermes:
    config:
      - key: venture.brief
        description: "Path or URL of the brief: customer, voice, constraints, autonomy"
        default: ""
      - key: publishing.approval
        description: "How the owner's approval is captured: hermes-approval or explicit-message"
        default: "explicit-message"
      - key: owner.channel
        description: "Where questions and owner actions reach the owner"
        default: "this conversation"
---
# Token Community Copy

Use for a scheduled community post, a release or deployment announcement, an audit result,
or a public answer to a community question about a token or protocol project.

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| The project's brief (`venture.brief`) | voice and allowed claims | the brief opens |
| A recent measurement table from `onchain-metrics` | the only allowed source of numbers | the table is dated within the agreed window |
| Explorer and documentation links | proof for every claim | each link opens |

If a required prerequisite is missing, stop before step 1. Say which one, what it blocks, and
the smallest access that would unblock it. Without a recent measurement table, draft without
numbers rather than with old ones.

## Configuration
- `venture.brief`: unset means ask the owner for voice and allowed claims before drafting.
- `publishing.approval` and `owner.channel`: how and where the owner approves the final text
  (see `approval-gated-publishing` on `agency-social-media-manager`).
- Set values with `hermes config set skills.config.<key> <value>`.

## Procedure
1. Pick one subject that is true and verifiable: a shipped change with its transaction or
   commit, a documented decision, an answered question.
2. Draft in the project's voice: plain, factual, no hype.
3. Run the hard-rule check line by line:
   - no price, prediction, target, chart, "buy", "pump", "moon" or similar;
   - no yield, return, reward or utility claim unless the deployed contract does it and you
     link to it;
   - no investment framing, nothing implying a regulated service;
   - every number from the `onchain-metrics` table with source and date, or removed;
   - no engagement bait, purchase-gated giveaways or requests to coordinate boosting.
4. Add proof links: explorer transaction, verified contract, commit, documentation.
5. State the write path honestly: hand the draft to `agency-social-media-manager` for the
   approval gate, or give the owner a ready-to-post package. Never claim it was posted.
6. If anyone edits the text afterwards, run the hard-rule check again on the edited version.

## Output standard
```
<channel> - proposed <date time>
<final text>
Proof: <links>
Hard-rule check: price none | returns none | investment framing none | numbers measured
Write path: approval gate | owner posts manually
```

## Traps
- A friendly sentence that implies returns ("holders benefit as volume grows"). Remove it.
- A holder count from an old screenshot.
- Engaging with price questions at all. Point to the documentation, never to the price.
- Copy written for one channel pasted into another with different rules.
