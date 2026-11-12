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

Use when a step needs the owner's own hands (deploying, merging, consoles, payments, signing
up for accounts, granting access, signing, contacting people) or a tool, token or permission
is missing, and when a work card finishes, blocks or receives the owner's answer. A missing
permission is an owner action, never something to work around.

## Trigger
A step needs something only the owner can do: deploy, merge, console access, a payment, an account, publishing outside the approval gate, or contacting people.

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| Write access to the tracker, when `owner.action_tracker` is `issue-tracker` | record the action | the tracker CLI or API is authenticated (e.g. `gh auth status`, `glab auth status`) |
| Write access to `delivery.issue_file`, when the tracker is `file` | record the action | the file exists and is writable |
| Board access, when `delivery.board` is `hermes-kanban` | card steps | `hermes kanban list` answers |

If a required prerequisite is missing, stop before step 1. Say which one, what it blocks, and
the smallest access that would unblock it. Preparing the package still makes sense alone:
deliver it in `owner.channel`, labelled "not recorded in the tracker".

## Configuration
- `owner.action_tracker`: `issue-tracker` opens an item in `delivery.issue_tracker`
  (`detect`: from `git remote get-url origin`, say what you detected); `file` appends to
  `delivery.issue_file`; `conversation` keeps it in `owner.channel` and repeats it in each
  status until it is done.
- `delivery.board`: `hermes-kanban` uses the card commands below; `tracker` uses the
  tracker's own status; `none` skips every card step and says so.
- Set values with `hermes config set skills.config.<key> <value>`; `hermes config migrate`
  asks for unset ones.

## Steps
1. Look for an existing record of the same action (search item bodies, open and recently
   closed) and update it instead of creating a twin.
2. Prepare everything the owner needs to finish in one sitting: the exact command, link or
   console path with every value filled in; the final draft or form contents; the cost and
   what is irreversible; what the owner should see when it worked.
3. Record it where `owner.action_tracker` says, labelled owner-action and titled with the
   action as a verb ("Merge the checkout fix"): one action per record, with its steps and a
   done-when the agent can check. An ask split out of a larger item gets its own record,
   linked from the parent.
4. Then ask, in one line in `owner.channel`: the action and the link. Block the work it
   holds up. When the agent writes to the tracker under the owner's own account, the tracker
   does not notify the owner: this message is the notification.
5. When the owner reports it done, verify it yourself (re-fetch, re-run, read the live
   state), close the record with the evidence, and unblock the work.

## Work cards
- When a card you own finishes or blocks, post ONE short message: on completion the outcome
  and its links; on a block the whole question (`owner-question-protocol`) or the owner
  action with its link. Automatic notifications are often truncated.
- When the owner answers a blocked card: record the answer verbatim on it, record the
  decision where it lives, then complete it with the outcome and the decision. With
  `hermes-kanban`: `hermes kanban comment <id> "<answer>"`, then
  `hermes kanban complete <id> --result "<outcome: decision>"`.
- Complete an answered card; never unblock or restart it when its work already produced a
  pull or merge request: restarting duplicates the work, and with `hermes-kanban` an unblocked
  card whose comments link a pull request can sit `ready` without ever being picked up. If the
  answer still needs something only the owner can give, keep it blocked on that action.
- In a channel split into topics with their own roles, send owner-action reminders to the
  topic where the owner expects them; never open another topic's conversation with them.

## Done when
- The owner has one message with everything prepared, the exact ask, and where it is recorded.
- The action stays recorded per `owner.action_tracker` until the owner confirms it is done, and the waiting work resumes from there.

## Output standard
```
Why: <what this unblocks>
Do: <numbered steps, every value filled in>
Cost / irreversible: <...>
Check: <what you should see when it worked>
After: <what the agent verifies and continues>
```

## Traps
- Asking first and preparing later: the owner opens the record and finds a to-do list.
- Working around the missing step: another account, a borrowed token, or a mode that skips
  approvals (`hermes -z` one-shot runs and `--yolo` both bypass them).
- A secret pasted into the record. Point to where the owner keeps it.
