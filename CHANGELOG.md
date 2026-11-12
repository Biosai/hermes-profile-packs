# Changelog

All notable changes to Hermes Profile Packs will be documented here.

## Unreleased

### Added (fork)

- Distilled three Hermes teams running in production into public, generalized content, adapting upstream profiles wherever one already owned the work:
  - **Hermes Property** (`property-*`), a new pack: an expert panel for a property investor in Belgium and France, with a canonical `shared/RULES.md` that `sync_shared.py` copies into every SOUL. Written in English; profiles reply in the investor's language.
  - New role-owned skills on existing Agency and Council profiles (Go backend craft, real test runs with counts, ready-to-merge gate, IaC with human apply, approval-gated publishing, double-entry books, endurance race plans, and more), added beside the upstream skills without editing any baselined file.
  - Two new Agency profiles: `agency-venture-operator` and `agency-onchain-engineer`.
  - Recipes `gated-repo-delivery`, `solo-founder-portfolio` and `property-deal-review`.
- Workflows are separate from skills (`docs/WORKFLOWS.md`): seven multi-profile workflows are defined in `workflows/*.yaml` and rendered into their coordinating profile by `scripts/sync_workflows.py`, which checks every step's profile and skills, dependencies, human deciders and settings; twelve single-profile workflows live under `skills/workflows/` (among them `open-pr-readiness-sweep`, `conversion-drop-diagnosis`, `mutation-proof`, `product-direction-review`, `one-to-one-email-send`). On a Hermes Kanban board a workflow runs as one card per step. Recipes list the workflows their team can run.
- A team with fewer profiles than a workflow has roles renders its own copy with a role assignment (`python scripts/sync_workflows.py --render <name> --solo`, or `--assign ROLE=WHO` per role). When one profile holds every role, the rendering says that no second profile checks the work and forbids reporting a step as independently reviewed. New registry setting `delivery.handoff` (`profile-turn`, `channel`, `owner-relay`) says how a step reaches another profile when no board runs the workflow, replacing the vague "the host's delegation".
- Skills shipped by several profiles have one canonical source in `shared-skills/`; `scripts/sync_shared_skills.py` writes the copies and validation holds them byte-identical.
- Deepened the fork's skills with the lessons of the private originals they replace in a running agent (claims, filing discipline, PR sweeps, funnel diagnosis, approval-gated sends, bookkeeping, endurance coaching), generalized and scrubbed. New registry setting `publishing.mailbox`.
- The root installer and README count generator now read packs from `packs.json` instead of a fixed list of three; a pack may declare its own `display_name` and recommendation `hints` there.

### Profile quality

- Clarified Council interaction modes so listening and direct answers can complete a conversation without mandatory files, actions or ending questions. Corrected assumed user biography, stale collaborator references and malformed SOUL Markdown.
- Made Council handoffs and optional continuity conditional on available, authorized native capabilities and minimum necessary personal context.
- Added domain-specific Academy human teaching kits, with diagnostics, differentiated misconceptions, worked reasoning, graduated hints and changed transfer tasks linked from existing skills. Preserved the separate Continuing Education contract.
- Added profile/skill review coverage, synthetic behavioral cases, a source-to-catalog mapping and explicit acceptance records. Live verification status is documented separately from source content changes.

### Added

- Completed coordinated capability selection across all 166 public distributions: 24 pinned skill trees across 241 targeted assignments, an on-demand guide for every profile, six optional plugin declarations and 13 disabled MCP templates. Included full skill support trees, provenance, licenses, egress/setup disclosures, native seeding compatibility and offline materialization checks; preserved original role-owned source and restrictions.
- Added complete machine-readable/readable matrices, a source preservation baseline, native install/seeding/discovery/update proof, least-privilege MCP allowlists, explicit credential/upload/billing gates and documented unsupported-candidate exclusions. Ordinary profile installation activates no external integration.

