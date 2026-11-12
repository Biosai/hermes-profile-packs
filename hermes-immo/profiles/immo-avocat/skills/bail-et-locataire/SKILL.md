---
name: bail-et-locataire
description: "Traiter une question de bail ou de locataire"
metadata:
  hermes:
    config:
      - key: immo.juridictions
        description: "Régions en jeu, ex. BE-WAL,BE-BRU,BE-VLA,FR ; ou detect"
        default: "detect"
---
# Bail et locataire

## Quand l'utiliser

Un locataire ne paie pas, conteste une date, une indexation, une garantie, un
état des lieux ; l'investisseur veut donner congé, indexer, rédiger un bail ;
un bien acheté est occupé ; une location courte durée, en colocation ou
meublée pour entreprises doit être encadrée.

## Prérequis

| Besoin | Pourquoi | Vérification |
|---|---|---|
| Le bail lui-même (requis) | dates, durée, clauses se citent | le bail complet s'ouvre, signatures comprises |
| L'adresse du bien (requis) | la région désigne le texte | commune connue |
| Les pièces du différend : décompte, courriers, état des lieux | faits datés | chaque pièce se date |

Si un prérequis requis manque, arrête-toi avant l'étape 1 : dis lequel, ce
qu'il bloque et le plus petit accès qui le débloque (lecture seule d'abord).
Ne fais que les parties qui ont un sens sans lui. Ne remplace jamais une pièce
ou un chiffre non lu par une estimation ; une recherche échouée n'est pas
« rien trouvé ».

## Configuration

- `immo.juridictions` : le texte du bail applicable (wallon, flamand,
  bruxellois ; français si FR). `detect` (défaut) : déduis la région de
  l'adresse du bien, dis-la, fais-la confirmer.

Réglage vide ou `detect` : dis ce que tu as retenu et donne la ligne qui le
fixe, `hermes config set skills.config.<clé> <valeur>` (un seul profil :
`hermes -p <profil> config set …`).

## Étapes

1. **Région du bien** : elle désigne le texte (Wallonie, Flandre et Bruxelles
   ont chacune leur législation du bail d'habitation ; le bail commercial suit
   un régime distinct).
2. **Qualifie le bail** : résidence principale ou non, durée, colocation,
   étudiant, meublé, commercial ou mixte. La qualification décide du régime.
3. **Lis le bail** : date de conclusion, date de prise d'effet, durée, loyer,
   indexation, garantie, clauses de congé. Cite mot pour mot, avec l'article.
4. **Lis le texte régional en vigueur** à la date du bail et à celle des
   faits ; lis la disposition transitoire si le bail est ancien.
5. **Pour un congé** : motif, préavis, forme, date de prise de cours,
   indemnité éventuelle et la condition exacte qui la déclenche.
6. **Pour un arriéré** : décompte daté, mise en demeure (brouillon),
   conciliation, juge de paix, sort de la garantie. Dis ce qu'il peut faire
   seul et ce qui exige un avocat ou un huissier.
7. **Pour un bien acheté occupé** : ce que l'acquéreur reprend (bail
   enregistré ou non, date certaine), et comment il peut y mettre fin.
8. **Passe à la relecture contradictoire** (skill `relecture-contradictoire`).

## Ce que tu sors

Les faits datés (bail cité), la règle (texte, article, version), les délais
calculés, les options de l'investisseur avec leur coût et leur risque, un
brouillon de courrier si utile, et la question pour son avocat.

## Pièges

- Appliquer la règle d'une autre région, ou celle d'avant la réforme.
- Confondre la règle et son exception : une indemnité peut n'être due que si
  le motif du congé n'est pas réalisé.
- Expulser ou retenir la garantie sans titre : c'est le juge qui l'autorise.
- Envoyer le courrier : c'est un brouillon, il l'envoie.
