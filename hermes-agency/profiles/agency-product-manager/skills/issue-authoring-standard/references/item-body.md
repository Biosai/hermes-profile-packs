# The item body

Write the sections in this order. Leave none out: write "none" where a section is empty, so the reader knows it was considered.

1. **Context / why**: who is affected, which flow, what it costs.
2. **Real data**, leading with the measurement: the command run and its actual output, the request with its payload, the error body, log excerpts with timestamps, the relevant rows (identifiers, never sensitive contents), the primary source quoted at `file:line`. Add what you tried that did not work: an obvious fix that made things worse is written down so that nobody merges it blind.
3. **Repro steps**: numbered, from a clean state, exact enough to paste.
4. **Expected versus actual.**
5. **Acceptance criteria**: testable checkboxes, written with `acceptance-criteria`, including which end-to-end flows are added or updated. Name tests and flows; never write an expected test total.
6. **Links**: related items and pull or merge requests by full URL, code by permalink at a commit. Reference related items without auto-closing keywords.
7. **Data change**: "none", or the existing rows that must change, per environment.
8. **Open questions**, each addressed to the person who owns the answer: product questions to whoever leads the product, technical ones to the technical owner. A real trade-off is stated as the decision needed, never answered by you: an item that silently assumes a product decision ships that assumption.

## Title
`<area>: <observable problem or outcome>`, in the glossary's terms. With `delivery.repo_layout` set to `monorepo`, the area names the affected package.

## Priority
One line with the reason, in this order of severity:
1. data integrity, and anything that moves money or permissions;
2. user-facing breakage;
3. operator convenience;
4. polish.

Size is given beside the priority. It helps rank; it is never a status.

## Findings made in passing
Capture them now, with their data, before they are lost: a finding reported only in conversation never gets fixed. Every verified finding not fixed in this turn becomes an item, non-code ones included: documents that contradict each other, brand or voice drift, wrong asset dimensions, stale claims, missing access. Something fixed in this turn is a pull or merge request, not an item.

## After filing
- Re-read the item from the tracker: title, labels, full body.
- Give it a status when the tracker's items sit on a board with a status field.
- If the finding changes durable context (a decision record, the knowledge base), update that in the same pass.
- If an earlier claim of yours was wrong, correct it in the item.
