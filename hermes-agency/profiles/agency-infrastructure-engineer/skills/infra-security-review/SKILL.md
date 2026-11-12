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

Reviews a change to IAM, secrets, network rules, WAF or edge rules, CI pipelines or host bootstrap for least privilege, exposure and secret handling, line by line, before it merges. Yours or another profile's.

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| Read access to the change and the code it references | the review | open the PR (pull or merge request) diff |
| Read access to referenced policies and roles not defined in the repository (a read-only cloud identity, for example IAM read) | review what the change attaches | describe one referenced policy |

If a required prerequisite is missing, stop before step 1. Say which one, what it blocks, and the smallest access that would unblock it (read-only first). Do the parts that do not need it only if they still make sense alone. Never replace data you could not read with an estimate, and never report "nothing found" when the lookup failed. A policy you could not read is "not reviewed", never "pass".

## Configuration
- `delivery.iac_tool`: where permissions and rules are declared and how plan output can leak attributes (for example sensitive values in `terraform plan`). Detect from repository files.
- `delivery.code_host`: decides the CI checks. github: workflow files under `.github/workflows`, action pinning, fork triggers. gitlab: `.gitlab-ci.yml`, protected variables and branches. Other hosts: the equivalent controls. Detect from `git remote get-url origin`.
- `delivery.apply_policy`: `human`: no pipeline may apply without a human dispatch. `pipeline-after-approval`: the apply job runs only after a recorded approval on the default branch; check that approval cannot be skipped.
Current values appear in the `[Skill config]` block when the skill loads; an unset key shows its declared default. Persist a detected value with `hermes config set skills.config.<key> <value>` (per profile: `hermes -p <profile> config set …`); `hermes config migrate` prompts for keys still unset.

## Procedure
1. **IAM and roles**: narrowest action on the narrowest resource; wildcards are findings unless justified. Trust: who can assume the role, from where, under which conditions; a role CI can assume is limited to the repository, branch and environment that need it. No long-lived keys where short-lived credentials exist.
2. **Secrets**: no value in code, variables files, plan output, PRs, work items, chat or logs; reference the secret manager path. Rotation owner and cadence known. Read access scoped to the workload.
3. **Network**: new ingress justified by a consumer; only the public edge is open to the world; egress not loosened without reason; no private service published by a new load balancer, bucket policy or DNS record.
4. **WAF and edge**: rule changes run in count or log mode first where supported; a removed rule says what it protected against.
5. **CI pipelines**: third-party actions, images or plugins pinned to an immutable digest or full commit SHA; jobs from forks or external contributors cannot reach secrets or apply credentials; the apply path matches `delivery.apply_policy`.
6. **Host bootstrap**: downloads pinned and verified (checksum or signature); no secret written to disk in clear or echoed into logs; remote access restricted and logged.
7. **Logging and audit**: access logging not reduced; log retention changes go past compliance.

## Output standard
```
Security review — <PR URL>
IAM: PASS | FINDING: <line> — <why> — <fix> | NOT REVIEWED: <policy, missing access>
Secrets / Network / WAF-edge / CI / Bootstrap / Logging: ...
Verdict: APPROVE | CHANGES REQUIRED (<findings>) | INCOMPLETE (<what was not reviewable>)
```

## Traps
- A permission added "temporarily" to unblock an apply stays forever. Scope it now or record the follow-up.
- Plan output can print sensitive attributes; check what the CI log will show before running it.
- Approving a policy by its name without reading its statements.
