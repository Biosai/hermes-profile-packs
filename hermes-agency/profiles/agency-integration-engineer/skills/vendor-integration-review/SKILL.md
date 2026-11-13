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

Use when a third-party API integration is new or changed, when a vendor announces a change or a deprecation, or on a periodic check of the vendors the product depends on.

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| A clone of the repositories that call the vendor, with fetch access | the integration code | `git fetch --dry-run` |
| Web access to the vendor's public documentation and changelog | sourced, dated vendor facts | open the vendor's API reference |
| Sandbox credentials, only to observe what the documentation leaves open | observed facts | one read-only sandbox call |

If one is missing, stop before step 1: say which, what it blocks, and the smallest access that unblocks it (read-only first). Never estimate data you could not read, and never report "nothing found" when the lookup failed. A vendor fact you could not source is marked UNSOURCED, never assumed.

## Configuration
- `delivery.default_branch`: code is read at `origin/<default>`; detect with `git symbolic-ref --short refs/remotes/origin/HEAD`.
- `delivery.repos`: every repository that calls the vendor or receives its calls; search all of them.
- `delivery.issue_tracker`: where findings and vendor-change drafts go. `file`: appended to `delivery.issue_file`. `none`: they stay in your report.

## Procedure
1. Fetch and pin the default branch of each repository in scope.
2. Map the data flow: which fields leave the system, to which vendor, for which purpose.
3. List the vendor facts the code relies on (rate limits, retry guidance, idempotency support, webhook delivery guarantees, status codes, formats), each with its source and the date observed.
4. Outbound calls: check retries and idempotency against `retry-idempotency`, which owns them. The review adds: every call has a timeout, each status class is mapped to its cause, and a user-facing error names the right one.
5. Inbound webhooks: check signature (verified before parsing, compared in constant time), replay, deduplication and ordering against `webhook-design`, which owns them.
6. Recovery: every retry, fallback or default that swallows a vendor failure leaves a trace: a log, a metric or an alert.
7. Reconciliation: a periodic comparison of the product's records with the vendor's exists, so a missed webhook is found rather than accumulated.
8. Sandbox versus production: list what the sandbox cannot prove, and who verifies it after release.
9. Audit trail: changes the vendor initiates are recorded.
10. For a vendor change notice: the affected code at the pinned commit, the effective date, and a draft work item per `delivery.issue_tracker`.

## Decision rules
- A field sent to the vendor that the purpose does not need is a finding. Regulated data sent abroad or to a sub-processor is flagged to the owner.
- A vendor fact holds as of a date: a remembered behavior is verified again before it is relied on again.
- A 4xx may be a malformed request, expired credentials, a rate limit or a missing resource; only a documented business refusal is a refusal.
- The review reports findings; redesigning retries or a webhook path is done with `retry-idempotency` and `webhook-design`.

## Quality gate
The review is complete when the report names the vendor, the subject and the pinned commit; the fields sent, and whether they are minimal; each fact relied on with its source and date, or UNSOURCED; outbound (timeouts, retries, idempotency, status mapping) and inbound (signature, replay, idempotent handling, ordering) as pass or finding; whether recovery is traced; the reconciliation job and its cadence, or none; the sandbox gaps and who verifies them after release; and one verdict: OK, or FINDINGS with their count.
