# The scope entry

The entry is short on purpose: every profile working on the project reads it first. The detail (customer, voice, constraints, autonomy per function) stays in the other parts of the project brief.

```
Project: <name>
What it is: <one sentence, and who pays for it>
Owns: <repositories, work tracker, domains, channels>
Binding constraint: <one sentence, in the owner's words; primary source when it comes from a rule>
Decisions (dated): <YYYY-MM-DD: decision>; <YYYY-MM-DD: decision>
Approved by the owner on <YYYY-MM-DD>
```

## Filling it
- Each line keeps the owner's own words. Where you reworded, say so.
- A line the owner has not answered yet reads "not answered yet (asked <date>)", never a guess.
- A decision that replaced an earlier one is listed with "supersedes <date>"; the earlier one stays in the brief's history.

## Autonomy
Record beside the entry, per function (for example delivery, publishing, spending), what a profile may do alone and what it only prepares for the owner. A function the owner has not spoken about is asked about, never assumed.

## Settings the answers imply
Offer these to the owner as lines to run, one per value that the answers settled:

```
hermes config set skills.config.delivery.code_host <value>
hermes config set skills.config.delivery.repos <paths or URLs>
hermes config set skills.config.delivery.issue_tracker <value>
hermes config set skills.config.delivery.merge_policy <value>
```

For one profile only: `hermes -p <profile> config set skills.config.<key> <value>`.
