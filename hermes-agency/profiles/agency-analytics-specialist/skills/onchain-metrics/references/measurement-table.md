# The measurement table

Written where `onchain.record` says, one table per window. Public copy takes numbers from here and nowhere else.

```
Window <start..end>   (sources: <explorer or RPC>, <platform statistics>; read <time>)
Network <name>, token <address>
Holders (excluding listed addresses): <n> (<+/-n>)   Transfers: <n>   Active addresses: <n>   Volume: <n> <unit>
Channels: <channel> <n> members (<+/-n>), real conversations: <n>
Anomalies: <cause, or "none found">   Not measured: <what, and why>
```

## Definitions to keep with the table
Write down how each number is counted. Where the project already defines one, its definition wins. Usual starting points:
- **Holders**: addresses with a balance above zero, minus the excluded addresses listed in the record (contract, treasury, liquidity pool, team). State the exclusion list's date.
- **Active addresses**: addresses that sent or received the token in the window, with the same exclusions.
- **Volume**: transferred amount in the window, in the token's unit; say whether transfers to and from excluded addresses are counted.
- **Members, followers**: each platform's own figure, read from its statistics, not from a screenshot.
- **Real conversations**: threads where a person other than the team wrote something that is not spam, a giveaway entry or a bot message. Say how they were counted.

Change a definition only with a note of the date and the reason: a number is comparable only with numbers under the same definition.

## Reading a jump
Before reporting growth, look for its mechanism: an airdrop, a bot wave, a listing, an exploit attempt, one large holder moving funds. Write the cause beside the number.

## Risks seen while measuring
Spam tokens sent to holders, impersonation accounts, phishing links. File each where `delivery.issue_tracker` says, with the address or the link written so that it cannot be clicked. Never interact with the token or open the link to check it.
