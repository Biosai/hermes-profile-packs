# When the gate or a send misbehaves

Each case ends the same way: stop, say what happened, and leave the next move to the owner.

## The approval gate does not ask on a call
- An approval given in conversation does not cover a call the approval gate fails to ask on. Fix the gate first, and offer the owner the platform's own interface meanwhile.
- Before the first use of any send-type call (send, schedule, switch live, list, spend), prove that the live gate asks on it. A merged fix is not a deployed one: test the gate that is running.
- Never test the gate by going around it: no mode that skips approvals (`hermes -z` one-shot runs, `--yolo`). If the gate looks broken, report it and stop.

## A send or schedule call failed unexpectedly
- Do not retry it, and do not try another endpoint or API version: the first call may have gone through, and each retry may reach real people.
- Read the state from the platform, read-only: what exists, what was sent, what is scheduled.
- Hand the step to the owner with that state and the exact action left to do.

## The owner scheduled the item in the platform's own interface
- Read each item back from the platform and compare its send time, with its time zone, with the intended one before saying "scheduled".
- If they differ, give the actual date and its consequence first, then the fix, and accept the owner's call.

## Reporting states
- "Queued" or "handed off" is not "published". "Published" needs the live link, opened and checked.
- Silence, a reaction or a relayed "looks good" is not an approval: the item stays "awaiting approval".
