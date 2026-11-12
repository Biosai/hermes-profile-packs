---
name: trois-scenarios
description: "Passer une stratégie en trois scénarios et prix plafond"
metadata:
  hermes:
    config:
      - key: immo.fiche_investisseur
        description: "Où vit la fiche investisseur : memory ou un chemin"
        default: "memory"
---
# Trois scénarios et prix plafond

## Quand l'utiliser

Pour toute stratégie chiffrée avant une offre, une enchère ou une levée
d'option ; quand l'investisseur demande « jusqu'où je peux monter ? ».

## Prérequis

| Besoin | Pourquoi | Vérification |
|---|---|---|
| Le budget travaux par niveau (requis) | travaux de chaque scénario | l'avis de `immo-conducteur-travaux` est cité |
| La valeur de sortie en fourchette (requis) | prix de sortie | comparables nommés, effectif |
| Les paramètres de scénario (fiche, sinon proposés) | décote, dépassement, durée | la fiche les donne, ou ils sont confirmés |

Si un prérequis requis manque, arrête-toi avant l'étape 1 : dis lequel, ce
qu'il bloque et le plus petit accès qui le débloque (lecture seule d'abord).
Ne fais que les parties qui ont un sens sans lui. Ne remplace jamais une pièce
ou un chiffre non lu par une estimation ; une recherche échouée n'est pas
« rien trouvé ».

## Configuration

- `immo.fiche_investisseur` : paramètres de scénario et marges minimales. En
  `memory` (défaut), demande-les à `immo-bras-droit` ; absents, propose-les,
  marqués « à confirmer ».

Réglage vide ou `detect` : dis ce que tu as retenu et donne la ligne qui le
fixe, `hermes config set skills.config.<clé> <valeur>` (un seul profil :
`hermes -p <profil> config set …`).

## Étapes

1. **Prends les paramètres de sa fiche** : décote de revente, dépassement de
   travaux, durée de chaque scénario, marge minimale par type d'opération.
   S'ils n'y sont pas, propose-en, dis lesquels tu as pris, et fais-les
   confirmer par le bras droit.
2. **Optimiste** : sortie au prix de marché (comparables), durée courte,
   travaux au bas de la fourchette.
3. **Réaliste** : sortie sous le marché, durée allongée, travaux au milieu.
4. **Sécurité** : sortie nettement sous le marché, travaux en dépassement,
   durée doublée, frais de portage en conséquence.
5. **Calcule le prix plafond** : prix de sortie − frais de sortie − travaux −
   portage − marge minimale − frais d'acquisition (qui dépendent eux-mêmes du
   prix : résous-le, ne l'approxime pas).
6. **Refais le calcul à l'envers** : du prix plafond, retrouve la marge. Si
   tu ne la retrouves pas, le calcul est faux.
7. **Nomme l'hypothèse qui fait tout basculer** : de combien doit-elle bouger
   pour que le scénario sécurité passe sous le seuil ?

## Ce que tu sors

Pour chaque stratégie : un tableau à trois colonnes (optimiste, réaliste,
sécurité) — prix de sortie, travaux, portage, frais, bénéfice, marge, durée —,
le prix plafond, la vérification à l'envers, et l'hypothèse sensible avec son
seuil de bascule. Verdict : tient ou ne tient pas en sécurité.

## Pièges

- Un prix plafond sans ses trois hypothèses (travaux, comparables, régime
  fiscal) n'est pas auditable.
- Calculer les droits sur le prix annoncé puis enchérir au-delà : les frais
  suivent le prix.
- Un scénario sécurité qui n'est qu'un réaliste un peu moins bon : il doit
  pouvoir arriver, pas seulement déplaire.
- Promettre le scénario optimiste : c'est une borne, pas une prévision.
