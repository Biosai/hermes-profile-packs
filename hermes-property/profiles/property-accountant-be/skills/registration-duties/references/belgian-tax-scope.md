# Belgian tax scope, and the regimes to examine

## No rate from memory

A rate, an allowance, a time limit, a cap is read in the text in force, with
its version date, or comes from the written answer of the investor's
accountant recorded in the investor file. Scales change, often on 1 January,
and not at the same time in the three regions. A figure from a conversation
with a general-purpose assistant, a website or the seller's spreadsheet is a
hint of where to look, never a source.

What the accountant's written answer has not confirmed is presented as
**options**, never as a single value: between two registration-duty regimes,
the difference on a single property can be worth a whole margin.

## Registration duties (*droits d'enregistrement*): the region first

Setting `property.jurisdictions`, otherwise from the property's address.
Wallonia, Flanders and Brussels each have their code, rates and regimes.
Regimes to examine:

- the ordinary rate;
- the reduced regime for buy-to-resell professionals (property dealer,
  *marchand de biens*) and its conditions of form, resale deadline and number
  of transactions;
- refund on a quick resale;
- allowances and regimes reserved for individuals, which generally do not
  apply to a company: to be checked.

Formal conditions are checked **deed by deed**: a statement missing from the
deed loses the reduced regime, often without a refund.

**The regime applied by default is the one in the investor file.** The most
favorable regime is presented as a scenario, with its conditions, until the
deed has met them.

## Particular structures

Purchase option, sale by units, split purchase (land and building),
contribution in kind: the duty regime depends on the drafting and on who buys.
Present scenarios, with conditions checked with `property-notary`.

## The rest of the scope

- **VAT** (skill `vat-regimes`): new construction, sale of a new building,
  renovation and its reduced rates under conditions (age of the dwelling,
  private use, certificate), demolition-reconstruction, accommodation with
  services.
- **Corporate income tax**, when the investor acts through a company (skill
  `corporate-tax-per-deal`): property held as inventory or as a fixed asset,
  depreciation, capital gain, reduced rate under conditions. How the investor
  wants tax shown (per deal or at year end) is one of the investor's rules:
  read it in the investor file.
- **The investor personally**: rent the investor receives from their company,
  risk of requalification, letting in their own name. Flag them: there is
  often a company-versus-individual trade-off.
- **Costs of the deal** (skill `deal-costs`): deed costs and fees, public-sale
  costs, property withholding tax (*précompte immobilier*), loan costs, own
  funds tied up.
- **Reading annual accounts** (the Centrale des bilans of the National Bank of
  Belgium): a target company, a seller, a commercial tenant.

## Outside this profile

- France, and any Belgian company that holds property in France:
  `property-accountant-fr` (this profile handles the Belgian half it flags).
- Whether the deed carries the statement that opens a regime:
  `property-notary`.
- The choice of strategy: `property-investment-partner`.
- A dispute with the tax authority, a clause: `property-lawyer`.
