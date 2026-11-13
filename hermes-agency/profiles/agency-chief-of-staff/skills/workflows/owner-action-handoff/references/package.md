# The package

Everything the owner needs to finish in one sitting. Prepare it before asking.

```
Why: <what this unblocks>
Do: <numbered steps, every value filled in>
Cost / irreversible: <...>
Check: <what you should see when it worked>
After: <what the agent verifies and continues>
```

- **Do** holds the exact command, link or console path, with every value filled in, and the final draft or form contents. Text the owner must copy is ready to paste, apart from any commentary.
- **Cost / irreversible** names the money, and what cannot be undone.
- **Check** is something the owner can see, and the agent can verify afterwards without the owner.
- No secret in the package or the record: point to where the owner keeps it.

## The record
- Labelled owner-action, titled with the action as a verb ("Merge the checkout fix").
- One action per record, with its steps and a done-when the agent can check.
- An ask split out of a larger item gets its own record, linked from the parent.
- Where `owner.action_tracker` says:

| Value | The record |
|---|---|
| `issue-tracker` | an item in `delivery.issue_tracker` (github: `gh issue create`; gitlab: `glab issue create`; any other tracker: its own CLI, API or web UI) |
| `file` | a section appended to `delivery.issue_file` |
| `conversation` | the package itself, where `owner.channel` says, repeated in each status until it is done |

## The ask
One line where `owner.channel` says: the action, and the link to the record. When the agent writes to the tracker under the owner's own account, the tracker does not notify the owner: this line is the notification.

## When the owner says it is done
Verify it yourself: re-fetch, re-run, read the live state. Close the record with that evidence, then unblock the work.
