# The duplicate search

A second item for a known cause splits the evidence and the discussion. Search before writing.

## How to search
- Search item **bodies**, never titles alone, across open and closed items.
- Use keywords that name a specific artifact: a file, a configuration key, an endpoint, an error string, a function. Generic words match everything.
- Read the lines around each hit before deciding.
- Prove that the search can find: a phrase you know exists is found, and a nonsense string is not. A search that returned nothing proves nothing until it is shown finding something.
- A search that failed (no access, an API error) is "not searched", never "no duplicates".

## What to do with a hit
| Hit | Action |
|---|---|
| Same root cause | add your data to that item; never a second item |
| Adjacent cause | a new item that says why it is not the other one, linked to it |
| Closed, and the problem is back | reopen it with the new evidence |

## Per tracker (`delivery.issue_tracker`)
- `github`: for example `gh issue list --state all --search "<term> in:body"`. The issues REST API returns pull requests too: filter them out.
- `gitlab`: for example `glab issue list --all --search "<term>"`.
- `jira`, `linear`, any other tracker: its own text search or API over descriptions, and say which search was used.
- `file`: search `delivery.issue_file`, closed sections included.
- `none`: there is nothing to search; say so.

## In the report
List the searches run (terms and scope), the control that proved the search works, and the hits read.
