---
name: question-urbanisme
description: "Rédiger la question exacte au service urbanisme"
metadata:
  hermes:
    config:
      - key: immo.juridictions
        description: "Régions en jeu, ex. BE-WAL,BE-BRU,BE-VLA,FR ; ou detect"
        default: "detect"
---
# La question au service urbanisme

## Quand l'utiliser

Quand un lot reste « inconnu », qu'une règle communale n'est pas trouvée ou
pas claire, qu'une division ou un changement de destination doit être
confirmé avant une offre.

## Prérequis

| Besoin | Pourquoi | Vérification |
|---|---|---|
| L'adresse et la référence cadastrale (requis) | identifier le bien sans ambiguïté | la parcelle se retrouve sur le portail cadastral |
| Ce qui est déjà su, pièces à l'appui (requis) | la question part de là | permis et règlement cités avec leur date |

Si un prérequis requis manque, arrête-toi avant l'étape 1 : dis lequel, ce
qu'il bloque et le plus petit accès qui le débloque (lecture seule d'abord).
Ne fais que les parties qui ont un sens sans lui. Ne remplace jamais une pièce
ou un chiffre non lu par une estimation ; une recherche échouée n'est pas
« rien trouvé ».

## Configuration

- `immo.juridictions` : décide la langue du courriel (néerlandais en Flandre,
  traduction de travail jointe) et le service compétent. `detect` (défaut) :
  déduis la région de l'adresse du bien, dis-la, fais-la confirmer.

Réglage vide ou `detect` : dis ce que tu as retenu et donne la ligne qui le
fixe, `hermes config set skills.config.<clé> <valeur>` (un seul profil :
`hermes -p <profil> config set …`).

## Étapes

1. **Rassemble l'identification du bien** : adresse, références cadastrales,
   propriétaire actuel si connu, nature de l'opération envisagée.
2. **Dis ce que tu sais déjà**, pièces à l'appui : permis connus (référence,
   date, objet), renseignements urbanistiques reçus, règlement lu (date).
3. **Pose une question fermée, ou deux au plus**, à laquelle la commune peut
   répondre par oui, non ou une référence : « Combien de logements le permis
   du … autorise-t-il ? », « Le règlement communal de division du … s'applique-
   t-il à une parcelle de … ? ».
4. **Demande la pièce, pas l'avis** : une copie du permis, l'extrait du
   registre, la délibération en vigueur.
5. **Indique le délai utile** (date d'enchère, fin d'option), sans menace ni
   pression.
6. **Rédige en brouillon**, dans la langue de la commune (néerlandais en
   Flandre ; traduction de travail jointe pour l'investisseur).
7. **Remets-le à l'investisseur** : c'est lui, ou son architecte, qui
   l'envoie. Note la question dans le dossier pour rattacher la réponse.

## Ce que tu sors

Un brouillon de courriel : objet clair, identification du bien, ce qui est
connu, la question fermée, la pièce demandée, le délai utile. Puis une ligne :
ce que chaque réponse possible change pour le dossier.

## Pièges

- Une question ouverte (« que peut-on faire avec ce bien ? ») obtient une
  réponse générale qui ne tranche rien.
- Révéler la stratégie ou le prix visé : la commune n'en a pas besoin.
- Envoyer soi-même : le courriel est un brouillon, toujours.
- Prendre une réponse orale ou un avis informel pour une autorisation.
