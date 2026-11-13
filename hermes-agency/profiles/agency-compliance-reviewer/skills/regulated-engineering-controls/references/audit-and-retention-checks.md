# Audit trail, retention and deletion: engineering checks

Companion to `regulated-engineering-controls`, step 6. `policy-control-mapping` owns the mapping
from requirement to control, `audit-evidence` the provenance of what you collect, and
`data-handling-review` the trace of where each data class lives. These checks are about the
mechanisms in the code.

## Audit trail
- Every write path to controlled records writes an entry, atomically with the write or with a
  guarantee that it cannot be lost.
- An entry records who (the human or system actor; both identities when one acts as another),
  what (the action, the record id, before and after for the fields that matter), when (a trusted
  clock, UTC), where (the entry point, a correlation id), and why when the obligation requires it.
- The store is append-only for the application. Migrations never rewrite audit rows.
- A failed audit write fails the business write, or raises an alert. A fallback that silently
  skips the entry makes the trail lie.
- Logs that rotate sooner than the retention obligation are not an audit trail.

## Retention and deletion
- Each data class has a rule from the owner: minimum keep, maximum keep, legal hold. A class with
  no rule is the first finding.
- Every copy is answered: primary tables, replicas, indexes, caches, exports, logs, analytics
  copies, vendor systems, backups. Each is deleted, anonymized, expiring by a stated time-to-live,
  or retained for a stated reason. "Unknown" is a finding.
- Deletion keeps integrity: it anonymizes references rather than orphaning them, skips and logs
  records under a hold, and can resume after an interruption.
- Nothing under a minimum rule is deleted early by a job, a cascade or a migration.

## Report format
```
Control map — origin/<default> @ <commit> — <UTC date>
O-3 <obligation> [interpretation: needs confirmation]
  Control: <mechanism> — Code: <path:line @ commit> (doors: API yes, batch yes, admin no)
  Tests: <names> — run <link>: PASS a / SKIP b / FAIL c
  Status: GAP (admin door) — draft: <item link | file entry | in report>
Summary: EVIDENCED n / CLAIMED n / GAP n — Not reviewed: <list>
```
A control is named as a mechanism, for example: "every change to a customer record writes an
append-only audit entry with the actor and the before and after values".
