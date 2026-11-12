---
name: vendor-integration-review
description: "Review a third-party API integration for data and failures"
metadata:
  hermes:
    config:
      - {key: delivery.default_branch, description: "Default branch name, or detect", default: "detect"}
      - {key: delivery.repos, description: "Working copies this profile may read or change (paths or URLs, comma-separated)", default: ""}
      - {key: delivery.issue_tracker, description: "Where work items go: github, gitlab, jira, linear, file, none, or detect", default: "detect"}
      - {key: delivery.issue_file, description: "Markdown file for work items when the tracker is file", default: ""}
    prerequisites:
      commands: [git]
---
# Vendor Integration Review

Reviews a third-party API integration for data flow, failure handling, webhook security and the dated vendor facts the code relies on. Use for a new integration, a change to one, a vendor changelog or deprecation notice, or a periodic watch of the vendors the product depends on.

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| A clone of the repositories that call the vendor, with fetch access | the integration code | `git fetch --dry-run` |
| Web access to the vendor's public documentation and changelog | sourced, dated vendor facts | open the vendor's API reference |
| Sandbox credentials, only to observe behavior the docs leave open | observed facts | one read-only sandbox call |

If a required prerequisite is missing, stop before step 1. Say which one, what it blocks, and the smallest access that would unblock it (read-only first). Do the parts that do not need it only if they still make sense alone. Never replace data you could not read with an estimate, and never report "nothing found" when the lookup failed. A vendor fact you could not source is marked UNSOURCED, never assumed.

## Configuration
- `delivery.default_branch`: code read at `origin/<default>`; detect with `git symbolic-ref --short refs/remotes/origin/HEAD`.
- `delivery.repos`: every repository that calls or receives calls from the vendor; search all of them.
- `delivery.issue_tracker`, `delivery.issue_file`: where findings and vendor-change drafts go. `file`: append to the file. `none`: they stay in your report.
Current values appear in the `[Skill config]` block when the skill loads; an unset key shows its declared default. Persist a detected value with `hermes config set skills.config.<key> <value>` (per profile: `hermes -p <profile> config set …`); `hermes config migrate` prompts for keys still unset.

## Procedure
1. **Map the data flow**: which fields leave the system, to which vendor, for which purpose. Anything not needed for the purpose is a finding. Regulated data sent abroad or to a sub-processor is flagged to the owner.
2. **List the vendor facts the code relies on** (rate limits, retries, idempotency support, webhook delivery guarantees, status codes, formats), each with its source and the date observed. A vendor fact holds as of a date.
3. **Outbound calls**: a timeout on every call; retries only for retryable failures, with backoff and a bound, and with an idempotency key when the call has side effects; each status class mapped to its cause (a 4xx may be a malformed request, expired credentials, a rate limit or a missing resource, not a business refusal); user-facing errors name the right cause.
4. **Inbound webhooks**: signature verified with a constant-time comparison before parsing; replay protection (timestamp window, event-id deduplication); idempotent handling; out-of-order delivery handled.
5. **Recovery**: a retry, fallback or default that swallows a vendor failure leaves a trace (log, metric, alert).
6. **Reconciliation**: a periodic comparison of the product's records with the vendor's, so a missed webhook is found rather than accumulated.
7. **Sandbox versus production**: what the sandbox cannot prove, and who verifies it after release.
8. **Audit trail** for vendor-initiated changes.
9. **Vendor change notice**: the affected code at `origin/<default>`, the effective date, and a draft routed per `delivery.issue_tracker`.

## Output standard
```
Vendor review — <vendor> — <subject link> — origin/<default> @ <sha>
Data out: <fields> — minimal ✔/✘
Facts relied on: <fact> — source <link> — observed <date> | UNSOURCED
Outbound: timeouts ✔ retries ✔ idempotency ✔ status mapping ✔
Inbound: signature ✔ replay ✔ idempotent ✔ ordering ✔
Recovery traced ✔/✘ — Reconciliation: <job, cadence> | none
Sandbox gaps: <list> — verified after release by <role>
Verdict: OK | FINDINGS (<n>)
```

## Traps
- A remembered vendor behavior is not a fact; re-verify before relying on it again.
- Retrying a non-idempotent call without a key creates duplicates at the vendor.
- Parsing a webhook body before verifying its signature exposes the parser to anyone.
