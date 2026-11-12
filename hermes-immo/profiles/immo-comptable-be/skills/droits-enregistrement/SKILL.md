---
name: droits-enregistrement
description: "Chiffrer les droits d'enregistrement, région par région"
metadata:
  hermes:
    config:
      - key: immo.juridictions
        description: "Régions en jeu, ex. BE-WAL,BE-BRU,BE-VLA,FR ; ou detect"
        default: "detect"
      - key: immo.fiche_investisseur
        description: "Où vit la fiche investisseur : memory ou un chemin"
        default: "memory"
---
# Droits d'enregistrement (Belgique)

## Quand l'utiliser

Pour toute acquisition à chiffrer (gré à gré, vente publique, levée
d'option, achat de lots, apport) et chaque fois qu'un prix plafond dépend des
frais d'entrée.

## Prérequis

| Besoin | Pourquoi | Vérification |
|---|---|---|
| L'adresse du bien (requis) | la région désigne le code | commune connue |
| La qualité de l'acquéreur (requis) | plusieurs régimes en dépendent | la fiche ou les statuts le disent |
| L'accès au code régional en vigueur (requis) | aucun taux de mémoire | le texte s'ouvre avec sa date de version |

Si un prérequis requis manque, arrête-toi avant l'étape 1 : dis lequel, ce
qu'il bloque et le plus petit accès qui le débloque (lecture seule d'abord).
Ne fais que les parties qui ont un sens sans lui. Ne remplace jamais une pièce
ou un chiffre non lu par une estimation ; une recherche échouée n'est pas
« rien trouvé ».

## Configuration

- `immo.juridictions` : quel code régional lire (BE-WAL, BE-VLA, BE-BRU) ; FR
  → `immo-comptable-fr`. `detect` (défaut) : déduis la région de l'adresse du
  bien, dis-la, fais-la confirmer.
- `immo.fiche_investisseur` : régime appliqué par défaut et écrits de son
  comptable ; illisible → tous les régimes sortent en scénarios.

Réglage vide ou `detect` : dis ce que tu as retenu et donne la ligne qui le
fixe, `hermes config set skills.config.<clé> <valeur>` (un seul profil :
`hermes -p <profil> config set …`).

## Étapes

1. **Établis la région du bien** : Wallonie, Flandre et Bruxelles ont chacune
   leur code des droits d'enregistrement, leurs taux, leurs régimes et leurs
   délais. Rien ne se transpose d'une région à l'autre.
2. **Établis l'acquéreur** : société ou personne physique, assujetti ou non,
   activité déclarée. Plusieurs régimes réduits sont réservés aux personnes
   physiques ; un autre aux professionnels de l'achat-revente.
3. **Lis le code régional en vigueur**, avec sa date de version : taux du
   régime ordinaire, du régime des professionnels de l'achat-revente, de tout
   abattement, et leurs conditions. Note article et version pour chacun.
4. **Liste les conditions du régime réduit** telles que le texte les écrit :
   qualité de l'acquéreur, déclaration ou affirmation dans l'acte, garantie,
   délai de revente, nombre d'opérations, sanction en cas de non-revente.
5. **Lis la fiche** : quel régime l'investisseur veut voir appliqué par
   défaut, et ce que l'écrit de son comptable a confirmé.
6. **Chiffre un scénario par régime possible** : droits, base (prix ou valeur
   vénale si supérieure), et effet sur le prix plafond.
7. **Restitution** : dis si le texte prévoit une restitution en cas de revente
   rapide, à quelles conditions et dans quel délai.
8. **Montages** (option, vente par lots, achat scindé, apport) : le régime
   dépend de la rédaction ; consulte `immo-notaire`, présente en scénarios.

## Ce que tu sors

Un tableau : régime, texte (article, région, version), taux lu, base, droits
en fourchette, conditions, qui les vérifie (acte → `immo-notaire`). Le régime
par défaut de la fiche en tête, l'autre en scénario. Mention « à confirmer par
son comptable » tant qu'un écrit ne l'a pas fait.

## Pièges

- Un taux de mémoire, ou celui d'une autre région : les barèmes changent, et
  pas en même temps.
- Une condition de forme absente de l'acte : régime réduit perdu, souvent sans
  restitution. L'écart peut valoir la marge entière.
- Calculer les droits sur le prix annoncé, puis enchérir au-delà.
- Appliquer à une société un abattement réservé aux personnes physiques.
