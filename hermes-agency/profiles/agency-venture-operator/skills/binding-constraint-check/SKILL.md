---
name: binding-constraint-check
description: "Test a venture plan against its one binding constraint"
metadata:
  hermes:
    config:
      - key: venture.brief
        description: "Path or URL of the brief: customer, voice, constraints, autonomy"
        default: ""
      - key: growth.analytics_source
        description: "Traffic and funnel numbers: ga4, plausible, posthog, matomo, other, none"
        default: "none"
---
# Binding Constraint Check

Use before a plan, feature, launch, hire or spend for this venture, when a plan drifts past
the constraint recorded in Scope, or when the constraint may have moved (a rule changed, a
dependency shipped, a first customer paid).

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| The recorded constraint (Scope or `venture.brief`) | the test needs a constraint to test against | Scope or the brief names one |
| Web access to primary sources, for a regulatory constraint | the rule's current text | the official page loads |
| Analytics read access, for a commercial constraint when `growth.analytics_source` is not `none` | the measured funnel step | a one-day report returns rows |

If a required prerequisite is missing, stop before step 1. Say which one, what it blocks, and
the smallest access that would unblock it. No recorded constraint: run `venture-scope-setup`
first. Never present a constraint you could not source as established.

## Configuration
- `venture.brief`: where the constraint and earlier decisions are read and where a moved
  constraint is proposed. Unset: rely on Scope and say there is no brief.
- `growth.analytics_source`: `none` means a commercial constraint is backed by what you can
  observe directly (orders, replies, sign-up records), labelled as such.
- Set values with `hermes config set skills.config.<key> <value>`.

## Procedure
1. State the current constraint in one sentence.
2. Establish it with evidence, not opinion:
   - regulatory or legal: the text of the rule or a named authority, with an as-of date. A
     summary or "X confirmed it" is second-hand: label it so;
   - commercial: the measured step where people stop, with source and date;
   - technical: the failing call, the missing integration, the log line.
3. Test the proposal: does it relax the constraint, work around it legitimately, or assume it
   away? A plan that assumes one person may do what a rule reserves for a licensed or
   incorporated entity is wrong before it starts. Say so plainly, even unasked.
4. Check what changed since the constraint was recorded; if it moved, propose the new
   wording with the evidence.
5. Rank: work that relaxes the constraint first; the rest waits. Name what is dropped.

## Output standard
```
Constraint: <one sentence> (source: <primary source or measurement, date>)
Proposal: <relaxes | works around | ignores> it, because <reason>.
Recommendation: <do | do after X | drop>. Dropping: <what this displaces>.
```

## Traps
- Designing around a regulatory constraint instead of meeting it.
- Treating a measured defect as the constraint without a before/after on its metric.
- Quoting a rule from memory. Rules change; cite the current text and its date.
- A "constraint" that is really a preference: record it as a decision instead.
