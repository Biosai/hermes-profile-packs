---
name: division-and-permits
description: "Say what it takes to divide or create a dwelling"
metadata:
  hermes:
    config:
      - key: property.jurisdictions
        description: "Regions in play, e.g. BE-WAL,BE-BRU,BE-VLA,FR; or detect"
        default: "detect"
---
# Division and permits

Use when a strategy assumes creating a unit, dividing a building, changing a use (shop into dwelling, attic into studio), splitting a plot, or regularizing an unrecognized dwelling.

## Prerequisites

| Needs | Why | Check |
|---|---|---|
| The address and plot (required) | zoning, municipal regulation | the plot can be found on the official geoportal |
| Access to the regional code and the municipal regulation (required) | the rule is read, not assumed | the text opens with its version date |
| An account on a regional portal (optional) | some layers require a login | the login works |

If a required prerequisite is missing, stop before step 1. Say which one, what
it blocks, and the smallest access that would unblock it (read-only first). Do
the parts that do not need it only if they still make sense alone. Never
replace data you could not read with an estimate, and never report "nothing
found" when the lookup failed.

## Configuration

- `property.jurisdictions`: picks the code (Wallonia, Flanders, Brussels,
  France) and the language of the regulation. `detect` (default): derive the
  region from the property's address, state it, and have it confirmed.

If a value is unset or `detect`, say what you used, and give the line that
sets it: `hermes config set skills.config.<key> <value>` (one profile:
`hermes -p <profile> config set …`).

## Procedure

1. **Region, municipality, plot**: establish them. Read the zoning on the
   official geoportal: the regional zoning plan (*plan de secteur*) in
   Wallonia, the regional plans in Brussels, the spatial implementation plans
   in Flanders; the local urban plan (PLU) in France.
2. **Qualify the operation**: creating a dwelling, dividing, changing use,
   changing the number of units, structural works, subdivision. Each
   qualification has its own regime.
3. **Read the regional code in force** on the official source, with its
   version date: does the operation need a permit, is it exempt, does it need
   a declaration? Coverage by region:
   [references/planning-rules-by-region.md](references/planning-rules-by-region.md).
4. **Look for the municipal rules**: division regulation, minimum unit size,
   maximum number of units, parking, planning charges. In Flanders this
   regulation is often the real filter. Note the date of the council decision;
   a city FAQ is not the regulation.
5. **Check the technical conditions** that make a separate dwelling possible:
   fire safety, sanitation standards, minimum areas and heights, natural
   light, independent access.
6. **Estimate the timeline** as a range (preparing the file, processing,
   possible appeals) and the risk of refusal, with what it rests on.
7. **Hand over**: the cost of the required works to
   `property-works-estimator`, whether the deal is worth it to
   `property-investment-partner`, the legal effects of an existing breach to
   `property-lawyer`.

## Decision rules

- Apply the rule of this municipality as in force today, never a neighboring
  municipality's or the one from two years ago: a division threshold read six
  months ago is read again before it supports a deal.
- A permit exemption is not the absence of rules: an exempt operation still
  has to meet the standards.
- A permit timeline is holding time and an assumption of the trade-off: give
  it as a range to `property-investment-partner`; it weighs on the margin as
  much as a cost does.
- Never promise a regularization: only the authority grants it.

## Quality gate

The work is done when the authorization was read in the code in force and the
municipal rules in the regulation itself. The deliverable gives, for each
targeted unit: the authorization required (text, article, version), the
applicable municipal rules (regulation, date), the technical conditions, the
timeline and risk as ranges, what remains **TO VERIFY**, and the question for
the municipality (skill `planning-office-question`).
