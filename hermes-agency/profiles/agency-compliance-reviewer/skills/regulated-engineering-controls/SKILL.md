---
name: regulated-engineering-controls
description: "Map regulated controls to evidence in code and tests"
metadata:
  hermes:
    config:
      - {key: delivery.repo_layout, description: "Repository layout: single, monorepo, multi-repo, or detect", default: "detect"}
      - {key: delivery.repos, description: "Working copies this profile may read or change (paths or URLs, comma-separated)", default: ""}
      - {key: delivery.default_branch, description: "Default branch name, or detect", default: "detect"}
      - {key: delivery.issue_tracker, description: "Where work items go: github, gitlab, jira, linear, file, none, or detect", default: "detect"}
      - {key: delivery.issue_file, description: "Markdown file for work items when the tracker is file", default: ""}
    prerequisites:
      commands: [git]
---
# Regulated Engineering Controls

Use when a control from a policy-to-control mapping must be proven in code, tests and runs, or when the audit trail and the retention and deletion mechanisms of a regulated product are reviewed.

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| The control mapping, or the owner's list of obligations with their sources | what to prove | each row has an id and a source |
| A clone of each repository in scope, with fetch access | code evidence | `git fetch --dry-run` |
| Read access to CI results or test logs at the current head | run evidence | open the latest run |
| Read access to infrastructure retention settings (logs, backups), for retention checks | copies outside the code | open one setting |

If one is missing, stop before step 1: say which, what it blocks, and the smallest access that unblocks it (read-only first). Never estimate data you could not read, and never report "nothing found" when the lookup failed. Without a list of obligations, ask the owner for it: never invent one.

## Configuration
- `delivery.repo_layout`, `delivery.repos`: `multi-repo`: a control's doors may sit in several repositories; search all of `delivery.repos` and cite `repo:path:line @ <commit>`. `monorepo`: list the doors per package.
- `delivery.default_branch`: evidence is read at `origin/<default>`; detect with `git symbolic-ref --short refs/remotes/origin/HEAD`.
- `delivery.issue_tracker`: where gap drafts go. `file`: appended to `delivery.issue_file`. `none`: they stay in your report.

## Procedure
1. Run `policy-control-mapping` first: it turns the requirement text into obligations, each with a control, an owner and a status. The steps below prove the controls that software implements.
2. For each such control, find the code on a freshly fetched default branch, cited `path:line @ <commit>`, at every door that reaches the controlled data: API, batch jobs, admin paths, webhook handlers, migrations, support tools.
3. Find the test of the control at each door, and confirm it would fail without the control.
4. Find the run at the current head, with PASS / SKIP / FAIL counts.
5. Set the engineering status: `EVIDENCED` (code, test and run at this head), `CLAIMED` (code without a test or a run), `GAP` (no control, or a door without it).
6. Review the audit trail and the retention and deletion mechanisms against [references/audit-and-retention-checks.md](references/audit-and-retention-checks.md).
7. Give each gap a one-line risk and a draft work item, routed per `delivery.issue_tracker`.
8. Store the result with the mapping, in versioned documentation, with the date and the commits.

## Decision rules
- You report evidence. You give no legal advice and never state that the product "is compliant": that judgment is the owner's and counsel's.
- When a control depends on interpreting an obligation, write the interpretation you assumed, mark it "needs confirmation" and send the question to the owner.
- A control at one door is not a control.
- Code that looks right is CLAIMED, not EVIDENCED. A skipped control test is no evidence.
- Logs that rotate sooner than the retention obligation are not an audit trail.
- A fallback that silently skips an audit entry makes the trail lie.
- "Unknown" for a copy of regulated data is a finding; so is a data class without a retention rule.
- Never paste regulated data into a work item to illustrate a finding: reference record ids.

## Quality gate
The review is complete when each obligation has its control, the code citation per door, the tests with the run and its counts, and a status; each gap has its draft where the tracker setting says; interpretations are marked "needs confirmation"; and the summary counts EVIDENCED, CLAIMED and GAP at a pinned commit and date, and lists what was not reviewed.
