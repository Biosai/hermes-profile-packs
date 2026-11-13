---
name: issue-authoring-standard
description: "Write a work item a developer can start without questions"
metadata:
  hermes:
    config:
      - {key: delivery.issue_tracker, description: "Where work items go: github, gitlab, jira, linear, file, none, or detect", default: "detect"}
      - {key: delivery.issue_file, description: "Markdown file for work items when the tracker is file", default: ""}
      - {key: delivery.code_host, description: "Where code is reviewed: github, gitlab, bitbucket, other, or detect", default: "detect"}
      - {key: delivery.repo_layout, description: "Repository layout: single, monorepo, multi-repo, or detect", default: "detect"}
      - {key: delivery.default_branch, description: "Default branch name, or detect", default: "detect"}
    prerequisites:
      commands: [git, gh, glab]
---
# Issue Authoring Standard

Use when writing or rewriting an engineering work item, so that a developer can start it without one follow-up question.

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| Write access to the issue tracker, or to `delivery.issue_file` | create and update items | open a draft, or the file |
| Search over existing items, open and closed | deduplication | one search returns results |
| A clone with fetch access | cite code at a commit | `git fetch --dry-run` |
| Read access to the logs, API or data the report needs | real data | one read query |

If one is missing, stop before step 1 and say which, what it blocks, and the smallest access that would unblock it (read-only first). Never replace data you could not read with an estimate, and never report "no duplicates" when the search failed.

## Configuration
- `delivery.issue_tracker`: file the item in the tracker (github: `gh issue create`; gitlab: `glab issue create`; another: its own CLI, API or web UI). `file`: append a section with a stable id to `delivery.issue_file`. `none`: the full item goes in the report.
- `delivery.code_host`: decides the permalink format.
- `delivery.repo_layout`: `monorepo`: name the affected package in the title. `multi-repo`: file in the repository that owns the fix and link the others.
- `delivery.default_branch`: where code is read, freshly fetched.
- For `detect`, say what was detected and suggest `hermes config set skills.config.<key> <value>`.

## Procedure
1. Gather the data first: the actual request and response, the log lines, the rows, the code at the default branch.
2. Search item bodies for duplicates, open and closed, and act on each hit as [the duplicate search](references/duplicate-search.md) says.
3. Write the body in the order of [the item body](references/item-body.md): context, real data, repro steps, expected versus actual, acceptance criteria (written with `acceptance-criteria`), links, data change, open questions.
4. Title it in the glossary's terms: `<area>: <observable problem or outcome>`.
5. Split multi-part work into child items, each a shippable unit.
6. Give a priority with a one-line reason: data integrity, money and permissions first, then user-facing breakage, operator convenience, polish. Ranking a whole backlog belongs to `prioritization`.
7. File every verified finding not fixed in this turn, with its data, non-code ones included: contradicting documents, voice drift, stale claims, missing access.
8. Re-read it as the developer. If you would ask anything, it is not done.
9. Re-read the filed item from the tracker, then update what it changes: its board status, a decision record, the knowledge base, an earlier claim of yours.

## Decision rules
- The error body is the report, never a paraphrase or "it seems that".
- Cite code by permalink at a commit: a branch moves under the reader.
- Criteria name tests or flows, never an expected test total, which goes stale at the next merge.
- One root cause per item, one item per root cause: new data on a known cause goes to its item, and a batch of findings can never be closed.
- A real trade-off is written as the decision needed, addressed to whoever owns it, never answered by you.
- An obvious fix is written as a precise item, never as code from the product manager: it would skip every gate.
- Reference related items without auto-closing keywords: closing is the owner's call.
- Size ranks; it is never a status.
- Something fixed in this turn is a pull or merge request, not an item.

## Quality gate
The item is ready when a developer could start it without a question and every claim in it is data or a cited source. The report gives the item's link (or file entry id, or "in report" when the tracker is `none`), the priority and size with the reason, and the duplicate searches run with their control.
