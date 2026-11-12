---
name: fresh-main-evidence
description: "Cite code from a fresh default branch at a pinned SHA"
metadata:
  hermes:
    config:
      - {key: delivery.code_host, description: "Where code is reviewed: github, gitlab, bitbucket, other, or detect", default: "detect"}
      - {key: delivery.repo_layout, description: "Repository layout: single, monorepo, multi-repo, or detect", default: "detect"}
      - {key: delivery.repos, description: "Working copies this profile may read or change (paths or URLs, comma-separated)", default: ""}
      - {key: delivery.default_branch, description: "Default branch name, or detect", default: "detect"}
    prerequisites:
      commands: [git, gh, glab]
---
# Fresh-Branch Evidence

Gathers evidence about what code contains from a freshly fetched default branch, cites `path:line @ <sha>`, and confirms absences with two sources. Use it before a review, a readiness verdict, a duplicate check, a work item that cites code, or any sentence of the form "X does / does not exist". Shared checkouts drift: a stale worktree once produced a confident "this does not exist" about code that did.

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| A clone of each repository in scope, with fetch access | read the current ref | `git fetch --dry-run` |
| Code search on the code host, for negative claims: `gh` (github), `glab` (gitlab), or its web search | the second source | one search returns results |

If a required prerequisite is missing, stop before step 1. Say which one, what it blocks, and the smallest access that would unblock it (read-only first). Do the parts that do not need it only if they still make sense alone. Never replace data you could not read with an estimate, and never report "nothing found" when the lookup failed. Without a second source, every absence is labeled single-source.

## Configuration
- `delivery.default_branch`: written `<default>`; detect with `git symbolic-ref --short refs/remotes/origin/HEAD`. Never assume `main`.
- `delivery.code_host`: decides the permalink format (`/blob/<sha>/path#L10` on github, `/-/blob/<sha>/path#L10` on gitlab) and the code search (`gh search code`, the gitlab search API). Detect from `git remote get-url origin`.
- `delivery.repo_layout`, `delivery.repos`: `multi-repo`: fetch and pin each repository in `delivery.repos` and cite `repo:path:line @ <sha>`; an absence holds only across all of them. `monorepo`: scope searches to the relevant packages, then widen once before claiming an absence.
Current values appear in the `[Skill config]` block when the skill loads; an unset key shows its declared default. Persist a detected value with `hermes config set skills.config.<key> <value>` (per profile: `hermes -p <profile> config set …`); `hermes config migrate` prompts for keys still unset.

## Procedure
1. **Fetch, then pin.** `git fetch --all --prune`; record `origin/<default> @ <sha>` per repository.
2. **Search the ref, not the worktree**: `git grep -n <pattern> origin/<default> -- <paths>`, `git show origin/<default>:<file>` (read a range), `git ls-tree -r --name-only origin/<default> -- <dir>`, `git log --oneline -n 20 origin/<default> -- <path>`.
3. **Leave shared checkouts alone**: fetch only; never pull, checkout, stash or edit. Report a checkout's distance with `git rev-list --count HEAD..origin/<default>` when it matters.
4. **Cite every positive claim** as `path:line @ <sha>` with a permalink at that SHA. Counts over adjectives: "three call sites write this table".
5. **Back every negative claim with two independent sources**: a ref search plus code-host search, or a ref search plus a runtime observation (a log, an API response). Search synonyms and the glossary's term too. With one source: "found no X in origin/<default> @ <sha> (single-source check)".
6. **Label verified versus claimed**: "verified at the SHA" and "stated by the work item or PR description" are different statements.
7. **Re-check when you report** if time passed; the branch may have moved.

## Verify tool output before you believe it
- A search that returns nothing may have failed, timed out, or not indexed the branch; an empty result is not an absence until a second source agrees.
- Some APIs answer HTTP 200 with an `errors` field; read the body.
- A green filtered by branch can belong to a superseded base; green is evidence about one SHA.

## Output standard
```
Evidence — origin/<default> @ <sha> (per repo) — <UTC time>
Claim: <statement> — <path:line @ sha> (<permalink>)
Absence: no <X> — sources: ref grep (<pattern>) + <second source> | single-source check
Not verified: <list>
```

## Traps
- Grepping a worktree behind the default branch and reporting it as a fact about the repository.
- One grep with one spelling as proof that nothing uses a concept.
- A permalink to a branch name that points at a different line next week.
