---
name: remaining-work-to-issues
description: "File the work left between the plan and the tracker"
metadata:
  hermes:
    tags: [workflow]
    config:
      - key: venture.brief
        description: "The venture's brief: customer, voice, constraints, autonomy"
        default: ""
      - key: delivery.code_host
        description: "Where code is reviewed: github, gitlab, bitbucket, other, or detect"
        default: "detect"
      - key: delivery.repos
        description: "Working copies this profile may read or change, comma-separated"
        default: ""
      - key: delivery.issue_tracker
        description: "Issue tracker: github, gitlab, jira, linear, file, none, or detect"
        default: "detect"
      - key: delivery.issue_file
        description: "Markdown file for work items when the tracker is 'file'"
        default: ""
    prerequisites:
      commands: ["git"]
---
# Remaining Work to Issues

Turns "create the issues for what is missing", "give me the high level", "what is left to do" or
a build plan into tracked items in dependency order. Defects found on the way belong to
`repo-audit-to-issues`; this workflow files forward work. It builds nothing.

## Trigger
The owner asks for the remaining work, a build plan or high-level items, or redirects you from
building to filing ("can you just create the issues?").

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| The plan of record: `venture.brief`, the repository's roadmap, or the owner's plan note | the definition of done | open it |
| Read access to every item in the tracker, open and closed | subtract what is tracked | one listing returns items |
| Read access to the repositories in `delivery.repos`, and to the live product | prove each gap is real | `git fetch --dry-run`; one page or call |
| Write access to the tracker, when `delivery.issue_tracker` is not `none` | file the items | create-permission check |

If a required prerequisite is missing, stop before step 1. Say which one, what it blocks, and the
smallest access that would unblock it (read-only first). Without a plan of record, ask the owner
for it: a gap list derived from your own idea of the product is a guess.

## Configuration
- `venture.brief`: where the plan of record starts; empty: ask the owner where it lives.
- `delivery.issue_tracker`, `delivery.issue_file`: where items go; `none` puts the ordered list
  in your report. Parent and child items use the tracker's own mechanism (sub-issues, epics,
  child items); `detect` from what existing items use.
- `delivery.code_host`, `delivery.repos`: where the gaps are checked; `detect` from
  `git remote get-url origin`.
- Set values with `hermes config set skills.config.<key> <value>`.

## Steps
1. Read the tracker before anything else and settle which ask this is. "Give me the high
   level" over a tracker that already holds the work means epics over existing items: derive
   the epic set from the repository's definition of done and parent every open item under
   exactly one; an orphan is a finding. "Items for what is left" means the gaps, and rolling
   up existing defects answers it with nothing new. A tracker holding only defect-level items
   and no forward work points to the second reading; when unsure, ask.
2. Read the plan of record for its amendments, not only its task table: struck rows,
   re-scoped callouts, a risk demoted in a sentence. The latest annotation wins over the
   original row; cite the amendment in the item that depends on it.
3. Remaining work = the plan's definition of done minus every tracked item. Do not derive it
   by walking the code: that produces defects, which the tracker already has.
4. Prove each gap: show that neither the repository nor the live product contains it.
5. Look for the prerequisite nobody asked for: what must be settled before the requested work
   and cannot be retrofitted (how money is represented and rounded is the recurring one: every
   stored amount inherits it). File it, and say it was not in the request and why it blocks.
6. When the request contradicts the repository's own stated constraints (an agent or
   contribution file forbidding a class of work before some gate), file the contradiction in
   the item. The owner's explicit decision outranks your inference, not the reverse: record it
   as a dated, deliberate bet and require the constraint file to be amended in the change that
   implements it. Never violate the constraint silently, and never refuse the owner silently.
7. A test that asserts current wrong behaviour (written because the fix was outside that
   session's remit) is named in the fixing item's acceptance criteria, to be inverted;
   otherwise the defect is protected by CI.
8. Write one item per decision, in dependency order. Label the one or two that unblock the
   rest; every blocked item names its blockers by number. Deduplicate and file with
   `repo-audit-to-issues` steps 6 to 8.
9. If you were redirected from building, treat it as a sign the order was wrong: check whether
   the repository had already scheduled the work you started, and say so in the reply. Code
   already written is committed as work in progress and parked as a draft (see
   `bounded-task-delivery`, "Unfinished work"), never discarded or left on disk.

## Done when
- Every gap between the plan of record and the tracker is an item, or is listed as not needed
  with the amendment that says so.
- Items are in dependency order, the unblockers are labelled, and each blocked item names its
  blockers by number.
- Nothing was built in this workflow.

## Output standard
```
Plan of record: <link> (amendments read: <n>)   Tracked before: <n> items
Filed: <n> — unblockers first: <links>   Not needed: <gap> — <amendment>
```
Item links on their own lines, as plain text.

## Traps
- Filing a gap the owner already closed in an amendment reads as not having read the plan.
- A flat list of peers makes the reader pick by interest instead of by what is next.
- "Blocked" without a predecessor reads as abandoned; with one, it reads as sequenced.
- A gap asserted from the plan alone is a guess until the repository and the product are checked.
