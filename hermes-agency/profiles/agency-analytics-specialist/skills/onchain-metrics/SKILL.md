---
name: onchain-metrics
description: "Measure on-chain and community numbers, read-only"
metadata:
  hermes:
    config:
      - key: onchain.record
        description: "Where networks, deployed addresses, transactions and signers are recorded"
        default: ""
      - key: delivery.issue_tracker
        description: "Issue tracker: github, gitlab, jira, linear, file, none, or detect"
        default: "detect"
      - key: delivery.issue_file
        description: "Markdown file for work items when the tracker is 'file'"
        default: ""
---
# Onchain Metrics

Use when the owner asked for a periodic measurement of a token or protocol project, or before any post, pitch or document quotes a holder, follower or volume number. The work is read-only measurement.

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| Read-only chain access: an explorer API or a read-only RPC endpoint | holders, transfers, volume | a balance or block query answers |
| Read access to each community platform's own statistics | members and activity per channel | the statistics page or API answers |
| The networks, token addresses and excluded addresses (contract, treasury, liquidity, team), from `onchain.record` | the right contracts, honest holder counts | the record lists them |

If one is missing, stop before step 1 and say which, what it blocks, and the smallest read-only access that would unblock it. Measure what you can and mark the rest "not measured". Never carry an old number forward as current, and never report "no activity" when a lookup failed.

## Configuration
- `onchain.record`: where the networks, the token addresses and the excluded addresses are read, and where the measurement table is written. Unset: ask before measuring, so that the count does not include the wrong wallets.
- `delivery.issue_tracker`: where risks seen while measuring are filed. `file`: appended to `delivery.issue_file`. `none`: they stay in the report. `detect`: the code host's tracker when it is enabled, saying so.
- Set values with `hermes config set skills.config.<key> <value>`.

## Procedure
1. Define each number once, as `measurement-plan` says (what is counted, what is excluded, window, unit, source), and keep the definitions with the table.
2. Note each source and the time of reading.
3. On-chain, per network in the record: holders excluding the listed addresses, transfers, active addresses and volume, over the same window each time.
4. Community: members and followers per channel, posts, replies, and an honest read of real conversation against noise (bots, spam, giveaway hunters).
5. Check the mechanism behind any jump: an airdrop, a bot wave, a listing, an exploit attempt, one large holder. Label a number that moved for a reason other than real interest.
6. Write [the measurement table](references/measurement-table.md) where `onchain.record` says. It is the only place public copy may take numbers from.
7. File the risks seen while measuring (spam tokens sent to holders, impersonation accounts, phishing links) per `delivery.issue_tracker`.

## Decision rules
- Read-only means no signature: never use a tool that asks to connect a wallet or to sign.
- Never interact with a suspicious token or open a suspicious link to check it.
- Contract, treasury, liquidity pool and team wallets are not holders.
- Growth driven by an airdrop or by bots is not traction: say what drove it.
- Compare only windows of the same length.
- A number that could not be read is "not measured", never the previous period's value.
- These are counts, not a journey: where people stop between the community and the product belongs to `funnel-analysis`.

## Quality gate
The measurement is done when the table gives the window, each source with the time it was read, every number under its recorded definition with the change since the previous window, the anomalies with their cause or "none found", and what was not measured, and the risks seen are filed or listed.
