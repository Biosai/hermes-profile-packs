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

Use when writing or reviewing Go service code: errors, context, goroutines, shared state, I/O, tests, modules and tooling.

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| Go toolchain at or above the `go` directive in `go.mod` | build, vet, test | `go version` against `go list -m -f '{{.GoVersion}}'` |
| The linter the repository configures, when it configures one | the lint gate | its `--version` |
| The services the integration tests expect, when you run them | integration evidence | the repository's documented check |

If one is missing, stop before step 1: say which, what it blocks, and the smallest access that unblocks it (read-only first). Never estimate data you could not read, and never report "nothing found" when the lookup failed.

## Configuration
- `delivery.repo_layout`: `monorepo`, or several modules (`go.work`, more than one `go.mod`): run build, vet, lint and tests per affected module and name each module in the evidence; `./...` from the root stops at module boundaries. `single`: run from the module root. `detect`: `find . -name go.mod -not -path '*/vendor/*'`; say what you found and suggest `hermes config set skills.config.delivery.repo_layout <value>`.

## Procedure
1. Read the repository's own conventions (contributor guide, lint configuration, agent instructions): they win where they are stricter.
2. List the modules the change touches, per `delivery.repo_layout`.
3. Write or review the code against [references/go-rules.md](references/go-rules.md): errors, context and goroutines, state and interfaces, I/O.
4. Write table-driven tests with `t.Run`, `t.Helper()` in helpers and `t.Cleanup` for teardown.
5. Run the tests as evidence: `go test -count=1`, `-race` on concurrent packages, `-tags=<tag>` for tagged integration tests, `-shuffle=on` to expose order dependence.
6. Count PASS / SKIP / FAIL from `-v` or `-json` output, not from the package summary line.
7. Run `gofmt`, `go vet ./...` and the configured linter (for example `staticcheck ./...`) with the same build tags as the tests.
8. Check the module: `go mod tidy` leaves no diff, `go.sum` is committed, no `replace` points to a local path.
9. Report per module.

## Decision rules
- Return errors; panic only for a programmer error that cannot be handled. Handle an error once: log it or return it, not both.
- Wrap with `%w` when a caller may need the cause: `errors.Is` fails silently through a layer that wrapped with `%v`.
- `ctx` is the first parameter of anything that does I/O or blocks. A goroutine started in a handler without the request's cancellation outlives the client.
- Every goroutine has an owner and an exit path. Work that must outlive the request is detached on purpose, with its own timeout and a comment saying why.
- `(cached)` means nothing ran. A `-run` pattern that matches nothing still prints `ok` with `[no tests to run]`.
- Tests behind a build tag are silently excluded without `-tags`, and unlinted when the linter runs without it.
- A linter that errors is a FAIL.
- Raw SQL strings are invisible to the compiler: search for each column a migration renames or drops.

## Quality gate
The work is ready when the pull or merge request gives, per module, the commands run (with `-count=1`, `-race` and tags), the PASS / SKIP / FAIL counts at the head commit, clean `gofmt`, `go vet` and linter results, and which rules of the reference the change touched.
