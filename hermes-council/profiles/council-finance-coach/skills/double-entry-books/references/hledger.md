# hledger

Used when `books.format` is `hledger`. The books' own notes win over this page where they differ.

## Checker
`hledger -f <main file> check`, run from the books' own folder so `include` lines resolve. It verifies that the journal parses, that entries balance and that balance assertions hold. `hledger -f <main file> check --strict` also requires every account and commodity to be declared: use it when the books declare them.

## An entry
```
2025-03-14 * Payee | Narration
    ; document: documents/2025-03-14-invoice.pdf
    expenses:office:supplies     42.00 EUR
    assets:bank:checking        -42.00 EUR
```
- `*` marks a cleared entry, `!` a pending one.
- At least two spaces separate the account name from the amount.
- Declare an account with `account assets:bank:checking`. Open a new one only when none fits.

## Balances
A balance assertion follows a posting's amount: `assets:bank:checking   -42.00 EUR = 1234.56 EUR` asserts the account's balance after that posting. Put it on the last posting dated on or before the statement's date.

## Foreign currency and lots
- Price per unit: `100.00 USD @ 0.92 EUR`; total price: `100.00 USD @@ 92.00 EUR`. Give the rate's source in a comment.
- Record the cost of each purchase with `@`. Check what the installed version does about lots before relying on it; otherwise keep one subaccount per lot and state the lot method in the books' notes.

## Links, estimates, tags
- Tags live in comments as `name: value`. Join the two legs of one flow with the same tag on both entries, for example `; link: invoice-2025-031`.
- An estimate carries `; estimate: true` and `; basis: ...`, removed when the document arrives.

## Documents
hledger has no documents convention of its own: follow the books' notes, and record the path in a `document:` tag on the entry.
