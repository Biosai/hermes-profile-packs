---
name: contract-change-authoring
description: "Write a contract change with failing-first tests"
metadata:
  hermes:
    config:
      - key: delivery.code_host
        description: "Where code is reviewed: github, gitlab, bitbucket, other, or detect"
        default: "detect"
      - key: delivery.default_branch
        description: "Default branch name, or detect"
        default: "detect"
      - key: delivery.merge_policy
        description: "Who merges: owner, reviewer, or auto-when-green"
        default: "owner"
      - key: owner.action_tracker
        description: "Where a waiting owner action is recorded: issue-tracker, file, conversation"
        default: "conversation"
      - key: onchain.record
        description: "Where networks, deployed addresses, transactions and signers are recorded"
        default: ""
    prerequisites:
      commands: ["git"]
---
# Contract Change Authoring

Use when changing contract source, deployment or upgrade scripts, access control, fees, supply, allowances, or configuration that a deployed contract reads.

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| Read and branch access to the contracts repository | the change and its tests | `git fetch --dry-run` |
| The project's contract toolchain (for example Foundry or Hardhat) | build, test, fuzz, gas | its test command runs on the default branch |
| A reviewer who did not write the change | independent review | the reviewer is named and has accepted |

If one is missing, stop before step 1: say which, what it blocks, and the smallest access that unblocks it. Never mark a change reviewed or tested when that step could not run.

## Configuration
- `delivery.code_host`, `delivery.default_branch`: the CLI (github: `gh`; gitlab: `glab`; any other host: its own), the words (pull or merge request, "the request" below) and the base. Detect from `git remote get-url origin` and `git symbolic-ref --short refs/remotes/origin/HEAD`.
- `delivery.merge_policy`: who merges after the reviews. Whatever its value, you never merge a contract change.
- `owner.action_tracker`: where each prepared mainnet action waits for the owner.
- `onchain.record`: where a mainnet transaction is recorded once the owner has signed it. Unset: ask.

## Procedure
1. Write the intent in one paragraph: what changes, why, and which invariants must hold (supply, ownership, who can pause or mint, fee bounds, upgrade authority).
2. Branch from a freshly fetched default branch: one change per branch.
3. Write the tests first: the new behavior and each invariant, seen failing on the unchanged contract for the right reason.
4. Make the change. Run the full suite, fuzz or property tests where they exist, static analysis and a gas comparison, and read the CI log to confirm each ran.
5. Open the request as a draft with the intent, the invariants, the test evidence (counts, CI log links, gas comparison) and the exact mainnet steps, if any.
6. Hand over. In the `contract-change` workflow the independent reviews, the testnet deployment, the merge and the owner's mainnet decision follow as their own steps, and a finding sends the work back to you. Without the workflow, run them in that order yourself: review by the code reviewer and security reviewer profiles when they are installed, otherwise by a person other than the author, then `testnet-deployment`.
7. For each mainnet action, prepare the exact transaction, its simulation and its verification plan, and record it for the owner where `owner.action_tracker` says. Once the owner has signed, verify as planned and record the transaction where `onchain.record` says.

## Decision rules
- No change is too small: "just a parameter" is behavior.
- Every mainnet action needs the owner's explicit approval and signature: deploying, upgrading, minting, pausing, transferring ownership, changing fees or allowances. You prepare; the owner signs.
- A guardrail is not trusted until seen failing: an access-control test counts only once it has failed against a deliberately broken contract.
- Your own review is never the independent review, and is never reported as one.
- A green suite proves nothing about a path it never exercised: confirm the changed path ran.
- Upgradeable contracts: check the storage layout against the deployed one, and account for every key that can upgrade.
- The owner decides whether a change touching funds or upgrade authority needs an external audit.

## Quality gate
The change is ready for review when the draft request states the change in one line and its invariants, and gives the new tests with their count, seen failing then passing, with the CI log link. It is complete when the request also carries the testnet network, addresses and transaction links, the reviewer and the state of the review, and for mainnet either "none" or the link to the prepared owner action.
