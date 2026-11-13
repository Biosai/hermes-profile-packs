# Real-run verification: examples per stack

Companion to `real-run-verification`. The procedure is the same for every stack; only the ways a
runner fakes a green, and the place where a shipped change shows, differ. These are examples: for
a stack not listed, look for the same four behaviors in its runner's documentation.

## Four ways a runner reports green without running your test
| Behavior | What to look for |
|---|---|
| A cached result is replayed | the run says so, or finishes instantly |
| The filter matched nothing | zero tests ran, exit status still 0 |
| A group of tests is excluded by default | tagged, ignored or marked tests need a flag |
| A missing tool or version only warns | the warning is in the log, the exit status is 0 |

## Examples (steps 3 and 4)
- **Go**: `go test -count=1`, since `(cached)` means nothing ran. `-race` on concurrent packages.
  Tagged integration tests run only with `-tags=<tag>`. A `-run` pattern that matches nothing
  prints `ok ... [no tests to run]`: count `--- PASS`, `--- SKIP` and `--- FAIL` from `-v` or
  `-json` output.
- **Python (pytest)**: `-rs` lists every skip with its reason. A `-k` expression or a marker that
  matches nothing reports the tests as deselected and none run: read the summary line, not the
  exit status alone. Tests marked for a real dependency are often deselected by the default
  configuration.
- **JavaScript and TypeScript (Jest, Vitest and similar)**: a run configured to pass with no tests
  exits 0 when the pattern matches no file. A focused test (`.only`) left in a file silently skips
  its siblings. Package managers often only warn on an `engines` mismatch: compare the runtime
  version with the one CI pins.
- **JVM (Gradle, Maven)**: a test task reported as up to date ran nothing: force it to rerun. A
  build invoked with tests skipped is green by construction: read the command CI runs.
- **Rust (cargo)**: a filter that matches nothing prints `0 passed` with the rest `filtered out`,
  and exits 0. Tests marked `#[ignore]` are counted as ignored, not run.
- **Any validator or linter**: one that checks only the files passed to it validates nothing when
  run bare (`0 files`, exit 0). Check the count processed before the exit status.

## Is the merged change shipped? (step 10)
Compare what is actually served or published with a build of the merged tree. Per kind of
deliverable:
- **Web front end**: fetch the page with a cache-busting parameter and compare the fingerprinted
  asset names with those of the build; request the new asset path directly (a 404 means the origin
  never received it); search the served bundle for a version marker.
- **Service or API**: read the version or build-information the running service exposes and
  compare it with the merge commit; call the changed behavior once against the deployed service.
- **Package, binary or container image**: read the version, tag or digest from the registry it is
  published to and compare it with the artifact built from the merged tree.
- **Database change**: read the version table of the environment: the migration is recorded there.
- **Infrastructure**: a fresh plan against the environment shows no changes.

After each new default-branch head, run the full live suite. Post the result on that commit when
the code host supports commit statuses; a green result needs no other message. A host that posts
statuses on request heads may post nothing on default-branch merges: check the last merge commits
before treating that silence as a signal either way.

## Toolchain, baseline and report
- Read the toolchain versions CI pins from the CI definition and from the host's build
  configuration, and run on those versions.
- A baseline records the head, the mode (mocked, or real sandboxes), the counts and the expected
  SKIP set with the reason for each skip. When it changes, record why.
- Before calling a failure flaky or upstream, rerun it alone and on a clean default branch, and
  record both results.
- A post-merge failure report carries the counts, the failing tests and the developer who owns the
  change.

```
Verification — <request URL> — head <commit> — origin/<default> <commit> — <UTC time>
Scope: <packages or repositories> — mode: mocked | live — environment: <files copied>
Run: <command> — PASS a / SKIP b (baseline c; unexpected: <names>) / FAIL d
AC1: MET | NOT MET (<observed versus expected>) | NOT VERIFIABLE (<why>)
New tests fail without the change: yes | no | not checked
Verdict: VERIFIED | NOT VERIFIED (<lines>) | BLOCKED (<reason>)
```
