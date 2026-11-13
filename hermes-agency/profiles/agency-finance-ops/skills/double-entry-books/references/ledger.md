# Ledger

Used when `books.format` is `ledger` (the `ledger` command-line tool). The books' own notes win over this page where they differ.

## Checker
`ledger -f <main file> balance`, run from the books' own folder so `include` lines resolve: an entry that does not balance or a failed assertion stops the report with an error. Add `--pedantic` when the books declare their accounts and commodities, so an undeclared one is an error too.

## An entry
```
2025/03/14 * Payee
    ; Narration
    ; Document: documents/2025-03-14-invoice.pdf
    Expenses:Office:Supplies     42.00 EUR
    Assets:Bank:Checking        -42.00 EUR
```
- `*` marks a cleared entry, `!` a pending one.
- At least two spaces separate the account name from the amount.
- Declare an account with `account Assets:Bank:Checking`. Open a new one only when none fits.

## Balances
A balance assertion follows a posting's amount: `Assets:Bank:Checking   -42.00 EUR = 1234.56 EUR` asserts the account's balance after that posting. Put it on the last posting dated on or before the statement's date.

## Foreign currency and lots
- Price per unit: `100.00 USD @ 0.92 EUR`; total price: `100.00 USD @@ 92.00 EUR`. Give the rate's source in a note.
- A lot keeps its cost: `10 TOKEN {250.00 EUR}`, sold as `-10 TOKEN {250.00 EUR} @ 300.00 EUR`. State the lot method in the books' notes: the tool does not choose the lot.

## Links, estimates, metadata
- Metadata lives in notes as `; Name: value`, tags as `; :tag:`. Join the two legs of one flow with the same `Link:` value on both entries.
- An estimate carries `; Estimate: true` and `; Basis: ...`, removed when the document arrives.

## Documents
Ledger has no documents convention of its own: follow the books' notes, and record the path in a `Document:` note on the entry.
