---
name: compromis-et-option
description: "Lire un compromis ou une option avant signature"
metadata:
  hermes:
    config:
      - key: immo.juridictions
        description: "Régions en jeu, ex. BE-WAL,BE-BRU,BE-VLA,FR ; ou detect"
        default: "detect"
---
# Compromis, promesse et option d'achat

## Quand l'utiliser

Avant toute signature d'un avant-contrat ; quand un vendeur ou une agence
envoie un projet ; quand une option approche de son échéance.

## Prérequis

| Besoin | Pourquoi | Vérification |
|---|---|---|
| Le projet d'avant-contrat complet (requis) | chaque clause se cite | toutes les pages et annexes s'ouvrent |
| La région du bien (requis) | conditions et mentions en dépendent | établie depuis l'adresse |

Si un prérequis requis manque, arrête-toi avant l'étape 1 : dis lequel, ce
qu'il bloque et le plus petit accès qui le débloque (lecture seule d'abord).
Ne fais que les parties qui ont un sens sans lui. Ne remplace jamais une pièce
ou un chiffre non lu par une estimation ; une recherche échouée n'est pas
« rien trouvé ».

## Configuration

- `immo.juridictions` : règles régionales (préemption, mentions, pièces) ; FR
  → droit français, À VÉRIFIER sans texte lu. `detect` (défaut) : déduis la
  région de l'adresse du bien, dis-la, fais-la confirmer.

Réglage vide ou `detect` : dis ce que tu as retenu et donne la ligne qui le
fixe, `hermes config set skills.config.<clé> <valeur>` (un seul profil :
`hermes -p <profil> config set …`).

## Étapes

1. **Identifie la pièce** : compromis (vente parfaite sous conditions),
   promesse unilatérale, option d'achat, offre acceptée. Sa nature décide de
   ce qui engage qui.
2. **Relève les éléments essentiels**, cités mot pour mot : parties, bien
   (description, cadastre, lots), prix, acompte ou arrhes, date de l'acte,
   occupation, charges.
3. **Conditions suspensives** : financement, urbanisme, sol, obtention d'un
   permis, absence de préemption. Pour chacune : délai, preuve à fournir, qui
   peut y renoncer, sort de l'acompte.
4. **Clauses de sortie** : dédit, pénalité, résolution ; montant, conditions.
5. **Pour une option** : sur quels lots, à quel prix, durée, prix de l'option
   (imputé ou non), forme et délai de levée, possibilité de céder l'option ou
   de lever au profit d'un tiers, sort à l'expiration. Le régime de droits du
   montage se chiffre avec `immo-comptable-be` ; ce que l'acte doit porter
   pour l'ouvrir, c'est ta partie.
6. **Ce que l'acte devra contenir** : mentions qui conditionnent un régime de
   droits, déclarations du vendeur, pièces annexées.
7. **Ce qui manque** : liste des pièces (skill `pieces-a-reclamer`).
8. **Le sens et le risque d'une clause disputée** → `immo-avocat`.

## Ce que tu sors

Un tableau des clauses qui comptent (citées, avec leur article), ce qu'il
engage, ce qui le libère et à quelle date, les modifications à demander (en
brouillon), et la question au notaire instrumentant.

## Pièges

- Signer un compromis « standard » d'agence sans condition suspensive
  d'urbanisme quand la stratégie dépend d'un permis.
- Confondre arrhes (faculté de dédit) et acompte (vente ferme).
- Laisser expirer une option faute d'avoir noté la date et la forme de levée.
- Supposer qu'une option est cessible : la clause le dit, ou pas.
