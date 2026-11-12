# Evidence techniques for an audit

Companion to `repo-audit-to-issues`. Each technique turns "I think this is wrong" into output a
reader can rerun. Most findings live where there is no pipeline to re-run and no log to quote:
in source code, in documentation, and in what is actually deployed.

## 1. CI history, not the latest run
- Page every run and count conclusions (`failure: 21, success: 0` is a finding about the
  pipeline's whole life, not about one commit).
- Break the latest run into jobs and steps: "CI is red" on a change to the landing page may be a
  contract coverage gate failing in another job.
- Expired logs (`HTTP 410` on GitHub) are not the finding. Clone, install with the versions the
  workflow pins, and run the failing script yourself: a local transcript is quotable.
- A check duplicated across two jobs: the copy on a runner that lacks the tool is the one that
  fails, while the other copy, installed by its own action, passes.
- Coverage instrumentation is not additive: excluding a folder from coverage changed how the run
  was instrumented and dropped an untouched file from 100% to 0%. Re-measure after any coverage
  configuration change; the obvious one-line fix is exactly the one to run before proposing.
- A throwaway probe copies a sibling test's fixture setup (grep the suite for the factory call)
  instead of guessing a mock's name or arity, and is deleted afterwards, the tree proved clean.

## 2. Extract a pure function and freeze the clock
Never retype the function under test: you would prove something about your paraphrase. Read the
real file, cut the function out verbatim with a regex, print it, then evaluate it under a
controlled clock. A type annotation is often all that stops a plain runtime from evaluating it.

```javascript
const src = require('fs').readFileSync('<repo>/<path>/<file>.ts', 'utf8');
const m = src.match(/export function today\(\): string \{[\s\S]*?\n\}/);
if (!m) { console.error('FAIL: function not found'); process.exit(1); }
console.log(m[0]);                                   // show what is evaluated
const fnText = m[0].replace('export function', 'function').replace('(): string', '()');
const FROZEN = Date.parse('<an instant that straddles the suspected boundary>');
const RealDate = Date;                               // keep it, or the oracle freezes too
global.Date = class extends RealDate { constructor(...a) { a.length ? super(...a) : super(FROZEN); } static now() { return FROZEN; } };
const today = eval(`(${fnText})`);
const oracle = new Intl.DateTimeFormat('en-CA', { timeZone: '<business zone>', dateStyle: 'short' }).format(new RealDate(FROZEN));
console.log(`oracle=${oracle} today()=${today()} ${today() === oracle ? 'MATCH' : 'MISMATCH <-- BUG'}`);
```

The oracle must use a different mechanism from the code under test. Run it twice: with the
process time zone as production runs it (the bug) and with the fix applied (the control).

## 3. Quantify the exposure window, then map it onto the callers
"Sometimes wrong" is unactionable. Sweep the whole cycle (24 hours, every month end, every
boundary) and count the mismatches: "5 hours out of 24". Then place each caller in or out of the
window: a nightly job outside it is safe; a webhook that fires at any hour is inside it every
day. That mapping is the finding; without it the item over-claims or under-claims.

## 4. A scan that found nothing proves nothing until it finds something
Pair every absence claim ("variable X is set nowhere") with the same scan, same corpus, for
something you know exists, and print both counts. Same for a duplicate search that returns zero
items. Trace each configuration variable to its single read site before crediting it with an
effect: a plausibly named variable may configure a vendor call, not the process.
A repository missing from a listing after a token change is a scope question before it is a
deletion claim: a narrower token sees fewer repositories. Confirm against a durable record (an
archive release, an item recording the retirement) before reporting it gone.
A watchdog that has been silent proves nothing until it has been seen firing: run a copy with a
lowered threshold and check the alert names the real target, feed it a deliberately invalid input
to exercise the failure branch, and restore the real settings afterwards.

## 5. Did a green test job run anything?
Count the test files the job could collect. A configured test target with no test files passes
in every common framework, so green means "it lints and compiles". Report the count; ask whether
CI should fail when a project has a test target and no tests.

## 6. Doc-versus-code contradictions: four classes to look for by name
| Class | Why it bites |
|---|---|
| A resolved-questions list still carrying the answer that was later reversed | quoted in good faith by whoever reads only their section |
| A stale "nothing calls this yet" in a doc or comment, while a caller exists | deliberate-sounding comments are the most credible stale ones |
| A type or enum narrower than the doc's list of supported values | the doc calls it decided, so nobody scopes the missing work |
| An infrastructure placeholder whose own comment admits it cannot work | self-documented latent breakage that ships |

State the rule when reporting: the code describes what runs, the doc may be the intent. Present
which side should change as a decision, never as silent cleanup. Name the deliberate, honest
boundaries too ("excluded until feature X exists"): an audit that only lists faults is discounted.

## 7. Two repositories of one product may share nothing
Test integration in both directions: scan each repository for the other's identifiers, hosts and
vendor names. Then tabulate the axes that would have to agree (custody or data ownership,
backend presence, package manager, authentication, supported networks or regions). Every axis
differing makes "wire them together" a product decision, not a task, and each repository looks
complete on its own terms. Hand-written shims that replace a vendor's native runtime mean the
shipped path is not the path the vendor tests: a runtime decision, not packaging.

## 8. Order findings by whose calendar controls them
When the audit feeds a plan, rank by who has to move: third-party lead times first (they cannot
be recovered by working harder; back-count from the fixed external date and print calendar and
working days), then whatever blocks verification (a missing secret that means a circuit never
ran end to end), then questions for a counterparty, then engineering, the only category whose
date you control.

## 9. What production ships: grep the deployed bundle
Build configuration states intent; the served files state fact. Fetch the page, extract its asset
URLs, fetch each, and grep the bytes for the value in question. Print the number of assets found:
an extractor that matched zero assets reads exactly like "the string is absent". Grep the same
bundles for a string you know the feature contains, as the control. Stripping tags from a
server-rendered page to read its text does not work; drive a browser or reason about the bundle.

## 10. Absences on a contract or API surface
For "no function can do X": enumerate the real surface (every function and the guards inside it),
attempt each plausible escape hatch as the deploy script deploys and print the exact revert or
error, and enumerate the deployed interface by name pattern (`transfer|withdraw|rescue|sweep`),
which catches a differently named function a source grep misses. Assert the arithmetic so the
probe fails if the finding goes stale, then delete the probe and prove the tree clean.
A parameter fixed by a one-shot initializer (the first configuration call after deploy, guarded
by an "already initialized" check) turns any document line it encodes, such as a price ladder or
an allocation table, into a deadline: it must be settled before the first production deploy, or
the fix is a redeploy plus a migration. Say so in the item: it is what makes it urgent.
For "feature X is not actually gated": grep the whole tree for the mechanism the gate could not
exist without (a chain or API client, a verifier, a key). None anywhere rules out a gate in code
you did not read. When the product's own disclosures claim the missing property, count and cite
them: a false statement about a live feature is a legal exposure, not a documentation defect.

## 11. Bootstrap impossibility
Before filing "the screen for X is missing", trace X's preconditions through the guards: if its
first use requires state that only exists after it has been used, the item is the bootstrap path
(a static page, an off-chain form, seeded state). Enumerate the callers of each internal that has
a legal or accounting side effect: when the only caller is unreachable, state that consequence; it
is usually more material than the missing screen.

## 12. Brand and artifact properties
A doc that tabulates artifact properties (image dimensions, filenames, endpoints, variables) is a
claim to check against the artifacts. Image dimensions can be read from a PNG header without a
library (`struct.unpack(">II", open(p, "rb").read(33)[16:24])`); look at the image before saying
what is wrong with it. When two docs disagree, name the one that wins and mark the other stale.
