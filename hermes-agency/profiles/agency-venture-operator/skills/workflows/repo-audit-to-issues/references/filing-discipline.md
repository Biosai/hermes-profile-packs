# Filing discipline: every finding tracked once

Companion to `repo-audit-to-issues`, steps 6 to 8. A finding reported only in chat is lost: chat
is not a tracker.

## When a finding becomes an item
Every time a finding is real (verified by execution or a primary source, not a suspicion), is not
being fixed in this turn, and belongs to a repository. Non-code findings count: contradictions
between documents, voice or brand drift, wrong asset dimensions, dead links, stale claims, missing
access. Something fixed in the same turn is a change request, not an item.

## Deduplicate on bodies, never on titles
The same problem is described in different words each time, so titles are the worst key. Pull
every item, open and closed, with its body, and search the text:

```bash
gh issue list --state all --limit 1000 --json number,state,title,body > items.json   # github
glab issue list --all --output json > items.json                                    # gitlab
```

Keywords must be specific artifacts: a filename, a config key, an invite code, an error string, a
function name. Generic words (`bug`, `test`, `CI`, `docs`) match everything and prove nothing. A
keyword hit is a lead: read the lines around it before deciding.

| Result | Action |
|---|---|
| Same root cause | Comment on the existing item with the new evidence. Never a second item. |
| Adjacent, different root cause | New item, and the body says why it is not the other one |
| Closed, problem returned | Reopen with the new evidence rather than filing again |
| Nothing | New item |

The adjacent case is the common one: three CI items can coexist (a job calling binaries absent
from its runner, a coverage gate measuring the wrong thing, a package CI never builds) because
fixing two does not fix the third. Each body says so.

An existing item saying "this should also be checked" is not coverage: actually checking it and
finding a problem is a new finding with its own evidence.

Prove the search can see, in the same run: a phrase known to exist is found and a nonsense string
is not. An empty corpus is indistinguishable from a wrong repository name, a bad filter or a token
without issue scope: on an empty tracker, run the same query against a sibling repository known
to hold items, print both counts, and name the control in the report.

## Filing a whole backlog in one pass
- Create the labels first. An item created with a label that does not exist is created without
  it, and nothing in the response says so. Label creation is safe to rerun: treat "already
  exists" as success.
- Label by who unblocks the item (the owner, a client, a professional's written answer,
  infrastructure, data coverage), not by component: sorted that way the list is a sequence.
- Do not merge two blockers because they share a subject. The test is closability: if fixing one
  thing closes it, it is one item.
- Point at the document instead of copying it: lead with the measurement or the quoted primary
  source, then reference the file that holds the depth. A copied analysis diverges, and the
  tracker copy is the one nobody updates.
- Re-read the items from the tracker. A created response proves the request was accepted, not
  that title, body and labels landed: an empty label list means a misspelt label, a truncated body
  usually means the payload was concatenated instead of encoded.

## Decisions versus execution
When a "which option?" item is answered, do not rewrite it into a build ticket. Comment the
decision on it, open one execution item per thing to build, and keep the original open as the
sequencing gate when later work waits on it. Re-read its scope first: a decision item does not
cover the build. Rank execution items by effort to payoff and say why. Surface the prerequisite
nobody named (who owns, moderates or maintains the thing) before the build steps.

## Keep filed items true
- When an owner decision resolves or reframes an item you filed, comment on it, including which
  part of your own analysis was wrong. Record what the decision does not license as well: a stance
  narrows the rules, it rarely deletes them.
- A document that reality seems to contradict may be scoped to a later stage of the venture (a
  launch-day tone, a post-launch metric). Ask which stage it assumes before filing "the doc is
  wrong"; the fix is often stating when each rule applies.
- When the environment changes during the session (a tool installed, access granted), correct the
  items that asserted the old state. The state you changed is not durable; the text describing it is.

## Reporting
Item links go on their own line as plain text, never inside a code block: chat clients render a
code block as preformatted text, copyable but not tappable. Code blocks are for things to paste.

## Checklist
- [ ] Every unresolved finding has an item, non-code ones included
- [ ] Deduplicated on bodies, open and closed, change requests filtered out, with specific keywords
- [ ] The search was shown able to find something; an empty tracker had a named sibling control
- [ ] Labels existed before the first item; every item re-read with labels and a full body
- [ ] Adjacent items say why they are not the existing one; each is closable by one fix
- [ ] Items reframed by an owner decision or a changed environment carry a correcting comment
