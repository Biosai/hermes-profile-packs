# Items and pitfalls of an audit

Companion to `repo-audit-to-issues`, steps 2, 3 and 7 to 9. `filing-discipline.md` covers
deduplication and filing a backlog; `evidence-techniques.md` covers how to prove a finding.

## What an item carries (step 7)
- The finding, with the date and the commit it was measured on.
- The real output, verbatim, never paraphrased.
- The root cause, quoting `file:line`.
- What a fix must decide: a choice, not a disguised recommendation.
- A scope of checkboxes that can each be proved done.
- Links to related items, without auto-closing keywords: closing is the owner's call.
- When it contradicts or supersedes an existing item, it says so, and the report flags it.

A finding in the report reads:
```
Symptom: <what happens>
Evidence: <command> -> <output excerpt>; control: <command> -> <expected output>
Impact: <who or what it hurts>   Likely fix: <...> (size: S/M/L)
```

## Filing (steps 7 and 8)
- Create the labels before the first item: an unknown label is silently dropped. Label by who can
  unblock the item.
- When existing items sit on a board or project view with a status field, new ones go there too,
  each with a status: an item without one is hidden from the default grouped view. Check each item
  by number with its status, never the board's total.

## Surveying and counting (steps 2 and 3)
- On github, an open-issue count includes pull requests and the issues API returns them too:
  filter them out before counting. On another host, check what its count includes.
- Count the conclusion of every CI run in the history, not the latest one. Expired CI logs are
  not a finding: reproduce locally with the runner's shape (runtime version, package manager,
  script name).
- Prove the duplicate search can see: a phrase you know exists is found, a nonsense string is
  not. On an empty tracker, run the same query on a sibling repository known to hold items, and
  name it in the report.

## Ranking (step 9)
- Rank by how directly each finding blocks the project's most pressing goal, then by who can
  unblock it: owner-only actions (a console click, a DNS record, a paid plan) apart from work a
  profile can do.
- When the owner says they cannot act now, lead with the work a profile can do and list the
  items that wait on the owner in one line.

## Pitfalls
- A green job proves a tool ran in that job; a sibling job may call it where it is not installed.
  Check which job installs what.
- A green badge is not "tests pass": open the log and count the tests that ran. A test target
  with zero test files passes in every framework.
- A repository's docs saying a gate passes are a claim: paste the gate's output, or say "not run".
- After a platform migration, search the product and marketing docs too (vision, mission,
  positioning): the opening sentences are the ones nobody re-reads.
- A credential rotated during the audit: a running process keeps the old value. Compare
  fingerprints of each source, never the value, and probe old and new before trusting a result.
- An owner decision that invalidates part of a filed item gets a comment on that item saying which
  part of the analysis was wrong; the correction does not stay in a conversation.
- A finding made during another task that does not fit that task's scope is an audit finding: it
  goes through steps 5 to 8, not into that task's change.

## What this workflow is not
It finds what is broken. Listing the work still missing between a plan and the tracker is a
different job: the product manager profile's `remaining-work-to-issues` workflow when that profile
is installed, otherwise a question for the owner.