- Added Hermes Wear device-awareness protocol, three on-demand device interpretation skills, and synthetic contract fixtures. Live watch/device tool integration remains separate and is not claimed complete.

- Expanded standalone `hermes-wear` to v1.1.0 with ten wrist-specific skills, voice transcript repair, quick capture, time/reminder safeguards, integration-backed confirmation, background run/reconnect recovery, private memory rules, watch safety, and explicit skills/read-only web toolsets while preserving the restricted execution boundary.
- Added `council-vehicle-steward` with four original, evidence-first skills for vehicle records, manual-linked maintenance, repair/recall questions, and ownership planning, preserving source uncertainty, privacy, and user approval for consequential actions.
- Added `agency-hermes-config-manager`, a conversational control-point specialist for safely inventorying, selecting, previewing, applying, verifying, and rolling back Hermes configuration across individual profiles or approved groups. It supports model/provider assignment and secure Hermes credential setup while requiring exact target approval, supported CLI interfaces, secret-safe handling, per-profile readback, active-profile protection, and explicit runtime-operator handoffs. Its procedures are original to this repository and grounded in verified Hermes CLI behavior.
- Added `agency-reverse-engineer`, an engineering specialist for authorized software-artifact triage, static and contained dynamic analysis, and protocol or format reconstruction. The profile produces evidence-backed reports, specifications, and reproducible validation artifacts while preserving explicit authorization, containment, non-exploitation, and adjacent security/implementation boundaries. Its procedures are original to this repository and do not vendor third-party material.
- Added `agency-botfather`, a portable profile-pack authoring specialist that sharpens approved role contracts, authors focused SOUL and skill artifacts, updates routing/roster documentation, preserves pinned third-party provenance, and validates distributions before independent review. Its `profile-pack-authoring` procedure adapts selected MIT-licensed methods from `techjanitor/botmaker` revision `93eb3b6d3976b115a372598fa5c02c4f6ab63ed2` while excluding live-profile mutation, runtime state, model/provider pins, safeguard overrides, and recursive profile factories.
- Added Hermes Academy Continuing Education with canonical learner and instructor skills, Dean routing, native Bot Chat and `message_agent` teaching, native goal and `/learn` integration, minimum-sufficient instruction, transfer assessment, and learner-skill preservation. Participating Agency profiles preload `academy-continuing-education`; faculty preload `teach-profile`; and the Dean preloads `faculty-routing`.
- Hardened Dean routing with manifest-owned category fallbacks, same-category interdisciplinary fallback only, fail-closed cross-category behavior, installed-profile-aware selection, exact-word and tie-safe role fallback, and a self-contained installed routing contract. Academy validation keeps manifest and Dean routing policy synchronized.
- Documented the required Hermes capabilities and the current standard-release compatibility limitation for Continuing Education.
- Added `docs/CONTINUING_EDUCATION.md` as the current behavior/status guide and updated the normative architecture contract with the selected transport and learner-skill preservation invariant.
- Integrated Team Recipes into the canonical root `install.py` wizard and agent/script interface, including direct recipe browsing, `--list-recipes`, `--recipe`, and `--tier` selection.
- Added confidence-aware recipe promotion: a recipe must clear both a minimum score and a minimum lead over alternatives before the installer presents it as a clear match; ambiguous goals fall back to individual profiles.
- Added additive `recipe_match` and `recipe_recommendations` fields to `--recommend --json` while preserving the existing individual-profile `recommendations` contract.
- Added shared `recipe_catalog.py` so `install.py` and the focused `recipes.py` client use one recipe registry/scoring/confidence implementation.
- Added exact root-installer recipe dry-run coverage and compatibility tests.
- Added a validated `recipes.json` team-composition layer with minimal, recommended, and expanded tiers across Agency, Council, and Academy.
- Added `recipes.py` for deterministic recipe discovery, recommendation, dry-run planning, JSON output, and explicit `--yes` installation through the existing profile installer.
- Added first-team onboarding, team operating guidance, post-install verification, troubleshooting, and sanitized worked examples.
- Added `coordination-pattern-selection` to Agency Orchestrator and strengthened its SOUL to prefer the smallest capable team instead of delegation-by-default.
- Added recipe schema validation and root recipe tests for tier monotonicity, profile resolution, recommendation behavior, and JSON dry-run plans.
- Documented the source/runtime boundary for recipes and optional routines.
- Added an interactive root installer wizard that recommends a small profile set from plain-language goals, supports pack/category browsing and direct search, previews the exact install plan, and still offers an explicit install-everything path.
- Added a deterministic agent/script interface with JSON catalog and recommendation output, exact profile/category selection, pack filtering, dry-run planning, and non-interactive `--yes` installation.
- Added profile-selection payload estimates so sparse installs show how much of the catalog they avoid installing.
- Added root installer tests and CI coverage while preserving the existing pack-first installer commands.

