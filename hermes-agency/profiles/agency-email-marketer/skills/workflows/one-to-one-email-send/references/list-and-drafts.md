# List and drafts

## The list
- Build it from the source of truth (user store, CRM or email platform), never from a remembered or pasted list.
- Exclude before drafting: internal accounts (the team's own domains, test markers), people who opted out or unsubscribed, likely minors (school domains).
- Store it with owner-only permissions, in a place that survives until the send: scratch folders may be pruned in between.
- Outside that file, only counts and anonymised rows (R1, R2).

## Consent
- Check marketing consent per person, on the person's own record. List exports and event payloads often omit the field.
- Consent sets the type of email. When few or none of the recipients consented to marketing, the message is a personal service or feedback message about the person's own account: no offer, no link, no tracking pixel.
- State the basis in the approval request, for the owner to approve, and record it in the project brief.

## The drafts
- One draft per language. Take each person's language from the profile, and from the signup data when the profile field is empty.
- Written in the owner's first person, short.
- Neutral toward the reader's gender where the language marks gender.
- A plain greeting when most first names are empty.
- Make replying easy: a few numbered options built from what is already measured about the question, plus an open "something else".
- Every draft goes in full into the approval request.

## The read-out rule
Fix it before sending, so that the replies cannot be read to fit a wish. It names:
- which replies count (a person's reply, not a bounce or an automatic reply);
- the number that leads to a decision, and which decision ("three or more naming the same detail: that detail is the next product decision");
- what too few replies mean ("fewer than three replies: no signal, not no problem");
- the dates of the read-outs, for example an interim one after a week and the verdict after two.

## The dry run
Assert the count against the approved list size, no duplicate, no excluded domain. Render one sample per variant and compare it, character for character, with the approved text.

## The send log
One line per recipient sent (anonymised row, variant, time, message id). The sender skips anyone already in the log, so a rerun after a failure never sends twice.
