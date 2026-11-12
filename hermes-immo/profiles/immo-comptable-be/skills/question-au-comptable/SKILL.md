---
name: question-au-comptable
description: "Rédiger la question au comptable et enregistrer sa réponse"
metadata:
  hermes:
    config:
      - key: immo.fiche_investisseur
        description: "Où vit la fiche investisseur : memory ou un chemin"
        default: "memory"
---
# La question au comptable de l'investisseur

## Quand l'utiliser

Quand un chiffre fiscal reste en options faute de confirmation ; avant un acte
dont le régime dépend d'une qualification ; quand l'investisseur transmet une
réponse de son comptable.

## Prérequis

| Besoin | Pourquoi | Vérification |
|---|---|---|
| La décision à trancher et ses scénarios chiffrés (requis) | une question fermée | les scénarios existent |
| L'accès en écriture à la fiche (pour enregistrer l'écrit) | l'écrit devient règle | la ligne écrite se relit |

Si un prérequis requis manque, arrête-toi avant l'étape 1 : dis lequel, ce
qu'il bloque et le plus petit accès qui le débloque (lecture seule d'abord).
Ne fais que les parties qui ont un sens sans lui. Ne remplace jamais une pièce
ou un chiffre non lu par une estimation ; une recherche échouée n'est pas
« rien trouvé ».

## Configuration

- `immo.fiche_investisseur` : où inscrire l'écrit. En `memory` (défaut),
  confie-le à `immo-bras-droit` ; un chemin → inscris-le toi-même si tu peux y
  écrire.

Réglage vide ou `detect` : dis ce que tu as retenu et donne la ligne qui le
fixe, `hermes config set skills.config.<clé> <valeur>` (un seul profil :
`hermes -p <profil> config set …`).

## Étapes

1. **Isole la décision** : quel choix ou quelle qualification fait changer le
   chiffre (régime de droits, stock ou immobilisation, taux de TVA, taux
   d'impôt, personne physique ou société).
2. **Rédige une question fermée**, une par décision : « Pour l'achat du bien X
   par la société, pouvons-nous satisfaire aux conditions du régime … (texte,
   article, version) : déclaration, garantie, délai de revente ? ».
3. **Joins le contexte minimal** : faits du dossier, montants en fourchette,
   texte et version, les scénarios chiffrés que sa réponse départagera.
4. **Dis ce que chaque réponse change** pour le dossier, en une ligne : il
   saura pourquoi la question compte.
5. **Remets le brouillon à l'investisseur** : c'est lui qui l'envoie, au
   comptable qu'il a choisi.
6. **À réception de l'écrit** : enregistre-le dans la même conversation (ou
   fais-le enregistrer par `immo-bras-droit`), mot pour mot, avec sa date, son
   auteur et sa **portée** — le cas exact qu'il traite.
7. **Applique-le** : l'option tranchée devient la règle, pour ce cas
   seulement ; les autres cas restent en options.

## Ce que tu sors

Un brouillon de question, prêt à envoyer par lui, et après réponse : la
ligne de fiche (écrit cité, auteur, date, portée) et le chiffre recalculé.

## Pièges

- Une question ouverte (« que me conseilles-tu ? ») obtient une réponse
  générale qui ne tranche rien.
- Étendre un écrit au-delà de son cas : une réponse pour la courte durée ne
  vaut pas pour la longue durée.
- Poser la question toi-même à l'investisseur : passe par le bras droit, qui
  tient les questions ouvertes.
- Attendre l'écrit pour livrer : livre en options, il tranche quand il veut.
