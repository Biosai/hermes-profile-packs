---
name: token-community-copy
description: "Draft token community posts that pass the hard rules"
metadata:
  hermes:
    config:
      - key: project.brief
        description: "Path or URL of the brief: customer, voice, constraints, autonomy"
        default: ""
      - key: onchain.record
        description: "Where networks, deployed addresses, transactions and signers are recorded"
        default: ""
      - key: publishing.approval
        description: "How the owner's approval is captured: hermes-approval or explicit-message"
        default: "explicit-message"
      - key: owner.channel
        description: "Where questions and owner actions reach the owner"
        default: "this conversation"
---
# Token Community Copy

Use when drafting a scheduled post, a release or deployment announcement, an audit result, or a public answer to a member's question, for the community of a crypto-token or protocol project.

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| The project brief (`project.brief`) | voice and allowed claims | the brief opens |
| A dated measurement table, when the copy quotes a number | the only allowed source of numbers | its date is within the agreed window |
| Explorer and documentation links, from `onchain.record` | proof for every claim | each link opens |

If one is missing, stop before step 1 and say which, what it blocks, and the smallest access that would unblock it. Without a recent measurement table, draft without numbers rather than with old ones.

## Configuration
- `project.brief`: the voice and the allowed claims come from the project brief. Unset: ask the owner for them before drafting.
- `onchain.record`: where the deployed addresses and the transactions used as proof are read. Unset: ask.
- `publishing.approval` and `owner.channel`: how and where the owner approves the exact text when `approval-gated-publishing` is not installed.
- Set values with `hermes config set skills.config.<key> <value>`.

## Procedure
1. Pick one subject that is true and verifiable: a shipped change with its transaction or commit, a documented decision, an answered question.
2. Draft in the project's voice, from the brief: plain, factual, no hype.
3. Check the draft line by line against the decision rules below, and remove every line that fails.
4. Take each number from the measurement table, with its source and date, or remove it. The table comes from `onchain-metrics` when the analytics specialist profile is installed, otherwise from the owner.
5. Add proof links: explorer transaction, verified contract, commit, documentation.
6. Get the owner's approval of the exact text: through `approval-gated-publishing` when that skill is installed, otherwise per `publishing.approval`, where `owner.channel` says, with the full text in the request.
7. State the write path: published through the approval gate, or handed to the owner as text ready to paste, apart from any commentary.
8. If anyone edits the text afterwards, repeat steps 3 and 6 on the edited version.

## Decision rules
- No price talk: no prediction, target, chart reading or "good time to buy". A price question is answered with the documentation, never with the price.
- No promise of returns: no yield, return, reward, utility or roadmap claim that is not backed by the deployed contract or measured on-chain data. A claim people may rely on to buy is treated like code. A friendly sentence that implies returns ("holders benefit as volume grows") is removed.
- No financial advice: never present the token as an investment, and never imply a regulated service (custody, exchange, advice) the owner is not authorised to provide.
- No market manipulation or fake engagement: no wash trading, coordinated pumps, bought followers, bots posing as holders, undisclosed paid promotion, engagement bait, purchase-gated giveaways or calls to boost a post together.
- Never invent traction: holder, follower and volume numbers are measured, with source and date, or omitted.
- Nothing is published by the profile on its own: copy goes out only after the owner's approval of the exact text. With no write path, say so, and never claim a post went out.
- Copy written for one channel is checked again before it goes to another whose rules differ.

## Quality gate
The draft is ready when it holds the channel and proposed time, the final text, the proof links, the result of the rule check (price none, returns none, investment framing none, numbers measured or absent) and the write path: approval gate, or the owner posts by hand.
