# Reviewing a knowledge change

For a pull or merge request against the knowledge base, the glossary or shared skills that someone else opened after a code merge.

## Checklist
1. Read the linked code change's state now. A knowledge change that describes unmerged code waits.
2. Run the validator on the head of the knowledge change. Rerun it after every push: a result from an earlier head proves nothing.
3. Search the code repository's default branch, freshly fetched, for every value, field, status code, default and flow the change states. Any claim not found is a defect.
4. Check the structure, the id scheme, the template and the glossary terms, and that no secret, internal-only host or regulated data appears.
5. Sort the defects:
   - small and certain (a typo, a broken link, a banned synonym): fix it or suggest the fix;
   - substantive (a claim that cannot be verified, a change of meaning): hold the change, comment with the evidence, and report. A "small" fix that changes meaning is substantive.
6. Merge only as `delivery.merge_policy` allows: `owner`, never merge, hand it over; `reviewer`, the approving reviewer merges, never the author; `auto-when-green`, only once your checks pass. A written, scoped exception from the owner applies only within its scope.

## Verdict
One line per change reviewed:

```
Reviewed: <change link>: APPROVED | MERGED (<policy>) | HELD (<reason>)
```

## Report after an update
```
Knowledge after <merged change link>, default branch @ <commit>
Concepts changed: <ids>
Knowledge base / Shared skills / Repository docs: <change link> | skipped: <reason>
Validator: PASS | FAIL <error> | none configured
```
