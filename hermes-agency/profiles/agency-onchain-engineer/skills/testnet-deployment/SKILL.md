---
name: testnet-deployment
description: "Deploy contracts to a testnet and verify on-chain"
metadata:
  hermes:
    config:
      - key: venture.brief
        description: "Path or URL of the brief: customer, voice, constraints, autonomy"
        default: ""
      - key: owner.channel
        description: "Where questions and owner actions reach the owner"
        default: "this conversation"
    prerequisites:
      commands: ["git"]
---
# Testnet Deployment

Use when a contract change must run on-chain before review or before any mainnet plan, or
when a front end, bot or integration needs a fresh testnet deployment.

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| A testnet RPC endpoint | deploy and read state | a block-number call answers |
| A signer the owner set up for the testnet deployer (keystore, hardware or signing service), funded | send deployment transactions | the deployer's testnet balance covers the estimate |
| Explorer access, plus a verification key if the explorer requires one | verify source | the explorer's API answers for the network |
| The project's contract toolchain | build and deploy scripts | its build command succeeds |

If a required prerequisite is missing, stop before step 1. Say which one, what it blocks, and
the smallest access that would unblock it. Never put a private key in the environment, a
file or a chat to get past a missing signer, and never fund yourself from a faucet unasked.

## Configuration
- `venture.brief`: the project record. Read the networks in use, the addresses already
  deployed, and who holds test funds. Unset: ask before deploying anything.
- `owner.channel`: where to ask for funds or a signer when the record names no holder.
- Set values with `hermes config set skills.config.<key> <value>`.

## Procedure
1. Confirm the target is a testnet and the config points to it (chain id, RPC, explorer). A
   script that can reach a mainnet by changing one variable gets a guard that refuses mainnet
   without an explicit flag; testnet is the default.
2. Estimate gas. If the deployer needs funds, ask the holder named in the record (or the
   owner) with network, address, amount and reason.
3. Deploy from a clean checkout of the branch under review. The key stays in the signer: you
   never read, print or copy it.
4. Verify by reading the chain, not the script's exit code: code at the address, source
   verified, owner and roles as intended, initial parameters, expected events.
5. Exercise the change with real transactions: the allowed path, the forbidden path (it must
   revert), edge values.
6. Record network, addresses, deployer, transaction hashes, verification links and the
   deployed commit in the project record and the change description. Mark earlier testnet
   deployments as superseded.

## Output standard
```
Network: <testnet> (chain id <n>)   Commit: <sha>
Contracts: <name> <address> (verified: <link>)
Checks: roles <ok>, parameters <ok>, forbidden path reverts <ok>
Transactions: <links>
```

## Traps
- A deployment script with a mainnet default.
- Addresses copied from memory or chat. Read them from the record or the chain.
- "Verified" meaning only that the transaction succeeded.
- Testnet tokens described in public as having value. They do not.
