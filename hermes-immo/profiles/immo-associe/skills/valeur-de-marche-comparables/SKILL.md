---
name: valeur-de-marche-comparables
description: "Estimer une valeur de marché sur quatre comparables nommés"
metadata:
  hermes:
    config:
      - key: immo.juridictions
        description: "Régions en jeu, ex. BE-WAL,BE-BRU,BE-VLA,FR ; ou detect"
        default: "detect"
---
# Valeur de marché par comparables

## Quand l'utiliser

Pour tout prix de sortie (revente), toute valeur de lot conservé, tout loyer
de marché, et pour contrôler une valeur avancée par un vendeur ou une agence.

## Prérequis

| Besoin | Pourquoi | Vérification |
|---|---|---|
| Le bien : type, surface sourcée, état, quartier (requis) | critères de comparaison | chaque critère a sa source |
| L'accès aux annonces et aux prix publiés (requis) | trouver les comparables | une recherche rend des résultats datés |

Si un prérequis requis manque, arrête-toi avant l'étape 1 : dis lequel, ce
qu'il bloque et le plus petit accès qui le débloque (lecture seule d'abord).
Ne fais que les parties qui ont un sens sans lui. Ne remplace jamais une pièce
ou un chiffre non lu par une estimation ; une recherche échouée n'est pas
« rien trouvé ».

## Configuration

- `immo.juridictions` : en France (FR), cherche d'abord les prix réalisés
  publiés (DVF) ; en Belgique, vérifie quelle source de prix réalisés existe,
  sinon les comparables sont des prix demandés. `detect` (défaut) : pays
  déduit de l'adresse.

Réglage vide ou `detect` : dis ce que tu as retenu et donne la ligne qui le
fixe, `hermes config set skills.config.<clé> <valeur>` (un seul profil :
`hermes -p <profil> config set …`).

## Étapes

1. **Définis le bien cible** : type, surface (source), étage, état, extérieur,
   stationnement, quartier précis. Ce sont tes critères de comparaison.
2. **Cherche les comparables** : même type, surface proche, même quartier,
   état comparable vu sur les photos. Note pour chacun : source, adresse ou
   localisation, surface, prix, date du relevé, et s'il s'agit d'un **prix
   demandé** (annonce) ou d'un **prix réalisé** (mutation publiée, vente
   publique adjugée).
3. **En France**, les mutations sont publiées (données DVF) : privilégie les
   prix réalisés. **En Belgique**, vérifie quelle source publique de prix
   réalisés existe pour la zone ; à défaut, tes comparables sont des prix
   demandés, et tu le dis.
4. **Écarte en les nommant** ceux qui sortent nettement du lot, au-dessus
   comme en dessous, avec la raison (état, surface, vue, erreur d'annonce).
5. **Garde au moins quatre comparables.** Moins de quatre : sors quand même
   la fourchette, avec l'effectif et la mention que la base est faible.
6. **Ajuste** pour les écarts de surface et d'état, en disant de combien et
   pourquoi ; un ajustement non justifié ne se fait pas.
7. **Sors la fourchette** (bas, médian, haut) et l'effectif.

## Ce que tu sors

Un tableau des comparables retenus (source, localisation, surface, prix,
€/m², date, demandé ou réalisé, ajustement), les écartés avec leur raison, et
la fourchette avec l'effectif.

## Pièges

- Le €/m² médian d'une commune trie les annonces ; il n'estime pas un bien,
  que le quartier et l'état faussent.
- Une annonce restée longtemps en ligne est un prix qui ne s'est pas réalisé.
- Un comparable sans date de relevé est un comparable faux en puissance.
- Comparer un appartement à des maisons, ou un bien loué à des biens libres.
