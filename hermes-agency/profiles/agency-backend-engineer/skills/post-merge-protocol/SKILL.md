---
name: post-merge-protocol
description: "Clean up and update docs after your change merges"
metadata:
  hermes:
    config:
      - {key: delivery.code_host, description: "Where code is reviewed: github, gitlab, bitbucket, other, or detect", default: "detect"}
      - {key: delivery.repo_layout, description: "Repository layout: single, monorepo, multi-repo, or detect", default: "detect"}
      - {key: delivery.repos, description: "Working copies this profile may read or change (paths or URLs, comma-separated)", default: ""}
      - {key: delivery.issue_tracker, description: "Where work items go: github, gitlab, jira, linear, file, none, or detect", default: "detect"}
      - {key: delivery.issue_file, description: "Markdown file for work items when the tracker is file", default: ""}
      - {key: delivery.board, description: "Where work is claimed: hermes-kanban, tracker, or none", default: "none"}
    prerequisites:
      commands: [git, gh, glab, hermes]
---
# Post-Merge Protocol

Cleans up, gets the downstream counterpart recorded, updates every knowledge target, and releases the claim. Use it unprompted on every merge of a PR (pull or merge request) you own, whether told or detected; if a scheduled run may have done it, check first.

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| Code-host CLI with read access: `gh` (github), `glab` (gitlab) | confirm the merge and its merged diff | `gh auth status` / `glab auth status` |
| Write access to the knowledge or docs repositories, to open PRs | knowledge updates | `git push --dry-run` on a scratch branch |
| Tracker access, unless `delivery.issue_tracker` is `none` | the counterpart item | open any item |
| `hermes` CLI, when `delivery.board` is `hermes-kanban` | release the claim | `hermes kanban boards list` |

If a required prerequisite is missing, stop before step 1. Say which one, what it blocks, and the smallest access that would unblock it (read-only first). Do the parts that do not need it only if they still make sense alone. Never replace data you could not read with an estimate, and never report "nothing found" when the lookup failed.

## Configuration
- `delivery.code_host`: how you confirm the merge (for example `gh pr view N --json state,mergeCommit` or `glab mr view N`). Detect from `git remote get-url origin`.
- `delivery.repo_layout`, `delivery.repos`: `multi-repo`: run the protocol when every PR of the item has merged, across all repositories in `delivery.repos`; the counterpart may belong to another repository. `monorepo`: the counterpart and docs may live in another package of the same repository.
- `delivery.issue_tracker`, `delivery.issue_file`: where the counterpart is recorded. `file`: append it to the file. `none`: put the full counterpart text in your report for the owner.
- `delivery.board`: `hermes-kanban`: complete the card with a summary. `tracker`: comment and move the item to its done state. `none`: skip, and say so.
Current values appear in the `[Skill config]` block when the skill loads; an unset key shows its declared default. Persist a detected value with `hermes config set skills.config.<key> <value>` (per profile: `hermes -p <profile> config set …`); `hermes config migrate` prompts for keys still unset.

## Procedure
0. **Clean up first.** Stop the item's test runs (match processes by working directory, never by a command-line pattern that also matches other sessions), start no new local end-to-end run after the merge (CI and post-merge runs cover it), take the local stack down, remove scratch files.
1. **Downstream counterpart.** If a consumer can observe the change (endpoint, contract, field, status code, user-visible behavior), record a counterpart item for the consumer with the shipped contract (paths, methods, payloads, status codes, error bodies, auth, idempotency) and the product answers collected up front, linked both ways. If the team files through one owner, hand it the text. If there is none, say "no counterpart, nothing filed": silence must never mean either.
2. **Knowledge targets, all four considered, each reported updated or skipped with a reason:** the knowledge base (by stable concept id), the team's shared skills, the repository's own docs (flow index, API docs, decision records, migration notes), and your profile memory. Updates go through PRs written from the merged diff, not the description.
3. **Planning state**: the item moves to done now, not before.
4. **Release the claim** once the follow-up PRs are open; do not wait for their merges. Unmerged work PRs still hold it.
5. **Report.**

## Output standard
```
Post-merge — <merged PR URL>
Cleanup: runs stopped n, stack down, scratch removed
Counterpart: <item URL or file entry> | text in report (tracker none) | no counterpart, nothing filed
Knowledge base / Shared skills / Repo docs: <PR URL> | skipped — <reason>
Memory: updated | skipped — <reason>
Claim: completed | board none, skipped
```
End with `WAITING ON YOU — review <follow-up PR URLs>` or `NOTHING NEEDED FROM YOU`.

## Traps
- A local end-to-end run after the merge burns the machine for a result CI already has.
- A knowledge PR describing intent rather than what merged.
- Keeping the claim open until the follow-up PRs merge blocks the next task.
