# The sweep by hand, on a host the script does not cover

Companion to `open-pr-readiness-sweep`. `scripts/audit_open_prs.py` reads the GitHub REST API and
nothing else. For any other value of `delivery.code_host`, do the same sweep with that host's own
CLI or API, and say in the report that it was done by hand.

## Controls first
Before believing any listing, prove the client can tell states apart:
1. an authenticated identity call succeeds and names the account;
2. a repository or project that does not exist answers "not found".
If either fails, stop. Zero open requests after failed controls is a failure, not a result.

## Scope
List the repositories from `delivery.repos`. An organization or group listing shows its own
non-archived repositories and never those owned by a personal account: list those separately.
Name once, and never itemize, a repository the owner excluded.

## Fields to collect, per open request
| Field | Why |
|---|---|
| Repository, number, title, link | identity |
| Draft or not | the human gate |
| Conflict state with its target branch | mergeable in git |
| Head commit | every CI answer is about this commit |
| CI runs or pipelines for that exact commit, each with its conclusion | did anything run, did it pass |
| Other commit statuses (deploy previews, external CI) | results outside the main CI |
| Approvals, and whether one is required | the human gate |
| Lines added and deleted, files changed, last update | size and staleness |
| The CI definitions of the repository | what a green is worth |

## Examples
**gitlab**: `glab mr list` for the open merge requests of a project; `glab mr view <id>` for the
draft flag, conflicts and merge status of one; pipelines for the exact commit through the
pipelines API (`glab api "projects/<id>/pipelines?sha=<sha>"`), since a plain pipeline list is not
filtered by commit; approvals through the merge request's approvals endpoint.

**Any other host**: its CLI when it has one, otherwise its web UI. Read the same fields, filter
CI by the head commit, and note which fields the host does not expose.

## Then
Classify each request exactly as the workflow's steps 3 to 9 say, and fill the verdict table of
`report-format.md`. The decision rules do not change with the host: an endpoint that returns an
error is named in the report, an empty list is not a green, and nothing is merged, closed or
edited.
