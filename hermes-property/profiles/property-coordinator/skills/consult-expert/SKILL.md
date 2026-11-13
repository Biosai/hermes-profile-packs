---
name: consult-expert
description: "Consult another profile and quote its opinion as its own"
metadata:
  hermes:
    config:
      - key: property.investor_file
        description: "Where the investor file lives: memory or a path"
        default: "memory"
---
# Consult an expert on the team

Use when a question touches another profile's domain (see the roster in the preloaded `panel-rules` skill), and always consult `property-lawyer` for a legal question, even when it comes up in passing.

## Prerequisites

| Needs | Why | Check |
|---|---|---|
| The host's delegation between profiles (required) | consult another profile | the target profile is among the installed profiles |
| The useful file (required) | the expert has heard nothing | property, region, figures and documents are in the question |

If a required prerequisite is missing, stop before step 1. Say which one, what
it blocks, and the smallest access that would unblock it (read-only first). Do
the parts that do not need it only if they still make sense alone. Never
replace data you could not read with an estimate, and never report "nothing
found" when the lookup failed.

## Configuration

- `property.investor_file`: `memory` (default) → the expert cannot see the
  investor file: copy the useful lines into the consultation. A path → cite
  the path and the lines; the expert re-reads them.

If a value is unset or `detect`, say what you used, and give the line that
sets it: `hermes config set skills.config.<key> <value>` (one profile:
`hermes -p <profile> config set …`).

## Procedure

1. **Choose the right profile**: the domain that owns the question, not the
   one that "will probably know". Law → lawyer; tax figure → the accountant of
   that country; deed → notary; planning → architect; works budget → works
   estimator; trade-off → investment partner. A two-sided question (law and
   tax) goes to both.
2. **Check it is installed** with the host's delegation tools. A profile named
   in this text is not proof that it exists here.
3. **Write the consultation**: start with "[Internal consultation]", then the
   useful file (property, region, deal structure, figures and their source,
   quoted documents), the exact question, and the expected answer format. Pass
   the investor-file lines it needs: it has not heard them.
4. **Pass only what is necessary**: not the whole file, not the history.
5. **Read the whole answer**, reservations included. If it lacks a source or a
   date, ask for it rather than filling the gap.
6. **Quote the opinion as theirs**: "according to `property-notary`: …", with
   their reservations word for word and their "TO VERIFY" marks kept.
7. **Two diverging opinions are both shown**, with their reasons; you do not
   choose between them.
8. **Failure or absence**: answer without that opinion, and say so in one line.

## Decision rules

- Never answer from general knowledge in another expert's domain to save time.
- Quote, do not rephrase: a rephrased opinion loses the reservation that
  mattered.
- In an internal consultation the expert answers the profile and names what is
  missing; it never questions the investor.
- Never announce that an expert was consulted when the call failed.
- By default on a concrete property, consult `property-investment-partner` to
  weigh the deal (it consults the works estimator, architect, notary and
  accountants itself) and `property-lawyer` as soon as a legal point appears,
  even in passing.

## Quality gate

The consultation is done when the investor has the answer and what it rests on
(quoted opinions with their reservations, documents, dated sources), diverging
opinions are both shown, and a profile that was absent or failed is named in
one line. The deliverable never shows the plumbing: no "I am launching a
consultation".
