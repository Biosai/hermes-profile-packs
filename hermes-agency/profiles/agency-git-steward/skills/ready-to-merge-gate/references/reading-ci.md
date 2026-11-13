# Reading CI and merge state for one commit

Companion to `ready-to-merge-gate`. A green is evidence about one commit: every command below is
filtered by the head commit, never by the branch name, because a branch-filtered green can belong
to a superseded base.

## Per `delivery.code_host`
**github**
- List workflow runs by commit: `gh run list --commit <sha>`. The legacy combined-status endpoint
  omits workflow runs, and check runs may attach to the request ref rather than the branch commit.
- An endpoint your token cannot read answers 403 with no list; parsed as an empty list it reads as
  all green. Assert the HTTP status before parsing.
- `mergeable` is null until computed: poll it rather than reading null as either answer.
- A mergeable state of `unstable` with no failing check found means your probe is blind, not that
  the request is clean.
- A rollup that is red on every request while the default branch is green is usually a token that
  cannot read some checks: read the request's comments and the job logs.

**gitlab**
- Read pipelines for the exact commit through the pipelines API
  (`GET /projects/<id>/pipelines?sha=<sha>`, for example with `glab api`). A plain pipeline list
  is not filtered by commit.

**Any other host**
- Use its own CLI or web UI, filter by the head commit, and write in the report which checks were
  read by hand.

## On every host
- An opaque red: the reason is usually in the request's review and conversation comments and in
  the failing job's log. Read them all before saying you cannot see it.
- Branch protection is often readable only with admin rights. Without them, READY means git state
  plus observed CI, and the report says so.
- A deploy-preview status is a build, not tests, and a cancelled preview can still post success:
  read its description, never the state alone.
- Say what the green is worth: list the jobs that ran at this head and what each executes (tests;
  compile and lint; a validator that parses files). Zero runs at this head is "nothing ran".

## Conflicts
- `git merge-tree --write-tree origin/<default> <branch>`, then search the output for `CONFLICT`.
  The deprecated three-argument form reports nothing.

## Report format
```
Gate — <request URL> — head <sha> — origin/<default> <sha> — <UTC time>
Scanners: PASS — <evidence>
Threads: FAIL — 2 open: <links>
Tests / Verification / Conflicts / Coverage / Data change / Migration / Base: ...
Verdict: READY TO MERGE | NOT READY (<failing lines>)
```
