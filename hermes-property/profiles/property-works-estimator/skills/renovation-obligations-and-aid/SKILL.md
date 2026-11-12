---
name: renovation-obligations-and-aid
description: "List a property's renovation obligations and aid"
metadata:
  hermes:
    config:
      - key: property.jurisdictions
        description: "Regions in play, e.g. BE-WAL,BE-BRU,BE-VLA,FR; or detect"
        default: "detect"
---
# Renovation obligations and aid

## When to use

When a property has a poor energy class; when the buyer could be required to
renovate; when equipment (heating, tank) is at the end of its life; when aid
is mentioned in a calculation.

## Prerequisites

| Needs | Why | Check |
|---|---|---|
| The address and the target acquisition date (required) | the obligations depend on them | region and date established |
| The property's energy certificate | starting class | the certificate opens and is dated |
| Access to the decrees and aid bodies (required) | no deadline from memory | the text opens with its date |

If a required prerequisite is missing, stop before step 1. Say which one, what
it blocks, and the smallest access that would unblock it (read-only first). Do
the parts that do not need it only if they still make sense alone. Never
replace data you could not read with an estimate, and never report "nothing
found" when the lookup failed.

## Configuration

- `property.jurisdictions`: decides which decrees and aid schemes to read.
  `detect` (default): derive the region from the property's address, state it,
  and have it confirmed.

If a value is unset or `detect`, say what you used, and give the line that
sets it: `hermes config set skills.config.<key> <value>` (one profile:
`hermes -p <profile> config set …`).

## Steps

1. **Establish the region** and the deed date: obligations differ by region
   and often apply from an acquisition date.
2. **Renovation obligations on purchase**: is there an obligation to reach a
   class within a period after acquisition? Read the decree in force, not the
   information page: an official page and the decree have already disagreed on
   the deadline. A draft text is not law.
3. **Certificates and reports at sale**: energy performance certificate (PEB,
   EPC), asbestos certificate, soil certificate, depending on the region.
4. **Letting bans** below an energy class (notably in France): timetable read
   on the text.
5. **Equipment**: bans on installing or replacing certain fossil-fuel heating
   systems, phased in over time; read the timetable on the decree and never
   budget equipment being phased out in a deep renovation.
6. **Aid**: grants, low-rate loans, tax reductions. For each: text and date,
   open or closed, **open to a company? to a landlord?**, conditions (class
   jump, prior audit, owner occupation, income), caps. A scheme can be
   replaced overnight: check that it is open at the date of the application.
7. **Credit it to a deal** only if every condition is met and verified;
   otherwise, a scenario marked **TO VERIFY**.

## Output

A table of obligations (text, version, deadline, cost of compliance as a
range) and a table of aid (text, status, the investor's eligibility,
conditions, amount as a range or "not eligible").

## Pitfalls

- Crediting aid reserved for households who occupy the dwelling to a company
  that buys to resell.
- Citing a deadline from a press release or an aid website: cite the text.
- Forgetting that an obligation creates the discount the investor exploits:
  it is costed, not dodged.
