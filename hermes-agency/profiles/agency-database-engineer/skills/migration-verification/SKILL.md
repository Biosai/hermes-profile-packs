---
name: migration-verification
description: "Prove a migration applies and keeps regulated data safe"
metadata:
  hermes:
    config:
      - {key: delivery.code_host, description: "Where code is reviewed: github, gitlab, bitbucket, other, or detect", default: "detect"}
      - {key: delivery.repo_layout, description: "Repository layout: single, monorepo, multi-repo, or detect", default: "detect"}
      - {key: delivery.default_branch, description: "Default branch name, or detect", default: "detect"}
    prerequisites:
      commands: [git, gh, glab]
---
# Migration Verification

Use when a written database migration must be proven, before review or merge, to apply on the deployed schema, in the right order, with a tested way back.

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| A clone with fetch access | the migration directory at the tip | `git fetch --dry-run` |
| Read access to open pull or merge requests | other migrations in flight | list them |
| A scratch database on the production engine and version | apply on a copy | run a trivial query |
| A schema-only dump at the production version, or a way to migrate the scratch database to it | the real starting point | the versions match |
| Read-only access to the version table, per environment | deployed versions | one select |

If one is missing, stop before step 1: say which, what it blocks, and the smallest access that unblocks it (read-only first). Never estimate data you could not read, and never report "nothing found" when the lookup failed. An unreadable environment is "not readable", never assumed current.

## Configuration
- `delivery.code_host`: how you find open requests that touch migration paths. github: `gh pr list --json number,files`; gitlab: `glab mr list`, then `glab mr diff <id>`; any other host: its CLI or web UI, saying what was checked by hand.
- `delivery.repo_layout`: `monorepo`: each service may own a migration directory and a version table; check the one the request touches and any that share its database. `multi-repo`: check every repository that migrates the same database.
- `delivery.default_branch`: the tip is read at `origin/<default>`; detect with `git symbolic-ref --short refs/remotes/origin/HEAD`.

## Procedure
1. Start once the migration is written: `schema-migration` owns its design (staging, locks, compatibility, recovery path).
2. Fetch. Read the migration directory at `origin/<default>` and note the tip: the last migration there.
3. Check the number: above the tip, and used by no other open request.
4. Read the deployed version in each environment.
5. Apply on a copy: bring the scratch database to the production version, run the migration up, record result and duration.
6. Prove the way back: when a down migration exists, run down, compare the schema with the starting one, then run up again. When none exists, the request must say the migration is irreversible.
7. Search the code for raw SQL naming each column the migration renames or drops: it fails only at runtime.
8. Check the effect on existing data: [references/data-effects.md](references/data-effects.md).
9. Report, in the format given in the same reference.

## Decision rules
- This skill is the home of the numbering rule. A migration tool that tracks one version number silently skips a migration numbered below the deployed version, and CI cannot see it, because CI migrates from an empty database.
- Check the number against the tip of the freshly fetched default branch, every open request that adds a migration, and the deployed version.
- Two open requests with the same number: the second to merge breaks. Tell both authors.
- Re-check the tip when you report, and after every rebase.
- Before renumbering, compare the migration with those already on the default branch, comments ignored: it may duplicate one that landed. Rename the up and down files together.
- Green CI is no evidence that the migration applies in production.
- A rename done as add, copy, drop is three operations: verify all three.

## Quality gate
The verification is complete when the report gives the migration's number against the tip at a pinned commit; collisions, linked; the deployed version per environment, or "not readable"; the result of up at the production version, and of down then up, or "irreversible"; raw SQL on changed columns; the data effects and whether the data change is declared; and one verdict: OK, FINDINGS or BLOCKING.
