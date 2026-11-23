---
name: crypto-exchange-exit
description: "Plan leaving a crypto exchange and picking an on-ramp"
metadata:
  hermes:
    config:
      - key: wallets.registry
        description: "Path of the register of the owner's wallets and exchange accounts"
        default: ""
      - key: books.location
        description: "Path to the folder or repository that holds the books"
        default: ""
      - key: owner.action_tracker
        description: "Where an owner action is recorded while it waits: issue-tracker, file, or conversation"
        default: "conversation"
---
# Crypto Exchange Exit

Use when the owner must move funds off a crypto exchange (restriction, delisting, closure, licence change), wants a decentralised venue that trades like an exchange, or needs a cheap fiat on-ramp, for a person or a company. The profile plans; the owner clicks.

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| The exchange's own notice to the owner, or its public announcements | the deadline and what is still allowed | the notice or the announcement page |
| The account's holdings: an export, a statement or screenshots | the inventory | every line has a quantity |
| Read access to `wallets.registry` | the receiving wallet's owner | the file is readable |

If one is missing, stop before step 1 and say which, what it blocks, and the smallest access that would unblock it. Without the exchange's own notice, any restriction found in the press is second-hand: say so.

## Configuration
- `wallets.registry`: the receiving wallet must have a row with the same owner as the exchange account's money; a new one is added as `wallet-registry` says.
- `books.location`: where the inventory and each transfer are booked, as `double-entry-books` says.
- `owner.action_tracker`: where each owner step of the plan is recorded with a check that proves it done. `conversation`: listed in the reply.
- Set values with `hermes config set skills.config.<key> <value>`.

## Procedure
1. **Whose money?** Ask in whose name the account is and whose money is in it. The owner decides the books, the tax lens, the receiving wallet and the on-ramp (personal identity checks or company checks). When the account is in a person's name but holds a company's money, the company's accountant classifies it: flag it, do not decide.
2. **Live status.** Read the exchange's own notice and its regulator's public register (for the EU, the ESMA register of crypto-asset service providers): licence, what is disabled (deposits, conversion, trading), custody fees, closure date. Recommend converting on the exchange only once the owner confirms conversion still works for him.
3. **Inventory.** Transcribe every line with a script: quantity, value, tags (monitoring, delisting). Report the total, the concentration of the largest lines, the lines worth less than their withdrawal fee, and any rows missing between screenshots; reconcile with the account's own total.
4. **Exit plan**, deadline first, following [the exit checklist](references/exit-checklist.md): history export before anything else, receiving wallet of the same owner, network per token, a test transfer first, delisting-tagged tokens first, dust written off.
5. **Books and tax.** A transfer between two wallets of the same owner is not a disposal; a swap or a sale is. While the owner's tax residence or regime is open, list each swap as an event to document. Book the inventory and the transfers in the owner's ledger with the documents attached.
6. **Venues and on-ramps.** Give the options for a person and for a company separately, as [the venue guide](references/venues.md) says, each with fees read from the provider's own fee page and the date read.

## Decision rules
- Never withdraw, swap, approve, sign, open an account or contact the exchange: each is the owner's step, prepared with its exact inputs.
- A receiving wallet never mixes two owners' money.
- A custody fee with a fixed minimum is computed against the actual balance, with the date.
- A company holding crypto needs its accountant's agreement first; say so before proposing a corporate on-ramp.
- An airdrop or claim page is never checked by connecting a wallet.
- Fees and licence status are re-read before each use, never reused from a previous answer.

## Quality gate
Done when the reply gives the deadline and its source, the reconciled inventory with its date, a numbered exit plan whose every step is the owner's with its check, the booking or the issue that tracks it, and dated personal and company on-ramp options.
