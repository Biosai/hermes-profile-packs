# Hermes Immo

Hermes Immo is a French-language expert panel for a small property investor who
runs his own company: buy-to-resell, purchase options, rentals (long stay,
short stay, shared housing, furnished corporate lets), building division and
public auctions. Belgium comes first, France second.

One orchestrator, `immo-bras-droit`, is the investor's right hand: it is the only
profile that asks him questions, keeps his investor profile and his answers with
their source, consults the specialists and delivers the synthesis. Seven
specialists each mirror a real professional and prepare that professional's
work.

The profiles, shared rules and skills are written in French, because the domain
is Belgian and French law and the users are francophone.

## Roster

| Profile | Category | Role | Jobs |
| --- | --- | --- | --- |
| `immo-bras-droit` | coordination | Right hand and orchestrator: one question at a time, investor profile, expert consultation, synthesis. | `questions-ouvertes-client`, `capture-donnees-client`, `suivi-demandes-client`, `consulter-expert`, `debat-experts` |
| `immo-architecte` | technique | How many dwellings are legally recognised, what it takes to create one more, plans and quantities, the exact question for the planning office. | `logements-reconnus`, `division-et-permis`, `lecture-plans-metres`, `question-urbanisme` |
| `immo-associe` | strategie | The sceptical partner of an investment committee: every way to make a property pay, in ranges, and which one survives the worst reasonable case. | `strategies-sur-un-bien`, `trois-scenarios`, `valeur-de-marche-comparables`, `rentabilite-locative`, `contradicteur-analyses-externes` |
| `immo-avocat` | droit | Every legal question goes through it: leases, landlord, buyer and building disputes, clauses, public sales, on the primary text, reviewed adversarially. | `relecture-contradictoire`, `sources-droit-primaire`, `bail-et-locataire`, `analyse-clause`, `dossier-litige` |
| `immo-comptable-be` | fiscalite | Belgian tax and accounting of the deal: registration duties by region, VAT, corporate tax, costs; options until the investor's accountant confirms in writing. | `droits-enregistrement`, `tva-immobilier`, `impot-societes-operation`, `frais-operation`, `question-au-comptable` |
| `immo-comptable-fr` | fiscalite | A Belgian company investing in France: French tax first, the Belgian half flagged, the exact question for a French chartered accountant. | `societe-belge-en-france`, `marchand-de-biens-france`, `regimes-locatifs-france`, `question-expert-comptable-fr` |
| `immo-notaire` | acte | What the investor signs, inherits and must ask before signing: preliminary contracts, options, auction conditions, the co-ownership file, documents to demand. | `compromis-et-option`, `cahier-des-charges-vente-publique`, `dossier-copropriete`, `pieces-a-reclamer`, `questionnaire-garde-fou` |
| `immo-conducteur-travaux` | travaux | Turns a listing, photos and certificates into cost items per level of intervention, from a library of work items; separates cost price from estimate. | `lecture-photo-travaux`, `bibliotheque-ouvrages`, `chiffrage-travaux`, `fournitures-quantites-prix`, `obligations-et-aides-renovation` |

Backbone: `immo-bras-droit`, `immo-associe`, `immo-comptable-be`,
`immo-notaire`, `immo-conducteur-travaux`.

## How the profiles work together

- **Questions belong to the right hand.** Specialists name the missing data and
  what it blocks; only `immo-bras-droit` asks the investor, one question at a
  time, and never re-asks a question he has settled or stopped.
- **The investor profile is the single source of his rules.** Whether he does
  the works himself (then the works line is a cost price for him and an
  estimate for everyone else), his zones, thresholds, scenario parameters and
  decisions are recorded with their source by `immo-bras-droit`. Nothing in it
  is assumed.
- **Consultation.** A profile that needs another's expertise sends a question
  starting with `[Consultation interne]`, carrying the dossier and the exact
  question. The answer is quoted as that profile's opinion, reservations
  included; two diverging opinions are both shown. Profiles verify that a
  collaborator is installed before relying on it, and say so when it is not.
- **Every legal question goes through `immo-avocat`**, even when it comes up in
  passing. Tax figures stay with the accountants, the deed with the notary,
  planning with the architect.
- **Expert debate.** On an important deal, `immo-bras-droit` puts the same
  question to several specialists, runs a contradictory second round and
  delivers a synthesis without taking sides.

## Authority boundaries

These profiles **prepare the work of regulated professionals; they do not give
regulated legal, tax, notarial or architectural advice and do not replace an
architect, lawyer, accountant or notary.** Each specialist produces the rule,
the text that carries it, the documents to gather and the exact question to put
to the real professional.

Rules every profile follows (from `shared/RULES.md`):

- every figure is a range with its sample size; missing data is named, never
  filled in (`INCOMPLET`);
