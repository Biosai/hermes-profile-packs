# Report format

## The audit
```
Revenue state as of <date> (sources: <analytics>, <payments>; read <how>, pulled <time>)
Awkward number first: <number and why it matters>
Funnel: sessions <n> (paid <x>%) -> intent <n> -> signup <n> -> activated <n> -> paid <n>
By channel: paid <rate> vs unpaid <rate>; best source ever: <source, rate, window>
Revenue: <amount> | last completed payment: <date> | not measured: <what, and what it leaves unknown>
Binding constraint: <step> (<evidence>)
Next test: <change>. Kill line: <metric> >= <threshold> by <date>. Dropping: <...>
```

## The quick pulse ("how are we doing today?")
One read, a short answer, in this order:
1. revenue, with the date of the last real payment;
2. the last 7 days against the previous 7: sessions, paid share, funnel steps as people;
3. the 90-day funnel, in counts;
4. the last step an outside person reached;
5. what changed the series, and what that does not explain;
6. one next step, as a question, and what is dropped.
