---
name: post-merge-kb-update
description: "Update knowledge and skills to match merged code"
metadata:
  hermes:
    config:
      - {key: delivery.code_host, description: "Where code is reviewed: github, gitlab, bitbucket, other, or detect", default: "detect"}
      - {key: delivery.repo_layout, description: "Repository layout: single, monorepo, multi-repo, or detect", default: "detect"}
      - {key: delivery.repos, description: "Working copies this profile may read or change (paths or URLs, comma-separated)", default: ""}
      - {key: delivery.default_branch, description: "Default branch name, or detect", default: "detect"}
      - {key: delivery.merge_policy, description: "Who merges: owner, reviewer, or auto-when-green", default: "owner"}
    prerequisites:
      commands: [git, gh, glab]
---
# Post-Merge Knowledge Update

Use when code has merged and the knowledge base, glossary or shared skills must be made true to it, or when a knowledge change someone else wrote after a merge needs review.

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| Read access to the code host | the merged diff and its state | github: `gh auth status`; gitlab: `glab auth status` |
| A clone of the code repositories, with fetch access | check every claim against code | `git fetch --dry-run` |
| Push access to branches of the knowledge repositories | open the update | `git push --dry-run` on a scratch branch |
| The knowledge repository's validator, when it has one | links, frontmatter, ids | run it on the current head |

If one is missing, stop before step 1 and say which, what it blocks, and the smallest access that would unblock it (read-only first). Never replace code you could not read with a description of it, and never report "nothing to update" when the lookup failed.

## Configuration
- `delivery.code_host`: how the merged diff is read (github: `gh pr diff <n>`; gitlab: `glab mr diff <n>`; another host: its own CLI or web UI, saying what was done by hand).
- `delivery.repo_layout` and `delivery.repos`: where the knowledge lives. `monorepo`: docs and skills may be folders of the code repository, and one change carries them. `multi-repo`: one change per knowledge repository in `delivery.repos`, each linking the merged code change.
- `delivery.default_branch`: claims are checked there, freshly fetched.
- `delivery.merge_policy`: who merges knowledge changes, as in `gated-delivery`. You never merge your own.
- For `detect`, say what was detected and suggest `hermes config set skills.config.<key> <value>`.

## Procedure
1. Read the merged diff, not its description: every concept, enum value, status, field, endpoint, default, limit and flow it adds, changes or removes.
2. Pin the default branch at its commit after the merge.
3. Find every description of each concept: the knowledge base by stable id, shared skills, the repository's docs. Search the glossary term and its known synonyms.
4. Per target, update, or skip with a reason.
5. Update by id. Quote values exactly as in code, link the merged change, cite `path:line @ <commit>`, and mark what is verified versus intended.
6. Run the validator on a fresh export. An error is a FAIL.
7. Open a pull or merge request titled `<concept>: <what changed> (after <merged change link>)`. Never push directly to a shared branch.
8. To review someone else's knowledge change, follow [the review checklist](references/review-a-knowledge-change.md), and merge only as `delivery.merge_policy` allows.

## Decision rules
- Code wins. A wrong page is worse than a missing one: every reader repeats it with confidence.
- Write from the diff: a merge sometimes differs from what its description intended.
- Never a second entry for one concept: a new page forks the truth.
- A knowledge change describing unmerged code waits.
- A "small" fix that changes meaning is substantive: hold it, comment with evidence, and report.
- Rerun the validator after every push. Never approve on a stale result.
- No secret, internal-only host or regulated data in a knowledge page.

## Quality gate
Done when every description of each changed concept is updated or skipped with a reason, and the validator passes on the head. The report gives the merged change and the pinned commit, the concept ids changed, per target (knowledge base, shared skills, repository docs) the change link or the skip reason, the validator result (PASS, FAIL with the error, or none configured), and for a review its verdict.
