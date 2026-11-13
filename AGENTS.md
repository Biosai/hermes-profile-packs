# AGENTS.md

## Repository purpose

This repository contains public, portable Hermes Agent profile packs. Treat profile names, pack manifests, installer behavior, distribution layout, shared-skill sources, and Academy routing policy as user-facing API.

## Required invariants

- `agency-*` belongs only under `hermes-agency/profiles/`.
- `council-*` belongs only under `hermes-council/profiles/`.
- `academy-*` belongs only under `hermes-academy/profiles/`.
- `property-*` belongs only under `hermes-property/profiles/`. Its team-wide rules live once in the shared skill `shared-skills/panel-rules/`, which every property profile ships and preloads.
- A skill copied into several profiles has one canonical source under `shared-skills/<name>/`. Edit it there, then run `python scripts/sync_shared_skills.py`; `shared-skills/targets.json` lists every copy and the tests hold them byte-identical.
- A workflow of two or more profiles is defined once in `workflows/<name>.yaml`, coordinated by the pack's orchestrator, and rendered into that profile's `skills/workflows/<name>/` by `python scripts/sync_workflows.py`; never hand-edit the rendering. A workflow of one profile is a hand-written skill under `skills/workflows/`.
- A skill added beside the baseline has the upstream shape (Use when, Procedure, Decision rules, Quality gate, at most 650 words) plus Prerequisites and Configuration; `python scripts/check_skill_shape.py` enforces it. Put it in the profile whose role owns the job, and name the skill that owns a rule instead of restating it.
- Extend an existing Agency or Council profile by ADDING a skill directory. Never edit an upstream SOUL or skill in place: `capabilities/baseline.json` pins them, and in-place edits make upstream merges conflict.
- Content distilled from live profiles must be generalized: no names, accounts, handles, chat ids, domains, client numbers, dated anecdotes or live-system paths.
- Never copy a live Hermes profile directory wholesale into the repository.
- Never commit auth files, `.env`, state databases, caches, logs, session dumps, PIDs, local mount paths, or personal home paths.
- `distribution.yaml` names must match their directory names.
- Manifest `jobs` must match the profile-specific skill directories for Council profiles.
- Preserve unrelated work.

## Continuing Education invariants

Hermes Academy Continuing Education must not depend on a separate distributed runtime, scheduler, message bus, node-management service, or parallel persistence layer. Keep the education flow within the standard Hermes capabilities documented by this repository.

The canonical shared skills are:

- `hermes-academy/shared-skills/academy-continuing-education/SKILL.md`
- `hermes-academy/shared-skills/teach-profile/SKILL.md`

Edit those canonical sources rather than hand-editing materialized copies. Validators enforce byte identity across participating learner/faculty distributions.

Academy routing policy has two synchronized forms:

- `hermes-academy/academy.json` owns specialist preferences and category fallbacks;
- `academy-dean`'s preloaded `faculty-routing` skill owns the installed runtime contract.

`hermes-academy/routing.py` is a repository reference implementation and test oracle only. Never make an installed Dean depend on that pack-root file being present after profile installation.

Continuing Education routing must fail closed:

- prefer the most specific installed specialist;
- use a broad fallback only within the specialist's own category;
- cross-category CE objectives must be narrowed instead of being assigned to an unrelated broad chair;
- uninstalled or unverified faculty must not be reported as installed;
- ambiguous role-description ties must not be broken by roster or iteration order.

Public status language must state the Hermes capabilities required by Continuing Education and distinguish implemented pack behavior from compatibility with a given Hermes release. Do not claim unqualified production readiness until the normal Hermes release used with Profile Packs provides those capabilities.

## Editing profiles

Prefer extending an existing specialist with a focused skill when ownership already exists. Add a new profile only when it has a distinct, durable responsibility.

Council profiles should use minimum-necessary personal context and hand off to specialists rather than accumulating every personal domain into one persona.

Agency profiles imported from the standalone pack should remain compatible with that distribution unless a deliberate migration is being performed.

## Validation

Before committing or pushing:

```bash
python validate.py
python -m unittest discover -s tests -p 'test_*.py'
python -m unittest discover -s hermes-agency/tests -p 'test_*.py'
python -m unittest discover -s hermes-council/tests -p 'test_*.py'
python -m unittest discover -s hermes-academy/tests -p 'test_*.py'
python -m unittest discover -s hermes-property/tests -p 'test_*.py'
```

Do not weaken a validator merely to make a failing artifact pass. Determine whether the finding is a real portability/security problem or an overly broad rule, then fix the correct layer.

For Continuing Education changes, keep the public guide, architecture contract, Academy teaching contract, Academy README, root README, and changelog truthful about the same compatibility boundary.