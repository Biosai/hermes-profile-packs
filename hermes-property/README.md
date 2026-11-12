# Hermes Property

Hermes Property is an expert panel for a small property investor who runs his
own company: buy-to-resell, purchase options, letting (long-term, short-term,
shared housing, furnished corporate lets), building division and public
auctions. Belgium comes first, France second.

One orchestrator, `property-coordinator`, is the investor's right hand: it is
the only profile that asks him questions, keeps his investor file and his
answers with their source, consults the specialists and delivers the
synthesis. Seven specialists each mirror a real professional and prepare that
professional's work.

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
| `property-accountant-be` | tax | Belgian tax and accounting of the deal: registration duties by region, VAT, corporate income tax, costs; options until the investor's accountant confirms in writing. | `registration-duties`, `vat-regimes`, `corporate-tax-per-deal`, `deal-costs`, `accountant-question` |
| `property-accountant-fr` | tax | A Belgian company investing in France: French tax first, the Belgian half flagged, the exact question for a French chartered accountant. | `belgian-company-in-france`, `dealer-regime-france`, `french-rental-regimes`, `french-accountant-question` |
| `property-notary` | conveyancing | What the investor signs, inherits and must ask before signing: preliminary contracts, options, auction conditions, the co-ownership file, documents to request. | `sale-agreement-and-option`, `auction-conditions`, `co-ownership-file`, `documents-to-request`, `pre-signing-checklist` |
| `property-works-estimator` | works | Turns a listing, photos and certificates into cost items per level of intervention, from a cost library; separates cost price from estimate. | `listing-photo-review`, `cost-library`, `works-estimate`, `materials-quantities-prices`, `renovation-obligations-and-aid` |

Backbone: `property-coordinator`, `property-investment-partner`,
`property-accountant-be`, `property-notary`, `property-works-estimator`.

## How the profiles work together

- **Questions belong to the coordinator.** Specialists name the missing data
  and what it blocks; only `property-coordinator` asks the investor, one
  question at a time, and never asks again a question he has settled or
  stopped.
- **The investor file is the single source of his rules.** Whether he does the
  works himself (then the works line is a cost price for him and an estimate
  for everyone else), his areas, thresholds, scenario parameters and decisions
  are recorded with their source by `property-coordinator`. Nothing in it is
  assumed.
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

Rules every profile follows (from `shared/RULES.md`):

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
| `property.investor_file` | `memory`, a path | `memory` | The investor file: what he does himself, areas, thresholds, scenario parameters, decisions, his advisers' written answers. In `memory`, only the profile that keeps it sees it, so the coordinator passes the useful lines to each expert. |
| `property.question_register` | `memory`, a path | `memory` | Open, answered, settled and stopped questions, plus a section for his requests. |
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

The team-wide rules live once in `shared/RULES.md` and are copied, byte for
byte, into a block at the end of every `SOUL.md`. Edit `shared/RULES.md`, then:

```bash
python sync_shared.py          # rewrite the block in every SOUL
python sync_shared.py --check  # report drift without writing
python validate.py
python -m unittest discover -s tests -p 'test_*.py'
```

`validate.py` fails if any SOUL's block differs from `shared/RULES.md`.

## Provenance

This pack was distilled from a team of Hermes profiles running in production
for one investor's company in Belgium, then generalized and translated: people
became roles, the investor's own numbers, strategy choices and deals were
removed, dated anecdotes became the rules they taught, and every tax rate or
legal threshold was replaced by the regime, its conditions and where to read
the current value.

## Jurisdiction scope

Belgium first (Wallonia, Flanders and Brussels, each with its own leasing,
planning and registration-duty rules), France second. For France, the profiles
are explicit that anything not read on Légifrance or the BOFiP during the
conversation is `TO VERIFY`.
