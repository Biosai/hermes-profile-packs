---
name: testnet-deployment
description: "Deploy contracts to a testnet and verify on-chain"
metadata:
  hermes:
    config:
      - key: onchain.record
        description: "Where networks, deployed addresses, transactions and signers are recorded"
        default: ""
      - key: owner.channel
        description: "Where questions and owner actions reach the owner"
        default: "this conversation"
    prerequisites:
      commands: ["git"]
---
# Testnet Deployment

Use when a contract change must run on-chain before any mainnet plan, or when a front end, bot or integration needs a fresh testnet deployment.

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| The on-chain record | the network, addresses already deployed, the deployer, who holds test funds | open where `onchain.record` says |
| A testnet RPC endpoint | deploy and read state | a block-number call answers |
| A signer the owner set up for the testnet deployer (keystore, hardware or signing service), funded | send the deployment transactions | the deployer's testnet balance covers the estimate |
| Explorer access, plus a verification key if the explorer requires one | verify source | the explorer's API answers for the network |
| The project's contract toolchain | build and deploy scripts | its build command succeeds |

If one is missing, stop before step 1: say which, what it blocks, and the smallest access that unblocks it. A missing signer is a stop, never a reason to put a key in the environment, a file or a message.

## Configuration
- `onchain.record`: read before deploying, written after. Unset: ask where it is before deploying anything.
- `owner.channel`: where to ask for funds or a signer when the record names no holder.

Set a value with `hermes config set skills.config.<key> <value>`.

## Procedure
1. Read the record: the network to use, the addresses already deployed there, the deployer and the holder of test funds.
2. Confirm the target is a testnet and the configuration points to it: chain id, RPC endpoint, explorer.
3. Estimate gas. If the deployer needs funds, send the holder named in the record a request stating network, destination, amount and reason.
4. Deploy from a clean checkout of the head under review, through the signer.
5. Verify by reading the chain: code at the address, source verified on the explorer, owner and roles as intended, initial parameters, expected events.
6. Exercise the change with real transactions: the allowed path, the forbidden path (it must revert), edge values.
7. Record network, chain id, addresses, deployer, transaction hashes, verification links and the deployed commit where `onchain.record` says, and in the change description. Mark earlier testnet deployments of the same contracts as superseded.

## Decision rules
- Keys are never read, printed, copied or moved, and you never hold a funded key.
- Test funds come from the holder named in the record, on a request; never from a faucet on your own initiative. When the record names no holder, ask through `owner.channel`.
- A deployment is verified by reading the chain (verified source, expected state), not by the deploy script's exit code or a transaction that succeeded.
- Testnet is the default: a script that can reach a mainnet by changing one variable gets a guard that refuses mainnet without an explicit flag.
- Read addresses from the record or the chain, never from memory or a conversation.
- Name the network in every statement about a deployment. Testnet tokens have no value: never describe them as having any.

## Quality gate
The deployment is complete when the report gives the network and chain id, the deployed commit, each contract with its address and verification link, the checks read from the chain (roles, parameters, the forbidden path reverting), the transaction links, and the record is updated.
