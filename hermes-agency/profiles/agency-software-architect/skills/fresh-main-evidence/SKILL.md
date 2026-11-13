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

Use when a statement about what the code contains, or does not contain, will be relied on: a review, a readiness verdict, a duplicate check, a work item that cites code.

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| A clone of each repository in scope, with fetch access | read the current ref | `git fetch --dry-run` |
| Code search on the code host, for negative claims | the second source | a search returns a known result |

If one is missing, stop before step 1: say which, what it blocks, and the smallest access that unblocks it (read-only first). Never estimate data you could not read, and never report "nothing found" when the lookup failed. Without a second source, every absence is labeled single-source.

## Configuration
- `delivery.default_branch`: `<default>` below. Detect with `git symbolic-ref --short refs/remotes/origin/HEAD`; never assume a name.
- `delivery.code_host`: the permalink format and the code search. github: `/blob/<sha>/<path>#L10`, `gh search code`; gitlab: `/-/blob/<sha>/<path>#L10`, its search API through `glab api`; any other host: its own permalink form and web search. Detect from `git remote get-url origin`.
- `delivery.repo_layout`, `delivery.repos`: `multi-repo`: fetch and pin each repository in `delivery.repos` and cite `repo:path:line @ <sha>`; an absence holds only across all of them. `monorepo`: scope searches to the relevant packages, then widen once before claiming an absence.

## Procedure
1. Fetch, then pin: `git fetch --all --prune`; record `origin/<default> @ <sha>` per repository.
2. Search the ref, not the working copy: `git grep -n <pattern> origin/<default> -- <paths>`, `git show origin/<default>:<file>`, `git ls-tree -r --name-only origin/<default> -- <dir>`, `git log --oneline -n 20 origin/<default> -- <path>`.
3. Cite every positive claim as `path:line @ <sha>`, with a permalink at that commit, and count: "three call sites write this table".
4. Back every negative claim with two independent sources: a ref search plus the code host's search, or a ref search plus a runtime observation (a log, an API response). Search synonyms and the glossary's term too.
5. Label each statement: verified at the commit, or stated by a work item or a request description.
6. Re-check the commit when you report, if time has passed: the branch may have moved.

## Decision rules
- This is the home of the rule: what the code contains is stated from a freshly fetched default branch at a pinned commit, never from a working copy, which may be behind.
- In a checkout another session uses, fetch only: never pull, switch branches, stash or edit. Report its distance with `git rev-list --count HEAD..origin/<default>` when it matters.
- With one source, write "found no X in origin/<default> @ <sha> (single-source check)".
- An empty search result is not an absence: the search may have failed, timed out or not indexed the branch.
- One search with one spelling does not prove that nothing uses a concept.
- A permalink to a branch name points at a different line later: link the commit.
- Check tool output before relying on it. A green is evidence about one commit and may belong to a superseded base. Some APIs answer success with an `errors` field in the body: read the body. The reason for an opaque red is usually in the request's comments and the failing job's log: read them before saying you cannot see it.

## Quality gate
The evidence is complete when the report gives the pinned commit per repository and the time; each claim with `path:line @ <sha>` and its permalink; each absence with its two sources, or marked single-source; and the list of what was not verified.
