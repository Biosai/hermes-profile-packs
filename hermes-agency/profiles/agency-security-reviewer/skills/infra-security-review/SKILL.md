---
name: infra-security-review
description: "Review IAM, secrets, network and CI changes for risk"
metadata:
  hermes:
    config:
      - {key: delivery.iac_tool, description: "Infrastructure-as-code tool: terraform, opentofu, pulumi, cloudformation, other, none, or detect", default: "detect"}
      - {key: delivery.code_host, description: "Where code is reviewed: github, gitlab, bitbucket, other, or detect", default: "detect"}
      - {key: delivery.apply_policy, description: "Who applies infrastructure changes: human or pipeline-after-approval", default: "human"}
    prerequisites:
      commands: [git]
---
# Infrastructure Security Review

Use when an infrastructure change written by someone else touches identity and access, secrets, network rules, firewall or edge rules, CI pipelines or host bootstrap, and needs an independent review before it merges.

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| Read access to the change and the code it references | the review | open the diff of the pull or merge request |
| Read access to the policies and roles the change references but the repository does not define (a read-only cloud identity) | what the change attaches | describe one referenced policy |
| You wrote no part of the change | independence | its author is another profile or person |

If one is missing, stop before step 1: say which, what it blocks, and the smallest access that unblocks it (read-only first). Never estimate data you could not read, and never report "nothing found" when the lookup failed. A policy you could not read is "not reviewed", never "pass".

## Configuration
- `delivery.iac_tool`: where permissions and rules are declared, and how plan output can expose sensitive attributes (for example values printed by `terraform plan`). Detect from repository files.
- `delivery.code_host`: which CI controls to check. github: workflow files, action pinning, triggers reachable from forks. gitlab: the pipeline file, protected variables and branches. Any other host: the equivalent controls. Detect from `git remote get-url origin`.
- `delivery.apply_policy`: `human`: no pipeline may apply without a person dispatching it. `pipeline-after-approval`: the apply job runs only after a recorded approval on the default branch; check that the approval cannot be skipped.

## Procedure
1. Pin the head under review. Run `security-review` for the method (assets, actors, trust boundaries, ranking); this skill adds the infrastructure areas.
2. Review each area the change touches against [references/checklist.md](references/checklist.md):
   - **Identity and roles**: the narrowest action on the narrowest resource; who can assume each role, from where; no long-lived key where short-lived credentials exist.
   - **Secrets**: no value in code, variable files, plan output, requests, work items, messages or logs; rotation known; read access scoped to the workload.
   - **Network**: new ingress justified by a consumer; nothing private published.
   - **Firewall and edge rules**: observed in count or log mode before enforcing; a removed rule says what it protected against.
   - **CI pipelines**: third-party code pinned to an immutable reference; jobs from forks cannot reach secrets; the apply path matches `delivery.apply_policy`.
   - **Host bootstrap**: downloads verified; no secret on disk in clear or in logs; remote access restricted and logged.
   - **Logging and audit**: access logging not reduced.
3. Read every policy and role the change references, statement by statement.
4. Write the review on the request: each area as PASS, FINDING (line, why, fix) or NOT REVIEWED (what, missing access), then one verdict.

## Decision rules
- This review is independent: the author of a change never performs it, and a self-check is never reported as one.
- You report the finding and the fix; the author makes it. A verdict belongs to the head it was given on: review the new head again.
- A wildcard is a finding unless the change justifies it.
- A permission added "temporarily" to unblock an apply stays: require it scoped now, or a recorded follow-up.
- Never approve a policy by its name: read its statements.
- Check what the CI log will show before a plan runs: plan output can print sensitive attributes.

## Quality gate
The review is complete when every area that the change touches has its line, each finding names the line, the reason and the fix, and the verdict is one of APPROVE, CHANGES REQUIRED (the findings) or INCOMPLETE (what could not be reviewed); anything NOT REVIEWED makes it INCOMPLETE.
