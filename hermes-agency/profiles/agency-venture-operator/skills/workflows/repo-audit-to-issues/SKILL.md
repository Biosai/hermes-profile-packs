---
name: repo-audit-to-issues
description: "Audit a repository into ranked, deduplicated findings"
metadata:
  hermes:
    tags: [workflow]
    config:
      - {key: delivery.code_host, description: "Where code is reviewed: github, gitlab, bitbucket, other, or detect", default: "detect"}
      - {key: delivery.repo_layout, description: "Repository layout: single, monorepo, multi-repo, or detect", default: "detect"}
      - {key: delivery.repos, description: "Working copies this profile may read or change, comma-separated", default: ""}
      - {key: delivery.default_branch, description: "Default branch name, or detect", default: "detect"}
      - {key: delivery.issue_tracker, description: "Issue tracker: github, gitlab, jira, linear, file, none, or detect", default: "detect"}
      - {key: delivery.issue_file, description: "Markdown file for work items when the tracker is 'file'", default: ""}
    prerequisites:
      commands: ["git"]
---
# Repo Audit to Issues

Use for "audit this repo", "what is broken", "what should I work on next", a repository nobody
has run for months, a scheduled sweep the owner asked for, a finding made during a task that
does not fit that task's scope, and before you assert that something is broken in a repository
you have not run. The output is findings, never a pull or merge request: the owner chooses what
gets built. When the ask is the work still missing rather than what is broken, use
`remaining-work-to-issues`.

## Trigger
A venture repository is taken on, or the owner asks for an audit or for what to work on next.

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| Read access to the repositories in `delivery.repos` | evidence by execution | `git -C <repo> fetch --dry-run` |
| The project's toolchain, at the versions CI pins | run tests and builds as CI does | the documented test command starts |
| CI run history and log read access on the code host | what CI actually ran, every run | e.g. `gh auth status`, `glab auth status` |
| Write access to the tracker, when `delivery.issue_tracker` is not `none` | file findings | create-permission check in the tracker |

If a required prerequisite is missing, stop before step 1. Say which one, what it blocks, and
the smallest access that would unblock it (read-only first). Never report "no findings" for
an area you could not read or run.

## Configuration
- `delivery.repos`: empty means the current directory only. `delivery.repo_layout`:
  `monorepo` scopes the audit, test runs and CI filters to the packages in question;
  `multi-repo` audits each repository and links related findings. `detect`: workspace files
  (package workspaces, build-tool modules) suggest a monorepo; say what you concluded.
- `delivery.default_branch`: audit the default branch as fetched; `detect` with
  `git symbolic-ref --short refs/remotes/origin/HEAD`. Never assume a name.
- `delivery.code_host`: decides the CLI and the words; `detect` from `git remote get-url origin`.
- `delivery.issue_tracker`: where findings go. `file` appends to `delivery.issue_file`;
  `none` keeps them in the report only; `detect` uses the code host's tracker if enabled. When
  existing items sit on a board or project view with a status field, new ones go there too,
  each with a status: an item without one is hidden from the default grouped view.
- Set values with `hermes config set skills.config.<key> <value>`.

## Steps
1. Fix the scope: which repositories or packages, which question (security, reliability,
   cost, dead code, a funnel step). One audit, one question.
2. Survey the whole surface first: every repository in `delivery.repos` and its open items,
   not only the one you were pointed at. On github an open-issue count includes pull
   requests, and the issues API returns them too: filter them out before counting.
3. Collect evidence by execution on a fresh fetch of the default branch: run the tests, build
   from clean, call the endpoint, read the deployed configuration. For CI, count the
   conclusion of every run in the history, not the latest one: "never green since the first
   run" is a different finding from "the last run failed". Expired CI logs are not a finding:
   reproduce locally with the runner's shape (runtime version, package manager, script name).
4. Run the obvious fix before you propose it, and write its measured effect into the item. A
   fix that makes things worse becomes a do-not-merge-blind warning in the body. Back up what
   you change for the experiment, restore it, and prove `git status --porcelain` is empty.
5. Add a positive control per finding: the probe passes where the problem is absent, and a
   scan that found nothing is shown finding something it should. Techniques:
   `references/evidence-techniques.md`. Public surfaces (site, accounts, links, domains) make
   claims too: `references/public-surface-audit.md`.
6. Deduplicate against existing items by their bodies, open and closed, with keywords that
   name a specific artifact (a file, a config key, an error string); read the lines around
   each hit. Same root cause: add the evidence there. Adjacent cause: a new item that says why
   it is not the other one. Closed and back: reopen with the new evidence. Prove the search
   can see: a phrase you know exists is found, nonsense is not; on an empty tracker, run the
   same query on a sibling repository known to hold items, and name it in the report.
7. One item per decision, closable by fixing one thing: two symptoms of one root cause are
   one item; one symptom hiding two blockers is two. The body carries the finding with the
   date and commit it was measured on, the real output verbatim (never paraphrased), the root
   cause quoting `file:line`, what a fix must decide (a choice, not a disguised
   recommendation) and a scope of checkboxes that can each be proved done. Link related items
   without auto-closing keywords: closing is the owner's call. An item that contradicts or
   supersedes an existing one says so, and the report flags it.
8. File: create the labels before the first item (an unknown label is silently dropped),
   labelled by who can unblock it. Re-read every filed item from the tracker: title, labels,
   full body. On a board, check each item by number with a status, never the board's total.
   Wording, matrix and backlog rules: `references/filing-discipline.md`.
9. Rank by how directly each blocks the venture's binding constraint, and by who can unblock
   it: owner-only actions (a console click, a DNS record, a paid scope) apart from work the
   agent can do. When the owner says they cannot act now, lead with the agent's work and
   list the parked items in one line.

## Done when
- Every finding is recorded once where `delivery.issue_tracker` says (in the report when
  `none`), ranked, with evidence and a positive control, and re-read from the tracker.
- The working tree is as you found it, proved clean.
- No pull or merge request was opened: an audit produces findings, not changes.

## Output standard
```
Symptom: <what happens>
Evidence: <command> -> <output excerpt>; control: <command> -> <expected output>
Impact: <who or what it hurts>   Likely fix: <...> (size: S/M/L)
```
Report: what was reproduced (with the numbers), what you did not touch, and one next action
offered as a question. Ranked links, one per line, as plain text rather than in a code block,
so chat clients make them tappable. State uncomfortable numbers flatly.

## Traps
- Reading a green badge as "tests pass": open the log and count the tests that ran. A test
  target with zero test files passes in every framework.
- A green job proves a tool ran in that job; a sibling job may call it where it is not
  installed. Check which job installs what.
- A repository's docs saying a gate passes are a claim: paste the gate's output or say "not run".
- After a platform migration, grep the product and marketing docs (vision, mission,
  positioning) too: the sentences that open a venture are the ones nobody re-reads.
- A credential rotated mid-audit: a running process keeps the old value. Compare fingerprints
  of each source (never the value) and probe old and new before trusting a result.
- An owner decision that invalidates part of a filed item gets a comment on that item saying
  which part of the analysis was wrong; the correction does not stay in chat.
- Twenty low-severity findings burying the one that matters. Rank, and say which one.
