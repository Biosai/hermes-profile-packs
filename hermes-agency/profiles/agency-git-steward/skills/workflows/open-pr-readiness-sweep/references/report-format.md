# Sweep report format

Companion to `open-pr-readiness-sweep`, step 10. The same table whatever the code host.

```
Open requests: N — mergeable M — red R — conflicting C        (corrections to an earlier probe first)
RED: <url> — <job> / <step> — <error line>
CONFLICTING: <url> — needs a rebase | stale snapshot, recommend closing
MERGEABLE, CI TESTS: <url> — <jobs that ran> — +<added>/-<deleted>
MERGEABLE, CI PROVES NOTHING: <url> — draft | docs-only | no CI definition
ORDER: <url> before <url> — <why>
CANNOT SEE: <endpoint> — HTTP <status>
```

- Each request is a full link, listed in merge order, with what it changes, what CI cannot prove
  (a mocked provider, an untested path) and what follows the merge (a deploy, and who does it).
- When the owner narrows the scope to one repository, answer only for that one.
- A repository the owner excluded is named once as excluded and never itemized.
- A dependency-bot backlog on an inactive repository without CI collapses to one line: every
  request is mergeable, none is proven safe, and each merge spawns replacements. A red dependency
  bump may be unsatisfiable alone (peer dependencies split across sibling bumps): report one
  coupled change, not N retries.
- End with a short list of next actions and one question: the cheapest request to handle today.
- The recommendations are addressed to whoever `delivery.merge_policy` names. The sweep never
  merges.

## Reading what you list
- A deploy-preview status is a build, not tests, and a cancelled preview can still post success:
  read the description, never the state alone.
- A draft is the normal resting state of an agent-authored content request: it awaits a decision,
  not code.
- "All clear" from one endpoint's silence is not a result: query a sibling endpoint first.
