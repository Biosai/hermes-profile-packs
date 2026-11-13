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
      - {key: project.brief, description: "Path or URL of the brief: customer, voice, constraints, autonomy", default: ""}
    prerequisites:
      commands: [python3]
---
# One-to-One Email Send

Sends short personal emails to a small, known list from the owner's own mailbox, each send covered by `approval-gated-publishing`, then reads the replies. Newsletters, automated flows and campaigns use the `email-send-with-approval` workflow.

## Trigger
The owner asks for, or has approved, personal emails to a small known list, or the replies to such a send need reading.

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| Read access to the list's source of truth (user store, CRM or email platform) | build the list, check consent | one count query returns |
| Send and read access to the owner's mailbox, unless `publishing.mailbox` is `none` | send, verify, read replies | the mailbox's sending identities list |
| `python3`, for the dry run and the send log | repeatable sends | `python3 --version` |

If one is missing, stop before step 1 and say which, what it blocks, and the smallest access that unblocks it (read-only first). With `publishing.mailbox` set to `none`, do steps 1 to 5 and hand the owner each message ready to paste, apart from any commentary. Never claim a send.

## Configuration
- `publishing.mailbox`: the integration that sends in the owner's name, used as [the mailboxes](references/mailboxes.md) reference says. `other`: ask which tool, and say what was used. `none`: the owner sends.
- `publishing.approval` and `owner.channel`: how and where the approval of the exact text is captured, as `approval-gated-publishing` says.
- `project.brief`: where the consent basis and the read-out rule are recorded.
- Set values with `hermes config set skills.config.<key> <value>`.

## Steps
1. Build the list from the source of truth, with the exclusions of the decision rules, and store it with owner-only permissions where it survives until the send.
2. Check each person's consent on that person's own record, and state the basis the message rests on.
3. Draft per language, in the owner's first person, easy to reply to, following [list and drafts](references/list-and-drafts.md).
4. Fix the read-out rule before sending: which replies, in what number, lead to which decision, and what too few mean. Record it in the project brief.
5. Ask for approval with `approval-gated-publishing`: every draft in full, the From address, the list size and the consent basis.
6. Check the sending identity: the approved From address must be one the mailbox may send as. If not, stop and ask the owner to add it.
7. Dry run: assert the count, no duplicate and no excluded domain, and render one sample per variant to compare with the approved text.
8. Send one message per recipient, a few seconds apart, idempotently: a send log skips anyone already sent, so a rerun never doubles.
9. Verify in the mailbox, not from the exit code: read back the From header and the sent state of every message, search for bounces and note each reason.
10. Record the send (counts, variants, bounces, read-out dates) on the work item, and schedule the read-outs with a read-only reply reader that strips addresses.

## Decision rules
- Nothing leaves before the owner's explicit approval of the exact text. A changed wording, sender address or list needs a new approval.
- One email per recipient: never several people in To, Cc or Bcc.
- Addresses and names never go into the conversation, notes or work items: counts and anonymised rows (R1, R2) only.
- Consent sets the type of email. Marketing consent is checked on the person's record: list and event payloads often omit it. Without it, the message is a personal service or feedback message about the person's own account, with no offer, link or tracking pixel.
- Before drafting, exclude internal accounts (the team's own domains, test markers), opt-outs and likely minors (school domains).
- Never send from another brand's address: it changes what was approved and reads as phishing.
- The replies are the owner's: the agent reads and codes them, never answers them. Tell bounce, auto-reply and person apart before counting a reply.
- Fewer replies than the read-out rule needs is "no signal", never "no problem".

## Done when
- Each approved recipient got exactly one message from the approved address, verified in the mailbox, and bounces are counted with their reasons.
- The read-out rule and dates are recorded, and no address or name left the mailbox.
- The report gives the count sent against the list size, the approved identity, the bounces with reasons, the read-out rule and dates, and where the send is recorded.
