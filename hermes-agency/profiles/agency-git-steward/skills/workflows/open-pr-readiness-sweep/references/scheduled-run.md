# Running the sweep on a schedule

Companion to `open-pr-readiness-sweep`. GitHub only, like the auditor it wraps.

## The wrapper
Schedule `scripts/scheduled_sweep.py`, not the auditor. Set `PR_SWEEP_ORG` (the owners to sweep,
comma-separated) and optionally `PR_SWEEP_WORKDIR` (where `prs_open.json` is written). Pass
`--token-env NAME` when the token is not in `GITHUB_TOKEN` or `GH_TOKEN`. The wrapper adds:
- output sorted by repository and number, with no timestamps, so identical state gives identical
  output;
- a `--- STRUCTURED ---` tail of one JSON object per request;
- a control gate: it exits non-zero, with the auditor's raw output, when the controls did not
  run or the auditor failed. A previous run's file never stands in for this run's result.

## Before scheduling it
Run it by hand and check: exit status 0; both controls printed; a request number you know is
present in the JSON tail (the key is `num`); and a count equal to the code host's own listing.

## The scheduled prompt
- Restate steps 4 to 8 of the workflow in the prompt: a scheduled run has no conversation to
  correct it.
- Ask for full links.
- With zero open requests, stay silent rather than posting "nothing to report".
- A token rotated while a long-running process is alive: the process keeps the old value in its
  environment. The auditor reads the profile's environment file before the process environment
  for that reason; after a rotation, check which source it printed.

## After your own pushes
Sweep after your own pushes too. When the red request is yours, fix it and report the observed
transition: a new run on the new head, going from failure to success.
