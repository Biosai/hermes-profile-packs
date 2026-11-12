---
name: approval-gated-publishing
description: "Draft freely; publish or send only after owner approval"
metadata:
  hermes:
    config:
      - key: publishing.approval
        description: "How the owner's approval is captured: hermes-approval or explicit-message"
        default: "explicit-message"
      - key: venture.brief
        description: "Path or URL of the brief: customer, voice, constraints, autonomy"
        default: ""
      - key: owner.channel
        description: "Where questions and owner actions reach the owner"
        default: "this conversation"
---
# Approval-Gated Publishing

Use for anything that would be seen outside: social posts, community announcements, email
campaigns and automated flows, directory or marketplace listings, ads and boosts. Drafts are
free. Publishing, sending, scheduling, listing and spending happen only after the owner (the
person accountable for the brand or account) approves that exact item.

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| The brand's brief (`venture.brief`) or the owner's answer on audience and voice | voice, allowed claims, accounts | the brief opens |
| A write path to the account (integration, API or tool), for direct publishing | publishing after approval | a read call on the account succeeds |
| Draft access in the email platform, for email | drafts and test sends | listing drafts or templates succeeds |

If a required prerequisite is missing, stop before step 1. Say which one, what it blocks, and
the smallest access that would unblock it. A missing write path is not a blocker: prepare a
manual handoff (step 7) and say there is no write path. Never claim an item went out.

## Configuration
- `publishing.approval`: `hermes-approval` submits each outward action through Hermes's
  approval prompt and proceeds only on approve; `explicit-message` asks in `owner.channel`
  and proceeds only on a message that approves that exact item.
- `venture.brief`: unset means ask the owner for audience, voice and allowed claims before
  drafting; never borrow another brand's.
- Set values with `hermes config set skills.config.<key> <value>`.

## Procedure
1. Read the brief. When one person runs several brands, each draft belongs to exactly one;
   never mix their voice, facts, numbers or handles.
2. Source every fact and number to the record (a link, a measured metric with its date).
   Followers, users, revenue, quotes and testimonials are measured or omitted.
3. Draft for the channel: length, format, alt text, tracked links; for email a plain-text
   part, a working unsubscribe link and an honest sender. No proof of consent, no mailing.
4. Check: links open, names spelled right, no placeholders, no claim beyond the brief.
5. Ask for approval per `publishing.approval`, one item at a time: brand, channel, audience
   and size, proposed time, final content, sources, what will be measured. Any change of
   substance after approval goes back for approval.
6. After approval only: publish, send, schedule (sending later) or switch the flow live.
   Open the live result, check it, record the link, time and approval reference.
7. No write path: give the owner a ready-to-post package (final text, media with alt text,
   checked links, account and time) and ask for the live link afterwards.
8. Read results from the platform's own numbers, read-only, after the agreed window.

## Output standard
```
<brand> / <channel> / proposed <date time>
<final content or link to the draft>
Audience: <segment, size, consent basis for email>   Sources: <links>
Status: draft | awaiting approval | approved (<ref>) | published (<link>) | measured
```

## Traps
- Testing the gate by bypassing it: never publish from a mode that skips approvals
  (`hermes -z` one-shot runs, `--yolo`). If the gate looks broken, report it and stop.
- Silence, a reaction or a relayed "looks good" treated as approval.
- "Queued" or "handed off" reported as "published".
- Switching an email flow live to test it. Test with the owner's own address while it is off.
- Engagement bait, fake urgency, bought followers or automated replies posing as people.
