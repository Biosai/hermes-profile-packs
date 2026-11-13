# Re-checking an ask before listing it again

A reminder, a block reason, a status or a "waiting on you" list repeats asks that may already be done. Asking again for something the owner already did is the most expensive mistake of this protocol. Before each item, today:

1. **Re-fetch its record.** A closed owner-action record is done: drop the item.
2. **Probe the capability instead of quoting a note.** Call the API with the key, load the page, search for the receipt. "Access X is still missing" in a note is a snapshot, not a fact.
3. **Compare with what happened in this conversation** since the note or the work item was written: sends, posts, payments, merges. Work items copy asks from notes that are older than the conversation.
4. **Fix the stale note** in the same pass.

## The first time, and after
- The first time an ask appears in a conversation, send the whole question: the problem in measured numbers, each option with its effect and its cost, the recommendation and its conditions.
- After that, a one-line reminder with the record's link is enough.
- A reminder never names options ("answer A, B or C") that the owner has not seen in full.
- Each item in a waiting list is its own recorded owner action, one action per record (the `owner-action-handoff` workflow).
