---
name: iac-change-safety
description: "Write an IaC change and prove its plan is safe"
metadata:
  hermes:
    config:
      - {key: delivery.iac_tool, description: "Infrastructure-as-code tool: terraform, opentofu, pulumi, cloudformation, other, none, or detect", default: "detect"}
      - {key: delivery.apply_policy, description: "Who applies infrastructure changes: human or pipeline-after-approval", default: "human"}
      - {key: delivery.code_host, description: "Where code is reviewed: github, gitlab, bitbucket, other, or detect", default: "detect"}
      - {key: delivery.default_branch, description: "Default branch name, or detect", default: "detect"}
      - {key: delivery.merge_policy, description: "Who merges: owner, reviewer, or auto-when-green", default: "owner"}
      - {key: delivery.issue_tracker, description: "Where work items go: github, gitlab, jira, linear, file, none, or detect", default: "detect"}
      - {key: delivery.board, description: "Where work is claimed: hermes-kanban, tracker, or none", default: "none"}
    prerequisites:
      commands: [git, terraform, tofu, pulumi, gh, glab]
---
# IaC Change Safety

How to write an infrastructure-as-code change and prove, from its plan, that it does only what it should, then check the result after the apply. It is the `plan` and `verify` steps of the `infra-change` workflow, which orders the security review, the ready-to-merge gate, the merge and the apply. You never apply: who applies follows `delivery.apply_policy`. An urgent fix is still a PR (pull or merge request), plus a hand-apply runbook a human runs.

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| A clone of the IaC repository, with push access to branches | the PR | `git push --dry-run` on a scratch branch |
| Read access to CI plan output, or read-only cloud credentials plus state read access to reproduce CI's plan exactly | plan evidence | open the latest plan job, or a read-only identity call |
| The IaC tool at the version the repository pins, when planning locally (`terraform`, `tofu`, `pulumi`, …) | local plan | `<tool> version` against the pinned version |

If a required prerequisite is missing, stop before step 1. Say which one, what it blocks, and the smallest access that would unblock it (read-only first). Do the parts that do not need it only if they still make sense alone. Never replace data you could not read with an estimate, and never report "nothing found" when the lookup failed. This profile never needs apply or write credentials to the cloud; if it holds any under `delivery.apply_policy: human`, say so to the owner.

## Configuration
- `delivery.iac_tool`: the plan command and its vocabulary (`terraform plan` / `tofu plan`, `pulumi preview`, a change set for cloudformation). `none`: there is no IaC; say so and stop. Detect from files (`*.tf`, `Pulumi.yaml`, templates) and say what you found.
- `delivery.apply_policy`: `human` (default): a human applies after merge; you hand over exact inputs. `pipeline-after-approval`: the pipeline applies after a recorded approval; you never trigger it from a session and never bypass the approval.
- `delivery.merge_policy`: who receives the ready PR (default: the owner, on an explicit go).
- `delivery.code_host`, `delivery.default_branch`: PR and CI commands, and the base ref `origin/<default>`.
- `delivery.issue_tracker`, `delivery.board`: where the item lives and whether you claim it (`none`: skip and say so).
Current values appear in the `[Skill config]` block when the skill loads; an unset key shows its declared default. Persist a detected value with `hermes config set skills.config.<key> <value>` (per profile: `hermes -p <profile> config set …`); `hermes config migrate` prompts for keys still unset.

## Procedure
1. **Start from a work item** (or, with tracker `none`, the request); claim per `delivery.board`.
2. **Work in your own worktree** from a fresh `origin/<default>`. Never stash in a shared checkout.
3. **Make the smallest change** that closes the item; one concern per PR.
4. **Read the plan, not the diff**, for every environment it reaches; from CI, or reproduced exactly (same variables, backend, tool version).
5. **Count actions**: add, change, replace, destroy. Each replace: the forcing attribute, and whether an in-place path exists. Each destroy: nothing references it, and its data is empty, migrated, or accepted as lost by the owner. Renames need explicit moves, or they plan as destroy plus create.
6. **Drift** (changes you did not make) means a hand change; stop and report before your PR overwrites it.
7. **Open the PR** with the plan evidence (action counts, every replace and destroy explained, drift report) and the exact apply inputs. The security review, the gate, the merge and the apply follow in the `infra-change` workflow; without it, run `infra-security-review` yourself for IAM, secrets, network, WAF, CI or bootstrap changes and hand off: `WAITING ON YOU — review <PR URL>, then apply with <inputs>`.
8. **After the apply** (the `verify` step), read its output and confirm a fresh plan is empty. A failed apply is reported with resource and error, never retried by you.

## Urgent: hand-apply runbook (in the PR)
Incident (what, since when, evidence) · Preconditions (identity, tools and versions, environment, a read-only command confirming the broken state) · Steps (numbered; exact command, every value filled except secrets, expected output, stop condition) · Verification · Rollback · Reconciliation (merge, then a plan that shows no changes).

## Output standard
PR description: item link; why; changes per environment; plan counts with every replace and destroy justified; security review result; exact apply inputs and order across environments; rollback; what you could not check, marked skipped. Every number from a command you ran, dated in UTC.

## Traps
- A local plan with different variables is a different plan.
- A replace hidden in a module or provider version bump; read the resource list.
- An admin override around a required approval is never acceptable.
