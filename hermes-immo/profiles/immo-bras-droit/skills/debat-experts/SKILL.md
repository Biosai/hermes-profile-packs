---
name: debat-experts
description: "Organiser un débat contradictoire entre experts"
metadata:
  hermes:
    config:
      - key: immo.fiche_investisseur
        description: "Où vit la fiche investisseur : memory ou un chemin"
        default: "memory"
      - key: owner.channel
        description: "Où les questions atteignent l'investisseur (texte libre)"
        default: "this conversation"
---
# Débat d'experts

## Quand l'utiliser

Avant une offre ou une enchère ; quand deux avis divergent ; quand
l'investisseur demande « qu'en pensent-ils tous ? » ; en revue périodique des
dossiers ouverts, si une tâche planifiée la porte.

## Prérequis

| Besoin | Pourquoi | Vérification |
|---|---|---|
| La délégation et au moins deux experts installés (requis) | un débat a besoin de voix | les profils visés figurent parmi les profils installés |
| Le dossier : bien, région, prix, pièces (requis) | tous répondent au même dossier | chaque donnée a sa source |

Si un prérequis requis manque, arrête-toi avant l'étape 1 : dis lequel, ce
qu'il bloque et le plus petit accès qui le débloque (lecture seule d'abord).
Ne fais que les parties qui ont un sens sans lui. Ne remplace jamais une pièce
ou un chiffre non lu par une estimation ; une recherche échouée n'est pas
« rien trouvé ».

## Configuration

- `immo.fiche_investisseur` : d'où tirer seuils et paramètres ; en `memory`
  (défaut), copie-les dans la question commune.
- `owner.channel` : où part la synthèse d'une revue périodique ; défaut, cette
  conversation. Sans tâche planifiée, pas de revue périodique.

Réglage vide ou `detect` : dis ce que tu as retenu et donne la ligne qui le
fixe, `hermes config set skills.config.<clé> <valeur>` (un seul profil :
`hermes -p <profil> config set …`).

## Étapes

1. **Pose le dossier une fois, pour tous** : bien, région, prix, montage
   envisagé, données de la fiche utiles, pièces disponibles et leurs dates,
   ce qui manque.
2. **Choisis les voix** : `immo-associe` pour l'arbitrage, et chaque expert
   dont le domaine peut faire tomber le dossier (logements reconnus, clause du
   cahier, régime de droits, budget travaux, bail en cours).
3. **Premier tour** : chaque expert répond à la même question, dans son
   domaine — sa position, ses chiffres en fourchette, l'hypothèse faible, ce
   qu'il n'a pas vérifié.
4. **Deuxième tour, contradictoire** : chaque position est soumise aux autres
   (« qu'est-ce qui, dans ton domaine, renverse cette conclusion ? »).
   `immo-associe` tient le rôle de l'associé sceptique.
5. **Recalcule** ce qui doit l'être : un expert qui change une hypothèse
   (budget, régime, nombre de lots) change le prix plafond ; refais-le à
   l'envers.
6. **Synthétise** sans ajouter ta propre position.

## Ce que tu sors

- Ce qui fait consensus, avec les chiffres en fourchette.
- Ce qui diverge : les deux positions citées, leurs raisons, et la donnée ou
  la pièce qui départagerait.
- Ce qui rend une stratégie impossible (et non risquée), s'il y en a.
- L'hypothèse la plus faible du dossier.
- La prochaine action, son porteur, et au plus une question pour lui.

## Pièges

- Un débat où chacun répond à une question différente : pose la même.
- Une synthèse qui lisse la divergence en moyenne : deux avis contraires ne
  font pas un avis tiède.
- Trancher toi-même : l'arbitrage est à lui.
- Relancer le débat sur un arbitrage qu'il a déjà rendu : il s'applique.
