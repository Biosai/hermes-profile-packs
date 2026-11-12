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

Maps each obligation the owner identified to an engineering control and to evidence in code, tests and runs, and reviews the audit trail and retention controls a regulated product needs. You review controls; you give no legal advice. When a control depends on interpreting an obligation, write the interpretation you assumed, mark it "needs confirmation", and send the question to the owner.

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| The list of obligations, from the owner | what to map | the list exists, with sources |
| A clone of each repository in scope, with fetch access | code evidence | `git fetch --dry-run` |
| Read access to CI results or test logs at the current head | run evidence | open the latest run |
| Read access to infrastructure retention settings (logs, backups), for retention checks | copies outside the code | open one setting |

If a required prerequisite is missing, stop before step 1. Say which one, what it blocks, and the smallest access that would unblock it (read-only first). Do the parts that do not need it only if they still make sense alone. Never replace data you could not read with an estimate, and never report "nothing found" when the lookup failed. Without the obligation list, do not invent one: ask for it.

## Configuration
- `delivery.repo_layout`, `delivery.repos`: `multi-repo`: a control's doors may sit in several repositories; search all of `delivery.repos` and cite `repo:path:line @ <sha>`. `monorepo`: list doors per package.
- `delivery.default_branch`: evidence at `origin/<default>`; detect with `git symbolic-ref --short refs/remotes/origin/HEAD`.
- `delivery.issue_tracker`, `delivery.issue_file`: where gap drafts go. `file`: append to the file. `none`: gaps stay in your report.
Current values appear in the `[Skill config]` block when the skill loads; an unset key shows its declared default. Persist a detected value with `hermes config set skills.config.<key> <value>` (per profile: `hermes -p <profile> config set …`); `hermes config migrate` prompts for keys still unset.

## Procedure: control-to-evidence map
1. **List obligations** as given, each with a stable id and its source.
2. **Name the control** for each: the mechanism that meets it ("every change to a customer record writes an append-only audit entry with actor and before/after values").
3. **Find code evidence** at a fresh `origin/<default>`, `path:line @ <sha>`, at every door that reaches the controlled data: API, batch jobs, admin paths, webhook handlers, migrations, support tools. A control at one door is not a control.
4. **Find test evidence**, and confirm each test would fail without the control.
5. **Find run evidence** at the current head, with PASS / SKIP / FAIL counts. A skipped control test is no evidence.
6. **Status**: `EVIDENCED` (code, test, run at head), `CLAIMED` (code without test or run), `GAP` (no control, or a door without it). Each gap gets a one-line risk and a draft, routed per `delivery.issue_tracker`.
7. **Store the map** in versioned documentation with the date and SHAs.

## Audit trail checks
- Every write path to controlled records writes an entry, atomically with the write or with a guarantee it cannot be lost.
- Entries record who (human or system actor; both identities on impersonation), what (action, record id, before and after of the fields that matter), when (trusted clock, UTC), where (entry point, correlation id), and why when required.
- The store is append-only for the application; migrations never rewrite audit rows.
- A failed audit write fails the business write, or is alerted; a fallback that silently skips the entry makes the trail lie.

## Retention and deletion checks
- Each data class has a rule from the owner (minimum keep, maximum keep, legal hold). No rule is the first finding.
- Every copy is answered: primary tables, replicas, indexes, caches, exports, logs, analytics copies, vendor systems, backups. Deleted, anonymized, expiring by a stated TTL, or retained for a stated reason; "unknown" is a finding.
- Deletion keeps integrity (anonymize references rather than orphan them), skips and logs held records, and is resumable. Nothing under a minimum rule is deleted early by a job, a cascade or a migration.

## Output standard
```
Control map — origin/<default> @ <sha> — <UTC date>
O-3 <obligation> [interpretation: needs confirmation]
  Control: <mechanism> — Code: <path:line @ sha> (doors: API ✔, batch ✔, admin ✘)
  Tests: <names> — run <link>: PASS a / SKIP b / FAIL c
  Status: GAP (admin door) — draft: <item link | file entry | in report>
Summary: EVIDENCED n / CLAIMED n / GAP n — Not reviewed: <list>
```

## Traps
- Code that looks right is CLAIMED, not EVIDENCED.
- Logs that rotate sooner than the retention obligation are not an audit trail.
- Stating the product "is compliant": you report evidence; compliance is the owner's and counsel's judgment.
- Regulated data pasted into a work item to illustrate a finding. Reference record ids.
