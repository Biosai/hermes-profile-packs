# The mailboxes

`publishing.mailbox` names the owner's mailbox. The send goes out in the owner's name, from an address the owner approved.

| Value | Sending and reading | Sending identities | Finding bounces |
|---|---|---|---|
| `gmail` | the mailbox's connector or API | the "send mail as" addresses of the account | for example a search for `from:(mailer-daemon OR postmaster)` after the send time |
| `microsoft365` | the mailbox's connector or API | the mailbox's own addresses and those it may send as | for example a search for non-delivery reports ("Undeliverable") after the send time |
| `other` | ask the owner which tool, and whether it has an API | ask how the tool lists allowed From addresses | the tool's own bounce or delivery report |
| `none` | the agent prepares each message and the owner sends it | the owner checks | the owner reports them |

Say in the report which tool was used and what was done by hand.

## Checks that hold for every mailbox
- **Sending identity.** The approved From address must be one the mailbox is allowed to send as. If it is not, stop and ask the owner to add it. Never fall back to another address.
- **After the send.** Read back, for every message, the From header and the sent state. An exit code or an API success is not proof.
- **Bounces.** Note the reason for each. Tell a bounce, an automatic reply and a person's reply apart before counting replies.
- **Replies.** Read them with read-only access, through a reader that strips addresses and names. The agent never answers.

## With `none`
Do steps 1 to 5 of the workflow, then hand the owner one message per recipient, ready to paste, apart from any commentary, with the From address to use. Ask the owner for the count sent and the bounces. Never report a send you did not see.
