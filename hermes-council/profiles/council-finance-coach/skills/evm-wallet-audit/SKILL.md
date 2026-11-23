---
name: evm-wallet-audit
description: "Audit an EVM wallet across chains, read-only"
metadata:
  hermes:
    config:
      - key: wallets.registry
        description: "Path of the register of the owner's wallets and exchange accounts"
        default: ""
      - key: books.location
        description: "Path to the folder or repository that holds the books"
        default: ""
    prerequisites:
      commands: ["python3"]
---
# EVM Wallet Audit

Use when the owner sends an EVM address and asks what it holds, where it is active, how its funds came in, or what it is linked to, or when a known wallet needs a fresh multichain inventory. The audit reads public data only.

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| Outbound HTTPS to public RPC endpoints and block explorers | balances, nonces, history | one `eth_blockNumber` call answers |
| A headless browser, for explorers that render with JavaScript or sit behind a bot wall | token lists and protocol positions | the browser loads one explorer page |
| Read access to `wallets.registry` | known labels and owners | the file is readable |

If one is missing, stop before step 1 and say which, what it blocks, and the smallest access that would unblock it. Measure what you can and mark each chain or source that failed as "not read". Never report "empty" for a chain you could not read.

## Configuration
- `wallets.registry`: looked up first, so a known wallet keeps its label and owner; a new wallet is proposed as a row there, as `wallet-registry` says. Unset: report the wallet unlabelled and ask where the register lives.
- `books.location`: where a booking would go once the owner agrees; the booking follows `double-entry-books`.
- Set values with `hermes config set skills.config.<key> <value>`.

## Procedure
1. **Known wallet?** Search the register and the books for the address and its short form before reading the chain.
2. **Native sweep.** On each EVM chain in [the explorer guide](references/explorers.md), call `eth_getBalance` and `eth_getTransactionCount` on a public RPC endpoint. A nonce above zero means the wallet sends there: go deep. A zero nonce can still hold received tokens, so the token step still applies.
3. **History and tokens** from an explorer API that answers without a key (Blockscout API v2 where it runs): transactions, token transfers, token balances, internal transactions. Save every response to a file and parse it with a script, never by eye.
4. **Protocol positions** from a portfolio viewer (lending, staking, liquidity), then confirm each with a `balanceOf` call on its receipt token: the deposit plus the yield shows there, not in the transfers.
5. **Counterparties.** For each address that is not a contract, classify it: a known wallet of the owner (from the register), a labelled exchange, or unknown. Very high transaction counts and balances suggest an exchange hot wallet: say "likely an exchange" without naming one. A small private wallet that funded the address may be the owner's: ask.
6. **Closed positions.** Compute each one's result in the token's own units, from amount in to amount out, and state it plainly, negative included.
7. **Spam.** Classify every token with [the spam rules](references/spam-tokens.md) before any total.

## Decision rules
- Read-only: never connect a wallet, sign, approve, revoke, swap or claim, and never open a link carried by a token's name.
- Spam is listed, never valued, booked or touched; unpriced or unidentified tokens are listed as such.
- Every figure carries its source and the time it was read. A failed source is named in the report.
- Addresses are shortened to their first and last four characters in every report, issue and pull request.
- Ownership comes from the owner, never from a funding pattern alone.
- Idle funds and stale approvals are reported; revoking or moving them is the owner's step.

## Quality gate
Done when the report gives the total and the time measured, holdings per chain, the dated history of how funds came in and moved, links to known wallets, protocol positions confirmed on chain, the spam list kept out of the total, the sources and the ones that failed, and one question: add the wallet to the register and the books?
