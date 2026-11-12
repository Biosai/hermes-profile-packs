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

Keeps the knowledge base, glossary and shared skills true to merged code, by stable concept id, and reviews knowledge PRs (pull or merge requests) others open after a merge. A wrong page is worse than a missing one: every profile that loads it repeats the mistake with confidence. Code wins.

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| Code-host CLI with read access: `gh` (github), `glab` (gitlab) | the merged diff and PR state | `gh auth status` / `glab auth status` |
| A clone of the code repositories, with fetch access | check every claim against code | `git fetch --dry-run` |
| Push access to branches of the knowledge and skills repositories | open update PRs | `git push --dry-run` on a scratch branch |
| The knowledge repository's validator, when it has one | links, frontmatter, ids | run it on the current head |

If a required prerequisite is missing, stop before step 1. Say which one, what it blocks, and the smallest access that would unblock it (read-only first). Do the parts that do not need it only if they still make sense alone. Never replace data you could not read with an estimate, and never report "nothing found" when the lookup failed.

## Configuration
- `delivery.code_host`: how you read the merged diff (for example `gh pr diff N`, `glab mr diff N`). Detect from `git remote get-url origin`.
- `delivery.repo_layout`, `delivery.repos`: where the knowledge lives. `monorepo`: docs and skills may be folders of the same repository; one PR can carry them. `multi-repo`: one PR per knowledge repository in `delivery.repos`, each linking the merged code PR.
- `delivery.default_branch`: claims are checked at `origin/<default>` of the code repository; detect with `git symbolic-ref --short refs/remotes/origin/HEAD`.
- `delivery.merge_policy`: who merges knowledge PRs. `owner` (default): never merge; hand over. `reviewer`: the approving reviewer merges; you never merge your own. `auto-when-green`: auto-merge only after your checks pass. A written, scoped exception from the owner overrides only within its scope.
Current values appear in the `[Skill config]` block when the skill loads; an unset key shows its declared default. Persist a detected value with `hermes config set skills.config.<key> <value>` (per profile: `hermes -p <profile> config set …`); `hermes config migrate` prompts for keys still unset.

## Procedure: write the update
1. **Read the merged diff**, not the description: every concept, enum value, status, field, endpoint, default, limit and flow it adds, changes or removes.
2. **Pin** `origin/<default> @ <sha>` after the merge.
3. **Find every description of each concept**: the knowledge base by stable id, shared skills, the repository's docs; grep the glossary term and known synonyms.
4. **Per target**: update, or skip with a reason.
5. **Update by id**: never a second entry for the same concept. Quote values exactly as in code, link the merged PR, cite `path:line @ <sha>`, mark what is verified versus intended.
6. **Run the validator** on a fresh export; an error is a FAIL.
7. **Open the PR**: `<concept>: <what changed> (after <merged PR link>)`. Never push directly to a shared branch.

## Procedure: review someone else's knowledge PR
1. Read the linked code PR's state now; a PR describing unmerged code waits.
2. Run the validator on the PR head.
3. Grep `origin/<default>` for every value, field, status code, default and flow the PR states; any claim not found is a defect.
4. Check structure, id scheme, template, glossary terms, and that no secret, internal-only host or regulated data appears.
5. Small and certain defects (typo, broken link, synonym): fix or suggest. Substantive ones (unverifiable claim, change of meaning): hold, comment with evidence, report.
6. Merge only as `delivery.merge_policy` allows.

## Output standard
```
Knowledge after <merged PR link> — origin/<default> @ <sha>
Concepts changed: <ids>
Knowledge base / Shared skills / Repo docs: <PR link> | skipped — <reason>
Validator: PASS | FAIL <error> | none configured
Reviewed: <PR link> — APPROVED | MERGED (policy) | HELD (<reason>)
```

## Traps
- Writing from the PR description; merges sometimes differ from intent.
- A new page for an existing concept forks the truth.
- "Small" fixes that change meaning are substantive.
- Approving on a stale validator result; rerun after every push.
