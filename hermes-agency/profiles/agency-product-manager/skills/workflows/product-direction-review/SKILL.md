---
name: product-direction-review
description: "Decide what to build next from evidence, and record it"
metadata:
  hermes:
    tags: [workflow]
    config:
      - {key: project.brief, description: "Path or URL of the brief: customer, voice, constraints, autonomy", default: ""}
      - {key: delivery.issue_tracker, description: "Where work items go: github, gitlab, jira, linear, file, none, or detect", default: "detect"}
      - {key: delivery.issue_file, description: "Markdown file for work items when the tracker is file", default: ""}
      - {key: owner.channel, description: "Where questions and owner actions reach the owner", default: "this conversation"}
    prerequisites:
      commands: [git]
---
# Product Direction Review

Sequences the product manager's own skills into one review: gather the evidence, decide with `roadmap-decision`, record the direction. It adds only what those skills leave open.

## Trigger
The owner asks how to make the product more useful or more used, proposes a feature, asks what the product has that an alternative lacks, or asks to document the product direction and act on it.

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| The project brief and the latest product notes | the review builds on measured state | `project.brief` opens; the notes are found from it |
| Read access to the product's code, before proposing a build | what already exists | a shallow clone or the code host's search works |
| Write access to the issue tracker, for step 7 | one item per action | edit one item, or `delivery.issue_file` is writable |

If one is missing, stop before step 1 and say which, what it blocks, and the smallest access that would unblock it (read-only first). Never report "nothing exists" when the code could not be read.

## Configuration
- `project.brief`: where the product's principles, customer and notes live, and where the direction note is written. Unset: ask.
- `delivery.issue_tracker` and `delivery.issue_file`: where step 7 files items. `none`: the items stay in the reply and the note. `detect`: from `git remote get-url origin`, saying so.
- `owner.channel`: where the one decision is asked.
- Set values with `hermes config set skills.config.<key> <value>`.

## Steps
1. Gather the evidence. Read the brief and the latest notes, and quote how many outside users reached the core use. Where a risky assumption has no evidence, plan its cheapest test with `product-discovery` instead of guessing.
2. Run [the evidence checks](references/evidence-checks.md): how often the user's problem recurs against how often the product is used, and where the first session ends.
3. Check the code for what already exists before proposing a build. Say "read in code, not verified end to end" until it is probed in production.
4. Put a proposed feature through the four tests of the evidence checks before any yes, then offer the version that already exists in principle.
5. Decide with `roadmap-decision`, capped at three outcomes for the horizon. Rank competing candidates with `prioritization`.
6. Answer the owner: the ranked outcomes, each tied to the step it serves with one metric, its baseline and a kill rule written in advance; what the owner may have missed; what is dropped; and one decision, with a recommendation, asked where `owner.channel` says.
7. When asked to record the direction, follow [recording the direction](references/recording-the-direction.md): file the items first, to the standard of `issue-authoring-standard`, then write the note in the project brief, and link note and items both ways in the same turn.
8. On the owner's go, cut the first release with `release-scope` and hand the items to delivery: the orchestrator profile's `issue-to-merge` workflow when it is installed, otherwise the team's own delivery process.

## Decision rules
- With fewer than about ten outside users who reached the core use, retention cannot be measured yet: recruiting testers is then the lever for product learning.
- Re-ordering an existing capability is far cheaper than a build.
- A feature that contradicts the product's own stated principles is a no, even if it would sell.
- A one-off use does not fix a return problem, and what competitors already sell is no edge.
- What the product has that an alternative lacks is the product strategist's `moat-analysis` when that profile is installed; otherwise answer with the two-column split of the evidence checks.
- An owner-only step (a deploy, a setup in a vendor's console, a merge) is recorded as an owner action with exact steps. Merged work that is not deployed gets its own: until it runs, a gate's read date counts down on code nobody uses.
- A product question is answered with the product state first, not with reminders of pending owner actions.

## Done when
- The owner has at most three ranked outcomes, each with a metric, a baseline and a kill rule, the dropped list, and one decision to make.
- When recording: every action has its own item, the note and the items link to each other, and the reply gives the link, the ordered list with owners, and the number that decides.
