# Did the fix work?

"Still zero after the fix?" has three separate answers: is it live, can the metric answer yet, and what does it say.

## a. Confirm it is live
- Re-run the probe on production with the user agent of the paid traffic.
- Fingerprint the live build from a change the fix introduced.
- Merged is not deployed. A work item closed by the merge is reopened with the probe output and a done-when that names the deploy.

## b. Size the test before reading the delta
```
python3 scripts/effect_size.py --before <successes> <total> --after <successes> <total> \
    --baseline <rate> --target <rate> --per-day <sessions per day>
```
It prints the sessions needed per arm and the days that takes. Push back on any verdict scheduled before that sample exists: it returns "flat" by construction. Report "shipped and verified" apart from "moved the funnel".

## c. Compare equal windows
Equal windows either side of the release, leaving out the release day and the days of your own testing. Test the difference:
```
python3 scripts/fisher_exact.py <successes_a> <total_a> <successes_b> <total_b>
```

| Result | Verdict |
|---|---|
| p < 0.05 | the change is real: report the two rates and the windows |
| p >= 0.05, sample >= required | "no detectable effect: this was not the constraint" |
| p >= 0.05, sample < required | "cannot conclude, need X more days" (give X) |

Retiring a hypothesis after repeated underpowered nulls is a prioritisation decision, not a finding: label it so.

## A verdict that runs on a schedule
When a scheduled verdict moves, write the power number and the table above into the job's own prompt. Then read the stored prompt back from the scheduler: an API success or a truncated preview does not prove that the guardrails were saved.

## The answer, in order
1. what is verified as shipped;
2. why the metric cannot answer yet: p, and sessions per arm against the sessions required;
3. when the zero started;
4. the constraint binding now;
5. what is dropped.
