# Register format

A Markdown table or a YAML file beside the books. The books' own conventions win over this page where they differ.

## Markdown table

| Label | Chains | Kind | Address | Owner | Purpose | Ledger account | Status | Added | Source |
|---|---|---|---|---|---|---|---|---|---|
| W1 | BSC | MPC wallet | `0x1234…abcd` | the person | savings | `Assets:Crypto:BSC:W1` | active | 2025-01-15 | owner, in conversation |
| W2 | Ethereum, Arbitrum | self-custody | `0x5678…ef01` | the company | test funds for a product | `Assets:Crypto:Test:W2` | active | 2025-02-03 | owner, in conversation |
| EX1 | — | exchange account | account ending `…1234` | opened in the person's name, money the company's | trading sandbox | `Assets:Exchange:EX1` | exit planned | 2025-03-01 | exchange statement |

## YAML

```yaml
- label: W1
  chains: [bsc]
  kind: mpc-wallet
  address: "0x1234…abcd"
  owner: person            # person | company:<name> | third-party:<name>
  purpose: savings
  ledger_account: Assets:Crypto:BSC:W1
  status: active
  added: 2025-01-15
  source: "owner, in conversation"
  links:
    - to: W2
      evidence: "tx 0xaaaa…bbbb"
```

## Kinds

- **self-custody**: one private key or seed phrase held by the owner.
- **smart-contract wallet**: a multisig or account-abstraction wallet; record the signers' labels, never their keys.
- **MPC wallet**: the key is split between the owner and a provider; the provider can block withdrawals.
- **exchange account**: custodial; the balance is the exchange's statement, not the chain.
- **app wallet**: a wallet an app created for in-app use; some balances live in the app, not on chain.

## Address shortening

First four characters after the prefix and last four: `0x1234…abcd`. Exchange accounts: the last four characters of the account or user id.
