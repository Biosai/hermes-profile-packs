---
name: analyse-clause
description: "Dire ce qu'une clause signifie, coûte et risque"
metadata:
  hermes:
    config:
      - key: immo.juridictions
        description: "Régions en jeu, ex. BE-WAL,BE-BRU,BE-VLA,FR ; ou detect"
        default: "detect"
---
# Analyse d'une clause

## Quand l'utiliser

Quand une clause décide d'un risque ou d'un coût : condition suspensive,
clause de dédit, garantie exclue, occupation, travaux votés en copropriété,
délai de paiement, pénalité, réception, révision de prix.

## Prérequis

| Besoin | Pourquoi | Vérification |
|---|---|---|
| La pièce complète, pas un extrait (requis) | une clause se lit avec ses définitions | toutes les pages sont là |
| La région ou le pays du bien (requis) | la règle légale en dépend | établi depuis l'adresse |

Si un prérequis requis manque, arrête-toi avant l'étape 1 : dis lequel, ce
qu'il bloque et le plus petit accès qui le débloque (lecture seule d'abord).
Ne fais que les parties qui ont un sens sans lui. Ne remplace jamais une pièce
ou un chiffre non lu par une estimation ; une recherche échouée n'est pas
« rien trouvé ».

## Configuration

- `immo.juridictions` : la règle légale à confronter à la clause. `detect`
  (défaut) : déduis la région de l'adresse du bien, dis-la, fais-la confirmer.

Réglage vide ou `detect` : dis ce que tu as retenu et donne la ligne qui le
fixe, `hermes config set skills.config.<clé> <valeur>` (un seul profil :
`hermes -p <profil> config set …`).

## Étapes

1. **Cite la clause mot pour mot**, avec son article et sa page, et le titre
   de la pièce et sa date.
2. **Lis la pièce entière** autour : définitions, renvois, clauses générales
   qui la complètent ou la contredisent.
3. **Identifie la règle légale** qu'elle applique ou écarte, et si cette règle
   est impérative (la clause qui y déroge est sans effet) ou supplétive (la
   clause prime).
4. **Dis ce qu'elle produit** dans le dossier, en clair : qui paie quoi, quand,
   à quelle condition. Chiffre l'effet en fourchette quand c'est possible, avec
   `immo-associe`.
5. **Cherche ce qui la renverse** : ambiguïté, condition non remplie, clause
   abusive au regard du texte, incompatibilité avec une autre clause.
6. **Distingue négociable et non négociable** : en vente publique, la clause du
   cahier des charges ne se négocie pas, elle se chiffre ; de gré à gré, propose
   une rédaction alternative.
7. **Pour la pratique de l'acte**, consulte `immo-notaire` ; pour l'effet
   fiscal, le comptable du pays.

## Ce que tu sors

La clause citée, sa règle légale (texte, version), ce qu'elle produit, son
coût en fourchette, ce qui pourrait la renverser, et — de gré à gré — une
proposition de rédaction en brouillon. Puis la question pour l'avocat ou le
notaire réel.

## Pièges

- Résumer une clause au lieu de la citer : le mot qui compte disparaît.
- Présumer qu'une règle légale s'applique alors que la clause l'écarte
  valablement.
- Lire une clause isolée de ses définitions.
- Conseiller de signer : tu dis ce qu'elle engage, il décide.
