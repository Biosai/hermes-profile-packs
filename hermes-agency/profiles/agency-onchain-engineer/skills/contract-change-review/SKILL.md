---
name: contract-change-review
description: "Take a contract change through tests, review, approval"
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
    prerequisites:
      commands: ["git"]
---
# Contract Change Review

Use for any change to contract source, deployment or upgrade scripts, access control, fees,
supply, allowances, or configuration a deployed contract reads. No change is too small:
"just a parameter" is behaviour.

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| Read and branch access to the contracts repository | the change and its tests | `git fetch` succeeds |
| The project's contract toolchain (for example Foundry or Hardhat) | build, test, fuzz, gas | its test command runs on the default branch |
| A testnet deployment path (`testnet-deployment` prerequisites) | the on-chain run | see that skill |
| A reviewer who did not write the change | independent review | a named reviewer accepted |

If a required prerequisite is missing, stop before step 1. Say which one, what it blocks, and
the smallest access that would unblock it. Never mark a change reviewed or tested when that
step could not run.

## Configuration
- `delivery.code_host` and `delivery.default_branch`: the CLI, the words (pull or merge
  request) and the base; `detect` as in `bounded-task-delivery`, and say what you found.
- `delivery.merge_policy`: who merges after approval. Whatever its value, contract changes
  also need the owner's explicit approval, and you never merge.
- `owner.action_tracker`: where each mainnet action is recorded for the owner.
- Set values with `hermes config set skills.config.<key> <value>`.

## Procedure
1. Write the intent in one paragraph: what changes, why, which invariants must hold (supply,
   ownership, who can pause or mint, fee bounds, upgrade authority).
2. Branch from a fresh fetch of the default branch, one change per branch.
3. Tests first: new behaviour and each invariant, seen failing on the unchanged contract for
   the right reason. For access control, also seen failing against a deliberately broken one.
4. Make the change. Run the full suite, fuzz or property tests where they exist, static
   analysis, a gas comparison. Read the CI log to confirm they ran.
5. Run it on a testnet with `testnet-deployment`.
6. Independent review by someone who did not write it (`agency-security-reviewer`,
   `agency-code-reviewer` or a person); the owner decides whether anything touching funds or
   upgrade authority needs an external audit. Record findings and their resolution.
7. Open the request as a draft with intent, invariants, test evidence, testnet addresses and
   transactions, the review record, and the exact mainnet steps if any.
8. The owner approves. Each mainnet action becomes an owner action, recorded per
   `owner.action_tracker`, with the prepared transaction, its simulation and its check.

## Output standard
```
Change: <one line>   Invariants: <list>
Tests: <n> new, seen failing <yes>, passing <yes> (<CI log link>)
Testnet: <network> <address> <transaction links>   Review: <reviewer> - <state>
Mainnet: none | owner action <link>
```

## Traps
- Reviewing your own change and calling it independent.
- A green suite that never exercised the changed path.
- Upgradeable contracts: an unchecked storage layout, or an upgrade key nobody accounted for.
