---
name: onchain-metrics
description: "Measure on-chain and community numbers, read-only"
metadata:
  hermes:
    config:
      - key: venture.brief
        description: "Path or URL of the brief: customer, voice, constraints, autonomy"
        default: ""
      - key: delivery.issue_tracker
        description: "Issue tracker: github, gitlab, jira, linear, file, none, or detect"
        default: "detect"
      - key: delivery.issue_file
        description: "Markdown file for work items when the tracker is 'file'"
        default: ""
---
# Onchain Metrics

Use for the periodic measurement the owner asked for, or before any post, pitch or document
quotes a holder, follower or volume number for a token or protocol project.

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| Read-only chain access: an explorer API or a read-only RPC endpoint | holders, transfers, volume | a balance or block query answers |
| Read access to each community platform's own statistics | members and activity per channel | the statistics page or API answers |
| The list of excluded addresses (contract, treasury, liquidity, team) in the project record | honest holder counts | the record lists them |

If a required prerequisite is missing, stop before step 1. Say which one, what it blocks, and
the smallest access that would unblock it (read-only first). Measure what you can and mark
the rest "not measured"; never carry an old number forward as current, and never report
"no activity" when a lookup failed. No tool that asks for a wallet signature: read-only means
no signature.

## Configuration
- `venture.brief`: the project record that holds the networks, the token addresses and the
  excluded addresses, and where the measurement table is written. Unset: ask before
  measuring, so the count does not include the wrong wallets.
- `delivery.issue_tracker`: where risks found while measuring are filed; `file` appends to
  `delivery.issue_file`; `none` keeps them in the report; `detect` uses the code host's
  tracker if enabled, and says so.
- Set values with `hermes config set skills.config.<key> <value>`.

## Procedure
1. Note each source and the time of reading.
2. On-chain: holders excluding the listed addresses, transfers, active addresses and volume,
   over the same window each time.
3. Community: members and followers per channel, posts, replies, and an honest read of real
   conversation versus noise (bots, spam, giveaway hunters).
4. Check the mechanism behind any jump: an airdrop, a bot wave, a listing, an exploit
   attempt, one large holder. A number that moved for a reason other than real interest is
   labelled as such.
5. Record the table in the project record. It is the only place public copy may take
   numbers from.
6. File risks seen while measuring (spam tokens sent to holders, impersonation accounts,
   phishing links) per `delivery.issue_tracker`. Never interact with a
   suspicious token or link to check it.

## Output standard
```
Window <start..end>   (sources: <explorer or RPC>, <platform statistics>)
Holders (excluding listed addresses): <n> (<+/-n>)   Transfers: <n>   Volume: <n> <unit>
Channels: <channel> <n> members (<+/-n>), real conversations: <n>
Anomalies: <cause, or "none found">   Not measured: <...>
```

## Traps
- Counting treasury, liquidity pool or team wallets as holders.
- Presenting growth driven by an airdrop or bots as traction.
- Comparing windows of different lengths.
