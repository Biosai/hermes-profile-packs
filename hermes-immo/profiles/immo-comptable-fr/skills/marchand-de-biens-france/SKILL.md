---
name: marchand-de-biens-france
description: "Cadrer l'achat-revente en France : droits, TVA, profits"
metadata:
  hermes:
    config:
      - key: immo.juridictions
        description: "Régions en jeu, ex. BE-WAL,BE-BRU,BE-VLA,FR ; ou detect"
        default: "detect"
---
# Achat-revente en France (marchand de biens)

## Quand l'utiliser

Quand la société de l'investisseur envisage d'acheter en France pour
revendre, avec ou sans travaux, en bloc ou par lots.

## Prérequis

| Besoin | Pourquoi | Vérification |
|---|---|---|
| Le bien, sa nature et la structure acheteuse (requis) | droits et TVA en dépendent | neuf, terrain ou ancien, et acheteur, écrits |
| L'accès à Légifrance et au BOFiP (requis, gratuit) | aucun chiffre de mémoire | le texte s'ouvre ; sinon À VÉRIFIER |

Si un prérequis requis manque, arrête-toi avant l'étape 1 : dis lequel, ce
qu'il bloque et le plus petit accès qui le débloque (lecture seule d'abord).
Ne fais que les parties qui ont un sens sans lui. Ne remplace jamais une pièce
ou un chiffre non lu par une estimation ; une recherche échouée n'est pas
« rien trouvé ».

## Configuration

- `immo.juridictions` : sans FR, signale que la France n'est pas configurée et
  ne propose rien de français ; une question qu'il pose lui-même reçoit sa
  réponse. `detect` (défaut) : FR si le bien est en France, confirmé.

Réglage vide ou `detect` : dis ce que tu as retenu et donne la ligne qui le
fixe, `hermes config set skills.config.<clé> <valeur>` (un seul profil :
`hermes -p <profil> config set …`).

## Étapes

1. **Annonce l'état des sources** : sans Légifrance ni BOFiP lus dans la
   conversation, tout chiffre est **À VÉRIFIER**.
2. **Droits de mutation** : lis le régime de l'engagement de revendre (CGI,
   art. 1115 — version en vigueur ; série BOFiP des droits de mutation) : délai,
   conditions, mention dans l'acte, sanction en cas de non-revente. La mention
   se vérifie avec `immo-notaire` sur l'acte.
3. **TVA** : lis le régime de la TVA immobilière (série BOFiP sur la TVA
   immobilière ; CGI, art. 268 pour la TVA sur marge — version en vigueur) :
   la vente est-elle soumise à TVA, sur le prix total ou sur la marge, selon la
   nature du bien (neuf, terrain à bâtir, ancien) et les conditions
   d'acquisition.
4. **Profits** : imposition des profits de marchand de biens (série BOFiP sur
   le champ des BIC) et, pour une société belge, le lien avec l'impôt sur les
   sociétés français (skill `societe-belge-en-france`).
5. **Calcule en scénarios** : un scénario par régime de droits et de TVA
   plausible, effet sur le prix plafond pour `immo-associe`.
6. **Signale la moitié belge** à `immo-comptable-be`.

## Ce que tu sors

Un tableau par impôt (droits, TVA, impôt sur les profits) : régime, texte et
version (ou À VÉRIFIER), conditions, effet en fourchette. Puis les mentions à
faire figurer dans l'acte, à vérifier par `immo-notaire`, et la question pour
un expert-comptable français.

## Pièges

- Supposer qu'un régime belge a son équivalent français à l'identique.
- Choisir entre TVA sur marge et TVA sur le prix total sans avoir lu les
  conditions d'acquisition qui ouvrent la marge.
- Laisser passer le délai de revente d'un engagement : la sanction est due.
- Chiffrer des droits sans savoir si la structure acheteuse est belge ou
  française.
