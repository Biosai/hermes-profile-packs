# Red and conflicting PRs: diagnosis, repair, delegated merging

Companion to `open-pr-readiness-sweep`. The sweep itself is read-only; this file is for the moment
the owner asks to "fix the conflicts", "make them green" or "merge everything", and for whoever
does that work. Merging still follows `delivery.merge_policy`, and closing a PR stays the owner's
call: recommend it with the evidence.

## Reading CI on github
| Endpoint | Needs | Shows |
|---|---|---|
| `commits/{sha}/check-runs` | the `checks` permission: 403 for many plain tokens | Checks API results |
| `commits/{sha}/status` | repository read | legacy statuses: deploy previews, external CI |
| `actions/runs?head_sha={sha}` | repository read | workflow runs and their conclusions |

One PR can have results in all three. Reading only the statuses can say "success" (a deploy
preview built) while a workflow run failed. Assert each status code: on a 403 the body has no
`check_runs` key, and `body.get("check_runs", [])` silently returns an empty, green-looking list.

| `mergeable_state` | Means |
|---|---|
| `clean` | mergeable, checks passing |
| `unstable` | mergeable, a non-required check failing |
| `blocked` | a required check or review missing |
| `dirty` | conflicts |
| `behind` | the base moved ahead |
| `unknown` | still being computed: poll again |

To name a red step: `GET /repos/{o}/{r}/actions/runs/{id}/jobs` gives each job's steps and their
conclusions; the job log endpoint answers with a redirect that must be followed without the
`Authorization` header (or use `gh run view <id> --log-failed`). A run with `startup_failure` and
zero jobs never executed anything (an unloadable workflow file or a superseded run; a very high
`run_attempt` means it was retried into the ground): push a new head and read the real run.

## A conflicting PR is one of two opposite situations
| Situation | Signature | Remedy |
|---|---|---|
| Genuine divergence | commits absent from the base; the diff adds and removes | rebase and resolve |
| Stale snapshot | commits already on the base under other SHAs; the diff is nearly all deletions | recommend closing: merging deletes newer work |

The interface shows both the same way. Three probes, in order, on a full clone (`git fetch
--unshallow` first: on a shallow clone every probe fails with "unknown revision", an error about
your clone, not the branch):
1. Rebase a scratch copy (`git checkout -B probe/<b> origin/<b> && git rebase origin/<default>`).
   `warning: skipped previously applied commit <sha>` for every commit means the branch adds nothing.
2. `git diff origin/<default> origin/<b> --shortstat`: `8 insertions(+), 4930 deletions(-)` is
   decisive. Read the few insertions: often older metadata values that would roll dates backwards.
3. Map each commit to the base by subject line, not SHA: squash merges and cherry-picks rewrite
   SHAs, so `merge-base --is-ancestor` and `git log base..branch` call merged work absent.
   `git log origin/<default> --oneline --grep="<first 50 chars of the subject>"`.

Check inclusion between open PRs the same way: a branch containing a sibling's commits makes the
sibling a strict subset, one decision rather than two. Post the evidence on the PR (the skipped
warnings, the shortstat, the subject-to-commit table) before recommending closure, and delete the
scratch branch afterwards.

A PR whose `mergeable` stays null through many polls while its siblings resolve may already be
merged: `git merge-base --is-ancestor <head> origin/<default>` returning true is proof. Leave it
open and say so.

Exception: a PR that turned conflicting while you were merging its siblings. Your merge moved the
base; that state is manufactured, not evidence of staleness. Re-run the probes against the new base.

## Merging a batch of sibling PRs (when the owner delegates it)
- Re-read `mergeable` immediately before each merge: a value from the sweep is worthless one
  merge later. Merge the widest diff first when several touch one file, so the rest reconcile once.
- Dependency bumps sharing a lockfile: merge one and the bot rebases the other itself. After a
  coupled change that reaches the target versions, wait: the bot closes superseded PRs and deletes
  their branches itself; re-read state before writing closing comments.
- Before merging a dependency-bot backlog, check the repository has workflows at all. With none,
  nothing proves a bump safe, and each merge spawns replacements.
- Report the cascade honestly: "three PRs became conflicting because my merges moved the base",
  not "three PRs have conflicts".
- A squash merge can absorb a sibling: probe by content, not subject (a squash lists absorbed
  subjects in its body). Grep the base for each surviving addition with a fixed string
  (`grep -F`), and prove the pattern fires somewhere first.
- An append-only log (a changelog, a decision or drafts log, newest first) branched before an
  intervening merge conflicts deceptively: hunks interleave across different entries, and
  resolving them one by one splices entries together while the file stays well formed. Signals:
  more conflict blocks than changes, both sides opening a hunk with a different dated heading.
  Reconstruct instead: take the base file whole, insert the branch's new entry, re-apply its few
  scalar edits, then assert every base section and table row survived and no markers remain
  before writing. Count the conflict blocks programmatically before writing any resolver.
- Push to the PR's own head ref (read it from the API), wait for the run on the new head SHA,
  then merge, and re-read `merged: true` afterwards; a 200 from the merge call is not confirmation.

## Making a red PR green
- Reproduce on the toolchain CI pins (the runtime version in the workflow and in the host's build
  config), downloading it if needed: package managers often only warn on an engines mismatch.
  Run every job the workflow runs, browser or end-to-end checks included: across a framework
  major version, a passing build proves only that it compiles.
- Run the repository's own gate script locally rather than pushing to see. A validator that only
  checks the files passed to it validates nothing when run bare (`Validated 0 file(s)`, exit 0):
  pass the changed paths and check the count before believing the exit code.
- Errors on a red PR may be transitive: a link or reference whose target reached the base through
  another PR after this branch forked. Rebase first, re-run, and only then fix what is still red;
  some of what remains may already be red on the base and unrelated to the PR.
- Markdown with wiki-style links: a link wrapped across a line break does not resolve. Keep each
  link target on one line, even past the column limit.
- Migrations: a branch cut long ago may carry a migration numbered below the base's tip. The
  numbering rule and how to renumber belong to the database engineer's `migration-verification`
  when that profile is installed; otherwise follow the repository's own migration policy. Here,
  only flag it: a request whose migration number is not above the base's tip is not mergeable.
- Ratchet allowlists (dead code, unused identifiers) fail on stale entries too. Confirm the entry
  became reachable (a real caller, or a reference by string name such as an ORM preload) before
  deleting it, and delete its orphaned justification comment. Add an entry only where the file's
  own convention allows it, citing a precedent in the same file.
- Separate the environment from the branch: when an end-to-end test fails on a dependency that is
  down (every attempt 5xx) on a PR that touches nothing near it, report the environment; read the
  test's own failure message before the diff.
- Never install a toolchain without consent just to check; say CI will be the prover.
- The deliverable is an observed transition: a new run ID on the new head going from failure to
  success. A re-run of the old run proves nothing about your fix.

## After a merge: verify the deploy, not the merge
A merged, green PR is not a shipped one. Build the merged tree on the pinned toolchain with the
host's build environment, fetch the production page with a cache-busting parameter, and compare
the fingerprinted asset names; request the new asset path directly (a real 404 proves the origin
never received it) and grep the served bundle for a version marker. A hosting provider that posts
statuses on PR heads may post nothing on default-branch merges: check the last dozen merge
commits before treating that silence as a failed deploy, and judge production from what it serves.
