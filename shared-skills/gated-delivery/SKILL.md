---
name: gated-delivery
description: "Deliver repo work via claim, real tests, gate and merge"
metadata:
  hermes:
    config:
      - {key: delivery.code_host, description: "Where code is reviewed: github, gitlab, bitbucket, other, or detect", default: "detect"}
      - {key: delivery.repo_layout, description: "Repository layout: single, monorepo, multi-repo, or detect", default: "detect"}
      - {key: delivery.default_branch, description: "Default branch name, or detect", default: "detect"}
      - {key: delivery.issue_tracker, description: "Where work items go: github, gitlab, jira, linear, file, none, or detect", default: "detect"}
      - {key: delivery.issue_file, description: "Markdown file for work items when the tracker is file", default: ""}
      - {key: delivery.board, description: "Where work is claimed: hermes-kanban, tracker, or none", default: "none"}
      - {key: delivery.merge_policy, description: "Who merges: owner, reviewer, or auto-when-green", default: "owner"}
      - {key: delivery.apply_policy, description: "Who applies infrastructure changes: human or pipeline-after-approval", default: "human"}
      - {key: owner.channel, description: "Where questions and owner actions reach the owner", default: "this conversation"}
    prerequisites:
      commands: [git, gh, glab, hermes]
---
# Gated Delivery

The operating law for repository work where humans keep the merge and apply decisions and agents prove their work. Load it before starting any work item. Each rule was learned from a failure; its reason lets you apply it where its letter does not reach. "The owner" is the person who decides technical questions and holds the merge and apply authority the settings below do not delegate. "PR" means pull or merge request, per the code host.

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| A clone of each repository in scope, with fetch access | evidence from a fresh default branch | `git fetch --dry-run` |
| Code-host CLI, authenticated with read access: `gh` (github), `glab` (gitlab) | PR, review and CI state | `gh auth status` / `glab auth status` |
| `hermes` CLI, when `delivery.board` is `hermes-kanban` | claims | `hermes kanban boards list` |

If a required prerequisite is missing, stop before step 1. Say which one, what it blocks, and the smallest access that would unblock it (read-only first). Do the parts that do not need it only if they still make sense alone. Never replace data you could not read with an estimate, and never report "nothing found" when the lookup failed.

## Configuration
Current values appear in the `[Skill config]` block when this skill loads; an unset key shows its declared default, so `detect` reads as "detect". For `detect`, detect the value, state what you detected, and suggest `hermes config set skills.config.<key> <value>` (per profile: `hermes -p <profile> config set …`) to make it permanent; `hermes config migrate` prompts for keys still unset. Never fall back silently to one team's habit.
- `delivery.code_host`: decides the CLI and the words. Detect from `git remote get-url origin`.
- `delivery.repo_layout`: `monorepo` scopes every change, test run, CI filter and piece of evidence to the affected packages; `multi-repo` pins one SHA per repository and links related PRs both ways. Detect from workspace files (several package manifests or a workspace file at the root) or from `delivery.repos`.
- `delivery.default_branch`: written `<default>` below. Detect with `git symbolic-ref --short refs/remotes/origin/HEAD`. Never assume `main`.
- `delivery.issue_tracker` / `delivery.issue_file`: where findings go. `file`: append to the named file. `none`: findings stay in your report.
- `delivery.board`: `hermes-kanban` (a board named `coordination` by convention), `tracker` (assign the work item and comment), `none` (skip claim steps and say so).
- `delivery.merge_policy`: `owner`: only the owner merges, on an explicit go per PR. `reviewer`: the approving human reviewer merges once the gate holds. `auto-when-green`: the code host merges when required checks pass, so turning auto-merge on is the merge decision and the gate must hold first. A profile never merges its own PR.
- `delivery.apply_policy`: `human`: a human applies infrastructure; you never do. `pipeline-after-approval`: a pipeline applies after a recorded approval; you never apply from a session and never bypass the approval.
- `owner.channel`: where every question and ask goes.

