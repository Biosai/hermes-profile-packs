# Report format

```
Loss: <step> loses <n of N> outside people (<window>, server-side)
Page says: <one sentence>   Substitute: <what they use instead>
Customers say: "<quote>" (<source>), "<quote>" (<source>)
Mismatch: <customer | problem | words | price>: <one line>
Test: <one change, or the evidence plan>. Kill line: <metric, threshold, date>. Owner: <...>
Also found, not the blocker: <defect, tracking status>
Dropped: <new features, page tests, more ad budget, ...>
```

- Counts below ten are given as counts with their window.
- Each quote names its source. A quote used outside the report needs the person's consent.
- With `growth.analytics_source` or `growth.payments_source` set to `none`, say which lines rest on behaviour observed directly instead of measured.
