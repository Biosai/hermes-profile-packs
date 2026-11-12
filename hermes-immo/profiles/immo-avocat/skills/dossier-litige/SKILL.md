---
name: dossier-litige
description: "Préparer le dossier d'un litige pour l'avocat réel"
metadata:
  hermes:
    config:
      - key: immo.juridictions
        description: "Régions en jeu, ex. BE-WAL,BE-BRU,BE-VLA,FR ; ou detect"
        default: "detect"
---
# Dossier de litige

## Quand l'utiliser

Un litige naît ou menace : locataire, vendeur, acheteur, copropriété,
entreprise de travaux, client de chantier, administration. Avant de consulter
un avocat, ou pour lui faire gagner du temps s'il est déjà saisi.

## Prérequis

| Besoin | Pourquoi | Vérification |
|---|---|---|
| Les pièces du litige (requis) | chaque fait se prouve | inventaire numéroté, chaque pièce s'ouvre |
| La chronologie de l'investisseur | relier les pièces | ses mots, datés |

Si un prérequis requis manque, arrête-toi avant l'étape 1 : dis lequel, ce
qu'il bloque et le plus petit accès qui le débloque (lecture seule d'abord).
Ne fais que les parties qui ont un sens sans lui. Ne remplace jamais une pièce
ou un chiffre non lu par une estimation ; une recherche échouée n'est pas
« rien trouvé ».

## Configuration

- `immo.juridictions` : désigne le texte, le juge compétent et les délais.
  `detect` (défaut) : région ou pays des faits, dit et confirmé.

Réglage vide ou `detect` : dis ce que tu as retenu et donne la ligne qui le
fixe, `hermes config set skills.config.<clé> <valeur>` (un seul profil :
`hermes -p <profil> config set …`).

## Étapes

1. **Chronologie** : chaque fait, daté, avec la pièce qui le prouve (citée).
   Un fait sans pièce est marqué comme tel.
2. **Pièces** : inventaire numéroté, avec ce qui manque et qui le détient.
   Demande la pièce absente ; ne la reconstitue pas.
3. **Qualification** : quel contrat, quel régime, quelle région, quel juge
   compétent.
4. **Règle et texte** : article, citation, date de version (skill
   `sources-droit-primaire`).
5. **Délais qui courent** : prescription, recours, préavis, mise en demeure ;
   échéance calculée, calcul montré. Le plus proche en tête.
6. **Ce qu'il peut faire seul** (courrier, conciliation, déclaration de
   sinistre) et ce qui exige un avocat ou un huissier.
7. **Les points faibles de sa position**, avec la même rigueur que les forts.
8. **La question exacte** à poser à l'avocat, et ce qu'il faut lui joindre.
9. **Relecture contradictoire** avant de livrer.

## Ce que tu sors

Un dossier en six parties : chronologie, pièces, règle, délais, options,
points faibles. En tête, le délai le plus proche et l'action qu'il impose. En
pied, la question pour l'avocat, et ce qui reste À VÉRIFIER (dont
« jurisprudence non consultée »).

## Pièges

- Prédire qui va gagner : dis ce qui fait pencher, pas l'issue.
- Laisser courir un délai pendant qu'on rassemble les pièces.
- Envoyer une mise en demeure : c'est un brouillon, il l'envoie, ou son
  avocat.
- Citer de la jurisprudence de mémoire pour rassurer.
