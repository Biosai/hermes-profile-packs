---
name: consulter-expert
description: "Consulter un autre profil et citer son avis comme le sien"
metadata:
  hermes:
    config:
      - key: immo.fiche_investisseur
        description: "Où vit la fiche investisseur : memory ou un chemin"
        default: "memory"
---
# Consulter un expert de l'équipe

## Quand l'utiliser

Dès qu'une question touche le domaine d'un autre profil (table en fin de
SOUL) — et toujours `immo-avocat` pour une question de droit, même au détour
d'un autre sujet. Ce skill sert à tous les profils, pas seulement au bras
droit.

## Prérequis

| Besoin | Pourquoi | Vérification |
|---|---|---|
| La délégation entre profils de l'hôte (requis) | consulter un autre profil | le profil visé figure parmi les profils installés |
| Le dossier utile (requis) | l'expert n'a rien entendu | bien, région, chiffres et pièces sont dans la question |

Si un prérequis requis manque, arrête-toi avant l'étape 1 : dis lequel, ce
qu'il bloque et le plus petit accès qui le débloque (lecture seule d'abord).
Ne fais que les parties qui ont un sens sans lui. Ne remplace jamais une pièce
ou un chiffre non lu par une estimation ; une recherche échouée n'est pas
« rien trouvé ».

## Configuration

- `immo.fiche_investisseur` : `memory` (défaut) → l'expert ne voit pas la
  fiche : copie les lignes utiles dans la consultation. Un chemin → cite le
  chemin et les lignes ; il les relira.

Réglage vide ou `detect` : dis ce que tu as retenu et donne la ligne qui le
fixe, `hermes config set skills.config.<clé> <valeur>` (un seul profil :
`hermes -p <profil> config set …`).

## Étapes

1. **Choisis le bon profil** : le domaine qui possède la question, pas celui
   qui « saura sans doute ». Droit → avocat ; chiffre fiscal → comptable du
   pays ; acte → notaire ; urbanisme → architecte ; budget travaux →
   conducteur de travaux ; arbitrage → associé. Une question à deux faces
   (droit et fiscalité) se pose aux deux.
2. **Vérifie qu'il est installé** avec les moyens de délégation de l'hôte. Un
   profil nommé dans ce texte n'est pas la preuve qu'il existe ici.
3. **Rédige la consultation** : commence par « [Consultation interne] », puis
   le dossier utile (bien, région, montage, chiffres et leur source, pièces
   citées), la question exacte, et la forme de réponse attendue. Transmets
   les données de la fiche dont il a besoin : il ne les a pas entendues.
4. **Ne transmets que le nécessaire** : pas toute la fiche, pas l'historique.
5. **Lis la réponse en entier**, réserves comprises. Si elle manque d'une
   source ou d'une date, redemande-la plutôt que de la combler.
6. **Cite l'avis comme le sien** : « selon `immo-notaire` : … », ses réserves
   mot pour mot, ses « À VÉRIFIER » conservés.
7. **Deux avis qui divergent se montrent tous les deux**, avec leurs raisons ;
   tu ne tranches pas entre eux.
8. **Échec ou absence** : réponds sans cet avis, et dis-le en une ligne.

## Ce que tu sors

La réponse à l'investisseur, sur quoi elle repose (avis cités, pièces,
sources datées), sans « je lance une consultation » : la tuyauterie ne se
montre pas.

## Pièges

- Répondre de culture générale pour gagner du temps, sur le domaine d'un autre.
- Reformuler un avis jusqu'à en perdre la réserve qui comptait.
- Laisser l'expert questionner l'investisseur : en consultation interne, il
  répond au profil et nomme ce qui manque.
- Annoncer qu'un expert a été consulté quand l'appel a échoué.
