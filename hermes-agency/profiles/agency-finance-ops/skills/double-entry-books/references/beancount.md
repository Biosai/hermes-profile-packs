# Beancount

Used when `books.format` is `beancount`. The books' own notes win over this page where they differ.

## Checker
`bean-check <main file>`, run from the books' own folder: `include` lines and document paths resolve from there. No output means the ledger passes. Fix every error; never comment an entry out to silence one.

## An entry
```
2025-03-14 * "Payee" "Narration" ^invoice-2025-031
  document: "documents/Expenses/Office/2025-03-14.invoice.pdf"
  Expenses:Office:Supplies    42.00 EUR
  Assets:Bank:Checking       -42.00 EUR
```
- `*` marks a complete entry, `!` one to review.
- Account names start with one of the five roots the ledger uses (by default `Assets`, `Liabilities`, `Equity`, `Income`, `Expenses`).
- An account exists only once opened: `2025-01-01 open Assets:Bank:Checking EUR`. Open a new one only when none fits.

## Balances
`2025-04-01 balance Assets:Bank:Checking 1234.56 EUR` asserts the balance at the start of that day: date it the day after the statement's date.

## Foreign currency and lots
- Price per unit: `100.00 USD @ 0.92 EUR`; total price: `100.00 USD @@ 92.00 EUR`. Give the rate's source in metadata (`rate-source: "..."`).
- A lot is bought at a cost, `10 TOKEN {250.00 EUR}`, and sold from that cost, `-10 TOKEN {250.00 EUR} @ 300.00 EUR`, with the gain posted to an income account.
- The lot method is declared on the account, for example `open Assets:Broker:TOKEN TOKEN "FIFO"`.

## Links, estimates, metadata
- `^link` on both entries joins the two legs of one flow, for example a payment recorded in two owners' books.
- An estimate carries `estimate: TRUE` and `basis: "..."` as metadata, removed when the document arrives.

## Documents
- With `option "documents" "<folder>"`, each file sits under `<folder>/<Account/Path>/` and is named `YYYY-MM-DD.<description>.<ext>`. Books holding several ledgers keep one such folder per book, for example `documents/<book>/<Account/Path>/`.
- A documents folder named in the options and missing on disk fails the check. Version control does not keep empty folders: put a placeholder file in each.
