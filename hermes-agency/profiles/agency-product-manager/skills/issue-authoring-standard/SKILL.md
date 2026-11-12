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

Writes or rewrites an engineering work item so a developer can start it without one follow-up question: real data, repro, acceptance criteria, data-change declaration. Non-negotiable, because every gap becomes a question, a wrong guess, or rework.

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| Write access to the tracker (its CLI or API), or to `delivery.issue_file` | create and update items | create a draft, or open the file |
| Search access to existing items, open and closed | deduplication | one search returns results |
| A clone with fetch access | cite code at a SHA | `git fetch --dry-run` |
| Read access to the system's logs, API or data, as far as the report needs | real data | one read query |

If a required prerequisite is missing, stop before step 1. Say which one, what it blocks, and the smallest access that would unblock it (read-only first). Do the parts that do not need it only if they still make sense alone. Never replace data you could not read with an estimate, and never report "nothing found" when the lookup failed. A duplicate search that failed is not "no duplicates".

## Configuration
- `delivery.issue_tracker`: `github`/`gitlab`/`jira`/`linear`: create the item there (for example `gh issue create`, `glab issue create`, or the tracker's API). `file`: append a section to `delivery.issue_file` with a stable id heading. `none`: write the full item in your report for the owner; never create one elsewhere. `detect`: infer from where existing items live and say what you found.
- `delivery.code_host`: decides permalink format and code search. Detect from `git remote get-url origin`.
- `delivery.repo_layout`: `monorepo`: name the affected package in the title and scope. `multi-repo`: create the item in the repository that owns the fix and link the others.
- `delivery.default_branch`: code is read at `origin/<default>`; detect with `git symbolic-ref --short refs/remotes/origin/HEAD`.
Current values appear in the `[Skill config]` block when the skill loads; an unset key shows its declared default. Persist a detected value with `hermes config set skills.config.<key> <value>` (per profile: `hermes -p <profile> config set …`); `hermes config migrate` prompts for keys still unset.

## Procedure
1. **Gather the data before writing.** Keep the actual request and response, copy log lines, query the rows, read the code at a freshly fetched `origin/<default>`. Never write "it seems that".
2. **Search for duplicates** in item bodies, never titles alone, open and closed (on github the issues API returns PRs too: filter them out), with keywords that name a specific artifact: a file, config key, endpoint, error string, function. Generic words match everything. Read the lines around each hit, then: same root cause, add your data there, never a second item; adjacent cause, a new item stating why it is not the other one; closed and back, reopen with the new evidence. Prove the search can find: a phrase you know exists is found, nonsense is not.
3. **Write the body in this order:**
   1. **Context / why**: who is affected, which flow, what it costs.
   2. **Real data**, leading with the measurement: the command run and its actual output, request with payload, error body, log excerpts with timestamps, relevant rows (identifiers, never sensitive contents), the primary source quoted at `file:line`. Add what you tried that did not work: an obvious fix that made it worse is written down so nobody merges it blind.
   3. **Repro steps**: numbered, from a clean state, exact enough to paste.
   4. **Expected versus actual.**
   5. **Acceptance criteria**: testable checkboxes, including which end-to-end flows are added or updated.
   6. **Links**: related items and PRs by full URL, code permalinked at a SHA. Reference related items without auto-closing keywords: closing is the owner's call.
   7. **Data change**: "none", or the existing rows that must change, per environment.
   8. **Open questions**, each addressed to the product lead or the technical owner. A real trade-off is stated as the decision needed, never answered by you.
4. **Title** in the glossary's terms: `<area>: <observable problem or outcome>`, naming the finding, not just the area.
5. **Split multi-part work** into child items, each a shippable unit.
6. **Priority with a one-line reason**: data integrity and anything moving money or permissions, then user-facing breakage, then operator convenience, then polish. Size ranks; it never becomes a status.
7. **Capture in-passing reports now**, with data, before they evaporate. Every verified finding not fixed in this turn becomes an item, non-code ones included (contradicting documents, brand or voice drift, wrong asset dimensions, stale claims, missing access): a finding reported only in chat is lost. Something fixed in this turn is a PR, not an item.
8. **Re-read it as the developer.** If you would ask anything, it is not done.
9. **After filing**: re-read the item from the tracker (title, labels, full body). When the tracker's items sit on a board with a status field, place it with a status. If the finding changes durable context (a decision record, the knowledge base), update that in the same pass. If an earlier claim of yours was wrong, correct it in the item.

## Output standard
The item's URL (or file entry id, or "in report" when the tracker is `none`) on its own line as plain text, never in a code block, so chat clients make it tappable; priority and size with the reason; and the duplicate searches you ran.

## Traps
- A paraphrased error is useless; the error body is the report.
- Code cited at a moving branch shifts under the reader; permalink at the SHA.
- A hard-coded expected test total goes stale at the next merge; name tests or flows.
- An item that silently assumes a product decision ships that assumption.
- An obvious fix written as code by the product manager skips every gate; write it as a precise item.
- One root cause per item: a batch of findings in one item can never be closed.
- A duplicate search that returned nothing proves nothing until it is shown finding something.
