# Hand-apply runbook for an urgent infrastructure fix

Companion to `iac-change-safety`. An urgent fix is still a pull or merge request; the runbook goes
in its description so that a person, never the profile, can apply by hand before the merge.
Write every section, in this order.

1. **Incident**: what is broken, since when, and the evidence.
2. **Preconditions**: the identity to use, the tools and their versions, the environment, and a
   read-only command that confirms the broken state.
3. **Steps**: numbered. Each gives the exact command, with every value filled in except secrets,
   the expected output, and the condition on which to stop.
4. **Verification**: how to see that the fix worked, from outside the tool.
5. **Rollback**: the exact way back.
6. **Reconciliation**: merge the request, then run a plan that shows no changes.

Date every number in UTC and take it from a command you ran.
