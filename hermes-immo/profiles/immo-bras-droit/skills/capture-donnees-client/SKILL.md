---
name: capture-donnees-client
description: "Enregistrer chiffres, réponses et règles de l'investisseur"
metadata:
  hermes:
    config:
      - key: immo.fiche_investisseur
        description: "Où vit la fiche investisseur : memory ou un chemin"
        default: "memory"
      - key: immo.registre_questions
        description: "Où vit le registre des questions et demandes : memory ou un chemin"
        default: "memory"
---
# Capture des données de l'investisseur

## Quand l'utiliser

Dès qu'il donne un chiffre (coût de chantier, loyer obtenu, prix payé), répond
à une question, tranche un arbitrage ou dicte une règle ; au premier échange,
pour établir sa fiche ; quand il transmet un écrit de son comptable, de son
notaire ou de son avocat.

## Prérequis

| Besoin | Pourquoi | Vérification |
|---|---|---|
| Un accès en écriture à la fiche (requis) | rien ne s'enregistre sinon | la ligne écrite se relit |
| Ses mots, ou la pièce (requis) | chaque ligne porte sa source | le message ou la pièce se cite |

Si un prérequis requis manque, arrête-toi avant l'étape 1 : dis lequel, ce
qu'il bloque et le plus petit accès qui le débloque (lecture seule d'abord).
Ne fais que les parties qui ont un sens sans lui. Ne remplace jamais une pièce
ou un chiffre non lu par une estimation ; une recherche échouée n'est pas
« rien trouvé ».

## Configuration

- `immo.fiche_investisseur` : `memory` (défaut) → la mémoire persistante de ce
  profil ; les experts ne la voient pas, transmets-leur les lignes utiles. Un
  chemin → ce fichier, que chaque profil peut lire.
- `immo.registre_questions` : où passer à « répondue » la question que la
  donnée tranche ; mêmes valeurs.

Réglage vide ou `detect` : dis ce que tu as retenu et donne la ligne qui le
fixe, `hermes config set skills.config.<clé> <valeur>` (un seul profil :
`hermes -p <profil> config set …`).

## La fiche investisseur : ce qu'il faut établir

- Sa société (forme, activité déclarée), son rôle, ses pays et régions.
- **S'il réalise les travaux lui-même** ou par sa propre entreprise, lesquels,
  et à quel prix de revient (matériaux, main-d'œuvre). Tant que ce n'est pas
  établi, la ligne travaux est une estimation d'entreprise.
- Ses stratégies admises et refusées, éventuellement par zone.
- Ses seuils : marge minimale par type d'opération, rendement minimal d'un lot
  conservé, budget, durée de portage acceptée.
- Ses paramètres de scénario (décote de revente, dépassement de travaux,
  durée) et ses règles de prix (décote d'entrée, prime de revente).
- Le régime de droits qu'il veut voir appliqué par défaut ; comment il veut
  voir l'impôt des sociétés (par projet ou en fin d'exercice).
- Son objectif chiffré, cité comme son objectif.
- Les écrits de ses conseillers, chacun limité au cas qu'il traite.

## Étapes

1. **Enregistre dans la même conversation**, pas « plus tard », là où
   `immo.fiche_investisseur` la place : ce qui n'est pas écrit est perdu, et
   les autres profils ne l'entendront jamais.
2. **Chaque ligne porte sa source** : qui, quand, quel canal, ses mots entre
   guillemets. Un chiffre sans date de relevé est un chiffre faux en
   puissance.
3. **Distingue le statut** : règle inscrite, chiffre mesuré (chantier réel,
   facture), estimation de sa part, simple évocation. Une évocation ne devient
   règle qu'après sa confirmation.
4. **Si la donnée répond à une question ouverte**, passe la question à
   « répondue » (skill `questions-ouvertes-client`).
5. **Dis ce que la donnée change** : quel calcul elle rend exact, quelle
   option elle tranche. Informe l'expert concerné à la prochaine consultation.
6. **Confirme en une ligne** ce qui est noté, sans relire toute la fiche.

## Ce que tu sors

Une ligne de fiche par donnée : valeur, unité, statut, source citée, date,
portée (quel type d'opération elle couvre).

## Pièges

- Généraliser un écrit : la réponse de son comptable sur la courte durée ne
  vaut pas pour la longue durée.
- Écraser une donnée ancienne sans garder la trace : remplace-la, en gardant
  l'ancienne valeur et sa date.
- Inscrire comme règle ce qu'il a dit une fois en passant.
- Supposer qu'il fait les travaux parce qu'il est du métier : demande-le, une
  fois, au moment où un dossier le rend concret.
