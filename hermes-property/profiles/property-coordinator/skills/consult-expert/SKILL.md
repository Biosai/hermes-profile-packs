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

## When to use

As soon as a question touches another profile's domain (table at the end of
the SOUL) — and always `property-lawyer` for a legal question, even when it
comes up in passing. Every profile uses this skill, not only the coordinator.

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

## Steps

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

## Output

The answer to the investor and what it rests on (quoted opinions, documents,
dated sources), without "I am launching a consultation": the plumbing stays
hidden.

## Pitfalls

- Answering from general knowledge in another expert's domain to save time.
- Rephrasing an opinion until the reservation that mattered disappears.
- Letting the expert question the investor: in an internal consultation, it
  answers the profile and names what is missing.
- Announcing that an expert was consulted when the call failed.
