---
name: owner-action-handoff
description: "Hand the owner a fully prepared action, then ask"
metadata:
  hermes:
    tags: [workflow]
    config:
      - key: owner.channel
        description: "Where questions and owner actions reach the owner"
        default: "this conversation"
      - key: owner.action_tracker
        description: "Where a waiting owner action is recorded: issue-tracker, file, conversation"
        default: "conversation"
      - key: delivery.issue_tracker
        description: "Issue tracker: github, gitlab, jira, linear, file, none, or detect"
        default: "detect"
      - key: delivery.issue_file
        description: "Markdown file for work items when the tracker is 'file'"
        default: ""
      - key: delivery.board
        description: "Where work is claimed: hermes-kanban, tracker, or none"
        default: "none"
    prerequisites:
      commands: ["hermes"]
---
# Owner Action Handoff

Hands the owner a step only the owner can do, fully prepared, then asks. A missing permission is an owner action, never something to work around.

## Trigger
A step needs the owner's own hands (deploying, merging, a console, a payment, signing up for an account, granting access, signing, publishing by hand, contacting people), a tool, token or permission is missing, or the owner answers work that was blocked on them.

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| Write access to the issue tracker, when `owner.action_tracker` is `issue-tracker` | record the action | its CLI or API is authenticated (github: `gh auth status`; gitlab: `glab auth status`) |
| Write access to `delivery.issue_file`, when `delivery.issue_tracker` is `file` | record the action | the file is writable |
| The `hermes` CLI, when `delivery.board` is `hermes-kanban` | mark and complete blocked work | `hermes kanban list` answers |

If one is missing, stop before step 1 and say which, what it blocks, and the smallest access that would unblock it. Preparing the package still makes sense alone: deliver it where `owner.channel` says, labelled "not recorded in the tracker".

## Configuration
- `owner.action_tracker`: `issue-tracker` opens an item in `delivery.issue_tracker` (`detect`: from `git remote get-url origin`, saying what was detected). `file` appends to `delivery.issue_file`. `conversation` keeps the action where `owner.channel` says and repeats it in each status until it is done.
- `delivery.board`: where blocked work is marked. `hermes-kanban`: on the card, with the commands of [work blocked on the owner](references/blocked-work.md). `tracker`: with the tracker's own status. `none`: skip the board steps and say so.
- Set values with `hermes config set skills.config.<key> <value>`.

## Steps
1. Look for an existing record of the same action (search item bodies, open and recently closed) and update it instead of creating a twin.
2. Prepare [the package](references/package.md), everything the owner needs to finish in one sitting: the exact command, link or console path with every value filled in, the final draft or form contents, the cost and what is irreversible, and what the owner should see when it worked.
3. Record it where `owner.action_tracker` says, labelled owner-action and titled with the action as a verb: one action per record, with its steps and a done-when the agent can check. An ask split out of a larger item gets its own record, linked from the parent.
4. Then ask, in one line where `owner.channel` says: the action and the link. Mark the work it holds up as blocked, where `delivery.board` says.
5. When the owner reports it done, verify it yourself (re-fetch, re-run, read the live state), close the record with the evidence, and unblock the work.
6. When the owner answers work that was blocked on a question, record the answer verbatim on it and the decision where decisions live (`decision-log`), then complete the work with the outcome, as the blocked-work reference says.

## Decision rules
- Prepare first, ask second: an owner who opens the record must not find a to-do list.
- Never work around the missing step: no other account, no borrowed token, no mode that skips approvals (`hermes -z` one-shot runs and `--yolo` both bypass them).
- Never paste a secret into the record. Point to where the owner keeps it.
- When the agent writes to the tracker under the owner's own account, the tracker does not notify the owner: the one-line ask is the notification.
- When work you own finishes or blocks, send one short message: the outcome with its links, the whole question (`owner-question-protocol`), or the owner action with its link. Automatic notifications are often truncated.
- Work that already produced a pull or merge request is completed with the answer, never restarted: restarting duplicates it. If the answer still needs something only the owner can give, the work stays blocked on that action.
- A reminder of an owner action goes where the owner expects it, never at the top of a conversation about something else.

## Done when
- The owner has one message with everything prepared, the exact ask, and where it is recorded.
- The action stays recorded as `owner.action_tracker` says until the owner confirms it and the agent has verified it, and the waiting work resumes from there.