## 0.4.0 - 2026-08-22

### Added

- Expanded **Hermes Academy** from 15 to 30 faculty profiles and from 60 to 120 purpose-built teaching skills.
- Added dedicated faculty for physics, chemistry, biology, statistics, data science, philosophy, law and legal studies, theology and religious studies, education and pedagogy, cybersecurity, cloud and systems, project management, automotive, culinary arts, and music.
- Added explicit specialist routing so clearly specialized requests prefer the dedicated faculty member while preserving `academy-natural-sciences-professor` as the interdisciplinary natural-sciences chair.
- Added Academy v0.2 tests that enforce the 30-profile / 120-skill release target, second-wave faculty presence, broad-chair preservation, and valid specialist routing.

## 0.3.0 - 2026-08-22

### Added

- Added **Hermes Academy**, a new `academy-*` profile pack for academic, technical, vocational, and professional teaching.
- Added an initial 15-profile faculty led by `academy-dean`, with 60 purpose-built teaching skills.
- Added professors for mathematics, writing and rhetoric, natural sciences, computer science, engineering, history, social sciences, economics, business, research methods, and health sciences.
- Added instructors for languages, skilled trades, and arts/design.
- Added the Academy teaching contract, installer, validator, tests, documentation, root routing, and CI coverage.

## 0.2.0 - 2026-08-22

### Added

- Expanded Hermes Council from 11 to 21 profiles and from 44 to 84 purpose-built skills.
- Added `council-health-navigator` for healthcare preparation, neutral health logging, preventive-care organization, and follow-up.
- Added `council-resilience-coach` for non-clinical stress regulation, recovery, and healthy coping.
- Added `council-time-attention-coach` for realistic planning, focus, attention management, and calendar boundaries.
- Added `council-career-coach` for career direction, opportunity evaluation, job-search strategy, and work boundaries.
- Added `council-personal-admin-steward` for documents, forms, renewals, appointments, accounts, and subscriptions.
- Added `council-preparedness-steward` for household emergency planning, go-bags, contact plans, and contingencies.
- Added `council-recreation-guide` for hobbies, restorative leisure, play, outings, and low-pressure novelty.
- Added `council-travel-planner` for current, practical trip planning, itineraries, packing, and budgets.
- Added `council-communication-coach` for assertiveness, listening, repair, conversation rehearsal, and message clarity.
- Added `council-community-coach` for friendship, belonging, support networks, and community participation.
- Expanded Council documentation with clearer safety, authority, and specialist-boundary guidance.

## 0.1.0 - 2026-08-22

### Added

- Initial public monorepo structure for reusable Hermes profile packs.
- Imported Hermes Agency with 109 professional profiles from the existing standalone profile-pack repository.
- Added Hermes Council with 11 personal-life profiles and 44 purpose-built skills.
- Added `council-steward` as the Council coordinator and minimum-context routing owner.
- Preserved the authored `council-life-coach` and `council-fitness-coach` SOUL definitions while converting them into portable profile distributions.
- Added repository-wide installation, validation, portability checks, CI, contribution guidance, security policy, and pack specification.