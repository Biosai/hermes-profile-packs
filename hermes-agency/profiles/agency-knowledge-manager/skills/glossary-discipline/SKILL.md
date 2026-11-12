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

Keeps one term per concept across the glossary, knowledge base, work items, PRs (pull or merge requests) and documents. Two words for one concept is a bug: readers assume two words mean two things, agents then build two of something, and nobody can search for the concept any more.

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| Read and PR access to wherever the glossary lives | add or change entries | open the glossary |
| A clone of the code, with fetch access | code names and mapping | `git fetch --dry-run` |
| Comment access on the tracker, unless `delivery.issue_tracker` is `none` or `file` | point authors to the right term | open any item |

If a required prerequisite is missing, stop before step 1. Say which one, what it blocks, and the smallest access that would unblock it (read-only first). Do the parts that do not need it only if they still make sense alone. Never replace data you could not read with an estimate, and never report "nothing found" when the lookup failed. With no glossary at all, propose where one should live and ask the owner before creating it.

## Configuration
- `delivery.default_branch`: code names are cited at `origin/<default>`; detect with `git symbolic-ref --short refs/remotes/origin/HEAD`.
- `delivery.issue_tracker`: where enforcement comments go. Tracker: a comment on the item. `file`: a note next to the entry. `none`: list corrections in your report.
Current values appear in the `[Skill config]` block when the skill loads; an unset key shows its declared default. Persist a detected value with `hermes config set skills.config.<key> <value>` (per profile: `hermes -p <profile> config set …`); `hermes config migrate` prompts for keys still unset.

## What an entry holds
- **Term**: the one word or phrase the team uses.
- **Definition**: one or two sentences, in other glossary terms where possible.
- **Code names**: identifiers that carry it (table, type, enum, API field), cited `path:line @ <sha>`.
- **Banned synonyms**, and why if not obvious.
- **Not to be confused with**: neighboring terms and the difference.
- **Stable id**, so documents link instead of redefining.

## Procedure: a new or changed term
1. **Check the code first.** The term matches what the code calls it, or the entry explains the mapping.
2. **Search entries and their synonyms.** If the concept exists, extend that entry.
3. **Write the entry** with every field above.
4. **Fix existing uses** in the knowledge base, shared skills and docs in the same PR; list the rest for follow-up.
5. **Open the PR**, and tell the product manager and the architect when the term changes how work items or reviews are worded.

## Procedure: enforcement
1. Check titles and bodies you review against the banned-synonym list.
2. In repositories you own, fix synonyms in the same PR.
3. Elsewhere, point the author to the entry and the correct term; do not rewrite their text yourself.
4. When a new word keeps appearing for an existing concept, decide with the owner whether it becomes the term or a banned synonym; never leave both.

## Output standard
For a change: the entry diff and the uses fixed (count and locations). For enforcement: `Term: <used> → <glossary term> (<entry link>) at <location>`.

## Traps
- Defining a term by its implementation; the definition says what it is for.
- A glossary that disagrees with the code. Code wins; fix the entry or the mapping.
- Banning a word that is correct for a different concept; use "not to be confused with".
