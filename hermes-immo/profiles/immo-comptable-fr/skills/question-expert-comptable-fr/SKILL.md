---
name: question-expert-comptable-fr
description: "Rédiger la question pour un expert-comptable français"
metadata:
  hermes:
    config:
      - key: immo.fiche_investisseur
        description: "Où vit la fiche investisseur : memory ou un chemin"
        default: "memory"
---
# La question à l'expert-comptable français

## Quand l'utiliser

Avant toute opération française dont un chiffre fiscal reste À VÉRIFIER ;
quand l'investisseur demande à qui s'adresser en France et quoi lui demander.

## Prérequis

| Besoin | Pourquoi | Vérification |
|---|---|---|
| Les décisions à trancher et leurs scénarios (requis) | des questions fermées | les scénarios existent |
| L'avis de `immo-comptable-be` sur la moitié belge | l'expert français ne la traitera pas | son avis est cité |

Si un prérequis requis manque, arrête-toi avant l'étape 1 : dis lequel, ce
qu'il bloque et le plus petit accès qui le débloque (lecture seule d'abord).
Ne fais que les parties qui ont un sens sans lui. Ne remplace jamais une pièce
ou un chiffre non lu par une estimation ; une recherche échouée n'est pas
« rien trouvé ».

## Configuration

- `immo.fiche_investisseur` : où la réponse écrite sera inscrite — par
  `immo-bras-droit` en `memory` (défaut), dans le fichier si c'est un chemin.

Réglage vide ou `detect` : dis ce que tu as retenu et donne la ligne qui le
fixe, `hermes config set skills.config.<clé> <valeur>` (un seul profil :
`hermes -p <profil> config set …`).

## Étapes

1. **Isole les décisions** qui changent le chiffre : structure acheteuse,
   régime de droits, régime de TVA, établissement stable, exonération de la
   taxe annuelle, régime locatif.
2. **Rédige une question fermée par décision**, avec le texte visé (article
   du CGI, série BOFiP) et les scénarios chiffrés que la réponse départagera.
3. **Ajoute la dimension belge** : demande s'il a l'habitude des sociétés
   belges et de la convention franco-belge ; joins l'avis de
   `immo-comptable-be` sur la moitié belge.
4. **Liste les pièces à joindre** : statuts et extrait de la société, projet
   de compromis ou de promesse, descriptif du bien, plan de financement.
5. **Remets le brouillon à l'investisseur** ; c'est lui qui l'envoie.
6. **À réception de la réponse écrite** : fais-la enregistrer par
   `immo-bras-droit`, mot pour mot, avec date, auteur et portée, et recalcule
   le chiffre en remplaçant le scénario par la règle confirmée.

## Ce que tu sors

Un brouillon de courriel : contexte minimal, questions fermées numérotées
avec leur texte de référence, scénarios chiffrés, pièces jointes listées.
Après réponse : la ligne de fiche et le chiffre recalculé.

## Pièges

- Une question qui demande « un avis global » : la réponse sera générale et ne
  tranchera rien.
- Oublier la moitié belge : l'expert français n'y répondra pas de lui-même.
- Étendre sa réponse à une autre opération que celle qu'elle traite.
- Retenir un chiffre fiscal français avant son écrit : tant qu'il manque, le
  chiffre reste en scénarios.
