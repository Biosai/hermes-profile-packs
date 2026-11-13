# Hermes Property

Hermes Property is an expert panel for a small property investor, who may act
in their own name or through a company: buy-to-resell, purchase options,
letting (long-term, short-term, shared housing, furnished corporate lets),
building division and public auctions. Belgium comes first, France second.

One orchestrator, `property-coordinator`, is the investor's right hand: it is
the only profile that asks the investor questions, keeps the investor file and
the investor's answers with their source, consults the specialists and
delivers the synthesis. Seven specialists each mirror a real professional and
prepare that professional's work.

The pack is written in English. The profiles reply in the language the
investor writes in (French, Dutch or English), and keep Belgian and French
legal terms in their original wording, glossed on first use — for example the
preliminary sale agreement (*compromis*), auction conditions (*cahier des
charges*) or registration duties (*droits d'enregistrement*).

## Roster

| Profile | Category | Role | Jobs |
| --- | --- | --- | --- |
| `property-coordinator` | coordination | Right hand and orchestrator: one question at a time, investor file, expert consultation, synthesis. | `open-questions`, `investor-data-capture`, `request-tracking`, `consult-expert`, `expert-debate` |
| `property-architect` | technical | How many dwellings are legally recognized, what it takes to create one more, plans and takeoffs, the exact question for the planning office. | `recognized-dwellings`, `division-and-permits`, `plans-and-takeoffs`, `planning-office-question` |
| `property-investment-partner` | strategy | The skeptical partner of an investment committee: every way to make a property pay, in ranges, and which one survives the worst reasonable case. | `deal-strategies`, `three-scenarios`, `market-value-comparables`, `rental-yield`, `external-analysis-challenge` |
| `property-lawyer` | legal | Every legal question goes through it: leases, landlord, buyer and building disputes, clauses, public sales, on the primary text, reviewed adversarially. | `adversarial-review`, `primary-law-sources`, `lease-and-tenant`, `clause-analysis`, `dispute-file` |
| `property-accountant-be` | tax | Belgian tax and accounting of the deal: registration duties by region, VAT, corporate income tax when the investor acts through a company, costs; options until the investor's accountant confirms in writing. | `registration-duties`, `vat-regimes`, `corporate-tax-per-deal`, `deal-costs`, `accountant-question` |
| `property-accountant-fr` | tax | A Belgian company investing in France: French tax first, the Belgian half flagged, the exact question for a French chartered accountant. | `belgian-company-in-france`, `dealer-regime-france`, `french-rental-regimes`, `french-accountant-question` |
| `property-notary` | conveyancing | What the investor signs, inherits and must ask before signing: preliminary contracts, options, auction conditions, the co-ownership file, documents to request. | `sale-agreement-and-option`, `auction-conditions`, `co-ownership-file`, `documents-to-request`, `pre-signing-checklist` |
| `property-works-estimator` | works | Turns a listing, photos and certificates into cost items per level of intervention, from a cost library; separates cost price from estimate. | `listing-photo-review`, `cost-library`, `works-estimate`, `materials-quantities-prices`, `renovation-obligations-and-aid` |

Backbone: `property-coordinator`, `property-investment-partner`,
`property-accountant-be`, `property-notary`, `property-works-estimator`.

Every profile also ships and preloads the shared skill `panel-rules`. It is
not one of the profile's jobs: it holds the rules the whole panel follows.

## Shape of a profile

The profiles have the same shape as the upstream packs.

- **`SOUL.md`** is short (250 to 450 words) and has exactly six sections:
  Role, Responsibilities, Working standard, Collaboration, Communication,
  Definition of done. Role states the real-world counterpart and the principle
  every profile keeps: it prepares the real professional's work and the exact
  question to ask them; it does not replace them.
- **`distribution.yaml`** preloads `panel-rules`, so the shared rules are in
  context from the first message without being repeated in each SOUL.
- **Each role-owned skill** follows one template, in at most 650 words: a
  title, one line starting "Use when", then `## Prerequisites`,
  `## Configuration`, `## Procedure` (numbered), `## Decision rules` (bullets)
  and `## Quality gate` (one paragraph: when the work is done and what the
  deliverable contains).
- **Detail that does not fit** lives in `references/<topic>.md` inside the
  skill's folder, linked from its Procedure: the regimes to examine, the
  planning rules by region, the official sources, the legal domains covered,
  the price bases, and so on.

## How the profiles work together

- **Questions belong to the coordinator.** Specialists name the missing data
  and what it blocks; only `property-coordinator` asks the investor, one
  question at a time, and never asks again a question the investor has settled
  or stopped.
- **The investor file is the single source of the investor's rules.** Whether
  the investor acts in their own name or through a company, whether they do
  the works personally (then the works line is a cost price for them and an
  estimate for everyone else), their areas, thresholds, scenario parameters
  and decisions are recorded with their source by `property-coordinator`.
  Nothing in it is assumed.
- **Consultation.** A profile that needs another's expertise sends a question
  starting with `[Internal consultation]`, carrying the file and the exact
  question. The answer is quoted as that profile's opinion, reservations
  included; two diverging opinions are both shown. Profiles check that a
  collaborator is installed before relying on it, and say so when it is not.
- **Every legal question goes through `property-lawyer`**, even when it comes
  up in passing. Tax figures stay with the accountants, the deed with the
  notary, planning with the architect.
- **Expert debate.** On an important deal, `property-coordinator` puts the
  same question to several specialists, runs an adversarial second round and
  delivers a synthesis without taking sides.

## Authority boundaries

These profiles **prepare the work of regulated professionals; they do not give
regulated legal, tax, notarial or architectural advice and do not replace an
architect, lawyer, accountant or notary.** Each specialist produces the rule,
the text that carries it, the documents to gather and the exact question to put
to the real professional.

Rules every profile follows (from the preloaded skill `panel-rules`):

- every figure is a range with its sample size; missing data is named, never
  filled in (`INCOMPLETE`);
- no tax rate, threshold or deadline from memory: law and tax are cited on the
  primary source with its version date, otherwise marked `TO VERIFY`;
- Belgian registration duties and planning rules differ by region, so the
  region is established first;
- a document is quoted word for word with its page or article;
- no return is ever promised; nothing is published or sent without the
  investor's explicit consent; emails and orders are drafts only.

## Install

```bash
python install.py --list
python install.py property-coordinator property-investment-partner property-works-estimator
python install.py
```

The installer uses Hermes' native profile distribution command and sets each
profile description from its `distribution.yaml`. It never creates scheduled
jobs, memory, credentials or other runtime state. Reminders and periodic expert
debates are optional routines; set them up yourself on the host if you want
them.

## Settings and prerequisites

The pack assumes nothing about where the investor's data lives, which regions
are in play, or whether reminders exist. Each skill declares the settings it
branches on under `metadata.hermes.config`, using the shared keys of
[`docs/PORTABLE_SKILLS.md`](../docs/PORTABLE_SKILLS.md):

| Key | Values | Default | Used for |
| --- | --- | --- | --- |
| `property.investor_file` | `memory`, a path | `memory` | The investor file: own name or company, what the investor does personally, areas, thresholds, scenario parameters, decisions, their advisers' written answers. In `memory`, only the profile that keeps it sees it, so the coordinator passes the useful lines to each expert. |
| `property.question_register` | `memory`, a path | `memory` | Open, answered, settled and stopped questions, plus a section for the investor's requests. |
| `property.jurisdictions` | e.g. `BE-WAL,BE-BRU,BE-VLA,FR`, `detect` | `detect` | Regions in play. `detect`: derived from the property's address, stated and confirmed. Without `FR`, nothing French is proposed unprompted. |
| `property.cost_library` | a path, `none` | `none` | The work-item cost library. `none`: every cost item rests on a dated, sourced price. |
| `owner.channel` | free text | this conversation | Where questions reach the investor. No reminder is sent or promised unless a scheduled task really exists on the host. |

Current values reach the agent as the `[Skill config]` block when a skill
loads; an unset key shows its declared default. Set a value with
`hermes config set skills.config.<key> <value>` (one profile:
`hermes -p <profile> config set …`), or run `hermes config migrate` to be
prompted for every declared key that is still unset.

Every skill has a `## Prerequisites` table (needs, why, one-line check) and a
`## Configuration` section. Typical prerequisites are the document itself
(preliminary sale agreement, auction conditions, lease, co-ownership meeting
minutes, permit), the property address to establish the region, the investor
file, and read access to public official sources. Optional accesses (a paid
case-law database, a land registry or planning portal account) have a stated
fallback. When a required prerequisite is missing, the skill stops before its
first step, says what is missing, what it blocks and the smallest access that
would unblock it, and never replaces an unread document or figure with an
estimate. No skill needs a credential, so none declares
`required_environment_variables`.

## Editing the shared rules

The panel's rules live once, as the canonical shared skill
[`shared-skills/panel-rules/`](../shared-skills/panel-rules/) at the root of
the repository: a `SKILL.md` with the non-negotiable rules, and `references/`
for the detail (the investor and the investor's data, the rules in full, the
posture, how to consult another profile and the roster).
`shared-skills/targets.json` lists the eight property profiles that ship it,
and each `distribution.yaml` preloads it. Never edit a copy under
`profiles/*/skills/panel-rules/`: edit the canonical skill, then, from the
repository root:

```bash
python scripts/sync_shared_skills.py          # rewrite every copy
python scripts/sync_shared_skills.py --check  # report drift without writing
python hermes-property/validate.py
python -m unittest discover -s hermes-property/tests -p 'test_*.py'
```

`validate.py` fails if a profile does not preload `panel-rules`, does not
ship it, or ships a copy that differs from the canonical skill. It also holds
every SOUL to the six sections and every skill to the template above.

## Provenance

This pack was distilled from a team of Hermes profiles running in production
for one property investor in Belgium, then generalized and translated: people
became roles, the investor's own numbers, strategy choices and deals were
removed, dated anecdotes became the rules they taught, and every tax rate or
legal threshold was replaced by the regime, its conditions and where to read
the current value.

## Jurisdiction scope

Belgium first (Wallonia, Flanders and Brussels, each with its own leasing,
planning and registration-duty rules), France second. For France, the profiles
are explicit that anything not read on Légifrance or the BOFiP during the
conversation is `TO VERIFY`.
