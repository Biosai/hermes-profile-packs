---
name: go-backend-craft
description: "Write and review Go backend code that stays correct"
metadata:
  hermes:
    config:
      - {key: delivery.repo_layout, description: "Repository layout: single, monorepo, multi-repo, or detect", default: "detect"}
    prerequisites:
      commands: [go, gofmt, git, staticcheck]
---
# Go Backend Craft

Error, context, concurrency, testing, module and tooling practices for Go services. Read the repository's own conventions first (contributor guide, lint configuration, agent instructions); they win where they are stricter.

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| Go toolchain at or above the `go` directive in `go.mod` | build, vet, test | `go version` vs `go list -m -f '{{.GoVersion}}'` |
| The linter the repository configures, when it configures one | lint gate | its `--version` |
| Services the integration tests expect, when you run them | integration evidence | the repository's documented check |

If a required prerequisite is missing, stop before step 1. Say which one, what it blocks, and the smallest access that would unblock it (read-only first). Do the parts that do not need it only if they still make sense alone. Never replace data you could not read with an estimate, and never report "nothing found" when the lookup failed.

## Configuration
- `delivery.repo_layout`: `monorepo` or several modules (`go.work`, more than one `go.mod`): run build, vet, lint and tests per affected module, and name each module in the evidence; `./...` from the root stops at module boundaries. `single`: run from the module root. Detect with `find . -name go.mod -not -path '*/vendor/*'`; state the result and suggest `hermes config set skills.config.delivery.repo_layout <value>` (per profile: `hermes -p <profile> config set …`).

## Errors
1. Return errors; panic only for programmer errors that cannot be handled.
2. Wrap with context where a layer adds meaning: `fmt.Errorf("load account %s: %w", id, err)`. Use `%w`, not `%v`, when callers may need the cause.
3. Check causes with `errors.Is` (sentinels such as `sql.ErrNoRows`) and `errors.As` (typed errors), never by comparing messages.
4. Handle an error once: log it or return it, not both.
5. Map errors to responses at one boundary, by cause; a dependency failure must not surface as "invalid input".

## Context and goroutines
1. `ctx context.Context` is the first parameter of anything that does I/O or blocks; pass the request's context to every database call and outbound request (`http.NewRequestWithContext`).
2. Never store a context in a struct; never call `context.Background()` in a request path.
3. `defer cancel()` right after `context.WithTimeout` or `WithCancel`.
4. Work that must outlive the request is detached on purpose, with its own timeout and a comment saying why.
5. Every goroutine has an owner and an exit path; select on `ctx.Done()` around sends and receives that may never complete.
6. Wait for what you start: `sync.WaitGroup` (`Add` before `go`) or `errgroup` to propagate the first error and cancel the rest. Bound concurrency. Only the sender closes a channel.

## State, interfaces, I/O
1. No package-level mutable state and no `init()` side effects; inject dependencies.
2. Maps are not safe for concurrent writes; guard or confine shared state; run `go test -race` on concurrent packages.
3. Small interfaces defined at the consumer; accept interfaces, return concrete types; no interface exported only for mocking.
4. `defer resp.Body.Close()`, `defer rows.Close()`, then check `rows.Err()`; `defer tx.Rollback()` after `Begin` (a no-op after `Commit`).
5. Outbound HTTP uses a client with an explicit timeout; the default client has none.
6. Raw SQL strings are invisible to the compiler: grep for each column a migration renames or drops.

## Tests
1. Table-driven tests with `t.Run`; `t.Helper()` in helpers; `t.Cleanup` for teardown.
2. Integration tests behind a build tag (`//go:build integration`) run only with `-tags=integration`; without it they are silently excluded.
3. `go test -count=1` when the result is evidence: `(cached)` means nothing ran.
4. A `-run` pattern that matches nothing still prints `ok` with `[no tests to run]`; confirm the intended tests ran (`-v` or `-json`).
5. `-shuffle=on` exposes order dependence.
6. Count PASS / SKIP / FAIL from `-v` or `-json` output, not the package summary line.

## Modules and tooling
1. `go mod tidy` leaves no diff; `go.sum` is committed; no committed `replace` to a local path.
2. `gofmt` clean, `go vet ./...`, and the configured linter (for example `staticcheck ./...`) with the same build tags as the tests, or tagged files go unlinted. A linter that errors is a FAIL.

## Output standard
In the PR: per module, the commands run (with `-count=1`, `-race`, tags), PASS / SKIP / FAIL counts at the head SHA, and which rules above the change touched.

## Traps
- Green from `go test ./...` when the relevant tests sit behind a tag you did not pass.
- A goroutine started in a handler without the request's cancellation outlives the client.
- `errors.Is` fails silently when a layer wrapped with `%v`.
