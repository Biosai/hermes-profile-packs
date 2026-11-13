---
name: approval-gated-publishing
description: "Draft freely; publish or send only after owner approval"
metadata:
  hermes:
    config:
      - key: publishing.approval
        description: "How the owner's approval is captured: hermes-approval or explicit-message"
        default: "explicit-message"
      - key: project.brief
        description: "Path or URL of the brief: customer, voice, constraints, autonomy"
        default: ""
      - key: owner.channel
        description: "Where questions and owner actions reach the owner"
        default: "this conversation"
---
# Approval-Gated Publishing

Use when anything would be seen outside: a social post, a community announcement, an email campaign or flow, a listing, an ad or a boost. Drafts are free. Publishing, sending, scheduling, listing and spending wait for the owner's approval of that exact item.

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| The project brief (`project.brief`), or the owner's answer on audience and voice | voice, allowed claims, accounts | the brief opens |
| A write path to the account, for direct publishing | publishing after approval | a read call on the account succeeds |
| Draft access in the email platform, for email | drafts and test sends | listing drafts succeeds |

If one is missing, stop before step 1 and say which, what it blocks, and the smallest access that would unblock it. A missing write path is not a blocker: prepare the handoff of step 7 and say so. Never claim an item went out.

## Configuration
- `publishing.approval`: `hermes-approval` submits each outward action through Hermes's approval prompt and proceeds only on approve. `explicit-message` asks where `owner.channel` says and proceeds only on a message approving that exact item.
- `project.brief`: unset means ask the owner for audience, voice and allowed claims before drafting. Never borrow another brand's.
- Set values with `hermes config set skills.config.<key> <value>`.

## Procedure
1. Read the brief. When one owner runs several brands, each draft belongs to exactly one: never mix their voice, facts, numbers or handles.
2. Source every fact and number to the record: a link, or a measured metric with its date. Followers, users, revenue, quotes and testimonials are measured or omitted.
3. Draft for the channel: length, format, alt text, tracked links. For email, apply [the email rules](references/email.md), consent first.
4. Check the draft: links open, names are right, no placeholder remains, no claim goes beyond the brief.
5. Ask for approval per `publishing.approval`, one item at a time, with [the approval request](references/approval-request.md): the final content in full, never a link and a summary.
6. After approval only: publish, send, schedule or switch the flow live. Open the live result, check it, and record the link, the time and the approval reference.
7. With no write path, hand the owner a package: the final text ready to paste, apart from any commentary, media with alt text, checked links, the account and the time. Ask for the live link afterwards.
8. Read results from the platform's own numbers, read-only, after the agreed window.

## Decision rules
- Approval covers one exact version: a change of wording, sender, audience or time goes back for approval.
- Only an explicit approval of that item counts, not silence, a reaction or a relayed "looks good".
- Never publish from a mode that skips approvals (`hermes -z` one-shot runs, `--yolo`), not even to test the gate. A gate that looks broken is reported, and the work stops.
- A send or schedule call that failed unexpectedly is never retried or routed another way: each retry may reach real people. Hand the step to the owner. [When the gate or a send misbehaves](references/gate-and-send-failures.md) covers this, a call the gate does not ask on, and a schedule the owner set.
- "Queued" or "handed off" is not "published"; "scheduled" is said only after reading the item back.
- An email flow is tested with the owner's own address while it is off, never by switching it live.
- No engagement bait, fake urgency, bought followers or automated replies posing as people.

## Quality gate
Done when every item has one stated status (draft, awaiting approval, approved with its reference, published with its link, or measured), nothing went out without approval of its exact version, and each published item was checked live. The report gives each item's record as laid out in the approval request reference.