- no tax rate, threshold or deadline from memory: law and tax are cited on the
  primary source with its version date, otherwise marked `À VÉRIFIER`;
- Belgian registration duties and planning rules differ by region, so the
  region is established first;
- a document is quoted word for word with its page or article;
- no return is ever promised; nothing is published or sent without the
  investor's explicit consent; emails and orders are drafts only.

## Install

```bash
python install.py --list
python install.py immo-bras-droit immo-associe immo-conducteur-travaux
python install.py
```

The installer uses Hermes' native profile distribution command and sets each
profile description from its `distribution.yaml`. It never creates scheduled
jobs, memory, credentials or other runtime state. Reminders and periodic expert
debates are described as optional routines; set them up yourself on the host
if you want them.

## Settings and prerequisites

The pack assumes nothing about where the investor's data lives, which regions
are in play, or whether reminders exist. Each skill declares the settings it
branches on under `metadata.hermes.config`, using the shared keys of
[`docs/PORTABLE_SKILLS.md`](../docs/PORTABLE_SKILLS.md):

| Key | Values | Default | Used for |
| --- | --- | --- | --- |
| `immo.fiche_investisseur` | `memory`, a path | `memory` | The investor profile: what he does himself, zones, thresholds, scenario parameters, decisions, his advisers' written answers. In `memory`, only the profile that keeps it sees it, so the right hand passes the useful lines to each expert. |
| `immo.registre_questions` | `memory`, a path | `memory` | Open, answered, settled and stopped questions, plus a section for his requests. |
| `immo.juridictions` | e.g. `BE-WAL,BE-BRU,BE-VLA,FR`, `detect` | `detect` | Regions in play. `detect`: derived from the property's address, stated and confirmed. Without `FR`, nothing French is proposed unprompted. |
| `immo.bibliotheque_ouvrages` | a path, `none` | `none` | The work-item cost library. `none`: every cost item rests on a dated, sourced price. |
| `owner.channel` | free text | this conversation | Where questions reach the investor. No reminder is sent or promised unless a scheduled task really exists on the host. |

Current values reach the agent as the `[Skill config]` block when a skill
loads; an unset key shows its declared default. Set a value with
`hermes config set skills.config.<key> <value>` (one profile:
`hermes -p <profile> config set …`), or run `hermes config migrate` to be
prompted for every declared key that is still unset.

Every skill opens with a `## Prérequis` table (need, why, one-line check) and a
`## Configuration` section. Typical prerequisites are the document itself
(compromis, cahier des charges, lease, co-ownership minutes, permit), the
property address to establish the region, the investor profile, and read
access to public official sources. Optional accesses (a paid case-law
database, a cadastral or planning portal account) have a stated fallback. When
a required prerequisite is missing, the skill stops before its first step,
says what is missing, what it blocks and the smallest access that would
unblock it, and never replaces an unread document or figure with an estimate.
No skill needs a credential, so none declares `required_environment_variables`.

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
for one investor's company in Belgium, then generalized: people became roles,
the investor's own numbers, strategy choices and dossiers were removed, dated
anecdotes became the rules they taught, and every tax rate or legal threshold
was replaced by the regime, its conditions and where to read the current value.

## Jurisdiction scope

Belgium first (Wallonia, Flanders and Brussels, each with its own leasing,
planning and registration-duty rules), France second. For France, the profiles
are explicit that anything not read on Légifrance or the BOFiP during the
conversation is `À VÉRIFIER`.

## Résumé en français

Hermes Immo est une équipe d'experts, en français, au service d'un investisseur
immobilier qui opère par sa propre société : achat-revente, option d'achat,
location longue et courte durée, colocation, meublé pour entreprises, division
d'immeubles et ventes publiques, en Belgique d'abord, en France ensuite. Le
bras droit (`immo-bras-droit`) est le seul à poser des questions à
l'investisseur, une à la fois ; il tient sa fiche et ses réponses avec leur
source, consulte les experts et livre la synthèse. L'architecte, l'associé,
l'avocat, les comptables belge et français, le notaire et le conducteur de
travaux préparent le travail des professionnels réels, sans les remplacer :
toute sortie est une fourchette avec son effectif, aucune donnée manquante
n'est comblée, le droit et la fiscalité se citent sur le texte primaire avec
leur date de version — sinon « À VÉRIFIER » —, et rien n'est envoyé sans son
accord. Aucun skill ne suppose où vivent la fiche et le registre, quelles régions
sont en jeu ni qu'un rappel existe : ce sont des réglages
(`hermes config set skills.config.<clé> <valeur>`), et chaque skill liste ses
prérequis et s'arrête proprement s'il en manque un. Installation :
`python install.py --list`, puis `python install.py <profils>`. Règles
communes : modifier `shared/RULES.md`, puis `python sync_shared.py`.
