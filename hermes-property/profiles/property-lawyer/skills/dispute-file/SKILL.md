---
name: dispute-file
description: "Prepare a dispute file for the real lawyer"
metadata:
  hermes:
    config:
      - key: property.jurisdictions
        description: "Regions in play, e.g. BE-WAL,BE-BRU,BE-VLA,FR; or detect"
        default: "detect"
---
# Dispute file

## When to use

A dispute arises or looms: tenant, seller, buyer, co-ownership, building
contractor, works client, administration. Before consulting a lawyer, or to
save the lawyer time if one is already instructed.

## Prerequisites

| Needs | Why | Check |
|---|---|---|
| The documents of the dispute (required) | every fact needs proof | numbered inventory, every document opens |
| The investor's chronology | link the documents | his words, dated |

If a required prerequisite is missing, stop before step 1. Say which one, what
it blocks, and the smallest access that would unblock it (read-only first). Do
the parts that do not need it only if they still make sense alone. Never
replace data you could not read with an estimate, and never report "nothing
found" when the lookup failed.

## Configuration

- `property.jurisdictions`: designates the text, the competent court and the
  time limits. `detect` (default): region or country of the facts, stated and
  confirmed.

If a value is unset or `detect`, say what you used, and give the line that
sets it: `hermes config set skills.config.<key> <value>` (one profile:
`hermes -p <profile> config set …`).

## Steps

1. **Chronology**: each fact, dated, with the document that proves it
   (quoted). A fact without a document is marked as such.
2. **Documents**: a numbered inventory, with what is missing and who holds it.
   Ask for the missing document; do not reconstruct it.
3. **Qualification**: which contract, which regime, which region, which
   competent court.
4. **Rule and text**: article, quotation, version date (skill
   `primary-law-sources`).
5. **Running time limits**: limitation, appeal, notice, formal notice;
   deadline computed, calculation shown. The nearest first.
6. **What he can do alone** (letter, conciliation, insurance claim) and what
   needs a lawyer or a bailiff.
7. **The weak points of his position**, with the same rigor as the strong
   ones.
8. **The exact question** for the lawyer, and what to attach.
9. **Adversarial review** before delivering.

## Output

A six-part file: chronology, documents, rule, time limits, options, weak
points. At the top, the nearest deadline and the action it requires. At the
bottom, the question for the lawyer, and what remains TO VERIFY (including
"case law not consulted").

## Pitfalls

- Predicting who will win: say what tips the balance, not the outcome.
- Letting a time limit run while gathering documents.
- Sending a formal notice: it is a draft; he or his lawyer sends it.
- Citing case law from memory to reassure him.
