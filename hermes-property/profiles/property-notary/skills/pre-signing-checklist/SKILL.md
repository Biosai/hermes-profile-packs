---
name: pre-signing-checklist
description: "Run the pre-signing checklist before signing"
metadata:
  hermes:
    config:
      - key: property.investor_file
        description: "Where the investor file lives: memory or a path"
        default: "memory"
---
# Pre-signing checklist

Use when a preliminary sale agreement is about to be signed, an option exercised or a bid placed, or the investor says "let's go".

## Prerequisites

| Needs | Why | Check |
|---|---|---|
| The file: documents received, experts' opinions (required) | every answer comes from a document | the documents open |
| The investor file | risks already accepted, safety scenario | the file can be read; otherwise nothing is "accepted" |

If a required prerequisite is missing, stop before step 1. Say which one, what
it blocks, and the smallest access that would unblock it (read-only first). Do
the parts that do not need it only if they still make sense alone. Never
replace data you could not read with an estimate, and never report "nothing
found" when the lookup failed.

## Configuration

- `property.investor_file`: the risks the investor has accepted by decision;
  in `memory` (default), ask `property-coordinator` for them.

If a value is unset or `detect`, say what you used, and give the line that
sets it: `hermes config set skills.config.<key> <value>` (one profile:
`hermes -p <profile> config set …`).

## Procedure

1. **Put each question to the file, not to memory.** For each one, the answer
   comes from a quoted document, or it is "unknown".
   - Is the number of dwellings the strategy assumes recognized?
   - Is the property vacant? If not, which leases, enforceable, until when?
   - Is there a basic deed and a co-ownership manager? Works voted?
   - A planning breach, an expropriation, a pre-emption right?
   - Soil, asbestos, flooding: what do the certificates say?
   - The target duty regime: will the deed carry the required statement?
   - Does the financing cover the price, the costs and the payment deadline?
   - Does a condition precedent protect against each risk not yet cleared?
   - Does the price hold in the safety scenario of
     `property-investment-partner`?
2. **Classify each answer**: cleared (document quoted), to clear before
   signing, covered by a condition precedent, accepted by the investor
   (recorded decision).
3. **An unexpected answer stops the signing** until a decision is made: say
   it clearly, without drama.
4. **Draft the remaining questions**: to the seller or the agency, to the
   notary handling the deed, to the co-ownership manager.
5. **Hand over**: legal risk → `property-lawyer`; duty regime →
   `property-accountant-be`; dwellings → `property-architect`.

## Decision rules

- Run the checklist before the signature, never after: an agreement signed
  before the answers freezes the risks.
- Never tick "cleared" on the seller's word without a document.
- Keep the questions that can stop the deal: a list so long that the investor
  stops reading it protects nobody.

## Quality gate

The checklist is done when every question has an answer taken from a quoted
document, or is marked unknown. The deliverable is the completed checklist
(question, answer, document, status), with the points that must be cleared
before signing at the top, then the draft questions.
