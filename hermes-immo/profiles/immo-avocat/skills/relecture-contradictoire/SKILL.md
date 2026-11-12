---
name: relecture-contradictoire
description: "Attaquer une réponse juridique avant de l'envoyer"
metadata:
  hermes:
    config:
      - key: immo.juridictions
        description: "Régions en jeu, ex. BE-WAL,BE-BRU,BE-VLA,FR ; ou detect"
        default: "detect"
---
# Relecture contradictoire

## Quand l'utiliser

Avant chaque réponse juridique, sans exception, y compris en consultation
interne. Ta première réponse est un brouillon.

## Prérequis

| Besoin | Pourquoi | Vérification |
|---|---|---|
| Le brouillon, les textes et les pièces qu'il cite (requis) | relire, c'est recomparer | chaque texte et chaque pièce s'ouvre |
| L'accès aux sources officielles (requis) | vérifier version et citations | le texte s'ouvre avec sa date de consolidation |

Si un prérequis requis manque, arrête-toi avant l'étape 1 : dis lequel, ce
qu'il bloque et le plus petit accès qui le débloque (lecture seule d'abord).
Ne fais que les parties qui ont un sens sans lui. Ne remplace jamais une pièce
ou un chiffre non lu par une estimation ; une recherche échouée n'est pas
« rien trouvé ».

## Configuration

- `immo.juridictions` : la région à vérifier en premier. `detect` (défaut) :
  déduis la région de l'adresse du bien, dis-la, fais-la confirmer. Un bien
  hors liste : relève-le.

Réglage vide ou `detect` : dis ce que tu as retenu et donne la ligne qui le
fixe, `hermes config set skills.config.<clé> <valeur>` (un seul profil :
`hermes -p <profil> config set …`).

## Étapes

1. **Le texte existe-t-il, et est-ce le bon ?** La région du bien ; la date de
   conclusion du bail ou du contrat, qui peut le faire tomber sous un régime
   antérieur — lis la disposition transitoire ; la date de version du texte
   que tu as lu. Des régimes cités de mémoire se sont déjà révélés
   inexistants.
2. **As-tu lu tout l'article ?** L'alinéa suivant, l'exception, l'incise, le
   renvoi. La phrase qui suit une règle dit souvent quand elle ne s'applique
   pas, ou permet aux parties d'y déroger.
3. **La règle est-elle impérative ou supplétive ?** Une règle peut être
   impérative sur un point et supplétive sur un autre ; une règle supplétive
   cède devant la clause : lis la pièce.
4. **Qu'est-ce qui renverse ta conclusion ?** Une clause qui déroge, une
   condition de forme non remplie (écrit, recommandé, délai, mentions
   obligatoires), un texte plus récent, la position de l'autre partie.
   Cherche-le, et dis ce que tu as trouvé.
5. **Chaque délai est recalculé** : point de départ, mode de notification,
   jours ouvrables ou calendrier, report d'échéance. Montre le calcul.
6. **Chaque citation est recomparée** au texte ouvert, mot pour mot. Une
   citation qui ne correspond pas se recopie, elle ne se reformule pas.
7. **Chaque pièce citée est relue** : date, montant, clause, page.
8. **Ce qui ne survit pas** sort marqué **À VÉRIFIER**, avec ce qu'il faudrait
   lire pour le lever.

## Ce que tu sors

La réponse corrigée, et en pied une ligne : ce que la relecture a changé (ou
« relecture sans changement »), et la liste des points À VÉRIFIER.

## Pièges

- Relire pour confirmer plutôt que pour réfuter : cherche ce qui te donne
  tort.
- Considérer qu'une source officieuse (consolidation, synthèse) fait foi sur
  un point qui décide d'un litige : remonte à la publication officielle.
- Laisser passer un délai calculé de tête parce que « c'est un mois ».
- Combler un vide par la jurisprudence de mémoire.
