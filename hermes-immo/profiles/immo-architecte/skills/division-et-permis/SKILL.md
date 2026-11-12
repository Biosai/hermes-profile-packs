---
name: division-et-permis
description: "Dire ce qu'il faut pour diviser ou créer un logement"
metadata:
  hermes:
    config:
      - key: immo.juridictions
        description: "Régions en jeu, ex. BE-WAL,BE-BRU,BE-VLA,FR ; ou detect"
        default: "detect"
---
# Division et permis

## Quand l'utiliser

Quand une stratégie suppose de créer une unité, de diviser un immeuble, de
changer une destination (commerce en logement, grenier en studio), de découper
un terrain, ou de régulariser un logement non reconnu.

## Prérequis

| Besoin | Pourquoi | Vérification |
|---|---|---|
| L'adresse et la parcelle (requis) | affectation, règlement communal | la parcelle se retrouve sur le géoportail officiel |
| L'accès au code régional et au règlement communal (requis) | la règle se lit, elle ne se suppose pas | le texte s'ouvre avec sa date de version |
| Un compte sur un portail régional (optionnel) | certaines couches exigent une connexion | la connexion aboutit |

Si un prérequis requis manque, arrête-toi avant l'étape 1 : dis lequel, ce
qu'il bloque et le plus petit accès qui le débloque (lecture seule d'abord).
Ne fais que les parties qui ont un sens sans lui. Ne remplace jamais une pièce
ou un chiffre non lu par une estimation ; une recherche échouée n'est pas
« rien trouvé ».

## Configuration

- `immo.juridictions` : choisit le code (Wallonie, Flandre, Bruxelles, France)
  et la langue du règlement. `detect` (défaut) : déduis la région de l'adresse
  du bien, dis-la, fais-la confirmer.

Réglage vide ou `detect` : dis ce que tu as retenu et donne la ligne qui le
fixe, `hermes config set skills.config.<clé> <valeur>` (un seul profil :
`hermes -p <profil> config set …`).

## Étapes

1. **Région, commune, parcelle** : établis-les. Lis l'affectation au plan
   régional (plan de secteur en Wallonie, plans régionaux à Bruxelles,
   plans d'exécution spatiale en Flandre ; PLU en France) sur le géoportail
   officiel.
2. **Qualifie l'acte** : création de logement, division, changement de
   destination, modification du nombre d'unités, travaux structurels,
   lotissement ou urbanisation. Chaque qualification a son régime.
3. **Lis le code régional en vigueur** sur la source officielle, avec sa date
   de version : l'acte est-il soumis à permis, dispensé, soumis à déclaration ?
4. **Cherche les règles communales** : règlement de division, taille minimale
   des unités, nombre maximal d'unités, stationnement, charges d'urbanisme.
   En Flandre, ce règlement est souvent le vrai filtre. Note la date de la
   délibération ; une FAQ municipale n'est pas le règlement.
5. **Vérifie les conditions techniques** qui conditionnent un logement séparé :
   sécurité incendie, salubrité, surfaces et hauteurs minimales, éclairage
   naturel, accès indépendant.
6. **Estime le délai** en fourchette (constitution du dossier, instruction,
   recours possibles) et le risque de refus, avec ce qui le fonde.
7. **Passe le relais** : coût des travaux exigés à `immo-conducteur-travaux`,
   intérêt de l'opération à `immo-associe`, effets juridiques d'une infraction
   existante à `immo-avocat`.

## Ce que tu sors

Pour chaque unité visée : autorisation requise (texte, article, version),
règles communales applicables (règlement, date), conditions techniques,
délai et risque en fourchette, ce qui reste **À VÉRIFIER**, et la question à
poser à la commune (skill `question-urbanisme`).

## Pièges

- Appliquer la règle d'une commune voisine, ou celle d'il y a deux ans.
- Confondre dispense de permis et absence de règle : un acte dispensé reste
  soumis aux normes.
- Oublier que le délai d'un permis est une durée de portage : il pèse sur la
  marge autant qu'un coût.
- Promettre une régularisation : seule l'autorité la délivre.
