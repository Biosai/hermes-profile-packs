# Cases that need their own handling

## The prerequisite nobody asked for
Look for what must be settled before the requested work and cannot be retrofitted afterwards. How money is represented and rounded is the recurring one: every stored amount inherits the choice. File it as its own item, and say in the reply that it was not in the request and why it blocks.

## A request that contradicts the repository's own stated constraints
For example an agent or contribution file that forbids a class of work before some gate.
- Record the contradiction in the item.
- The owner's explicit decision outranks your inference, not the reverse: record it as a dated, deliberate bet.
- Require, in the item's acceptance criteria, that the constraint file be amended in the change that implements the work.
- Never violate the constraint silently, and never refuse the owner silently.

## A test that asserts the current wrong behaviour
Such a test exists when a fix was outside the remit of whoever wrote it. Name it in the acceptance criteria of the fixing item, to be inverted. Otherwise the defect is protected by the checks that run on every change.

## A build redirected into filing
When the owner turns a build into "just create the issues":
- treat it as a sign that the order was wrong;
- check whether the repository had already scheduled the work that was started, and say so in the reply;
- code already written is committed as work in progress by its author and parked as a draft pull or merge request, never discarded or left only on disk. The full-stack engineer profile's `bounded-task-delivery` workflow, when installed, says how unfinished work is parked.

## The two readings of the ask
| The owner says | The tracker holds | Do |
|---|---|---|
| "give me the high level" | the work, as many items | epics over the existing items, each open item under exactly one; an orphan is a finding |
| "items for what is left" | only defect-level items, no forward work | the gaps: the plan's definition of done minus what is tracked |
| unclear | anything | ask |

## Report
```
Plan of record: <link> (amendments read: <n>)   Tracked before: <n> items
Filed: <n>, unblockers first: <links>
Not needed: <gap>: <amendment>
```
