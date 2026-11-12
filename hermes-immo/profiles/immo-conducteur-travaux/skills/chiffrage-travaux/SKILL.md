---
name: chiffrage-travaux
description: "Chiffrer les travaux d'un bien par niveau d'intervention"
metadata:
  hermes:
    config:
      - key: immo.bibliotheque_ouvrages
        description: "Chemin de la bibliothèque d'ouvrages, ou none"
        default: "none"
      - key: immo.fiche_investisseur
        description: "Où vit la fiche investisseur : memory ou un chemin"
        default: "memory"
---
# Chiffrage des travaux

## Quand l'utiliser

À chaque dossier que `immo-associe` arbitre ; pour un prix plafond ; pour
comparer revente et location ; pour contrôler un budget venu d'ailleurs.

## Prérequis

| Besoin | Pourquoi | Vérification |
|---|---|---|
| La lecture du bien : photos, annonce, certificats (requis) | postes visibles | le skill `lecture-photo-travaux` est passé |
| Une base de prix (requis) | aucune moyenne de marché | chaque poste nomme sa base : bibliothèque, prix de revient ou relevé daté |

Si un prérequis requis manque, arrête-toi avant l'étape 1 : dis lequel, ce
qu'il bloque et le plus petit accès qui le débloque (lecture seule d'abord).
Ne fais que les parties qui ont un sens sans lui. Ne remplace jamais une pièce
ou un chiffre non lu par une estimation ; une recherche échouée n'est pas
« rien trouvé ».

## Configuration

- `immo.bibliotheque_ouvrages` : un chemin → base par défaut ; `none` (défaut)
  → chaque poste repose sur un prix relevé et daté, statut « relevé,
  indicatif ».
- `immo.fiche_investisseur` : s'il fait les travaux, lesquels, à quel prix de
  revient ; illisible → estimation d'entreprise, dite.

Réglage vide ou `detect` : dis ce que tu as retenu et donne la ligne qui le
fixe, `hermes config set skills.config.<clé> <valeur>` (un seul profil :
`hermes -p <profil> config set …`).

## Étapes

1. **Lis la fiche** : l'investisseur fait-il les travaux lui-même, lesquels,
   à quel prix de revient ? Les postes qu'il réalise se chiffrent à son prix
   de revient ; les autres, en estimation d'entreprise.
2. **Pars de la lecture du bien** (skill `lecture-photo-travaux`) et des
   quantités (`immo-architecte` si les plans existent).
3. **Définis trois niveaux** : en l'état (mise en sécurité seulement),
   rafraîchissement (finitions, sanitaires, peinture), rénovation complète
   (techniques, enveloppe, saut de classe énergétique si visé).
4. **Par poste et par niveau** : quantité × prix de base (ligne de
   bibliothèque, prix de revient ou prix relevé et daté), en fourchette basse
   et haute. La base de chaque poste est nommée.
5. **Provision d'imprévus** en ligne séparée, plus large quand la visite n'a
   pas eu lieu.
6. **Obligations** : une rénovation qui vise une classe énergétique ou qui
   déclenche une obligation suit le texte en vigueur (skill
   `obligations-et-aides-renovation`) ; aucun équipement en voie
   d'interdiction n'est budgété.
7. **Durée** de chaque niveau en fourchette : elle est une hypothèse de
   portage pour `immo-associe`.
8. **Relis à l'envers** : le total divisé par la surface est-il plausible pour
   ce niveau ? Sinon, cherche le poste fautif.

## Ce que tu sors

Un budget par niveau : postes, quantités, fourchettes, provision, total,
durée ; ce qui reste inconnu sans visite ; la ligne de statut — « base :
bibliothèque, indicatif », « base : relevé, indicatif », « base : prix de
revient de sa fiche » ou « base : son chantier réel <référence> ». Montants hors TVA ; la TVA est l'affaire de
`immo-comptable-be`.

## Pièges

- Un prix au m² global au lieu de postes : on ne sait plus ce qui est
  compté.
- Chiffrer à son prix de revient ce qu'il ne fait pas lui-même.
- Oublier les frais annexes : évacuation, échafaudage, raccordements,
  protections, nettoyage.
- Un budget sans « à voir en visite » : il prétend savoir ce qu'il ignore.
