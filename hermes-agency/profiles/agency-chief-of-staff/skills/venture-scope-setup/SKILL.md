---
name: venture-scope-setup
description: "Record a project's scope in the brief, in the owner's words"
metadata:
  hermes:
    config:
      - key: project.brief
        description: "Path or URL of the brief: customer, voice, constraints, autonomy"
        default: ""
      - key: owner.channel
        description: "Where questions and owner actions reach the owner"
        default: "this conversation"
---
# Venture Scope Setup

Use when work starts on a product, venture or client project whose scope is not yet in the project brief, when a task depends on a fact the brief does not state, or when the project changed (a pivot, a dropped market, a new constraint) and the brief is stale.

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| The owner, reachable where `owner.channel` says | only the owner can describe the project | a message can be posted there |
| Write access to the project brief, when `project.brief` is set | the approved scope is recorded there | the file or page is writable |

If one is missing, stop before step 1 and say which, what it blocks, and the smallest access that would unblock it. Without the owner there is no scope: never fill it from another project or from the product category.

## Configuration
- `project.brief`: read in step 1 and written in step 5. Unset: propose where a brief could live, and give the owner the line `hermes config set skills.config.project.brief <path or URL>` to run once it exists.
- `owner.channel`: where the questions and the draft go.

## Procedure
1. Read the brief. List every scope entry that is missing, undated, or contradicted elsewhere in the record.
2. Ask the owner only for what is missing, one question at a time, the most blocking first:
   - what the project is in one sentence, and who pays for it;
   - which repositories, work tracker, domains and channels belong to it;
   - the binding constraint as the owner sees it;
   - the decisions already made, each with its date;
   - the autonomy of each function: what is done alone, what is only prepared.
3. Keep each answer in the owner's own words, with the date it was given.
4. Draft the scope as [the scope entry](references/scope-entry.md): five short lines, the detail staying elsewhere in the brief. Propose it as text for approval.
5. On approval, write it to the brief with the approval date.
6. Suggest the settings the answers imply (code host, repositories, tracker, merge policy) as `hermes config set skills.config.<key> <value>` lines, handed to the owner with the `owner-action-handoff` workflow.
7. Re-read the brief after writing, report its link, and say which earlier entries the new scope supersedes.

## Decision rules
- Never fill a gap with a fact from another project, however similar it looks.
- The scope lives in the project brief, never only in a conversation or in memory: the next session starts blank.
- The owner's words are recorded as given. An interpretation is labelled as yours until the owner confirms it.
- A constraint said to come from a rule or a regulator is recorded with its primary source, or marked "source to confirm".
- A dated decision is a fence: an option the owner dropped is never written back into a later plan.
- A newer dated statement supersedes an older one, which is kept and marked superseded as `decision-log` says, never erased.
- One brief per project. When one owner runs several projects, each scope is asked for and recorded separately.

## Quality gate
The scope is set when the brief holds the approved, dated entry (what the project is and who pays, what belongs to it, the binding constraint, the dated decisions), the autonomy of each function is recorded, the brief was re-read after writing, and the report gives its link and what remains unanswered.
