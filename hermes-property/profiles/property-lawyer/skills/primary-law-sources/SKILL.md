---
name: primary-law-sources
description: "Find and cite the legal text that is authoritative"
metadata:
  hermes:
    config:
      - key: property.jurisdictions
        description: "Regions in play, e.g. BE-WAL,BE-BRU,BE-VLA,FR; or detect"
        default: "detect"
---
# Primary law sources

## When to use

For every rule you are about to cite, and for any profile on the team that
must cite a text (the accountant for a tax code, the notary for co-ownership,
the architect for a planning code).

## Prerequisites

| Needs | Why | Check |
|---|---|---|
| Web access to the official sources (required, free) | read the authoritative text | Justel, Wallex, Vlaamse Codex or Légifrance open |
| A paid case-law database (optional) | decisions not published in the free databases | access is configured; otherwise "case law not consulted" |

If a required prerequisite is missing, stop before step 1. Say which one, what
it blocks, and the smallest access that would unblock it (read-only first). Do
the parts that do not need it only if they still make sense alone. Never
replace data you could not read with an estimate, and never report "nothing
found" when the lookup failed.

## Configuration

- `property.jurisdictions`: designates the sources to open (BE-WAL: Wallex and
  Justel; BE-VLA: Vlaamse Codex; BE-BRU: Justel and the Moniteur belge; FR:
  Légifrance). `detect` (default): region derived from the facts, then
  confirmed.

If a value is unset or `detect`, say what you used, and give the line that
sets it: `hermes config set skills.config.<key> <value>` (one profile:
`hermes -p <profile> config set …`).

## Where to read

- **Belgium, federal and regional**: the Moniteur belge (the official
  gazette, authoritative) and Justel (the consolidated legislation database
  of the Federal Public Service Justice: an unofficial consolidation, handy
  for reading the current version).
- **Wallonia**: Wallex. **Flanders**: Vlaamse Codex — the text exists only in
  Dutch: quote the Dutch, your translation is a "working translation".
  **Brussels**: Moniteur belge and Justel, in French or Dutch.
- **Belgian case law**: Juportal (Court of Cassation, a selection of appeal
  and first-instance decisions). Decisions of the justice of the peace (*juge
  de paix*, the lease judge) are rare there.
- **France**: Légifrance (codes, statutes, decrees, published case law);
  BOFiP for tax doctrine.

## Steps

1. **Establish the region and the date** of the facts: they designate the
   text and its version.
2. **Open the consolidated text** and note the consolidation update date and
   the acts that amended the article.
3. **An article can have several versions** (one per region, or before and
   after a reform): cite the one that applies, naming it.
4. **An article missing from a page is not the absence of a rule**: a large
   code is split into several pages or books; find the right one.
5. **On a point that decides a dispute**, go back to the publication in the
   Moniteur belge (or the Journal officiel) that the list of amendments
   points to.
6. **Cite**: text, article, word-for-word quotation, version date read.

## Output

For each rule: text, article, exact quotation, source consulted, version
date, and if needed the regional version named.

## Pitfalls

- A lawyer's, notary's or trade association's website, a brochure or the
  press help you find the article; they prove nothing.
- An internal summary note tells you where to look; one has been wrong
  before.
- Citing a court decision you have not read: forbidden.
- Translating a Flemish text and quoting the translation as the text.
