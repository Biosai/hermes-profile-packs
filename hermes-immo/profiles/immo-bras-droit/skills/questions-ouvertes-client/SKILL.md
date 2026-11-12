---
name: questions-ouvertes-client
description: "Choisir la seule question utile à poser à l'investisseur"
metadata:
  hermes:
    config:
      - key: immo.registre_questions
        description: "Où vit le registre des questions et demandes : memory ou un chemin"
        default: "memory"
      - key: owner.channel
        description: "Où les questions atteignent l'investisseur (texte libre)"
        default: "this conversation"
---
# Questions ouvertes à l'investisseur

## Quand l'utiliser

À chaque message de l'investisseur, avant de répondre ; à chaque relance
planifiée ; quand il dit « stop » ; quand il répond, même des jours plus tard, à
une question posée ailleurs.

## Prérequis

| Besoin | Pourquoi | Vérification |
|---|---|---|
| Le registre des questions (requis) | savoir ce qui est ouvert, tranché ou arrêté | sa dernière entrée se lit |
| Une tâche planifiée de l'hôte (pour relancer) | une relance n'existe que si un mécanisme la porte | elle figure parmi les tâches planifiées de l'hôte |
| L'accès à `owner.channel`, si ce n'est pas cette conversation | poser là où il lira | la session peut écrire sur ce canal |

Si un prérequis requis manque, arrête-toi avant l'étape 1 : dis lequel, ce
qu'il bloque et le plus petit accès qui le débloque (lecture seule d'abord).
Ne fais que les parties qui ont un sens sans lui. Ne remplace jamais une pièce
ou un chiffre non lu par une estimation ; une recherche échouée n'est pas
« rien trouvé ».

## Configuration

- `immo.registre_questions` : `memory` (défaut) → la mémoire persistante de ce
  profil, relue avant chaque question ; un chemin → ce fichier, relu et mis à
  jour à chaque réponse. Illisible : aucune question n'est posée.
- `owner.channel` : où la question l'atteint ; défaut, cette conversation. Un
  canal que cette session ne peut pas joindre : prépare la question et dis-le,
  sans la poser ailleurs.

Réglage vide ou `detect` : dis ce que tu as retenu et donne la ligne qui le
fixe, `hermes config set skills.config.<clé> <valeur>` (un seul profil :
`hermes -p <profil> config set …`).

## Étapes

1. **Lis le registre des questions**, pas ton souvenir : ouvertes, répondues,
   tranchées, arrêtées. Une question tranchée ou arrêtée sort du jeu,
   définitivement.
2. **Livre d'abord** ce qu'il demande, en disant sur quoi ça repose. La
   question vient après la réponse, jamais avant.
3. **Choisis une seule question** : celle que son message vient de rendre
   concrète. Il parle d'un immeuble à diviser → la question sur son seuil de
   marge pour une division, pas celle sur la courte durée. Si rien ne rend une
   question concrète, n'en pose pas.
4. **Formule-la pour qu'il réponde en une ligne** : un choix entre deux ou
   trois options chiffrées vaut mieux qu'une question ouverte. Dis ce que sa
   réponse débloque (« avec ce chiffre, le prix plafond devient exact »).
5. **Sa réponse s'enregistre dans la même conversation** (skill
   `capture-donnees-client`) : la question passe à « répondue », avec ses mots,
   la date et le canal.
6. **Relance** : seulement si une tâche planifiée de l'hôte la porte (voir
   Prérequis), par `owner.channel`. Une relance porte une seule question et sa
   référence, pour que sa réponse se rattache sans ambiguïté. Sans tâche
   planifiée, pas de relance, et pas de promesse d'en faire.
7. **Arrêt** : « stop sur ce point » arrête cette question ; « stop rappels »
   les arrête toutes. Enregistre l'arrêt avec ses mots et la date, confirme en
   une ligne, et ne la repose plus, nulle part.

## Ce que tu sors

- Dans la conversation : la réponse, puis au plus une question.
- Dans le registre : chaque question avec son état (ouverte, répondue,
  tranchée, arrêtée), sa source et sa date, et ce qu'elle débloque.

## Pièges

- Deux questions dans un message : il répond à la plus facile, ou à aucune.
- Reposer une question tranchée parce qu'elle « semble ouverte » dans un
  récapitulatif fait de tête. Le registre fait foi.
- Lever un arrêt soi-même parce que la donnée serait utile : seul
  l'investisseur lève un arrêt. Sans la donnée, dis seulement sur quoi repose
  le résultat.
- Transformer une question en « à faire » ou « en attente de toi » dans un
  bilan : c'est la reposer.
- Laisser un expert poser la question lui-même : il nomme la donnée qui
  manque, toi seul la demandes.
