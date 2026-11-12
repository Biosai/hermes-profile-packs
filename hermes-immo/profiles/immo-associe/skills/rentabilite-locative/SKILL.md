---
name: rentabilite-locative
description: "Chiffrer le cash-flow d'une location, avant impôt"
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
# Rentabilité locative

## Quand l'utiliser

Quand un bien ou un lot est destiné à être loué, conservé après division, ou
quand il faut comparer revente et location.

## Prérequis

| Besoin | Pourquoi | Vérification |
|---|---|---|
| L'adresse et le type de location (requis) | régime, autorisations, loyers | région et type sont établis |
| La grille officielle des loyers, si la région en publie une | le loyer se lit, il ne s'estime pas | la grille s'ouvre avec sa date |
| La fiche investisseur (pour le seuil de rendement) | comparer au seuil | la fiche se lit ; sinon, pas de verdict de seuil |

Si un prérequis requis manque, arrête-toi avant l'étape 1 : dis lequel, ce
qu'il bloque et le plus petit accès qui le débloque (lecture seule d'abord).
Ne fais que les parties qui ont un sens sans lui. Ne remplace jamais une pièce
ou un chiffre non lu par une estimation ; une recherche échouée n'est pas
« rien trouvé ».

## Configuration

- `immo.juridictions` : décide grille de loyers, règles de courte durée et
  régime du bail. `detect` (défaut) : déduis la région de l'adresse du bien,
  dis-la, fais-la confirmer.
- `immo.fiche_investisseur` : seuil de rendement d'un lot conservé ; en
  `memory` (défaut), demande-le à `immo-bras-droit`.

Réglage vide ou `detect` : dis ce que tu as retenu et donne la ligne qui le
fixe, `hermes config set skills.config.<clé> <valeur>` (un seul profil :
`hermes -p <profil> config set …`).

## Étapes

1. **Qualifie le type de location** : longue durée, colocation, courte durée
   (meublé de tourisme), meublé pour entreprises (séjours de quelques mois).
   Chaque type a son régime juridique (`immo-avocat`), fiscal (comptables) et
   ses autorisations (`immo-architecte` : changement d'usage, enregistrement).
2. **Vérifie qu'il est permis** : une courte durée interdite ou soumise à
   autorisation non obtenue sort « impossible ».
3. **Source les loyers** :
   - si la région publie une **grille indicative des loyers**, lis-la sur le
     site officiel, avec sa date ; ne l'estime pas ;
   - sinon, au moins quatre annonces comparables nommées ;
   - courte durée : un prix par nuit et une occupation n'ont en général pas de
     source publique fiable ; présente-les en **scénarios**, jamais comme une
     mesure ;
   - colocation : seulement là où une demande est démontrée (annonces,
     plateformes, établissements proches).
4. **Liste les charges** : précompte ou taxe foncière, assurance, entretien,
   gestion, vacance locative, charges non récupérables, ménage et linge en
   courte durée, mobilier et son renouvellement en meublé.
5. **Calcule** en fourchette : loyer annuel, charges, cash-flow avant impôt,
   rendement brut et net sur prix de revient total.
6. **Compare** au seuil de rendement de sa fiche pour un lot conservé.

## Ce que tu sors

Par type de location : loyer (source, date), charges, cash-flow **avant
impôt** (la mention est obligatoire), rendements brut et net, en fourchette,
avec les hypothèses de vacance et d'occupation marquées comme scénarios.

## Pièges

- Prendre le loyer demandé par le vendeur ou le bail en cours pour un loyer de
  marché : c'est une donnée, pas un comparable.
- Un taux d'occupation de courte durée « moyen » trouvé en ligne : c'est un
  scénario, au mieux.
- Oublier la fiscalité de l'investisseur : sans l'avis du comptable, le
  chiffre reste avant impôt, et se dit.
- Déguiser un dossier locatif en prix plafond de revente.
