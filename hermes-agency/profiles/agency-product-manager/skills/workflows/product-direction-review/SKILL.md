---
name: product-direction-review
description: "Decide what to build next to make the product stick"
metadata:
  hermes:
    tags: [workflow]
    config:
      - {key: venture.brief, description: "Path or URL of the brief: customer, voice, constraints, autonomy", default: ""}
      - {key: delivery.issue_tracker, description: "Where work items go: github, gitlab, jira, linear, file, none, or detect", default: "detect"}
      - {key: delivery.issue_file, description: "Markdown file for work items when the tracker is file", default: ""}
      - {key: owner.channel, description: "Where questions and owner actions reach the owner", default: "this conversation"}
    prerequisites:
      commands: [git]
---
# Product Direction Review

Acting as product lead: value for users, usefulness, return visits, and what to build. The
answer is a short ranked list tied to measured steps, not a feature wish list.

## Trigger
The owner asks how to make the product more useful or stickier, proposes a feature ("should
we add X in beta?"), asks how the product is more than a wrapper around a general tool, or
asks to document the product vision and act on it.

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| The brief and the latest product notes (return diagnosis, competitor map, strategy review) | the review builds on measured state | `venture.brief` opens; the notes are found from it |
| Read access to the product's code, before proposing a build | what already exists | a shallow clone or the code host's search works |
| Write access to the tracker, for step 7 | one item per action | edit one item, or `delivery.issue_file` is writable |

If a required prerequisite is missing, stop before step 1. Say which one, what it blocks, and
the smallest access that would unblock it (read-only first). Do the parts that do not need it
only if they still make sense alone. Never report "nothing exists" when the code could not be
read.

## Configuration
- `venture.brief`: where the product's principles, customer and notes live. Unset: ask.
- `delivery.issue_tracker` / `delivery.issue_file`: where step 7 files items; `none`: the
  items stay in the reply and the note. `detect`: from `git remote get-url origin`, say so.
- `owner.channel`: where the one decision is asked. In a channel split into topics with
  roles, answer in the product topic with the product state; owner-action reminders belong
  where the owner expects them, not at the top of a product conversation.
- Set values with `hermes config set skills.config.<key> <value>`.

## Steps
1. **Read the record first** and quote the cohort size. With fewer than about ten outside
   users who reached the core use, retention is not measurable yet: recruiting testers is
   then the lever for product learning, not only for acquisition.
2. **Compare usage frequency with the market leaders' core loop, not their features.** How
   often does the user's problem recur, and does the product sit on that recurrence? A
   problem that recurs many times a day is won by a seconds-long in-and-out loop; a session
   product serves an occasional need.
3. **Find where the first session ends.** When the value lands outside the product later,
   the product needs a loop back to that moment (an outcome check-in) on the channel that
   actually reaches users: count each channel's reach per outside user first.
4. **Check the code for what already exists** before proposing a build. Re-ordering an
   existing capability is far cheaper. Say "read in code, not verified end to end" until it
   is probed in production.
5. **A proposed feature gets four tests before any yes:** the rules of the platform where the
   output is used (read, labelled primary or third-party source); the product's own stated
   principles (a feature that contradicts them is a no even if it sells); whether competitors
   already sell it (a commodity is no edge); how often it is used (a one-off use does not fix a
   return problem). Then offer the version that already exists in principle.
6. **"More than a wrapper?" gets an honest two-column split.** Not an edge: infrastructure and
   prompt know-how (copyable in an afternoon), the model (the user can buy the same one). An
   edge: what a general tool structurally does not do (reach out first, remember each case
   over weeks, sit on the recurring moment, learn what worked for this user). Mark which
   rows are reachable at today's volume.
7. **Answer, and document when asked.** At most three builds, ranked, each tied to the funnel
   step it serves with one metric, its baseline and a pre-written kill rule; then what the
   owner may have missed, what is dropped, and ONE decision with a recommendation. To
   document the vision, file the items first (they carry the numbers the note cites), each
   searched for duplicates across open and closed:
   - a build: why (with the measured number), scope, not in scope, a feature gate (step,
     metric, baseline, read date, remove-if rule), done-when with proof and a production
     check, and any precondition ("not before the first returning user");
   - an owner-only step (deploy, a setup only possible in a vendor's UI, a merge): an owner
     action with exact steps and what it blocks. Merged but undeployed work gets its own
     deploy action: until then the gate's read date counts down on code nobody runs.

   Then the note, in the brief's knowledge base on a fresh branch: the awkward number first
   and that everything below is hypothesis; the thesis and a "substitute vs us" table; the
   smallest changes first, each mapped to an item; decisions (question, answer, why, date);
   plan (item, owner, state, link); how we will know; what is dropped. Link note and items
   both ways in the same turn.
8. **On "go"**, build through the `issue-to-merge` workflow.

## Done when
- The owner has at most three ranked builds, each with a metric, a baseline and a kill rule,
  the dropped list, and one decision to make.
- When documenting: every action has its own item, the note and the items link to each other,
  and the reply gives the link, the ordered list with owners, and the number that decides.
