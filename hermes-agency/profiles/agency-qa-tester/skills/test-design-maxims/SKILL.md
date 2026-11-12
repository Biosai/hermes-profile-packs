---
name: test-design-maxims
description: "Check tests against maxims that catch false greens"
metadata:
  hermes:
    prerequisites:
      commands: [git]
---
# Test Design Maxims

A test that cannot fail is worse than no test: it buys confidence it has not earned. Each maxim names a defect class that shipped somewhere before.

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| Read access to the tests and the code under test | review against the maxims | open the files |
| Ability to run the tests locally, only for the revert check | prove a test fails without the change | the suite's own setup check |

If a required prerequisite is missing, stop before step 1. Say which one, what it blocks, and the smallest access that would unblock it (read-only first). Do the parts that do not need it only if they still make sense alone. Never replace data you could not read with an estimate, and never report "nothing found" when the lookup failed.

## Configuration
This skill reads no settings: the maxims hold for any language, framework, repository layout or tracker. Where a maxim needs a team-specific fact (a fixture helper, a cleanup hook), use the repository's own convention and name it in your review.

## How to apply
1. For each new or changed test, ask the question each maxim raises.
2. If a maxim applies and the test does not satisfy it, fix the test before relying on its result.
3. In a review, name the maxim, the test, and the concrete way it can pass falsely.

## Fixtures and state
1. **A fixture comes from the product path.** Create test data through the product's own API or service layer, not raw inserts. Hand-made rows encode states the product never produces and miss fields it always writes.
2. **A fixture must seed a reachable state.** If no sequence of real operations could produce it, the test proves behavior on an impossible world.
3. **A restore must undo every side effect.** A test or rollback that changes environment variables, configuration, clocks, flags, files or rows restores all of them, not only the one it remembers; otherwise the next test inherits it.
4. **A shared-table pass is another writer.** When tests share a table, a test that scans or counts the whole table sees others' rows. Scope assertions to the rows this test created.

## Concurrency and parallel runs
5. **A race test must manufacture its race.** Force the interleaving with barriers or many actors released at once, and assert the contention happened. A test that passes because the race never occurred proves nothing.
6. **A parallel test's cleanups outlive it.** Cleanup runs on the framework's schedule, not when the function returns. Register teardown with the cleanup hook; never tear down what a sibling still uses.
7. **A test server's close can be process-wide.** Shutting down a test dependency may reset shared state such as default HTTP clients and their connection pools, breaking parallel tests that never touched it. Give each test its own client.

## Faults and fixes
8. **A fault test must fault inside the unit.** Inject the failure where the unit calls its dependency, and assert the fault was hit. A test whose setup fails before reaching the unit exercises the harness.
9. **Deflaking must not assert less.** Removing an assertion, widening a tolerance or retrying until green turns a flaky test into a dead one. Find the cause, or quarantine it visibly, with a recorded work item or, when the team has no tracker, a line in your report.

## What the code under test must be tested for
10. **An invariant needs every door.** A rule enforced in the API but not in the batch job, admin path, webhook handler or migration is a suggestion. Test each door.
11. **Fields valid alone can be nonsense together.** Test combinations: a start after its end, a unit that does not match its amount, a status contradicting a timestamp.
12. **Served values must round-trip.** Whatever the API returns must be accepted back by the API that consumes it (format, precision, casing, time zone). Send a served value back.
13. **A vocabulary has many enumerations.** A status set lives in the schema, constraints, code, API spec, client and docs. A new value is tested against every list.
14. **Refusals must not misattribute.** An error must name its real cause; blaming the caller's input when a dependency failed misleads users and debuggers.
15. **A 4xx is not a refusal.** A dependency's 4xx can mean malformed request, expired credentials, rate limit or missing resource. Only a documented business refusal is a refusal.
16. **Relations must not fail silently.** A required lookup that returns empty when the related record is missing makes a broken reference look like "no data".
17. **Recovery must not hide the problem.** A retry, fallback or default that swallows a failure must leave a trace (log, metric, alert). Assert the trace.
18. **A shared flight has no caller.** When concurrent requests are coalesced, one caller cancelling must not fail the others, and one caller's identity must not leak into the shared result.
19. **Per-call error collection needs a private collector.** A shared collector mixes other calls' errors into yours.
20. **A loop must not be bounded only by its own predicate.** A poll or retry that exits only when its condition becomes true never exits when it does not. Test the independent bound.
21. **A fixed budget is a data-size ceiling.** A fixed timeout, page size or memory budget caps the volume the code can handle. Test near the ceiling.
22. **Vendor assertions are dated facts.** "The vendor does X" holds as of a date and a source; tests that encode it say both.

## Output standard
In a review: `Maxim 5 — <test name> — passes without contention: actors start sequentially`. In your own work: the maxims checked for each new test file.

## Traps
- A test that passes with the change reverted is not testing the change.
- This list is not exhaustive. Add a maxim when a new false green teaches one.
