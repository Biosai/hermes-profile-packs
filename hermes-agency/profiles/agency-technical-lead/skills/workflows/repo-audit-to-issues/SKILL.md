---
name: repo-audit-to-issues
description: "Audit a repository into ranked, deduplicated findings"
metadata:
  hermes:
    tags: [workflow]
    config:
      - {key: delivery.code_host, description: "Where code is reviewed: github, gitlab, bitbucket, other, or detect", default: "detect"}
      - {key: delivery.repo_layout, description: "Repository layout: single, monorepo, multi-repo, or detect", default: "detect"}
      - {key: delivery.repos, description: "Working copies this profile may read or change, comma-separated", default: ""}
      - {key: delivery.default_branch, description: "Default branch name, or detect", default: "detect"}
      - {key: delivery.issue_tracker, description: "Issue tracker: github, gitlab, jira, linear, file, none, or detect", default: "detect"}
      - {key: delivery.issue_file, description: "Markdown file for work items when the tracker is 'file'", default: ""}
    prerequisites:
      commands: ["git"]
---
# Repo Audit to Issues

## Trigger
A repository is taken on; the owner asks for an audit, for what is broken or for what to work on next; a repository has not been run for months; a scheduled audit the owner asked for is due; or you are about to call something broken in a repository you have not run.

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| Read access to the repositories in `delivery.repos` | evidence by execution | `git -C <repo> fetch --dry-run` |
| The project's toolchain, at the versions CI pins | run tests and builds as CI does | the documented test command starts |
| Read access to CI run history and logs | what CI ran, across every run | list the runs |
| Write access to the tracker, unless `delivery.issue_tracker` is `none` | file the findings | create-permission check |

If one is missing, stop before step 1: say which, what it blocks, and the smallest access that unblocks it (read-only first). Never report "no findings" for an area you could not read or run.

## Configuration
- `delivery.repos`, `delivery.repo_layout`: empty means the current directory only. `monorepo`: scope the audit, the test runs and the CI filters to the packages in question. `multi-repo`: audit each repository and link related findings. `detect`: workspace files suggest a monorepo; say what you concluded.
- `delivery.default_branch`: audit the default branch as fetched. Detect with `git symbolic-ref --short refs/remotes/origin/HEAD`; never assume a name.
- `delivery.code_host`: the CLI and the words. github: `gh`; gitlab: `glab`; any other host: its own CLI or web UI. Detect from `git remote get-url origin`.
- `delivery.issue_tracker`: where findings go. `file`: appended to `delivery.issue_file`. `none`: the report only. `detect`: the code host's tracker, if enabled.

## Steps
1. Fix the scope: which repositories or packages, and which question (security, reliability, cost, dead code, one step of a funnel). One audit, one question.
2. Survey the whole surface first: every repository in `delivery.repos` and its open items. Trace the area in question with `codebase-scoping`, so each finding names the code and the specialty that owns it.
3. Collect evidence by execution on a freshly fetched default branch: run the tests, build from clean, call the endpoint, read the deployed configuration, count the conclusion of every CI run. Techniques: [references/evidence-techniques.md](references/evidence-techniques.md). Public surfaces (site, accounts, links, domains): [references/public-surface-audit.md](references/public-surface-audit.md).
4. Run the obvious fix before proposing it, and write its measured effect into the item. Restore what you changed and prove `git status --porcelain` is empty.
5. Add a positive control per finding: the probe passes where the problem is absent, and a scan that found nothing is shown finding something it should.
6. Deduplicate against existing items by their bodies, open and closed: [references/filing-discipline.md](references/filing-discipline.md).
7. Write one item per decision and file it where `delivery.issue_tracker` says; what an item carries, and the pitfalls of an audit: [references/items-and-pitfalls.md](references/items-and-pitfalls.md).
8. Read every filed item back from the tracker: title, labels, full body.
9. Rank by how directly each finding blocks the project's most pressing goal, and by who can unblock it.
10. Report what was reproduced, with the numbers; what you did not touch; the ranked links, one per line as plain text; and one next action offered as a question.

## Decision rules
- An audit produces findings, never a pull or merge request: the owner chooses what gets built.
- One item per decision, closable by fixing one thing: two symptoms of one root cause are one item; one symptom hiding two blockers is two.
- Same root cause as an existing item: add the evidence there. Adjacent cause: a new item that says why it is not the other one. Closed and back: reopen with the new evidence.
- "Never green since the first run" is a different finding from "the last run failed".
- A fix that makes things worse becomes a do-not-merge-blind warning in the item.
- Owner-only actions (a console click, a DNS record, a paid plan) are listed apart from work a profile can do.
- Twenty low-severity findings must not bury the one that matters: rank, and say which one. State uncomfortable numbers flatly.

## Done when
- Every finding is recorded once where `delivery.issue_tracker` says (in the report when `none`), ranked, with evidence and a positive control, and read back from the tracker.
- The working tree is as you found it, proved clean.
- No pull or merge request was opened.
