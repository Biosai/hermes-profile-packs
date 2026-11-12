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

Answers "which PRs can I merge?", "what is ready to ship?" and the daily digest across every repository in scope. It gives a read-only portfolio verdict; for the one PR (pull or merge request) the owner then picks, the full check is `ready-to-merge-gate`. Merging stays with whoever `delivery.merge_policy` names.

## Trigger
The owner asks which PRs are mergeable across repositories, before a cleanup session, after a burst of agent-authored drafts, or on the schedule the owner set.

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| Code-host read access to repositories, PRs, commit statuses, CI runs and reviews | inventory and CI state | `gh auth status` / `glab auth status`; the positive control in step 1 |
| `python3`, when `delivery.code_host` is github | `scripts/audit_open_prs.py` | `python3 --version` |
| A clone with full history, only to diagnose a conflicting PR | stale-versus-divergent probes | the clone is not shallow |

If a required prerequisite is missing, stop before step 1. Say which one, what it blocks, and the smallest access that would unblock it (read-only first). Do the parts that do not need it only if they still make sense alone. Never replace data you could not read with an estimate, and never report "nothing found" when the lookup failed. Zero open PRs from a run whose controls failed is a failure, never "nothing to review".

## Configuration
- `delivery.repos`: the repositories swept. An organization or group URL stands for all its non-archived repositories; repositories owned outside it (a personal account) are listed separately, since an organization listing never shows them. Empty: the current repository only. A repository the owner excluded is named once as excluded and never itemised.
- `delivery.code_host`: github: run `python3 scripts/audit_open_prs.py <org>`. It reads `GITHUB_TOKEN`, `GH_TOKEN` or `HERMES_GITHUB_TOKEN` (the profile's `.env` file first, since a running process keeps a rotated-away value), then `gh auth token`, and writes `prs_open.json` in the working directory. gitlab or other: collect the same fields with the CLI (for example `glab mr list`, pipelines filtered by SHA). `detect` from `git remote get-url origin`.
- `delivery.merge_policy`: whom the recommendations address. The sweep never merges.
- `owner.channel`: where the digest goes.
Current values appear in the `[Skill config]` block when the skill loads; an unset key shows its declared default. Persist a value with `hermes config set skills.config.<key> <value>` (per profile: `hermes -p <profile> config set …`); `hermes config migrate` prompts for keys still unset.

## Steps
1. **Controls first**: an authenticated identity call succeeds, and a nonexistent repository answers not found. If either fails, stop: the client cannot tell states apart.
2. **Enumerate** the repositories in scope, then every open PR. On github `mergeable` is absent from list responses and null until computed: re-fetch each PR and poll until it resolves.
3. **Three independent answers per PR**, never collapsed: git-mergeable (no conflicts); CI state (did anything run at this head, and did it pass); human gate (draft, review required, an editorial or product decision).
4. **Read CI only from endpoints you can see, asserting each HTTP status before parsing.** A 403 body carries no list, and an empty list reads as green. On github a plain token may get 403 on check runs: use commit statuses plus workflow runs by head SHA. Zero runs at the head (HTTP 200, count 0) is "nothing ran", not green.
5. **Chase contradictions before writing**: `unstable` (a non-required check failing) with no failing check found means your probe is blind. Fix the probe; never reconcile in prose.
6. **Grade what green is worth**: read each repository's workflow files and name what they execute (tests; compile and lint; a validator that parses files; nothing at all), then list the jobs that actually ran at this head.
7. **Drill red** to the job, the step and the error line in its log; one bad character in one file is a one-commit fix, a validator rejecting the content is a rewrite. A red run whose jobs have zero steps never ran (a runner or billing failure): report "CI did not run" and offer a rerun, never "failing code". A red policy job that holds a PR for a human (an auto-merge policy) is a hold: print its reason and list the PR as waiting on that human. Keep conflicts apart from failing jobs: a conflicting PR needs a rebase and its CI colour is stale. A conflicting PR may also be a stale snapshot whose merge would delete newer work: `references/red-and-dirty-prs.md`.
8. **Say what you cannot see**: branch protection is unreadable without admin rights, so "mergeable" means git state plus observed CI, not "the merge button is green for you". Count approvals; none anywhere is itself a finding.
9. **Order siblings**: when two PRs edit the same files (dependency bumps sharing a lockfile), say which goes first instead of listing both as independently mergeable.
10. **Report and stop.** Never merge, close or edit. When the owner then delegates fixing or merging, follow `references/red-and-dirty-prs.md`.

## Scheduled run
Wrap the auditor with `scripts/scheduled_sweep.py` (set `PR_SWEEP_ORG`, optionally `PR_SWEEP_WORKDIR`): output sorted by repository and number with no timestamps, a `--- STRUCTURED ---` JSON tail, and a control gate that exits non-zero with the raw output when the controls did not run. Run it by hand before scheduling it: exit 0, both controls printed, a known PR number present in the JSON tail (the key is `num`), and a count equal to the code host's own listing. The scheduled prompt restates steps 4 to 8, because a scheduled agent has no conversation to correct it, and asks for full PR links. With zero open PRs, stay silent rather than posting "nothing to report". Sweep after your own pushes too: when the red PR is yours, fix it and report the observed transition (a new run on the new head, failure to success).

## Done when
- Every open PR in scope has its three answers; every red one is named to job, step and error line.
- Every endpoint that failed is named in the report, and nothing was merged, closed or edited.

## Output standard
```
Open PRs: N — mergeable M — red R — conflicting C        (corrections to an earlier probe first)
RED: <url> — <job> / <step> — <error line>
CONFLICTING: <url> — needs a rebase | stale snapshot, recommend closing
MERGEABLE, CI TESTS: <url> — <jobs that ran> — +<added>/-<deleted>
MERGEABLE, CI PROVES NOTHING: <url> — draft | docs-only | no workflow
ORDER: <url> before <url> — <why>
CANNOT SEE: <endpoint> — HTTP <status>
```
Each PR as a full link, in merge order, with what it changes, what CI cannot prove (a mocked provider, an untested path) and what follows the merge (a deploy, and who does it). When the owner narrows the scope to one repository, answer only that one. End with a short menu of next actions and one question: the cheapest PR to handle today.

## Traps
- A dependency-bot backlog on an inactive repository without workflows: every PR is mergeable and none is proven safe, and each merge spawns replacements. Collapse it to one line.
- A deploy-preview status is a build, not tests, and a cancelled preview can still post success: read the description, never the state alone.
- A draft is the normal resting state of agent-authored content PRs: it awaits a decision, not code.
- A red dependency-bot PR may be unsatisfiable alone (peer dependencies split across sibling bumps): one coupled change, not N retries.
- "All clear" from one endpoint's silence: query a sibling endpoint first.
