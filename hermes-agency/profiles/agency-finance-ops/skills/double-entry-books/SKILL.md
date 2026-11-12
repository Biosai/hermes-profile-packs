---
name: double-entry-books
description: "Keep plain-text double-entry books for a person or company"
metadata:
  hermes:
    config:
      - key: books.format
        description: "Bookkeeping format: beancount, hledger, ledger, spreadsheet, or detect"
        default: "detect"
      - key: books.location
        description: "Path to the folder or repository that holds the books"
        default: ""
    prerequisites:
      commands: ["bean-check", "hledger", "ledger", "git"]
---
# Double-Entry Books

Use when the user keeps, or wants to keep, double-entry books: booking receipts, invoices
and statements, reconciling balances, closing a month, or preparing a tax question. This is
record-keeping and education, not regulated accounting, tax, legal or investment advice. The
accountant's figures are the statutory ones; these books are the user's management record.

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| Read access to the books at `books.location` | every figure comes from them | the folder opens and lists the ledger files |
| The format's checker: `bean-check` (beancount), `hledger check` (hledger), `ledger` (ledger) | balance and syntax checks | `command -v <tool>` |
| Write access, only when the user agreed to changes | adding entries | the file is writable |
| `git`, when the books are version-controlled | a reviewable change | `git -C <books> status` |

If a required prerequisite is missing, stop before step 1. Say which one, what it blocks, and
the smallest access that would unblock it (read-only first). Without the checker, say that
entries are unchecked; never report balances you could not compute.

## Configuration
- `books.location`: unset means ask where the books are; never search the user's files.
- `books.format`: `detect` looks at the files there (`.beancount`; `.journal` or `.hledger`;
  `.ledger` or `.dat`; `.csv`, `.xlsx`, `.ods` for spreadsheet), says what it found and
  suggests saving it. `spreadsheet` has no checker: totals are recomputed and shown.
- Set values with `hermes config set skills.config.<key> <value>`.

## Principles
- Separate books for separate owners: a person's money and a company's money never share a
  book. A brand or trading name of a company is that company. Money paid personally for the
  company is recorded as owed between them, in each book by its conventions.
- The ledger is the record: every figure stated comes from the books, a document or a cited
  source, with its date. Keeping the books never pays, transfers, trades, signs, files or
  contacts anyone; those steps belong to the user.

## Procedure
1. Identify whose money each item is. When unclear, ask; never guess the entity.
2. Read the books' own notes (accounts, currencies, conventions) before adding to them.
3. Book balanced entries: date, payee, narration, accounts, amounts, currency, a link to the
   source document; foreign amounts in their original currency with the rate used and its
   source. Open a new account only when none fits, and say so. State the lot method for
   crypto and other lots (e.g. FIFO). Link both legs of a flow between owners (beancount
   `^link`). Mark an estimate as such with its basis in metadata (e.g. `estimate: TRUE`,
   `basis: "..."`) and replace it when the document arrives.
4. File each source document beside the books under the format's convention (beancount:
   `documents/<book>/<Account/Path>/`), account numbers masked to the last four in notes.
5. Change files only when requested or agreed; in version control, on a branch, as a
   reviewable change with the documents attached. First look for an open change touching the
   same ledger and add to it: two parallel ledger changes conflict on the same files. Where
   ready changes merge automatically, open it as a draft so nothing lands unseen, and say
   whether the repository's checks run the ledger checker; if not, yours is the only gate.
6. Run the checker on every ledger touched, from the books' own folder (relative document
   paths resolve from there; a missing documents folder fails the check, so keep a placeholder
   file in each), and fix every error; never silence one.
7. Reconcile each account against its statement at the same date. Explain each difference;
   an unexplained one stays visible as an open item, never a plug entry.
8. Monthly close: list the exports only the user can fetch, book and reconcile, then a
   numbers-first summary and the next dated deadlines. Data or access only the user can
   supply is recorded as an action for them, with a check that proves it done.
9. Tax questions, especially across countries: facts with sources, assumptions, options
   with a worked estimate each, what would change the answer, primary sources with an as-of
   date, and the questions to confirm with an accountant or tax adviser.

## Output standard
Match the requested outcome: a direct answer, entries, a reconciliation, a close summary or
a tax options brief. Keep facts, the user's statements and assumptions visibly separate, and
give the as-of date of every figure.

## Traps
- Personal and company items in one book or one summary line.
- An "adjustment" entry to make the check pass. Find the real difference.
- Account numbers or balances copied outside the books. Mask to the last four characters.
- Unknown tokens airdropped to a wallet: never interact, never value, never approve.
