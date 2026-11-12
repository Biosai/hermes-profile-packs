---
name: repo-audit-to-issues
description: "Audit a repository into ranked, deduplicated findings"
metadata:
  hermes:
    config:
      - key: delivery.code_host
        description: "Where code is reviewed: github, gitlab, bitbucket, other, or detect"
        default: "detect"
      - key: delivery.repo_layout
        description: "Repository layout: single, monorepo, multi-repo, or detect"
        default: "detect"
      - key: delivery.repos
        description: "Working copies this profile may read or change, comma-separated"
        default: ""
      - key: delivery.default_branch
        description: "Default branch name, or detect"
        default: "detect"
      - key: delivery.issue_tracker
        description: "Issue tracker: github, gitlab, jira, linear, file, none, or detect"
        default: "detect"
      - key: delivery.issue_file
        description: "Markdown file for work items when the tracker is 'file'"
        default: ""
    prerequisites:
      commands: ["git"]
---
# Repo Audit to Issues

Use for "audit this repo", "what is broken", "what should I work on next", a scheduled sweep
the owner asked for, or a finding made during a task that does not fit that task's scope.
The output is findings, never a pull or merge request: the owner chooses what gets built.

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| Read access to the repositories in `delivery.repos` | evidence by execution | `git -C <repo> fetch --dry-run` |
| The project's toolchain | run tests and builds | the documented test command starts |
| CI log read access on the code host | confirm what CI actually ran | e.g. `gh auth status`, `glab auth status` |
| Write access to the tracker, when `delivery.issue_tracker` is not `none` | file findings | create-permission check in the tracker |

If a required prerequisite is missing, stop before step 1. Say which one, what it blocks, and
the smallest access that would unblock it (read-only first). Never report "no findings" for
an area you could not read or run.

## Configuration
- `delivery.repos`: empty means the current directory only. `delivery.repo_layout`:
  `monorepo` scopes the audit, test runs and CI filters to the packages in question;
  `multi-repo` audits each repository and links related findings. `detect`: workspace files
  (package workspaces, build-tool modules) suggest a monorepo; say what you concluded.
- `delivery.default_branch`: audit the default branch as fetched; `detect` with
  `git symbolic-ref --short refs/remotes/origin/HEAD`. Never assume a name.
- `delivery.code_host`: decides the CLI and the words; `detect` from
  `git remote get-url origin`.
- `delivery.issue_tracker`: where findings go. `file` appends to `delivery.issue_file`;
  `none` keeps them in the report only; `detect` uses the code host's tracker if enabled.
- Set values with `hermes config set skills.config.<key> <value>`.

## Procedure
1. Fix the scope: which repositories or packages, which question (security, reliability,
   cost, dead code, a funnel step). One audit, one question.
2. Collect evidence by execution on a fresh fetch of the default branch: run the tests and
   read the CI log, build from clean, call the endpoint, read the deployed configuration.
3. Add a positive control per finding: the probe passes where the problem is absent.
4. Deduplicate against existing items (bodies, open and closed); add evidence to an existing
   item or reopen it instead of opening a twin.
5. One item per finding: symptom as title; evidence, control, impact, likely cause, fix and
   size in the body. Label severity honestly.
6. Rank by how directly each blocks the venture's binding constraint, and report the list.

## Output standard
```
Symptom: <what happens>
Evidence: <command> -> <output excerpt>; control: <command> -> <expected output>
Impact: <who or what it hurts>   Likely fix: <...> (size: S/M/L)
```
Report: ranked links (or entries), one line each, constraint-blocking ones first.

## Traps
- Reading a green badge as "tests pass": open the log and confirm the tests ran.
- Deduplicating on titles only. Search bodies, closed items too.
- Twenty low-severity findings burying the one that matters. Rank, and say which one.
