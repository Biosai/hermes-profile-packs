---
name: sources-droit-primaire
description: "Trouver et citer le texte de loi qui fait foi"
metadata:
  hermes:
    config:
      - key: immo.juridictions
        description: "Régions en jeu, ex. BE-WAL,BE-BRU,BE-VLA,FR ; ou detect"
        default: "detect"
---
# Sources du droit primaire

## Quand l'utiliser

Pour toute règle que tu vas citer, et pour tout profil de l'équipe qui doit
citer un texte (le comptable pour un code fiscal, le notaire pour la
copropriété, l'architecte pour un code d'urbanisme).

## Prérequis

| Besoin | Pourquoi | Vérification |
|---|---|---|
| L'accès web aux sources officielles (requis, gratuit) | lire le texte qui fait foi | Justel, Wallex, Vlaamse Codex ou Légifrance s'ouvrent |
| Une base de jurisprudence payante (optionnel) | décisions publiées ailleurs que dans les bases gratuites | l'accès est configuré ; sinon « jurisprudence non consultée » |

Si un prérequis requis manque, arrête-toi avant l'étape 1 : dis lequel, ce
qu'il bloque et le plus petit accès qui le débloque (lecture seule d'abord).
Ne fais que les parties qui ont un sens sans lui. Ne remplace jamais une pièce
ou un chiffre non lu par une estimation ; une recherche échouée n'est pas
« rien trouvé ».

## Configuration

- `immo.juridictions` : désigne les sources à ouvrir (BE-WAL : Wallex et
  Justel ; BE-VLA : Vlaamse Codex ; BE-BRU : Justel et Moniteur belge ; FR :
  Légifrance). `detect` (défaut) : région déduite des faits, confirmée.

Réglage vide ou `detect` : dis ce que tu as retenu et donne la ligne qui le
fixe, `hermes config set skills.config.<clé> <valeur>` (un seul profil :
`hermes -p <profil> config set …`).

## Où lire

- **Belgique, fédéral et régional** : le Moniteur belge (publication
  officielle, fait foi) et Justel (base de législation consolidée du SPF
  Justice : consolidation officieuse, pratique pour lire la version à jour).
- **Wallonie** : Wallex. **Flandre** : Vlaamse Codex — le texte n'existe qu'en
  néerlandais : cite le néerlandais, ta traduction est « de travail ».
  **Bruxelles** : Moniteur belge et Justel, en français ou en néerlandais.
- **Jurisprudence belge** : Juportal (Cassation, une sélection d'appels et de
  premières instances). Les décisions de justice de paix y sont rares.
- **France** : Légifrance (codes, lois, décrets, jurisprudence publiée) ;
  BOFiP pour la doctrine fiscale.

## Étapes

1. **Établis la région et la date** des faits : elles désignent le texte et sa
   version.
2. **Ouvre le texte consolidé** et note la date de mise à jour de la
   consolidation, et les actes qui ont modifié l'article.
3. **Un article peut avoir plusieurs versions** (une par région, ou avant et
   après une réforme) : cite celle qui s'applique, en la nommant.
4. **Un article absent d'une page n'est pas l'absence de règle** : un grand
   code est découpé en plusieurs pages ou livres ; cherche la bonne.
5. **Sur un point qui décide d'un litige**, remonte à la publication au
   Moniteur belge (ou au Journal officiel) que la liste des modifications
   désigne.
6. **Cite** : texte, article, citation mot pour mot, date de version lue.

## Ce que tu sors

Pour chaque règle : texte, article, citation exacte, source consultée, date
de version, et si besoin la version régionale nommée.

## Pièges

- Un site d'avocat, de notaire, de fédération, une brochure ou la presse aident
  à trouver l'article ; ils ne prouvent rien.
- Une fiche de synthèse interne dit où chercher ; elle a déjà été fausse.
- Citer une décision de justice sans l'avoir lue : interdit.
- Traduire un texte flamand et citer la traduction comme le texte.
