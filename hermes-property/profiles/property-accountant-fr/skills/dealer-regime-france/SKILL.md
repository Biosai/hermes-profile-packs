---
name: dealer-regime-france
description: "Frame buy-to-resell in France: duties, VAT, profits"
metadata:
  hermes:
    config:
      - key: property.jurisdictions
        description: "Regions in play, e.g. BE-WAL,BE-BRU,BE-VLA,FR; or detect"
        default: "detect"
---
# Buy-to-resell in France (property dealer regime)

## When to use

When the investor's company considers buying in France to resell, with or
without works, as a whole or by units.

## Prerequisites

| Needs | Why | Check |
|---|---|---|
| The property, its nature and the buying entity (required) | duties and VAT depend on them | new, land or old, and the buyer, in writing |
| Access to Légifrance and the BOFiP (required, free) | no figure from memory | the text opens; otherwise TO VERIFY |

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

1. **State the status of your sources**: without Légifrance or the BOFiP read
   in this conversation, every figure is **TO VERIFY**.
2. **Transfer duties** (*droits de mutation*): read the regime of the
   undertaking to resell (*engagement de revendre*; CGI, art. 1115 — version in
   force; the BOFiP series on transfer duties): time limit, conditions,
   statement in the deed, penalty if not resold. Check the statement in the
   deed with `property-notary`.
3. **VAT**: read the property VAT regime (BOFiP series on property VAT; CGI,
   art. 268 for VAT on the margin — version in force): is the sale subject to
   VAT, on the full price or on the margin, depending on the nature of the
   property (new, building land, old) and the conditions of acquisition.
4. **Profits**: taxation of property dealer profits (BOFiP series on the scope
   of business profits) and, for a Belgian company, the link with French
   corporate income tax (skill `belgian-company-in-france`).
5. **Cost in scenarios**: one scenario per plausible duty and VAT regime, with
   the effect on the ceiling price for `property-investment-partner`.
6. **Flag the Belgian half** to `property-accountant-be`.

## Output

A table per tax (duties, VAT, tax on profits): regime, text and version (or
TO VERIFY), conditions, effect as a range. Then the statements the deed must
contain, for `property-notary` to check, and the question for a French
chartered accountant.

## Pitfalls

- Assuming a Belgian regime has an identical French equivalent.
- Choosing between VAT on the margin and VAT on the full price without reading
  the acquisition conditions that open the margin scheme.
- Letting the resale deadline of an undertaking pass: the penalty is due.
- Costing duties without knowing whether the buying entity is Belgian or
  French.
