---
name: wallet-registry
description: "Keep a register of whose each crypto wallet is, and why"
metadata:
  hermes:
    config:
      - key: wallets.registry
        description: "Path of the register of the owner's wallets and exchange accounts"
        default: ""
      - key: books.location
        description: "Path to the folder or repository that holds the books"
        default: ""
---
# Wallet Registry

Use when a person or a company holds several crypto wallets or exchange accounts, a new address appears, or a wallet must be booked, audited or reported. This is record-keeping, not custody.

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| The register at `wallets.registry`, or the owner's agreement to create it | one place that says whose each wallet is | the file exists, or the owner said yes |
| Write access to it | adding and correcting rows | the file is writable |
| The owner, for every classification | only the owner knows whose money it is | an answer in the conversation |

If one is missing, stop before step 1 and say which, what it blocks, and the smallest access that would unblock it. Never guess an owner or a purpose to fill a row.

## Configuration
- `wallets.registry`: unset means ask where the register should live; propose the books' folder (`books.location`) or a private note beside them, never a public place. The row layout is in [the register format](references/register-format.md).
- `books.location`: where the books are, so each row can name the ledger account it is booked in.
- Set values with `hermes config set skills.config.<key> <value>`.

## Procedure
1. **Look it up first.** Before auditing, booking or asking about an address, search the register for it, and the books for its short form. A known address keeps its label; never give one wallet two labels.
2. **One row per wallet or exchange account**, with a short label (W1, W2…) used everywhere else: chain or chains, kind (self-custody, smart-contract wallet, MPC wallet, exchange account, app wallet), the address shortened to its first and last four characters, the owner, the purpose, the ledger account, the date added and the source of each fact.
3. **Owner.** Ask whose money it is: the person, a named company, or a third party the owner only operates for. The name an exchange account is opened in does not settle whose money is in it; record both and say who decides (the owner, or the company's accountant for a company).
4. **Purpose.** Savings, operating cost, test or sandbox funds, a product's treasury, an app's in-game wallet. Test wallets funded for a product are that product's owner's operating cost, not savings, unless the owner says otherwise.
5. **Links.** Record which wallets fund each other and which exchange accounts feed them, each with one transaction as evidence. A transfer between two wallets of the same owner is not a disposal; between two owners it is, in both books.
6. **Status.** Active, dormant, emptied, compromised or retired, with the date. A retired wallet stays in the register.
7. **Change.** Classifications change only on the owner's word, with the date it was given. Update the register in the same change as the books, as `double-entry-books` says.

## Decision rules
- The register holds no key, seed phrase, password or exchange API secret, ever, and no full address in a message, an issue or a pull request: first and last four characters only.
- An address seen only as a counterparty is not the owner's until the owner says so.
- A wallet the owner's agent itself controls for test funds is not the owner's savings; it gets its own row with that purpose.
- One row, one owner. A wallet that mixes two owners' money is flagged for the owner, not split by guesswork.
- Balances belong in the books, not in the register: the register says whose and why, the books say how much.

## Quality gate
Done when every wallet and exchange account in scope has one row with a label, an owner given by the owner, a purpose, a ledger account or "not booked", and a dated source, and no row holds a secret or a full address.
