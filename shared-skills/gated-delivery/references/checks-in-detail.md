# Gated delivery: the checks in detail

Companion to `gated-delivery`. The skill states the law; this file holds the detail behind each
step. "The request" is the pull or merge request; `<default>` is the default branch.

## Settings: what `detect` does
- `delivery.code_host`: read it from `git remote get-url origin`.
- `delivery.default_branch`: `git symbolic-ref --short refs/remotes/origin/HEAD`. Never assume a
  name.
- `delivery.repo_layout`: several package manifests or a workspace file at the root suggest a
  monorepo; several entries in `delivery.repos` mean multi-repo.
- `delivery.issue_tracker`: the code host's own tracker when it is enabled.
State what you detected and suggest `hermes config set skills.config.<key> <value>` (for one
profile: `hermes -p <profile> config set ...`).

## Step 1: the claim
- Look for a claim before any substantial item: a fix, a review, a migration, a test campaign, a
  refactor, a design review.
- `hermes-kanban`: the card assigned to you is the claim. Work reaches you as that card; you never
  create a card to mark, park or reserve work.
- `tracker`: take a free item by assigning it to yourself, or by a dated comment on it, before you
  start.
- `none`: there is nowhere to claim. Say so and go on.
- Confirm your own claim with a dated progress note, and link the request on it as soon as it
  exists. Never confirm another session's claim: that hides the silence the board exists to show.
- An item absent from the board may still be assigned in the tracker: a board can lag the tracker,
  so check both before treating work as free.
- An item that waits on a person's answer is not free work.
- Releasing a claim when you abandon the work is bookkeeping, not failure.

## Step 3: tests
- A skip is a test that did not run. Report the command with the counts, and whether dependencies
  were mocked or real.
- Before blaming flakiness or upstream, reproduce on a clean default branch and rerun the one
  test alone.
- Compare the SKIP count with a baseline measured at the head under test. A fresh worktree lacks
  git-ignored files (a local environment file, keys), so suites skip silently and report green.
- A green obtained with mocked dependencies is a statement about the mocks. Say which run you mean.

## Step 4: the conditions for "done"
- Do not say done, and do not ask for a merge, until every condition holds.
- Scanner findings: check every surface that reports them (the dashboard and the request's
  comments can disagree).
- Review threads: none open, bot threads and outdated ones included.
- CI: required checks green on the current head. No conclusion yet is pending.
- Conflicts: `git merge-tree --write-tree origin/<default> <branch>`, then look for `CONFLICT`. The
  deprecated three-argument form reports nothing.
- The default branch has not moved since you checked: re-check when you report. After a rebase,
  meet any gate that arrived with the new base.
- Behavior changes ship tests that raise coverage.
- When the git steward profile is installed, its `ready-to-merge-gate` is the full, evidence-backed
  version of this list.

## Step 5: merge and apply
- `delivery.merge_policy`: `owner`: only the owner merges, on an explicit go per request.
  `reviewer`: the approving human reviewer merges once the conditions hold. `auto-when-green`: the
  code host merges when required checks pass, so turning auto-merge on is the merge decision and
  the conditions must hold first. A profile never merges its own request.
- `delivery.apply_policy`: `human`: a person applies infrastructure changes. `pipeline-after-approval`:
  a pipeline applies after a recorded approval; never start it from a session and never bypass
  the approval.

## Step 6: findings
- Search item bodies, open and closed, before filing. Same root cause: add your evidence to the
  existing item. A verified finding never stays only in a conversation.

## Step 7: the report
- Link every request and work item by full URL, or by its entry in the issue file. With
  `multi-repo`, link related requests both ways.
- End every report with what you need from the owner, what is still running and when you report
  next, or that nothing is needed. Never end on "starting now".

## Shared knowledge
- A standing rule from the owner is written where the profile that follows it reads it every time,
  not left in a conversation.
- Use the terms of the project's glossary.

## Keeping tool output small
- Send logs and test runs to a file; read the tail or a count.
- Search with line numbers before reading a range of a file.
- Start a diff with its stat. Select only the JSON fields you need.
- Do not re-read what has not changed.
