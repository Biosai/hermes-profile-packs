# Migration verification: effects on existing data

Companion to `migration-verification`, step 8. `schema-migration` owns the design of the change
(staging, locks, timing at production scale, compatibility). These checks are about what running
it does to rows that already exist.

1. **Classify** the affected tables and columns by data class and by the retention rule that
   applies to each.
2. **Constraint and type changes**: get the count of rows that would violate the new constraint
   or be truncated by the new type, per environment. Zero is a result to state, not to assume.
3. **Backfills and corrections** change existing rows. The request must declare them: what
   changes, how many rows per environment, how it is applied. Counts scope a data change; only the
   owner authorizes applying it. An undeclared data change is blocking.
4. **Drops and truncations** of data under a minimum retention rule wait until the data is
   archived under the same controls.
5. **New copies** of regulated data need a retention answer and a place in the deletion
   mechanism.
6. **Audit tables**: never update or delete audit rows, and never backfill history with invented
   values.
7. **Sensitive columns**: encryption and access restrictions survive the change.
8. **Irreversibility** is stated in the request when the way back would lose data.

The retention rules and the audit trail themselves are reviewed by the compliance reviewer
profile when it is installed (`regulated-engineering-controls`); this list only checks that one
migration does not break them.

## Report format
```
Migration — <request link> — <file> — number <n>
Tip on origin/<default> @ <commit>: <m> — above tip: yes/no — collisions: none | <links>
Deployed: <environment>: <version> | not readable
Up at production version: OK in <t>s | FAIL <error> — down/up: OK | irreversible, stated
Raw SQL on changed columns: none | <path:line>
Retention conflicts / new copies / audit rows rewritten: <...>
Data change declared: yes | NO (blocking)
Verdict: OK | FINDINGS (<n>) | BLOCKING (<n>)
```
