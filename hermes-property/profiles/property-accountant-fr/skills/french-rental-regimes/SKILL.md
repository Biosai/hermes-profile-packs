---
name: french-rental-regimes
description: "Compare French rental regimes and holding entities"
metadata:
  hermes:
    config:
      - key: property.jurisdictions
        description: "Regions in play, e.g. BE-WAL,BE-BRU,BE-VLA,FR; or detect"
        default: "detect"
---
# French rental regimes

Use when a French property is meant to be let, or the investor wonders through which entity to hold a French property.

## Prerequisites

| Needs | Why | Check |
|---|---|---|
| The property's address and type of letting (required) | municipal authorizations, regime | municipality known |
| Access to Légifrance and the BOFiP (required, free) | no figure from memory | the text opens; otherwise TO VERIFY |

If a required prerequisite is missing, stop before step 1. Say which one, what
it blocks, and the smallest access that would unblock it (read-only first). Do
the parts that do not need it only if they still make sense alone. Never
replace data you could not read with an estimate, and never report "nothing
found" when the lookup failed.

## Configuration

- `property.jurisdictions`: without FR, say that France is not configured and
  propose nothing French on your own; a question the investor asks still gets
  its answer. `detect` (default): FR if the property is in France, then
  confirmed.

If a value is unset or `detect`, say what you used, and give the line that
sets it: `hermes config set skills.config.<key> <value>` (one profile:
`hermes -p <profile> config set …`).

## Procedure

1. **State the status of your sources**: without a text read, **TO VERIFY**.
2. **Qualify the letting**: unfurnished (property income), long-term
   furnished, furnished tourist let (*meublé de tourisme*, short-term),
   letting to companies. The rules on furnished tourist lets change through
   successive reforms: read the version in force.
3. **Authorizations**: change of use, registration and declaration number,
   caps on nights in some municipalities — check with `property-architect`
   for planning and the municipality.
4. **Letting bans** by energy class (the DPE energy performance diagnosis):
   read the timetable on Légifrance, cross-check with
   `property-works-estimator`.
5. **Entity**: the Belgian company, a French non-trading property company
   (*société civile*), a French simplified joint-stock company (SAS), direct
   ownership. For each: tax on results, whether depreciation is possible,
   exit (capital gain, duties on the sale of shares), obligations. Present
   them in a table, without deciding.
6. **Belgian half**: how Belgium treats the income depending on the entity;
   consult `property-accountant-be`.
7. **Cash flow**: rent and cost figures come from
   `property-investment-partner`; you add the tax per entity, as ranges.

## Decision rules

- The entity is chosen before the purchase: changing it later costs duties.
  Say it before the investor signs, not after.
- Never compute a short-term yield without checking that it is authorized in
  the municipality.
- Never ignore a letting-ban timetable that falls within the holding period.
- Never present one entity as "the best": that is the call of the investor and
  their chartered accountant.

## Quality gate

The comparison is done when every regime and entity is set side by side,
without a choice made for the investor. The deliverable is a table of regime ×
entity: tax, depreciation, authorizations, obligations, exit, effect as a
range, text and version (or TO VERIFY); then the Belgian opinion quoted and
the question for a French chartered accountant.
