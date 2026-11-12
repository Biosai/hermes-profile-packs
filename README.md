# Hermes Profile Packs

Curated profile packs for [Hermes Agent](https://github.com/NousResearch/hermes-agent).

This repository is the public upstream home for reusable Hermes profile distributions maintained as coherent teams rather than isolated prompts.

## Packs

| Pack | Namespace | Purpose |
| --- | --- | --- |
| **Hermes Agency** | `agency-*` | Professional specialists for engineering, product, design, QA, operations, marketing, content, and coordinated project work. |
| **Hermes Council** | `council-*` | Personal specialists for growth, health, fitness, parenting, relationships, communication, community, faith, finances, home stewardship, personal admin, career, learning, recreation, travel, nutrition, sleep, and preparedness. |
| **Hermes Academy** | `academy-*` | Professors and instructors for academic, technical, vocational, and professional learning. |
| **Hermes Property** | `property-*` | An expert panel for a property investor in Belgium and France: deal strategy, works costing, tax, deeds, leases and planning. Each expert prepares the real professional's work; none replaces it. |

### What this fork adds

This fork adds what three teams of Hermes profiles running in production learned, generalized for public use: names, accounts, numbers and history removed, and the rules each team learned the hard way kept. It adapts upstream profiles where one already owns the work and adds new profiles only where none does:

- **Hermes Property** (`property-*`), a new pack: no upstream profile covers property investment under Belgian and French law. Its team-wide rules live once in `hermes-property/shared/RULES.md`; `sync_shared.py` copies them into every SOUL and the pack validator holds them byte-identical.
- **Adapted Agency and Council profiles**: new role-owned skills added beside the upstream ones (see [Adaptations](#adaptations-in-this-fork)). Upstream SOUL and skill files are never edited in place, so `capabilities/baseline.json` still holds and upstream changes merge cleanly.
- **Two new Agency profiles** for work no upstream profile owned: `agency-venture-operator` and `agency-onchain-engineer`.
- **Workflows**, kept apart from skills: seven multi-profile workflows defined in `workflows/` (such as `issue-to-merge`, `after-merge`, `infra-change`, `property-deal-review`) and twelve single-profile ones. See [`docs/WORKFLOWS.md`](docs/WORKFLOWS.md).
- **Team Recipes** that assemble them and list the workflows each team can run: `gated-repo-delivery`, `solo-founder-portfolio` and `property-deal-review`.

The packs deliberately separate durable context domains. Agency executes professional work, Council supports the person, and Academy teaches. A work profile should not need private life context, a personal profile should not inherit repository state merely because both run on Hermes, and a teaching profile should not silently become a production executor.

<!-- profile-counts:start -->
Hermes Agency contains 115 professional specialists. Hermes Council contains 22 focused profiles and 90 purpose-built personal-life skills. Hermes Academy contains 30 faculty profiles and 120 purpose-built teaching skills.
Hermes Property contains 8 profiles and 38 role-owned skills.
<!-- profile-counts:end -->

### Academy Continuing Education

Hermes Academy Continuing Education lets a profile learn a reusable capability from an installed instructor. A request such as `Go learn API security` routes through the Academy Dean, creates a learning goal, supports study and demonstrated transfer through Bot Chat, and saves the capability to the learner's skill store through `/learn`. It requires no separate training or distributed runtime.

The flow requires a Hermes build that supports `goal_manage`, profile-distribution `preload_skills`, bounded goal-judge feedback, and the associated Bot Chat behavior. Confirm those capabilities in your Hermes release before using Continuing Education; compatibility with the standard Hermes release is not yet guaranteed.

See the [`Continuing Education guide`](docs/CONTINUING_EDUCATION.md) and [`architecture contract`](docs/CONTINUING_EDUCATION_ARCHITECTURE.md).

## Adaptations in this fork

Where an upstream profile already owned the work, this fork adds role-owned skills beside its existing ones instead of creating a near-duplicate profile. Every added skill follows [`docs/PORTABLE_SKILLS.md`](docs/PORTABLE_SKILLS.md): settings such as the code host, repository layout, issue tracker, board, merge and apply policy are declared under `metadata.hermes.config` (set them with `hermes config set skills.config.<key> <value>`, or let `hermes config migrate` prompt for them), credentials under `required_environment_variables`, and each skill names its prerequisites and stops cleanly when one is missing.

| Profile | Added skills | Added workflows |
| --- | --- | --- |
| `agency-backend-engineer` | `go-backend-craft`, `issue-clarification`, `merge-followups`, `gated-delivery` | |
| `agency-qa-tester` | `real-run-verification`, `test-design-maxims`, `gated-delivery` | `mutation-proof` |
| `agency-product-manager` | `issue-authoring-standard`, `ready-to-merge-gate`, `gated-delivery` | `issue-to-merge`, `after-merge`, `ready-queue`, `product-direction-review`, `open-pr-readiness-sweep` |
| `agency-software-architect` | `fresh-main-evidence`, `readiness-review`, `gated-delivery` | |
| `agency-infrastructure-engineer` | `iac-change-safety`, `infra-security-review`, `gated-delivery` | `infra-change` |
| `agency-compliance-reviewer` | `regulated-engineering-controls`, `vendor-integration-review`, `migration-verification`, `gated-delivery` | |
| `agency-knowledge-manager` | `post-merge-kb-update`, `glossary-discipline`, `gated-delivery` | |
| `agency-orchestrator` | `gated-delivery` | `coordination-board` |
| `agency-chief-of-staff` | `owner-question-protocol` | `owner-action-handoff` |
| `agency-growth-marketer` | `revenue-state-audit`, `value-proposition-diagnosis` | `conversion-drop-diagnosis` |
| `agency-social-media-manager` | `approval-gated-publishing` | `publish-with-approval` |
| `agency-email-marketer` | `approval-gated-publishing` | `email-send-with-approval`, `one-to-one-email-send` |
| `agency-finance-ops`, `council-finance-coach` | `double-entry-books` | |
| `council-fitness-coach` | `endurance-race-plan` | `gear-shopping-list` |

New profiles, only where no upstream profile owned the work:

| Profile | Role |
| --- | --- |
| `agency-venture-operator` | Works one venture only, from its brief and binding constraint. Install one copy per venture. Workflows `repo-audit-to-issues`, `remaining-work-to-issues` and `bounded-task-delivery`. |
| `agency-onchain-engineer` | One token or protocol project, testnet first. Coordinates the `contract-change` workflow (independent code and security review, testnet, owner-approved mainnet). |
| `property-*` (8 profiles) | Expert panel for a property investor in Belgium and France. The coordinator runs the `property-deal-review` workflow. See [`hermes-property/README.md`](hermes-property/README.md). |

**Skills and workflows are separate.** A skill is know-how a role brings to any task; a workflow is an ordered process with a trigger, where each step names who acts, with which skills, and where a human decides. Workflows live in each profile's `skills/workflows/` (the Hermes `workflows` category). A workflow that hands work between profiles is defined once in `workflows/<name>.yaml` and rendered into its coordinating profile by `python scripts/sync_workflows.py`; on a Hermes Kanban board it runs as one card per step. See [`docs/WORKFLOWS.md`](docs/WORKFLOWS.md).

`gated-delivery`, `approval-gated-publishing` and `double-entry-books` ship in several profiles. Each has one canonical source in `shared-skills/`; edit it there and run `python scripts/sync_shared_skills.py`.

## Role-specific capability upgrade

Every profile, including standalone Wear, now has an on-demand capability guide. The release includes 24 reviewed skill trees with full supporting files, six role-selected plugin opt-ins, and 13 disabled MCP integration templates. Existing role-owned jobs, tool restrictions, bundled-skill opt-outs and user-controlled activation remain intact.

See the [complete profile matrix](docs/CAPABILITY_MATRIX.md), [capability guide and privacy/setup rules](docs/CAPABILITIES.md), and [verified results and limitations](docs/CAPABILITY_VALIDATION.md). Normal profile installation never downloads/enables plugins, authenticates accounts or starts remote integrations.

## Start small with Team Recipes

You rarely need all 175 profiles. Team Recipes are validated compositions of existing profiles for common outcomes, with `minimal`, `recommended`, and `expanded` tiers.

The main installer understands them directly:

```bash
python install.py --list-recipes
python install.py --recommend "build and ship a web app"
python install.py --recipe software-delivery --tier minimal --dry-run
python install.py --recipe software-delivery --tier recommended --yes
```

Recommendation is confidence-aware. A recipe is promoted only when one formation is a strong, unambiguous fit; otherwise the installer falls back to individual profile matches instead of forcing a template.

Recipes are portable selection guidance only. They do not create memory, cron jobs, Bot groups, Kanban state, credentials, or other runtime state. Installation still uses the normal Profile Packs/Hermes distribution path.

See [`docs/TEAM_RECIPES.md`](docs/TEAM_RECIPES.md) and [`docs/FIRST_TEAM.md`](docs/FIRST_TEAM.md).

## Repository layout

```text
hermes-profile-packs/
├── hermes-agency/
├── hermes-council/
├── hermes-academy/
├── hermes-property/
├── shared-skills/          # canonical copies of skills shipped by several profiles
├── workflows/              # multi-profile workflow definitions (docs/WORKFLOWS.md)
├── docs/
│   ├── CONTINUING_EDUCATION.md
│   └── CONTINUING_EDUCATION_ARCHITECTURE.md
├── examples/
├── tests/
├── scripts/
│   └── update_readme_counts.py # Regenerates README profile and skill counts
├── packs.json
├── recipes.json
├── recipe_catalog.py       # Shared recipe loading/scoring/confidence engine
├── install.py              # Canonical human + agent profile/recipe selector
├── recipes.py              # Focused recipe-only convenience client
└── validate.py
```

Runtime state is never distributed. Authentication material, `.env` files, logs, caches, databases, local paths, session history, and machine-specific configuration do not belong in this repository.

## Install

For most people, launch the selector:

```bash
python install.py
```

The wizard can recommend a validated Team Recipe when a goal maps cleanly to one, browse recipes directly, browse packs/categories, search exact profiles, preview the exact install plan, and still offer an explicit install-everything path.

For agents and scripts:

```bash
python install.py --agent-help --json
python install.py --catalog --json
python install.py --list-recipes --json
python install.py --recommend "build a web app" --json
python install.py --recipe software-delivery --tier minimal --dry-run --json
python install.py --recipe software-delivery --tier recommended --yes --json
python install.py --profiles agency-backend-engineer agency-frontend-engineer --dry-run --json
python install.py --all --yes --json
```

`--catalog`, `--list-recipes`, and `--recommend` are read-only. Existing `--recommend --json` consumers keep the individual-profile `recommendations` array; recipe results are additive through `recipe_match` and `recipe_recommendations`.

Legacy pack-first commands remain supported.

See [`docs/INSTALLER.md`](docs/INSTALLER.md) for the full contract.

## Focused recipe client

`recipes.py` remains supported when a recipe-only surface is convenient:

```bash
python recipes.py --list
python recipes.py --recommend "learn cybersecurity"
python recipes.py cybersecurity-learning --tier recommended --dry-run
```

Both entry points use the same shared recipe engine.

## Operate the team

Use [`docs/OPERATING_PLAYBOOK.md`](docs/OPERATING_PLAYBOOK.md), [`docs/INSTALLATION_VERIFICATION.md`](docs/INSTALLATION_VERIFICATION.md), and [`docs/TROUBLESHOOTING.md`](docs/TROUBLESHOOTING.md).

## Profile quality

Council supports listening, reflection, decisions, action and requested plans without requiring a file or task for every conversation. Academy human teaching includes domain-specific diagnostics, misconceptions, hints and transfer practice; direct answers remain available.

See [`docs/PROFILE_QUALITY.md`](docs/PROFILE_QUALITY.md), the source-to-catalog [`mapping`](docs/CATALOG_MAPPING.md), and the [`acceptance record`](docs/QUALITY_ACCEPTANCE.md) for verified behavior and compatibility limits.

## Validate

```bash
python validate.py
python scripts/update_readme_counts.py --check
python scripts/sync_shared_skills.py --check
python scripts/sync_workflows.py --check
python -m unittest discover -s tests -p 'test_*.py'
```

`validate.py` also checks that the generated README profile and skill counts match the pack manifests. After adding or removing a profile or skill, run `python scripts/update_readme_counts.py` to refresh the README. GitHub README files cannot run inline JavaScript, so the committed Markdown is generated and CI-enforced instead.

The validation suite checks pack manifests, namespaces, distribution metadata, skills, portability, secret/path hygiene, team recipe references/tier invariants, generated documentation counts, and root selector behavior.

## Design principles

1. **Coherent teams, not prompt dumps.** Profiles have explicit ownership and clean handoffs.
2. **Namespace isolation.** `agency-*` is professional, `council-*` is personal, `academy-*` is educational, and `property-*` serves a property investor.
3. **Portable distributions only.** No runtime state, secrets, personal filesystem paths, or local caches.
4. **Specialists remain specialists.** Profiles hand off rather than silently absorbing unrelated domains.
5. **Smallest useful team.** Add profiles only for distinct expertise, independent review, or useful parallelism.
6. **Conservative recommendation.** A recipe is promoted only when the deterministic match is strong and unambiguous.
7. **Human agency stays central.** Council supports decisions and capability; it does not run a person's life.
8. **Safety beats role-play.** Profiles do not manufacture authority they do not possess.
9. **Academy teaches for transfer.** Teaching should make the learner progressively more capable.

See [`PACK_SPEC.md`](PACK_SPEC.md), [`CONTRIBUTING.md`](CONTRIBUTING.md), and [`SECURITY.md`](SECURITY.md).

## License

AGPL-3.0-only. See [`LICENSE`](LICENSE).
## Standalone smartwatch distribution

[Hermes Wear](hermes-wear/README.md) provides a portable wrist assistant profile through native Hermes installation, separately from the three team catalogs.
