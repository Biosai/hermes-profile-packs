---
name: tva-immobilier
description: "Dire quel régime de TVA belge s'applique à l'opération"
metadata:
  hermes:
    config:
      - key: immo.fiche_investisseur
        description: "Où vit la fiche investisseur : memory ou un chemin"
        default: "memory"
---
# TVA immobilière (Belgique)

## Quand l'utiliser

Quand un budget travaux doit être chiffré TVA comprise ; quand on vend ou
achète un bâtiment neuf ; quand une location inclut des services ; quand
l'investisseur envisage de démolir et reconstruire.

## Prérequis

| Besoin | Pourquoi | Vérification |
|---|---|---|
| L'opération et l'usage après travaux (requis) | le régime en dépend | décrits par écrit |
| L'âge du bâtiment (requis pour un taux réduit) | condition du taux réduit | une pièce date la première occupation |
| L'accès au code de la TVA et aux arrêtés (requis) | aucun taux de mémoire | le texte s'ouvre avec sa date |

Si un prérequis requis manque, arrête-toi avant l'étape 1 : dis lequel, ce
qu'il bloque et le plus petit accès qui le débloque (lecture seule d'abord).
Ne fais que les parties qui ont un sens sans lui. Ne remplace jamais une pièce
ou un chiffre non lu par une estimation ; une recherche échouée n'est pas
« rien trouvé ».

## Configuration

- `immo.fiche_investisseur` : s'il fait les travaux par sa propre entreprise,
  et les écrits de son comptable, chacun limité à son cas. En `memory`
  (défaut), demande-les à `immo-bras-droit`.

Réglage vide ou `detect` : dis ce que tu as retenu et donne la ligne qui le
fixe, `hermes config set skills.config.<clé> <valeur>` (un seul profil :
`hermes -p <profil> config set …`).

## Étapes

1. **Qualifie l'opération** : travaux immobiliers (rénovation,
   transformation, construction), vente d'un bâtiment neuf (au sens TVA),
   démolition-reconstruction, location (exemptée en principe) ou hébergement
   avec services.
2. **Qualifie le bien et l'usage** : logement privé ou non, âge du bâtiment
   depuis sa première occupation, destinataire final, usage après travaux
   (habitation, location de courte durée, usage professionnel).
3. **Lis le code de la TVA et ses arrêtés en vigueur** (SPF Finances), avec
   la date de version : taux normal, taux réduits et leurs conditions
   cumulatives (âge, usage, attestation du client, facturation directe au
   destinataire), régimes temporaires et leur échéance.
4. **Vérifie qui facture à qui** : si l'investisseur réalise les travaux
   par sa propre entreprise, la facturation entre ses sociétés a ses propres
   règles ; si une entreprise tierce facture, l'attestation du client
   conditionne souvent le taux réduit.
5. **Pour la vente d'un bâtiment neuf**, dis si la vente est soumise à TVA (et
   non aux droits d'enregistrement) et ce que cela change pour l'acquéreur.
6. **Chiffre** l'effet sur le budget de `immo-conducteur-travaux` : un
   scénario par taux possible tant que les conditions ne sont pas établies.

## Ce que tu sors

Régime retenu ou scénarios, texte (article, version), conditions et preuves à
réunir (attestation, âge du bâtiment, usage), effet en fourchette sur le
budget ou le prix, et la question pour son comptable.

## Pièges

- Appliquer un taux réduit à un usage qui l'exclut : un changement d'usage
  après travaux peut faire perdre le taux.
- Étendre la réponse écrite de son comptable sur un usage à un autre usage.
- Oublier qu'un régime temporaire a une date de fin : lis-la.
- Confondre TVA sur la vente d'un neuf et droits d'enregistrement : c'est
  l'un ou l'autre, selon la qualification, à établir.
