# Approval request and item record

One request per item. The owner is the person accountable for the brand or the account, and must be able to approve from the request alone.

```
<brand> / <channel> / proposed <date time, time zone>
<final content in full>
Audience: <segment, size; for email, the consent basis>
Sources: <links, or the measured metric with its date>
Measured after: <which numbers, after which window>
```

After the answer, keep one record per item and update its status as it moves:

```
<brand> / <channel> / proposed <date time>
<final content, or the link to the draft>
Audience: <segment, size, consent basis for email>   Sources: <links>
Status: draft | awaiting approval | approved (<reference>) | published (<link>) | measured
```

The approval reference is the Hermes approval, or the owner's message that approved that exact item, quoted with its date.
