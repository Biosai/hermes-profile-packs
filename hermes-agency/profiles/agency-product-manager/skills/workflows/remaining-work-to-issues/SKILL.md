---
name: remaining-work-to-issues
description: "File the work left between the plan and the tracker"
metadata:
  hermes:
    tags: [workflow]
    config:
      - key: project.brief
        description: "Path or URL of the brief: customer, voice, constraints, autonomy"
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

Files the forward work left between the plan of record and the issue tracker, in dependency order. It builds nothing.

## Trigger
The owner asks what is left to do, asks for a build plan or high-level items, or redirects a build into filing ("can you just create the issues?").

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| The plan of record: the project brief (`project.brief`), the repository's roadmap, or the owner's plan note | the definition of done | it opens |
| Read access to every tracker item, open and closed | subtract what is tracked | one listing returns items |
| Read access to the repositories in `delivery.repos`, and to the live product | prove each gap is real | `git fetch --dry-run`; one page or call |
| Write access to the tracker, unless `delivery.issue_tracker` is `none` | file the items | create-permission check |

If one is missing, stop before step 1 and say which, what it blocks, and the smallest access that would unblock it (read-only first). Without a plan of record, ask the owner for it: a gap list derived from your own idea of the product is a guess.

## Configuration
- `project.brief`: where the plan of record starts. Empty: ask the owner where it lives.
- `delivery.issue_tracker` and `delivery.issue_file`: where items go. `none`: the ordered list goes in the report. Parents and children use the tracker's own mechanism (sub-issues, epics, child items), detected from what existing items use.
- `delivery.code_host` and `delivery.repos`: where the gaps are checked. `detect`: from `git remote get-url origin`.
- Set values with `hermes config set skills.config.<key> <value>`.

## Steps
1. Read the tracker first, and settle which ask this is. "The high level" over a tracker that already holds the work means epics over existing items: derive the epic set from the plan's definition of done and parent every open item under exactly one. "Items for what is left" means the gaps. When unsure, ask.
2. Read the plan of record for its amendments, not only its task table: struck rows, re-scoped callouts, a risk demoted in a sentence. Cite the amendment in the item that depends on it.
3. Compute the remaining work: the plan's definition of done minus every tracked item.
4. Prove each gap: show that neither the repository nor the live product contains it.
5. Look for [the cases that need their own handling](references/special-cases.md): a prerequisite nobody asked for, a request that contradicts the repository's stated constraints, a test that asserts wrong behaviour, a build redirected into filing.
6. Write one item per decision, to the standard of `issue-authoring-standard`, duplicate search included, in dependency order. Label the one or two that unblock the rest. Every blocked item names its blockers by number.
7. Report the plan of record and the amendments read, the items tracked before, the items filed with the unblockers first, and each gap not needed with the amendment that says so.

## Decision rules
- The latest annotation of the plan wins over the original row: filing a gap the owner closed in an amendment reads as not having read the plan.
- Never derive remaining work by walking the code: that produces defects, which the tracker already has. A defect found on the way is filed apart, through the technical lead profile's `repo-audit-to-issues` when it is installed, otherwise as one item of its own.
- An open item under no epic is a finding. Rolling up existing defects does not answer "what is left", and a tracker holding only defects points to that reading.
- A gap asserted from the plan alone is a guess until the repository and the product are checked.
- The owner's explicit decision outranks your inference. Never violate a repository constraint silently, and never refuse the owner silently.
- A flat list of peers makes the reader pick by interest. "Blocked" without a predecessor reads as abandoned; with one, as sequenced.
- Code already written is never discarded or left only on disk.

## Done when
- Every gap between the plan of record and the tracker is an item, or is listed as not needed with the amendment that says so.
- Items are in dependency order, the unblockers are labelled, and each blocked item names its blockers by number.
- Nothing was built in this workflow.
