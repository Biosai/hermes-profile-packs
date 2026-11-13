---
name: double-entry-books
description: "Keep double-entry books for a person or a company"
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

Use when a person or a company keeps, or wants to keep, double-entry books: booking documents, reconciling balances, closing a month, or preparing a tax question. This is record-keeping and education, not regulated accounting, tax, legal or investment advice.

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| Read access to the books at `books.location` | every figure comes from them | the ledger files list |
| The format's checker, when it has one | balance and syntax checks | `command -v <tool>` |
| Write access, once the owner agreed to changes | adding entries | the file is writable |
| `git`, when the books are version-controlled | a reviewable change | `git -C <books> status` |

If one is missing, stop before step 1 and say which, what it blocks, and the smallest access that would unblock it (read-only first). Without the checker, say entries are unchecked. Never report a balance you could not compute.

## Configuration
- `books.location`: unset means ask where the books are; never search for them.
- `books.format` selects the syntax and the checker: [beancount](references/beancount.md), [hledger](references/hledger.md), [ledger](references/ledger.md) or [spreadsheet](references/spreadsheet.md). `detect` reads the file extensions there (`.beancount`; `.journal` or `.hledger`; `.ledger` or `.dat`; `.csv`, `.xlsx` or `.ods`), says what it found and suggests saving it.
- Set values with `hermes config set skills.config.<key> <value>`.

## Procedure
1. Identify whose money each item is: which person or legal entity. When unclear, ask.
2. Read the books' own notes (accounts, currencies, conventions) and the reference for `books.format` first.
3. Book balanced entries: date, payee, narration, accounts, amounts, currency and a link to the source document, filed beside the books under their convention. Keep a foreign amount in its original currency, with the rate used and its source. Open a new account only when none fits, and say so.
4. State the lot method for assets held in lots, for example FIFO. Link both legs of a flow between two owners. Mark an estimate as one, with its basis, and replace it when the document arrives.
5. Change files only when asked or agreed; under version control, on a branch, as a reviewable change with the documents attached.
6. Run the format's checker on every ledger touched, from the books' own folder, and fix every error. Without a checker, recompute the totals and show them.
7. Reconcile each account against its statement at the same date. Explain each difference; an unexplained one stays visible as an open item.
8. For a monthly close or a tax question, follow [closing and tax questions](references/close-and-tax.md).

## Decision rules
- Separate books for separate owners: a person's money and a company's never share a book or a summary line. A company's trading name is that company. Money one owner paid for another is recorded as owed between them, in each book.
- Every figure stated comes from the books, a document or a cited source, with its date. Where an accountant or a filed return holds the statutory figures, those prevail.
- Keeping the books never pays, transfers, trades, signs, files or contacts anyone: those steps are the owner's.
- No plug or "adjustment" entry to make a check or a reconciliation pass, no silenced checker error: find the real difference.
- Add to an open change touching the same ledger rather than opening a parallel one. Where ready changes merge automatically, open a draft, and say whether the repository's checks run the checker.
- Balances are not copied outside the books, and account numbers are masked to their last four characters.
- Unknown tokens sent to a wallet: never interact, value or approve.

## Quality gate
Done when the answer matches what was asked, every ledger touched passes its checker or shows recomputed totals, and facts, the owner's statements and assumptions are kept apart, each figure with its as-of date.
