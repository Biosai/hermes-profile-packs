---
name: one-to-one-email-send
description: "Send approved one-to-one emails from the owner's mailbox"
metadata:
  hermes:
    tags: [workflow]
    config:
      - {key: publishing.mailbox, description: "Owner's mailbox for one-to-one sends: gmail, microsoft365, other, none", default: "none"}
      - {key: publishing.approval, description: "How the owner's approval is captured: hermes-approval or explicit-message", default: "explicit-message"}
      - {key: owner.channel, description: "Where questions and owner actions reach the owner", default: "this conversation"}
      - {key: venture.brief, description: "Path or URL of the brief: customer, voice, constraints, autonomy", default: ""}
    prerequisites:
      commands: [python3]
---
# One-to-One Email Send

Short personal emails to a small, known list (a feedback ask to past signups, a note to
testers), sent from the owner's own mailbox after the owner approves the exact wording, then
reading the replies. Newsletters, flows and campaigns use `email-send-with-approval`. Every
rule of `approval-gated-publishing` applies.

## Trigger
The owner approved, or asks for, personal emails to a small known list (past signups,
churned users, testers), or the replies to such a send need reading.

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| Read access to the list's source of truth (user store, CRM or email platform events) | build the list and check consent | one count query returns |
| Send and read access to the owner's mailbox, when `publishing.mailbox` is not `none` | send, verify, read replies | the mailbox's send-as identities can be listed |

If a required prerequisite is missing, stop before step 1. Say which one, what it blocks, and
the smallest access that would unblock it (read-only first). With `publishing.mailbox` set to
`none`, do steps 1 to 3 and hand the owner the messages to send; never claim a send.

## Configuration
- `publishing.mailbox`: the integration that sends in the owner's name. `other`: ask which
  tool and say what you used.
- `publishing.approval`: how the OK on the exact text is captured (`approval-gated-publishing`).
- `venture.brief`: where the consent basis and the read-out rule are recorded.
- Set values with `hermes config set skills.config.<key> <value>`.

## Always
- The owner's explicit OK on the exact text before anything leaves. Changing the wording,
  sender address or list after the OK needs a new OK.
- Never paste addresses or names into the chat, notes or work items: counts and anonymised
  rows (R1, R2) only.
- One email per recipient; never several people in To, Cc or Bcc.
- The agent never answers the replies: they are the owner's. The agent reads and codes them.
- Consent sets the type of email. Check marketing consent per person on the person's record
  (list and event payloads often omit it). With few consented, the message is a personal
  service or feedback email about the person's own account: no offer, no link, no tracking
  pixel. State this basis for the owner to approve.
- Exclude likely minors (school domains) and internal accounts (the team's own domains, test
  markers) before drafting.

## Steps
1. Build the list from the source of truth with the exclusions. Store it with owner-only
   permissions where it survives until the send (scratch folders may be pruned in between).
   Take each person's language from the signup data when the profile field is empty.
2. Draft per language, in the owner's first person, gender-neutral toward the reader where
   the language genders. Make replying easy: numbered options built from the measured
   drop-off reasons, plus an open "something else". If most first names are empty, use a
   plain greeting. Paste every full draft inline in the approval request.
3. Fix the read-out rule before sending (e.g. "three or more naming the same detail: next
   product decision; fewer than three replies: 'no signal', not 'no problem'") and record it.
4. Check the sending identity: the approved From address must be an accepted send-as identity
   of the mailbox. If not, stop and ask the owner to add it. Never send from another brand's
   address: it changes what was approved and reads as phishing.
5. Dry run: assert the count, no duplicates, no excluded domains, and print one rendered
   sample per variant; compare them with the approved text.
6. Send one message per recipient, a few seconds apart, idempotently: a send log skips anyone
   already sent, so a rerun after a failure never doubles.
7. Verify in the mailbox, not from the exit code: read back the From header and sent state of
   every message, search for bounces (e.g. `from:(mailer-daemon OR postmaster)`) and note each
   reason; tell bounce, auto-reply and person apart before counting a reply.
8. Schedule the read-outs (e.g. an interim at day 7, the verdict at day 14) with a read-only
   reply reader that strips addresses, and record the send (counts, variants, bounces,
   read-out dates) on the work item.

## Done when
- Each approved recipient got exactly one message from the approved address, verified in the
  mailbox, and bounces are counted with their reasons.
- The read-out rule and dates are recorded, and no address or name left the mailbox.

## Output standard
```
Sent <n>/<N> (<variant counts>) from <approved identity>; bounces <b> (<reasons>)
Read-out rule: <rule>. Interim <date>, verdict <date>. Recorded: <link>
```
