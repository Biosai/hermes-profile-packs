---
name: open-pr-readiness-sweep
description: "Sweep every open PR for a read-only merge verdict"
required_environment_variables:
  - name: GITHUB_TOKEN
    prompt: "Token with read access to the repositories swept"
    help: "A fine-grained token with read access to contents, pull requests, statuses and actions"
    required_for: "running scripts/audit_open_prs.py when delivery.code_host is github"
    optional: true
metadata:
  hermes:
    tags: [workflow]
    config:
      - {key: delivery.code_host, description: "Where code is reviewed: github, gitlab, bitbucket, other, or detect", default: "detect"}
      - {key: delivery.repos, description: "Repositories swept: paths or URLs (an org URL = all its repos)", default: ""}
      - {key: delivery.merge_policy, description: "Who merges: owner, reviewer, or auto-when-green", default: "owner"}
      - {key: owner.channel, description: "Where questions and owner actions reach the owner", default: "this conversation"}
    prerequisites:
      commands: [git, gh, glab, python3]
---
# Open PR Readiness Sweep

## Trigger
The owner asks which open pull or merge requests can be merged across the repositories in scope; before a cleanup session; after a burst of agent-authored drafts; or on the schedule the owner set.

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| Read access on the code host to repositories, requests, commit statuses, CI runs and reviews | inventory and CI state | the controls of step 1 |
| `python3` and a token, when `delivery.code_host` is `github` | the bundled `scripts/audit_open_prs.py` | `python3 scripts/audit_open_prs.py --help` |
| A clone with full history, only to diagnose a conflicting request | stale-versus-divergent probes | the clone is not shallow |

The bundled script works for `github` only. On any other host, run the sweep by hand with that host's CLI and fill the same verdict table: [references/sweep-by-hand.md](references/sweep-by-hand.md).

If one is missing, stop before step 1: say which, what it blocks, and the smallest access that unblocks it (read-only first). Zero open requests from a run whose controls failed is a failure, never "nothing to review".

## Configuration
- `delivery.code_host`: `github`: `python3 scripts/audit_open_prs.py <owner> [<owner> ...]` writes `prs_open.json` in the working directory. It reads the token from `GITHUB_TOKEN`, then `GH_TOKEN`, then `gh auth token`; `--token-env NAME` reads another variable instead. Any other value: by hand, as above. Detect from `git remote get-url origin`.
- `delivery.repos`: the repositories swept. An organization or group URL stands for all its non-archived repositories; repositories owned by a personal account are listed separately. Empty: the current repository only. A repository the owner excluded is named once as excluded, never itemized.
- `delivery.merge_policy`: whom the recommendations address.
- `owner.channel`: where the report goes.

## Steps
1. Run the controls first: an authenticated identity call succeeds, and a repository that does not exist answers "not found". If either fails, stop.
2. Enumerate the repositories in scope, then every open request, and resolve each one's mergeable state.
3. Give each request three independent answers, never collapsed: mergeable in git (no conflict); CI at this head (did anything run, and did it pass); human gate (draft, review required, a product or editorial decision).
4. Read CI only from endpoints you can see, asserting each HTTP status before parsing.
5. Chase contradictions before writing: a state that says a check fails while you found none means your probe is blind. Fix the probe; never reconcile in prose.
6. Grade what green is worth: read each repository's CI definitions and name what they execute (tests; compile and lint; a validator that parses files; nothing), then list the jobs that ran at this head.
7. Drill each red to the job, the step and the error line in its log, and keep conflicts apart from failing jobs: [references/red-and-dirty-prs.md](references/red-and-dirty-prs.md).
8. Say what you cannot see, such as branch protection without admin rights, and count approvals.
9. Order siblings: when two requests edit the same files (dependency bumps sharing a lockfile), say which goes first.
10. Report through `owner.channel` in the format of [references/report-format.md](references/report-format.md), and stop. For the one request the owner then picks, run `ready-to-merge-gate`.

## Decision rules
- The sweep is read-only: never merge, close or edit. Merging stays with whoever `delivery.merge_policy` names; when the owner delegates fixing or merging, follow the red-and-dirty reference.
- An endpoint you cannot read returns an error and no list, and an empty list reads as green. Zero runs at the head is "nothing ran", not green.
- A red run whose jobs have zero steps never ran: report "CI did not run" and offer a rerun, never "failing code".
- A red policy job that holds a request for a person is a hold: give its reason and list the request as waiting on that person.
- A conflicting request needs a rebase and its CI color is stale. It may also be a stale snapshot whose merge would delete newer work.
- When branch protection is unreadable, "mergeable" means git state plus observed CI. No approval anywhere is itself a finding.
- Silence from one endpoint is not "all clear": query a sibling endpoint first.
- A scheduled run follows [references/scheduled-run.md](references/scheduled-run.md), and stays silent when there is no open request.

## Done when
- Every open request in scope has its three answers; every red one is named to job, step and error line.
- Every endpoint that failed is named in the report.
- Nothing was merged, closed or edited.
