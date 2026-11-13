---
name: glossary-discipline
description: "Keep one glossary term per concept, everywhere"
metadata:
  hermes:
    config:
      - {key: delivery.default_branch, description: "Default branch name, or detect", default: "detect"}
      - {key: delivery.issue_tracker, description: "Where work items go: github, gitlab, jira, linear, file, none, or detect", default: "detect"}
    prerequisites:
      commands: [git]
---
# Glossary Discipline

Use when a term is added or changed, or when a work item, a pull or merge request or a document uses a second word for a concept that already has one. Designing or restructuring the whole term set belongs to `taxonomy`.

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| Read access to the glossary, and a way to propose changes to it | add or change entries | the glossary opens |
| A clone of the code, with fetch access | code names and their mapping | `git fetch --dry-run` |
| Comment access on the issue tracker, unless `delivery.issue_tracker` is `none` or `file` | point authors to the right term | any item opens |

If one is missing, stop before step 1 and say which, what it blocks, and the smallest access that would unblock it (read-only first). Never report "no existing entry" when the search failed. With no glossary at all, propose where one should live and ask the owner before creating it.

## Configuration
- `delivery.default_branch`: code names are cited there, freshly fetched. `detect`: `git symbolic-ref --short refs/remotes/origin/HEAD`.
- `delivery.issue_tracker`: where a correction goes. A tracker: a comment on the item. `file`: a note next to the entry. `none`: the corrections are listed in the report.
- For `detect`, say what was detected and suggest `hermes config set skills.config.<key> <value>`.

## Procedure
1. Check the code first: the term matches what the code calls the concept, or the entry explains the mapping.
2. Search the entries and their synonyms. If the concept exists, extend that entry.
3. Write the entry with every one of [the entry fields](references/entry-fields.md): term, definition, code names, banned synonyms, "not to be confused with", stable id.
4. Fix existing uses in the knowledge base, shared skills and docs in the same change. List the rest for follow-up.
5. Open the pull or merge request. When the term changes how work items or reviews are worded, tell the people or profiles who write them.
6. When reviewing, check titles and bodies against the banned synonyms.
7. In repositories you own, fix a synonym in the same change. Elsewhere, point the author to the entry and the correct term; do not rewrite their text.
8. When a new word keeps appearing for an existing concept, decide with the owner whether it becomes the term or a banned synonym.

## Decision rules
- One term per concept. Readers assume two words mean two things, agents then build two of something, and nobody can search for the concept any more.
- Code wins: when the glossary disagrees with the code, fix the entry or the mapping.
- A definition says what the concept is for, never how it is implemented.
- Never ban a word that is correct for a different concept: use "not to be confused with".
- Never leave a term and its rival both in use.
- Documents link the entry by its stable id instead of redefining the term.

## Quality gate
A term change is done when the entry holds every field, the uses are fixed in the same change (count and locations reported) and the rest is listed. Enforcement is done when each correction is reported as `Term: <used> -> <glossary term> (<entry link>) at <location>` where `delivery.issue_tracker` says.
