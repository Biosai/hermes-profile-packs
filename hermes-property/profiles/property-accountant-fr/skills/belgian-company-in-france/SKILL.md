---
name: belgian-company-in-france
description: "Frame the tax of a Belgian company investing in France"
metadata:
  hermes:
    config:
      - key: property.jurisdictions
        description: "Regions in play, e.g. BE-WAL,BE-BRU,BE-VLA,FR; or detect"
        default: "detect"
---
# A Belgian company investing in France

## When to use

As soon as the investor's Belgian company considers a French operation:
purchase, letting, resale, or holding a property already acquired.

## Prerequisites

| Needs | Why | Check |
|---|---|---|
| FR in `property.jurisdictions`, or his explicit request (required) | the scope opens at his request | the setting contains FR, or his request is quoted |
| The company's articles and situation (required) | qualification and obligations | articles and register extract open |
| Access to Légifrance and the BOFiP (required, free) | no figure from memory | the series or article opens; otherwise everything is TO VERIFY |

If a required prerequisite is missing, stop before step 1. Say which one, what
it blocks, and the smallest access that would unblock it (read-only first). Do
the parts that do not need it only if they still make sense alone. Never
replace data you could not read with an estimate, and never report "nothing
found" when the lookup failed.

## Configuration

- `property.jurisdictions`: without FR, say that France is not configured and
  propose nothing French on your own; a question he asks himself still gets
  its answer. `detect` (default): FR if the property is in France, then
  confirmed.

If a value is unset or `detect`, say what you used, and give the line that
sets it: `hermes config set skills.config.<key> <value>` (one profile:
`hermes -p <profile> config set …`).

## Steps

1. **State the status of your sources** first: anything not read on
   Légifrance or the BOFiP in this conversation is **TO VERIFY**.
2. **Qualify the activity in France**: habitual resale (property dealer,
   *marchand de biens*), unfurnished or furnished letting, holding as an asset.
   The qualification decides which taxes apply.
3. **Corporate income tax**: income and gains from a property located in France
   are taxable there in principle; check whether there is a permanent
   establishment and its consequences (the BOFiP series on the territorial
   scope of corporate tax).
4. **Annual tax on property held by legal entities** (CGI, art. 990 D and
   following — read the version in force): check the exemptions and the
   filings they depend on; it can cost every year if the exemption is not
   claimed.
5. **Capital gains of non-residents** (CGI, art. 244 bis A — version in
   force): withholding, any fiscal representative.
6. **Franco-Belgian tax treaty**: check on an official source which text is in
   force at the date of the operation, then read the article on income from
   immovable property and the method for eliminating double taxation.
7. **Filing obligations**: registration, tax returns, declaration of property
   held, fiscal representative.
8. **Flag the Belgian half** to `property-accountant-be`: how Belgium treats
   this income or gain, and quote its opinion.

## Output

Per tax: rule, text (article, BOFiP series, version or TO VERIFY), effect as a
range, filing obligation, deadline. Then the Belgian opinion quoted, and the
question for a French chartered accountant.

## Pitfalls

- Forgetting the annual tax on property: it does not show in a margin
  calculation, it shows every year.
- Citing a treaty article without checking which text is in force.
- Treating France alone: a cross-border operation has two halves.
- Proposing a French property on your own initiative when
  `property.jurisdictions` does not include FR.
