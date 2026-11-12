---
name: ready-to-merge-gate
description: "Decide if a change is ready to merge, with evidence"
metadata:
  hermes:
    config:
      - {key: delivery.code_host, description: "Where code is reviewed: github, gitlab, bitbucket, other, or detect", default: "detect"}
      - {key: delivery.repo_layout, description: "Repository layout: single, monorepo, multi-repo, or detect", default: "detect"}
      - {key: delivery.default_branch, description: "Default branch name, or detect", default: "detect"}
      - {key: delivery.merge_policy, description: "Who merges: owner, reviewer, or auto-when-green", default: "owner"}
    prerequisites:
      commands: [git, gh, glab]
---
# Ready-to-Merge Gate

Verifies every ready-to-merge line with evidence at the current head, before a PR (pull or merge request) is presented as finished or anyone asks for a merge. One failing line means the work is in progress.

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| Code-host CLI with read access to PRs, reviews and CI: `gh` (github), `glab` (gitlab) | threads, findings, CI | `gh auth status` / `glab auth status` |
| A clone with fetch access | conflicts, base freshness | `git fetch --dry-run` |
| Read access to the security-scanning dashboard, when the team uses one | line 1 | open the project's findings |

If a required prerequisite is missing, stop before step 1. Say which one, what it blocks, and the smallest access that would unblock it (read-only first). Do the parts that do not need it only if they still make sense alone. Never replace data you could not read with an estimate, and never report "nothing found" when the lookup failed. A line you could not check is "not checked", and the verdict is NOT READY.

## Configuration
- `delivery.code_host`: decides how you read CI. github: workflow runs by commit (`gh run list --commit <sha>`); the legacy combined-status endpoint omits Actions. gitlab: pipelines for that exact SHA through the pipelines API (`GET /projects/<id>/pipelines?sha=<sha>`, e.g. with `glab api`); a plain pipeline list is not filtered by commit. Detect from `git remote get-url origin`.
- `delivery.repo_layout`: `monorepo`: required checks and the impacted-test selection cover every affected package and its dependents. `multi-repo`: an item with several PRs is ready only when all are; list them together.
- `delivery.default_branch`: written `<default>`; detect with `git symbolic-ref --short refs/remotes/origin/HEAD`.
- `delivery.merge_policy`: who receives READY. `owner`: the owner, with `WAITING ON YOU — go to merge`. `reviewer`: the approving reviewer, who merges. `auto-when-green`: auto-merge may be turned on only after every line holds.
Current values appear in the `[Skill config]` block when the skill loads; an unset key shows its declared default. Persist a detected value with `hermes config set skills.config.<key> <value>` (per profile: `hermes -p <profile> config set …`); `hermes config migrate` prompts for keys still unset.

## Procedure
Fetch. Record the PR head SHA and the `origin/<default>` SHA. Check each line and write its evidence.
1. **Scanners resolved** on changed files, on the dashboard and in PR comments (they disagree): fixed, or dismissed with a written reason.
2. **No open review threads**, bots and outdated ones included.
3. **Tests**: the developer's impacted selection with PASS / SKIP / FAIL counts at this head; required CI green at this head. A skip from a missing credential is a FAIL; no conclusion yet is pending. Say what the green is worth: list the jobs that ran at this head and what they execute (tests; compile and lint; a validator that parses files). Zero CI runs at this head is "nothing ran", not green.
4. **QA verdict** VERIFIED against the acceptance criteria, at this head or with a later diff that cannot change the result.
5. **No conflicts**: `git merge-tree --write-tree origin/<default> <branch>`, grep CONFLICT. Never the deprecated three-argument form. A conflicting branch whose commits are already on `<default>` under other SHAs (a rebase skips every commit; the diff is nearly all deletions) is a stale snapshot: merging it deletes newer work, so the verdict is "recommend closing", never "rebase and merge".
6. **Coverage raised** by tests that exercise the new behavior.
7. **Data change declared**: "none", or the rows per environment, declared before code started or, if found later, before merge and restated after merge as an actionable note. Counts scope a data change; only the owner authorizes applying it.
8. **Migrations** numbered above the tip, unique across open PRs, proven at the production version. A renumbered migration may duplicate one already landed: diff it against the base's migrations, comments ignored.
9. **Base current**: `git rev-list --count <head>..origin/<default>` is zero when you report. After a rebase, require any new CI gate, template or definition of done to have been met.

## Output standard
```
Gate — <PR URL> — head <sha> — origin/<default> <sha> — <UTC time>
1 scanners: PASS — <evidence>
2 threads: FAIL — 2 open: <links>
...
Verdict: READY TO MERGE | NOT READY (lines 2, 7)
```
READY goes to whoever `delivery.merge_policy` names. NOT READY goes back with the failing lines.

## Traps
- A branch-filtered green can belong to a superseded base; match the SHA.
- A rollup red on every PR while `<default>` is green is usually a token that cannot read some checks; read comments and job logs.
- Never hard-code an expected PASS total; demand counts measured at this head.
- An endpoint your token cannot read answers 403 with no list; parsed as an empty list it reads as all green. Assert the HTTP status before parsing; on github a mergeable state of `unstable` with no failing check found means your probe is blind.
- `mergeable` on github is null until computed: poll it rather than reading null as either answer.
- Branch protection is unreadable without admin rights: then READY means git state plus observed CI, and the report says so.
- A deploy-preview status is a build, not tests, and a cancelled preview can post success: read its description.
- Across many PRs at once, use the `open-pr-readiness-sweep` workflow; this gate is for the one PR about to be merged.
