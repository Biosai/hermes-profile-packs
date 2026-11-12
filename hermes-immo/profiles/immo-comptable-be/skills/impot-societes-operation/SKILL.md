---
name: impot-societes-operation
description: "Traiter l'impôt des sociétés d'une opération"
metadata:
  hermes:
    config:
      - key: immo.fiche_investisseur
        description: "Où vit la fiche investisseur : memory ou un chemin"
        default: "memory"
---
# Impôt des sociétés d'une opération

## Quand l'utiliser

Quand l'investisseur ou un expert demande le résultat après impôt d'une
opération, compare revente et conservation, ou s'interroge sur la sortie d'un
bien de la société.

## Prérequis

| Besoin | Pourquoi | Vérification |
|---|---|---|
| Les chiffres de l'opération (requis) | base du résultat | marge, frais et travaux sourcés |
| La règle de présentation de la fiche | par projet ou en fin d'exercice | la fiche se lit ; sinon, avant impôt et dit |

Si un prérequis requis manque, arrête-toi avant l'étape 1 : dis lequel, ce
qu'il bloque et le plus petit accès qui le débloque (lecture seule d'abord).
Ne fais que les parties qui ont un sens sans lui. Ne remplace jamais une pièce
ou un chiffre non lu par une estimation ; une recherche échouée n'est pas
« rien trouvé ».

## Configuration

- `immo.fiche_investisseur` : comment il veut voir l'impôt, et ce que son
  comptable a confirmé. En `memory` (défaut), demande-le à `immo-bras-droit` ;
  illisible → chiffre avant impôt et dis-le.

Réglage vide ou `detect` : dis ce que tu as retenu et donne la ligne qui le
fixe, `hermes config set skills.config.<clé> <valeur>` (un seul profil :
`hermes -p <profil> config set …`).

## Étapes

1. **Lis sa règle dans la fiche** : juge-t-il un projet avant impôt, l'impôt
   se calculant en fin d'exercice sur l'ensemble des bénéfices, ou veut-il un
   résultat après impôt par projet ? Applique-la ; à défaut, chiffre avant
   impôt et dis-le.
2. **Qualifie le bien** : stock (achat pour revendre) ou immobilisation
   (conservé, loué). La qualification change le traitement comptable, la
   plus-value et l'amortissement ; elle est à confirmer par son comptable.
3. **Lis le Code des impôts sur les revenus en vigueur** : taux ordinaire,
   taux réduit et ses conditions (rémunération du dirigeant, structure de
   l'actionnariat, taille), régimes de plus-values, règles d'amortissement.
4. **Calcule le résultat de l'opération** : marge, frais déductibles,
   amortissement s'il y a lieu. L'amortissement diffère l'impôt, il ne le
   supprime pas : dis-le.
5. **Présente l'impôt en fourchette**, un scénario par taux possible, tant que
   son comptable n'a pas confirmé la situation de la société.
6. **Signale les effets en personne** : rémunération, dividende, loyer perçu
   de la société, avantage de toute nature. C'est souvent là que se joue
   l'arbitrage, et c'est à son comptable de trancher.

## Ce que tu sors

Qualification (stock ou immobilisation, à confirmer), résultat avant impôt,
impôt en fourchette par scénario de taux, texte et version, effets en
personne signalés, question pour son comptable.

## Pièges

- Un tableau qui mélange l'amortissement seul et le résultat global d'un
  bien compare deux choses différentes.
- Appliquer le taux réduit sans en vérifier toutes les conditions.
- Ajouter un bloc d'impôt que sa règle exclut de la présentation par projet.
- Oublier que l'impôt d'une société dépend de l'ensemble de ses résultats,
  pas d'une seule opération.
