---
name: strategies-sur-un-bien
description: "Tester toutes les stratégies sur un bien avant d'écarter"
metadata:
  hermes:
    config:
      - key: immo.fiche_investisseur
        description: "Où vit la fiche investisseur : memory ou un chemin"
        default: "memory"
      - key: immo.juridictions
        description: "Régions en jeu, ex. BE-WAL,BE-BRU,BE-VLA,FR ; ou detect"
        default: "detect"
---
# Toutes les stratégies sur un bien

## Quand l'utiliser

Dès qu'un bien concret arrive (annonce, vente publique, offre d'un vendeur,
immeuble qu'il détient déjà) et qu'il faut décider quoi en faire.

## Prérequis

| Besoin | Pourquoi | Vérification |
|---|---|---|
| Les faits du bien : adresse, prix, surface, avec leur source (requis) | rien ne se chiffre sans eux | chaque fait a sa source |
| La fiche investisseur (requis pour écarter sur un seuil) | stratégies admises, seuils, zones | la fiche se lit ; sinon rien ne s'écarte sur un seuil, et tu le dis |
| Les avis architecte, travaux, comptable | lots reconnus, budget, frais | leurs réponses sont citées |

Si un prérequis requis manque, arrête-toi avant l'étape 1 : dis lequel, ce
qu'il bloque et le plus petit accès qui le débloque (lecture seule d'abord).
Ne fais que les parties qui ont un sens sans lui. Ne remplace jamais une pièce
ou un chiffre non lu par une estimation ; une recherche échouée n'est pas
« rien trouvé ».

## Configuration

- `immo.fiche_investisseur` : en `memory` (défaut), demande à
  `immo-bras-droit` seuils, zones et stratégies admises ; un chemin → lis-les.
- `immo.juridictions` : une stratégie qui exige une région hors liste se
  signale. `detect` (défaut) : déduis la région de l'adresse du bien, dis-la,
  fais-la confirmer.

Réglage vide ou `detect` : dis ce que tu as retenu et donne la ligne qui le
fixe, `hermes config set skills.config.<clé> <valeur>` (un seul profil :
`hermes -p <profil> config set …`).

## Étapes

1. **Lis sa fiche** : stratégies admises ou refusées, par zone ; seuils ;
   paramètres de scénario ; s'il fait les travaux.
2. **Établis les faits du bien** : région, type, surface (source), nombre de
   lots annoncés et reconnus (`immo-architecte`), état (`immo-conducteur-
   travaux`), occupation, copropriété (`immo-notaire`). Ce qui manque se nomme.
3. **Liste toutes les stratégies plausibles** avant d'en écarter une :
   - option sur tous les lots ; option partielle + achat du reste ;
   - achat, division, revente totale ou partielle avec lots conservés ;
   - revente en l'état, rafraîchie, rénovée ;
   - location longue durée, colocation, courte durée, meublé pour entreprises ;
   - découpe de terrain, de garages, de volumes ; combinaisons.
4. **Écarte avec une raison écrite** : hors zone selon sa fiche, impossible
   (lot non reconnu, courte durée interdite), ou marge sous son seuil après
   calcul. « Ça ne me paraît pas intéressant » n'est pas une raison.
5. **Chiffre chaque stratégie retenue** en fourchette : prix d'entrée, frais
   d'acquisition (scénarios de `immo-comptable-be`), travaux par niveau
   (`immo-conducteur-travaux`), portage, prix de sortie ou loyers
   (comparables), frais de sortie.
6. **Passe-les aux trois scénarios** (skill `trois-scenarios`).
7. **Classe** : la meilleure en tête, celle qui tient en sécurité marquée.

## Ce que tu sors

Un tableau des stratégies : bénéfice (fourchette), marge sur prix d'achat,
apport immobilisé, rendement de l'apport, durée, tient en sécurité (oui/non),
et les stratégies écartées avec leur raison. En pied : coût des travaux, base
de comparables, régime fiscal d'acquisition.

## Pièges

- Écarter un immeuble sur la seule revente globale sans avoir testé la
  division ou la revente partielle.
- Mélanger les régimes : le locatif se juge en cash-flow et rendement, pas en
  prix plafond de revente.
- Appliquer les frais d'acquisition au prix total d'un montage dont une partie
  passe sous option.
- Proposer une stratégie que sa fiche réserve à une autre zone : signale-la.
