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

Proves a database migration is numbered above the tip, applies at the production version, and neither drops what must be kept nor rewrites audit history. A tool that tracks one version number silently skips a migration numbered below the current version; CI migrates from empty and never sees it.

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| A clone with fetch access | migration directory at the tip | `git fetch --dry-run` |
| Code-host CLI with read access: `gh` (github), `glab` (gitlab) | other open PRs (pull or merge requests) adding migrations | `gh auth status` / `glab auth status` |
| A scratch database and its client (for example a local container and `psql` or `mysql`) | apply at the production version | connect and run a trivial query |
| A schema-only dump at the production version, or the ability to migrate a scratch database to it | the realistic starting point | the dump's version matches |
| Read-only access to deployed version tables, per environment | deployed versions | one select on the version table |

If a required prerequisite is missing, stop before step 1. Say which one, what it blocks, and the smallest access that would unblock it (read-only first). Do the parts that do not need it only if they still make sense alone. Never replace data you could not read with an estimate, and never report "nothing found" when the lookup failed. An environment you could not read is "not readable", never assumed current.

## Configuration
- `delivery.code_host`: how you find open PRs that touch migration paths (for example `gh pr list --json number,files`, or `glab mr list` then `glab mr diff <id>`). Detect from `git remote get-url origin`.
- `delivery.repo_layout`: `monorepo`: each service may own a migration directory and version table; check the one the PR touches and any that share its database. `multi-repo`: check every repository that migrates the same database.
- `delivery.default_branch`: the tip is read at `origin/<default>`; detect with `git symbolic-ref --short refs/remotes/origin/HEAD`.
Current values appear in the `[Skill config]` block when the skill loads; an unset key shows its declared default. Persist a detected value with `hermes config set skills.config.<key> <value>` (per profile: `hermes -p <profile> config set …`); `hermes config migrate` prompts for keys still unset.

## Procedure: does it apply?
1. **Fetch**; read the migration directory at `origin/<default>`; note the tip.
2. **Above the tip?** If the default branch moved since the branch was cut, it may no longer be.
3. **Unique across open PRs?** Two with the same number: the second to merge breaks. Report to both owners.
4. **Deployed versions**, per environment you can read.
5. **Apply at the production version**: restore the schema dump (or migrate a scratch database to that version), run up, record result and duration; down then up if down migrations exist.
6. **Raw SQL** naming renamed or dropped columns fails only at runtime; grep for it.

## Procedure: what does it do to controlled data?
7. **Classify** affected tables and columns by data class and retention rule.
8. **Drops and truncations** under a minimum retention rule wait until the data is archived under the same controls.
9. **New copies** of regulated data need a retention answer and a place in the deletion mechanism.
10. **Audit tables**: never update or delete audit rows, never backfill history with invented values.
11. **Backfills and corrections** change existing rows: the PR must declare them (what, rows per environment, how applied). Counts scope them; only the owner authorizes applying them.
12. **Constraint and type changes**: ask for the count of rows that would violate or be truncated, per environment.
13. **Locks and timing** at production scale; encryption and access on sensitive columns survive; irreversibility is stated.

## Output standard
```
Migration — <PR link> — <file> — number <n>
Tip on origin/<default> @ <sha>: <m> — above tip: yes/no — collisions: none | <links>
Deployed: <env>: <v> | not readable
Up at production version: OK in <t>s | FAIL <error> — down/up: OK | n/a
Raw SQL on changed columns: none | <path:line>
Retention conflicts / new copies / audit rows rewritten: <...>
Data change declared: yes | NO (blocking)
Verdict: OK | FINDINGS (<n>) | BLOCKING (<n>)
```

## Traps
- A green CI is not evidence the migration applies in production.
- Renumbering after a rebase is easy to forget; re-check the tip when you report.
- A rename done as add, copy, drop is three operations; review all three.