## 1. Claim before you start
Several sessions share the same repositories; duplicated work is pure waste. Before any substantial item (fix, review, migration, test campaign, refactor, design review), look for a claim where `delivery.board` says. With `none`, skip this section and say so.
- Claimed with recent activity: do not touch it; tell the owner which session holds it. Claimed but stale: still do not take it over; point the owner at the claiming session.
- Never pick an item parked as waiting on a human. An item missing from the board is not "no free work": the board mirrors the tracker and lags it, so add the item, then claim it.
- Unclaimed: claim it first, with `session: <name> — started <UTC time>`. On Hermes Kanban, park the card as blocked at once: a dispatchable claim gets picked up by a worker and the work runs twice.
- Confirm your own claims with a dated progress comment, never another session's: refreshing someone else's claim hides the silence the board exists to show. Link the PR on the claim as soon as it exists.
- Complete only against proof: the change merged on `<default>` and the work item closed; otherwise it waits in a verify state. Completing frees the claim. Release with a one-line reason when you abandon: bookkeeping, not failure.

## 2. Testing means the real thing, with numbers
- Report PASS / SKIP / FAIL counts, never "tests pass". A skip is a test that did not run; a skip from a missing credential or local file is a FAIL.
- Compare SKIP with a baseline measured at the head under test. A fresh worktree lacks git-ignored files (local env, keys) and suites then skip silently and report green.
- Mock-only green is a claim about the mocks. Say which run you mean.
- Before blaming upstream or flakiness, reproduce on a clean `<default>` and rerun the single test in isolation.
- A reviewer, linter or validator that errors is a FAIL, never a pass.

## 3. "Done" means ready to merge, all of it
Do not say done, and do not ask for a merge, until every line holds:
1. Security and code-scanning findings on changed files are fixed or dismissed with a reason, on every surface (dashboards and PR comments disagree).
2. No open review threads, bots and outdated ones included.
3. Impacted tests ran with counts; required CI is green on the current head. No conclusion yet means pending.
4. No conflicts: `git merge-tree --write-tree origin/<default> <branch>`, then look for CONFLICT. The deprecated three-argument form reports nothing.
5. Behavior changes ship tests that raise coverage.
6. Changes to existing data rows are declared in writing before merge.
7. `<default>` has not moved since you verified, re-checked when you report; after a rebase, run any new gate.

## 4. Merge and apply follow the settings
Merge only as `delivery.merge_policy` allows; apply only as `delivery.apply_policy` allows. Never change production data or cloud resources by hand. A standing exception exists only in writing from the owner, with an exact scope.

## 5. Evidence comes from a fresh default branch
Shared checkouts drift: a stale worktree once produced a confident "this does not exist" about code that did. Fetch, search the ref (`git grep -n <pattern> origin/<default> -- <paths>`), cite `path:line @ <sha>` with a permalink at that SHA. A negative claim needs two sources. Never pull, checkout, stash or edit in a checkout another session uses; work in your own worktree.

## 6. Verify tool output before you believe it
- A branch-filtered green can belong to a superseded base: green is evidence about one SHA.
- Some APIs answer HTTP 200 with an `errors` field; read the body.
- An opaque red: the reason is usually in the PR's review and conversation comments and the failing job's log. Read them all before saying you cannot see it.
- On github: the legacy combined-status endpoint omits Actions, and check runs may attach to the PR ref, not the branch SHA. List workflow runs by commit (`gh run list --commit <sha>`). A rollup red on every PR while `<default>` is green is usually a token that cannot read some app checks.

## 7. Check migration numbering at the tip
A tool that tracks one version number silently skips a migration numbered below the tip, and CI cannot see it because CI migrates from empty. Compare with the tip on `origin/<default>`, every open PR, and the deployed version; prove it applies at the production version. Raw SQL is invisible to the compiler.

## 8. Report so the owner never has to ask
- Link every PR and work item by full URL (or file entry id). A status is read from its source when you write it, never from memory.
- Numbers over adjectives; verified versus claimed. A check that could not run is "skipped", never "clean".
- End every turn with one of `WAITING ON YOU — <exact ask>`, `STILL BUSY — <what runs, next report>`, `NOTHING NEEDED FROM YOU — <why>`. Never end on "starting now".

## 9. Keep shared knowledge true
Code wins: fix documents that disagree, in the same delivery. A standing rule from the owner goes into the SOUL that follows it. Use the glossary's terms. No secret values in PRs, work items, chat or logs.
A verified finding you will not fix in this turn becomes a work item where `delivery.issue_tracker` says, never only a chat line: search item bodies, open and closed, first; same root cause, add your evidence to the existing item.

## 10. Keep tool output small
Logs and test runs go to a file; read `tail` or `grep -c`. `grep -n` before reading a range. Diffs start with `--stat`. Select JSON fields. Never re-read what has not changed.
