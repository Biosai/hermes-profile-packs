# Hermes Profile Pack Specification

## Namespaces

A pack owns a stable prefix. Every profile directory and `distribution.yaml` name must begin with that prefix.

- Hermes Agency: `agency-*`
- Hermes Council: `council-*`
- Hermes Academy: `academy-*`
- Hermes Property: `property-*`

Names use lowercase kebab-case and are treated as public API once released.

## Required profile files

Every profile must contain:

- `distribution.yaml` with `name`, `version`, `description`, `author`, and `license`.
- `SOUL.md` defining role, responsibilities, working standard, collaboration boundaries, communication, and completion criteria.
- At least one profile-specific `skills/<skill>/SKILL.md`.

A skill file begins with YAML frontmatter containing a matching `name` and useful `description`, followed by a concrete procedure or operating guidance.

## Portable versus runtime state

Profile packs contain source artifacts only. Never commit:

- tokens, passwords, cookies, API keys, OAuth credentials, or private keys
- `.env` or authentication files
- logs, caches, databases, process IDs, sockets, or session history
- absolute user-home paths or machine-specific mount paths
- generated Hermes runtime state

## Metadata and jobs

Pack manifests are the authoritative roster. A roster entry includes:

- stable profile `name`
- human-readable `display_name`
- category
- concise `role`
- `jobs`, which map to the profile's owned reusable skills

The manifest is designed for discovery and routing; `SOUL.md` remains the behavioral contract.

## Team recipes

`recipes.json` is the authoritative registry for portable team compositions.

A recipe is not a new runtime primitive. It references existing released profile identities and describes a useful formation for a common outcome.

Every recipe must contain:

- stable lowercase kebab-case `id`;
- `display_name`;
- one owning `pack`, a pack registered in `packs.json`;
- `description` and `when_to_use`;
- non-empty search `keywords`;
- `minimal`, `recommended`, and `expanded` tiers;
- a non-empty `workflow`;
- non-empty observable `success_criteria`;
- optional runtime routine suggestions;
- optional `workflows`: the names of the workflow definitions that make the recipe's `workflow` steps runnable (see below).

Tier rules:

- every profile reference must exist in the owning pack;
- no cross-pack profile references are allowed inside a single recipe;
- `minimal` must be a subset of `recommended`;
- `recommended` must be a subset of `expanded`;
- larger tiers should add distinct expertise, independent review, or useful parallelism rather than status or duplication.

Recipe installation must reuse the normal Profile Packs/Hermes distribution path. Recipes may suggest runtime routines, but must never create cron jobs, memory, sessions, groups, Kanban state, credentials, or other live state during installation.

## Skills added beside the upstream ones

A profile is extended by adding a skill folder, never by editing a baselined file. An added skill has the shape of the skills around it, so a reader cannot tell which came later:

- a title, one line starting "Use when", then `## Procedure`, `## Decision rules` and `## Quality gate`, in at most 650 words; detail goes to `references/` inside the skill folder;
- `## Prerequisites`, and `## Configuration` when it reads settings, come before the procedure. They are this repository's portability convention (`docs/PORTABLE_SKILLS.md`): what differs between teams is a setting from one shared registry, and missing access stops the skill cleanly;
- one skill per job and one home per rule: a skill names the skill that owns a rule instead of restating it, and lives in the profile whose role owns the job;
- no story from one team's past, no tool, vendor, chat platform or country assumed without a setting or a stated prerequisite.

`python scripts/check_skill_shape.py` enforces the shape and runs in `python validate.py`.

## Workflows

A skill is know-how; a workflow is an ordered process with a trigger (`docs/WORKFLOWS.md`).

- A workflow that involves two or more profiles is defined once in `workflows/<name>.yaml` and coordinated by the pack's orchestrator, the profile its manifest names in `orchestrator`. Its steps are held by the profiles that own each job in the matching recipe; the orchestrator routes, it does not do their work.
- A workflow of one profile, with or without a human decision, lives in that profile under `skills/workflows/<name>/`.
- A checking step says where the work goes back on failure, a human step may send it back with a change request, and the number of fix rounds is bounded. A verdict belongs to the head it was given on.
- Role-owned workflow folders are not supplemental payloads: they are outside `capabilities/skills.lock.json`.

## Separation of concerns

Profiles should own a bounded domain. When a request materially belongs elsewhere, complete the part owned by the current profile and hand off the rest with sufficient context.

Council profiles have an additional privacy rule: only the minimum personal context needed for the task should cross profile boundaries.

Academy profiles have an additional teaching rule: adapt instruction to the learner's goal and level, teach reasoning and transferable skill rather than merely dumping answers, distinguish education from professional execution or advice, and verify current standards or facts when material.

## Supplemental capabilities

Role-owned jobs remain the top-level `skills/<job>/SKILL.md` API. Additional
reviewed capabilities may use native category directories. `capabilities/profiles.json`
owns their exact per-profile selection; `capabilities/skills.lock.json` pins the
complete source/support trees and installation paths. `capabilities.py --check`
must pass before release; materialization is an offline source-packaging operation,
not a runtime installer. Never activate plugins, MCPs, accounts, downloads or jobs
from a normal pack install. See `docs/CAPABILITIES.md`.

## Versioning

Profile and pack versions use semantic versioning.

- Patch: wording, examples, or compatible skill improvements.
- Minor: new profiles, skills, recipes, or backward-compatible metadata.
- Major: renamed/removed profiles or recipes, incompatible distribution behavior, or semantic contract changes.
