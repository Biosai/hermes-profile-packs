# The test design maxims

Companion to `test-design-maxims`, step 2. Each maxim names one way a test passes while the
behavior is wrong. Cite a maxim by its number.

## Fixtures and state
1. **A fixture comes from the product path.** Create test data through the product's own API or
   service layer, not raw inserts. Hand-made rows encode states the product never produces and
   miss fields it always writes.
2. **A fixture must seed a reachable state.** If no sequence of real operations could produce it,
   the test proves behavior on an impossible world.
3. **A restore must undo every side effect.** A test or rollback that changes environment
   variables, configuration, clocks, flags, files or rows restores all of them, not only the one
   it remembers; otherwise the next test inherits it.
4. **A shared-table pass is another writer.** When tests share a table, a test that scans or
   counts the whole table sees others' rows. Scope assertions to the rows this test created.

## Concurrency and parallel runs
5. **A race test must manufacture its race.** Force the interleaving with barriers or many actors
   released at once, and assert the contention happened. A test that passes because the race
   never occurred proves nothing.
6. **A parallel test's cleanups outlive it.** Cleanup runs on the framework's schedule, not when
   the function returns. Register teardown with the cleanup hook; never tear down what a sibling
   still uses.
7. **A test server's close can be process-wide.** Shutting down a test dependency may reset shared
   state such as default HTTP clients and their connection pools, breaking parallel tests that
   never touched it. Give each test its own client.

## Faults and fixes
8. **A fault test must fault inside the unit.** Inject the failure where the unit calls its
   dependency, and assert the fault was hit. A test whose setup fails before reaching the unit
   exercises the harness.
9. **Deflaking must not assert less.** Removing an assertion, widening a tolerance or retrying
   until green turns a flaky test into a dead one. Find the cause, or quarantine it visibly, with
   a recorded work item or, when the team has no tracker, a line in your report.

## What the code under test must be tested for
10. **An invariant needs every door.** A rule enforced in the API but not in the batch job, admin
    path, webhook handler or migration is a suggestion. Test each door.
11. **Fields valid alone can be nonsense together.** Test combinations: a start after its end, a
    unit that does not match its amount, a status contradicting a timestamp.
12. **Served values must round-trip.** Whatever the API returns must be accepted back by the API
    that consumes it (format, precision, casing, time zone). Send a served value back.
13. **A vocabulary has many enumerations.** A status set lives in the schema, constraints, code,
    API specification, client and docs. A new value is tested against every list.
14. **Refusals must not misattribute.** An error must name its real cause; blaming the caller's
    input when a dependency failed misleads users and debuggers.
15. **A 4xx is not a refusal.** A dependency's 4xx can mean a malformed request, expired
    credentials, a rate limit or a missing resource. Only a documented business refusal is a
    refusal.
16. **Relations must not fail silently.** A required lookup that returns empty when the related
    record is missing makes a broken reference look like "no data".
17. **Recovery must not hide the problem.** A retry, fallback or default that swallows a failure
    must leave a trace (log, metric, alert). Assert the trace.
18. **A shared flight has no caller.** When concurrent requests are coalesced, one caller
    cancelling must not fail the others, and one caller's identity must not leak into the shared
    result.
19. **Per-call error collection needs a private collector.** A shared collector mixes other calls'
    errors into yours.
20. **A loop must not be bounded only by its own predicate.** A poll or retry that exits only when
    its condition becomes true never exits when it does not. Test the independent bound.
21. **A fixed budget is a data-size ceiling.** A fixed timeout, page size or memory budget caps
    the volume the code can handle. Test near the ceiling.
22. **Vendor assertions are dated facts.** "The vendor does X" holds as of a date and a source;
    tests that encode it say both.

## What a check must assert
Whether a check bites is proven, not read: the `mutation-proof` workflow owns that proof and the
rules that go with it (assert the value the change moves; fail by name, never by crashing; an
empty collection is a finding; a pass rate needs its denominator; testing the judge does not test
the collector).
