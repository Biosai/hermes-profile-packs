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
   source document; foreign amounts with the rate used and its source. Open a new account
   only when none fits, and say so.
4. Change files only when requested or agreed; in version control, on a branch, as a
   reviewable change with the documents attached.
5. Run the checker on every ledger touched and fix every error; never silence one.
6. Reconcile each account against its statement at the same date. Explain each difference;
   an unexplained one stays visible as an open item, never a plug entry.
7. Monthly close: list the exports only the user can fetch, book and reconcile, then a
   numbers-first summary and the next dated deadlines.
8. Tax questions, especially across countries: facts with sources, assumptions, options
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
