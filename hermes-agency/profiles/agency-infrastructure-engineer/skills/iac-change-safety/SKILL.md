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
    prerequisites:
      commands: [git, terraform, tofu, pulumi, gh, glab]
---
# IaC Change Safety

Use when writing an infrastructure-as-code change: to prove from its plan that it does only what it should, and to check the result after its apply.

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| A clone of the IaC repository, with push access to branches | the pull or merge request | `git push --dry-run` |
| Read access to CI plan output, or read-only cloud and state access | plan evidence | open the latest plan job |
| The IaC tool at the pinned version, when planning locally | a plan equal to CI's | `<tool> version` |

If one is missing, stop before step 1: say which, what it blocks, and the smallest access that unblocks it (read-only first). Never estimate data you could not read, and never report "nothing found" when the lookup failed.

## Configuration
- `delivery.iac_tool`: the plan command. terraform: `terraform plan`; opentofu: `tofu plan`; pulumi: `pulumi preview`; cloudformation: a change set; other: its dry run. `none`: there is no IaC; say so and stop. Detect from files (`*.tf`, `Pulumi.yaml`, templates) and say what you found.
- `delivery.apply_policy`: `human`: a person applies after the merge, from your exact inputs. `pipeline-after-approval`: a pipeline applies after a recorded approval, which you never trigger or bypass.
- `delivery.merge_policy`: who receives the ready request.
- `delivery.code_host`, `delivery.default_branch`: the CLI for the request and CI (github: `gh`; gitlab: `glab`; other: its own) and the base ref.

## Procedure
1. Run `infrastructure-change` first for the design: current state, blast radius, sequencing, recovery.
2. Work from a work item, in your own worktree, on a freshly fetched default branch.
3. Make the smallest change that closes it: one concern per request.
4. Read the plan for every environment the change reaches, from CI or reproduced exactly (same variables, backend and tool version).
5. Count the adds, changes, replaces and destroys. For each replace: the attribute that forces it, and whether an in-place path exists. For each destroy: nothing references it, and its data is empty, migrated, or accepted as lost by the owner.
6. Look for drift: planned changes you did not write.
7. Open the request with the plan evidence (action counts, every replace and destroy explained, the drift report), the exact apply inputs and their order across environments, and the rollback.
8. Hand over. In the `infra-plan-to-apply` workflow the security review, the gate, the merge and the apply follow as their own steps. Without it, a change to identity, secrets, network exposure, a firewall, CI or host bootstrap first gets an independent review: the security reviewer profile when it is installed, otherwise a person other than the author.
9. After the apply, read its output and confirm a fresh plan shows no changes.

## Decision rules
- You never apply and never need write credentials to the cloud: tell the owner if you hold any. An urgent fix is still a request, plus a runbook a person runs: [references/hand-apply-runbook.md](references/hand-apply-runbook.md).
- Read the plan's resource list, not the diff: a replace can hide in a module or provider version bump.
- A local plan with different variables is a different plan.
- A rename needs an explicit move, or it plans as destroy plus create.
- Drift means a resource was changed by hand: stop and report before your request overwrites it.
- A failed apply is reported with the resource and the error, never retried by you.
- An admin override around a required approval is never acceptable.

## Quality gate
The change is ready when the request links the work item and gives the changes per environment, the plan counts with every replace and destroy justified, the security review result when one was required, the exact apply inputs and order, the rollback, and what could not be checked. It is done when a fresh plan after the apply is empty.
