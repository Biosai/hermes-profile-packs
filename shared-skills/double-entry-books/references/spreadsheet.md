# Spreadsheet books

Used when `books.format` is `spreadsheet`. No checker exists: every total is recomputed and shown. The workbook's own notes win over this page where they differ.

## Layout
- One sheet of postings, one row per posting: date, entry id, account, amount (debit positive, credit negative, or two columns), currency, payee, narration, document link.
- One sheet listing the accounts, each with its type: asset, liability, equity, income or expense. Add an account only when none fits.
- One workbook per owner. Never a second owner's rows in the same sheet.

## The checks to recompute
1. Each entry balances: the amounts sharing one entry id sum to zero, per currency. List every id that does not.
2. Every account used is on the accounts sheet.
3. No row lacks a date, an account, an amount or a currency.
4. The balance of each reconciled account at the statement's date equals the statement.
Show the totals you computed and how, so the owner can repeat the check.

## Foreign currency and lots
- Keep the original amount and currency, and add the rate, its source and the converted amount as columns.
- For assets held in lots, keep one row per lot with its quantity and cost, and state the lot method in the workbook's notes.

## Links and estimates
- The two legs of one flow share a link value in a `link` column.
- An estimate is flagged in an `estimate` column with its basis beside it, and replaced when the document arrives.

## Changes
- Without version control, work on a dated copy and hand over the list of rows added or changed.
- Never replace a formula with a typed value, and never hide a row to make a total agree.
