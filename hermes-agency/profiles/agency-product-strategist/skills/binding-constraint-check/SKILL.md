---
name: binding-constraint-check
description: "Test a plan against the project's one binding constraint"
metadata:
  hermes:
    config:
      - key: project.brief
        description: "Path or URL of the brief: customer, voice, constraints, autonomy"
        default: ""
      - key: growth.analytics_source
        description: "Traffic and funnel numbers: ga4, plausible, posthog, matomo, other, none"
        default: "none"
---
# Binding Constraint Check

Use when a plan, feature, launch, hire or spend is proposed for the project, when a plan drifts past the constraint recorded in the project brief, or when that constraint may have moved: a rule changed, a dependency shipped, a first customer paid.

## Prerequisites
| Needs | Why | Check |
|---|---|---|
| The constraint recorded in the project brief (`project.brief`) | the test needs a constraint to test against | the brief names one |
| Web access to primary sources, for a regulatory constraint | the rule's current text | the official page loads |
| Analytics read access, for a commercial constraint, unless `growth.analytics_source` is `none` | the measured step where people stop | a one-day report returns rows |

If one is missing, stop before step 1 and say which, what it blocks, and the smallest access that would unblock it. With no recorded constraint, ask the owner for it and have it recorded in the brief first, through the chief of staff profile's `venture-scope-setup` when that profile is installed. Never present a constraint you could not source as established.

## Configuration
- `project.brief`: where the constraint and earlier decisions are read, and where a moved constraint is proposed. Unset: ask the owner where the brief is, and say that no constraint is on record.
- `growth.analytics_source`: where a commercial constraint is measured. `none`: it rests on what can be observed directly (orders, replies, sign-up records), labelled as such.
- Set values with `hermes config set skills.config.<key> <value>`.

## Procedure
1. State the current constraint in one sentence.
2. Establish it with evidence, not opinion:
   - regulatory or legal: the text of the rule or a named authority, with an as-of date;
   - commercial: the measured step where people stop, with its source and date;
   - technical: the failing call, the missing integration, the log line.
3. Test the proposal: does it relax the constraint, work around it legitimately, or assume it away? Say which plainly, even unasked.
4. Check what changed since the constraint was recorded. If it moved, propose the new wording with the evidence, for the owner to approve in the brief.
5. Rank: work that relaxes the constraint comes first, the rest waits. Name what is dropped.
6. Hand on what this check does not cover: the full case for a new opportunity belongs to `opportunity-assessment`, the order of several bets under the constraint to `portfolio-prioritization`.

## Decision rules
- A plan that assumes one person may do what a rule reserves for a licensed or incorporated entity is wrong before it starts.
- A regulatory constraint is met, never designed around.
- A summary, or "someone confirmed it", is second-hand: label it so. Never quote a rule from memory: rules change, so cite the current text and its date.
- A measured defect is not the constraint until a before and after on its metric shows it.
- A "constraint" that is really a preference is recorded as a decision instead.

## Quality gate
The check is done when the report states the constraint in one sentence with its primary source or measurement and its date, says whether the proposal relaxes, works around or ignores it and why, and recommends do, do after a named condition, or drop, with what the recommendation displaces.
