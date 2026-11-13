# Infrastructure security review: the checklist

Companion to `infra-security-review`, step 2. Review only the areas the change touches, line by
line, and write a result for each.

## Identity and roles
- The narrowest action on the narrowest resource. A wildcard is a finding unless the change
  justifies it.
- Trust: who can assume the role, from where, under which conditions. A role CI can assume is
  limited to the repository, branch and environment that need it.
- No long-lived key where short-lived credentials exist.
- A policy referenced by name is read statement by statement before it is approved.

## Secrets
- No value in code, variable files, plan output, requests, work items, messages or logs. The
  change references the secret manager path instead.
- The rotation owner and cadence are known.
- Read access is scoped to the workload that needs the secret.
- When a value may already be exposed, `secret-exposure-review` owns the full trace and the
  response.

## Network
- New ingress is justified by a named consumer.
- Only the public edge is open to the world.
- Egress is not loosened without a reason.
- No private service is published by a new load balancer, bucket policy or DNS record.

## Firewall and edge rules
- A rule change runs in count or log mode first, where the product supports it.
- A removed rule says what it protected against.

## CI pipelines
- Third-party actions, images or plugins are pinned to an immutable digest or a full commit hash.
- Jobs triggered from forks or by external contributors cannot reach secrets or apply credentials.
- The apply path matches `delivery.apply_policy`: under `human`, no pipeline applies without a
  person dispatching it; under `pipeline-after-approval`, the apply job runs only after a recorded
  approval on the default branch, and the approval cannot be skipped.
- Per `delivery.code_host`: on github, read the workflow files, the pinning of each action and the
  triggers reachable from forks; on gitlab, the pipeline file, protected variables and protected
  branches; on any other host, the equivalent controls.

## Host bootstrap
- Downloads are pinned and verified by checksum or signature.
- No secret is written to disk in clear or echoed into logs.
- Remote access is restricted and logged.

## Logging and audit
- Access logging is not reduced.
- A change to log retention is flagged for a compliance review: the compliance reviewer profile
  when it is installed, otherwise the owner.

## Plan output
- Plan output can print sensitive attributes. Check what the CI log will show before the plan
  runs, per `delivery.iac_tool`.

## Review format
```
Security review — <request URL> — head <commit>
Identity: PASS | FINDING: <line> — <why> — <fix> | NOT REVIEWED: <policy, missing access>
Secrets / Network / Firewall-edge / CI / Bootstrap / Logging: ...
Verdict: APPROVE | CHANGES REQUIRED (<findings>) | INCOMPLETE (<what was not reviewable>)
```
