---
name: listing-photo-review
description: "Review a listing, its photos and certificates"
metadata:
  hermes:
    config:
      - key: property.jurisdictions
        description: "Regions in play, e.g. BE-WAL,BE-BRU,BE-VLA,FR; or detect"
        default: "detect"
---
# Listing and photo review

Use when a property arrives with a listing, photos, an energy certificate or a report, before any estimate, or to prepare a viewing.

## Prerequisites

| Needs | Why | Check |
|---|---|---|
| The listing and its photos (required) | you read what is shown | the photos open at a legible size |
| The certificates announced | energy, electrical, asbestos | every certificate opens and is dated |

If a required prerequisite is missing, stop before step 1. Say which one, what
it blocks, and the smallest access that would unblock it (read-only first). Do
the parts that do not need it only if they still make sense alone. Never
replace data you could not read with an estimate, and never report "nothing
found" when the lookup failed.

## Configuration

- `property.jurisdictions`: names the expected certificates (PEB in Wallonia
  and Brussels, EPC in Flanders, DPE in France) and the obligations they
  trigger. `detect` (default): derived from the address.

If a value is unset or `detect`, say what you used, and give the line that
sets it: `hermes config set skills.config.<key> <value>` (one profile:
`hermes -p <profile> config set …`).

## Procedure

1. **Inventory what you have**: number of photos, rooms shown, rooms missing,
   certificates (energy, electrical, asbestos, soil) and their date.
2. **Room by room, what the photo shows**: floors, walls, ceilings, joinery,
   sanitary fittings, kitchen, radiators, electrical panel, damp marks,
   cracks. Note the photo number.
3. **Envelope**: roof (type, visible condition, viewing angle), façades,
   windows, gutters, visible insulation. A roof seen from below does not show
   its condition.
4. **Risk signals**: stepped cracks, stains, saltpeter, reported smells, old
   electrical installation, old boiler, materials likely to contain asbestos
   given the period, sagging.
5. **Certificates**: the energy class and what it implies (obligations, aid,
   letting bans: skill `renovation-obligations-and-aid`), remarks from the
   electrical inspection.
6. **Consistency**: the listing says "renovated", the photo shows an old
   panel; the announced area does not match the number of rooms. Pass the gap
   on.
7. **What is missing**: every element not visible becomes a "to check at the
   viewing" line, never an assumption.

## Decision rules

- A photo shows what it shows: never assume the condition of what is not
  photographed. A room not photographed, a roof seen from below, a cellar
  missing from the photos (often missing for a reason) are "to check at the
  viewing".
- A retouched or old agency photo is not the current condition.
- Flag a structural doubt, do not diagnose it from a single photo: an engineer
  or an expert will.
- Count the common parts of a building in co-ownership.

## Quality gate

The review is done when every visible element has an observed condition and
every element not visible has a line to check at the viewing. The deliverable
is a table of visible items (element, observed condition, photo no., likely
level of intervention), the risk signals, and the "to check at the viewing"
list ranked by impact on the budget.
