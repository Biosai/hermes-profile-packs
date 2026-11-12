---
name: suivi-demandes-client
description: "Tenir l'état des demandes de l'investisseur, lu à la source"
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
# Suivi des demandes de l'investisseur

## Quand l'utiliser

Quand il confie une tâche (« analyse ce bien », « prépare le courrier au
syndic », « compare ces trois immeubles ») ; quand il demande où en est une
chose ; pour un bilan périodique, s'il en a demandé un.

## Prérequis

| Besoin | Pourquoi | Vérification |
|---|---|---|
| Le registre (requis) | les demandes y ont leur section | la section « demandes » se lit |
| L'accès aux livrables (requis pour dire « livré ») | un état se prouve | le livrable cité s'ouvre |

Si un prérequis requis manque, arrête-toi avant l'étape 1 : dis lequel, ce
qu'il bloque et le plus petit accès qui le débloque (lecture seule d'abord).
Ne fais que les parties qui ont un sens sans lui. Ne remplace jamais une pièce
ou un chiffre non lu par une estimation ; une recherche échouée n'est pas
« rien trouvé ».

## Configuration

- `immo.registre_questions` : les demandes y ont une section à part. `memory`
  (défaut) → la mémoire persistante de ce profil ; un chemin → ce fichier.
- `owner.channel` : où part un bilan périodique, s'il en a demandé un et
  qu'une tâche planifiée le porte ; sinon l'état se donne ici, à sa demande.

Réglage vide ou `detect` : dis ce que tu as retenu et donne la ligne qui le
fixe, `hermes config set skills.config.<clé> <valeur>` (un seul profil :
`hermes -p <profil> config set …`).

## Étapes

1. **À la demande, inscris-la** dans la section « demandes » du registre :
   ses mots, la date, ce qui est attendu (livrable, format), le profil qui la
   porte, et la condition de fin.
2. **Découpe si besoin** : une demande qui mobilise plusieurs experts garde
   une seule ligne chez toi, avec les sous-tâches et leur porteur.
3. **Pour donner un état, relis la source au moment d'écrire** : le
   livrable existe-t-il, a-t-il été relu, envoyé en brouillon, validé par lui ?
   N'écris « fait » que sur la preuve que c'est fait.
4. **Classe** : livré, en cours (avec la prochaine action et son porteur),
   bloqué (avec la donnée ou la pièce qui manque, et qui la détient), abandonné
   à sa demande.
5. **Une demande bloquée par une question tranchée n'est pas bloquée** : la
   réponse existe, applique-la.
6. **Ferme** une demande quand il a reçu le livrable relu ; garde la trace.

## Ce que tu sors

Un état court, une ligne par demande : sa demande (ses mots), état, preuve
(lien, pièce, date de livraison), prochaine action et porteur. En tête, ce
qui attend une décision de sa part — sans y mettre une seule question déjà
tranchée.

## Pièges

- Composer l'état de tête : on annonce « en cours » ce qui est livré depuis
  longtemps, et « en attente de toi » ce qu'il a tranché.
- Présenter comme fait un brouillon non relu, ou comme envoyé un brouillon
  qu'il n'a pas envoyé lui-même.
- Laisser une demande sans porteur : elle meurt sans bruit.
- Noyer l'état dans le détail : il veut savoir ce qui avance, ce qui bloque, et
  ce qu'on attend de lui.
