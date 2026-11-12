---
name: real-run-verification
description: "Verify a done claim with real runs and counted results"
metadata:
  hermes:
    config:
      - {key: delivery.code_host, description: "Where code is reviewed: github, gitlab, bitbucket, other, or detect", default: "detect"}
      - {key: delivery.repo_layout, description: "Repository layout: single, monorepo, multi-repo, or detect", default: "detect"}
      - {key: delivery.default_branch, description: "Default branch name, or detect", default: "detect"}
      - {key: delivery.board, description: "Where work is claimed: hermes-kanban, tracker, or none", default: "none"}
      - {key: delivery.issue_tracker, description: "Where work items go: github, gitlab, jira, linear, file, none, or detect", default: "detect"}
    prerequisites:
      commands: [git, gh, glab, go]
---
# Real-Run Verification

Verifies a done claim, or runs a campaign others will rely on, so every result carries PASS / SKIP / FAIL counts checked against a measured baseline. Default posture: disbelief. A claim without a run you executed at the current head is unverified, including your own runs at an older head.

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| A clone with fetch access, and a worktree you own | run at the exact head | `git fetch --dry-run` |
| The git-ignored files and services the suite needs (local env, keys, containers) | a run that does not skip silently | the suite's own setup check, then the SKIP count |
| Code-host CLI with read access: `gh` (github), `glab` (gitlab) | PR head, CI results | `gh auth status` / `glab auth status` |
| Real vendor sandbox credentials, only for a live-mode run | live evidence | the suite's live-mode check |

If a required prerequisite is missing, stop before step 1. Say which one, what it blocks, and the smallest access that would unblock it (read-only first). Do the parts that do not need it only if they still make sense alone. Never replace data you could not read with an estimate, and never report "nothing found" when the lookup failed. A run without its credentials is reported as not run, never as green.

## Configuration
- `delivery.code_host`: how you read the PR head and CI (for example `gh pr view N --json headRefOid`, `glab mr view N`). Detect from `git remote get-url origin`.
- `delivery.repo_layout`: `monorepo`: run the affected packages' suites plus their dependents, and say which packages you covered. `multi-repo`: pin one SHA per repository involved.
- `delivery.default_branch`: the clean ref for comparison runs; detect with `git symbolic-ref --short refs/remotes/origin/HEAD`.
- `delivery.board`: claim the verification (`hermes-kanban` card, `tracker` assignment), or skip and say so (`none`).
- `delivery.issue_tracker`: where a post-merge regression goes; `none` keeps it in your report.
Current values appear in the `[Skill config]` block when the skill loads; an unset key shows its declared default. Persist a detected value with `hermes config set skills.config.<key> <value>` (per profile: `hermes -p <profile> config set …`); `hermes config migrate` prompts for keys still unset.

## Procedure
1. **Claim** per `delivery.board`. If another session holds it, stop and say who.
2. **Pin** the PR head SHA and the `origin/<default>` SHA; everything you report is about these.
3. **Prepare your own worktree** and copy in the git-ignored files with tight permissions. Use the repository's own test entry point (script or make target), not a bare runner, on the toolchain versions CI pins (read them from the CI file and the host's build config): package managers often only warn on an engines mismatch.
4. **Send output to a file**; compute counts from the log.
5. **Read SKIP before PASS.** Compare with the baseline for this head and mode; list unexpected skips. A skip from a missing credential is a FAIL; more skips than baseline means a broken environment.
6. **Check each acceptance criterion**, beyond the happy path: empty, missing, duplicate, concurrent, unauthorized, dependency failing.
7. **Check the new tests test**: revert the change locally and confirm they fail by name; for a fix with several ways to be undone, run the `mutation-proof` workflow.
8. **Before calling a failure flaky or upstream**, rerun it alone and on a clean `origin/<default>`; record both.
9. **Say which mode ran**: mocked, or real vendor sandboxes.
10. **Record baselines**: head SHA, mode, counts, expected SKIP set with reasons; record why when it changes.

## Go suites
`go test -count=1` (`(cached)` means nothing ran); `-race` on concurrent packages; tagged integration tests run only with `-tags=<tag>`; a `-run` pattern matching nothing prints `ok ... [no tests to run]`, so count `--- PASS/SKIP/FAIL` from `-v` or `-json`.

## Post-merge live run
On each new default-branch head: the full live suite, result posted on that commit when the code host supports commit statuses, silent when green. On failure: counts and failing tests, recorded per `delivery.issue_tracker`, owning developer named. Fix forward; never revert automatically.
A merged change is not a shipped one. Compare what production serves with a build of the merged tree: fingerprinted asset names fetched with a cache-busting parameter, the new asset path requested directly (a 404 means the origin never received it), a version marker grepped from the served bundle. A host that posts no status on default-branch merges proves nothing by its silence.

## Output standard
```
Verification — <PR URL> — head <sha> — origin/<default> <sha> — <UTC time>
Scope: <packages or repos> — mode: mocked | live — env: <files copied>
Run: <command> — PASS a / SKIP b (baseline c; unexpected: <names>) / FAIL d
AC1: MET | NOT MET (<observed vs expected>) | NOT VERIFIABLE (<why>)
New tests fail without the change: yes | no | not checked
Verdict: VERIFIED | NOT VERIFIED (<lines>) | BLOCKED (<reason>)
```

## Traps
- Re-reading the developer's numbers is not verification.
- A baseline remembered from weeks ago is wrong; suites grow with every merge.
- A background run you never read back did not happen.
- A validator that checks only the files passed to it validates nothing when run bare (`0 files`, exit 0): check the count processed before the exit code.
- A CI fix is proven by an observed transition: a new run ID on the new head, failure then success. Re-running the old run proves nothing.
